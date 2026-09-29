# Question 7: What is Dependency Injection? Explain its types in .NET Core Web API.

## Answer

### What is Dependency Injection (DI)?

**Dependency Injection** is a design pattern where objects receive their dependencies from external sources rather than creating them internally.

Think of it like this:
- **Without DI**: "I'll make my own coffee" (create dependencies yourself)
- **With DI**: "Someone brings me coffee" (dependencies are provided to you)

---

## Why Use Dependency Injection?

### 1. **Loose Coupling**
Classes don't create their own dependencies, making them independent

### 2. **Testability**
Easy to mock dependencies for unit testing

### 3. **Maintainability**
Change implementations without modifying the class

### 4. **Follows SOLID Principles**
Especially Dependency Inversion Principle

---

## Example: Without DI vs With DI

### ❌ Without Dependency Injection (Bad)

```csharp
public class OrderService
{
    // Creating dependency directly - TIGHT COUPLING!
    private readonly SqlServerDatabase _database = new SqlServerDatabase();
    private readonly EmailService _emailService = new EmailService();
    
    public void CreateOrder(Order order)
    {
        _database.Save(order);
        _emailService.SendOrderConfirmation(order);
    }
}

// Problems:
// 1. Hard to test - can't mock SqlServerDatabase or EmailService
// 2. Hard to change - what if you want to use MongoDB instead?
// 3. OrderService is responsible for creating its dependencies
```

### ✅ With Dependency Injection (Good)

```csharp
// Define interfaces (abstractions)
public interface IDatabase
{
    void Save(Order order);
}

public interface IEmailService
{
    void SendOrderConfirmation(Order order);
}

// OrderService depends on abstractions, not concrete implementations
public class OrderService
{
    private readonly IDatabase _database;
    private readonly IEmailService _emailService;
    
    // Dependencies are INJECTED through constructor
    public OrderService(IDatabase database, IEmailService emailService)
    {
        _database = database;
        _emailService = emailService;
    }
    
    public void CreateOrder(Order order)
    {
        _database.Save(order);
        _emailService.SendOrderConfirmation(order);
    }
}

// Concrete implementations
public class SqlServerDatabase : IDatabase
{
    public void Save(Order order) { /* SQL Server logic */ }
}

public class EmailService : IEmailService
{
    public void SendOrderConfirmation(Order order) { /* Email logic */ }
}
```

---

## Dependency Injection in .NET Core

In .NET Core, DI is **built-in**! You register services in `Startup.cs` or `Program.cs`.

### Registration in Startup.cs

```csharp
public class Startup
{
    public void ConfigureServices(IServiceCollection services)
    {
        // Register services here
        services.AddScoped<IDatabase, SqlServerDatabase>();
        services.AddScoped<IEmailService, EmailService>();
        services.AddScoped<OrderService>();
    }
}
```

### Using in Controllers

```csharp
[ApiController]
[Route("api/[controller]")]
public class OrdersController : ControllerBase
{
    private readonly OrderService _orderService;
    
    // DI container automatically injects OrderService
    public OrdersController(OrderService orderService)
    {
        _orderService = orderService;
    }
    
    [HttpPost]
    public IActionResult CreateOrder([FromBody] Order order)
    {
        _orderService.CreateOrder(order);
        return Ok("Order created successfully");
    }
}
```

---

## Types of Dependency Injection Lifetimes

.NET Core supports **three lifetimes** for services:

### 1. **Transient** (`AddTransient`)

**Lifetime**: Created **every time** they are requested

**Use when**: 
- Lightweight, stateless services
- Operations that don't maintain state
- Short-lived operations

```csharp
services.AddTransient<IEmailService, EmailService>();

// Every time you request IEmailService, a NEW instance is created
// Request 1: new EmailService() - Instance A
// Request 2: new EmailService() - Instance B (different instance)
// Request 3: new EmailService() - Instance C (different instance)
```

**Example Scenario:**
```csharp
public class EmailService : IEmailService
{
    public EmailService()
    {
        Console.WriteLine("EmailService created");
    }
    
    public void Send(string message)
    {
        // Send email
    }
}

// In controller:
public class OrderController : ControllerBase
{
    private readonly IEmailService _emailService1;
    private readonly IEmailService _emailService2;
    
    public OrderController(IEmailService emailService1, IEmailService emailService2)
    {
        _emailService1 = emailService1; // New instance
        _emailService2 = emailService2; // Another new instance
        
        // Output: "EmailService created" twice
    }
}
```

---

### 2. **Scoped** (`AddScoped`)

**Lifetime**: Created **once per HTTP request** (or scope)

**Use when**:
- Database contexts (DbContext)
- Repository patterns
- Services that maintain state within a request
- **Most common for web applications**

```csharp
services.AddScoped<IUserRepository, UserRepository>();

// Within the same HTTP request, the SAME instance is used
// Request 1: new UserRepository() - Used for entire request 1
// Request 2: new UserRepository() - New instance for request 2
```

**Example Scenario:**
```csharp
public class UserRepository : IUserRepository
{
    private readonly AppDbContext _context;
    
    public UserRepository(AppDbContext context)
    {
        _context = context; // Same DbContext throughout the request
    }
}

// Register as Scoped
services.AddScoped<AppDbContext>();
services.AddScoped<IUserRepository, UserRepository>();

// In controller:
public class UserController : ControllerBase
{
    private readonly IUserRepository _repo1;
    private readonly IUserRepository _repo2;
    
    public UserController(IUserRepository repo1, IUserRepository repo2)
    {
        _repo1 = repo1; // Same instance
        _repo2 = repo2; // Same instance (within same request)
        
        // _repo1 and _repo2 are THE SAME object
    }
}
```

**Real-world example:**
```csharp
services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(Configuration.GetConnectionString("DefaultConnection")));

// DbContext is Scoped by default
// One DbContext per HTTP request
// Disposed automatically after request completes
```

---

### 3. **Singleton** (`AddSingleton`)

**Lifetime**: Created **once** and shared across the **entire application lifetime**

**Use when**:
- Configuration settings
- Caching services
- Logging services
- Services without state or with thread-safe state
- **Be careful with thread safety!**

```csharp
services.AddSingleton<ICacheService, CacheService>();

// Created ONCE when first requested
// Same instance used for ALL requests throughout app lifetime
```

**Example Scenario:**
```csharp
public class CacheService : ICacheService
{
    private readonly Dictionary<string, object> _cache = new();
    
    public CacheService()
    {
        Console.WriteLine("CacheService created - happens ONCE");
    }
    
    public void Set(string key, object value)
    {
        _cache[key] = value; // Shared across all users!
    }
}

// Register as Singleton
services.AddSingleton<ICacheService, CacheService>();

// All controllers, all requests use the SAME CacheService instance
```

**Configuration example:**
```csharp
public class AppSettings
{
    public string ApiKey { get; set; }
    public string BaseUrl { get; set; }
}

// Register as Singleton
services.Configure<AppSettings>(Configuration.GetSection("AppSettings"));
services.AddSingleton<IConfiguration>(Configuration);
```

---

## Lifetime Comparison Table

| Lifetime | Created | Disposed | Use Case | Example |
|----------|---------|----------|----------|---------|
| **Transient** | Every request | Immediately after use | Lightweight, stateless operations | EmailService, Logger |
| **Scoped** | Once per HTTP request | End of request | Database contexts, repositories | DbContext, UnitOfWork |
| **Singleton** | Once per app lifetime | App shutdown | Configuration, caching | AppSettings, MemoryCache |

---

## Visual Representation

```
Application Start
│
├─ HTTP Request 1
│  ├─ Singleton (Instance A) ─────┐
│  ├─ Scoped (Instance 1)         │
│  └─ Transient (New each time)   │
│                                  │
├─ HTTP Request 2                  │
│  ├─ Singleton (Instance A) ◄────┘ (Same instance!)
│  ├─ Scoped (Instance 2)         
│  └─ Transient (New each time)   
│
└─ HTTP Request 3
   ├─ Singleton (Instance A) ◄───── (Still same instance!)
   ├─ Scoped (Instance 3)
   └─ Transient (New each time)
```

---

## Common Registration Patterns

```csharp
public void ConfigureServices(IServiceCollection services)
{
    // Transient - lightweight services
    services.AddTransient<IEmailService, EmailService>();
    services.AddTransient<ISmsService, SmsService>();
    
    // Scoped - database and repositories
    services.AddDbContext<AppDbContext>(); // Scoped by default
    services.AddScoped<IUserRepository, UserRepository>();
    services.AddScoped<IOrderRepository, OrderRepository>();
    services.AddScoped<IUnitOfWork, UnitOfWork>();
    
    // Singleton - configuration and caching
    services.AddSingleton<IConfiguration>(Configuration);
    services.AddSingleton<IMemoryCache, MemoryCache>();
    services.AddSingleton<ILogger, Logger>();
    
    // Built-in services
    services.AddControllers();
    services.AddHttpClient(); // Singleton HttpClientFactory
}
```

---

## Best Practices

1. ✅ **Default to Scoped** for most services in web APIs
2. ✅ **Use Transient** for stateless, lightweight services
3. ✅ **Use Singleton** carefully - ensure thread safety
4. ✅ **Always depend on interfaces**, not concrete classes
5. ❌ **Don't inject Scoped into Singleton** (will cause issues)

```csharp
// ❌ BAD - Scoped service in Singleton
services.AddSingleton<MySingletonService>(); // Depends on DbContext
services.AddScoped<DbContext>(); // This will cause problems!

// ✅ GOOD - Match lifetimes appropriately
services.AddScoped<MyService>();
services.AddScoped<DbContext>();
```

---

## Summary

**Dependency Injection = Providing dependencies from outside**

**Three Lifetimes:**
- **Transient**: New every time
- **Scoped**: New per request
- **Singleton**: One for entire app

Choose based on your needs and state management requirements!
