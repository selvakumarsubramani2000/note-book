# 🔍 Querying & Persistence — CRUD, LINQ, Tracking, Loading

> **Trainer's Note:** This is the daily EF Core muscle memory: add/update/delete, write LINQ that becomes SQL, page results, and load related data without accidental performance disasters. Read the generated SQL in your mind as you write LINQ.

---

## 📑 Table of Contents
1. [DbSet and SaveChanges Mental Model](#1-dbset-and-savechanges-mental-model)
2. [Create (Add)](#2-create-add)
3. [Read (Find, First, LINQ)](#3-read-find-first-linq)
4. [Update](#4-update)
5. [Delete (Remove)](#5-delete-remove)
6. [Filtering, Sorting, Projection](#6-filtering-sorting-projection)
7. [Pagination with Skip/Take](#7-pagination-with-skiptake)
8. [Tracking vs AsNoTracking](#8-tracking-vs-asnotracking)
9. [Loading Related Data](#9-loading-related-data)
10. [Async APIs and Cancellation](#10-async-apis-and-cancellation)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. DbSet and SaveChanges Mental Model

```
DbContext tracks changes in memory
        │
   Add / modify / remove entities
        │
        ▼
   SaveChanges / SaveChangesAsync
        │
        ▼
   SQL INSERT/UPDATE/DELETE sent in a transaction
```

| Concept | Meaning |
|---------|---------|
| `DbSet<Product>` | Query + change entry point for products |
| **Tracked entity** | Context watches property changes |
| `SaveChanges()` | Persists pending inserts/updates/deletes |
| Unit of work (built-in) | One context can batch multiple changes |

```csharp
_db.Products.Add(product);
_db.Products.Add(another);
await _db.SaveChangesAsync(); // both saved together
```

---

## 2. Create (Add)

```csharp
public async Task<Product> CreateAsync(string name, decimal price, int categoryId, CancellationToken ct)
{
    var product = new Product
    {
        Name = name,
        Price = price,
        CategoryId = categoryId,
        IsActive = true,
        CreatedAtUtc = DateTime.UtcNow
    };

    _db.Products.Add(product);
    await _db.SaveChangesAsync(ct);
    // product.Id populated for identity columns after save
    return product;
}
```

### AddRange
```csharp
_db.Products.AddRange(p1, p2, p3);
await _db.SaveChangesAsync(ct);
```

---

## 3. Read (Find, First, LINQ)

### Find (by PK, may use store/local cache)
```csharp
var product = await _db.Products.FindAsync(new object[] { id }, ct);
```

### First / FirstOrDefault / Single
```csharp
var product = await _db.Products
    .FirstOrDefaultAsync(p => p.Id == id, ct);

var activeKeyboard = await _db.Products
    .FirstAsync(p => p.Name == "Keyboard" && p.IsActive, ct);

// Single throws if 0 or >1 rows match
var bySku = await _db.Products.SingleAsync(p => p.Id == id, ct);
```

| Method | 0 rows | >1 rows |
|--------|--------|---------|
| `First` | throws | returns first |
| `FirstOrDefault` | `null`/default | returns first |
| `Single` | throws | throws |
| `SingleOrDefault` | default | throws |

### List queries
```csharp
var items = await _db.Products
    .Where(p => p.IsActive)
    .ToListAsync(ct);
```

---

## 4. Update

### Pattern A — load tracked entity, mutate, save
```csharp
var product = await _db.Products.FirstOrDefaultAsync(p => p.Id == id, ct);
if (product is null) return null;

product.Name = newName;
product.Price = newPrice;
await _db.SaveChangesAsync(ct);
```
EF tracks the entity, detects property changes, generates `UPDATE`.

### Pattern B — attach/update (know when you use it)
```csharp
var product = new Product { Id = id, Name = newName, Price = newPrice, CategoryId = categoryId };
_db.Products.Update(product); // marks all properties modified
await _db.SaveChangesAsync(ct);
```
`Update` can overwrite fields you didn’t intend if the object is incomplete. Prefer load+mutate for beginners.

### Mark only some properties (advanced awareness)
```csharp
_db.Entry(product).Property(p => p.Price).IsModified = true;
```

---

## 5. Delete (Remove)

```csharp
var product = await _db.Products.FindAsync(new object[] { id }, ct);
if (product is null) return false;

_db.Products.Remove(product);
await _db.SaveChangesAsync(ct);
return true;
```

### Soft delete alternative (business apps)
```csharp
product.IsActive = false; // or IsDeleted = true
await _db.SaveChangesAsync(ct);
```
Often better than hard delete for audits and recovery.

### RemoveRange
```csharp
_db.Products.RemoveRange(orphans);
await _db.SaveChangesAsync(ct);
```

---

## 6. Filtering, Sorting, Projection

### Filter + sort
```csharp
var items = await _db.Products
    .Where(p => p.IsActive && p.Price >= minPrice)
    .OrderBy(p => p.Name)
    .ThenByDescending(p => p.Price)
    .ToListAsync(ct);
```

### Compose dynamically
```csharp
IQueryable<Product> query = _db.Products.AsQueryable();

if (!string.IsNullOrWhiteSpace(search))
    query = query.Where(p => p.Name.Contains(search));

if (categoryId is not null)
    query = query.Where(p => p.CategoryId == categoryId);

query = query.OrderBy(p => p.Name);
```

`IQueryable<T>` builds an expression tree — SQL executes when you materialize (`ToListAsync`, `FirstAsync`, …).

### Project to DTO (efficient selects)
```csharp
var dtos = await _db.Products
    .Where(p => p.IsActive)
    .Select(p => new ProductResponseDto(p.Id, p.Name, p.Price))
    .ToListAsync(ct);
```
Projection pulls only needed columns and avoids over-fetching navigations.

---

## 7. Pagination with Skip/Take

```csharp
public async Task<(List<ProductResponseDto> Items, int Total)> GetPageAsync(
    int page,
    int pageSize,
    CancellationToken ct)
{
    if (page < 1) page = 1;
    if (pageSize < 1) pageSize = 20;

    var query = _db.Products.AsNoTracking().Where(p => p.IsActive);

    var total = await query.CountAsync(ct);

    var items = await query
        .OrderBy(p => p.Id) // stable ordering is required for paging
        .Skip((page - 1) * pageSize)
        .Take(pageSize)
        .Select(p => new ProductResponseDto(p.Id, p.Name, p.Price))
        .ToListAsync(ct);

    return (items, total);
}
```

```
Page 1: Skip(0).Take(20)
Page 2: Skip(20).Take(20)
Page 3: Skip(40).Take(20)
```

Always **OrderBy** before Skip/Take for deterministic pages.

---

## 8. Tracking vs AsNoTracking

### Tracking (default for entities returned from DbSet)
EF Core snapshots values and watches changes → great for updates.

### No-tracking
```csharp
var products = await _db.Products
    .AsNoTracking()
    .Where(p => p.IsActive)
    .ToListAsync(ct);
```

| Use tracking when | Use `AsNoTracking` when |
|-------------------|-------------------------|
| You will update/delete entity | Read-only queries / lists |
| Need change detection | API GET endpoints |
| Working graph stays attached | Max read performance / less memory |

```
GET lists/details   → AsNoTracking (+ Select DTO)
POST/PUT flows      → track entity, SaveChanges
```

---

## 9. Loading Related Data

### Eager loading — `Include` / `ThenInclude`
```csharp
var product = await _db.Products
    .AsNoTracking()
    .Include(p => p.Category)
    .Include(p => p.Tags)
    .FirstOrDefaultAsync(p => p.Id == id, ct);
```

Nested:
```csharp
var order = await _db.Orders
    .Include(o => o.Items)
        .ThenInclude(i => i.Product)
    .FirstOrDefaultAsync(o => o.Id == orderId, ct);
```

```
One query (conceptually) brings parent + related rows
(SQL may be joins or split queries depending on config)
```

### Explicit loading
```csharp
var product = await _db.Products.FirstAsync(p => p.Id == id, ct);
await _db.Entry(product).Reference(p => p.Category).LoadAsync(ct);
await _db.Entry(product).Collection(p => p.Tags).LoadAsync(ct);
```

### Lazy loading
Related data loads automatically when navigation is accessed — **requires** proxies + special setup.

| Strategy | Pros | Cons |
|----------|------|------|
| Eager `Include` | Explicit, predictable | Over-include can pull too much |
| Explicit `Load` | Controlled secondary queries | More code |
| Lazy | Convenient | Hidden N+1 queries; surprises |

**Beginner/default recommendation:** eager or projection; avoid lazy until you know N+1 well.

### N+1 warning preview
```csharp
// ❌ classic N+1 if Category lazy-loads per row
var products = await _db.Products.ToListAsync();
foreach (var p in products)
{
    Console.WriteLine(p.Category?.Name); // may query per product
}
```
Prefer:
```csharp
var products = await _db.Products.Include(p => p.Category).AsNoTracking().ToListAsync();
```
or project `p.Category.Name` in `Select`.

### Split queries (awareness)
```csharp
.AsSplitQuery()
```
Helps some complex multi-include queries avoid huge cartesian joins.

---

## 10. Async APIs and Cancellation

Prefer async EF methods in web apps so threads aren’t blocked on I/O.

```csharp
await _db.Products.ToListAsync(ct);
await _db.Products.CountAsync(ct);
await _db.SaveChangesAsync(ct);
await _db.Products.AnyAsync(p => p.Name == name, ct);
```

Pass `CancellationToken` from ASP.NET actions:
```csharp
[HttpGet]
public async Task<ActionResult<List<ProductResponseDto>>> GetAll(CancellationToken ct)
{
    var items = await _service.GetAllAsync(ct);
    return Ok(items);
}
```

### Materialization reminders
| Keeps query in DB (IQueryable) | Executes now |
|--------------------------------|--------------|
| `Where`, `OrderBy`, `Select`, `Skip`, `Take` | `ToListAsync`, `FirstAsync`, `CountAsync`, `AnyAsync` |

Don’t call `ToList()` too early, then filter in memory by accident.

---

## 11. Knowledge Check

**Q1.** When does EF Core send INSERT/UPDATE/DELETE to the database?  
**Q2.** Difference between `FirstOrDefaultAsync` and `SingleOrDefaultAsync`?  
**Q3.** Why is load-then-mutate safer than `Update(incompleteEntity)` for beginners?  
**Q4.** Why must paging queries include a stable `OrderBy`?  
**Q5.** When should you use `AsNoTracking()`?  
**Q6.** What does `Include` do?  
**Q7.** What is an N+1 query problem in one sentence?

### Mini practice
Implement `ProductService` methods:
1. Create product  
2. Get by id with category (`Include`) as DTO  
3. Search with filter + sort + page (`Skip/Take`) using `AsNoTracking`  
4. Update price  
5. Soft-delete (`IsActive = false`)  
Log or inspect SQL (EF logging) for the list query.

### Answers (short)
1. On `SaveChanges` / `SaveChangesAsync`  
2. Single* throws if multiple matches; First* returns the first  
3. `Update` marks all properties modified; may null/overwrite unintentionally  
4. Without order, page contents are undefined  
5. Read-only queries  
6. Eager-loads related data in the query  
7. 1 query for parents + N queries for each parent’s children  

---

## ✅ What You Should Feel Confident About

- [ ] Perform Add / query / update / remove + `SaveChangesAsync`  
- [ ] Write filtered, sorted, projected LINQ queries  
- [ ] Paginate with `Skip`/`Take` safely  
- [ ] Choose tracking vs `AsNoTracking`  
- [ ] Eager-load with `Include` / `ThenInclude`  
- [ ] Avoid early materialization and basic N+1 patterns  

**Previous:** [02-code-first-approach-and-migrations.md](./02-code-first-approach-and-migrations.md)  
**Next:** [04-repository-and-unit-of-work.md](./04-repository-and-unit-of-work.md) — repository & unit of work patterns on top of EF Core.
