# 📘 Backend Development & Architecture Guide (.NET + SQL Server)

## Who Is This For?
You're a developer who wants to understand **how backend systems are built** —
how to structure projects, design databases, write APIs, and follow industry
best practices using **.NET** and **SQL Server**.

---

## Table of Contents
1. [What Does a Backend Developer Do?](#1-what-does-a-backend-developer-do)
2. [Architecture Patterns](#2-architecture-patterns)
3. [Clean Architecture - The Industry Standard](#3-clean-architecture---the-industry-standard)
4. [Project Structure - Solution Organization](#4-project-structure---solution-organization)
5. [Database Setup & Design](#5-database-setup--design-sql-server--ef-core)
6. [The Request Pipeline - How ASP.NET Core Works](#6-the-request-pipeline)
7. [API Design - RESTful Best Practices](#7-api-design---restful-best-practices)
8. [Dependency Injection (DI)](#8-dependency-injection-di)
9. [Repository Pattern & Unit of Work](#9-repository-pattern--unit-of-work)
10. [Validation](#10-validation)
11. [Error Handling & Logging](#11-error-handling--logging)
12. [Authentication & Authorization](#12-authentication--authorization)
13. [Configuration Management](#13-configuration-management)
14. [Caching](#14-caching)
15. [Best Practices Checklist](#15-best-practices-checklist)

---

## 1. What Does a Backend Developer Do?

```
Frontend (React/Angular)          Backend (.NET)             Database (SQL Server)
┌──────────────────┐    HTTP     ┌──────────────────┐  SQL   ┌──────────────┐
│                  │  Request   │                  │ Query  │              │
│  User clicks     │──────────▶│  Receives request │──────▶│  Stores data  │
│  "Create Vendor" │           │  Validates data   │       │  Runs queries │
│                  │  JSON     │  Applies rules    │ Data  │  Returns rows │
│  Shows result    │◀──────────│  Returns response │◀──────│              │
│                  │  Response │                  │       │              │
└──────────────────┘           └──────────────────┘       └──────────────┘
```

### Backend Developer Responsibilities:
```
┌─────────────────────────────────────────────────────────────────────┐
│  1. API Development        → Build REST/gRPC endpoints             │
│  2. Database Management    → Design schemas, write queries          │
│  3. Business Logic         → Implement rules (pricing, validation)  │
│  4. Authentication         → Login, JWT tokens, role permissions    │
│  5. Error Handling         → Graceful failures, logging             │
│  6. Performance            → Caching, query optimization            │
│  7. Security               → SQL injection, CORS, HTTPS             │
│  8. Testing                → Unit tests, integration tests          │
│  9. Deployment             → CI/CD, Docker, cloud hosting           │
│  10. Documentation         → API docs (Swagger), README              │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Architecture Patterns

### How Do You Structure a Backend? There Are Several Approaches:

### Pattern 1: Monolith (Simple — Good for Small Apps)
```
┌──────────────────────────────────────────────┐
│           Single .NET Project                │
│                                              │
│  Controllers + Services + Data + Models      │
│  Everything in ONE project                   │
│                                              │
│  ✅ Simple to build and deploy               │
│  ✅ Good for small teams / MVPs              │
│  ❌ Gets messy as app grows                  │
│  ❌ Hard to test individual parts            │
│  ❌ One change can break everything          │
└──────────────────────────────────────────────┘
```

### Pattern 2: N-Tier / Layered Architecture (Traditional)
```
┌────────────────────────────────┐
│  Presentation Layer            │  ← Controllers, API endpoints
│  (VendorDirectory.API)         │
├────────────────────────────────┤
│  Business Logic Layer          │  ← Services, rules, validation
│  (VendorDirectory.Services)    │
├────────────────────────────────┤
│  Data Access Layer             │  ← EF Core, Repositories, SQL
│  (VendorDirectory.Data)        │
├────────────────────────────────┤
│  Database                      │  ← SQL Server
└────────────────────────────────┘

✅ Clear separation of concerns
✅ Each layer has one job
❌ All layers depend downward (tight coupling)
❌ Business logic depends on database technology
```

### Pattern 3: Clean Architecture ⭐ (Recommended)
```
┌─────────────────────────────────────────────────────────────┐
│                    CLEAN ARCHITECTURE                       │
│                                                             │
│         ┌───────────────────────────────┐                  │
│         │      API / Presentation       │  ← Outer layer   │
│         │   (Controllers, Middleware)    │                  │
│         └───────────────┬───────────────┘                  │
│                         │                                   │
│         ┌───────────────▼───────────────┐                  │
│         │      Infrastructure           │  ← Outer layer   │
│         │  (EF Core, SQL, External APIs) │                  │
│         └───────────────┬───────────────┘                  │
│                         │                                   │
│         ┌───────────────▼───────────────┐                  │
│         │      Application              │  ← Middle layer  │
│         │  (Use Cases, Services, DTOs)   │                  │
│         └───────────────┬───────────────┘                  │
│                         │                                   │
│         ┌───────────────▼───────────────┐                  │
│         │      Domain / Core            │  ← Center (CORE) │
│         │  (Entities, Interfaces, Rules) │                  │
│         │  NO dependencies on anything!  │                  │
│         └───────────────────────────────┘                  │
│                                                             │
│  Rule: Dependencies point INWARD only!                      │
│  Core knows NOTHING about database or HTTP                  │
└─────────────────────────────────────────────────────────────┘
```


---

## 3. Clean Architecture - The Industry Standard

### Why Clean Architecture?
```
Problem with traditional layered apps:
  Your business logic (VendorService) DEPENDS on SqlVendorRepository
  Want to switch from SQL Server to MongoDB? Rewrite EVERYTHING!

Clean Architecture solution:
  Business logic depends on INTERFACES (IVendorRepository)
  SQL Server implementation is in a separate project
  Want MongoDB? Just write a NEW implementation. Business logic untouched!
```

### The 4 Layers Explained:

```
Layer 1: DOMAIN (Core) — The heart of your application
  • Entities (Vendor, User, Order)
  • Interfaces (IVendorRepository) — contracts only
  • Domain exceptions, Value objects, Enums
  • ❌ NO EF Core, NO SQL, NO HTTP — pure C# only!

Layer 2: APPLICATION — Business logic / Use cases
  • Services (VendorService) — orchestrate business rules
  • DTOs (Data Transfer Objects) — shape data for API
  • Validators, Mapping profiles
  • References: Domain only

Layer 3: INFRASTRUCTURE — External concerns
  • EF Core DbContext, Repository implementations
  • External API clients (email, payment)
  • Database migrations
  • References: Domain + Application

Layer 4: API (Presentation) — HTTP layer
  • Controllers, Middleware, Program.cs, Swagger
  • References: Application + Infrastructure
```

---

## 4. Project Structure - Solution Organization

### Real .NET Solution Structure (Clean Architecture):

```
VendorDirectory.sln                     ← Solution file
│
├── src/
│   ├── VendorDirectory.Domain/         ← Layer 1: Core entities & interfaces
│   │   ├── Entities/
│   │   │   ├── Vendor.cs
│   │   │   ├── User.cs
│   │   │   └── BaseEntity.cs
│   │   ├── Interfaces/
│   │   │   ├── IVendorRepository.cs
│   │   │   ├── IUserRepository.cs
│   │   │   └── IUnitOfWork.cs
│   │   ├── Enums/
│   │   │   ├── VendorStatus.cs
│   │   │   └── UserRole.cs
│   │   └── Exceptions/
│   │       ├── NotFoundException.cs
│   │       └── ValidationException.cs
│   │
│   ├── VendorDirectory.Application/    ← Layer 2: Business logic
│   │   ├── DTOs/
│   │   │   ├── VendorDto.cs
│   │   │   ├── CreateVendorRequest.cs
│   │   │   └── UpdateVendorRequest.cs
│   │   ├── Services/
│   │   │   ├── IVendorService.cs
│   │   │   └── VendorService.cs
│   │   ├── Validators/
│   │   │   └── CreateVendorValidator.cs
│   │   └── Mappings/
│   │       └── VendorMappingProfile.cs
│   │
│   ├── VendorDirectory.Infrastructure/ ← Layer 3: Data access
│   │   ├── Data/
│   │   │   ├── AppDbContext.cs
│   │   │   └── Configurations/
│   │   │       ├── VendorConfiguration.cs
│   │   │       └── UserConfiguration.cs
│   │   ├── Repositories/
│   │   │   ├── VendorRepository.cs
│   │   │   └── UserRepository.cs
│   │   ├── Migrations/
│   │   │   └── (auto-generated by EF Core)
│   │   └── DependencyInjection.cs
│   │
│   └── VendorDirectory.API/            ← Layer 4: HTTP endpoints
│       ├── Controllers/
│       │   ├── VendorsController.cs
│       │   └── AuthController.cs
│       ├── Middleware/
│       │   └── ExceptionHandlingMiddleware.cs
│       ├── Program.cs
│       ├── appsettings.json
│       └── appsettings.Development.json
│
├── tests/
│   ├── VendorDirectory.UnitTests/
│   │   ├── Services/
│   │   │   └── VendorServiceTests.cs
│   │   └── Validators/
│   │       └── CreateVendorValidatorTests.cs
│   └── VendorDirectory.IntegrationTests/
│       └── Controllers/
│           └── VendorsControllerTests.cs
│
└── README.md
```

### Creating This Solution (Terminal Commands):
```bash
# Create solution
dotnet new sln -n VendorDirectory

# Create projects
dotnet new classlib -n VendorDirectory.Domain -o src/VendorDirectory.Domain
dotnet new classlib -n VendorDirectory.Application -o src/VendorDirectory.Application
dotnet new classlib -n VendorDirectory.Infrastructure -o src/VendorDirectory.Infrastructure
dotnet new webapi -n VendorDirectory.API -o src/VendorDirectory.API

# Add projects to solution
dotnet sln add src/VendorDirectory.Domain
dotnet sln add src/VendorDirectory.Application
dotnet sln add src/VendorDirectory.Infrastructure
dotnet sln add src/VendorDirectory.API

# Set up dependencies (IMPORTANT — direction matters!)
cd src/VendorDirectory.Application
dotnet add reference ../VendorDirectory.Domain          # App → Domain

cd ../VendorDirectory.Infrastructure
dotnet add reference ../VendorDirectory.Domain          # Infra → Domain
dotnet add reference ../VendorDirectory.Application     # Infra → Application

cd ../VendorDirectory.API
dotnet add reference ../VendorDirectory.Application     # API → Application
dotnet add reference ../VendorDirectory.Infrastructure  # API → Infrastructure
```

---

## 5. Database Setup & Design (SQL Server + EF Core)

### Step 1: Domain Entities (Domain Layer)
```csharp
// Domain/Entities/BaseEntity.cs
public abstract class BaseEntity
{
    public int Id { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? UpdatedAt { get; set; }
    public bool IsDeleted { get; set; } = false;
}

// Domain/Entities/Vendor.cs
public class Vendor : BaseEntity
{
    public string VendorName { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public string? Phone { get; set; }
    public string Category { get; set; } = string.Empty;
    public string State { get; set; } = string.Empty;
    public VendorStatus Status { get; set; } = VendorStatus.Active;

    // Navigation property (relationship to User)
    public int? CreatedById { get; set; }
    public User? CreatedBy { get; set; }
}

// Domain/Enums/VendorStatus.cs
public enum VendorStatus
{
    Active = 1,
    Inactive = 2,
    Pending = 3
}
```

### Step 2: EF Core Configuration (Infrastructure Layer)
```csharp
// Infrastructure/Data/AppDbContext.cs
public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    public DbSet<Vendor> Vendors => Set<Vendor>();
    public DbSet<User> Users => Set<User>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Apply all configurations from this assembly
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(AppDbContext).Assembly);

        // Global query filter: exclude soft-deleted records
        modelBuilder.Entity<Vendor>().HasQueryFilter(v => !v.IsDeleted);
    }

    // Auto-set CreatedAt/UpdatedAt on save
    public override Task<int> SaveChangesAsync(CancellationToken ct = default)
    {
        foreach (var entry in ChangeTracker.Entries<BaseEntity>())
        {
            if (entry.State == EntityState.Added)
                entry.Entity.CreatedAt = DateTime.UtcNow;
            if (entry.State == EntityState.Modified)
                entry.Entity.UpdatedAt = DateTime.UtcNow;
        }
        return base.SaveChangesAsync(ct);
    }
}

// Infrastructure/Data/Configurations/VendorConfiguration.cs
public class VendorConfiguration : IEntityTypeConfiguration<Vendor>
{
    public void Configure(EntityTypeBuilder<Vendor> builder)
    {
        builder.ToTable("Vendors");

        builder.HasKey(v => v.Id);
        builder.Property(v => v.VendorName).IsRequired().HasMaxLength(200);
        builder.Property(v => v.Email).IsRequired().HasMaxLength(200);
        builder.Property(v => v.Phone).HasMaxLength(20);
        builder.Property(v => v.Category).IsRequired().HasMaxLength(100);
        builder.Property(v => v.State).IsRequired().HasMaxLength(50);

        // Index for frequently queried columns
        builder.HasIndex(v => v.Email).IsUnique();
        builder.HasIndex(v => v.Status);
        builder.HasIndex(v => v.State);

        // Relationship: Vendor → User (many-to-one)
        builder.HasOne(v => v.CreatedBy)
            .WithMany()
            .HasForeignKey(v => v.CreatedById)
            .OnDelete(DeleteBehavior.SetNull);
    }
}
```

### Step 3: Connection String & Migrations
```json
// appsettings.json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=VendorDirectoryDb;Trusted_Connection=true;TrustServerCertificate=true;"
  }
}
```
```csharp
// Program.cs — Register DbContext
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));
```
```bash
# EF Core Migration Commands
dotnet ef migrations add InitialCreate --project src/VendorDirectory.Infrastructure --startup-project src/VendorDirectory.API
dotnet ef database update --project src/VendorDirectory.Infrastructure --startup-project src/VendorDirectory.API

# Common migration commands:
dotnet ef migrations add AddPhoneToVendor    # New migration
dotnet ef migrations remove                   # Undo last migration
dotnet ef database update                     # Apply to database
dotnet ef migrations script                   # Generate SQL script
```

### Code-First vs Database-First:
```
Code-First (Recommended for new projects):
  Write C# classes → EF Core generates database tables
  You control the schema via C# code + migrations
  ✅ Version controlled, ✅ Automated, ✅ Clean

Database-First (For existing databases):
  Database tables already exist → EF Core generates C# classes
  dotnet ef dbcontext scaffold "ConnectionString" Microsoft.EntityFrameworkCore.SqlServer
  Useful when migrating legacy databases
```

---

## 6. The Request Pipeline

How does an HTTP request travel through your ASP.NET Core app?

```
Client Request: GET /api/vendors/1
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│  1. Kestrel Web Server    → Receives raw HTTP request       │
│  2. Middleware Pipeline   → Each middleware processes request│
│     ├── Exception Handling Middleware  (catches errors)      │
│     ├── HTTPS Redirection Middleware                        │
│     ├── Authentication Middleware     (validates JWT token)  │
│     ├── Authorization Middleware     (checks permissions)    │
│     ├── CORS Middleware              (cross-origin rules)   │
│     └── Routing Middleware           (finds the controller) │
│  3. Controller            → VendorsController.GetById(1)    │
│  4. Service               → VendorService.GetByIdAsync(1)   │
│  5. Repository            → VendorRepository.GetByIdAsync(1)│
│  6. EF Core               → SELECT * FROM Vendors WHERE Id=1│
│  7. SQL Server             → Returns data                   │
│  8. Response flows BACK up through the pipeline             │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
Client Response: 200 OK { "id": 1, "vendorName": "Acme" }
```

### Program.cs - Where You Configure Everything:
```csharp
var builder = WebApplication.CreateBuilder(args);

// ── 1. REGISTER SERVICES (Dependency Injection) ───
builder.Services.AddControllers();
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("Default")));
builder.Services.AddScoped<IVendorRepository, VendorRepository>();
builder.Services.AddScoped<IVendorService, VendorService>();
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options => { /* JWT config */ });
builder.Services.AddSwaggerGen();

var app = builder.Build();

// ── 2. CONFIGURE MIDDLEWARE PIPELINE (ORDER MATTERS!) ───
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthentication();    // Must come BEFORE Authorization!
app.UseAuthorization();
app.MapControllers();
app.Run();
```

---

## 7. API Design - RESTful Best Practices

### REST Naming Conventions:
```
✅ GOOD (noun-based, plural):
  GET    /api/vendors           → Get all vendors
  GET    /api/vendors/1         → Get vendor by ID
  POST   /api/vendors           → Create a vendor
  PUT    /api/vendors/1         → Update entire vendor
  PATCH  /api/vendors/1         → Partially update vendor
  DELETE /api/vendors/1         → Delete vendor

❌ BAD (verb-based):
  GET    /api/getVendors        → Don't use verbs in URL
  POST   /api/createVendor      → HTTP method IS the verb
  DELETE /api/deleteVendor/1    → Redundant verb
```

### HTTP Status Codes — Use the Right One:
```
2xx SUCCESS:
  200 OK              → Successful GET, PUT, PATCH
  201 Created         → Successful POST (return Location header)
  204 No Content      → Successful DELETE (nothing to return)

4xx CLIENT ERROR:
  400 Bad Request     → Invalid data (validation failed)
  401 Unauthorized    → No token or invalid token
  403 Forbidden       → Valid token but no permission
  404 Not Found       → Resource doesn't exist
  409 Conflict        → Duplicate (email already exists)
  422 Unprocessable   → Valid syntax but logical error

5xx SERVER ERROR:
  500 Internal Error  → Something broke on server (log it!)
  503 Unavailable     → Server overloaded or down
```

### Controller Example:
```csharp
[ApiController]
[Route("api/[controller]")]
public class VendorsController : ControllerBase
{
    private readonly IVendorService _service;
    public VendorsController(IVendorService service) => _service = service;

    [HttpGet]
    public async Task<ActionResult<PagedResult<VendorDto>>> GetAll(
        [FromQuery] int page = 1, [FromQuery] int pageSize = 10,
        [FromQuery] string? search = null)
    {
        var result = await _service.GetAllAsync(page, pageSize, search);
        return Ok(result);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<VendorDto>> GetById(int id)
    {
        var vendor = await _service.GetByIdAsync(id);
        return vendor == null ? NotFound() : Ok(vendor);
    }

    [HttpPost]
    [Authorize(Roles = "Admin")]
    public async Task<ActionResult<VendorDto>> Create(CreateVendorRequest request)
    {
        var vendor = await _service.CreateAsync(request);
        return CreatedAtAction(nameof(GetById), new { id = vendor.Id }, vendor);
    }

    [HttpPut("{id}")]
    [Authorize(Roles = "Admin")]
    public async Task<ActionResult<VendorDto>> Update(int id, UpdateVendorRequest request)
    {
        var vendor = await _service.UpdateAsync(id, request);
        return vendor == null ? NotFound() : Ok(vendor);
    }

    [HttpDelete("{id}")]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> Delete(int id)
    {
        var deleted = await _service.DeleteAsync(id);
        return deleted ? NoContent() : NotFound();
    }
}
```

### API Response Standard Format:
```csharp
// Consistent API responses
public class ApiResponse<T>
{
    public bool Success { get; set; }
    public T? Data { get; set; }
    public string? Message { get; set; }
    public List<string> Errors { get; set; } = new();
}

// Success: { "success": true, "data": { ... }, "message": null }
// Error:   { "success": false, "data": null, "message": "Validation failed", "errors": ["Name is required"] }

// Pagination response
public class PagedResult<T>
{
    public List<T> Items { get; set; } = new();
    public int TotalCount { get; set; }
    public int Page { get; set; }
    public int PageSize { get; set; }
    public int TotalPages => (int)Math.Ceiling(TotalCount / (double)PageSize);
    public bool HasNextPage => Page < TotalPages;
    public bool HasPreviousPage => Page > 1;
}
```

---

## 8. Dependency Injection (DI)

DI = Let the framework CREATE and PROVIDE dependencies instead of you doing `new` everywhere.

### The 3 Service Lifetimes:
```csharp
// ── Program.cs ─────────────────────────────────────

// TRANSIENT: New instance EVERY time it's requested
// Use for: Lightweight, stateless services
builder.Services.AddTransient<IEmailService, EmailService>();

// SCOPED: One instance PER HTTP REQUEST (most common for DB work)
// Use for: DbContext, Repositories, Services
builder.Services.AddScoped<IVendorRepository, VendorRepository>();
builder.Services.AddScoped<IVendorService, VendorService>();
builder.Services.AddScoped<AppDbContext>();

// SINGLETON: One instance for the ENTIRE application lifetime
// Use for: Caching, Configuration, HttpClient factory
builder.Services.AddSingleton<ICacheService, MemoryCacheService>();
```

### Visual — How DI Works:
```
WITHOUT DI (Tightly Coupled):                WITH DI (Loosely Coupled):
┌────────────────────────┐                   ┌────────────────────────┐
│ VendorController       │                   │ VendorController       │
│                        │                   │                        │
│ var svc = new          │                   │ IVendorService _svc;   │
│   VendorService(       │                   │                        │
│     new SqlVendorRepo( │                   │ Controller(IVendor     │
│       new AppDbContext( │                  │   Service svc)         │
│         ...)));        │                   │ { _svc = svc; }        │
│                        │                   │                        │
│ ❌ Creates everything  │                   │ ✅ Framework provides  │
│    manually!           │                   │    everything!         │
│ ❌ Can't swap/test     │                   │ ✅ Swap with mock!     │
└────────────────────────┘                   └────────────────────────┘
```

---

## 9. Repository Pattern & Unit of Work

### Repository — Abstracts Data Access:
```csharp
// Domain/Interfaces/IRepository.cs — Generic base
public interface IRepository<T> where T : BaseEntity
{
    Task<T?> GetByIdAsync(int id);
    Task<List<T>> GetAllAsync();
    Task<T> AddAsync(T entity);
    void Update(T entity);
    void Delete(T entity);
}

// Domain/Interfaces/IVendorRepository.cs — Vendor-specific
public interface IVendorRepository : IRepository<Vendor>
{
    Task<List<Vendor>> GetByStatusAsync(VendorStatus status);
    Task<Vendor?> GetByEmailAsync(string email);
    Task<PagedResult<Vendor>> GetPagedAsync(int page, int pageSize, string? search);
}

// Infrastructure/Repositories/VendorRepository.cs — SQL Server implementation
public class VendorRepository : IVendorRepository
{
    private readonly AppDbContext _db;
    public VendorRepository(AppDbContext db) => _db = db;

    public async Task<Vendor?> GetByIdAsync(int id)
        => await _db.Vendors.FindAsync(id);

    public async Task<List<Vendor>> GetAllAsync()
        => await _db.Vendors.AsNoTracking().ToListAsync();

    public async Task<Vendor> AddAsync(Vendor entity)
    {
        await _db.Vendors.AddAsync(entity);
        return entity;
    }

    public void Update(Vendor entity) => _db.Vendors.Update(entity);
    public void Delete(Vendor entity) => entity.IsDeleted = true; // Soft delete

    public async Task<List<Vendor>> GetByStatusAsync(VendorStatus status)
        => await _db.Vendors.Where(v => v.Status == status).ToListAsync();

    public async Task<Vendor?> GetByEmailAsync(string email)
        => await _db.Vendors.FirstOrDefaultAsync(v => v.Email == email);
}
```

### Unit of Work — Coordinating Multiple Repos:
```csharp
// Domain/Interfaces/IUnitOfWork.cs
public interface IUnitOfWork : IDisposable
{
    IVendorRepository Vendors { get; }
    IUserRepository Users { get; }
    Task<int> SaveChangesAsync();
}

// Infrastructure/UnitOfWork.cs
public class UnitOfWork : IUnitOfWork
{
    private readonly AppDbContext _db;
    public IVendorRepository Vendors { get; }
    public IUserRepository Users { get; }

    public UnitOfWork(AppDbContext db,
        IVendorRepository vendors, IUserRepository users)
    {
        _db = db;
        Vendors = vendors;
        Users = users;
    }

    public async Task<int> SaveChangesAsync()
        => await _db.SaveChangesAsync();

    public void Dispose() => _db.Dispose();
}

// Usage in Service:
public class VendorService
{
    private readonly IUnitOfWork _uow;
    public VendorService(IUnitOfWork uow) => _uow = uow;

    public async Task TransferVendor(int vendorId, int newOwnerId)
    {
        var vendor = await _uow.Vendors.GetByIdAsync(vendorId);
        var user = await _uow.Users.GetByIdAsync(newOwnerId);

        vendor.CreatedById = user.Id;
        _uow.Vendors.Update(vendor);

        await _uow.SaveChangesAsync();  // ONE save for both operations!
    }
}
```

---

## 10. Validation

### DTOs (Data Transfer Objects) — What the Client Sends/Receives:
```csharp
// Application/DTOs/CreateVendorRequest.cs
public class CreateVendorRequest
{
    public string VendorName { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public string? Phone { get; set; }
    public string Category { get; set; } = string.Empty;
    public string State { get; set; } = string.Empty;
}

// Application/DTOs/VendorDto.cs — What we RETURN (never expose Entity directly!)
public class VendorDto
{
    public int Id { get; set; }
    public string VendorName { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public string Category { get; set; } = string.Empty;
    public string Status { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; }
    // ❌ Don't include: PasswordHash, IsDeleted, internal fields
}
```

### FluentValidation (Recommended):
```csharp
// Install: dotnet add package FluentValidation.AspNetCore

// Application/Validators/CreateVendorValidator.cs
public class CreateVendorValidator : AbstractValidator<CreateVendorRequest>
{
    public CreateVendorValidator()
    {
        RuleFor(x => x.VendorName)
            .NotEmpty().WithMessage("Vendor name is required")
            .MaximumLength(200).WithMessage("Name cannot exceed 200 characters")
            .MinimumLength(2).WithMessage("Name must be at least 2 characters");

        RuleFor(x => x.Email)
            .NotEmpty().WithMessage("Email is required")
            .EmailAddress().WithMessage("Invalid email format");

        RuleFor(x => x.Category)
            .NotEmpty()
            .Must(c => new[] { "Supplier", "Manufacturer", "Distributor" }.Contains(c))
            .WithMessage("Category must be Supplier, Manufacturer, or Distributor");

        RuleFor(x => x.Phone)
            .Matches(@"^\+?[\d\-\s]{10,15}$")
            .When(x => !string.IsNullOrEmpty(x.Phone))
            .WithMessage("Invalid phone format");
    }
}

// Register in Program.cs
builder.Services.AddFluentValidationAutoValidation();
builder.Services.AddValidatorsFromAssembly(typeof(CreateVendorValidator).Assembly);
```

---

## 11. Error Handling & Logging

### Global Exception Handling Middleware:
```csharp
// API/Middleware/ExceptionHandlingMiddleware.cs
public class ExceptionHandlingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<ExceptionHandlingMiddleware> _logger;

    public ExceptionHandlingMiddleware(RequestDelegate next,
        ILogger<ExceptionHandlingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await _next(context);  // Continue pipeline
        }
        catch (Exception ex)
        {
            await HandleExceptionAsync(context, ex);
        }
    }

    private async Task HandleExceptionAsync(HttpContext context, Exception ex)
    {
        var (statusCode, message) = ex switch
        {
            NotFoundException   => (404, ex.Message),
            ValidationException => (400, ex.Message),
            UnauthorizedAccessException => (401, "Unauthorized"),
            _ => (500, "An unexpected error occurred")
        };

        _logger.LogError(ex, "Error: {Message} | Path: {Path}",
            ex.Message, context.Request.Path);

        context.Response.StatusCode = statusCode;
        context.Response.ContentType = "application/json";

        await context.Response.WriteAsJsonAsync(new ApiResponse<object>
        {
            Success = false,
            Message = message,
            Errors = statusCode == 400 ? new List<string> { ex.Message } : new()
        });
    }
}

// Register in Program.cs (FIRST middleware!)
app.UseMiddleware<ExceptionHandlingMiddleware>();
```

### Structured Logging with Serilog:
```csharp
// Install: dotnet add package Serilog.AspNetCore

// Program.cs
builder.Host.UseSerilog((context, config) => config
    .ReadFrom.Configuration(context.Configuration)
    .WriteTo.Console()
    .WriteTo.File("logs/app-.log", rollingInterval: RollingInterval.Day)
    .Enrich.FromLogContext());

// Usage in any class:
public class VendorService
{
    private readonly ILogger<VendorService> _logger;

    public async Task<VendorDto> CreateAsync(CreateVendorRequest request)
    {
        _logger.LogInformation("Creating vendor: {VendorName}", request.VendorName);
        // ... create vendor ...
        _logger.LogInformation("Vendor created: {VendorId}", vendor.Id);
        return vendorDto;
    }
}
```

### Log Levels:
```
Level           When to Use                            Example
─────────────────────────────────────────────────────────────────
Trace           Detailed debugging (rarely in prod)    SQL query text
Debug           Dev-time diagnostics                   "Entering method X"
Information     Normal operations                      "Vendor 5 created"
Warning         Unexpected but handled                 "Retry attempt 2/3"
Error           Failures (handled exceptions)          "DB connection failed"
Critical        App is crashing                        "Out of memory"
```

---

## 12. Authentication & Authorization

### JWT Authentication Flow:
```
1. Client sends: POST /api/auth/login { email, password }
2. Server validates credentials
3. Server generates JWT token:
   Header:  { "alg": "HS256", "typ": "JWT" }
   Payload: { "sub": "1", "email": "admin@test.com", "role": "Admin", "exp": 1234567890 }
   Signature: HMACSHA256(header + payload, SECRET_KEY)
4. Server returns: { "token": "eyJhbGci..." }
5. Client stores token and sends it with every request:
   Headers: { "Authorization": "Bearer eyJhbGci..." }
6. Server validates token on each request via middleware
```

### JWT Setup in .NET:
```csharp
// Program.cs
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = builder.Configuration["Jwt:Issuer"],
            ValidAudience = builder.Configuration["Jwt:Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Key"]!))
        };
    });

// Protect endpoints:
[Authorize]                           // Any authenticated user
[Authorize(Roles = "Admin")]          // Only Admin role
[Authorize(Roles = "Admin,Manager")]  // Admin OR Manager
[AllowAnonymous]                      // No auth needed (login, register)
```

---

## 13. Configuration Management

### appsettings.json Structure:
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=VendorDb;..."
  },
  "Jwt": {
    "Key": "your-secret-key-minimum-32-characters-long",
    "Issuer": "VendorDirectory",
    "Audience": "VendorDirectory",
    "ExpirationMinutes": 60
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.EntityFrameworkCore": "Warning"
    }
  }
}
```

### Environment-Specific Config:
```
appsettings.json                 ← Base (shared)
appsettings.Development.json     ← Dev overrides (local DB, debug logging)
appsettings.Production.json      ← Prod overrides (real DB, error-only logging)

.NET auto-selects based on ASPNETCORE_ENVIRONMENT variable
```

### Strongly-Typed Configuration (Best Practice):
```csharp
// Application/Settings/JwtSettings.cs
public class JwtSettings
{
    public string Key { get; set; } = string.Empty;
    public string Issuer { get; set; } = string.Empty;
    public string Audience { get; set; } = string.Empty;
    public int ExpirationMinutes { get; set; } = 60;
}

// Program.cs — bind config to class
builder.Services.Configure<JwtSettings>(builder.Configuration.GetSection("Jwt"));

// Usage via DI
public class AuthService
{
    private readonly JwtSettings _jwt;
    public AuthService(IOptions<JwtSettings> jwtOptions) => _jwt = jwtOptions.Value;
}
```

### ⚠️ NEVER Store Secrets in appsettings.json for Production!
```
Development:  appsettings.Development.json is OK
Production:   Use these instead:
  • Azure Key Vault
  • Environment Variables
  • dotnet user-secrets (for local dev)
  • AWS Secrets Manager / HashiCorp Vault
```

---

## 14. Caching

### Why Cache?
```
Without Cache:
  Every request → hits database → slow query → returns data
  100 users request same vendor list → 100 DB queries!

With Cache:
  1st request → hits database → stores result in cache → returns data
  2nd-100th request → gets data from cache instantly → 0 DB queries!
```

### In-Memory Cache (Single Server):
```csharp
// Program.cs
builder.Services.AddMemoryCache();

// Service
public class VendorService
{
    private readonly IMemoryCache _cache;
    private readonly IVendorRepository _repo;

    public async Task<List<VendorDto>> GetAllAsync()
    {
        string cacheKey = "vendors_all";

        // Try cache first
        if (_cache.TryGetValue(cacheKey, out List<VendorDto>? cached))
            return cached!;  // 🚀 Cache HIT — no DB query!

        // Cache MISS — query DB
        var vendors = await _repo.GetAllAsync();
        var dtos = vendors.Select(v => MapToDto(v)).ToList();

        // Store in cache for 5 minutes
        _cache.Set(cacheKey, dtos, TimeSpan.FromMinutes(5));

        return dtos;
    }

    // Invalidate cache when data changes
    public async Task<VendorDto> CreateAsync(CreateVendorRequest request)
    {
        var vendor = /* ... create vendor ... */;
        _cache.Remove("vendors_all");  // Clear cache so next call gets fresh data
        return MapToDto(vendor);
    }
}
```

### Distributed Cache with Redis (Multiple Servers):
```csharp
// Program.cs
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = "localhost:6379";
    options.InstanceName = "VendorApp_";
});

// Usage — same IDistributedCache interface
public class VendorService
{
    private readonly IDistributedCache _cache;

    public async Task<List<VendorDto>> GetAllAsync()
    {
        var cached = await _cache.GetStringAsync("vendors_all");
        if (cached != null)
            return JsonSerializer.Deserialize<List<VendorDto>>(cached)!;

        var vendors = /* ... query DB ... */;
        await _cache.SetStringAsync("vendors_all",
            JsonSerializer.Serialize(vendors),
            new DistributedCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5)
            });
        return vendors;
    }
}
```

### When to Cache vs Not Cache:
```
✅ Cache: Data that doesn't change often (vendor list, categories, config)
✅ Cache: Expensive queries (reports, aggregations)
✅ Cache: Frequently accessed endpoints

❌ Don't Cache: User-specific data that changes constantly
❌ Don't Cache: Real-time data (stock prices, live chat)
❌ Don't Cache: Sensitive data (passwords, tokens)
```

---

## 15. Best Practices Checklist

### 🏗️ Architecture:
```
✅ Use Clean Architecture (Domain → Application → Infrastructure → API)
✅ Keep Domain layer free of external dependencies
✅ Use interfaces for all services and repositories
✅ Use Dependency Injection everywhere (never new up services)
✅ Separate concerns — each class has ONE responsibility (SRP)
```

### 🗄️ Database:
```
✅ Use Code-First migrations (version-controlled schema)
✅ Use EF Core configurations (not Data Annotations) for complex mappings
✅ Always use async/await for DB operations
✅ Use AsNoTracking() for read-only queries
✅ Implement soft delete (IsDeleted flag) instead of hard delete
✅ Add CreatedAt, UpdatedAt, CreatedBy to all tables
✅ Add indexes on columns used in WHERE, JOIN, ORDER BY
✅ Use parameterized queries (never concatenate user input!)
```

### 🌐 API:
```
✅ Use RESTful naming (nouns, plural: /api/vendors)
✅ Return correct HTTP status codes (200, 201, 400, 404, 500)
✅ Use DTOs — never expose domain entities to the API
✅ Implement pagination for list endpoints
✅ Use API versioning (/api/v1/vendors)
✅ Add Swagger/OpenAPI documentation
✅ Validate ALL input (FluentValidation)
```

### 🔐 Security:
```
✅ Use JWT for authentication
✅ Use HTTPS everywhere (UseHttpsRedirection)
✅ Hash passwords (BCrypt/PBKDF2, NEVER plain text)
✅ Use [Authorize] on all endpoints, [AllowAnonymous] selectively
✅ Store secrets in Key Vault, NOT in appsettings.json
✅ Implement CORS properly
✅ Rate limit APIs to prevent abuse
```

### 📋 Code Quality:
```
✅ Use async/await consistently (never .Result or .Wait())
✅ Handle exceptions globally with middleware
✅ Use structured logging (Serilog) with log levels
✅ Write unit tests for services and validators
✅ Write integration tests for controllers
✅ Use strongly-typed configuration (IOptions<T>)
✅ Follow naming conventions (PascalCase for public, _camelCase for private)
```

---

## 📝 Quick Revision — Full Request Flow

```
Client: POST /api/vendors { "vendorName": "Acme" }
  │
  ▼
Kestrel (Web Server)
  ▼
ExceptionHandlingMiddleware     ← Catches any errors
  ▼
AuthenticationMiddleware        ← Validates JWT token
  ▼
AuthorizationMiddleware         ← Checks role = "Admin"
  ▼
VendorsController.Create()      ← [HttpPost] endpoint
  ▼
CreateVendorValidator           ← FluentValidation checks data
  ▼
VendorService.CreateAsync()     ← Business logic / rules
  ▼
VendorRepository.AddAsync()     ← EF Core adds entity
  ▼
AppDbContext.SaveChangesAsync() ← Auto-sets CreatedAt
  ▼
SQL Server                      ← INSERT INTO Vendors VALUES (...)
  ▼
Response: 201 Created { "id": 1, "vendorName": "Acme", ... }
```

### Key Concepts to Know :
```
┌──────────────────────┬───────────────────────────────────────────────┐
│ Concept              │ What It Is                                     │
├──────────────────────┼───────────────────────────────────────────────┤
│ Clean Architecture   │ 4-layer structure with inward dependencies    │
│ Repository Pattern   │ Abstract data access behind interfaces        │
│ Unit of Work         │ Coordinate multiple repos, one SaveChanges    │
│ DI / IoC             │ Framework creates & injects dependencies      │
│ Middleware Pipeline  │ Chain of handlers processing HTTP requests     │
│ DTOs                 │ Data shape for API (not database entities)     │
│ EF Core Migrations   │ Version-controlled database schema changes    │
│ JWT Authentication   │ Stateless token-based auth                    │
│ FluentValidation     │ Input validation library with clean syntax    │
│ Global Error Handler │ Middleware that catches all unhandled errors   │
│ Serilog              │ Structured logging for diagnostics            │
│ Caching              │ Store frequently-used data in memory/Redis    │
│ CORS                 │ Control which domains can call your API       │
│ Soft Delete          │ Mark records as deleted, don't remove them    │
│ API Versioning       │ /api/v1/ vs /api/v2/ for backward compat     │
└──────────────────────┴───────────────────────────────────────────────┘
```

---

**Related Guides:**
**[SQL Learning →](../sql-learning/01-SQL-Basics.md)**
**[OOP Concepts →](../oops-learning/01-OOP-Complete-Guide.md)**
**[gRPC Guide →](../grpc-learning/01-gRPC-Complete-Guide.md)**