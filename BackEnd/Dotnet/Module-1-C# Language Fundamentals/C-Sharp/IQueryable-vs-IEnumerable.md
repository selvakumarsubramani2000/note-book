# IQueryable vs IEnumerable — Complete Guide

> **Goal:** Understand `IQueryable<T>` and `IEnumerable<T>`, when to use each, and how they impact performance in real-world applications.

**Context:** This guide uses the **Vendor Directory** domain (Vendors, Categories, Users) to demonstrate practical differences.

---

## 📑 Table of Contents

1. [What is IEnumerable&lt;T&gt;?](#1-what-is-ienumerablet)
2. [What is IQueryable&lt;T&gt;?](#2-what-is-iqueryablet)
3. [Key Differences](#3-key-differences)
4. [Execution: Deferred vs Immediate](#4-execution-deferred-vs-immediate)
5. [Performance Comparison](#5-performance-comparison)
6. [When to Use Which?](#6-when-to-use-which)
7. [Real-World Examples](#7-real-world-examples)
8. [Common Pitfalls](#8-common-pitfalls)
9. [Best Practices](#9-best-practices)

---

## 1. What is IEnumerable&lt;T&gt;?

`IEnumerable<T>` is the **base interface** for all collections in C# that can be iterated (foreach-able).

### Definition
```csharp
namespace System.Collections.Generic
{
    public interface IEnumerable<T> : IEnumerable
    {
        IEnumerator<T> GetEnumerator();
    }
}
```

### Key Characteristics

- **In-Memory Iteration**: Works with collections already loaded in memory
- **Forward-Only**: Can only move forward through the collection
- **LINQ to Objects**: Uses **in-memory** LINQ operators
- **Execution**: Query logic executes **in .NET runtime** (client-side)
- **Namespace**: `System.Collections.Generic`

### Basic Example
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

// In-memory collection
List<Vendor> vendors = new List<Vendor>
{
    new Vendor { Id = 1, Name = "Acme Corp", IsActive = true, Rating = 4.5m },
    new Vendor { Id = 2, Name = "Globex Inc", IsActive = false, Rating = 3.8m },
    new Vendor { Id = 3, Name = "Initech", IsActive = true, Rating = 4.9m }
};

// IEnumerable<Vendor> - data already in memory
IEnumerable<Vendor> activeVendors = vendors.Where(v => v.IsActive);

// Iteration
foreach (var vendor in activeVendors)
{
    Console.WriteLine(vendor.Name);
}
// Output:
// Acme Corp
// Initech
```

### What Happens Behind the Scenes?
1. All vendors are **already in memory** (`List<Vendor>`)
2. `.Where()` iterates through **in-memory** collection
3. Filtering happens **in C# code** (client-side)
4. No database query is generated

---

## 2. What is IQueryable&lt;T&gt;?

`IQueryable<T>` is an interface for **building and executing queries** against a data source (usually a database).

### Definition
```csharp
namespace System.Linq
{
    public interface IQueryable<T> : IEnumerable<T>, IQueryable
    {
        Type ElementType { get; }
        Expression Expression { get; }      // 🔑 Expression Tree
        IQueryProvider Provider { get; }    // 🔑 Query Provider
    }
}
```

### Key Characteristics

- **Queryable Data Source**: Works with remote data sources (databases, web services)
- **Expression Trees**: Builds **expression trees** that represent queries
- **LINQ to SQL/EF**: Translates LINQ to **SQL queries**
- **Execution**: Query logic executes **on the server** (database)
- **Namespace**: `System.Linq`
- **Implements `IEnumerable<T>`**: Can be treated as enumerable when needed

### Basic Example
```csharp
using System;
using System.Linq;
using Microsoft.EntityFrameworkCore;

public class VendorDbContext : DbContext
{
    public DbSet<Vendor> Vendors { get; set; }
}

// Using IQueryable with Entity Framework
using (var context = new VendorDbContext())
{
    // IQueryable<Vendor> - data still in database
    IQueryable<Vendor> activeVendors = context.Vendors.Where(v => v.IsActive);
    
    // Query hasn't executed yet! (deferred execution)
    
    // Query executes NOW when we iterate
    foreach (var vendor in activeVendors)
    {
        Console.WriteLine(vendor.Name);
    }
}
```

### What Happens Behind the Scenes?
1. `.Where()` builds an **expression tree** (not executed yet)
2. When iteration starts, expression tree is translated to **SQL**:
   ```sql
   SELECT Id, Name, IsActive, Rating
   FROM Vendors
   WHERE IsActive = 1
   ```
3. SQL executes **on the database server**
4. Only filtered results are brought to memory

### Expression Trees (The Secret Sauce)

`IQueryable<T>` uses **expression trees** to represent code as data:

```csharp
// This lambda: v => v.IsActive
// Becomes an expression tree that can be analyzed and translated

Expression<Func<Vendor, bool>> expr = v => v.IsActive;

// The provider (e.g., EF Core) analyzes this tree and generates:
// SQL: WHERE IsActive = 1
```

---

## 3. Key Differences

| Feature | `IEnumerable<T>` | `IQueryable<T>` |
|---------|------------------|-----------------|
| **Namespace** | `System.Collections.Generic` | `System.Linq` |
| **Inheritance** | Base interface | Inherits from `IEnumerable<T>` |
| **Data Location** | In-memory (client-side) | Remote source (server-side) |
| **Query Execution** | In .NET runtime (C# code) | On data source (SQL server) |
| **Query Building** | Delegates (`Func<T>`) | Expression Trees (`Expression<Func<T>>`) |
| **LINQ Provider** | LINQ to Objects | LINQ to SQL, LINQ to EF, etc. |
| **Use Case** | Collections, arrays, lists | Databases, OData, web services |
| **Performance** | All data in memory first | Filters at source (efficient) |
| **Deferred Execution** | Yes (for LINQ operators) | Yes (until materialization) |
| **Query Translation** | No (direct execution) | Yes (to SQL, OData, etc.) |
| **Best For** | Small in-memory datasets | Large datasets in databases |

### Visual Comparison

```
IEnumerable<T> (In-Memory)
┌─────────────────────────────────────┐
│  Database                           │
│  ↓ (all 1,000,000 rows)             │
│  Application Memory                 │
│  ├─ Vendor 1                        │
│  ├─ Vendor 2                        │
│  ├─ ...                             │
│  └─ Vendor 1,000,000                │
│  ↓ (filter in C#)                   │
│  Result: 10 active vendors          │
└─────────────────────────────────────┘
⚠️ Loads ALL data to memory first!


IQueryable<T> (Server-Side)
┌─────────────────────────────────────┐
│  Database                           │
│  ↓ (SQL: WHERE IsActive = 1)        │
│  Database filters 1,000,000 rows    │
│  ↓ (only 10 rows)                   │
│  Application Memory                 │
│  ├─ Vendor 1                        │
│  ├─ ...                             │
│  └─ Vendor 10                       │
│  Result: 10 active vendors          │
└─────────────────────────────────────┘
✅ Only filtered data comes to memory!
```

---

## 4. Execution: Deferred vs Immediate

Both `IEnumerable<T>` and `IQueryable<T>` support **deferred execution**, but they differ in **where** the execution happens.

### Deferred Execution (Lazy Evaluation)

Query doesn't execute until you **materialize** it (iterate or call terminal operators).

```csharp
// ❌ Query NOT executed yet
IQueryable<Vendor> query = context.Vendors.Where(v => v.Rating > 4.0m);

// ✅ Query executes NOW
var results = query.ToList();  // Terminal operator
```

### Terminal Operators (Force Execution)

| Operator | Returns | Description |
|----------|---------|-------------|
| `ToList()` | `List<T>` | Executes query, returns list |
| `ToArray()` | `T[]` | Executes query, returns array |
| `ToDictionary()` | `Dictionary<K,V>` | Executes query, returns dictionary |
| `ToHashSet()` | `HashSet<T>` | Executes query, returns hash set |
| `Count()` | `int` | Executes, returns count |
| `First()` | `T` | Executes, returns first element |
| `Single()` | `T` | Executes, returns single element |
| `Any()` | `bool` | Executes, returns true/false |
| `Sum()` | numeric | Executes, returns sum |
| `Average()` | numeric | Executes, returns average |

### Example: Deferred Execution
```csharp
// Building the query (not executed)
var query = context.Vendors
    .Where(v => v.IsActive)
    .OrderBy(v => v.Name)
    .Select(v => new { v.Id, v.Name });

Console.WriteLine("Query built, but not executed yet!");

// Now it executes
var vendors = query.ToList();  // 💥 SQL query runs here

// Generated SQL:
// SELECT Id, Name
// FROM Vendors
// WHERE IsActive = 1
// ORDER BY Name
```

---

## 5. Performance Comparison

### Scenario 1: Filtering 1 Million Records

#### ❌ IEnumerable (Poor Performance)
```csharp
// BAD: Loads ALL 1 million vendors to memory
IEnumerable<Vendor> allVendors = context.Vendors.AsEnumerable();

// Filter in C# code (in-memory)
var activeVendors = allVendors.Where(v => v.IsActive).ToList();

// What happens:
// 1. SELECT * FROM Vendors (1 million rows)
// 2. Load all to memory (~500 MB)
// 3. Filter in C# code
// ⚠️ Time: ~5 seconds, Memory: ~500 MB
```

#### ✅ IQueryable (Excellent Performance)
```csharp
// GOOD: Filters at database level
IQueryable<Vendor> activeVendors = context.Vendors.Where(v => v.IsActive);
var result = activeVendors.ToList();

// What happens:
// 1. SELECT * FROM Vendors WHERE IsActive = 1 (10,000 rows)
// 2. Load only filtered results (~5 MB)
// ✅ Time: ~100 ms, Memory: ~5 MB
```

### Scenario 2: Pagination

#### ❌ IEnumerable (Inefficient)
```csharp
// BAD: Loads all data, then skips/takes in memory
var page = context.Vendors
    .AsEnumerable()              // ⚠️ Converts to IEnumerable
    .Skip(100)
    .Take(10)
    .ToList();

// SQL: SELECT * FROM Vendors (all rows)
// Then C# does Skip/Take in memory
```

#### ✅ IQueryable (Efficient)
```csharp
// GOOD: Skip/Take translated to SQL
var page = context.Vendors
    .Skip(100)
    .Take(10)
    .ToList();

// SQL: SELECT * FROM Vendors 
//      ORDER BY Id 
//      OFFSET 100 ROWS 
//      FETCH NEXT 10 ROWS ONLY
```

### Performance Summary Table

| Operation | IEnumerable | IQueryable | Winner |
|-----------|-------------|------------|--------|
| Filter 1M rows | 5 sec, 500 MB | 100 ms, 5 MB | IQueryable |
| Pagination | Loads all rows | Loads only page | IQueryable |
| Sorting | In-memory sort | Database sort | IQueryable |
| Joining | In-memory join | SQL JOIN | IQueryable |
| Aggregates | Loops all data | SQL COUNT/SUM | IQueryable |

---

## 6. When to Use Which?

### Use `IEnumerable&lt;T&gt;` When:

✅ **Working with in-memory collections**
```csharp
List<Vendor> vendors = GetVendorsFromCache();
IEnumerable<Vendor> filtered = vendors.Where(v => v.Rating > 4);
```

✅ **Small datasets already loaded**
```csharp
var categories = new[] { "Electronics", "Groceries", "Books" };
var sorted = categories.OrderBy(c => c);
```

✅ **Using LINQ operations not supported by query provider**
```csharp
// Some complex C# logic not translatable to SQL
var results = context.Vendors
    .ToList()  // Load to memory first
    .Where(v => ComplexCSharpMethod(v));
```

✅ **After materialization (ToList, ToArray)**
```csharp
List<Vendor> vendors = context.Vendors.ToList();  // Now it's IEnumerable
var active = vendors.Where(v => v.IsActive);      // In-memory filtering
```

### Use `IQueryable&lt;T&gt;` When:

✅ **Querying databases (EF Core, Dapper, LINQ to SQL)**
```csharp
IQueryable<Vendor> query = context.Vendors.Where(v => v.IsActive);
```

✅ **Large datasets that need filtering at source**
```csharp
// Efficient: only 100 rows loaded
var topVendors = context.Vendors
    .Where(v => v.Rating > 4.5m)
    .OrderByDescending(v => v.Rating)
    .Take(100)
    .ToList();
```

✅ **Building dynamic queries**
```csharp
IQueryable<Vendor> query = context.Vendors;

if (isActiveFilter)
    query = query.Where(v => v.IsActive);

if (minRating.HasValue)
    query = query.Where(v => v.Rating >= minRating.Value);

var results = query.ToList();  // Single SQL query with all filters
```

✅ **OData APIs or remote data sources**
```csharp
// Web API controller
[HttpGet]
public IQueryable<Vendor> GetVendors()
{
    return _context.Vendors;  // Allows client to add filters via OData
}
```

---

## 7. Real-World Examples

### Example 1: Vendor Search (Entity Framework Core)

```csharp
public class VendorService
{
    private readonly VendorDbContext _context;
    
    public VendorService(VendorDbContext context)
    {
        _context = context;
    }
    
    // ✅ GOOD: Use IQueryable for database queries
    public async Task<List<Vendor>> SearchVendors(string searchTerm, decimal? minRating)
    {
        IQueryable<Vendor> query = _context.Vendors;
        
        if (!string.IsNullOrEmpty(searchTerm))
        {
            query = query.Where(v => v.Name.Contains(searchTerm));
        }
        
        if (minRating.HasValue)
        {
            query = query.Where(v => v.Rating >= minRating.Value);
        }
        
        // Executes as single SQL query:
        // SELECT * FROM Vendors 
        // WHERE Name LIKE '%searchTerm%' AND Rating >= @minRating
        return await query.ToListAsync();
    }
    
    // ❌ BAD: Converting to IEnumerable too early
    public List<Vendor> SearchVendorsBad(string searchTerm)
    {
        IEnumerable<Vendor> allVendors = _context.Vendors.AsEnumerable();
        
        // Filter happens in C# code after loading ALL vendors
        return allVendors
            .Where(v => v.Name.Contains(searchTerm))
            .ToList();
    }
}
```

### Example 2: Repository Pattern

```csharp
public interface IRepository<T> where T : class
{
    // Return IQueryable to allow further composition
    IQueryable<T> GetAll();
    IQueryable<T> FindBy(Expression<Func<T, bool>> predicate);
}

public class Repository<T> : IRepository<T> where T : class
{
    private readonly DbContext _context;
    private readonly DbSet<T> _dbSet;
    
    public Repository(DbContext context)
    {
        _context = context;
        _dbSet = context.Set<T>();
    }
    
    public IQueryable<T> GetAll()
    {
        return _dbSet;  // Returns IQueryable for further filtering
    }
    
    public IQueryable<T> FindBy(Expression<Func<T, bool>> predicate)
    {
        return _dbSet.Where(predicate);
    }
}

// Usage
public class VendorService
{
    private readonly IRepository<Vendor> _vendorRepo;
    
    public List<Vendor> GetActiveVendors()
    {
        // Build query step by step
        return _vendorRepo
            .GetAll()
            .Where(v => v.IsActive)
            .OrderBy(v => v.Name)
            .ToList();  // Single SQL query executed here
    }
}
```

### Example 3: Mixing IQueryable and IEnumerable

```csharp
public List<VendorDto> GetVendorsWithComplexLogic(decimal minRating)
{
    // Step 1: Filter at database (IQueryable)
    IQueryable<Vendor> dbQuery = _context.Vendors
        .Where(v => v.IsActive && v.Rating >= minRating)
        .OrderByDescending(v => v.Rating)
        .Take(100);
    
    // Step 2: Load to memory
    List<Vendor> vendors = dbQuery.ToList();
    
    // Step 3: Apply complex C# logic (IEnumerable)
    IEnumerable<VendorDto> results = vendors.Select(v => new VendorDto
    {
        Id = v.Id,
        Name = v.Name,
        Badge = GetVendorBadge(v),  // Complex C# method
        Score = CalculateScore(v)    // Complex calculation
    });
    
    return results.ToList();
}

// Complex method that can't be translated to SQL
private string GetVendorBadge(Vendor vendor)
{
    if (vendor.Rating >= 4.8m && vendor.OrderCount > 1000)
        return "🏆 Gold";
    if (vendor.Rating >= 4.5m)
        return "🥈 Silver";
    return "🥉 Bronze";
}
```

---

## 8. Common Pitfalls

### Pitfall 1: Premature Materialization

```csharp
// ❌ BAD: ToList() too early
var vendors = context.Vendors.ToList();  // Loads ALL vendors
var active = vendors.Where(v => v.IsActive).ToList();

// ✅ GOOD: Filter first, then materialize
var active = context.Vendors
    .Where(v => v.IsActive)
    .ToList();
```

### Pitfall 2: AsEnumerable() Trap

```csharp
// ❌ BAD: AsEnumerable() switches to in-memory processing
var results = context.Vendors
    .AsEnumerable()              // Everything after this runs in C#
    .Where(v => v.IsActive)
    .OrderBy(v => v.Name)
    .ToList();

// SQL: SELECT * FROM Vendors (all rows!)
// Then filters/sorts in memory

// ✅ GOOD: Keep it as IQueryable
var results = context.Vendors
    .Where(v => v.IsActive)
    .OrderBy(v => v.Name)
    .ToList();

// SQL: SELECT * FROM Vendors WHERE IsActive = 1 ORDER BY Name
```

### Pitfall 3: Mixing Query Providers

```csharp
// ❌ WILL THROW EXCEPTION
var vendors = context.Vendors.Where(v => v.IsActive);
var users = context.Users.Where(u => u.IsActive);

// Can't join IQueryable from different contexts
var combined = vendors.Join(users, ...);  // Runtime error!

// ✅ GOOD: Load to memory first, then join
var vendorList = vendors.ToList();
var userList = users.ToList();
var combined = vendorList.Join(userList, ...);
```

### Pitfall 4: Query Inside Loop

```csharp
// ❌ BAD: N+1 query problem
var vendors = context.Vendors.ToList();
foreach (var vendor in vendors)
{
    // Executes a query for EACH vendor
    var orders = context.Orders
        .Where(o => o.VendorId == vendor.Id)
        .ToList();
}

// ✅ GOOD: Use Include for eager loading
var vendors = context.Vendors
    .Include(v => v.Orders)
    .ToList();

// Or load all orders at once
var vendorIds = vendors.Select(v => v.Id).ToList();
var orders = context.Orders
    .Where(o => vendorIds.Contains(o.VendorId))
    .ToList();
```

---

## 9. Best Practices

### ✅ Best Practice 1: Keep IQueryable as Long as Possible

```csharp
// Build query step by step
public IQueryable<Vendor> BuildVendorQuery(VendorSearchCriteria criteria)
{
    IQueryable<Vendor> query = _context.Vendors;
    
    if (criteria.IsActive.HasValue)
        query = query.Where(v => v.IsActive == criteria.IsActive.Value);
    
    if (!string.IsNullOrEmpty(criteria.SearchTerm))
        query = query.Where(v => v.Name.Contains(criteria.SearchTerm));
    
    return query;  // Don't materialize yet
}

// Caller can add more filters or pagination
var query = BuildVendorQuery(criteria);
var page = query.Skip(50).Take(10).ToList();  // Single SQL query
```

### ✅ Best Practice 2: Use Projection to Reduce Data Transfer

```csharp
// ❌ BAD: Load entire entities
var vendors = context.Vendors
    .Where(v => v.IsActive)
    .ToList();

// ✅ GOOD: Select only needed fields
var vendors = context.Vendors
    .Where(v => v.IsActive)
    .Select(v => new VendorDto
    {
        Id = v.Id,
        Name = v.Name,
        Rating = v.Rating
    })
    .ToList();

// SQL: SELECT Id, Name, Rating FROM Vendors WHERE IsActive = 1
```

### ✅ Best Practice 3: Use AsNoTracking for Read-Only Queries

```csharp
// For read-only operations, disable change tracking
var vendors = context.Vendors
    .AsNoTracking()
    .Where(v => v.IsActive)
    .ToList();

// Faster and uses less memory
```

### ✅ Best Practice 4: Understand When to Use Each

```csharp
// Decision flowchart
IQueryable<Vendor> GetVendors()
{
    // Is data from database? → IQueryable
    // Is data in-memory? → IEnumerable
    // Need to compose queries? → IQueryable
    // Need complex C# logic? → ToList() first, then IEnumerable
    
    return _context.Vendors;  // IQueryable for composition
}
```

---

## 🎯 Key Takeaways

| Concept | Key Point |
|---------|-----------|
| **IEnumerable&lt;T&gt;** | In-memory iteration, LINQ to Objects, client-side execution |
| **IQueryable&lt;T&gt;** | Query building, expression trees, server-side execution |
| **Performance** | IQueryable filters at source, IEnumerable filters in memory |
| **Use IQueryable** | For databases, large datasets, remote sources |
| **Use IEnumerable** | For in-memory collections, after ToList(), complex C# logic |
| **Deferred Execution** | Both support it; execution happens at different locations |
| **Materialization** | ToList/ToArray/Count forces query execution |
| **Golden Rule** | Keep IQueryable as long as possible before materializing |

---

## 📚 Further Reading

- [LINQ Query Execution (Microsoft Docs)](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/linq/query-execution)
- [Expression Trees (Microsoft Docs)](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/expression-trees/)
- [Entity Framework Core Query Optimization](https://docs.microsoft.com/en-us/ef/core/performance/)

---

## 💡 Quick Reference

```csharp
// IEnumerable: In-memory
List<Vendor> vendors = GetVendors();
IEnumerable<Vendor> active = vendors.Where(v => v.IsActive);  // In C# code

// IQueryable: Database
IQueryable<Vendor> query = context.Vendors.Where(v => v.IsActive);  // To SQL

// Conversion
IQueryable<Vendor> queryable = context.Vendors;
IEnumerable<Vendor> enumerable = queryable.AsEnumerable();  // Switch to LINQ to Objects
List<Vendor> list = queryable.ToList();  // Materialize to List

// Return types in methods
public IQueryable<Vendor> GetVendorsQuery() => context.Vendors;  // Allow composition
public List<Vendor> GetVendorsList() => context.Vendors.ToList();  // Final result
```

---

**Happy Querying!** 🚀
