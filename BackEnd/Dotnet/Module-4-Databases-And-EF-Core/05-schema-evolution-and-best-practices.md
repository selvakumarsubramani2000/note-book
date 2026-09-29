# 🛡️ Schema Evolution & EF Core Best Practices — Ship Data Changes Safely

> **Trainer's Note:** The hard part is not `database update` on your laptop. The hard part is **changing a live database** without breaking APIs, losing data, or melting performance. This file covers production schema evolution, zero-downtime friendly habits, and EF performance pitfalls (including N+1).

---

## 📑 Table of Contents
1. [Schema Evolution in Production](#1-schema-evolution-in-production)
2. [Migration Strategies for Teams](#2-migration-strategies-for-teams)
3. [Breaking Changes and Expand/Contract](#3-breaking-changes-and-expandcontract)
4. [Data Migrations vs Schema Migrations](#4-data-migrations-vs-schema-migrations)
5. [Deployment Checklist](#5-deployment-checklist)
6. [EF Core Performance Best Practices](#6-ef-core-performance-best-practices)
7. [Connection Pooling and DbContext Lifetimes](#7-connection-pooling-and-dbcontext-lifetimes)
8. [Killing the N+1 Problem](#8-killing-the-n1-problem)
9. [Common Pitfalls Checklist](#9-common-pitfalls-checklist)
10. [Production Observability for Data Access](#10-production-observability-for-data-access)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. Schema Evolution in Production

Applications change. Tables must change with them — **with history**.

```
v1: Products(Id, Name, Price)
v2: Products(Id, Name, Price, IsActive)
v3: Products(Id, Name, Price, IsActive, CategoryId) + Categories
```

| Environment | How schema moves |
|-------------|------------------|
| Local dev | `dotnet ef database update` is fine |
| CI | Build + migrate against test DB |
| Production | Reviewed script / controlled migrator job |

**Rule:** Every production schema change is a reviewed migration artifact — never “hot-edit” live tables as the only record.

---

## 2. Migration Strategies for Teams

### Option A — apply migrations at startup (simple apps)
```csharp
await db.Database.MigrateAsync();
```
Pros: simple.  
Cons: multi-instance race risks, slower startup, weaker change control.

### Option B — generate SQL scripts (recommended for serious prod)
```bash
dotnet ef migrations script PreviousMigration LatestMigration -o artifacts/migrate.sql
```
DBA/CI applies script with backup + approval.

### Option C — dedicated migration step in pipeline
```
build → test → migrate job → deploy new API
```
or expand/contract multi-phase deploy (below).

### Team rules of thumb
1. One migration per logical change when practical  
2. Never edit old migrations already applied to shared environments  
3. If you must fix: add a **new** migration  
4. Keep migration names descriptive  
5. Prefer forward-fixed history over rewriting shared history  

---

## 3. Breaking Changes and Expand/Contract

A **breaking schema change** can crash old app instances still running during deploy.

### Expand / Contract pattern
```
1) EXPAND: add new column/table (nullable or with default) — old app still works
2) DEPLOY app that writes both old+new (or dual-read)
3) BACKFILL data
4) DEPLOY app that reads new only
5) CONTRACT: remove old column in a later migration
```

### Examples
| Risky direct change | Safer multi-step |
|---------------------|------------------|
| Rename column immediately | Add new column → dual-write → backfill → switch reads → drop old |
| Make column non-nullable instantly | Add nullable → backfill → set non-nullable |
| Drop column still read by old API | Remove code usage first (or dual version) → drop later |
| Destructive type change | Add new column, convert, switch |

```
Bad single bang:
  Drop Column MiddleName   + deploy new API at same second
  (old nodes may still SELECT MiddleName)

Better:
  deploy code that stops using MiddleName
  then migrate drop column
```

### Compatibility mindset
During rolling deploys, **old and new API binaries may both run**. Schema must tolerate both for a while when possible.

---

## 4. Data Migrations vs Schema Migrations

| Type | Example |
|------|---------|
| **Schema migration** | Add column `IsActive bit not null default 1` |
| **Data migration** | Set `IsActive = 0` where `LastSale < 2020` |

### Where to put data moves
1. EF migration `migrationBuilder.Sql("UPDATE ...")` for small controlled backfills  
2. Separate one-off console/worker job for large backfills  
3. Idempotent scripts you can re-run safely  

```csharp
protected override void Up(MigrationBuilder migrationBuilder)
{
    migrationBuilder.AddColumn<bool>(
        name: "IsActive",
        table: "Products",
        nullable: false,
        defaultValue: true);

    migrationBuilder.Sql(
        "UPDATE Products SET IsActive = 0 WHERE Name LIKE '%DEPRECATED%'");
}
```

Large table rewrites may lock production — batch updates (`TOP (1000)` loops / `LIMIT` batches) during maintenance windows.

---

## 5. Deployment Checklist

Before production schema change:

- [ ] Backup / snapshot strategy confirmed  
- [ ] Migration reviewed (Up SQL understood)  
- [ ] Expand/contract needed?  
- [ ] Indexes considered for new filters  
- [ ] Defaults/nullability safe for existing rows  
- [ ] Rollback story (Down or forward-fix migration)  
- [ ] App version compatibility during rolling deploy  
- [ ] Run on staging with production-like data volume  
- [ ] Measure migration duration  

```
prefer forward fix over scary Down on prod:
  bad migration applied → add corrective migration
```

---

## 6. EF Core Performance Best Practices

### 1) Filter in the database
```csharp
// ✅
await _db.Products.Where(p => p.IsActive).ToListAsync();

// ❌ load all then filter in memory
var all = await _db.Products.ToListAsync();
var active = all.Where(p => p.IsActive).ToList();
```

### 2) Project what you need
```csharp
await _db.Products
    .Where(p => p.IsActive)
    .Select(p => new ProductResponseDto(p.Id, p.Name, p.Price))
    .ToListAsync();
```

### 3) AsNoTracking for reads
```csharp
_db.Products.AsNoTracking()...
```

### 4) Don’t over-Include
Include only navigations you will use. Prefer `Select` for API shapes.

### 5) Index hot filters
```csharp
// Fluent
b.HasIndex(x => x.Name);
b.HasIndex(x => new { x.CategoryId, x.IsActive });
```

### 6) Batch SaveChanges
Don’t call `SaveChangesAsync` inside a per-row loop when one save can work.

### 7) Avoid client evaluation surprises
If EF cannot translate LINQ to SQL, it may throw (modern versions) or pull data client-side depending on context — keep query logic SQL-translatable.

### 8) Pagination always ordered
`OrderBy` + `Skip` + `Take`.

### 9) Compiled queries / raw SQL (later tools)
For hot paths, advanced features exist. Measure first.

### 10) Use correct collection APIs
`AnyAsync` instead of `CountAsync() > 0` when you only need existence.

---

## 7. Connection Pooling and DbContext Lifetimes

### DbContext lifetime
- Default `AddDbContext` → **scoped**  
- **Do not** register DbContext as singleton  
- **Do not** share one context across threads  

```
Request A → Context A
Request B → Context B
```

### Connection pooling
ADO.NET providers pool physical connections. Opening/closing logically is cheap compared to true TCP setup.

EF opens connections as needed; disposing scoped context returns connections to the pool.

### When to use `AddDbContextPool`
```csharp
builder.Services.AddDbContextPool<ShopDbContext>(opt =>
    opt.UseSqlServer(cs));
```
Pools context instances for reduced overhead in high-throughput apps. Learn after basics work. Still not a cross-request sticky unit of work.

### Long-running work
For background jobs, create a **scope**:
```csharp
await using var scope = _scopeFactory.CreateAsyncScope();
var db = scope.ServiceProvider.GetRequiredService<ShopDbContext>();
```
Don’t capture a request-scoped context in a hosted service singleton.

---

## 8. Killing the N+1 Problem

### What N+1 looks like
```
1 query:  SELECT * FROM Products
N queries: SELECT * FROM Categories WHERE Id = @p0  (per product)
```

### Typical causes
- Lazy loading navigations in loops  
- Calling a repository `GetCategory(id)` inside `foreach`  
- Serial awaits in loops without bulk loading  

### Fixes
#### Eager load
```csharp
var products = await _db.Products
    .Include(p => p.Category)
    .AsNoTracking()
    .ToListAsync();
```

#### Projection
```csharp
var rows = await _db.Products
    .AsNoTracking()
    .Select(p => new
    {
        p.Id,
        p.Name,
        CategoryName = p.Category!.Name
    })
    .ToListAsync();
```

#### Explicit bulk load then join in memory ( occasional)
```csharp
var products = await _db.Products.AsNoTracking().ToListAsync();
var categoryIds = products.Select(p => p.CategoryId).Distinct().ToList();
var categories = await _db.Categories.Where(c => categoryIds.Contains(c.Id))
    .AsNoTracking().ToListAsync();
```

### Detection
- EF Core logging / `LogTo`  
- SQL Profiler / pg_stat / Application Insights dependencies  
- “Why is this endpoint making 120 SQL calls?”  

```csharp
options.LogTo(Console.WriteLine, LogLevel.Information)
       .EnableSensitiveDataLogging(); // DEV only
```

---

## 9. Common Pitfalls Checklist

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Context as singleton | Random crashes / threading bugs | Scoped context |
| SaveChanges per loop | Slow writes | Batch changes |
| Missing `OrderBy` on page | Random pages | Stable sort |
| Giant Includes | Slow reads / huge payloads | Project DTOs |
| N+1 lazy loads | Latency spikes | Include/Select |
| Tracking huge read lists | High memory | `AsNoTracking` |
| Editing applied migrations | Drift between envs | Add new migration |
| Cascade delete surprises | Data gone | Choose `DeleteBehavior` intentionally |
| String-concat filters | Injection / bad SQL habits | LINQ parameters / parameterized raw SQL |
| Blocking `.Result` on async | Thread pool starvation | `await` all the way |

### Raw SQL safety
```csharp
// parameterized ✅
await _db.Products
    .FromSqlInterpolated($"SELECT * FROM Products WHERE Name = {name}")
    .ToListAsync();
```
Never stitch raw user input into SQL strings.

---

## 10. Production Observability for Data Access

| Signal | Why it matters |
|--------|----------------|
| EF/SQL duration metrics | Catch slow queries early |
| Failure rates (timeouts/deadlocks) | Capacity and indexing issues |
| Migration version applied | Know which schema is live |
| Correlation id on requests | Trace API → SQL |

### Practical habits
1. Log slow query threshold in non-prod  
2. Add indexes from real query patterns  
3. Review migration scripts like production code  
4. Keep seed data out of production migrate path unless intentional  
5. Load-test list endpoints with realistic volumes  

---

## 11. Knowledge Check

**Q1.** Why is editing an already-applied migration dangerous on a team?  
**Q2.** Explain expand/contract in one short paragraph.  
**Q3.** Schema migration vs data migration — example of each.  
**Q4.** Why is scoped `DbContext` preferred for Web APIs?  
**Q5.** Name three EF performance best practices.  
**Q6.** How do you identify an N+1 problem?  
**Q7.** What is safer for production deploys — silent startup migrate on 20 nodes, or a reviewed SQL migration step?  

### Mini practice
1. Add a non-nullable `Sku` column to `Product` using expand/contract thinking (nullable first + backfill + tighten)  
2. Write a list endpoint that projects DTOs with category name (no N+1)  
3. Enable EF SQL logging in Development and verify **one** list query  
4. Create a migration script file for the change instead of only `database update`  
5. Find one query in your code that can use `AsNoTracking`  

### Answers (short)
1. Environments diverge; history becomes lying about schema  
2. Add compatible new structure first, dual-run/backfill, switch, remove old later  
3. Add column vs UPDATE existing rows to populate values  
4. One unit-of-work per request; avoids thread-safety issues  
5. Filter in DB, project, no-tracking reads, indexes, batch saves, avoid N+1…  
6. One parent query + per-row child queries in logs/profiler  
7. Reviewed dedicated migration step/script  

---

## ✅ What You Should Feel Confident About

- [ ] Evolve schema with migrations in a team-safe way  
- [ ] Apply expand/contract thinking for breaking changes  
- [ ] Separate schema vs data backfill concerns  
- [ ] Use scoped contexts and understand pooling at a basic level  
- [ ] Write queries that avoid N+1 and over-fetching  
- [ ] Review EF performance pitfalls before production  

**Previous:** [04-repository-and-unit-of-work.md](./04-repository-and-unit-of-work.md)

---

## 🚀 Module 4 Wrap-Up

You can now connect ASP.NET Core to a real relational database with EF Core:

| Skill | File |
|-------|------|
| Packages, DbContext, DI, connection strings | 01 |
| Code-First entities, relationships, migrations, seed | 02 |
| CRUD, LINQ, paging, tracking, Include | 03 |
| Repository + Unit of Work layering | 04 |
| Production schema evolution & performance practices | 05 |

### End-to-end backend slice you can build
```
Controller (DTO in/out)
   → Service (rules)
   → Repository / UoW
   → DbContext + EF Core
   → SQL Server / PostgreSQL
```

### Production-ready data habits checklist
- [ ] Connection strings not in git  
- [ ] Migrations reviewed before prod  
- [ ] Expand/contract for risky changes  
- [ ] Read queries no-tracking + projected  
- [ ] No N+1 on list endpoints  
- [ ] Indexes for hot filters  
- [ ] Scoped DbContext only  

**Suggested next module:** Authentication & Authorization — identity models, JWT bearer auth, policies/roles, securing controllers, and protecting data access by user context.
