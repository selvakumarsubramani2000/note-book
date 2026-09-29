# Question 50: LINQ queries and their optimization

## Answer

### What is LINQ?

**LINQ (Language Integrated Query)** allows you to query collections using C# syntax instead of loops. It works with databases, arrays, lists, XML, and more.

**Benefits:**
- Write less code
- Type-safe queries
- IntelliSense support
- Consistent syntax across data sources

---

## LINQ Syntax Types

### 1. Query Syntax (SQL-like)

```csharp
var products = from p in _context.Products
               where p.Price > 50
               orderby p.Name
               select p;
```

### 2. Method Syntax (Lambda) - More Common

```csharp
var products = _context.Products
    .Where(p => p.Price > 50)
    .OrderBy(p => p.Name)
    .ToList();
```

---

## Common LINQ Operations

### Filtering - Where

```csharp
// Single condition
var expensiveProducts = products.Where(p => p.Price > 100);

// Multiple conditions
var filtered = products.Where(p => p.Price > 50 && p.CategoryId == 1);

// Complex conditions
var result = products.Where(p => 
    p.Price > 50 && 
    (p.CategoryId == 1 || p.CategoryId == 2) &&
    p.Name.Contains("Laptop"));
```

### Selecting - Select

```csharp
// Select specific properties
var productNames = products.Select(p => p.Name);

// Project to anonymous type
var productInfo = products.Select(p => new
{
    p.ProductId,
    p.Name,
    p.Price
});

// Project to DTO
var productDtos = products.Select(p => new ProductDto
{
    Id = p.ProductId,
    Name = p.Name,
    Price = p.Price,
    Category = p.Category.CategoryName
});
```

### Ordering - OrderBy, ThenBy

```csharp
// Single order
var ordered = products.OrderBy(p => p.Price);

// Descending
var orderedDesc = products.OrderByDescending(p => p.Price);

// Multiple ordering
var multiOrder = products
    .OrderBy(p => p.CategoryId)
    .ThenByDescending(p => p.Price)
    .ThenBy(p => p.Name);
```

### Grouping - GroupBy

```csharp
// Group by category
var grouped = products.GroupBy(p => p.CategoryId);

foreach (var group in grouped)
{
    Console.WriteLine($"Category: {group.Key}");
    foreach (var product in group)
    {
        Console.WriteLine($"  - {product.Name}");
    }
}

// Group with aggregation
var categoryStats = products
    .GroupBy(p => p.CategoryId)
    .Select(g => new
    {
        CategoryId = g.Key,
        Count = g.Count(),
        TotalValue = g.Sum(p => p.Price),
        AveragePrice = g.Average(p => p.Price),
        MinPrice = g.Min(p => p.Price),
        MaxPrice = g.Max(p => p.Price)
    });
```

### Joining - Join

```csharp
// Inner join
var productsWithCategory = products
    .Join(categories,
        product => product.CategoryId,
        category => category.CategoryId,
        (product, category) => new
        {
            product.Name,
            product.Price,
            CategoryName = category.CategoryName
        });

// Left join (using GroupJoin)
var leftJoin = products
    .GroupJoin(categories,
        p => p.CategoryId,
        c => c.CategoryId,
        (p, c) => new { Product = p, Categories = c })
    .SelectMany(
        x => x.Categories.DefaultIfEmpty(),
        (x, category) => new
        {
            x.Product.Name,
            CategoryName = category?.CategoryName ?? "No Category"
        });
```

### Aggregation

```csharp
// Count
var count = products.Count();
var expensiveCount = products.Count(p => p.Price > 100);

// Sum
var totalValue = products.Sum(p => p.Price);

// Average
var avgPrice = products.Average(p => p.Price);

// Min/Max
var minPrice = products.Min(p => p.Price);
var maxPrice = products.Max(p => p.Price);

// Any/All
bool hasExpensive = products.Any(p => p.Price > 1000);
bool allInStock = products.All(p => p.StockQuantity > 0);
```

### Pagination

```csharp
// Skip and Take
var page1 = products
    .OrderBy(p => p.Name)
    .Skip(0)
    .Take(10);

var page2 = products
    .OrderBy(p => p.Name)
    .Skip(10)
    .Take(10);

// Generic pagination
public async Task<PagedResult<Product>> GetPagedAsync(int pageNumber, int pageSize)
{
    var query = _context.Products.AsQueryable();
    
    var totalCount = await query.CountAsync();
    
    var items = await query
        .OrderBy(p => p.Name)
        .Skip((pageNumber - 1) * pageSize)
        .Take(pageSize)
        .ToListAsync();
    
    return new PagedResult<Product>
    {
        Items = items,
        TotalCount = totalCount,
        PageNumber = pageNumber,
        PageSize = pageSize
    };
}
```

---

## Real-World Examples

### E-Commerce Product Search

```csharp
public async Task<List<ProductDto>> SearchProductsAsync(ProductSearchDto search)
{
    var query = _context.Products.AsQueryable();
    
    // Filter by search term
    if (!string.IsNullOrEmpty(search.SearchTerm))
    {
        query = query.Where(p => 
            p.Name.Contains(search.SearchTerm) ||
            p.Description.Contains(search.SearchTerm));
    }
    
    // Filter by category
    if (search.CategoryId.HasValue)
    {
        query = query.Where(p => p.CategoryId == search.CategoryId.Value);
    }
    
    // Filter by price range
    if (search.MinPrice.HasValue)
    {
        query = query.Where(p => p.Price >= search.MinPrice.Value);
    }
    
    if (search.MaxPrice.HasValue)
    {
        query = query.Where(p => p.Price <= search.MaxPrice.Value);
    }
    
    // Filter by availability
    if (search.InStockOnly)
    {
        query = query.Where(p => p.StockQuantity > 0);
    }
    
    // Sorting
    query = search.SortBy switch
    {
        "price_asc" => query.OrderBy(p => p.Price),
        "price_desc" => query.OrderByDescending(p => p.Price),
        "name_asc" => query.OrderBy(p => p.Name),
        "name_desc" => query.OrderByDescending(p => p.Name),
        _ => query.OrderBy(p => p.ProductId)
    };
    
    // Pagination
    var result = await query
        .Skip((search.PageNumber - 1) * search.PageSize)
        .Take(search.PageSize)
        .Select(p => new ProductDto
        {
            Id = p.ProductId,
            Name = p.Name,
            Price = p.Price,
            CategoryName = p.Category.CategoryName,
            InStock = p.StockQuantity > 0
        })
        .ToListAsync();
    
    return result;
}
```

### Sales Report with Complex Aggregations

```csharp
public async Task<SalesReportDto> GetSalesReportAsync(DateTime startDate, DateTime endDate)
{
    var salesData = await _context.Orders
        .Where(o => o.OrderDate >= startDate && o.OrderDate <= endDate)
        .Include(o => o.OrderDetails)
            .ThenInclude(od => od.Product)
                .ThenInclude(p => p.Category)
        .ToListAsync();
    
    var report = new SalesReportDto
    {
        TotalOrders = salesData.Count(),
        TotalRevenue = salesData.Sum(o => o.TotalAmount),
        AverageOrderValue = salesData.Average(o => o.TotalAmount),
        
        TopSellingProducts = salesData
            .SelectMany(o => o.OrderDetails)
            .GroupBy(od => new { od.ProductId, od.Product.Name })
            .Select(g => new TopProductDto
            {
                ProductId = g.Key.ProductId,
                ProductName = g.Key.Name,
                TotalQuantitySold = g.Sum(od => od.Quantity),
                TotalRevenue = g.Sum(od => od.Quantity * od.UnitPrice)
            })
            .OrderByDescending(p => p.TotalRevenue)
            .Take(10)
            .ToList(),
        
        SalesByCategory = salesData
            .SelectMany(o => o.OrderDetails)
            .GroupBy(od => od.Product.Category.CategoryName)
            .Select(g => new CategorySalesDto
            {
                CategoryName = g.Key,
                TotalSales = g.Sum(od => od.Quantity * od.UnitPrice),
                ItemsSold = g.Sum(od => od.Quantity)
            })
            .OrderByDescending(c => c.TotalSales)
            .ToList(),
        
        DailySales = salesData
            .GroupBy(o => o.OrderDate.Date)
            .Select(g => new DailySalesDto
            {
                Date = g.Key,
                OrderCount = g.Count(),
                Revenue = g.Sum(o => o.TotalAmount)
            })
            .OrderBy(d => d.Date)
            .ToList()
    };
    
    return report;
}
```

---

## LINQ Optimization Tips

### 1. Use AsNoTracking for Read-Only Queries

```csharp
// ❌ BAD - Tracking overhead
var products = await _context.Products.ToListAsync();

// ✅ GOOD - No tracking, faster
var products = await _context.Products
    .AsNoTracking()
    .ToListAsync();
```

### 2. Select Only What You Need

```csharp
// ❌ BAD - Loads entire entity
var products = await _context.Products.ToListAsync();

// ✅ GOOD - Only specific columns
var productNames = await _context.Products
    .Select(p => new { p.ProductId, p.Name })
    .ToListAsync();
```

### 3. Filter Early (Server-Side)

```csharp
// ❌ BAD - Loads all, filters in memory
var products = await _context.Products.ToListAsync();
var filtered = products.Where(p => p.Price > 100);

// ✅ GOOD - Filters in database
var filtered = await _context.Products
    .Where(p => p.Price > 100)
    .ToListAsync();
```

### 4. Avoid N+1 Query Problem

```csharp
// ❌ BAD - N+1 queries
var products = await _context.Products.ToListAsync();
foreach (var product in products)
{
    var category = await _context.Categories
        .FirstAsync(c => c.CategoryId == product.CategoryId);  // N queries!
}

// ✅ GOOD - Single query with Include
var products = await _context.Products
    .Include(p => p.Category)
    .ToListAsync();
```

### 5. Use Compiled Queries for Repeated Queries

```csharp
// Define compiled query
private static readonly Func<AppDbContext, int, Task<Product>> _getProductById =
    EF.CompileAsyncQuery((AppDbContext context, int id) =>
        context.Products.FirstOrDefault(p => p.ProductId == id));

// Use compiled query (faster on repeated calls)
var product = await _getProductById(_context, productId);
```

### 6. Avoid Loading Large Collections

```csharp
// ❌ BAD - Can load thousands of records
var category = await _context.Categories
    .Include(c => c.Products)
    .FirstAsync(c => c.CategoryId == 1);

// ✅ GOOD - Paginate or filter
var category = await _context.Categories
    .Include(c => c.Products.Where(p => p.Price > 50).Take(10))
    .FirstAsync(c => c.CategoryId == 1);
```

### 7. Use Any() Instead of Count() > 0

```csharp
// ❌ BAD - Counts all records
if (await _context.Products.CountAsync() > 0)

// ✅ GOOD - Stops at first match
if (await _context.Products.AnyAsync())
```

### 8. Avoid Mixing Client and Server Evaluation

```csharp
// ❌ BAD - Calls C# method in query (client evaluation)
var products = await _context.Products
    .Where(p => IsExpensive(p.Price))  // Can't translate to SQL!
    .ToListAsync();

// ✅ GOOD - Use SQL-compatible operations
var products = await _context.Products
    .Where(p => p.Price > 100)
    .ToListAsync();
```

---

## Common LINQ Patterns

### Find or Default

```csharp
var product = await _context.Products
    .FirstOrDefaultAsync(p => p.ProductId == id);

if (product == null)
    throw new NotFoundException($"Product {id} not found");
```

### Distinct

```csharp
var uniqueCities = customers
    .Select(c => c.City)
    .Distinct();
```

### Union, Intersect, Except

```csharp
var list1 = new[] { 1, 2, 3, 4 };
var list2 = new[] { 3, 4, 5, 6 };

var union = list1.Union(list2);        // 1,2,3,4,5,6
var intersect = list1.Intersect(list2); // 3,4
var except = list1.Except(list2);       // 1,2
```

---

## Summary

**LINQ Benefits:**
- ✅ Type-safe queries
- ✅ IntelliSense support
- ✅ Readable code
- ✅ Works with multiple data sources

**Optimization Keys:**
1. Use `AsNoTracking()` for reads
2. Select only needed columns
3. Filter server-side with `Where()`
4. Use `Include()` to avoid N+1
5. Use `Any()` instead of `Count() > 0`
6. Avoid client evaluation

Master LINQ for efficient data querying!
