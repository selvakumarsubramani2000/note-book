# 🎭 Mocking & Isolation — Test Your Code, Not SQL or the Network

> **Trainer's Note:** Real services depend on repositories, `DbContext`, email gateways, and other APIs. Unit tests stay fast by replacing those collaborators with **test doubles**. This file teaches **Moq** for mocks and when a simple **fake** is better — including repositories, EF-facing ports, and `HttpClient` exteriors.

---

## 📑 Table of Contents
1. [Why Isolation Matters](#1-why-isolation-matters)
2. [Test Double Vocabulary](#2-test-double-vocabulary)
3. [Interfaces Make Mocking Possible](#3-interfaces-make-mocking-possible)
4. [Getting Moq](#4-getting-moq)
5. [Moq Basics: Setup and Returns](#5-moq-basics-setup-and-returns)
6. [Verifying Calls](#6-verifying-calls)
7. [Mocking Repositories](#7-mocking-repositories)
8. [Mocking “Database” Dependencies Sensibly](#8-mocking-database-dependencies-sensibly)
9. [Mocking External HTTP Services](#9-mocking-external-http-services)
10. [Fakes vs Mocks + Common Pitfalls](#10-fakes-vs-mocks--common-pitfalls)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. Why Isolation Matters

```
ProductService
  ├── IProductRepository   → SQL
  ├── IEmailSender         → SMTP/network
  └── IClock               → system time
```

| If tests use real deps | If tests use doubles |
|------------------------|----------------------|
| Need DB running | Run offline |
| Slow | Milliseconds |
| Flaky network | Deterministic |
| Many failure reasons | Failures point at **your** logic |

**Isolation** means: the test can fail only because the unit under test is wrong (or the test itself is wrong) — not because SQL is down.

---

## 2. Test Double Vocabulary

| Term | Simple meaning | Example |
|------|----------------|---------|
| **Stub** | Provides canned answers | `GetById` returns a sample product |
| **Fake** | Lightweight working implementation | In-memory list repository |
| **Mock** | Programmed double you can **verify** interactions on | Moq object with `Verify` |
| **Dummy** | Passed in but unused | Extra constructor arg |
| **Spy** | Records calls for later asserts | Manual list of sent emails |

In everyday speech people say “mock” for all of these. Be precise when teaching/designing.

```
System under test (SUT)
        │
        ▼
  dependency double (mock/fake/stub)
```

---

## 3. Interfaces Make Mocking Possible

Constructor injection + interfaces (from your DI module) enable isolation.

```csharp
public interface IProductRepository
{
    Task<bool> ExistsByNameAsync(string name, CancellationToken ct = default);
    Task AddAsync(Product product, CancellationToken ct = default);
    Task<int> SaveChangesAsync(CancellationToken ct = default);
}

public class ProductService
{
    private readonly IProductRepository _repo;

    public ProductService(IProductRepository repo) => _repo = repo;

    public async Task<ProductDto> CreateAsync(CreateProductRequest request, CancellationToken ct = default)
    {
        if (await _repo.ExistsByNameAsync(request.Name, ct))
            throw new ConflictException("Product name already exists");

        var product = new Product(request.Name, request.Price);
        await _repo.AddAsync(product, ct);
        await _repo.SaveChangesAsync(ct);
        return new ProductDto(product.Id, product.Name, product.Price);
    }
}
```

You unit-test `ProductService` by injecting `Mock<IProductRepository>.Object` — not SQL.

---

## 4. Getting Moq

**Moq** is the most common mocking library in .NET samples.

```bash
dotnet add tests/Shop.Application.Tests package Moq
```

> Only install packages you approve on your machine/policy. Moq is widely used and open source; still treat new dependencies as intentional.

### Using statements
```csharp
using Moq;
using Xunit;
```

---

## 5. Moq Basics: Setup and Returns

```csharp
var repo = new Mock<IProductRepository>();

repo.Setup(r => r.ExistsByNameAsync("Keyboard", It.IsAny<CancellationToken>()))
    .ReturnsAsync(false);

repo.Setup(r => r.AddAsync(It.IsAny<Product>(), It.IsAny<CancellationToken>()))
    .Returns(Task.CompletedTask);

repo.Setup(r => r.SaveChangesAsync(It.IsAny<CancellationToken>()))
    .ReturnsAsync(1);

var sut = new ProductService(repo.Object);
```

| Piece | Meaning |
|-------|---------|
| `new Mock<T>()` | Create mock of interface/abstract class |
| `Setup(...)` | Configure a member |
| `Returns` / `ReturnsAsync` | Canned result |
| `Throws` / `ThrowsAsync` | Force dependency failure |
| `It.IsAny<T>()` | Match any argument of that type |
| `repo.Object` | Concrete instance to inject |

### Full happy-path test
```csharp
[Fact]
public async Task CreateAsync_NewName_ReturnsDto()
{
    // Arrange
    var repo = new Mock<IProductRepository>();
    repo.Setup(r => r.ExistsByNameAsync("Keyboard", It.IsAny<CancellationToken>()))
        .ReturnsAsync(false);
    repo.Setup(r => r.AddAsync(It.IsAny<Product>(), It.IsAny<CancellationToken>()))
        .Returns(Task.CompletedTask);
    repo.Setup(r => r.SaveChangesAsync(It.IsAny<CancellationToken>()))
        .ReturnsAsync(1);

    var sut = new ProductService(repo.Object);

    // Act
    var dto = await sut.CreateAsync(new CreateProductRequest("Keyboard", 1499m));

    // Assert
    Assert.Equal("Keyboard", dto.Name);
    Assert.Equal(1499m, dto.Price);
}
```

---

## 6. Verifying Calls

Sometimes the important behavior is **what the SUT calls**.

```csharp
[Fact]
public async Task CreateAsync_DuplicateName_DoesNotAdd()
{
    var repo = new Mock<IProductRepository>();
    repo.Setup(r => r.ExistsByNameAsync("Keyboard", It.IsAny<CancellationToken>()))
        .ReturnsAsync(true);

    var sut = new ProductService(repo.Object);

    await Assert.ThrowsAsync<ConflictException>(() =>
        sut.CreateAsync(new CreateProductRequest("Keyboard", 10m)));

    repo.Verify(r => r.AddAsync(It.IsAny<Product>(), It.IsAny<CancellationToken>()),
        Times.Never);
    repo.Verify(r => r.SaveChangesAsync(It.IsAny<CancellationToken>()),
        Times.Never);
}
```

### Times helpers
```csharp
Times.Never
Times.Once
Times.Exactly(2)
Times.AtLeastOnce
```

### Argument matchers in Verify
```csharp
repo.Verify(r => r.AddAsync(
        It.Is<Product>(p => p.Name == "Mouse" && p.Price == 500m),
        It.IsAny<CancellationToken>()),
    Times.Once);
```

Verify **meaningful** interactions — not every property get.

---

## 7. Mocking Repositories

Repositories are the #1 mock target for application services.

```csharp
public interface IOrderRepository
{
    Task<Order?> GetByIdAsync(Guid id, CancellationToken ct = default);
    Task AddAsync(Order order, CancellationToken ct = default);
}
```

```csharp
var orders = new Mock<IOrderRepository>();
var existing = new Order(Guid.Parse("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"), "user-1");

orders.Setup(r => r.GetByIdAsync(existing.Id, It.IsAny<CancellationToken>()))
      .ReturnsAsync(existing);

orders.Setup(r => r.GetByIdAsync(It.Is<Guid>(id => id != existing.Id), It.IsAny<CancellationToken>()))
      .ReturnsAsync((Order?)null);
```

### Pattern: arrange dependency outcomes, act on service, assert domain result
```
Arrange mock Exists/Get returns
Act    service.Create / Cancel / Refund
Assert DTO / exception / Verify save called
```

---

## 8. Mocking “Database” Dependencies Sensibly

### Prefer ports over mocking EF types
| Approach | Recommendation |
|----------|----------------|
| Mock `IProductRepository` | ✅ Best for unit tests |
| Mock `DbSet<Product>` / full `DbContext` | ⚠️ Painful and brittle for beginners |
| Real EF against InMemory/SQLite | ✅ Integration tests (file 03) |

```
Unit:        service → mock IRepository
Integration: API/DB → real EF provider (InMemory or SQLite)
```

### If your service takes `AppDbContext` directly
That’s harder to unit-test cleanly. Prefer introducing a repository or query interface.

### Stubbing unit-of-work style
```csharp
var uow = new Mock<IUnitOfWork>();
uow.Setup(x => x.Products).Returns(productRepo.Object);
uow.Setup(x => x.SaveChangesAsync(It.IsAny<CancellationToken>()))
   .ReturnsAsync(1);
```

### Throwing DB failures
```csharp
repo.Setup(r => r.SaveChangesAsync(It.IsAny<CancellationToken>()))
    .ThrowsAsync(new InvalidOperationException("disk full"));
```
Useful to ensure the service surfaces/handles failures correctly (without a real DB).

---

## 9. Mocking External HTTP Services

Don’t hit real Stripe/email/geo APIs in unit tests.

### Better design: wrap HttpClient
```csharp
public interface IShippingApi
{
    Task<decimal> GetShippingQuoteAsync(string city, CancellationToken ct = default);
}

public class ShippingApiClient : IShippingApi
{
    private readonly HttpClient _http;
    public ShippingApiClient(HttpClient http) => _http = http;
    // uses _http.GetFromJsonAsync...
}
```

### Unit-test consumers by mocking the interface
```csharp
var shipping = new Mock<IShippingApi>();
shipping.Setup(s => s.GetShippingQuoteAsync("Chennai", It.IsAny<CancellationToken>()))
        .ReturnsAsync(75m);

var sut = new CheckoutService(shipping.Object, /* ... */);
var total = await sut.CalculateTotalAsync(cart, "Chennai");
Assert.Equal(cart.ItemsTotal + 75m, total);
```

### Mocking HttpMessageHandler (when you must test the client class)
```csharp
var handler = new Mock<HttpMessageHandler>();
// Setup Protected SendAsync ... (advanced)
var http = new HttpClient(handler.Object) { BaseAddress = new Uri("https://shipping.test/") };
var client = new ShippingApiClient(http);
```

Beginners: mock **`IShippingApi`** at the service boundary first. Mocking handlers is a later skill.

### What never to do in unit tests
```csharp
// ❌ real network
await _http.GetAsync("https://api.production.example/v1/shipping");
```

---

## 10. Fakes vs Mocks + Common Pitfalls

### Hand-written fake repository
```csharp
public class InMemoryProductRepository : IProductRepository
{
    private readonly List<Product> _items = new();

    public Task<bool> ExistsByNameAsync(string name, CancellationToken ct = default)
        => Task.FromResult(_items.Any(p => p.Name == name));

    public Task AddAsync(Product product, CancellationToken ct = default)
    {
        _items.Add(product);
        return Task.CompletedTask;
    }

    public Task<int> SaveChangesAsync(CancellationToken ct = default)
        => Task.FromResult(0);
}
```

| Moq | Fake |
|-----|------|
| Fast stub of one method | Natural multi-step state |
| Great for Verify | Great for “save then exists” flows |
| Interface-churn maintenance | A bit more code |

### Pitfalls
| Pitfall | Fix |
|---------|-----|
| Mocking the SUT itself | Mock dependencies only |
| Over-Verify call order for everything | Assert business outcomes first |
| Setup never matches arguments | Use correct `It.Is` / values |
| Deep-mocking EF `DbSet` | Use repository ports or integration tests |
| Shared static mock state | Create mocks per test |
| Testing only that the mock was configured | Assert results that matter to users |

### Strict mocks (optional)
```csharp
var repo = new Mock<IProductRepository>(MockBehavior.Strict);
```
Unexpected calls fail the test — useful, sometimes noisy.

---

## 11. Knowledge Check

**Q1.** Why isolate dependencies in unit tests?  
**Q2.** Stub vs mock in one sentence each?  
**Q3.** What does `repo.Object` give you?  
**Q4.** How do you return a value from an async mock method?  
**Q5.** How do you assert `AddAsync` was never called?  
**Q6.** Should beginners mock `DbSet<T>` or `IProductRepository`?  
**Q7.** How should external HTTP APIs appear in unit tests?

### Mini practice
1. Add Moq to `Shop.Application.Tests`  
2. Unit-test `ProductService.CreateAsync` happy path  
3. Unit-test duplicate name → conflict + `Verify` never adds  
4. Write the same happy path with `InMemoryProductRepository`  
5. Introduce `IShippingApi` mock in a checkout total test  

### Answers (short)
1. Speed, determinism, offline runs, failures pinpoint your logic  
2. Stub supplies answers; mock can also verify interactions  
3. The generated implementation instance of the mocked interface  
4. `ReturnsAsync(...)`  
5. `Verify(..., Times.Never)`  
6. `IProductRepository` (or similar port)  
7. Behind an interface (or tested handler); never live network in unit tests  

---

## ✅ What You Should Feel Confident About

- [ ] Explain isolation and test doubles in plain language  
- [ ] Use Moq `Setup` / `ReturnsAsync` / `ThrowsAsync`  
- [ ] `Verify` critical repository interactions  
- [ ] Mock repositories instead of deep EF types  
- [ ] Isolate external HTTP behind interfaces  
- [ ] Choose fake vs mock appropriately  

**Previous:** [01-unit-testing.md](./01-unit-testing.md)  
**Next:** [03-integration-and-functional-testing.md](./03-integration-and-functional-testing.md) — `WebApplicationFactory`, InMemory/SQLite, and auth flows.
