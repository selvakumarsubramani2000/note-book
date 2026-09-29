# Question 49: Async/await and asynchronous programming

## Answer

### What is Async/Await?

**Async/await** is a programming pattern that allows you to write asynchronous code that looks and behaves like synchronous code, making it easier to read and maintain.

**Key Concept**: Don't block threads while waiting for I/O operations (database, file, network calls).

---

## Why Use Async/Await?

### The Problem (Synchronous Code)

```csharp
public IActionResult GetProducts()
{
    // This BLOCKS the thread for 2 seconds!
    Thread.Sleep(2000); // Simulating database call
    
    var products = _repository.GetAll(); // Blocks thread
    return Ok(products);
}
```

**Problem**: While waiting, the thread cannot handle other requests → **Poor scalability**

### The Solution (Asynchronous Code)

```csharp
public async Task<IActionResult> GetProducts()
{
    // This RELEASES the thread while waiting!
    await Task.Delay(2000); // Simulating database call
    
    var products = await _repository.GetAllAsync(); // Doesn't block thread
    return Ok(products);
}
```

**Benefit**: While waiting, the thread can handle other requests → **Better scalability**

---

## Basic Syntax

```csharp
// Method signature components:
public async Task<ReturnType> MethodNameAsync()
{
    var result = await SomeAsyncOperation();
    return result;
}

// 1. 'async' keyword on method
// 2. Return type is Task<T> or Task
// 3. Method name ends with 'Async' (convention)
// 4. Use 'await' to wait for async operations
```

---

## Return Types

### 1. `Task<T>` - Returns a value

```csharp
public async Task<Product> GetProductAsync(int id)
{
    var product = await _repository.GetByIdAsync(id);
    return product; // Returns Product, but method returns Task<Product>
}

// Usage
var product = await GetProductAsync(5);
```

### 2. `Task` - No return value (like void)

```csharp
public async Task SendEmailAsync(string email, string message)
{
    await _emailService.SendAsync(email, message);
    // No return value
}

// Usage
await SendEmailAsync("user@example.com", "Hello");
```

### 3. `void` - Fire and forget (rarely used, avoid!)

```csharp
// ❌ BAD - Use only for event handlers
public async void ButtonClick(object sender, EventArgs e)
{
    await SomeOperationAsync();
}

// ✅ GOOD - Use Task instead
public async Task ProcessDataAsync()
{
    await SomeOperationAsync();
}
```

---

## Real-World Examples

### Example 1: Database Operations

```csharp
public class ProductRepository
{
    private readonly AppDbContext _context;
    
    public ProductRepository(AppDbContext context)
    {
        _context = context;
    }
    
    // Synchronous (❌ Blocks thread)
    public List<Product> GetAll()
    {
        return _context.Products.ToList(); // Blocks until query completes
    }
    
    // Asynchronous (✅ Releases thread)
    public async Task<List<Product>> GetAllAsync()
    {
        return await _context.Products.ToListAsync(); // Doesn't block
    }
    
    public async Task<Product> GetByIdAsync(int id)
    {
        return await _context.Products.FindAsync(id);
    }
    
    public async Task<Product> CreateAsync(Product product)
    {
        _context.Products.Add(product);
        await _context.SaveChangesAsync();
        return product;
    }
    
    public async Task<bool> UpdateAsync(Product product)
    {
        _context.Products.Update(product);
        await _context.SaveChangesAsync();
        return true;
    }
    
    public async Task<bool> DeleteAsync(int id)
    {
        var product = await _context.Products.FindAsync(id);
        if (product == null)
            return false;
        
        _context.Products.Remove(product);
        await _context.SaveChangesAsync();
        return true;
    }
}
```

### Example 2: Web API Controller

```csharp
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    private readonly IProductRepository _repository;
    private readonly IEmailService _emailService;
    
    public ProductsController(
        IProductRepository repository,
        IEmailService emailService)
    {
        _repository = repository;
        _emailService = emailService;
    }
    
    // GET: api/products
    [HttpGet]
    public async Task<IActionResult> GetAll()
    {
        var products = await _repository.GetAllAsync();
        return Ok(products);
    }
    
    // GET: api/products/5
    [HttpGet("{id}")]
    public async Task<IActionResult> Get(int id)
    {
        var product = await _repository.GetByIdAsync(id);
        
        if (product == null)
            return NotFound();
        
        return Ok(product);
    }
    
    // POST: api/products
    [HttpPost]
    public async Task<IActionResult> Create([FromBody] Product product)
    {
        var createdProduct = await _repository.CreateAsync(product);
        
        // Send email notification (also async)
        await _emailService.SendAsync(
            "admin@example.com", 
            $"New product created: {product.Name}");
        
        return CreatedAtAction(nameof(Get), new { id = createdProduct.Id }, createdProduct);
    }
}
```

### Example 3: Multiple Async Operations

```csharp
public class OrderService
{
    private readonly IOrderRepository _orderRepo;
    private readonly IProductRepository _productRepo;
    private readonly IEmailService _emailService;
    private readonly ISmsService _smsService;
    
    // Sequential execution (slower)
    public async Task<Order> CreateOrderSequentialAsync(CreateOrderRequest request)
    {
        // These run ONE AFTER ANOTHER
        var products = await _productRepo.GetByIdsAsync(request.ProductIds); // Wait
        var order = await _orderRepo.CreateAsync(request);                   // Then wait
        await _emailService.SendOrderConfirmationAsync(order);               // Then wait
        await _smsService.SendOrderNotificationAsync(order);                 // Then wait
        
        return order;
    }
    
    // Parallel execution (faster) ✅
    public async Task<Order> CreateOrderParallelAsync(CreateOrderRequest request)
    {
        // Get products
        var products = await _productRepo.GetByIdsAsync(request.ProductIds);
        var order = await _orderRepo.CreateAsync(request);
        
        // These run IN PARALLEL (both at the same time)
        var emailTask = _emailService.SendOrderConfirmationAsync(order);
        var smsTask = _smsService.SendOrderNotificationAsync(order);
        
        // Wait for both to complete
        await Task.WhenAll(emailTask, smsTask);
        
        return order;
    }
}
```

---

## Task.WhenAll and Task.WhenAny

### Task.WhenAll - Wait for all tasks

```csharp
public async Task<DashboardData> GetDashboardDataAsync(int userId)
{
    // Start all tasks simultaneously
    var ordersTask = _orderRepo.GetUserOrdersAsync(userId);
    var productsTask = _productRepo.GetFeaturedAsync();
    var statsTask = _statsService.GetUserStatsAsync(userId);
    
    // Wait for ALL to complete
    await Task.WhenAll(ordersTask, productsTask, statsTask);
    
    return new DashboardData
    {
        Orders = ordersTask.Result,        // or await ordersTask
        Products = productsTask.Result,
        Stats = statsTask.Result
    };
}
```

### Task.WhenAny - Wait for first one

```csharp
public async Task<string> GetDataFromFastestSourceAsync()
{
    var task1 = GetDataFromSource1Async();
    var task2 = GetDataFromSource2Async();
    var task3 = GetDataFromSource3Async();
    
    // Return result from whichever completes first
    var completedTask = await Task.WhenAny(task1, task2, task3);
    return await completedTask;
}
```

---

## Exception Handling

```csharp
public async Task<Product> GetProductWithErrorHandlingAsync(int id)
{
    try
    {
        var product = await _repository.GetByIdAsync(id);
        return product;
    }
    catch (SqlException ex)
    {
        _logger.LogError(ex, "Database error retrieving product {ProductId}", id);
        throw new RepositoryException("Failed to retrieve product", ex);
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Unexpected error retrieving product {ProductId}", id);
        throw;
    }
}

// With multiple async operations
public async Task ProcessOrderAsync(int orderId)
{
    try
    {
        var order = await _orderRepo.GetByIdAsync(orderId);
        await _paymentService.ProcessPaymentAsync(order);
        await _emailService.SendConfirmationAsync(order);
    }
    catch (PaymentException ex)
    {
        // Handle payment-specific errors
        _logger.LogError(ex, "Payment failed for order {OrderId}", orderId);
        await _orderRepo.UpdateStatusAsync(orderId, OrderStatus.PaymentFailed);
        throw;
    }
}
```

---

## ConfigureAwait(false)

```csharp
// In library code (not Web API controllers)
public async Task<Product> GetProductAsync(int id)
{
    // ConfigureAwait(false) = Don't capture context (better performance in libraries)
    var product = await _repository.GetByIdAsync(id).ConfigureAwait(false);
    return product;
}

// In Web API controllers - DON'T use ConfigureAwait(false)
[HttpGet("{id}")]
public async Task<IActionResult> Get(int id)
{
    // No ConfigureAwait needed in ASP.NET Core
    var product = await _repository.GetByIdAsync(id);
    return Ok(product);
}
```

**Rule**: In ASP.NET Core, you don't need `ConfigureAwait(false)` - it's already optimized.

---

## Common Mistakes

### ❌ Mistake 1: Using .Result or .Wait() (Deadlock risk)

```csharp
// ❌ BAD - Can cause deadlock
public void GetProduct(int id)
{
    var product = _repository.GetByIdAsync(id).Result; // BLOCKS thread!
}

// ✅ GOOD
public async Task<Product> GetProduct(int id)
{
    var product = await _repository.GetByIdAsync(id);
    return product;
}
```

### ❌ Mistake 2: Not awaiting async methods

```csharp
// ❌ BAD - Email won't be sent!
public async Task CreateOrder(Order order)
{
    await _orderRepo.CreateAsync(order);
    _emailService.SendConfirmationAsync(order); // Missing await!
}

// ✅ GOOD
public async Task CreateOrder(Order order)
{
    await _orderRepo.CreateAsync(order);
    await _emailService.SendConfirmationAsync(order);
}
```

### ❌ Mistake 3: Async void

```csharp
// ❌ BAD - Can't catch exceptions
public async void ProcessOrder(int orderId)
{
    await _orderService.ProcessAsync(orderId);
}

// ✅ GOOD
public async Task ProcessOrder(int orderId)
{
    await _orderService.ProcessAsync(orderId);
}
```

---

## Performance Benefits

```csharp
// Benchmark: 100 concurrent requests

// Synchronous (blocking)
// Throughput: 10 requests/second
// Threads needed: 100
public List<Product> GetProducts()
{
    Thread.Sleep(1000); // Blocks thread
    return _context.Products.ToList();
}

// Asynchronous (non-blocking)
// Throughput: 1000 requests/second
// Threads needed: 10-20
public async Task<List<Product>> GetProductsAsync()
{
    await Task.Delay(1000); // Releases thread
    return await _context.Products.ToListAsync();
}
```

---

## Best Practices

1. ✅ **Use async/await for I/O operations** (database, file, network)
2. ✅ **Don't use async for CPU-bound work** (use Task.Run for that)
3. ✅ **Always await async methods**
4. ✅ **Return Task, not async void** (except event handlers)
5. ✅ **Use async all the way** (don't mix sync and async)
6. ✅ **Name async methods with 'Async' suffix**
7. ❌ **Don't use .Result or .Wait()** (deadlock risk)
8. ❌ **Don't use async for simple property getters**

---

## Summary

**Async/Await:**
- **async** = Marks method as asynchronous
- **await** = Waits for async operation without blocking thread
- **`Task<T>`** = Return type for async methods that return value
- **Task** = Return type for async methods that don't return value

**Benefits:**
- ✅ Better scalability
- ✅ Improved responsiveness
- ✅ Efficient resource usage

**Use for**: Database calls, HTTP requests, file I/O, external APIs

Async/await is essential for building scalable web applications!
