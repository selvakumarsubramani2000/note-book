# 🧪 Unit Testing — Fast Safety Nets for Backend Logic

> **Trainer's Note:** Backend confidence does not come from “it worked in Swagger once.” It comes from **automated tests** that re-check behavior every time you change code. This file starts with **unit tests**: small, fast checks of business logic with **no real database**.

---

## 📑 Table of Contents
1. [Why Automated Tests Matter](#1-why-automated-tests-matter)
2. [Test Frameworks: xUnit, NUnit, MSTest](#2-test-frameworks-xunit-nunit-mstest)
3. [Why This Notebook Chooses xUnit](#3-why-this-notebook-chooses-xunit)
4. [Create a Unit Test Project](#4-create-a-unit-test-project)
5. [Arrange–Act–Assert (AAA)](#5-arrangeactassert-aaa)
6. [Facts and Theories](#6-facts-and-theories)
7. [Testing Service / Business Logic in Isolation](#7-testing-service--business-logic-in-isolation)
8. [Domain Logic Without a Database](#8-domain-logic-without-a-database)
9. [Naming, Structure, and Good Habits](#9-naming-structure-and-good-habits)
10. [Running Tests](#10-running-tests)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. Why Automated Tests Matter

Manual testing does not scale. APIs grow. Teams change. Bugs return.

| Benefit | What it means for .NET backends |
|---------|----------------------------------|
| **Regression safety** | Old order/login rules still pass after a new feature |
| **Faster refactors** | Rename services / extract classes without fear |
| **Living documentation** | Tests show how `ProductService` is supposed to behave |
| **Better design** | Hard-to-test code often means tight coupling |
| **CI gate** | Pull requests fail before bad code reaches main |

```
Without tests:
  change pricing → click Swagger → “seems fine” → production surprise

With tests:
  change pricing → dotnet test → red/green in seconds
```

### What unit tests are (and are not)

| Unit tests **are** | Unit tests are **not** |
|--------------------|------------------------|
| Fast (ms) | Full browser flows |
| Focused on one unit of behavior | Replacing manual exploratory testing |
| Isolated from SQL/network | Proof the whole system is deployed correctly |
| Run on every commit | A reason to skip code review |

---

## 2. Test Frameworks: xUnit, NUnit, MSTest

.NET has three mainstream unit test frameworks. All can test the same C# code.

| Framework | Flavor | Common attributes | Notes |
|-----------|--------|-------------------|-------|
| **xUnit** | Modern default for many new .NET projects | `[Fact]`, `[Theory]` | Clean design; new instance per test by default |
| **NUnit** | Very popular, long history | `[Test]`, `[TestCase]` | Rich assertions ecosystem; familiar to many teams |
| **MSTest** | Microsoft “in the box” style | `[TestMethod]`, `[DataRow]` | Common in older VS enterprise solutions |

### Side-by-side sketch

```csharp
// xUnit
[Fact]
public void Add_Works() => Assert.Equal(5, MathOps.Add(2, 3));

// NUnit
[Test]
public void Add_Works() => Assert.That(MathOps.Add(2, 3), Is.EqualTo(5));

// MSTest
[TestMethod]
public void Add_Works() => Assert.AreEqual(5, MathOps.Add(2, 3));
```

### How to choose on a real team
1. Match the **existing** solution when contributing  
2. For greenfield, pick one and stay consistent  
3. Framework differences matter less than **what** you test and how isolated it is  

---

## 3. Why This Notebook Chooses xUnit

This notebook standardizes on **xUnit** because:

| Reason | Detail |
|--------|--------|
| Industry default | Most modern ASP.NET Core samples/docs use xUnit |
| Simple model | `[Fact]` / `[Theory]` is easy to teach |
| Isolation-friendly | New test class instance per test method by default |
| Ecosystem | Works great with Moq, FluentAssertions, `WebApplicationFactory` |
| CLI-native | `dotnet new xunit` + `dotnet test` |

You can translate everything here to NUnit/MSTest later if your job requires it.

---

## 4. Create a Unit Test Project

```bash
# from solution root
dotnet new xunit -n Shop.Application.Tests -o tests/Shop.Application.Tests
dotnet sln add tests/Shop.Application.Tests/Shop.Application.Tests.csproj
dotnet add tests/Shop.Application.Tests reference src/Shop.Application/Shop.Application.csproj
dotnet test
```

### Typical solution layout

```
Shop.sln
  src/
    Shop.Api/
    Shop.Application/      ← services to test
    Shop.Domain/           ← entities/rules to test
  tests/
    Shop.Application.Tests/
    Shop.Domain.Tests/
```

### Delete the template stub
Replace `UnitTest1.cs` with real test classes named after the production type:

```
PriceCalculatorTests.cs
ProductServiceTests.cs
BankAccountTests.cs
```

---

## 5. Arrange–Act–Assert (AAA)

Every unit test should read like a short story with three beats.

```csharp
[Fact]
public void Withdraw_SufficientFunds_DecreasesBalance()
{
    // Arrange — set up the world
    var account = new BankAccount(openingBalance: 100m);

    // Act — do one thing
    account.Withdraw(40m);

    // Assert — check the outcome
    Assert.Equal(60m, account.Balance);
}
```

| Phase | Job | Tips |
|-------|-----|------|
| **Arrange** | Create system under test (SUT) + inputs | Keep setup readable |
| **Act** | Single primary action | One main behavior per test |
| **Assert** | Verify result / state / error | Prefer clear expected values |

### Smells to avoid
- Multiple unrelated acts in one test  
- Hidden dependency on real SQL “just this once”  
- Giant setup copied into 20 tests (extract helpers carefully)  

---

## 6. Facts and Theories

### `[Fact]` — one concrete scenario
```csharp
[Fact]
public void CalculateTotal_EmptyList_ReturnsZero()
{
    var calc = new PriceCalculator();
    var total = calc.CalculateTotal(Array.Empty<decimal>());
    Assert.Equal(0m, total);
}
```

### `[Theory]` — same logic, many inputs
```csharp
[Theory]
[InlineData(0, 0)]
[InlineData(1, 1)]
[InlineData(2, 2)]
[InlineData(3, 6)]
public void Factorial_ReturnsExpected(int input, int expected)
{
    Assert.Equal(expected, MathUtils.Factorial(input));
}
```

| Use Fact when | Use Theory when |
|---------------|-----------------|
| Story is unique | Rule is the same shape across rows |
| Setup is elaborate | Inputs/outputs are tabular |
| Name needs full scenario text | You want concise coverage of edges |

---

## 7. Testing Service / Business Logic in Isolation

A **service unit test** targets application rules without HTTP and without SQL.

### Production sketch
```csharp
public class PricingService
{
    public decimal ApplyDiscount(decimal amount, decimal percentOff)
    {
        if (amount < 0) throw new ArgumentOutOfRangeException(nameof(amount));
        if (percentOff is < 0 or > 100)
            throw new ArgumentOutOfRangeException(nameof(percentOff));

        var discounted = amount * (1 - (percentOff / 100m));
        return decimal.Round(discounted, 2, MidpointRounding.AwayFromZero);
    }
}
```

### Unit tests
```csharp
public class PricingServiceTests
{
    private readonly PricingService _sut = new();

    [Theory]
    [InlineData(100, 10, 90)]
    [InlineData(99.99, 0, 99.99)]
    [InlineData(50, 100, 0)]
    public void ApplyDiscount_ValidInputs_ReturnsExpected(
        decimal amount, decimal percent, decimal expected)
    {
        var result = _sut.ApplyDiscount(amount, percent);
        Assert.Equal(expected, result);
    }

    [Fact]
    public void ApplyDiscount_NegativeAmount_Throws()
    {
        Assert.Throws<ArgumentOutOfRangeException>(() => _sut.ApplyDiscount(-1, 10));
    }
}
```

No `DbContext`. No `HttpClient`. Pure logic → pure unit test.

---

## 8. Domain Logic Without a Database

Put rules on entities/value objects; unit-test them directly.

```csharp
public class BankAccount
{
    public decimal Balance { get; private set; }

    public BankAccount(decimal openingBalance)
    {
        if (openingBalance < 0)
            throw new ArgumentOutOfRangeException(nameof(openingBalance));
        Balance = openingBalance;
    }

    public void Withdraw(decimal amount)
    {
        if (amount <= 0) throw new ArgumentOutOfRangeException(nameof(amount));
        if (amount > Balance) throw new InvalidOperationException("Insufficient funds");
        Balance -= amount;
    }
}
```

```csharp
public class BankAccountTests
{
    [Fact]
    public void Withdraw_InsufficientFunds_Throws()
    {
        var account = new BankAccount(20m);
        Assert.Throws<InvalidOperationException>(() => account.Withdraw(50m));
    }

    [Fact]
    public void Withdraw_ValidAmount_UpdatesBalance()
    {
        var account = new BankAccount(50m);
        account.Withdraw(20m);
        Assert.Equal(30m, account.Balance);
    }
}
```

### When the service needs a repository?
You still write a **unit** test — but you replace the repository with a **mock or fake** (next file). The rule remains: **no real database** in unit tests.

```
Unit test boundary:

  ✅ ProductService + fake/mock IProductRepository
  ❌ ProductService + SQL Server
  ❌ Controller + full Kestrel + SQL   ← that is integration (file 03)
```

---

## 9. Naming, Structure, and Good Habits

### Method naming pattern
```
Method_Scenario_ExpectedResult

Withdraw_InsufficientFunds_Throws
ApplyDiscount_TenPercent_ReducesTotal
Create_DuplicateName_ThrowsConflict
```

### Asserts you’ll use constantly
| Assert | Meaning |
|--------|---------|
| `Assert.Equal(expected, actual)` | Values equal |
| `Assert.True` / `Assert.False` | Booleans |
| `Assert.Null` / `Assert.NotNull` | Null checks |
| `Assert.Contains` | Item in collection / substring |
| `Assert.Throws<T>` | Sync exception |
| `Assert.ThrowsAsync<T>` | Async exception |

### Async example
```csharp
[Fact]
public async Task GetTotalAsync_ReturnsSum()
{
    var sut = new MathService();
    var result = await sut.AddAsync(2, 3);
    Assert.Equal(5, result);
}
```

### Habits
1. Test **behavior**, not private implementation details  
2. Prefer many small tests over one giant test  
3. Keep unit tests offline-capable (airplane mode should pass)  
4. Don’t assert framework behavior Microsoft already tests  

---

## 10. Running Tests

```bash
dotnet test
dotnet test tests/Shop.Application.Tests
dotnet test --filter FullyQualifiedName~Withdraw
dotnet test --verbosity normal
```

### IDE
- Visual Studio Test Explorer  
- VS Code / C# Dev Kit Test Explorer  
- Rider Unit Tests  

### Red–Green–Refactor
```
1. Red     write a failing test
2. Green   write minimal code to pass
3. Refactor clean up while tests stay green
```

---

## 11. Knowledge Check

**Q1.** Name three benefits of automated tests for backend teams.  
**Q2.** xUnit vs NUnit vs MSTest — which does this notebook use and why?  
**Q3.** What are the three AAA steps?  
**Q4.** When do you prefer `[Theory]` over `[Fact]`?  
**Q5.** Why should unit tests avoid real databases?  
**Q6.** Give a good test name for “discount percent over 100 is rejected.”  
**Q7.** Which project reference does `Shop.Application.Tests` need?

### Mini practice
1. Create `tests/Shop.Domain.Tests` with xUnit  
2. Implement `BankAccount` + the tests above  
3. Add a `[Theory]` for successful withdrawals  
4. Run `dotnet test` until green  
5. Write `PricingService` tests for three discount cases + one invalid case  

### Answers (short)
1. Regression safety, faster refactors, living docs, CI gates…  
2. xUnit — modern default, simple, great ASP.NET ecosystem fit  
3. Arrange, Act, Assert  
4. Same behavior shape across many inputs  
5. Keep them fast, deterministic, offline, focused on your logic  
6. `ApplyDiscount_PercentOver100_Throws`  
7. The Application (or Domain) project under test — not necessarily the whole API host  

---

## ✅ What You Should Feel Confident About

- [ ] Explain why backends need automated tests  
- [ ] Compare xUnit / NUnit / MSTest at a high level  
- [ ] Create and run an xUnit project  
- [ ] Write AAA-style Facts and Theories  
- [ ] Unit-test domain and service rules without SQL  
- [ ] Name tests clearly and run them from CLI/IDE  

**Next:** [02-mocking-and-isolation.md](./02-mocking-and-isolation.md) — Moq, fakes, and testing services that depend on repositories or HTTP.
