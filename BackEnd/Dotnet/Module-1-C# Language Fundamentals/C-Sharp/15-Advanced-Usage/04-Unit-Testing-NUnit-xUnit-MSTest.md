# 🧪 Unit Testing with NUnit, xUnit & MSTest in C#

> **Trainer's Note:** Unit tests verify small pieces of logic quickly. In .NET, xUnit, NUnit, and MSTest are the common frameworks. Learn one well, recognize all three.

---

## 📑 Table of Contents
1. [Why Unit Tests?](#1-why-unit-tests)
2. [xUnit Example](#2-xunit-example)
3. [NUnit and MSTest Quick View](#3-nunit-and-mstest-quick-view)
4. [AAA Pattern and Good Habits](#4-aaa-pattern-and-good-habits)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Why Unit Tests?

A **unit test** checks one unit (often one method) in isolation.

### Real-world analogy
```
Before sending a bike for delivery:
  Check brakes
  Check lights
  Check tire pressure

Unit tests = checklist for small parts before full journey
```

Benefits:
- catch bugs early
- safe refactoring
- documents expected behavior

---

## 2. xUnit Example

xUnit is very common in modern .NET templates.

```csharp
public class Calculator
{
    public int Add(int a, int b) => a + b;
}
```

```csharp
using Xunit;

public class CalculatorTests
{
    [Fact]
    public void Add_TwoNumbers_ReturnsSum()
    {
        // Arrange
        var calc = new Calculator();

        // Act
        int result = calc.Add(2, 3);

        // Assert
        Assert.Equal(5, result);
    }

    [Theory]
    [InlineData(1, 1, 2)]
    [InlineData(5, 0, 5)]
    public void Add_ManyInputs_Works(int a, int b, int expected)
    {
        var calc = new Calculator();
        Assert.Equal(expected, calc.Add(a, b));
    }
}
```

---

## 3. NUnit and MSTest Quick View

### NUnit
```csharp
using NUnit.Framework;

public class CalculatorTests
{
    [Test]
    public void Add_Works()
    {
        var calc = new Calculator();
        Assert.That(calc.Add(2, 3), Is.EqualTo(5));
    }
}
```

### MSTest
```csharp
using Microsoft.VisualStudio.TestTools.UnitTesting;

[TestClass]
public class CalculatorTests
{
    [TestMethod]
    public void Add_Works()
    {
        var calc = new Calculator();
        Assert.AreEqual(5, calc.Add(2, 3));
    }
}
```

### Framework attributes (simple map)
| Idea | xUnit | NUnit | MSTest |
|------|-------|-------|--------|
| Test method | `[Fact]` | `[Test]` | `[TestMethod]` |
| Test class | (plain class) | (plain class) | `[TestClass]` |
| Data cases | `[Theory]` / `[InlineData]` | `[TestCase]` | `[DataTestMethod]` / `[DataRow]` |

---

## 4. AAA Pattern and Good Habits

**AAA = Arrange → Act → Assert**

| Habit | Why |
|-------|-----|
| Name tests clearly | `Method_Scenario_Expected` |
| Test one behavior | easier failures |
| Avoid testing private guts directly | test public behavior |
| Use fakes/mocks for dependencies | true unit isolation |
| Keep tests fast | run often |

### Run tests
```bash
dotnet test
```

---

## 5. Knowledge Check

1. What does a unit test verify?
2. What is the AAA pattern?
3. Name one attribute used by xUnit, NUnit, and MSTest for a basic test.
4. Why are clear test names important?

---

**Previous:** [← Dependency Injection](./03-Dependency-Injection.md)  
**Next:** [NuGet Package Management →](./05-Package-Management-with-NuGet.md)
