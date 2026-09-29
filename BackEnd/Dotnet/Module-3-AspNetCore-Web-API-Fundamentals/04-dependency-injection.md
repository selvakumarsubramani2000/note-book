# 🔌 Dependency Injection — Loose Coupling for Real APIs

> **Trainer's Note:** DI is not academic theory in ASP.NET Core — it is the default way the framework wires your app. Learn lifetimes and constructor injection now, and your controllers stay thin while business logic becomes testable.

---

## 📑 Table of Contents
1. [What Problem Does DI Solve?](#1-what-problem-does-di-solve)
2. [Core Terms](#2-core-terms)
3. [Built-in DI Container](#3-built-in-di-container)
4. [Service Lifetimes](#4-service-lifetimes)
5. [Choosing Transient vs Scoped vs Singleton](#5-choosing-transient-vs-scoped-vs-singleton)
6. [Constructor Injection in Controllers](#6-constructor-injection-in-controllers)
7. [Building a Service Layer](#7-building-a-service-layer)
8. [Registering Your Own Services](#8-registering-your-own-services)
9. [Interfaces as Contracts](#9-interfaces-as-contracts)
10. [Common DI Pitfalls](#10-common-di-pitfalls)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. What Problem Does DI Solve?

Without DI, classes create their own dependencies:

```csharp
public class ProductsController : ControllerBase
{
    private readonly ProductService _service = new ProductService(
        new ProductRepository(new SqlConnection("...")),
        new EmailSender());
}
```

Problems:
- Hard to **test** (cannot swap fake repository)
- Hard to **change** email provider later
- Controller knows **how to construct** the whole graph
- Lifetimes and shared resources become messy

**Dependency Injection** = dependencies are **provided from outside** (usually constructor).

```csharp
public class ProductsController : ControllerBase
{
    private readonly IProductService _service;

    public ProductsController(IProductService service)
    {
        _service = service;
    }
}
```

ASP.NET Core creates the controller and **injects** the service automatically.

---

## 2. Core Terms

| Term | Meaning |
|------|---------|
| **Service** | A class that provides functionality (not only microservice!) |
| **Dependency** | Another object your class needs to work |
| **Injection** | Supplying that dependency from outside |
| **Container / IServiceProvider** | Builds object graphs and manages lifetimes |
| **Registration** | Telling the container: “when X is asked, create Y” |
| **Resolution** | Container creates an instance when needed |

```
Registration (startup)          Resolution (per request)
builder.Services.AddScoped...   Controller constructed
                                → container supplies IProductService
```

---

## 3. Built-in DI Container

ASP.NET Core includes a DI container out of the box.

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
// your registrations:
builder.Services.AddScoped<IProductService, ProductService>();

var app = builder.Build();
```

| You call | Framework does |
|----------|----------------|
| `builder.Services.Add...` | Stores recipes for creating types |
| Request hits controller | Resolves controller + graph |
| Request ends | Disposes scoped/transient disposables as designed |

You rarely call `new` for application services once DI is set up.

---

## 4. Service Lifetimes

Three primary lifetimes:

| Lifetime | Method | Instance lifespan |
|----------|--------|-------------------|
| **Transient** | `AddTransient` | New instance **every time** it is requested |
| **Scoped** | `AddScoped` | One instance **per HTTP request** (per scope) |
| **Singleton** | `AddSingleton` | **One** instance for the whole app process |

```
App process starts
  └── Singleton services created once (lazy or at start)

Each HTTP request
  └── Scope created
        ├── Scoped services shared inside this request
        └── Transient services created as needed
  └── Scope disposed at end of request
```

### Registration examples
```csharp
builder.Services.AddTransient<IEmailFormatter, EmailFormatter>();
builder.Services.AddScoped<IProductService, ProductService>();
builder.Services.AddScoped<IProductRepository, ProductRepository>();
builder.Services.AddSingleton<IClock, SystemClock>();
```

---

## 5. Choosing Transient vs Scoped vs Singleton

### Practical guide for APIs
| Kind of dependency | Usual lifetime | Why |
|--------------------|----------------|-----|
| DbContext / unit of work | **Scoped** | One DB context per request is standard |
| Business services using DbContext | **Scoped** | Align with request + DbContext |
| Lightweight stateless helpers | Transient or Scoped | Both OK; scoped often fine |
| Configuration wrappers / caches | **Singleton** | Share safely if thread-safe |
| HttpClient | Use `IHttpClientFactory` | Don’t invent naive singleton HttpClient patterns alone |

### Memory picture
```
Singleton:   [================ app lifetime ================]
Scoped:              [== request 1 ==]   [== request 2 ==]
Transient:           * * *               * * *
```

### Danger mix
**Do not** inject a **scoped** service into a **singleton** directly.
The singleton would hold the scoped instance forever → captive dependency bug.

```
❌ Singleton → depends on Scoped DbContext
✅ Singleton → depends only on other singletons / factories
✅ Scoped service → depends on Scoped or Singleton
```

---

## 6. Constructor Injection in Controllers

Preferred injection style in ASP.NET Core: **constructor injection**.

```csharp
[ApiController]
[Route("api/products")]
public class ProductsController : ControllerBase
{
    private readonly IProductService _products;

    public ProductsController(IProductService products)
    {
        _products = products;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<ProductResponseDto>>> GetAll(CancellationToken ct)
    {
        var items = await _products.GetAllAsync(ct);
        return Ok(items);
    }
}
```

### Rules
1. Ask for **interfaces** when you want swappable implementations  
2. Keep constructors honest — only real dependencies  
3. Avoid doing heavy work in constructors  
4. Prefer `readonly` fields assigned once  

### Multiple dependencies
```csharp
public ProductsController(
    IProductService products,
    ILogger<ProductsController> logger)
{
    _products = products;
    _logger = logger;
}
```
`ILogger<T>` is registered by the host automatically.

---

## 7. Building a Service Layer

Thin controllers + focused services = maintainable APIs.

```
Controller   → HTTP concerns (status codes, binding)
Service      → application/business use-cases
Repository   → data access (later with EF Core)
```

### Interface + implementation
```csharp
public interface IProductService
{
    Task<IReadOnlyList<ProductResponseDto>> GetAllAsync(CancellationToken ct = default);
    Task<ProductResponseDto?> GetByIdAsync(int id, CancellationToken ct = default);
    Task<ProductResponseDto> CreateAsync(CreateProductRequestDto request, CancellationToken ct = default);
}

public class ProductService : IProductService
{
    private readonly IProductRepository _repo;
    private readonly ILogger<ProductService> _logger;

    public ProductService(IProductRepository repo, ILogger<ProductService> logger)
    {
        _repo = repo;
        _logger = logger;
    }

    public async Task<ProductResponseDto> CreateAsync(CreateProductRequestDto request, CancellationToken ct = default)
    {
        var product = new Product(request.Name, request.Price);
        await _repo.AddAsync(product, ct);
        _logger.LogInformation("Created product {ProductId}", product.Id);
        return new ProductResponseDto(product.Id, product.Name, product.Price);
    }

    // GetAllAsync / GetByIdAsync ...
}
```

### Controller stays boring (good!)
```csharp
[HttpPost]
public async Task<ActionResult<ProductResponseDto>> Create(
    CreateProductRequestDto request,
    CancellationToken ct)
{
    var created = await _products.CreateAsync(request, ct);
    return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
}
```

---

## 8. Registering Your Own Services

In `Program.cs`:

```csharp
builder.Services.AddScoped<IProductRepository, InMemoryProductRepository>();
builder.Services.AddScoped<IProductService, ProductService>();
```

### Registration styles
```csharp
// Interface → implementation (preferred)
services.AddScoped<IProductService, ProductService>();

// Concrete only (harder to mock/swap)
services.AddScoped<ProductService>();

// Factory when creation needs logic
services.AddSingleton<ICache>(_ => new MemoryCacheWrapper());

// Register multiple interfaces to one type carefully (advanced)
```

### Extension method organization (clean Program.cs)
```csharp
// ServiceCollectionExtensions.cs
public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddShopApplication(this IServiceCollection services)
    {
        services.AddScoped<IProductService, ProductService>();
        services.AddScoped<IProductRepository, InMemoryProductRepository>();
        return services;
    }
}

// Program.cs
builder.Services.AddShopApplication();
```

---

## 9. Interfaces as Contracts

Why `IProductService` instead of only `ProductService`?

| Benefit | Explanation |
|---------|-------------|
| Test doubles | Unit tests inject fakes |
| Swap implementations | In-memory vs SQL repository |
| Clear API of dependency | What methods exist matters, not private details |
| Aligns with DIP (SOLID) | Depend on abstractions |

### Beginner in-memory repository
```csharp
public interface IProductRepository
{
    Task<Product?> GetByIdAsync(int id, CancellationToken ct = default);
    Task<IReadOnlyList<Product>> GetAllAsync(CancellationToken ct = default);
    Task AddAsync(Product product, CancellationToken ct = default);
}

public class InMemoryProductRepository : IProductRepository
{
    private readonly List<Product> _items = new();
    private int _nextId = 1;

    public Task AddAsync(Product product, CancellationToken ct = default)
    {
        // demo only: assign id via your domain design
        _items.Add(product);
        return Task.CompletedTask;
    }

    public Task<IReadOnlyList<Product>> GetAllAsync(CancellationToken ct = default)
        => Task.FromResult((IReadOnlyList<Product>)_items.ToList());

    public Task<Product?> GetByIdAsync(int id, CancellationToken ct = default)
        => Task.FromResult(_items.FirstOrDefault(p => p.Id == id));
}
```

Replace with EF Core repository later **without rewriting controllers**.

---

## 10. Common DI Pitfalls

| Pitfall | Fix |
|---------|-----|
| `new` service inside controller | Inject instead |
| Everything Singleton “for speed” | Use scoped for request data; measure first |
| Scoped into Singleton | Redesign; use `IServiceScopeFactory` only when truly needed |
| Fat controllers | Move rules to services |
| 15 constructor dependencies | Class doing too much — split |
| Not registering a type | Runtime exception: unable to resolve service |
| Disposable transient held incorrectly | Understand disposal rules; prefer scoped for many request resources |

### Exception you will see
```
Unable to resolve service for type 'IProductService'
while attempting to activate 'ProductsController'.
```
→ Register it in `Program.cs`.

### Method injection (less common)
```csharp
[HttpGet]
public IActionResult Get([FromServices] IProductService products) => Ok();
```
Prefer constructor injection for required dependencies.

---

## 11. Knowledge Check

**Q1.** What does DI stand for, and what problem does it primarily solve in APIs?  
**Q2.** Where do you register services — before or after `builder.Build()`?  
**Q3.** Difference between Transient, Scoped, and Singleton?  
**Q4.** What lifetime do you typically use for business services with database work?  
**Q5.** Why inject `IProductService` instead of creating `new ProductService()` in the controller?  
**Q6.** What is a captive dependency?  
**Q7.** Name one sign a controller needs a service layer.

### Mini practice
1. Create `IProductService` + `ProductService`  
2. Create `IProductRepository` + in-memory implementation  
3. Register both as Scoped  
4. Inject service into `ProductsController`  
5. Implement GET all / GET by id / POST create  
6. Optionally write a fake repository for a unit test  

### Answers (short)
1. Dependency Injection — supply dependencies externally for decoupling/testability  
2. Before `Build()` via `builder.Services`  
3. Per-resolve / per-request / per-app  
4. Scoped  
5. Loose coupling, testability, lifetime management  
6. Longer-lived service permanently holding shorter-lived dependency  
7. Business rules, data access, or orchestration cluttering HTTP action methods  

---

## ✅ What You Should Feel Confident About

- [ ] Explain DI in plain words with a controller example  
- [ ] Register services with `AddTransient` / `AddScoped` / `AddSingleton`  
- [ ] Choose sensible lifetimes for API services  
- [ ] Use constructor injection  
- [ ] Split business logic into a service layer behind interfaces  
- [ ] Diagnose “unable to resolve service” mistakes  

**Previous:** [03-models-and-dtos.md](./03-models-and-dtos.md)  
**Next:** [05-middleware-and-request-pipeline.md](./05-middleware-and-request-pipeline.md) — how every request flows through middleware.
