# Day 2 — Dependency Injection (Deep Understanding)

> **Goal:** Understand what DI is, why ASP.NET Core is built around it, and deeply internalize the difference between **Transient**, **Scoped**, and **Singleton** with runnable examples.

**Prerequisite:** [Day 1 — Middleware Pipeline](./Day-01-Middleware-Pipeline.md)

---

## 📑 Table of Contents

1. [What is Dependency Injection?](#1-what-is-dependency-injection)
2. [The Problem DI Solves](#2-the-problem-di-solves)
3. [The ASP.NET Core DI Container](#3-the-aspnet-core-di-container)
4. [Constructor Injection (the 99% pattern)](#4-constructor-injection-the-99-pattern)
5. [Service Lifetimes — Transient / Scoped / Singleton](#5-service-lifetimes--transient--scoped--singleton)
6. [Practical Example: See the difference with your own eyes](#6-practical-example-see-the-difference-with-your-own-eyes)
7. [Choosing the Right Lifetime](#7-choosing-the-right-lifetime)
8. [Common Pitfalls](#8-common-pitfalls)
9. [Advanced Registration Patterns](#9-advanced-registration-patterns)
10. [Other Injection Points](#10-other-injection-points)
11. [Key Takeaways & Exercises](#11-key-takeaways--exercises)

---

## 1. What is Dependency Injection?

**Dependency Injection** is a design pattern where an object **receives** its dependencies from the outside rather than creating them itself.

```csharp
// ❌ Without DI — hard-coded dependency
public class VendorService
{
    private readonly SqlRepository _repo = new SqlRepository();  // tightly coupled!
}

// ✅ With DI — dependency is injected
public class VendorService
{
    private readonly IRepository _repo;

    public VendorService(IRepository repo)   // ← someone gives it to me
    {
        _repo = repo;
    }
}
```

### Benefits
- **Loose coupling** — depend on interfaces, not concrete classes.
- **Testability** — swap real DB with an in-memory fake in tests.
- **Configuration** — change behavior in `Program.cs` without touching consumers.
- **Lifetime management** — the container handles creation & disposal.

---

## 2. The Problem DI Solves

### Without DI (tight coupling)
```csharp
public class VendorController
{
    private readonly VendorService _svc = new VendorService(
        new SqlRepository(
            new ConfigurationReader(),
            new Logger()));

    // Hard to test. Hard to change. Hard to maintain.
}
```

### With DI (clean & flexible)
```csharp
public class VendorController : ControllerBase
{
    private readonly VendorService _svc;

    public VendorController(VendorService svc) => _svc = svc;
}
```

The **container** handles the object graph automatically.

---

## 3. The ASP.NET Core DI Container

ASP.NET Core ships with a **built-in** DI container. You access it through `IServiceCollection` (to register) and `IServiceProvider` (to resolve).

```csharp
var builder = WebApplication.CreateBuilder(args);

// ──────────────────────────────────────────
// Register services (the "service collection")
// ──────────────────────────────────────────
builder.Services.AddControllers();
builder.Services.AddScoped<IVendorRepository, VendorRepository>();
builder.Services.AddScoped<VendorService>();
builder.Services.AddSingleton<ICacheService, MemoryCacheService>();
builder.Services.AddTransient<IEmailSender, SmtpEmailSender>();

var app = builder.Build();    // container is built here — immutable afterward
```

### Three Registration Methods
| Method | Lifetime | New instance per... |
|--------|----------|---------------------|
| `AddTransient<T>()` | Transient | **Every injection** |
| `AddScoped<T>()` | Scoped | **HTTP request** |
| `AddSingleton<T>()` | Singleton | **Application lifetime** |

## 4. Constructor Injection (the 99% pattern)

You simply declare dependencies as constructor parameters. The container provides them.

```csharp
public class VendorService
{
    private readonly IVendorRepository _repo;
    private readonly ILogger<VendorService> _logger;
    private readonly ICacheService _cache;

    public VendorService(
        IVendorRepository repo,
        ILogger<VendorService> logger,
        ICacheService cache)
    {
        _repo = repo;
        _logger = logger;
        _cache = cache;
    }

    public async Task<Vendor?> GetAsync(int id)
    {
        if (_cache.TryGet<Vendor>($"v-{id}", out var cached)) return cached;

        var vendor = await _repo.FindAsync(id);
        if (vendor != null) _cache.Set($"v-{id}", vendor);
        return vendor;
    }
}
```

### Variant — C# 12 Primary Constructor
```csharp
public class VendorService(
    IVendorRepository repo,
    ILogger<VendorService> logger) : IVendorService
{
    public Task<Vendor?> GetAsync(int id) => repo.FindAsync(id);
}
```

---

## 5. Service Lifetimes — Transient / Scoped / Singleton

This is the topic most developers get confused by. Let's nail it down.

### 🎯 Transient — `AddTransient`
A **new** instance every time the service is requested.

```
Request 1:
  Controller → new VendorService (A)
  Middleware → new VendorService (B)   ← different instance!
Request 2:
  Controller → new VendorService (C)
```

**Use for:** lightweight, stateless services (validators, DTO mappers).

### 🎯 Scoped — `AddScoped`
**One** instance **per HTTP request**. Shared across everything that needs it within that request.

```
Request 1:
  Controller → VendorService (A)
  Middleware → VendorService (A)       ← same instance
  Service    → VendorService (A)
Request 2:
  Controller → VendorService (B)       ← new instance for new request
```

**Use for:** `DbContext` (EF Core), anything that should see one consistent view within a request.

### 🎯 Singleton — `AddSingleton`
**One** instance for the entire application lifetime.

```
Request 1: → CacheService (A)
Request 2: → CacheService (A)    ← same
Request N: → CacheService (A)    ← same
```

**Use for:** caches, configuration, HTTP clients (via `IHttpClientFactory`), stateless helpers.

---

## 6. Practical Example: See the difference with your own eyes

Create a tiny demo showing instance IDs for each lifetime.

### Step 1 — Three services, all identical except lifetime
```csharp
public interface ITransientService  { Guid Id { get; } }
public interface IScopedService     { Guid Id { get; } }
public interface ISingletonService  { Guid Id { get; } }

public class TransientService  : ITransientService  { public Guid Id { get; } = Guid.NewGuid(); }
public class ScopedService     : IScopedService     { public Guid Id { get; } = Guid.NewGuid(); }
public class SingletonService  : ISingletonService  { public Guid Id { get; } = Guid.NewGuid(); }
```

### Step 2 — Register them
```csharp
builder.Services.AddTransient<ITransientService, TransientService>();
builder.Services.AddScoped   <IScopedService,    ScopedService>();
builder.Services.AddSingleton<ISingletonService, SingletonService>();
```

### Step 3 — Consume them in two places per request
```csharp
// A "wrapper" service that itself pulls in the three again
public class LifetimeWrapper(
    ITransientService t, IScopedService s, ISingletonService si)
{
    public Guid T => t.Id;
    public Guid S => s.Id;
    public Guid Si => si.Id;
}

builder.Services.AddScoped<LifetimeWrapper>();
```

### Step 4 — Endpoint that shows both injections
```csharp
app.MapGet("/lifetimes", (
    ITransientService  t1,
    ITransientService  t2,
    IScopedService     s1,
    IScopedService     s2,
    ISingletonService  si1,
    ISingletonService  si2,
    LifetimeWrapper    wrapper) =>
{
    return Results.Ok(new
    {
        Transient1      = t1.Id,
        Transient2      = t2.Id,     // 👈 DIFFERENT from Transient1
        Scoped1         = s1.Id,
        Scoped2         = s2.Id,     // 👈 SAME as Scoped1
        ScopedInWrapper = wrapper.S, // 👈 SAME as Scoped1 (same request)
        Singleton1      = si1.Id,
        Singleton2      = si2.Id     // 👈 SAME (forever)
    });
});
```

### Step 5 — Observe
Hit the endpoint twice:

```json
// Request 1
{
  "transient1":      "aa-11",        // different
  "transient2":      "bb-22",        // different
  "scoped1":         "cc-33",        // same within request
  "scoped2":         "cc-33",        // same
  "scopedInWrapper": "cc-33",        // same
  "singleton1":      "ff-99",        // FOREVER same
  "singleton2":      "ff-99"
}

// Request 2
{
  "transient1":      "dd-44",
  "transient2":      "ee-55",
  "scoped1":         "gg-66",        // NEW scoped
  "scoped2":         "gg-66",
  "scopedInWrapper": "gg-66",
  "singleton1":      "ff-99",        // 🔒 SAME as request 1
  "singleton2":      "ff-99"
}
```

---

## 7. Choosing the Right Lifetime

Use this decision tree:

```
Does the service have state that changes per-request?
├─ Yes  → Scoped
└─ No   → Is the object expensive to create or thread-safe & stateless?
         ├─ Yes → Singleton
         └─ No  → Transient
```

### Common Real-World Choices
| Service | Lifetime | Why |
|---------|----------|-----|
| `DbContext` (EF Core) | **Scoped** | Tracks entities per request; not thread-safe |
| Repository | **Scoped** | Uses the scoped DbContext |
| Business service (e.g., `VendorService`) | **Scoped** | Uses scoped repositories |
| `IMemoryCache` | **Singleton** | Shared cache across app |
| `HttpClient` (via `AddHttpClient`) | Singleton handler pool | Managed by factory |
| `IConfiguration`, `IOptions<T>` | **Singleton** | Immutable config |
| Validator, mapper | **Transient** | Cheap, stateless |
| `ILogger<T>` | **Singleton** | Provided by framework |

---

## 8. Common Pitfalls

### ⚠️ Pitfall 1 — Captive Dependency
Injecting a **shorter-lived** service into a **longer-lived** one traps the shorter one forever.

```csharp
// ❌ BAD — DbContext (Scoped) captured by Singleton = used across ALL requests!
public class VendorCache    // Singleton
{
    private readonly AppDbContext _db;    // Scoped — BAD!

    public VendorCache(AppDbContext db) => _db = db;
}
```
.NET will actually throw `InvalidOperationException: Cannot consume scoped service from singleton` when you build the provider in development mode (validation enabled).

**Fix:** inject `IServiceScopeFactory` and create a scope when needed.
```csharp
public class VendorCache
{
    private readonly IServiceScopeFactory _scopeFactory;
    public VendorCache(IServiceScopeFactory f) => _scopeFactory = f;

    public async Task RefreshAsync()
    {
        using var scope = _scopeFactory.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        // use db
    }
}
```

### ⚠️ Pitfall 2 — Service Locator Anti-Pattern
Don't inject `IServiceProvider` everywhere to resolve things manually.

```csharp
// ❌ Avoid
public class BadService(IServiceProvider sp)
{
    public void Do()
    {
        var repo = sp.GetRequiredService<IRepository>();  // smells bad
    }
}
```
Prefer constructor injection — dependencies become **explicit**.

### ⚠️ Pitfall 3 — Singleton with mutable state + no locking
Shared state across all requests = race conditions.
```csharp
// ❌ NOT thread-safe
public class Counter    // Singleton
{
    public int Count { get; set; } = 0;    // race condition!
}
```
Use `Interlocked`, `lock`, or a `ConcurrentDictionary`.

### ⚠️ Pitfall 4 — `DbContext` as Singleton
`DbContext` is NOT thread-safe and tracks entities. Must be **Scoped**.

---

## 9. Advanced Registration Patterns

### Register Multiple Implementations of the Same Interface
```csharp
builder.Services.AddScoped<INotifier, EmailNotifier>();
builder.Services.AddScoped<INotifier, SmsNotifier>();
builder.Services.AddScoped<INotifier, PushNotifier>();

// Inject ALL of them
public class NotificationService(IEnumerable<INotifier> notifiers)
{
    public Task NotifyAll(string msg) =>
        Task.WhenAll(notifiers.Select(n => n.SendAsync(msg)));
}
```

### Factory Registration (for runtime decisions)
```csharp
builder.Services.AddScoped<IRepository>(sp =>
{
    var config = sp.GetRequiredService<IConfiguration>();
    return config["Db:Provider"] == "Sql"
        ? new SqlRepository(...)
        : new MongoRepository(...);
});
```

### Open Generic Registration
```csharp
// Single line registers Repository<Vendor>, Repository<User>, Repository<Order>, etc.
builder.Services.AddScoped(typeof(IRepository<>), typeof(Repository<>));
```

### Keyed Services (.NET 8+)
```csharp
builder.Services.AddKeyedSingleton<INotifier, EmailNotifier>("email");
builder.Services.AddKeyedSingleton<INotifier, SmsNotifier>("sms");

public class OrderService([FromKeyedServices("email")] INotifier notifier) { }
```

### TryAdd — only register if not already registered
```csharp
builder.Services.TryAddScoped<IVendorService, VendorService>();
```

### Conditional Registration
```csharp
if (builder.Environment.IsDevelopment())
    builder.Services.AddScoped<IEmailSender, ConsoleEmailSender>();
else
    builder.Services.AddScoped<IEmailSender, SmtpEmailSender>();
```

---
## 10. Other Injection Points

Besides constructors, you can inject services at these spots:

### Action Method Parameter (`[FromServices]`)
```csharp
[HttpGet("{id}")]
public async Task<IActionResult> Get(int id, [FromServices] IVendorService svc)
{
    var v = await svc.GetAsync(id);
    return v is null ? NotFound() : Ok(v);
}
```
Useful when only one action needs that service (keeps the controller constructor lean).

### Minimal APIs
```csharp
app.MapGet("/vendors/{id}", async (int id, IVendorService svc) =>
    await svc.GetAsync(id) is { } v ? Results.Ok(v) : Results.NotFound());
```

### Middleware `InvokeAsync` parameters
```csharp
public async Task InvokeAsync(HttpContext ctx, IVendorService svc)    // injected per-request
{
    // ...
    await _next(ctx);
}
```
> Only **method** parameters get per-request DI — constructor parameters of convention middleware are resolved **once** at startup (so don't inject Scoped services there).

---

## 11. Key Takeaways & Exercises

### 🎯 Summary Table
| Concept | Remember |
|---------|----------|
| **DI** | Dependencies arrive from outside — usually via constructor |
| **Container** | `builder.Services` to register, `IServiceProvider` to resolve |
| **Transient** | New instance every resolution |
| **Scoped** | One per HTTP request |
| **Singleton** | One for the entire app lifetime |
| **Captive dep** | Never inject Scoped into Singleton — use `IServiceScopeFactory` |
| **Controllers/Minimal APIs** | Constructor DI is the default |
| **[FromServices]** | Per-action DI alternative |

### Exercises

**Exercise 1 — Lifetime Demo**
Build the `/lifetimes` endpoint from section 6. Hit it with `curl http://localhost:5000/lifetimes` twice. Confirm:
- Transient Ids differ every time
- Scoped Ids match within a request but differ across requests
- Singleton Ids never change

**Exercise 2 — Captive Dependency**
Register a Singleton that takes `AppDbContext` (Scoped) in its constructor. Run the app and capture the startup error. Then fix it with `IServiceScopeFactory`.

<details>
<summary>💡 Answer</summary>

`Program.cs`:
```csharp
builder.Host.UseDefaultServiceProvider(opts =>
{
    opts.ValidateOnBuild = true;       // fail fast
    opts.ValidateScopes  = true;       // catch captive deps
});
```
You'll see: *"Cannot consume scoped service 'AppDbContext' from singleton..."*.
Fix by injecting `IServiceScopeFactory`.
</details>

**Exercise 3 — Multiple Implementations**
Register three `INotifier` implementations (Email/SMS/Push). Inject `IEnumerable<INotifier>` into a `NotificationService` and loop through them.

**Exercise 4 — Keyed Service**
Register two `IPricingStrategy` implementations (Domestic, International) using keyed DI. Route your `OrderController` to use the right one based on an incoming header.

**Exercise 5 — Open Generics**
Register `IRepository<T>` → `Repository<T>` as open generics. Resolve `IRepository<Vendor>` and `IRepository<User>` from the same registration.

---

## ➡️ Next: [Day 3 — Filters & Global Exception Handling](./Day-03-Filters-Global-Exception-Handling.md)

Tomorrow you'll learn:
- Action filters, Result filters, Exception filters
- The filter pipeline vs middleware pipeline
- `IExceptionHandler` (.NET 8+) for global errors
- ProblemDetails and RFC-7807 error responses

