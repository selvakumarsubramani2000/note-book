# Question 21: What design patterns have you used in your projects? Explain one in detail.

## Answer

Design patterns are proven solutions to common software design problems. Here are the most commonly used patterns in .NET projects.

---

## Most Common Design Patterns in .NET

### 1. Repository Pattern ⭐⭐⭐ (Most Used)

**Purpose**: Abstract data access logic from business logic

**Problem**: Business logic shouldn't know about database details  
**Solution**: Create a layer between business logic and data access

```csharp
// Interface
public interface IRepository<T> where T : class
{
    Task<T> GetByIdAsync(int id);
    Task<IEnumerable<T>> GetAllAsync();
    Task<T> AddAsync(T entity);
    Task UpdateAsync(T entity);
    Task DeleteAsync(int id);
}

// Implementation
public class ProductRepository : IRepository<Product>
{
    private readonly AppDbContext _context;
    
    public ProductRepository(AppDbContext context)
    {
        _context = context;
    }
    
    public async Task<Product> GetByIdAsync(int id)
    {
        return await _context.Products
            .Include(p => p.Category)
            .FirstOrDefaultAsync(p => p.ProductId == id);
    }
    
    public async Task<IEnumerable<Product>> GetAllAsync()
    {
        return await _context.Products.ToListAsync();
    }
    
    public async Task<Product> AddAsync(Product entity)
    {
        _context.Products.Add(entity);
        await _context.SaveChangesAsync();
        return entity;
    }
    
    public async Task UpdateAsync(Product entity)
    {
        _context.Products.Update(entity);
        await _context.SaveChangesAsync();
    }
    
    public async Task DeleteAsync(int id)
    {
        var product = await GetByIdAsync(id);
        if (product != null)
        {
            _context.Products.Remove(product);
            await _context.SaveChangesAsync();
        }
    }
}

// Usage in Service
public class ProductService
{
    private readonly IRepository<Product> _productRepository;
    
    public ProductService(IRepository<Product> productRepository)
    {
        _productRepository = productRepository;
    }
    
    public async Task<Product> GetProductAsync(int id)
    {
        return await _productRepository.GetByIdAsync(id);
    }
}

// Registration in Startup.cs
services.AddScoped<IRepository<Product>, ProductRepository>();
```

**Benefits:**
- ✅ Separation of concerns
- ✅ Easy to test (can mock repository)
- ✅ Easy to switch databases
- ✅ Centralized data access logic

---

### 2. Unit of Work Pattern ⭐⭐

**Purpose**: Manage transactions across multiple repositories

```csharp
public interface IUnitOfWork : IDisposable
{
    IRepository<Product> Products { get; }
    IRepository<Category> Categories { get; }
    IRepository<Order> Orders { get; }
    Task<int> SaveChangesAsync();
    Task BeginTransactionAsync();
    Task CommitTransactionAsync();
    Task RollbackTransactionAsync();
}

public class UnitOfWork : IUnitOfWork
{
    private readonly AppDbContext _context;
    private IRepository<Product> _products;
    private IRepository<Category> _categories;
    private IRepository<Order> _orders;
    
    public UnitOfWork(AppDbContext context)
    {
        _context = context;
    }
    
    public IRepository<Product> Products =>
        _products ??= new ProductRepository(_context);
    
    public IRepository<Category> Categories =>
        _categories ??= new CategoryRepository(_context);
    
    public IRepository<Order> Orders =>
        _orders ??= new OrderRepository(_context);
    
    public async Task<int> SaveChangesAsync()
    {
        return await _context.SaveChangesAsync();
    }
    
    public async Task BeginTransactionAsync()
    {
        await _context.Database.BeginTransactionAsync();
    }
    
    public async Task CommitTransactionAsync()
    {
        await _context.Database.CommitTransactionAsync();
    }
    
    public async Task RollbackTransactionAsync()
    {
        await _context.Database.RollbackTransactionAsync();
    }
    
    public void Dispose()
    {
        _context.Dispose();
    }
}

// Usage
public class OrderService
{
    private readonly IUnitOfWork _unitOfWork;
    
    public async Task CreateOrderAsync(CreateOrderDto dto)
    {
        await _unitOfWork.BeginTransactionAsync();
        
        try
        {
            var order = new Order { /* ... */ };
            await _unitOfWork.Orders.AddAsync(order);
            
            // Update product stock
            var product = await _unitOfWork.Products.GetByIdAsync(dto.ProductId);
            product.StockQuantity -= dto.Quantity;
            await _unitOfWork.Products.UpdateAsync(product);
            
            await _unitOfWork.SaveChangesAsync();
            await _unitOfWork.CommitTransactionAsync();
        }
        catch
        {
            await _unitOfWork.RollbackTransactionAsync();
            throw;
        }
    }
}
```

---

### 3. Dependency Injection Pattern ⭐⭐⭐

**Purpose**: Inject dependencies instead of creating them

```csharp
// Without DI (Bad)
public class OrderService
{
    private readonly ProductRepository _repository = new ProductRepository();
    // Tight coupling!
}

// With DI (Good)
public class OrderService
{
    private readonly IProductRepository _repository;
    
    public OrderService(IProductRepository repository)
    {
        _repository = repository; // Injected!
    }
}

// Registration
services.AddScoped<IProductRepository, ProductRepository>();
services.AddScoped<OrderService>();
```

---

### 4. Factory Pattern ⭐⭐

**Purpose**: Create objects without exposing creation logic

```csharp
// Payment factory
public interface IPaymentProcessor
{
    Task<PaymentResult> ProcessAsync(decimal amount);
}

public class CreditCardProcessor : IPaymentProcessor
{
    public async Task<PaymentResult> ProcessAsync(decimal amount)
    {
        // Credit card logic
        return new PaymentResult { Success = true };
    }
}

public class PayPalProcessor : IPaymentProcessor
{
    public async Task<PaymentResult> ProcessAsync(decimal amount)
    {
        // PayPal logic
        return new PaymentResult { Success = true };
    }
}

// Factory
public interface IPaymentProcessorFactory
{
    IPaymentProcessor Create(PaymentMethod method);
}

public class PaymentProcessorFactory : IPaymentProcessorFactory
{
    private readonly IServiceProvider _serviceProvider;
    
    public PaymentProcessorFactory(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }
    
    public IPaymentProcessor Create(PaymentMethod method)
    {
        return method switch
        {
            PaymentMethod.CreditCard => _serviceProvider.GetService<CreditCardProcessor>(),
            PaymentMethod.PayPal => _serviceProvider.GetService<PayPalProcessor>(),
            _ => throw new ArgumentException("Invalid payment method")
        };
    }
}

// Usage
public class OrderService
{
    private readonly IPaymentProcessorFactory _factory;
    
    public async Task ProcessPaymentAsync(Order order)
    {
        var processor = _factory.Create(order.PaymentMethod);
        var result = await processor.ProcessAsync(order.TotalAmount);
    }
}
```

---

### 5. Strategy Pattern ⭐⭐

**Purpose**: Define family of algorithms, make them interchangeable

```csharp
// Discount strategies
public interface IDiscountStrategy
{
    decimal Calculate(decimal price);
}

public class NoDiscountStrategy : IDiscountStrategy
{
    public decimal Calculate(decimal price) => price;
}

public class PercentageDiscountStrategy : IDiscountStrategy
{
    private readonly decimal _percentage;
    
    public PercentageDiscountStrategy(decimal percentage)
    {
        _percentage = percentage;
    }
    
    public decimal Calculate(decimal price)
    {
        return price - (price * _percentage / 100);
    }
}

public class FixedAmountDiscountStrategy : IDiscountStrategy
{
    private readonly decimal _amount;
    
    public FixedAmountDiscountStrategy(decimal amount)
    {
        _amount = amount;
    }
    
    public decimal Calculate(decimal price)
    {
        return Math.Max(0, price - _amount);
    }
}

// Usage
public class PricingService
{
    public decimal CalculateFinalPrice(decimal price, IDiscountStrategy strategy)
    {
        return strategy.Calculate(price);
    }
}

// In action
var pricing = new PricingService();
var finalPrice = pricing.CalculateFinalPrice(100, new PercentageDiscountStrategy(10));
// Result: 90
```

---

### 6. Singleton Pattern ⭐⭐

**Purpose**: Ensure only one instance exists

```csharp
// Manual Singleton (old way)
public class ConfigurationManager
{
    private static ConfigurationManager _instance;
    private static readonly object _lock = new object();
    
    private ConfigurationManager() { }
    
    public static ConfigurationManager Instance
    {
        get
        {
            if (_instance == null)
            {
                lock (_lock)
                {
                    if (_instance == null)
                    {
                        _instance = new ConfigurationManager();
                    }
                }
            }
            return _instance;
        }
    }
}

// Modern way - DI with Singleton lifetime
services.AddSingleton<IConfigurationManager, ConfigurationManager>();
```

---

### 7. Observer Pattern ⭐⭐

**Purpose**: Notify multiple objects about state changes

```csharp
// Using events
public class OrderProcessor
{
    public event EventHandler<OrderEventArgs> OrderCreated;
    public event EventHandler<OrderEventArgs> OrderShipped;
    
    public async Task CreateOrderAsync(Order order)
    {
        // Create order
        await _repository.AddAsync(order);
        
        // Notify observers
        OrderCreated?.Invoke(this, new OrderEventArgs { Order = order });
    }
}

// Observers
public class EmailNotificationService
{
    public EmailNotificationService(OrderProcessor processor)
    {
        processor.OrderCreated += OnOrderCreated;
    }
    
    private async void OnOrderCreated(object sender, OrderEventArgs e)
    {
        await SendEmailAsync(e.Order);
    }
}

public class InventoryService
{
    public InventoryService(OrderProcessor processor)
    {
        processor.OrderCreated += OnOrderCreated;
    }
    
    private async void OnOrderCreated(object sender, OrderEventArgs e)
    {
        await UpdateInventoryAsync(e.Order);
    }
}
```

---

### 8. Decorator Pattern ⭐

**Purpose**: Add behavior to objects dynamically

```csharp
// Base interface
public interface INotificationService
{
    Task SendAsync(string message);
}

// Concrete implementation
public class EmailNotificationService : INotificationService
{
    public async Task SendAsync(string message)
    {
        await SendEmailAsync(message);
    }
}

// Decorator - adds logging
public class LoggingNotificationDecorator : INotificationService
{
    private readonly INotificationService _inner;
    private readonly ILogger _logger;
    
    public LoggingNotificationDecorator(INotificationService inner, ILogger logger)
    {
        _inner = inner;
        _logger = logger;
    }
    
    public async Task SendAsync(string message)
    {
        _logger.LogInformation("Sending notification: {Message}", message);
        await _inner.SendAsync(message);
        _logger.LogInformation("Notification sent successfully");
    }
}

// Decorator - adds retry logic
public class RetryNotificationDecorator : INotificationService
{
    private readonly INotificationService _inner;
    private readonly int _maxRetries;
    
    public async Task SendAsync(string message)
    {
        for (int i = 0; i < _maxRetries; i++)
        {
            try
            {
                await _inner.SendAsync(message);
                return;
            }
            catch when (i < _maxRetries - 1)
            {
                await Task.Delay(1000 * (i + 1));
            }
        }
    }
}
```

---

## Most Frequently Used (Real Projects)

1. **Repository Pattern** - Almost every project
2. **Dependency Injection** - Every modern .NET project
3. **Factory Pattern** - When creating multiple implementations
4. **Strategy Pattern** - For interchangeable algorithms
5. **Unit of Work** - With complex transactions

---

## Benefits of Design Patterns

✅ **Code Reusability**  
✅ **Maintainability**  
✅ **Testability**  
✅ **Loose Coupling**  
✅ **Industry Standard Solutions**  

---

## Summary

**Essential Patterns for .NET:**
- **Repository** - Data access abstraction
- **Unit of Work** - Transaction management
- **Dependency Injection** - Loose coupling
- **Factory** - Object creation
- **Strategy** - Algorithm selection

Use patterns to solve specific problems, not for every situation!
