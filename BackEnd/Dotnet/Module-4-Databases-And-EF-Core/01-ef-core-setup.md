# 🗄️ EF Core Setup — Connect Your API to a Real Database

> **Trainer's Note:** Controllers and services are only half of a backend. Data must live somewhere durable. **EF Core** (Entity Framework Core) is Microsoft’s modern ORM for .NET — you work with C# classes and LINQ; EF Core translates that to SQL. This file gets packages, `DbContext`, DI, and connection strings right.

---

## 📑 Table of Contents
1. [What Is EF Core?](#1-what-is-ef-core)
2. [Providers and NuGet Packages](#2-providers-and-nuget-packages)
3. [Install Packages](#3-install-packages)
4. [Create Entity Classes (Preview)](#4-create-entity-classes-preview)
5. [Create and Configure DbContext](#5-create-and-configure-dbcontext)
6. [Register DbContext with DI (`AddDbContext`)](#6-register-dbcontext-with-di-adddbcontext)
7. [Connection Strings Securely](#7-connection-strings-securely)
8. [SQL Server vs PostgreSQL Config](#8-sql-server-vs-postgresql-config)
9. [Verify the Wiring](#9-verify-the-wiring)
10. [Project Placement Tips](#10-project-placement-tips)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. What Is EF Core?

**ORM** = Object-Relational Mapper.  
EF Core maps **C# objects** ↔ **database tables**.

```
Your code                          Database
────────                           ────────
Product class          ←maps→      Products table
product.Name = "Pen"   ←maps→      Name column
DbSet<Product>         ←maps→      table access
LINQ Where(...)        ←maps→      SQL SELECT ... WHERE
SaveChanges()          ←maps→      INSERT/UPDATE/DELETE
```

| Without EF Core | With EF Core |
|-----------------|--------------|
| Hand-written SQL everywhere | LINQ + entities |
| Manual reader mapping | Materialized objects |
| Easy to mismatch columns | Strongly typed model |

EF Core is **not** the database. You still need SQL Server, PostgreSQL, SQLite, etc. EF Core is the **bridge**.

---

## 2. Providers and NuGet Packages

Each database needs a **provider** package.

| Database | Common package |
|----------|----------------|
| SQL Server | `Microsoft.EntityFrameworkCore.SqlServer` |
| PostgreSQL | `Npgsql.EntityFrameworkCore.PostgreSQL` |
| SQLite | `Microsoft.EntityFrameworkCore.Sqlite` |
| In-memory (tests only) | `Microsoft.EntityFrameworkCore.InMemory` |

### Tooling package (migrations CLI)
| Package / tool | Purpose |
|----------------|---------|
| `Microsoft.EntityFrameworkCore.Design` | Design-time support for migrations |
| `dotnet-ef` global/local tool | `dotnet ef migrations ...` commands |

```
Shop.Api / Shop.Infrastructure
  ├── EF Core + provider package
  ├── Design package (private assets often)
  └── Your DbContext
```

---

## 3. Install Packages

From the project that will hold `DbContext` (often Infrastructure or the API for beginners):

### SQL Server
```bash
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
dotnet add package Microsoft.EntityFrameworkCore.Design
```

### PostgreSQL
```bash
dotnet add package Npgsql.EntityFrameworkCore.PostgreSQL
dotnet add package Microsoft.EntityFrameworkCore.Design
```

### EF CLI tool (once per machine or as local tool)
```bash
# global tool
dotnet tool install --global dotnet-ef

# verify
dotnet ef --version
```

If the tool already exists, update:
```bash
dotnet tool update --global dotnet-ef
```

### Match major versions
Use EF Core major version aligned with your target framework (example: EF Core 8 with `net8.0`).

---

## 4. Create Entity Classes (Preview)

An **entity** is a class EF Core maps to a table.

```csharp
namespace Shop.Domain.Entities;

public class Product
{
    public int Id { get; set; }                 // Primary key by convention
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public bool IsActive { get; set; } = true;
    public DateTime CreatedAtUtc { get; set; } = DateTime.UtcNow;
}
```

Conventions beginners should know:
| Convention | Effect |
|------------|--------|
| `Id` or `ProductId` | Treated as primary key |
| `string` | becomes nullable/non-nullable text per config |
| Navigation properties | Used for relationships (next file) |

Keep domain entities free of SQL Server–specific junk when possible. Provider configuration lives in `DbContext`/Infrastructure.

---

## 5. Create and Configure DbContext

`DbContext` = your session with the database + the model entry point.

```csharp
using Microsoft.EntityFrameworkCore;
using Shop.Domain.Entities;

namespace Shop.Infrastructure.Persistence;

public class ShopDbContext : DbContext
{
    public ShopDbContext(DbContextOptions<ShopDbContext> options)
        : base(options)
    {
    }

    public DbSet<Product> Products => Set<Product>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity<Product>(entity =>
        {
            entity.ToTable("Products");
            entity.HasKey(x => x.Id);
            entity.Property(x => x.Name)
                .IsRequired()
                .HasMaxLength(200);
            entity.Property(x => x.Price)
                .HasPrecision(18, 2);
        });
    }
}
```

### Anatomy
| Piece | Role |
|-------|------|
| Constructor `DbContextOptions<T>` | Enables DI configuration (connection, provider) |
| `DbSet<T>` | Gateway to query/save that entity type |
| `OnModelCreating` | Fluent configuration (keys, lengths, relations) |

```
HTTP request
   → controller/service
   → ShopDbContext (scoped)
   → provider
   → SQL database
```

---

## 6. Register DbContext with DI (`AddDbContext`)

In `Program.cs` (or Infrastructure extension method):

### SQL Server
```csharp
builder.Services.AddDbContext<ShopDbContext>(options =>
    options.UseSqlServer(
        builder.Configuration.GetConnectionString("ShopDb")));
```

### PostgreSQL
```csharp
builder.Services.AddDbContext<ShopDbContext>(options =>
    options.UseNpgsql(
        builder.Configuration.GetConnectionString("ShopDb")));
```

### What `AddDbContext` does
- Registers `ShopDbContext` as **scoped** (one instance per HTTP request by default)
- Wires `DbContextOptions<ShopDbContext>`
- Plays nicely with ASP.NET Core DI lifetimes

```csharp
// service constructor injection
public class ProductService
{
    private readonly ShopDbContext _db;

    public ProductService(ShopDbContext db)
    {
        _db = db;
    }
}
```

### Optional: extra flags while learning
```csharp
builder.Services.AddDbContext<ShopDbContext>(options =>
{
    options.UseSqlServer(builder.Configuration.GetConnectionString("ShopDb"));
#if DEBUG
    options.EnableSensitiveDataLogging(); // never in production logs
    options.EnableDetailedErrors();
#endif
});
```

---

## 7. Connection Strings Securely

### `appsettings.json` (local shape only)
```json
{
  "ConnectionStrings": {
    "ShopDb": "Server=localhost,1433;Database=ShopDb;User Id=sa;Password=Your_local_password;TrustServerCertificate=True;Encrypt=True"
  }
}
```

PostgreSQL example:
```json
{
  "ConnectionStrings": {
    "ShopDb": "Host=localhost;Port=5432;Database=shopdb;Username=shop;Password=Your_local_password"
  }
}
```

### Read in code
```csharp
var cs = builder.Configuration.GetConnectionString("ShopDb");
// maps to key ConnectionStrings:ShopDb
```

### Security rules
| Do | Don't |
|----|-------|
| Use User Secrets in Development | Commit real production passwords |
| Use env vars / vault in Production | Log full connection strings |
| Different DB per environment | Share prod DB for casual local testing |
| Least-privilege DB users | Use `sa` / superuser in production apps |

### Development user secrets
```bash
dotnet user-secrets init
dotnet user-secrets set "ConnectionStrings:ShopDb" "Server=...;Password=...;"
```

### Production environment variable
```bash
ConnectionStrings__ShopDb=Server=...;Password=...;
```
(`__` is the nested key separator for env vars.)

### `appsettings.Development.json`
Override only non-secret local defaults when possible; keep secrets in user-secrets/env.

---

## 8. SQL Server vs PostgreSQL Config

| Topic | SQL Server | PostgreSQL |
|-------|------------|------------|
| Package | `...SqlServer` | `Npgsql.EntityFrameworkCore.PostgreSQL` |
| Extension | `UseSqlServer(cs)` | `UseNpgsql(cs)` |
| Local default port | 1433 | 5432 |
| Identity columns | Common | Common (serial/identity) |
| Case sensitivity | Usually case-insensitive identifiers | Often case-sensitive depending on quoting |
| Good for | Many Windows/.NET shops, Azure SQL | Linux/cloud-native stacks, open source shops |

### Beginner recommendation
- Learning on Windows corporate stack → **SQL Server** / LocalDB / Docker SQL  
- Learning cross-platform / Linux containers → **PostgreSQL** in Docker is excellent  
- Tiny demos without installing a server → **SQLite** (know its limits)

LocalDB sample (Windows):
```
Server=(localdb)\\mssqllocaldb;Database=ShopDb;Trusted_Connection=True;TrustServerCertificate=True
```

---

## 9. Verify the Wiring

### 1) Build
```bash
dotnet build
```

### 2) Temporary smoke test endpoint (dev only)
```csharp
app.MapGet("/diag/db", async (ShopDbContext db) =>
{
    var canConnect = await db.Database.CanConnectAsync();
    return Results.Ok(new { canConnect });
});
```

### 3) Common failures
| Symptom | Likely cause |
|---------|--------------|
| Cannot resolve `ShopDbContext` | Forgot `AddDbContext` |
| Connection refused | DB not running / wrong host port |
| Login failed | Bad user/password |
| Certificate error | Adjust `TrustServerCertificate` carefully (dev only) |
| Wrong provider method | Used `UseSqlServer` with Postgres connection |

---

## 10. Project Placement Tips

### Beginner single-project
```
Shop.Api
  ├── Entities/
  ├── Persistence/ShopDbContext.cs
  └── Program.cs  (AddDbContext)
```

### Cleaner multi-project (recommended soon)
```
Shop.Domain          → entities (no EF package required ideally)
Shop.Infrastructure  → DbContext, provider packages, repositories
Shop.Api             → Program.cs registers Infrastructure
```

```csharp
// Shop.Api Program.cs
builder.Services.AddInfrastructure(builder.Configuration);

// Infrastructure
public static IServiceCollection AddInfrastructure(
    this IServiceCollection services,
    IConfiguration config)
{
    services.AddDbContext<ShopDbContext>(opt =>
        opt.UseSqlServer(config.GetConnectionString("ShopDb")));
    return services;
}
```

API project still needs a design-time path for EF tools (often `--project` + `--startup-project` flags later).

---

## 11. Knowledge Check

**Q1.** What problem does EF Core solve for backend developers?  
**Q2.** Why do you need a provider package like SqlServer or Npgsql?  
**Q3.** What is `DbContext` in one sentence?  
**Q4.** What lifetime does `AddDbContext` use by default, and why does that fit web apps?  
**Q5.** Which configuration key does `GetConnectionString("ShopDb")` read?  
**Q6.** How should production passwords be supplied?  
**Q7.** Name one difference in registration between SQL Server and PostgreSQL.

### Mini practice
1. Create/use your Module 3 API solution  
2. Add EF Core + one provider package  
3. Create `Product` entity + `ShopDbContext`  
4. Register with `AddDbContext`  
5. Put connection string in config/user-secrets  
6. Hit a `/diag/db` can-connect endpoint  

### Answers (short)
1. Maps objects/LINQ to relational SQL safely and productively  
2. Talks the dialect/protocol of that database  
3. EF session + model entry point for a database  
4. Scoped — one context per HTTP request avoids threading/sharing issues  
5. `ConnectionStrings:ShopDb`  
6. Env vars / secret store / vault — not git  
7. `UseSqlServer` vs `UseNpgsql` (+ different packages/connection string shapes)

---

## ✅ What You Should Feel Confident About

- [ ] Explain EF Core vs the database server itself  
- [ ] Install provider + design packages  
- [ ] Write a basic `DbContext` with `DbSet<>`  
- [ ] Register context via `AddDbContext`  
- [ ] Configure connection strings safely per environment  
- [ ] Smoke-test database connectivity  

**Next:** [02-code-first-approach-and-migrations.md](./02-code-first-approach-and-migrations.md) — entities, relationships, migrations, seeding.
