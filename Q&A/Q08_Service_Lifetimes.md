# Question 8: What is the difference between Scoped, Transient, and Singleton lifetimes?

## Answer

This is one of the most important concepts in .NET Core Dependency Injection! Let me explain each lifetime with detailed examples.

---

## Quick Summary

| Lifetime | When Created | When Destroyed | Instances |
|----------|-------------|----------------|-----------|
| **Transient** | Every time requested | After use | Many (new each time) |
| **Scoped** | Once per HTTP request | End of request | One per request |
| **Singleton** | Once for entire app | App shutdown | One for entire app |

---

## 1. Transient Lifetime

### Definition
A **new instance is created every single time** the service is requested from the container.

### Registration
```csharp
services.AddTransient<IEmailService, EmailService>();
```

### Detailed Example

```csharp
public class EmailService : IEmailService
{
    private readonly Guid _instanceId;
    
    public EmailService()
    {
        _instanceId = Guid.NewGuid();
        Console.WriteLine($"EmailService created with ID: {_instanceId}");
    }
    
    public void Send(string message)
    {
        Console.WriteLine($"Sending email from instance: {_instanceId}");
    }
}

public class OrderController : ControllerBase
{
    private readonly IEmailService _emailService1;
    private readonly IEmailService _emailService2;
    
    public OrderController(IEmailService emailService1, IEmailService emailService2)
    {
        _emailService1 = emailService1; // New instance - ID: ABC123
        _emailService2 = emailService2; // Different instance - ID: DEF456
    }
    
    [HttpPost]
    public IActionResult CreateOrder()
    {
        _emailService1.Send("Order created"); // Instance: ABC123
        _emailService2.Send("Order created"); // Instance: DEF456
        return Ok();
    }
}

// Output when endpoint is hit:
// EmailService created with ID: abc-123-def
// EmailService created with ID: xyz-789-ghi
// Sending email from instance: abc-123-def
// Sending email from instance: xyz-789-ghi
```

### When to Use Transient

✅ **Good for:**
- Lightweight services
- Stateless services
- Services that don't hold resources
- Operations that are quick and don't maintain state

**Examples:**
- Email services
- SMS services
- Validators
- Simple calculators
- Formatters

❌ **Avoid for:**
- Database contexts
- Services that maintain state
- Services with expensive initialization
- Services that hold resources (file handles, connections)

---

## 2. Scoped Lifetime

### Definition
A **new instance is created once per client request** (HTTP request in web apps). The same instance is used throughout that request.

### Registration
```csharp
services.AddScoped<IUserRepository, UserRepository>();
```

### Detailed Example

```csharp
public class UserRepository : IUserRepository
{
    private readonly Guid _instanceId;
    private readonly AppDbContext _context;
    
    public UserRepository(AppDbContext context)
    {
        _instanceId = Guid.NewGuid();
        _context = context;
        Console.WriteLine($"UserRepository created with ID: {_instanceId}");
    }
    
    public User GetUser(int id)
    {
        Console.WriteLine($"Getting user from instance: {_instanceId}");
        return _context.Users.Find(id);
    }
}

public class UserService
{
    private readonly IUserRepository _repository;
    
    public UserService(IUserRepository repository)
    {
        _repository = repository; // Same instance as controller
    }
    
    public User GetUserProfile(int id)
    {
        return _repository.GetUser(id);
    }
}

public class UserController : ControllerBase
{
    private readonly IUserRepository _repository;
    private readonly UserService _service;
    
    public UserController(IUserRepository repository, UserService service)
    {
        _repository = repository; // Instance: ABC123
        _service = service;       // Uses same repository instance: ABC123
    }
    
    [HttpGet("{id}")]
    public IActionResult GetUser(int id)
    {
        var user1 = _repository.GetUser(id);       // Instance: ABC123
        var user2 = _service.GetUserProfile(id);   // Same instance: ABC123
        return Ok(user1);
    }
}

// Output for Request 1:
// UserRepository created with ID: abc-123
// Getting user from instance: abc-123
// Getting user from instance: abc-123

// Output for Request 2 (new HTTP request):
// UserRepository created with ID: xyz-789
// Getting user from instance: xyz-789
// Getting user from instance: xyz-789
```

### When to Use Scoped

✅ **Good for:**
- **Database contexts (DbContext)** - Most common use!
- Repository patterns
- Unit of Work pattern
- Services that need to maintain state within a request
- Services that should be shared within a request but not across requests

**Examples:**
- Entity Framework DbContext
- Repositories
- Unit of Work
- Request-specific caching
- User context/session information

❌ **Avoid for:**
- Background services
- Singleton services (can't inject scoped into singleton)

---

## 3. Singleton Lifetime

### Definition
A **single instance is created once** when first requested and **reused for the entire application lifetime**.

### Registration
```csharp
services.AddSingleton<ICacheService, CacheService>();
```

### Detailed Example

```csharp
public class CacheService : ICacheService
{
    private readonly Guid _instanceId;
    private readonly Dictionary<string, object> _cache;
    
    public CacheService()
    {
        _instanceId = Guid.NewGuid();
        _cache = new Dictionary<string, object>();
        Console.WriteLine($"CacheService created with ID: {_instanceId}");
    }
    
    public void Set(string key, object value)
    {
        Console.WriteLine($"Setting cache from instance: {_instanceId}");
        _cache[key] = value;
    }
    
    public object Get(string key)
    {
        Console.WriteLine($"Getting cache from instance: {_instanceId}");
        return _cache.ContainsKey(key) ? _cache[key] : null;
    }
}

// Request 1
public class UserController : ControllerBase
{
    private readonly ICacheService _cache;
    
    public UserController(ICacheService cache)
    {
        _cache = cache; // Instance: ABC123
    }
    
    [HttpPost]
    public IActionResult CacheUser()
    {
        _cache.Set("user1", "John"); // Instance: ABC123
        return Ok();
    }
}

// Request 2 (different request, same instance!)
public class ProductController : ControllerBase
{
    private readonly ICacheService _cache;
    
    public ProductController(ICacheService cache)
    {
        _cache = cache; // SAME instance: ABC123
    }
    
    [HttpGet]
    public IActionResult GetCachedUser()
    {
        var user = _cache.Get("user1"); // Can access data from Request 1!
        return Ok(user); // Returns "John"
    }
}

// Output (across multiple requests):
// CacheService created with ID: abc-123  (only created ONCE)
// Setting cache from instance: abc-123
// Getting cache from instance: abc-123   (same instance)
```

### When to Use Singleton

✅ **Good for:**
- Configuration settings
- Logging services (with thread-safe implementation)
- Caching services
- Services that are expensive to create
- Thread-safe stateless services
- Application-wide shared resources

**Examples:**
- IConfiguration
- IMemoryCache
- ILogger (if implemented correctly)
- Application settings
- Feature flags
- Third-party API clients (if thread-safe)

❌ **Avoid for:**
- Services that maintain user-specific state
- Database contexts
- Services that aren't thread-safe
- **Never inject Scoped or Transient dependencies into Singleton!**

---

## Critical Rule: Service Lifetime Hierarchy

```
Singleton
    ↓ Can use
Singleton

Scoped
    ↓ Can use
Scoped, Singleton

Transient
    ↓ Can use
Transient, Scoped, Singleton
```

### ❌ WRONG - Will cause problems!

```csharp
// DON'T DO THIS!
services.AddSingleton<MySingletonService>(); // Lives forever
services.AddScoped<DbContext>(); // Lives per request

public class MySingletonService
{
    // ❌ PROBLEM: Singleton trying to use Scoped service!
    // DbContext will be "captured" and won't be disposed properly
    public MySingletonService(DbContext context)
    {
        // This DbContext will live forever, causing memory leaks!
    }
}
```

### ✅ CORRECT - Proper hierarchy

```csharp
services.AddScoped<MyService>();
services.AddScoped<DbContext>();

public class MyService
{
    // ✅ GOOD: Scoped can use Scoped
    public MyService(DbContext context)
    {
        // Both are created and disposed per request
    }
}
```

---

## Practical Example: E-Commerce Application

```csharp
public void ConfigureServices(IServiceCollection services)
{
    // Singleton - Application-wide shared services
    services.AddSingleton<IMemoryCache, MemoryCache>();
    services.AddSingleton<IConfiguration>(Configuration);
    services.AddSingleton<IHttpContextAccessor, HttpContextAccessor>();
    
    // Scoped - Per-request services (most common)
    services.AddDbContext<AppDbContext>(); // Scoped by default
    services.AddScoped<IUserRepository, UserRepository>();
    services.AddScoped<IProductRepository, ProductRepository>();
    services.AddScoped<IOrderRepository, OrderRepository>();
    services.AddScoped<IUnitOfWork, UnitOfWork>();
    services.AddScoped<IUserService, UserService>();
    services.AddScoped<IOrderService, OrderService>();
    
    // Transient - Lightweight, stateless services
    services.AddTransient<IEmailService, EmailService>();
    services.AddTransient<ISmsService, SmsService>();
    services.AddTransient<INotificationService, NotificationService>();
    services.AddTransient<IPdfGenerator, PdfGenerator>();
}
```

---

## Memory & Performance Considerations

### Transient
- ⚠️ **Can create many objects** → More memory allocations
- ⚠️ **More garbage collection** if used heavily
- ✅ **No state management issues**

### Scoped
- ✅ **Balanced** - One instance per request
- ✅ **Perfect for DbContext** - tracks changes during request
- ✅ **Automatic cleanup** after request

### Singleton
- ✅ **Best performance** - created once
- ✅ **Minimal memory** - single instance
- ⚠️ **Must be thread-safe!**
- ⚠️ **Can cause memory leaks** if not careful

---

## Quick Decision Guide

**Ask yourself:**

1. **Does it maintain state specific to a request?**
   → Use **Scoped**

2. **Is it a database context?**
   → Use **Scoped** (always!)

3. **Is it lightweight and stateless?**
   → Use **Transient**

4. **Does it need to be shared across the entire app?**
   → Use **Singleton** (ensure thread-safety!)

5. **Not sure?**
   → Default to **Scoped** - it's the safest choice for web APIs

---

## Summary

- **Transient**: New every time = Many instances
- **Scoped**: New per request = One per request
- **Singleton**: One forever = One for entire app

**Most common in Web APIs: Scoped** (especially for repositories and DbContext)
