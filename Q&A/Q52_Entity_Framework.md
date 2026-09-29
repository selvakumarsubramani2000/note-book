# Question 52: Entity Framework or Dapper ORM

## Answer

### What are ORMs?

**ORM (Object-Relational Mapping)** tools map database tables to C# classes, allowing you to work with databases using objects instead of raw SQL.

**Entity Framework (EF)** and **Dapper** are the two most popular ORMs in .NET.

---

## Entity Framework Core

### What is Entity Framework Core?

**Entity Framework Core** is a full-featured, heavy-weight ORM that provides:
- Automatic query generation
- Change tracking
- Migrations
- LINQ support
- Lazy loading
- Complete abstraction from SQL

### Installation

```bash
dotnet add package Microsoft.EntityFrameworkCore
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
dotnet add package Microsoft.EntityFrameworkCore.Tools
```

### Basic Setup

```csharp
// 1. Define Entity Classes
public class Product
{
    public int ProductId { get; set; }
    public string Name { get; set; }
    public decimal Price { get; set; }
    public int CategoryId { get; set; }
    
    // Navigation property
    public Category Category { get; set; }
    public ICollection<OrderDetail> OrderDetails { get; set; }
}

public class Category
{
    public int CategoryId { get; set; }
    public string CategoryName { get; set; }
    
    public ICollection<Product> Products { get; set; }
}

public class Order
{
    public int OrderId { get; set; }
    public DateTime OrderDate { get; set; }
    public decimal TotalAmount { get; set; }
    public int CustomerId { get; set; }
    
    public ICollection<OrderDetail> OrderDetails { get; set; }
}

public class OrderDetail
{
    public int OrderDetailId { get; set; }
    public int OrderId { get; set; }
    public int ProductId { get; set; }
    public int Quantity { get; set; }
    public decimal UnitPrice { get; set; }
    
    public Order Order { get; set; }
    public Product Product { get; set; }
}

// 2. Create DbContext
public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options)
        : base(options)
    {
    }
    
    public DbSet<Product> Products { get; set; }
    public DbSet<Category> Categories { get; set; }
    public DbSet<Order> Orders { get; set; }
    public DbSet<OrderDetail> OrderDetails { get; set; }
    
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Configure relationships
        modelBuilder.Entity<Product>()
            .HasOne(p => p.Category)
            .WithMany(c => c.Products)
            .HasForeignKey(p => p.CategoryId);
        
        modelBuilder.Entity<OrderDetail>()
            .HasOne(od => od.Order)
            .WithMany(o => o.OrderDetails)
            .HasForeignKey(od => od.OrderId);
        
        modelBuilder.Entity<OrderDetail>()
            .HasOne(od => od.Product)
            .WithMany(p => p.OrderDetails)
            .HasForeignKey(od => od.ProductId);
        
        // Configure properties
        modelBuilder.Entity<Product>()
            .Property(p => p.Price)
            .HasPrecision(10, 2);
    }
}

// 3. Register in Startup.cs
public void ConfigureServices(IServiceCollection services)
{
    services.AddDbContext<AppDbContext>(options =>
        options.UseSqlServer(Configuration.GetConnectionString("DefaultConnection")));
}
```

### CRUD Operations with Entity Framework

```csharp
public class ProductRepository
{
    private readonly AppDbContext _context;
    
    public ProductRepository(AppDbContext context)
    {
        _context = context;
    }
    
    // CREATE
    public async Task<Product> CreateAsync(Product product)
    {
        _context.Products.Add(product);
        await _context.SaveChangesAsync();
        return product;
    }
    
    // READ - Single
    public async Task<Product> GetByIdAsync(int id)
    {
        return await _context.Products
            .Include(p => p.Category)  // Eager loading
            .FirstOrDefaultAsync(p => p.ProductId == id);
    }
    
    // READ - All
    public async Task<List<Product>> GetAllAsync()
    {
        return await _context.Products
            .Include(p => p.Category)
            .ToListAsync();
    }
    
    // READ - With filtering
    public async Task<List<Product>> GetByCategoryAsync(int categoryId)
    {
        return await _context.Products
            .Where(p => p.CategoryId == categoryId)
            .Where(p => p.Price > 0)
            .OrderBy(p => p.Name)
            .ToListAsync();
    }
    
    // UPDATE
    public async Task<Product> UpdateAsync(Product product)
    {
        _context.Products.Update(product);
        await _context.SaveChangesAsync();
        return product;
    }
    
    // DELETE
    public async Task<bool> DeleteAsync(int id)
    {
        var product = await _context.Products.FindAsync(id);
        if (product == null)
            return false;
        
        _context.Products.Remove(product);
        await _context.SaveChangesAsync();
        return true;
    }
    
    // Complex query
    public async Task<List<Product>> SearchAsync(string searchTerm, decimal minPrice, decimal maxPrice)
    {
        return await _context.Products
            .Include(p => p.Category)
            .Where(p => p.Name.Contains(searchTerm) || p.Category.CategoryName.Contains(searchTerm))
            .Where(p => p.Price >= minPrice && p.Price <= maxPrice)
            .OrderBy(p => p.Name)
            .Take(50)
            .ToListAsync();
    }
}
```

### EF Core Features

#### 1. Migrations

```bash
# Create migration
dotnet ef migrations add InitialCreate

# Update database
dotnet ef database update

# Rollback migration
dotnet ef database update PreviousMigration
```

#### 2. Tracking vs No-Tracking

```csharp
// With tracking (default) - slower, but can update
var product = await _context.Products.FindAsync(id);
product.Price = 99.99;
await _context.SaveChangesAsync();  // Automatically tracked

// No tracking - faster for read-only
var products = await _context.Products
    .AsNoTracking()
    .ToListAsync();
```

#### 3. Raw SQL

```csharp
// Execute raw SQL
var products = await _context.Products
    .FromSqlRaw("SELECT * FROM Products WHERE Price > {0}", 50)
    .ToListAsync();

// Execute stored procedure
var result = await _context.Database
    .ExecuteSqlRawAsync("EXEC UpdateProductPrices @Category = {0}", "Electronics");
```

---

## Dapper

### What is Dapper?

**Dapper** is a lightweight, micro-ORM that provides:
- Fast performance (close to raw ADO.NET)
- Manual query writing
- Minimal overhead
- Simple object mapping
- No change tracking
- No migrations

### Installation

```bash
dotnet add package Dapper
dotnet add package Microsoft.Data.SqlClient
```

### Basic Setup

```csharp
public class ProductRepository
{
    private readonly string _connectionString;
    
    public ProductRepository(IConfiguration configuration)
    {
        _connectionString = configuration.GetConnectionString("DefaultConnection");
    }
    
    private IDbConnection CreateConnection()
    {
        return new SqlConnection(_connectionString);
    }
}
```

### CRUD Operations with Dapper

```csharp
using Dapper;

public class ProductRepository
{
    private readonly string _connectionString;
    
    public ProductRepository(IConfiguration configuration)
    {
        _connectionString = configuration.GetConnectionString("DefaultConnection");
    }
    
    // CREATE
    public async Task<int> CreateAsync(Product product)
    {
        using var connection = new SqlConnection(_connectionString);
        
        var sql = @"INSERT INTO Products (Name, Price, CategoryId) 
                    VALUES (@Name, @Price, @CategoryId);
                    SELECT CAST(SCOPE_IDENTITY() as int);";
        
        return await connection.QuerySingleAsync<int>(sql, product);
    }
    
    // READ - Single
    public async Task<Product> GetByIdAsync(int id)
    {
        using var connection = new SqlConnection(_connectionString);
        
        var sql = @"SELECT p.*, c.CategoryName 
                    FROM Products p
                    INNER JOIN Categories c ON p.CategoryId = c.CategoryId
                    WHERE p.ProductId = @Id";
        
        return await connection.QuerySingleOrDefaultAsync<Product>(sql, new { Id = id });
    }
    
    // READ - All
    public async Task<IEnumerable<Product>> GetAllAsync()
    {
        using var connection = new SqlConnection(_connectionString);
        
        var sql = "SELECT * FROM Products ORDER BY Name";
        
        return await connection.QueryAsync<Product>(sql);
    }
    
    // READ - With parameters
    public async Task<IEnumerable<Product>> GetByCategoryAsync(int categoryId)
    {
        using var connection = new SqlConnection(_connectionString);
        
        var sql = @"SELECT * FROM Products 
                    WHERE CategoryId = @CategoryId 
                    ORDER BY Name";
        
        return await connection.QueryAsync<Product>(sql, new { CategoryId = categoryId });
    }
    
    // UPDATE
    public async Task<bool> UpdateAsync(Product product)
    {
        using var connection = new SqlConnection(_connectionString);
        
        var sql = @"UPDATE Products 
                    SET Name = @Name, Price = @Price, CategoryId = @CategoryId 
                    WHERE ProductId = @ProductId";
        
        var affectedRows = await connection.ExecuteAsync(sql, product);
        return affectedRows > 0;
    }
    
    // DELETE
    public async Task<bool> DeleteAsync(int id)
    {
        using var connection = new SqlConnection(_connectionString);
        
        var sql = "DELETE FROM Products WHERE ProductId = @Id";
        
        var affectedRows = await connection.ExecuteAsync(sql, new { Id = id });
        return affectedRows > 0;
    }
    
    // Multiple results
    public async Task<(IEnumerable<Product> products, int totalCount)> GetPagedAsync(
        int pageNumber, int pageSize)
    {
        using var connection = new SqlConnection(_connectionString);
        
        var sql = @"
            SELECT * FROM Products 
            ORDER BY Name 
            OFFSET @Offset ROWS FETCH NEXT @PageSize ROWS ONLY;
            
            SELECT COUNT(*) FROM Products;";
        
        using var multi = await connection.QueryMultipleAsync(sql, 
            new { Offset = (pageNumber - 1) * pageSize, PageSize = pageSize });
        
        var products = await multi.ReadAsync<Product>();
        var totalCount = await multi.ReadSingleAsync<int>();
        
        return (products, totalCount);
    }
    
    // Stored Procedure
    public async Task<IEnumerable<Product>> GetProductsByCategoryProc(int categoryId)
    {
        using var connection = new SqlConnection(_connectionString);
        
        return await connection.QueryAsync<Product>(
            "GetProductsByCategory",
            new { CategoryId = categoryId },
            commandType: CommandType.StoredProcedure);
    }
}
```

---

## Entity Framework vs Dapper

| Feature | Entity Framework Core | Dapper |
|---------|----------------------|--------|
| **Performance** | Slower (tracking overhead) | Very fast (minimal overhead) |
| **Complexity** | High learning curve | Simple, easy to learn |
| **SQL Control** | Automatic (LINQ) | Manual (write SQL) |
| **Change Tracking** | ✅ Yes | ❌ No |
| **Migrations** | ✅ Yes | ❌ No |
| **Lazy Loading** | ✅ Yes | ❌ No |
| **Code First** | ✅ Yes | ❌ No |
| **Raw SQL** | Possible | Native |
| **Best For** | Complex domain models | Performance-critical, simple queries |

---

## When to Use Each

### Use Entity Framework When:

✅ **Complex domain models** with many relationships  
✅ **Rapid development** - less code to write  
✅ **Change tracking** needed  
✅ **Code-first** approach preferred  
✅ **Migrations** needed for database evolution  

### Use Dapper When:

✅ **Performance is critical** - high-throughput systems  
✅ **Simple CRUD** operations  
✅ **Complex SQL** queries needed  
✅ **Database-first** approach  
✅ **Existing stored procedures** to use  

---

## Best Practices

### Entity Framework:
1. ✅ Use `AsNoTracking()` for read-only queries
2. ✅ Use `Include()` for eager loading to avoid N+1 queries
3. ✅ Avoid loading entire tables - use `Where()` first
4. ✅ Use projections (`Select`) when you don't need full entities
5. ✅ Dispose DbContext properly (use DI with Scoped lifetime)

### Dapper:
1. ✅ Use parameterized queries (prevent SQL injection)
2. ✅ Dispose connections properly (use `using` statements)
3. ✅ Use `QueryAsync` for better scalability
4. ✅ Consider caching connection strings
5. ✅ Use `QueryMultipleAsync` for multiple result sets

---

## Summary

**Entity Framework Core:**
- Full-featured ORM
- Automatic query generation
- Best for complex applications
- Slower but more features

**Dapper:**
- Lightweight micro-ORM
- Manual SQL queries
- Best for performance
- Faster but more code

Many projects use **both**: EF Core for complex operations, Dapper for performance-critical queries!
