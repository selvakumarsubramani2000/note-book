# 🧱 Code-First & Migrations — Model in C#, Evolve the Database

> **Trainer's Note:** In Code-First, **your C# entities are the source of truth**. Migrations turn model changes into versioned SQL steps so every environment upgrades safely. Learn relationships and migrations carefully — this is how real teams ship schema changes.

---

## 📑 Table of Contents
1. [Code-First vs Other Approaches](#1-code-first-vs-other-approaches)
2. [Designing Entity Classes](#2-designing-entity-classes)
3. [Keys: Primary and Foreign](#3-keys-primary-and-foreign)
4. [Relationships Overview](#4-relationships-overview)
5. [DataAnnotations vs Fluent API](#5-dataannotations-vs-fluent-api)
6. [One-to-Many Configuration](#6-one-to-many-configuration)
7. [Many-to-Many Configuration](#7-many-to-many-configuration)
8. [Migrations Workflow](#8-migrations-workflow)
9. [Reading Generated Migration Files](#9-reading-generated-migration-files)
10. [Data Seeding](#10-data-seeding)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. Code-First vs Other Approaches

| Approach | Source of truth | Typical flow |
|----------|-----------------|--------------|
| **Code-First** | C# model | Change entities → add migration → update database |
| Database-First | Existing DB | Scaffold entities from DB |
| Model-First (classic) | Visual model | Less common in modern EF Core apps |

```
Code-First loop:

  Edit entity/DbContext
        │
        ▼
  dotnet ef migrations add <Name>
        │
        ▼
  Migration class (Up/Down) generated
        │
        ▼
  dotnet ef database update
        │
        ▼
  Database schema matches model
```

This module focuses on **Code-First**.

---

## 2. Designing Entity Classes

```csharp
public class Category
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;

    // Navigation: one category has many products
    public List<Product> Products { get; set; } = new();
}

public class Product
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }

    // FK + navigation
    public int CategoryId { get; set; }
    public Category? Category { get; set; }
}
```

### Practical design tips
1. Use clear names (`Product`, not `Tbl_Product_Master`)  
2. Prefer `Id` for PK unless team standard says otherwise  
3. Include FK scalar (`CategoryId`) **and** navigation (`Category`) when useful  
4. Initialize collection navigations  
5. Avoid leaking UI-only fields into entities  

---

## 3. Keys: Primary and Foreign

### Primary key (PK)
Uniquely identifies a row.

```csharp
public int Id { get; set; } // convention PK
```

Fluent:
```csharp
entity.HasKey(x => x.Id);
```

Composite keys (when needed):
```csharp
entity.HasKey(x => new { x.OrderId, x.ProductId });
```

### Foreign key (FK)
Points to another table’s PK.

```csharp
public int CategoryId { get; set; } // FK scalar
public Category? Category { get; set; } // navigation
```

```
Categories             Products
----------             --------
Id (PK)  <──────────   CategoryId (FK)
Name                   Id (PK)
                       Name
```

---

## 4. Relationships Overview

| Relationship | Meaning | Example |
|--------------|---------|---------|
| **One-to-Many** | Parent has many children | Category → Products |
| **One-to-One** | Each side one related row | User → UserProfile |
| **Many-to-Many** | Both sides many | Product ↔ Tag |

```
One-to-Many:
  Category 1 ──── * Product

Many-to-Many:
  Product * ──── * Tag
         (join table)
```

Required vs optional:
- Required child FK → child must have parent  
- Optional FK (nullable) → child may stand alone  

---

## 5. DataAnnotations vs Fluent API

### DataAnnotations (attributes on entity)
```csharp
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

public class Product
{
    public int Id { get; set; }

    [Required, MaxLength(200)]
    public string Name { get; set; } = string.Empty;

    [Column(TypeName = "decimal(18,2)")]
    public decimal Price { get; set; }

    [ForeignKey(nameof(Category))]
    public int CategoryId { get; set; }

    public Category? Category { get; set; }
}
```

### Fluent API (`OnModelCreating`)
```csharp
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    modelBuilder.Entity<Product>(b =>
    {
        b.ToTable("Products");
        b.HasKey(x => x.Id);
        b.Property(x => x.Name).IsRequired().HasMaxLength(200);
        b.Property(x => x.Price).HasPrecision(18, 2);

        b.HasOne(x => x.Category)
         .WithMany(x => x.Products)
         .HasForeignKey(x => x.CategoryId)
         .OnDelete(DeleteBehavior.Restrict);
    });
}
```

### Comparison
| | DataAnnotations | Fluent API |
|--|-----------------|------------|
| Location | On entity class | Central in `DbContext` |
| Readability for simple rules | Good | Good |
| Complex relationships | Limited | **Best** |
| Keeps domain pure | Can clutter domain | Better separation |
| Team preference | Quick prototypes | Most production models |

**Recommendation:** Fluent API for relationships/precision; light annotations optional. Many teams use Fluent exclusively.

You can also split Fluent config into `IEntityTypeConfiguration<T>` classes:
```csharp
public class ProductConfiguration : IEntityTypeConfiguration<Product>
{
    public void Configure(EntityTypeBuilder<Product> b) { /* ... */ }
}

// OnModelCreating
modelBuilder.ApplyConfigurationsFromAssembly(typeof(ShopDbContext).Assembly);
```

---

## 6. One-to-Many Configuration

```csharp
modelBuilder.Entity<Product>(b =>
{
    b.HasOne(p => p.Category)          // Product has one Category
     .WithMany(c => c.Products)        // Category has many Products
     .HasForeignKey(p => p.CategoryId)
     .OnDelete(DeleteBehavior.Restrict);
});
```

### Delete behaviors (know these)
| Behavior | Effect when parent deleted |
|----------|----------------------------|
| `Cascade` | Children deleted too |
| `Restrict` / `NoAction` | Block delete if children exist |
| `SetNull` | Child FK set null (needs nullable FK) |
| `ClientCascade` etc. | Client-side variants (advanced) |

Beginner-safe default for many business apps: **Restrict** unless you truly want cascade.

---

## 7. Many-to-Many Configuration

### EF Core modern skip navigations
```csharp
public class Product
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public List<Tag> Tags { get; set; } = new();
}

public class Tag
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public List<Product> Products { get; set; } = new();
}

// Fluent (optional explicit control)
modelBuilder.Entity<Product>()
    .HasMany(p => p.Tags)
    .WithMany(t => t.Products)
    .UsingEntity(j => j.ToTable("ProductTags"));
```

### Explicit join entity (when join has extra fields)
```csharp
public class ProductTag
{
    public int ProductId { get; set; }
    public Product Product { get; set; } = null!;
    public int TagId { get; set; }
    public Tag Tag { get; set; } = null!;
    public DateTime LinkedAtUtc { get; set; }
}
```
Configure two one-to-many relations to the join entity.

---

## 8. Migrations Workflow

### Prerequisites
- `dotnet-ef` tool installed  
- `Microsoft.EntityFrameworkCore.Design` package referenced  
- Startup project can build and resolve DI/DbContext  

### Add a migration
```bash
dotnet ef migrations add InitialCreate ^
  --project src/Shop.Infrastructure ^
  --startup-project src/Shop.Api
```

(PowerShell line continuation is `` ` ``; bash uses `\`.)

### Apply migrations to database
```bash
dotnet ef database update ^
  --project src/Shop.Infrastructure ^
  --startup-project src/Shop.Api
```

### Common commands
| Command | Purpose |
|---------|---------|
| `dotnet ef migrations add <Name>` | Snapshot model change as migration |
| `dotnet ef database update` | Apply pending migrations |
| `dotnet ef database update <Migration>` | Upgrade/downgrade to specific migration |
| `dotnet ef migrations list` | Show migrations |
| `dotnet ef migrations remove` | Remove last *unapplied* migration (careful) |
| `dotnet ef dbcontext script` | Generate SQL script |
| `dotnet ef migrations script` | Script from/to migrations (deployment friendly) |

### Naming tips
```
InitialCreate
AddProductIsActive
AddOrdersTable
IncreaseProductNameLength
```
Names should describe intent — future you will thank present you.

### Development loop
```
1. Change entity/config
2. migrations add
3. Review generated code
4. database update
5. Test API
```

Never invent manual schema drift on shared environments without a migration trail.

---

## 9. Reading Generated Migration Files

A migration class roughly looks like:

```csharp
public partial class InitialCreate : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.CreateTable(
            name: "Categories",
            columns: table => new
            {
                Id = table.Column<int>(nullable: false)
                    .Annotation("SqlServer:Identity", "1, 1"),
                Name = table.Column<string>(maxLength: 100, nullable: false)
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_Categories", x => x.Id);
            });

        // more tables, indexes, FKs...
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropTable(name: "Categories");
    }
}
```

| Part | Meaning |
|------|---------|
| `Up` | Apply forward change |
| `Down` | Reverse change (best effort) |
| Model snapshot | EF’s latest full model picture (`*DbContextModelSnapshot.cs`) |

### Review checklist before update
1. Unexpected column drops?  
2. Cascade deletes you didn’t intend?  
3. Precision/length wrong?  
4. Indexes missing for frequent filters?  
5. Data loss risk on type changes?  

For production, prefer generating **SQL scripts** and reviewing in CI/CD rather than blind `database update` on live systems.

```bash
dotnet ef migrations script FromMigration ToMigration -o migrate.sql
```

---

## 10. Data Seeding

### Model seed (via Fluent)
```csharp
modelBuilder.Entity<Category>().HasData(
    new Category { Id = 1, Name = "Electronics" },
    new Category { Id = 2, Name = "Books" });

modelBuilder.Entity<Product>().HasData(
    new Product { Id = 1, Name = "Keyboard", Price = 1499m, CategoryId = 1 });
```
Seed data becomes part of migrations — good for static reference data.

### Runtime seed (on startup) — flexible
```csharp
public static async Task SeedAsync(ShopDbContext db)
{
    if (await db.Categories.AnyAsync()) return;

    db.Categories.AddRange(
        new Category { Name = "Electronics" },
        new Category { Name = "Books" });

    await db.SaveChangesAsync();
}

// Program.cs (Development only is safest for demos)
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<ShopDbContext>();
    await db.Database.MigrateAsync(); // apply migrations
    if (app.Environment.IsDevelopment())
        await SeedAsync(db);
}
```

| Seed style | Best for |
|------------|----------|
| `HasData` | Stable lookup values versioned with schema |
| Startup/runtime seed | Demo data, env-specific samples |
| External scripts | Large reference imports |

Don’t seed huge production datasets in `HasData` migrations carelessly.

---

## 11. Knowledge Check

**Q1.** In Code-First, what is the source of truth — SQL tables or C# model?  
**Q2.** What is the difference between a PK and an FK?  
**Q3.** Configure one-to-many in plain words: `HasOne` / `WithMany` / `HasForeignKey`.  
**Q4.** When do you prefer Fluent API over DataAnnotations?  
**Q5.** What do `migrations add` and `database update` each do?  
**Q6.** Why inspect `Up`/`Down` before applying?  
**Q7.** Name one safe way to provide starter categories for local development.

### Mini practice
1. Create `Category` and `Product` with one-to-many  
2. Configure via Fluent API + delete behavior Restrict  
3. Add many-to-many `Tag`  
4. `migrations add InitialCreate` and read the file  
5. `database update`  
6. Seed two categories and three products  

### Answers (short)
1. C# model  
2. PK uniquely IDs a row; FK references another table’s PK  
3. Child has one parent; parent has many children; child holds FK  
4. Complex relations, precision, centralized config, cleaner domain  
5. Create migration code / apply migrations to DB  
6. Catch destructive or unintended schema SQL early  
7. Runtime Development seed or careful `HasData`  

---

## ✅ What You Should Feel Confident About

- [ ] Explain Code-First workflow  
- [ ] Model entities with PKs, FKs, navigations  
- [ ] Configure one-to-many and many-to-many  
- [ ] Choose Fluent API for serious relationship config  
- [ ] Add and apply migrations with `dotnet ef`  
- [ ] Read migration `Up`/`Down` at a basic level  
- [ ] Seed reference/demo data responsibly  

**Previous:** [01-ef-core-setup.md](./01-ef-core-setup.md)  
**Next:** [03-querying-and-persistence.md](./03-querying-and-persistence.md) — CRUD, LINQ, tracking, and loading strategies.
