# Performance & Scalability in .NET: From Slow to Fast

> **Production-ready guide** to optimizing ASP.NET Core applications for high traffic  
> **Focus**: Caching strategies, database optimization, async/await, and real-world scenarios

## Real-World Scenario

**The Problem**:
Your e-commerce API is live. Black Friday is coming. Current performance:
- Homepage loads in 3 seconds (should be < 500ms)
- Product search takes 2 seconds (should be < 200ms)
- Checkout fails under 100 concurrent users
- Database CPU at 80% during normal traffic
- Memory usage grows until app crashes

**The Impact**:
- Lost sales (users abandon slow sites)
- Poor SEO ranking (Google penalizes slow sites)
- High infrastructure costs (need more servers)
- Angry customers and bad reviews

**The Goal**: Handle 10,000 concurrent users with < 500ms response times

---

## Table of Contents

1. [Caching Strategies](#caching-strategies)
2. [Database Optimization](#database-optimization)
3. [Async/Await Best Practices](#asyncawait-best-practices)
4. [Connection Pooling](#connection-pooling)
5. [Response Compression](#response-compression)
6. [Load Testing](#load-testing)
7. [Monitoring & Profiling](#monitoring--profiling)

---

## Caching Strategies

### The Caching Hierarchy

```
1. In-Memory Cache (fastest, limited to single server)
   ↓
2. Distributed Cache (Redis - shared across servers)
   ↓
3. CDN (for static assets)
   ↓
4. Database (slowest)
```

### 1. In-Memory Caching

**When to use**:
- ✅ Data that rarely changes (configuration, categories)
- ✅ Single-server deployment
- ✅ Small data sets (< 100MB)

**When NOT to use**:
- ❌ Multi-server deployment (cache not shared)
- ❌ Large data sets (memory pressure)
- ❌ Frequently changing data

**Implementation**:
```csharp
// Program.cs
builder.Services.AddMemoryCache();

// Service
public class ProductService
{
    private readonly IMemoryCache _cache;
    private readonly IProductRepository _productRepository;
    
    public ProductService(IMemoryCache cache, IProductRepository productRepository)
    {
        _cache = cache;
        _productRepository = productRepository;
    }
    
    public async Task<List<Category>> GetCategoriesAsync()
    {
        const string cacheKey = "categories";
        
        // Try to get from cache
        if (_cache.TryGetValue(cacheKey, out List<Category> categories))
        {
            return categories; // Cache hit!
        }
        
        // Cache miss - get from database
        categories = await _productRepository.GetCategoriesAsync();
        
        // Store in cache with expiration
        var cacheOptions = new MemoryCacheEntryOptions
        {
            AbsoluteExpirationRelativeToNow = TimeSpan.FromHours(1),
            SlidingExpiration = TimeSpan.FromMinutes(15)
        };
        
        _cache.Set(cacheKey, categories, cacheOptions);
        
        return categories;
    }
}
```

**Cache Eviction Strategies**:
```csharp
// Absolute expiration: Expires after fixed time
AbsoluteExpirationRelativeToNow = TimeSpan.FromHours(1)

// Sliding expiration: Resets timer on each access
SlidingExpiration = TimeSpan.FromMinutes(15)

// Priority: What to evict first when memory is low
Priority = CacheItemPriority.High // or Low, Normal, NeverRemove

// Size limit: Limit cache size
Size = 1, // Each entry counts as 1
options.SizeLimit = 1024 // Total cache size
```

### 2. Distributed Caching (Redis)

**When to use**:
- ✅ Multi-server deployment (load balanced)
- ✅ Session state across servers
- ✅ Large data sets
- ✅ Need cache persistence

**Setup**:
```bash
# Install Redis
docker run -d -p 6379:6379 redis

# Install NuGet package
dotnet add package Microsoft.Extensions.Caching.StackExchangeRedis
```

**Configuration**:
```csharp
// Program.cs
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = builder.Configuration.GetConnectionString("Redis");
    options.InstanceName = "MyApp_";
});

// appsettings.json
{
  "ConnectionStrings": {
    "Redis": "localhost:6379"
  }
}
```

**Implementation**:
```csharp
public class ProductService
{
    private readonly IDistributedCache _cache;
    private readonly IProductRepository _productRepository;
    
    public ProductService(IDistributedCache cache, IProductRepository productRepository)
    {
        _cache = cache;
        _productRepository = productRepository;
    }
    
    public async Task<Product> GetProductAsync(int id)
    {
        var cacheKey = $"product_{id}";
        
        // Try to get from Redis
        var cachedProduct = await _cache.GetStringAsync(cacheKey);
        if (cachedProduct != null)
        {
            return JsonSerializer.Deserialize<Product>(cachedProduct);
        }
        
        // Cache miss - get from database
        var product = await _productRepository.GetByIdAsync(id);
        
        // Store in Redis
        var options = new DistributedCacheEntryOptions
        {
            AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(30)
        };
        
        await _cache.SetStringAsync(
            cacheKey,
            JsonSerializer.Serialize(product),
            options
        );
        
        return product;
    }
    
    // Invalidate cache when product is updated
    public async Task UpdateProductAsync(Product product)
    {
        await _productRepository.UpdateAsync(product);
        
        // Remove from cache
        var cacheKey = $"product_{product.Id}";
        await _cache.RemoveAsync(cacheKey);
    }
}
```

### 3. Cache-Aside Pattern (Lazy Loading)

**Pattern**:
```
1. Check cache
2. If found (cache hit), return cached data
3. If not found (cache miss):
   a. Get from database
   b. Store in cache
   c. Return data
```

**Implementation**:
```csharp
public async Task<T> GetOrCreateAsync<T>(
    string cacheKey,
    Func<Task<T>> factory,
    TimeSpan? expiration = null)
{
    // Try cache first
    var cached = await _cache.GetStringAsync(cacheKey);
    if (cached != null)
    {
        return JsonSerializer.Deserialize<T>(cached);
    }
    
    // Cache miss - execute factory
    var data = await factory();
    
    // Store in cache
    var options = new DistributedCacheEntryOptions
    {
        AbsoluteExpirationRelativeToNow = expiration ?? TimeSpan.FromMinutes(10)
    };
    
    await _cache.SetStringAsync(
        cacheKey,
        JsonSerializer.Serialize(data),
        options
    );
    
    return data;
}

// Usage
var product = await GetOrCreateAsync(
    $"product_{id}",
    () => _productRepository.GetByIdAsync(id),
    TimeSpan.FromMinutes(30)
);
```

### 4. Response Caching (HTTP Cache)

**When to use**:
- ✅ Public data (same for all users)
- ✅ Static or rarely changing content
- ✅ GET requests only

**Setup**:
```csharp
// Program.cs
builder.Services.AddResponseCaching();

var app = builder.Build();
app.UseResponseCaching(); // Must be before UseEndpoints
app.MapControllers();
```

**Usage**:
```csharp
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    // Cache for 60 seconds
    [HttpGet]
    [ResponseCache(Duration = 60, Location = ResponseCacheLocation.Any)]
    public async Task<IActionResult> GetProducts()
    {
        var products = await _productService.GetProductsAsync();
        return Ok(products);
    }
    
    // Cache for 5 minutes, vary by query string
    [HttpGet("search")]
    [ResponseCache(Duration = 300, VaryByQueryKeys = new[] { "q", "category" })]
    public async Task<IActionResult> Search([FromQuery] string q, [FromQuery] string category)
    {
        var results = await _productService.SearchAsync(q, category);
        return Ok(results);
    }
    
    // No caching for user-specific data
    [HttpGet("my-orders")]
    [ResponseCache(NoStore = true, Location = ResponseCacheLocation.None)]
    public async Task<IActionResult> GetMyOrders()
    {
        var orders = await _orderService.GetMyOrdersAsync();
        return Ok(orders);
    }
}
```

### 5. Output Caching (.NET 7+)

**More powerful than Response Caching**:
```csharp
// Program.cs
builder.Services.AddOutputCache(options =>
{
    // Default policy
    options.AddBasePolicy(builder => builder.Expire(TimeSpan.FromSeconds(60)));
    
    // Named policy
    options.AddPolicy("Products", builder => 
        builder.Expire(TimeSpan.FromMinutes(5))
               .Tag("products"));
});

var app = builder.Build();
app.UseOutputCache();

// Controller
[HttpGet]
[OutputCache(PolicyName = "Products")]
public async Task<IActionResult> GetProducts()
{
    var products = await _productService.GetProductsAsync();
    return Ok(products);
}

// Invalidate cache by tag
public async Task UpdateProduct(Product product)
{
    await _productRepository.UpdateAsync(product);
    
    // Invalidate all cached responses tagged with "products"
    await _outputCacheStore.EvictByTagAsync("products", default);
}
```

### Caching Decision Matrix

| Data Type | Caching Strategy | Expiration | Example |
|-----------|------------------|------------|---------|
| Static config | In-Memory | 1 hour | Categories, settings |
| Product catalog | Redis | 30 minutes | Product details |
| User session | Redis | 20 minutes | Shopping cart |
| Search results | Redis | 5 minutes | Product search |
| Public API | Response Cache | 1 minute | Public product list |
| User-specific | No cache | N/A | User orders, profile |

---

## Database Optimization

### 1. The N+1 Query Problem

**The Problem**:
```csharp
// ❌ BAD: N+1 queries
public async Task<List<OrderDto>> GetOrdersAsync()
{
    var orders = await _context.Orders.ToListAsync(); // 1 query
    
    var orderDtos = new List<OrderDto>();
    foreach (var order in orders) // N queries!
    {
        var user = await _context.Users.FindAsync(order.UserId); // Query per order!
        orderDtos.Add(new OrderDto
        {
            Id = order.Id,
            UserName = user.Name
        });
    }
    
    return orderDtos;
}

// If you have 100 orders, this executes 101 queries!
```

**The Fix**: Use `Include` (eager loading)
```csharp
// ✅ GOOD: 1 query with JOIN
public async Task<List<OrderDto>> GetOrdersAsync()
{
    var orders = await _context.Orders
        .Include(o => o.User) // JOIN in single query
        .ToListAsync();
    
    return orders.Select(o => new OrderDto
    {
        Id = o.Id,
        UserName = o.User.Name
    }).ToList();
}

// SQL generated:
// SELECT o.*, u.* FROM Orders o INNER JOIN Users u ON o.UserId = u.Id
```

**Multiple levels**:
```csharp
// Include nested relationships
var orders = await _context.Orders
    .Include(o => o.User)
    .Include(o => o.Items)
        .ThenInclude(i => i.Product)
    .ToListAsync();
```

### 2. Projection (Select Only What You Need)

**The Problem**:
```csharp
// ❌ BAD: Fetching entire entity when you only need 2 fields
public async Task<List<ProductDto>> GetProductsAsync()
{
    var products = await _context.Products.ToListAsync(); // Fetches ALL columns!

    return products.Select(p => new ProductDto
    {
        Id = p.Id,
        Name = p.Name
        // Only using 2 fields, but fetched 20!
    }).ToList();
}
```

**The Fix**: Use `Select` (projection)
```csharp
// ✅ GOOD: Fetch only needed columns
public async Task<List<ProductDto>> GetProductsAsync()
{
    return await _context.Products
        .Select(p => new ProductDto
        {
            Id = p.Id,
            Name = p.Name
        })
        .ToListAsync();
}

// SQL generated:
// SELECT p.Id, p.Name FROM Products p
// (instead of SELECT * FROM Products)
```

**Performance impact**:
- Fetching 2 columns vs 20 columns = 10x less data transferred
- Less memory usage
- Faster serialization

### 3. AsNoTracking for Read-Only Queries

**The Problem**:
```csharp
// ❌ SLOW: EF Core tracks all entities (overhead)
public async Task<List<Product>> GetProductsAsync()
{
    return await _context.Products.ToListAsync();
    // EF Core creates change tracking snapshots for ALL products
}
```

**The Fix**: Use `AsNoTracking` for read-only queries
```csharp
// ✅ FAST: No change tracking
public async Task<List<Product>> GetProductsAsync()
{
    return await _context.Products
        .AsNoTracking() // 30-40% faster!
        .ToListAsync();
}
```

**When to use**:
- ✅ Read-only queries (GET endpoints)
- ✅ Queries for display purposes
- ✅ Large result sets

**When NOT to use**:
- ❌ When you need to update entities
- ❌ When you need change tracking

### 4. Pagination

**The Problem**:
```csharp
// ❌ BAD: Fetching all 1 million products
public async Task<List<Product>> GetProductsAsync()
{
    return await _context.Products.ToListAsync(); // OutOfMemoryException!
}
```

**The Fix**: Use `Skip` and `Take`
```csharp
// ✅ GOOD: Fetch 20 products at a time
public async Task<PagedResult<Product>> GetProductsAsync(int page = 1, int pageSize = 20)
{
    var query = _context.Products.AsNoTracking();

    var totalCount = await query.CountAsync();

    var products = await query
        .OrderBy(p => p.Id) // MUST order for consistent pagination
        .Skip((page - 1) * pageSize)
        .Take(pageSize)
        .ToListAsync();

    return new PagedResult<Product>
    {
        Items = products,
        TotalCount = totalCount,
        Page = page,
        PageSize = pageSize,
        TotalPages = (int)Math.Ceiling(totalCount / (double)pageSize)
    };
}

// SQL generated:
// SELECT * FROM Products ORDER BY Id OFFSET 20 ROWS FETCH NEXT 20 ROWS ONLY
```

**Optimization**: Avoid `CountAsync` on every request
```csharp
// Cache total count (it doesn't change often)
var totalCount = await _cache.GetOrCreateAsync(
    "products_total_count",
    async () => await _context.Products.CountAsync(),
    TimeSpan.FromMinutes(10)
);
```

### 5. Compiled Queries

**For frequently executed queries**:
```csharp
// Define compiled query (once)
private static readonly Func<ApplicationDbContext, int, Task<Product>> GetProductByIdQuery =
    EF.CompileAsyncQuery((ApplicationDbContext context, int id) =>
        context.Products.FirstOrDefault(p => p.Id == id));

// Use compiled query (many times)
public async Task<Product> GetProductAsync(int id)
{
    return await GetProductByIdQuery(_context, id);
    // 10-20% faster than regular query
}
```

### 6. Bulk Operations

**The Problem**:
```csharp
// ❌ SLOW: 1000 individual INSERT statements
public async Task ImportProductsAsync(List<Product> products)
{
    foreach (var product in products)
    {
        _context.Products.Add(product);
        await _context.SaveChangesAsync(); // 1000 round trips to database!
    }
}
```

**The Fix**: Batch operations
```csharp
// ✅ FAST: Single batch INSERT
public async Task ImportProductsAsync(List<Product> products)
{
    _context.Products.AddRange(products);
    await _context.SaveChangesAsync(); // 1 round trip!
}

// Or use library for even better performance
// Install: dotnet add package EFCore.BulkExtensions
public async Task ImportProductsAsync(List<Product> products)
{
    await _context.BulkInsertAsync(products); // 100x faster!
}
```

### 7. Database Indexes

**Identify slow queries**:
```sql
-- SQL Server: Find missing indexes
SELECT
    OBJECT_NAME(s.object_id) AS TableName,
    i.name AS IndexName,
    s.avg_fragmentation_in_percent
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED') s
INNER JOIN sys.indexes i ON s.object_id = i.object_id AND s.index_id = i.index_id
WHERE s.avg_fragmentation_in_percent > 30
ORDER BY s.avg_fragmentation_in_percent DESC;
```

**Add indexes in EF Core**:
```csharp
// In entity configuration
public class ProductConfiguration : IEntityTypeConfiguration<Product>
{
    public void Configure(EntityTypeBuilder<Product> builder)
    {
        // Single column index
        builder.HasIndex(p => p.Name);

        // Composite index (for queries filtering by both)
        builder.HasIndex(p => new { p.CategoryId, p.Price });

        // Unique index
        builder.HasIndex(p => p.Sku).IsUnique();

        // Filtered index (SQL Server)
        builder.HasIndex(p => p.IsActive)
            .HasFilter("IsActive = 1");
    }
}
```

**When to add indexes**:
- ✅ Columns used in WHERE clauses
- ✅ Columns used in JOIN conditions
- ✅ Columns used in ORDER BY
- ✅ Foreign keys

**When NOT to add indexes**:
- ❌ Tables with frequent INSERTs/UPDATEs (indexes slow down writes)
- ❌ Columns with low cardinality (e.g., boolean fields)
- ❌ Small tables (< 1000 rows)

### 8. Connection Pooling

**Default behavior** (already enabled):
```csharp
// Connection string with pooling (default)
"Server=localhost;Database=MyApp;User Id=sa;Password=***;Max Pool Size=100;Min Pool Size=10;"
```

**How it works**:
1. App requests connection from pool
2. If available, reuse existing connection
3. If not, create new connection (up to Max Pool Size)
4. When done, return connection to pool (don't close!)

**Best practices**:
```csharp
// ✅ GOOD: DbContext is Scoped, automatically disposed
public class OrderRepository
{
    private readonly ApplicationDbContext _context;

    public OrderRepository(ApplicationDbContext context)
    {
        _context = context; // Connection from pool
    }

    public async Task<Order> GetOrderAsync(int id)
    {
        return await _context.Orders.FindAsync(id);
    } // Connection returned to pool at end of request
}

// ❌ BAD: Creating DbContext manually
public async Task<Order> GetOrderAsync(int id)
{
    using var context = new ApplicationDbContext(); // New connection every time!
    return await context.Orders.FindAsync(id);
}
```

---

## Async/Await Best Practices

### 1. Always Use Async for I/O Operations

**The Problem**:
```csharp
// ❌ BAD: Blocking thread while waiting for database
public Order GetOrder(int id)
{
    var order = _context.Orders.Find(id); // Blocks thread!
    return order;
}

// With 100 concurrent requests:
// - 100 threads blocked
// - Thread pool exhaustion
// - App becomes unresponsive
```

**The Fix**: Use async/await
```csharp
// ✅ GOOD: Thread is released while waiting
public async Task<Order> GetOrderAsync(int id)
{
    var order = await _context.Orders.FindAsync(id); // Thread released!
    return order;
}

// With 100 concurrent requests:
// - Only a few threads needed
// - Threads handle other requests while waiting
// - App stays responsive
```

### 2. Avoid Async Void

**The Problem**:
```csharp
// ❌ BAD: Can't catch exceptions, can't await
public async void ProcessOrderAsync(int orderId)
{
    var order = await _context.Orders.FindAsync(orderId);
    // If exception occurs here, it crashes the app!
}
```

**The Fix**: Use `async Task`
```csharp
// ✅ GOOD: Can catch exceptions, can await
public async Task ProcessOrderAsync(int orderId)
{
    var order = await _context.Orders.FindAsync(orderId);
    // Exceptions can be caught by caller
}
```

**Exception**: Event handlers
```csharp
// OK: Event handlers must be void
button.Click += async (sender, e) =>
{
    await ProcessOrderAsync(orderId);
};
```

### 3. Don't Block on Async Code

**The Problem**:
```csharp
// ❌ DEADLOCK RISK!
public Order GetOrder(int id)
{
    var order = GetOrderAsync(id).Result; // Blocks!
    return order;
}

public Order GetOrder2(int id)
{
    var order = GetOrderAsync(id).GetAwaiter().GetResult(); // Also blocks!
    return order;
}
```

**Why it deadlocks**:
1. `Result` blocks current thread
2. Async method tries to resume on same thread
3. Thread is blocked waiting for async method
4. Async method is waiting for thread
5. **Deadlock!**

**The Fix**: Use async all the way
```csharp
// ✅ GOOD: Async all the way
public async Task<Order> GetOrderAsync(int id)
{
    var order = await GetOrderFromDbAsync(id);
    return order;
}
```

### 4. ConfigureAwait(false) in Libraries

**In application code** (ASP.NET Core):
```csharp
// ✅ GOOD: No need for ConfigureAwait in ASP.NET Core
public async Task<Order> GetOrderAsync(int id)
{
    var order = await _context.Orders.FindAsync(id);
    return order;
}
```

**In library code**:
```csharp
// ✅ GOOD: Use ConfigureAwait(false) in libraries
public async Task<Order> GetOrderAsync(int id)
{
    var order = await _context.Orders.FindAsync(id).ConfigureAwait(false);
    return order;
}
```

**Why**:
- ASP.NET Core doesn't have SynchronizationContext
- `ConfigureAwait(false)` is unnecessary in ASP.NET Core
- But use it in libraries to avoid capturing context

### 5. Parallel Async Operations

**Sequential** (slow):
```csharp
// ❌ SLOW: 3 seconds total (1s + 1s + 1s)
public async Task<OrderSummary> GetOrderSummaryAsync(int orderId)
{
    var order = await _orderRepository.GetByIdAsync(orderId); // 1 second
    var user = await _userRepository.GetByIdAsync(order.UserId); // 1 second
    var products = await _productRepository.GetByIdsAsync(order.ProductIds); // 1 second

    return new OrderSummary { Order = order, User = user, Products = products };
}
```

**Parallel** (fast):
```csharp
// ✅ FAST: 1 second total (all run in parallel)
public async Task<OrderSummary> GetOrderSummaryAsync(int orderId)
{
    var orderTask = _orderRepository.GetByIdAsync(orderId);
    var userTask = _userRepository.GetByIdAsync(order.UserId);
    var productsTask = _productRepository.GetByIdsAsync(order.ProductIds);

    // Wait for all to complete
    await Task.WhenAll(orderTask, userTask, productsTask);

    return new OrderSummary
    {
        Order = orderTask.Result,
        User = userTask.Result,
        Products = productsTask.Result
    };
}
```

**Or use `Task.WhenAll` with results**:
```csharp
public async Task<OrderSummary> GetOrderSummaryAsync(int orderId)
{
    var results = await Task.WhenAll(
        _orderRepository.GetByIdAsync(orderId),
        _userRepository.GetByIdAsync(userId),
        _productRepository.GetByIdsAsync(productIds)
    );

    return new OrderSummary
    {
        Order = results[0],
        User = results[1],
        Products = results[2]
    };
}
```

### 6. Avoid Async in Loops

**The Problem**:
```csharp
// ❌ SLOW: Sequential execution
public async Task ProcessOrdersAsync(List<int> orderIds)
{
    foreach (var orderId in orderIds)
    {
        await ProcessOrderAsync(orderId); // Waits for each to complete
    }
}
// 100 orders × 1 second each = 100 seconds
```

**The Fix**: Process in parallel
```csharp
// ✅ FAST: Parallel execution
public async Task ProcessOrdersAsync(List<int> orderIds)
{
    var tasks = orderIds.Select(id => ProcessOrderAsync(id));
    await Task.WhenAll(tasks);
}
// 100 orders in parallel = ~1 second (limited by resources)
```

**With concurrency limit**:
```csharp
// ✅ BEST: Parallel with limit (avoid overwhelming database)
public async Task ProcessOrdersAsync(List<int> orderIds)
{
    var semaphore = new SemaphoreSlim(10); // Max 10 concurrent

    var tasks = orderIds.Select(async id =>
    {
        await semaphore.WaitAsync();
        try
        {
            await ProcessOrderAsync(id);
        }
        finally
        {
            semaphore.Release();
        }
    });

    await Task.WhenAll(tasks);
}
```

---

## Response Compression

**Enable compression**:
```csharp
// Program.cs
builder.Services.AddResponseCompression(options =>
{
    options.EnableForHttps = true; // Enable for HTTPS
    options.Providers.Add<BrotliCompressionProvider>();
    options.Providers.Add<GzipCompressionProvider>();
});

builder.Services.Configure<BrotliCompressionProviderOptions>(options =>
{
    options.Level = CompressionLevel.Fastest; // Balance between speed and size
});

var app = builder.Build();
app.UseResponseCompression(); // Must be early in pipeline
```

**Impact**:
- JSON response: 100KB → 10KB (90% reduction)
- Faster transfer over network
- Lower bandwidth costs

**When to use**:
- ✅ Large JSON responses
- ✅ Text-based responses
- ✅ APIs consumed over internet

**When NOT to use**:
- ❌ Already compressed data (images, videos)
- ❌ Very small responses (< 1KB)
- ❌ Internal APIs on fast network

---

## Load Testing

### Using k6

**Install**:
```bash
# Windows
choco install k6

# macOS
brew install k6

# Linux
sudo apt-get install k6
```

**Simple load test**:
```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 50 },  // Ramp up to 50 users
    { duration: '1m', target: 50 },   // Stay at 50 users
    { duration: '30s', target: 100 }, // Ramp up to 100 users
    { duration: '1m', target: 100 },  // Stay at 100 users
    { duration: '30s', target: 0 },   // Ramp down
  ],
};

export default function () {
  const res = http.get('https://localhost:5001/api/products');

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1);
}
```

**Run test**:
```bash
k6 run load-test.js
```

**Results**:
```
     ✓ status is 200
     ✓ response time < 500ms

     checks.........................: 100.00% ✓ 5000      ✗ 0
     data_received..................: 15 MB   250 kB/s
     data_sent......................: 450 kB  7.5 kB/s
     http_req_duration..............: avg=245ms min=100ms med=230ms max=450ms p(90)=350ms p(95)=400ms
     http_reqs......................: 5000    83.33/s
```

---

## Monitoring & Profiling

### Application Insights

**Setup**:
```bash
dotnet add package Microsoft.ApplicationInsights.AspNetCore
```

**Configuration**:
```csharp
// Program.cs
builder.Services.AddApplicationInsightsTelemetry(options =>
{
    options.ConnectionString = builder.Configuration["ApplicationInsights:ConnectionString"];
});

// appsettings.json
{
  "ApplicationInsights": {
    "ConnectionString": "InstrumentationKey=..."
  }
}
```

**Track custom metrics**:
```csharp
public class OrderService
{
    private readonly TelemetryClient _telemetry;

    public OrderService(TelemetryClient telemetry)
    {
        _telemetry = telemetry;
    }

    public async Task CreateOrderAsync(Order order)
    {
        var stopwatch = Stopwatch.StartNew();

        try
        {
            await _orderRepository.AddAsync(order);

            // Track success
            _telemetry.TrackMetric("OrderCreated", 1);
            _telemetry.TrackMetric("OrderCreationTime", stopwatch.ElapsedMilliseconds);
        }
        catch (Exception ex)
        {
            // Track failure
            _telemetry.TrackException(ex);
            _telemetry.TrackMetric("OrderCreationFailed", 1);
            throw;
        }
    }
}
```

### MiniProfiler (for development)

**Setup**:
```bash
dotnet add package MiniProfiler.AspNetCore.Mvc
dotnet add package MiniProfiler.EntityFrameworkCore
```

**Configuration**:
```csharp
// Program.cs
builder.Services.AddMiniProfiler(options =>
{
    options.RouteBasePath = "/profiler";
}).AddEntityFramework();

var app = builder.Build();
app.UseMiniProfiler();
```

**View results**: Navigate to `/profiler/results-index`

---

## Summary

### Performance Checklist

**Caching**:
- [ ] Use in-memory cache for static data
- [ ] Use Redis for distributed caching
- [ ] Implement cache-aside pattern
- [ ] Set appropriate expiration times
- [ ] Invalidate cache on updates

**Database**:
- [ ] Fix N+1 queries with `Include`
- [ ] Use `AsNoTracking` for read-only queries
- [ ] Project only needed columns with `Select`
- [ ] Implement pagination
- [ ] Add indexes on frequently queried columns
- [ ] Use bulk operations for large inserts

**Async/Await**:
- [ ] Use async for all I/O operations
- [ ] Avoid `async void`
- [ ] Don't block on async code (`.Result`, `.Wait()`)
- [ ] Run independent operations in parallel

**Infrastructure**:
- [ ] Enable response compression
- [ ] Configure connection pooling
- [ ] Use CDN for static assets
- [ ] Load test before production

**Monitoring**:
- [ ] Set up Application Insights
- [ ] Track custom metrics
- [ ] Monitor database query performance
- [ ] Set up alerts for slow requests

### Performance Targets

| Metric | Target | Excellent |
|--------|--------|-----------|
| API response time | < 500ms | < 200ms |
| Database query | < 100ms | < 50ms |
| Page load time | < 2s | < 1s |
| Concurrent users | 1000+ | 10,000+ |
| Error rate | < 1% | < 0.1% |

---

**Remember**: Premature optimization is the root of all evil. Profile first, optimize second! 🚀
