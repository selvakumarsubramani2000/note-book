# 🏛️ Repository & Unit of Work — Structure Data Access Cleanly

> **Trainer's Note:** EF Core’s `DbContext` already acts like a unit of work + repository-ish surface. Teams still often add **Repository** and **Unit of Work** layers for testability, boundaries, and consistency. Learn the patterns — and also when a thin abstraction is enough.

---

## 📑 Table of Contents
1. [Why Abstract Data Access?](#1-why-abstract-data-access)
2. [Repository Pattern Basics](#2-repository-pattern-basics)
3. [Generic Repository Interface](#3-generic-repository-interface)
4. [Generic Repository Implementation (EF Core)](#4-generic-repository-implementation-ef-core)
5. [Specific Repositories](#5-specific-repositories)
6. [Unit of Work Pattern](#6-unit-of-work-pattern)
7. [Wiring DI](#7-wiring-di)
8. [Using Repositories from Application Services](#8-using-repositories-from-application-services)
9. [Do You Always Need These Patterns?](#9-do-you-always-need-these-patterns)
10. [Testing Benefits](#10-testing-benefits)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. Why Abstract Data Access?

```
Controller → Service → Repository → DbContext → Database
```

| Goal | How repositories help |
|------|------------------------|
| Keep EF out of controllers | Controllers never see `DbSet` |
| Centralize queries | Product filters live in one place |
| Test application logic | Fake `IProductRepository` in unit tests |
| Swap persistence details | Harder, but boundary is clearer |
| Consistent SaveChanges | Unit of Work coordinates commits |

### Important honesty
`DbContext` already:
- tracks entities
- batches changes
- saves transactionally with `SaveChanges`

Repository/UoW are **organizational patterns**, not magic features EF lacks. Over-abstracting can hurt — balance is a senior skill. This file teaches a clean beginner-to-mid version.

---

## 2. Repository Pattern Basics

A **repository** mediates between domain/application and data mapping layers.

```
IProductRepository
  ├── GetByIdAsync
  ├── ListActiveAsync
  ├── Add
  └── Remove
```

### What belongs in a repository
- Query methods returning entities or projected data  
- Add/remove of aggregates you own  
- Persistence-oriented details (includes, no-tracking reads)  

### What does not belong
- HTTP status codes  
- Complex multi-aggregate business workflows (service/application layer)  
- UI mapping unrelated to persistence  

---

## 3. Generic Repository Interface

```csharp
public interface IRepository<TEntity> where TEntity : class
{
    Task<TEntity?> GetByIdAsync(int id, CancellationToken ct = default);
    Task<IReadOnlyList<TEntity>> ListAsync(CancellationToken ct = default);
    Task AddAsync(TEntity entity, CancellationToken ct = default);
    void Update(TEntity entity);
    void Remove(TEntity entity);
}
```

Generic repos handle common CRUD. Real apps still need **specific** methods for real queries.

---

## 4. Generic Repository Implementation (EF Core)

```csharp
public class Repository<TEntity> : IRepository<TEntity> where TEntity : class
{
    protected readonly ShopDbContext Db;
    protected readonly DbSet<TEntity> Set;

    public Repository(ShopDbContext db)
    {
        Db = db;
        Set = db.Set<TEntity>();
    }

    public virtual async Task<TEntity?> GetByIdAsync(int id, CancellationToken ct = default)
        => await Set.FindAsync(new object[] { id }, ct);

    public virtual async Task<IReadOnlyList<TEntity>> ListAsync(CancellationToken ct = default)
        => await Set.AsNoTracking().ToListAsync(ct);

    public virtual async Task AddAsync(TEntity entity, CancellationToken ct = default)
        => await Set.AddAsync(entity, ct);

    public virtual void Update(TEntity entity) => Set.Update(entity);

    public virtual void Remove(TEntity entity) => Set.Remove(entity);
}
```

Notes:
- `protected` members let specific repositories extend behavior  
- Read methods often use `AsNoTracking`  
- Write paths leave tracking on  

Many generic interfaces also take `Expression<Func<T,bool>>` filters. Start simple; add when repeated.

---

## 5. Specific Repositories

### Interface
```csharp
public interface IProductRepository : IRepository<Product>
{
    Task<Product?> GetByIdWithCategoryAsync(int id, CancellationToken ct = default);
    Task<(IReadOnlyList<Product> Items, int Total)> SearchAsync(
        string? search,
        int? categoryId,
        int page,
        int pageSize,
        CancellationToken ct = default);
    Task<bool> ExistsByNameAsync(string name, CancellationToken ct = default);
}
```

### Implementation
```csharp
public class ProductRepository : Repository<Product>, IProductRepository
{
    public ProductRepository(ShopDbContext db) : base(db) { }

    public async Task<Product?> GetByIdWithCategoryAsync(int id, CancellationToken ct = default)
    {
        return await Set.AsNoTracking()
            .Include(p => p.Category)
            .FirstOrDefaultAsync(p => p.Id == id, ct);
    }

    public async Task<(IReadOnlyList<Product> Items, int Total)> SearchAsync(
        string? search,
        int? categoryId,
        int page,
        int pageSize,
        CancellationToken ct = default)
    {
        IQueryable<Product> query = Set.AsNoTracking().Where(p => p.IsActive);

        if (!string.IsNullOrWhiteSpace(search))
            query = query.Where(p => p.Name.Contains(search));

        if (categoryId is not null)
            query = query.Where(p => p.CategoryId == categoryId);

        var total = await query.CountAsync(ct);

        var items = await query
            .OrderBy(p => p.Name)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync(ct);

        return (items, total);
    }

    public Task<bool> ExistsByNameAsync(string name, CancellationToken ct = default)
        => Set.AnyAsync(p => p.Name == name, ct);
}
```

Specific repositories capture **query intent** with meaningful names — services stay readable.

---

## 6. Unit of Work Pattern

**Unit of Work (UoW)** keeps a business transaction consistent across multiple repositories.

```
Create order:
  - add Order
  - add OrderItems
  - decrease stock on Products
  - Save once
```

### Interface
```csharp
public interface IUnitOfWork : IAsyncDisposable
{
    IProductRepository Products { get; }
    ICategoryRepository Categories { get; }
    // IOrderRepository Orders { get; }

    Task<int> SaveChangesAsync(CancellationToken ct = default);
}
```

### Implementation wrapping one DbContext
```csharp
public class UnitOfWork : IUnitOfWork
{
    private readonly ShopDbContext _db;

    public UnitOfWork(
        ShopDbContext db,
        IProductRepository products,
        ICategoryRepository categories)
    {
        _db = db;
        Products = products;
        Categories = categories;
    }

    public IProductRepository Products { get; }
    public ICategoryRepository Categories { get; }

    public Task<int> SaveChangesAsync(CancellationToken ct = default)
        => _db.SaveChangesAsync(ct);

    public ValueTask DisposeAsync() => _db.DisposeAsync();
}
```

### Why share one `DbContext`?
All repositories in one request must use the **same scoped context** so tracking and single `SaveChanges` work as one unit.

```
HTTP request scope
  └── ShopDbContext (1 instance)
        ├── ProductRepository
        ├── OrderRepository
        └── UnitOfWork.SaveChangesAsync()
```

### Transactions (when SaveChanges isn’t enough alone)
```csharp
await using var tx = await _db.Database.BeginTransactionAsync(ct);
try
{
    // multiple operations
    await _db.SaveChangesAsync(ct);
    await tx.CommitAsync(ct);
}
catch
{
    await tx.RollbackAsync(ct);
    throw;
}
```
EF already wraps a single `SaveChanges` in a transaction; explicit transactions help multi-save or multi-context flows.

---

## 7. Wiring DI

```csharp
public static IServiceCollection AddInfrastructure(this IServiceCollection services, IConfiguration config)
{
    services.AddDbContext<ShopDbContext>(opt =>
        opt.UseSqlServer(config.GetConnectionString("ShopDb")));

    services.AddScoped<IProductRepository, ProductRepository>();
    services.AddScoped<ICategoryRepository, CategoryRepository>();
    services.AddScoped<IUnitOfWork, UnitOfWork>();

    // If generic repo is used directly:
    services.AddScoped(typeof(IRepository<>), typeof(Repository<>));

    return services;
}
```

All **scoped** — aligned with `DbContext`.

---

## 8. Using Repositories from Application Services

```csharp
public class ProductService : IProductService
{
    private readonly IUnitOfWork _uow;

    public ProductService(IUnitOfWork uow)
    {
        _uow = uow;
    }

    public async Task<ProductResponseDto> CreateAsync(CreateProductRequestDto request, CancellationToken ct)
    {
        if (await _uow.Products.ExistsByNameAsync(request.Name, ct))
            throw new InvalidOperationException("Product name already exists");

        var product = new Product
        {
            Name = request.Name,
            Price = request.Price,
            CategoryId = request.CategoryId,
            IsActive = true,
            CreatedAtUtc = DateTime.UtcNow
        };

        await _uow.Products.AddAsync(product, ct);
        await _uow.SaveChangesAsync(ct);

        return new ProductResponseDto(product.Id, product.Name, product.Price);
    }
}
```

### Multi-repository consistency
```csharp
public async Task PlaceOrderAsync(PlaceOrderRequest request, CancellationToken ct)
{
    var product = await _uow.Products.GetByIdAsync(request.ProductId, ct)
        ?? throw new KeyNotFoundException("Product not found");

    // mutate product stock, add order aggregate via _uow.Orders, etc.
    await _uow.Orders.AddAsync(order, ct);
    await _uow.SaveChangesAsync(ct); // both sides commit together
}
```

Controllers still only talk to services — not repositories — in a strict clean layout:
```
Controller → IProductService → IUnitOfWork / IProductRepository → DbContext
```

---

## 9. Do You Always Need These Patterns?

| Approach | When it fits |
|----------|--------------|
| **DbContext directly in services** | Small apps, early prototypes, modular monolith simplicity |
| **Repositories without UoW** | Many teams; call `SaveChanges` on context/service end |
| **Repositories + UoW** | Larger apps, multiple aggregates per use-case, team standard |
| **Specification pattern / query objects** | Advanced query composition needs |

### Pragmatic beginner path
1. Start with services + `DbContext`  
2. Extract repository when queries get noisy/duplicated  
3. Add UoW when multiple repos must commit as one story  
4. Avoid generic-repo-only architecture that hides EF and blocks efficient `Select` projections  

### Leakage warning
If every repository method is `IQueryable` returning outward, you didn’t really abstract EF — and that can be OK if intentional. Be deliberate.

---

## 10. Testing Benefits

```csharp
public class FakeProductRepository : IProductRepository
{
    private readonly List<Product> _items = new();
    // implement members against in-memory list
}

// unit test ProductService with fake repo / fake UoW
```

Application rules can be tested **without** SQL. Still keep a few integration tests against a real DB (or Testcontainers) for EF query correctness.

---

## 11. Knowledge Check

**Q1.** What problem does the repository pattern aim to solve?  
**Q2.** Why create `IProductRepository` instead of only `IRepository<Product>`?  
**Q3.** What is Unit of Work responsible for in your API request?  
**Q4.** Why must repositories share one scoped `DbContext`?  
**Q5.** Where should HTTP 404 decisions live — repository or controller/service boundary?  
**Q6.** Name one risk of overusing generic repositories.  
**Q7.** True/False: `DbContext` already behaves somewhat like a Unit of Work.

### Mini practice
1. Implement `IRepository<T>` + `Repository<T>`  
2. Implement `IProductRepository` + `ProductRepository` with search + exists  
3. Implement `IUnitOfWork`  
4. Register scoped services  
5. Refactor `ProductService` to use UoW  
6. Write one unit test with a fake repository for duplicate-name logic  

### Answers (short)
1. Isolate data access, centralize queries, improve testability/boundaries  
2. Express product-specific queries/intent beyond generic CRUD  
3. Coordinate changes across repositories and commit once  
4. Shared tracking + single transaction/SaveChanges  
5. Controller/service (or application result type) — not low-level repo ideally  
6. Forced lowest-common-denominator APIs; awkward efficient queries  
7. True  

---

## ✅ What You Should Feel Confident About

- [ ] Explain repository and unit of work in plain language  
- [ ] Implement generic + specific EF repositories  
- [ ] Coordinate multi-entity changes with UoW/`SaveChanges`  
- [ ] Register everything scoped with `DbContext`  
- [ ] Keep controllers free of EF types  
- [ ] Judge when *not* to over-abstract  

**Previous:** [03-querying-and-persistence.md](./03-querying-and-persistence.md)  
**Next:** [05-schema-evolution-and-best-practices.md](./05-schema-evolution-and-best-practices.md) — production schema changes, performance, and N+1 defenses.
