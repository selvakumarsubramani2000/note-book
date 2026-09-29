# Dependency Injection in .NET: Mastering Service Lifetimes

> **Production-ready guide** to DI container, service lifetimes, and avoiding common pitfalls  
> **Focus**: Memory implications, performance, and real-world scenarios

## Real-World Scenario

**The Problem**:
Your API starts throwing random errors after running for a few hours:
- "Cannot access a disposed object" exceptions
- Memory leaks causing OutOfMemoryException
- DbContext thread-safety violations
- Singleton services holding onto Scoped dependencies

**The Root Cause**: Incorrect service lifetime configuration

**The Impact**:
- Production crashes
- Unpredictable behavior
- Memory bloat
- Difficult-to-reproduce bugs

**The Solution**: Understanding service lifetimes and dependency rules

---

## Table of Contents

1. [Service Lifetimes Explained](#service-lifetimes-explained)
2. [The Dependency Rule](#the-dependency-rule)
3. [Common Scenarios](#common-scenarios)
4. [Memory Implications](#memory-implications)
5. [Common Pitfalls](#common-pitfalls)
6. [Best Practices](#best-practices)
7. [Advanced Patterns](#advanced-patterns)

---

## Service Lifetimes Explained

### The Three Lifetimes

| Lifetime | Created | Disposed | Use Case |
|----------|---------|----------|----------|
| **Transient** | Every time requested | Immediately after use | Lightweight, stateless services |
| **Scoped** | Once per HTTP request | End of HTTP request | DbContext, request-specific services |
| **Singleton** | Once per application | Application shutdown | Configuration, caching, thread-safe services |

### 1. Transient

**Created**: Every time you request it  
**Disposed**: As soon as possible (when scope ends)

```csharp
services.AddTransient<IEmailService, EmailService>();
```

**Example**:
```csharp
public class OrdersController : ControllerBase
{
    private readonly IEmailService _emailService1;
    private readonly IEmailService _emailService2;
    
    public OrdersController(IEmailService emailService1, IEmailService emailService2)
    {
        _emailService1 = emailService1;
        _emailService2 = emailService2;
        
        // These are DIFFERENT instances!
        Console.WriteLine(_emailService1 == _emailService2); // False
    }
}
```

**When to use**:
- ✅ Lightweight services with no state
- ✅ Services that are not thread-safe
- ✅ Services used infrequently

**When NOT to use**:
- ❌ Heavy objects (expensive to create)
- ❌ Services that maintain state
- ❌ DbContext (use Scoped instead)

### 2. Scoped

**Created**: Once per HTTP request (or scope)  
**Disposed**: At the end of the HTTP request

```csharp
services.AddScoped<IOrderRepository, OrderRepository>();
services.AddScoped<ApplicationDbContext>();
```

**Example**:
```csharp
public class OrdersController : ControllerBase
{
    private readonly IOrderRepository _orderRepo1;
    private readonly IOrderRepository _orderRepo2;
    
    public OrdersController(IOrderRepository orderRepo1, IOrderRepository orderRepo2)
    {
        _orderRepo1 = orderRepo1;
        _orderRepo2 = orderRepo2;
        
        // These are the SAME instance (within same HTTP request)!
        Console.WriteLine(_orderRepo1 == _orderRepo2); // True
    }
}
```

**When to use**:
- ✅ **DbContext** (most important!)
- ✅ Repositories
- ✅ Unit of Work
- ✅ Services that need request-specific data (ICurrentUserService)

**When NOT to use**:
- ❌ Services that need to be shared across requests
- ❌ Services that are expensive to create and can be reused

### 3. Singleton

**Created**: Once when first requested  
**Disposed**: When application shuts down

```csharp
services.AddSingleton<ICacheService, RedisCacheService>();
```

**Example**:
```csharp
// First request
var cache1 = serviceProvider.GetService<ICacheService>();

// Second request (different HTTP request, different user)
var cache2 = serviceProvider.GetService<ICacheService>();

// These are the SAME instance!
Console.WriteLine(cache1 == cache2); // True
```

**When to use**:
- ✅ Configuration services
- ✅ Caching services (Redis, MemoryCache)
- ✅ Logging services
- ✅ Thread-safe services with no state
- ✅ Services that are expensive to create

**When NOT to use**:
- ❌ Services that are not thread-safe
- ❌ Services that hold request-specific data
- ❌ **DbContext** (NEVER!)

---

## The Dependency Rule

### ✅ Allowed Dependencies

```
Singleton → Singleton ✅
Scoped → Singleton ✅
Scoped → Scoped ✅
Transient → Singleton ✅
Transient → Scoped ✅
Transient → Transient ✅
```

### ❌ Forbidden Dependencies (Captive Dependencies)

```
Singleton → Scoped ❌ DANGER!
Singleton → Transient ❌ DANGER!
Scoped → Transient ⚠️ Usually OK, but wasteful
```

### Why Captive Dependencies Are Dangerous

**Example of the problem**:
```csharp
// ❌ WRONG: Singleton depends on Scoped
public class CacheService : ICacheService // Registered as Singleton
{
    private readonly ApplicationDbContext _context; // Scoped!
    
    public CacheService(ApplicationDbContext context)
    {
        _context = context; // ❌ DbContext will be held forever!
    }
    
    public async Task<Product> GetProductAsync(int id)
    {
        // ❌ This DbContext was created for the FIRST request
        // and will be reused for ALL subsequent requests!
        // This causes thread-safety issues and stale data!
        return await _context.Products.FindAsync(id);
    }
}
```

**What happens**:
1. First HTTP request creates CacheService (Singleton)
2. CacheService gets a DbContext (Scoped to first request)
3. First request ends, but DbContext is held by Singleton
4. Second HTTP request uses same CacheService
5. Second request uses DbContext from first request ❌
6. **Result**: Thread-safety violations, disposed object exceptions, stale data

**How to fix**:
```csharp
// ✅ CORRECT: Use IServiceProvider to get Scoped service when needed
public class CacheService : ICacheService // Singleton
{
    private readonly IServiceProvider _serviceProvider;
    
    public CacheService(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }
    
    public async Task<Product> GetProductAsync(int id)
    {
        // Create a scope and get DbContext within that scope
        using var scope = _serviceProvider.CreateScope();
        var context = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
        
        return await context.Products.FindAsync(id);
    }
}
```

**Or better**: Don't inject DbContext into Singleton at all. Use a Scoped service instead:
```csharp
// ✅ BEST: Make CacheService Scoped
services.AddScoped<ICacheService, CacheService>();
```

---

## Common Scenarios

### Scenario 1: DbContext Lifetime

**Question**: Should DbContext be Transient, Scoped, or Singleton?

**Answer**: **Always Scoped**

**Why**:
- ❌ **Transient**: New instance for every injection = multiple DbContexts per request = different change trackers = chaos
- ❌ **Singleton**: Shared across all requests = thread-safety issues = disposed object exceptions
- ✅ **Scoped**: One instance per request = consistent change tracking = thread-safe

**Example**:
```csharp
// ✅ CORRECT
services.AddScoped<ApplicationDbContext>();
services.AddScoped<IOrderRepository, OrderRepository>();
services.AddScoped<IProductRepository, ProductRepository>();

// Both repositories will share the same DbContext instance within a request
public class OrderRepository : IOrderRepository
{
    private readonly ApplicationDbContext _context;
    
    public OrderRepository(ApplicationDbContext context)
    {
        _context = context;
    }
}

public class ProductRepository : IProductRepository
{
    private readonly ApplicationDbContext _context; // Same instance as OrderRepository!
    
    public ProductRepository(ApplicationDbContext context)
    {
        _context = context;
    }
}
```

### Scenario 2: Repository Lifetime

**Question**: Should repositories be Transient, Scoped, or Singleton?

**Answer**: **Scoped** (to match DbContext)

**Why**:
- Repositories depend on DbContext (Scoped)
- Should have same lifetime as DbContext
- One repository instance per request is sufficient

```csharp
services.AddScoped<IOrderRepository, OrderRepository>();
services.AddScoped<IProductRepository, ProductRepository>();
```

### Scenario 3: MediatR Handlers

**Question**: What lifetime for Command/Query handlers?

**Answer**: **Transient** (MediatR default)

**Why**:
- Handlers are created, used once, and disposed
- Lightweight and stateless
- Can safely depend on Scoped services (DbContext, repositories)

```csharp
// MediatR registers handlers as Transient by default
services.AddMediatR(cfg => cfg.RegisterServicesFromAssembly(Assembly.GetExecutingAssembly()));
```

**Handler example**:
```csharp
// Transient handler depending on Scoped repository ✅
public class CreateOrderCommandHandler : IRequestHandler<CreateOrderCommand, Result>
{
    private readonly IOrderRepository _orderRepository; // Scoped
    
    public CreateOrderCommandHandler(IOrderRepository orderRepository)
    {
        _orderRepository = orderRepository;
    }
    
    public async Task<Result> Handle(CreateOrderCommand request, CancellationToken ct)
    {
        // Handler is created, executes, and is disposed
        // Repository is scoped to the HTTP request
    }
}
```

### Scenario 4: Caching Service

**Question**: Should caching service be Singleton or Scoped?

**Answer**: **Singleton**

**Why**:
- Cache should be shared across all requests
- Expensive to create (Redis connection)
- Thread-safe by design

```csharp
services.AddSingleton<ICacheService, RedisCacheService>();

// Or use built-in
services.AddMemoryCache(); // Registered as Singleton
services.AddStackExchangeRedisCache(options => { /* ... */ }); // Singleton
```

### Scenario 5: Current User Service

**Question**: Should ICurrentUserService be Singleton, Scoped, or Transient?

**Answer**: **Scoped**

**Why**:
- User is specific to the HTTP request
- Needs access to HttpContext (request-scoped)

```csharp
services.AddScoped<ICurrentUserService, CurrentUserService>();
services.AddHttpContextAccessor(); // Required, registered as Singleton

public class CurrentUserService : ICurrentUserService
{
    private readonly IHttpContextAccessor _httpContextAccessor;
    
    public CurrentUserService(IHttpContextAccessor httpContextAccessor)
    {
        _httpContextAccessor = httpContextAccessor;
    }
    
    public int? UserId
    {
        get
        {
            var userIdClaim = _httpContextAccessor.HttpContext?.User
                .FindFirst(ClaimTypes.NameIdentifier)?.Value;
            
            return int.TryParse(userIdClaim, out var userId) ? userId : null;
        }
    }
}
```

### Scenario 6: Email Service

**Question**: Should email service be Transient, Scoped, or Singleton?

**Answer**: **Depends on implementation**

**Option 1: Transient** (if lightweight):
```csharp
services.AddTransient<IEmailService, EmailService>();

public class EmailService : IEmailService
{
    public async Task SendAsync(string to, string subject, string body)
    {
        // Create SMTP client, send email, dispose
        using var client = new SmtpClient();
        // ...
    }
}
```

**Option 2: Singleton** (if using connection pool):
```csharp
services.AddSingleton<IEmailService, SendGridEmailService>();

public class SendGridEmailService : IEmailService
{
    private readonly SendGridClient _client; // Reusable, thread-safe
    
    public SendGridEmailService(IConfiguration configuration)
    {
        var apiKey = configuration["SendGrid:ApiKey"];
        _client = new SendGridClient(apiKey);
    }
    
    public async Task SendAsync(string to, string subject, string body)
    {
        // Reuse client across all requests
        await _client.SendEmailAsync(/* ... */);
    }
}
```

---

## Memory Implications

### Transient Services

**Memory pattern**:
```
Request 1: Create → Use → Dispose → GC
Request 2: Create → Use → Dispose → GC
Request 3: Create → Use → Dispose → GC
```

**Memory impact**:
- ✅ Low memory footprint (disposed quickly)
- ❌ High GC pressure if created frequently
- ❌ CPU overhead from frequent instantiation

**Example**:
```csharp
// If this is called 1000 times per request:
services.AddTransient<IValidator, OrderValidator>();

// You create 1000 validator instances per request!
// Better: Make it Scoped or Singleton
```

### Scoped Services

**Memory pattern**:
```
Request 1: Create → Use → Use → Use → Dispose
Request 2: Create → Use → Use → Use → Dispose
Request 3: Create → Use → Use → Use → Dispose
```

**Memory impact**:
- ✅ Moderate memory footprint
- ✅ Reused within request (efficient)
- ✅ Disposed at end of request (no leaks)

**Example**:
```csharp
services.AddScoped<ApplicationDbContext>();

// One DbContext per request, no matter how many times injected
// Disposed automatically at end of request
```

### Singleton Services

**Memory pattern**:
```
App Start: Create → Use forever → Dispose on shutdown
```

**Memory impact**:
- ⚠️ Held in memory for entire application lifetime
- ✅ No creation overhead after first use
- ❌ Memory leak if not careful!

**Example of memory leak**:
```csharp
// ❌ MEMORY LEAK!
public class CacheService : ICacheService // Singleton
{
    private readonly List<Order> _cachedOrders = new(); // Grows forever!
    
    public void CacheOrder(Order order)
    {
        _cachedOrders.Add(order); // Never removed!
    }
}
```

**Fix**:
```csharp
// ✅ CORRECT: Use proper cache with expiration
public class CacheService : ICacheService // Singleton
{
    private readonly IMemoryCache _cache;
    
    public CacheService(IMemoryCache cache)
    {
        _cache = cache;
    }
    
    public void CacheOrder(Order order)
    {
        _cache.Set($"order_{order.Id}", order, TimeSpan.FromMinutes(10)); // Expires!
    }
}
```

---

## Common Pitfalls

### Pitfall 1: Captive Dependency (Singleton → Scoped)

**The Problem**:
```csharp
// ❌ WRONG
services.AddSingleton<IOrderService, OrderService>();
services.AddScoped<ApplicationDbContext>();

public class OrderService : IOrderService // Singleton
{
    private readonly ApplicationDbContext _context; // Scoped!

    public OrderService(ApplicationDbContext context)
    {
        _context = context; // ❌ DbContext captured by Singleton!
    }
}
```

**What happens**:
- OrderService is created once at app startup
- It captures the first DbContext instance
- That DbContext is never disposed
- All subsequent requests use the same DbContext
- **Result**: Thread-safety violations, disposed object exceptions

**How to detect**:
```csharp
// Enable scope validation in Development
var builder = WebApplication.CreateBuilder(args);

builder.Host.UseDefaultServiceProvider(options =>
{
    options.ValidateScopes = true; // Throws exception if captive dependency detected
    options.ValidateOnBuild = true; // Validates at startup
});
```

**How to fix**:
```csharp
// Option 1: Change Singleton to Scoped
services.AddScoped<IOrderService, OrderService>();

// Option 2: Use IServiceProvider to create scope
public class OrderService : IOrderService // Singleton
{
    private readonly IServiceProvider _serviceProvider;

    public OrderService(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }

    public async Task<Order> GetOrderAsync(int id)
    {
        using var scope = _serviceProvider.CreateScope();
        var context = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
        return await context.Orders.FindAsync(id);
    }
}
```

### Pitfall 2: Disposing Scoped Services Manually

**The Problem**:
```csharp
// ❌ WRONG
public class OrdersController : ControllerBase
{
    private readonly ApplicationDbContext _context;

    public OrdersController(ApplicationDbContext context)
    {
        _context = context;
    }

    [HttpGet("{id}")]
    public async Task<IActionResult> GetOrder(int id)
    {
        var order = await _context.Orders.FindAsync(id);
        _context.Dispose(); // ❌ DON'T DO THIS!
        return Ok(order);
    }
}
```

**What happens**:
- You dispose the DbContext manually
- ASP.NET Core tries to dispose it again at end of request
- **Result**: ObjectDisposedException

**How to fix**:
```csharp
// ✅ CORRECT: Let DI container handle disposal
public class OrdersController : ControllerBase
{
    private readonly ApplicationDbContext _context;

    public OrdersController(ApplicationDbContext context)
    {
        _context = context;
    }

    [HttpGet("{id}")]
    public async Task<IActionResult> GetOrder(int id)
    {
        var order = await _context.Orders.FindAsync(id);
        // Don't dispose! DI container will do it at end of request
        return Ok(order);
    }
}
```

### Pitfall 3: Multiple DbContext Instances Per Request

**The Problem**:
```csharp
// ❌ WRONG
services.AddTransient<ApplicationDbContext>(); // Transient!

public class OrderService
{
    private readonly ApplicationDbContext _context;

    public OrderService(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task CreateOrderAsync(Order order)
    {
        _context.Orders.Add(order);
        await _context.SaveChangesAsync();
    }
}

public class ProductService
{
    private readonly ApplicationDbContext _context;

    public ProductService(ApplicationDbContext context)
    {
        _context = context; // Different instance!
    }

    public async Task UpdateStockAsync(int productId, int quantity)
    {
        var product = await _context.Products.FindAsync(productId);
        product.StockQuantity -= quantity;
        await _context.SaveChangesAsync();
    }
}

// In handler:
public class CreateOrderCommandHandler
{
    private readonly OrderService _orderService;
    private readonly ProductService _productService;

    public async Task Handle(CreateOrderCommand request)
    {
        await _orderService.CreateOrderAsync(order); // Uses DbContext #1
        await _productService.UpdateStockAsync(productId, qty); // Uses DbContext #2

        // ❌ Changes are in different DbContexts!
        // ❌ No transaction coordination!
    }
}
```

**How to fix**:
```csharp
// ✅ CORRECT: Use Scoped
services.AddScoped<ApplicationDbContext>();

// Now both services share the same DbContext instance per request
```

### Pitfall 4: Injecting IServiceProvider Everywhere

**The Problem**:
```csharp
// ❌ ANTI-PATTERN: Service Locator
public class OrderService
{
    private readonly IServiceProvider _serviceProvider;

    public OrderService(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }

    public async Task CreateOrderAsync(Order order)
    {
        var repo = _serviceProvider.GetRequiredService<IOrderRepository>();
        var emailService = _serviceProvider.GetRequiredService<IEmailService>();
        var cache = _serviceProvider.GetRequiredService<ICacheService>();

        // ❌ Hides dependencies
        // ❌ Hard to test
        // ❌ Runtime errors instead of compile-time errors
    }
}
```

**Why it's bad**:
- Hides dependencies (can't see what service needs from constructor)
- Hard to test (need to mock IServiceProvider)
- Runtime errors if service not registered
- Defeats the purpose of DI

**How to fix**:
```csharp
// ✅ CORRECT: Explicit dependencies
public class OrderService
{
    private readonly IOrderRepository _orderRepository;
    private readonly IEmailService _emailService;
    private readonly ICacheService _cacheService;

    public OrderService(
        IOrderRepository orderRepository,
        IEmailService emailService,
        ICacheService cacheService)
    {
        _orderRepository = orderRepository;
        _emailService = emailService;
        _cacheService = cacheService;
    }

    // ✅ Dependencies are explicit
    // ✅ Easy to test (mock interfaces)
    // ✅ Compile-time safety
}
```

**When IServiceProvider is OK**:
- Creating scopes in Singleton services (shown earlier)
- Factory patterns
- Plugin systems

### Pitfall 5: Forgetting to Register Services

**The Problem**:
```csharp
// Program.cs
services.AddScoped<IOrderRepository, OrderRepository>();
// Forgot to register IProductRepository!

// Controller
public class OrdersController
{
    private readonly IOrderRepository _orderRepository;
    private readonly IProductRepository _productRepository; // Not registered!

    public OrdersController(
        IOrderRepository orderRepository,
        IProductRepository productRepository)
    {
        _orderRepository = orderRepository;
        _productRepository = productRepository; // ❌ Runtime error!
    }
}
```

**Error**:
```
InvalidOperationException: Unable to resolve service for type 'IProductRepository'
```

**How to prevent**:
```csharp
// Option 1: Validate on build
builder.Host.UseDefaultServiceProvider(options =>
{
    options.ValidateOnBuild = true; // Fails at startup if service missing
});

// Option 2: Use extension methods to group registrations
public static class DependencyInjection
{
    public static IServiceCollection AddRepositories(this IServiceCollection services)
    {
        services.AddScoped<IOrderRepository, OrderRepository>();
        services.AddScoped<IProductRepository, ProductRepository>();
        services.AddScoped<IUserRepository, UserRepository>();
        // All repositories in one place

        return services;
    }
}

// Program.cs
services.AddRepositories();
```

### Pitfall 6: Circular Dependencies

**The Problem**:
```csharp
public class OrderService
{
    private readonly ProductService _productService;

    public OrderService(ProductService productService)
    {
        _productService = productService;
    }
}

public class ProductService
{
    private readonly OrderService _orderService; // ❌ Circular!

    public ProductService(OrderService orderService)
    {
        _orderService = orderService;
    }
}
```

**Error**:
```
InvalidOperationException: A circular dependency was detected
```

**How to fix**:
```csharp
// Option 1: Extract shared logic to a third service
public class InventoryService
{
    // Shared logic
}

public class OrderService
{
    private readonly InventoryService _inventoryService;

    public OrderService(InventoryService inventoryService)
    {
        _inventoryService = inventoryService;
    }
}

public class ProductService
{
    private readonly InventoryService _inventoryService;

    public ProductService(InventoryService inventoryService)
    {
        _inventoryService = inventoryService;
    }
}

// Option 2: Use events/mediator pattern
public class OrderService
{
    private readonly IMediator _mediator;

    public async Task CreateOrderAsync(Order order)
    {
        // Instead of calling ProductService directly, publish event
        await _mediator.Publish(new OrderCreatedEvent { OrderId = order.Id });
    }
}

public class ProductService : INotificationHandler<OrderCreatedEvent>
{
    public async Task Handle(OrderCreatedEvent notification)
    {
        // React to event
    }
}
```

---

## Best Practices

### 1. Use Extension Methods for Registration

**Organize by layer**:
```csharp
// Application/DependencyInjection.cs
public static class DependencyInjection
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        services.AddMediatR(cfg => cfg.RegisterServicesFromAssembly(Assembly.GetExecutingAssembly()));
        services.AddValidatorsFromAssembly(Assembly.GetExecutingAssembly());
        services.AddAutoMapper(Assembly.GetExecutingAssembly());

        return services;
    }
}

// Infrastructure/DependencyInjection.cs
public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        // Database
        services.AddDbContext<ApplicationDbContext>(options =>
            options.UseSqlServer(configuration.GetConnectionString("DefaultConnection")));

        // Repositories
        services.AddScoped<IOrderRepository, OrderRepository>();
        services.AddScoped<IProductRepository, ProductRepository>();

        // Services
        services.AddScoped<IEmailService, EmailService>();
        services.AddSingleton<ICacheService, RedisCacheService>();

        return services;
    }
}

// Program.cs
builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);
```

### 2. Enable Scope Validation in Development

```csharp
var builder = WebApplication.CreateBuilder(args);

if (builder.Environment.IsDevelopment())
{
    builder.Host.UseDefaultServiceProvider(options =>
    {
        options.ValidateScopes = true; // Detect captive dependencies
        options.ValidateOnBuild = true; // Validate at startup
    });
}
```

### 3. Use TryAdd for Optional Services

```csharp
// Won't throw if already registered
services.TryAddScoped<IEmailService, EmailService>();

// Useful for libraries that provide default implementations
// but allow users to override
```

### 4. Register Multiple Implementations

```csharp
// Register multiple implementations
services.AddScoped<INotificationService, EmailNotificationService>();
services.AddScoped<INotificationService, SmsNotificationService>();
services.AddScoped<INotificationService, PushNotificationService>();

// Inject all implementations
public class NotificationService
{
    private readonly IEnumerable<INotificationService> _notificationServices;

    public NotificationService(IEnumerable<INotificationService> notificationServices)
    {
        _notificationServices = notificationServices;
    }

    public async Task NotifyAllAsync(string message)
    {
        foreach (var service in _notificationServices)
        {
            await service.SendAsync(message);
        }
    }
}
```

### 5. Use Keyed Services (.NET 8+)

```csharp
// Register with keys
services.AddKeyedScoped<IPaymentService, StripePaymentService>("stripe");
services.AddKeyedScoped<IPaymentService, PayPalPaymentService>("paypal");

// Inject specific implementation
public class OrderService
{
    private readonly IPaymentService _paymentService;

    public OrderService([FromKeyedServices("stripe")] IPaymentService paymentService)
    {
        _paymentService = paymentService;
    }
}
```

### 6. Use Factory Pattern for Complex Creation

```csharp
// Register factory
services.AddSingleton<IPaymentServiceFactory, PaymentServiceFactory>();

public interface IPaymentServiceFactory
{
    IPaymentService Create(PaymentMethod method);
}

public class PaymentServiceFactory : IPaymentServiceFactory
{
    private readonly IServiceProvider _serviceProvider;

    public PaymentServiceFactory(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }

    public IPaymentService Create(PaymentMethod method)
    {
        return method switch
        {
            PaymentMethod.CreditCard => _serviceProvider.GetRequiredService<StripePaymentService>(),
            PaymentMethod.PayPal => _serviceProvider.GetRequiredService<PayPalPaymentService>(),
            _ => throw new ArgumentException("Invalid payment method")
        };
    }
}

// Usage
public class OrderService
{
    private readonly IPaymentServiceFactory _paymentServiceFactory;

    public async Task ProcessPaymentAsync(Order order)
    {
        var paymentService = _paymentServiceFactory.Create(order.PaymentMethod);
        await paymentService.ProcessAsync(order.Total);
    }
}
```

### 7. Avoid Constructor Over-Injection

**Problem**:
```csharp
// ❌ Too many dependencies (code smell!)
public class OrderService
{
    public OrderService(
        IOrderRepository orderRepository,
        IProductRepository productRepository,
        IUserRepository userRepository,
        IEmailService emailService,
        ISmsService smsService,
        ICacheService cacheService,
        ILogger<OrderService> logger,
        IMapper mapper,
        IMediator mediator,
        IConfiguration configuration)
    {
        // 10+ dependencies = doing too much!
    }
}
```

**Solution**:
```csharp
// ✅ Split into smaller services
public class OrderService
{
    private readonly IOrderRepository _orderRepository;
    private readonly INotificationService _notificationService; // Abstracts email/SMS
    private readonly ILogger<OrderService> _logger;

    public OrderService(
        IOrderRepository orderRepository,
        INotificationService notificationService,
        ILogger<OrderService> logger)
    {
        _orderRepository = orderRepository;
        _notificationService = notificationService;
        _logger = logger;
    }
}
```

---

## Advanced Patterns

### Pattern 1: Decorator Pattern

**Use case**: Add behavior to existing service without modifying it

```csharp
// Base service
public interface IOrderService
{
    Task<Order> GetOrderAsync(int id);
}

public class OrderService : IOrderService
{
    private readonly IOrderRepository _orderRepository;

    public OrderService(IOrderRepository orderRepository)
    {
        _orderRepository = orderRepository;
    }

    public async Task<Order> GetOrderAsync(int id)
    {
        return await _orderRepository.GetByIdAsync(id);
    }
}

// Decorator: Add caching
public class CachedOrderService : IOrderService
{
    private readonly IOrderService _innerService;
    private readonly ICacheService _cacheService;

    public CachedOrderService(IOrderService innerService, ICacheService cacheService)
    {
        _innerService = innerService;
        _cacheService = cacheService;
    }

    public async Task<Order> GetOrderAsync(int id)
    {
        var cacheKey = $"order_{id}";
        var cached = await _cacheService.GetAsync<Order>(cacheKey);
        if (cached != null) return cached;

        var order = await _innerService.GetOrderAsync(id);
        await _cacheService.SetAsync(cacheKey, order, TimeSpan.FromMinutes(10));

        return order;
    }
}

// Registration
services.AddScoped<OrderService>(); // Concrete implementation
services.AddScoped<IOrderService>(sp =>
{
    var orderService = sp.GetRequiredService<OrderService>();
    var cacheService = sp.GetRequiredService<ICacheService>();
    return new CachedOrderService(orderService, cacheService);
});
```

### Pattern 2: Options Pattern

**Use case**: Inject configuration as strongly-typed objects

```csharp
// Configuration class
public class EmailSettings
{
    public string SmtpServer { get; set; }
    public int Port { get; set; }
    public string Username { get; set; }
    public string Password { get; set; }
}

// appsettings.json
{
  "EmailSettings": {
    "SmtpServer": "smtp.gmail.com",
    "Port": 587,
    "Username": "user@example.com",
    "Password": "password"
  }
}

// Registration
services.Configure<EmailSettings>(builder.Configuration.GetSection("EmailSettings"));

// Usage
public class EmailService : IEmailService
{
    private readonly EmailSettings _settings;

    public EmailService(IOptions<EmailSettings> options)
    {
        _settings = options.Value;
    }

    public async Task SendAsync(string to, string subject, string body)
    {
        // Use _settings.SmtpServer, _settings.Port, etc.
    }
}
```

### Pattern 3: Named Options

```csharp
// Multiple configurations
services.Configure<EmailSettings>("Primary", config.GetSection("PrimaryEmail"));
services.Configure<EmailSettings>("Secondary", config.GetSection("SecondaryEmail"));

// Usage
public class EmailService
{
    private readonly EmailSettings _primarySettings;
    private readonly EmailSettings _secondarySettings;

    public EmailService(IOptionsSnapshot<EmailSettings> options)
    {
        _primarySettings = options.Get("Primary");
        _secondarySettings = options.Get("Secondary");
    }
}
```

---

## Summary

### Quick Reference

| Service Type | Lifetime | Use Case | Example |
|--------------|----------|----------|---------|
| **DbContext** | Scoped | Database access | `ApplicationDbContext` |
| **Repository** | Scoped | Data access | `OrderRepository` |
| **MediatR Handler** | Transient | Command/Query handling | `CreateOrderCommandHandler` |
| **Cache** | Singleton | Shared cache | `RedisCacheService` |
| **Logger** | Singleton | Logging | `ILogger<T>` |
| **Current User** | Scoped | Request-specific user | `CurrentUserService` |
| **Email Service** | Transient/Singleton | Depends on implementation | `EmailService` |
| **Configuration** | Singleton | App settings | `IOptions<T>` |

### Key Takeaways

1. **DbContext is always Scoped** - Never Transient or Singleton
2. **Repositories match DbContext lifetime** - Scoped
3. **Avoid captive dependencies** - Singleton can't depend on Scoped
4. **Enable scope validation in Development** - Catch errors early
5. **Don't dispose Scoped services manually** - Let DI container handle it
6. **Use extension methods for registration** - Organize by layer
7. **Avoid IServiceProvider injection** - Use explicit dependencies
8. **Watch for memory leaks in Singletons** - Use proper caching with expiration

### Common Mistakes to Avoid

❌ Singleton depending on Scoped (captive dependency)
❌ DbContext as Transient or Singleton
❌ Manually disposing Scoped services
❌ Injecting IServiceProvider everywhere
❌ Forgetting to register services
❌ Circular dependencies

---

## Next Steps

1. **Practice with a sample project** - Implement different lifetimes
2. **Enable scope validation** - Catch errors in development
3. **Read about MediatR** - Understand pipeline behaviors
4. **Learn about Options pattern** - Strongly-typed configuration
5. **Study Decorator pattern** - Add behavior without modifying code

### Related Guides

- **Clean Architecture** - How DI fits into layered architecture
- **Repository Pattern** - When to use Scoped vs Transient
- **Performance Optimization** - Impact of service lifetimes on performance
- **Testing** - How to mock dependencies in unit tests

---

**Remember**: Service lifetime is not just about when objects are created and disposed - it's about correctness, performance, and memory management. Choose wisely! 🎯
```
