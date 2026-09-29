# ⚙️ Configuration & Options — Settings Without Hard-Coding

> **Trainer's Note:** Production APIs must not bury connection strings and magic numbers inside C# files. ASP.NET Core configuration layers `appsettings`, environment variables, and secrets — then the **Options pattern** gives your code typed, testable settings.

---

## 📑 Table of Contents
1. [Why Configuration Exists](#1-why-configuration-exists)
2. [appsettings.json Basics](#2-appsettingsjson-basics)
3. [Environment-Based Settings](#3-environment-based-settings)
4. [Configuration Providers and Priority](#4-configuration-providers-and-priority)
5. [Reading Values with IConfiguration](#5-reading-values-with-iconfiguration)
6. [The Options Pattern](#6-the-options-pattern)
7. [IOptions vs IOptionsSnapshot vs IOptionsMonitor](#7-ioptions-vs-ioptionssnapshot-vs-ioptionsmonitor)
8. [Validating Options](#8-validating-options)
9. [Secrets, Connection Strings, and Safety](#9-secrets-connection-strings-and-safety)
10. [End-to-End Example](#10-end-to-end-example)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. Why Configuration Exists

```
Bad:
  var tax = 0.18m;                 // hard-coded
  var cs = "Server=...;Pwd=..."; // hard-coded secret

Good:
  values from configuration
  different per environment
  injected into services
```

| Need | Configuration approach |
|------|------------------------|
| Feature flags | appsettings / env vars |
| DB connection | secrets + env-specific config |
| SMTP server | Options class `EmailSettings` |
| Page size defaults | Options / appsettings |
| API keys | User secrets / env / vault — never git |

---

## 2. appsettings.json Basics

Default JSON structure:

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*",
  "Shop": {
    "DefaultPageSize": 20,
    "MaxPageSize": 100,
    "SupportEmail": "support@shop.local"
  },
  "ConnectionStrings": {
    "ShopDb": "Server=localhost;Database=Shop;Trusted_Connection=True;TrustServerCertificate=True"
  }
}
```

### Nested sections map to keys with `:`
```
Shop:DefaultPageSize
Shop:SupportEmail
ConnectionStrings:ShopDb
```

`WebApplication.CreateBuilder(args)` loads `appsettings.json` automatically.

---

## 3. Environment-Based Settings

ASP.NET Core environment name (common values):
- `Development`
- `Staging`
- `Production`

### Files
| File | Role |
|------|------|
| `appsettings.json` | Base settings for all environments |
| `appsettings.Development.json` | Local developer overrides |
| `appsettings.Production.json` | Production overrides |

### Example `appsettings.Development.json`
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Debug"
    }
  },
  "Shop": {
    "DefaultPageSize": 5
  }
}
```

### How environment is chosen
| Source | Example |
|--------|---------|
| `launchSettings.json` | `"ASPNETCORE_ENVIRONMENT": "Development"` |
| Environment variable | `ASPNETCORE_ENVIRONMENT=Production` |
| Dotnet CLI / host config | deployment settings |

```csharp
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
}
```

```
Loading order idea:
  appsettings.json
    + appsettings.{Environment}.json  (overrides)
    + environment variables            (override again)
    + command line                     (highest common override)
```

---

## 4. Configuration Providers and Priority

`CreateBuilder` sets up a layered configuration system. Later providers override earlier ones.

### Typical priority (simplified, low → high)
1. `appsettings.json`  
2. `appsettings.{Environment}.json`  
3. User secrets (Development)  
4. Environment variables  
5. Command-line arguments  

```
Same key Shop:DefaultPageSize

appsettings.json                = 20
appsettings.Development.json    = 5
env var Shop__DefaultPageSize   = 50   ← wins if set
```

### Environment variable naming
Nested JSON keys use `__` (double underscore) in env vars:
```bash
Shop__DefaultPageSize=50
ConnectionStrings__ShopDb=...
```

---

## 5. Reading Values with IConfiguration

### Inject `IConfiguration`
```csharp
public class ProductsController : ControllerBase
{
    private readonly IConfiguration _config;

    public ProductsController(IConfiguration config)
    {
        _config = config;
    }

    [HttpGet("config-demo")]
    public IActionResult Demo()
    {
        var pageSize = _config.GetValue<int>("Shop:DefaultPageSize");
        var email = _config["Shop:SupportEmail"];
        var cs = _config.GetConnectionString("ShopDb");
        return Ok(new { pageSize, email, hasConnectionString = cs is not null });
    }
}
```

### Common APIs
| API | Use |
|-----|-----|
| `config["Section:Key"]` | String lookup |
| `config.GetValue<T>("Key")` | Typed conversion |
| `config.GetConnectionString("name")` | `ConnectionStrings:name` |
| `config.GetSection("Shop")` | Bound subsection |

### Fine for quick reads — not ideal everywhere
String keys scatter through code (`"Shop:DefaultPageSize"`). Typos fail late. Prefer **Options pattern** for structured settings.

---

## 6. The Options Pattern

**Options pattern** = bind a config section to a strongly typed class and inject it.

### 1) Settings class
```csharp
public class ShopOptions
{
    public const string SectionName = "Shop";

    public int DefaultPageSize { get; set; } = 20;
    public int MaxPageSize { get; set; } = 100;
    public string SupportEmail { get; set; } = string.Empty;
}
```

### 2) Register binding
```csharp
builder.Services.Configure<ShopOptions>(
    builder.Configuration.GetSection(ShopOptions.SectionName));
```

Or:
```csharp
builder.Services
    .AddOptions<ShopOptions>()
    .Bind(builder.Configuration.GetSection(ShopOptions.SectionName))
    .ValidateDataAnnotations()
    .ValidateOnStart();
```

### 3) Inject into service
```csharp
public class ProductService : IProductService
{
    private readonly ShopOptions _options;

    public ProductService(IOptions<ShopOptions> options)
    {
        _options = options.Value;
    }

    public int NormalizePageSize(int requested)
    {
        if (requested <= 0) return _options.DefaultPageSize;
        return Math.Min(requested, _options.MaxPageSize);
    }
}
```

### Benefits
- IntelliSense and refactor-safe properties  
- One section schema  
- Easy unit tests with custom options values  
- Clear ownership of settings  

---

## 7. IOptions vs IOptionsSnapshot vs IOptionsMonitor

| Interface | Lifetime behavior | Reloads on change? | Typical use |
|-----------|-------------------|--------------------|-------------|
| **`IOptions<T>`** | Options object is singleton-ish | No (fixed after start for practical beginner view) | App-wide stable settings |
| **`IOptionsSnapshot<T>`** | Scoped | Yes, per request if config reloads | Settings that may change and are used in request services |
| **`IOptionsMonitor<T>`** | Singleton + change notifications | Yes + callbacks | React when settings change live |

```csharp
public EmailService(IOptionsSnapshot<EmailOptions> options)
{
    _options = options.Value; // fresh per request scope if reloaded
}
```

### Beginner default
Start with **`IOptions<T>`** or **`IOptionsSnapshot<T>`** for request services.  
Learn `IOptionsMonitor<T>` when you need live reload reactions.

### Never inject `IOptionsSnapshot<T>` into a singleton
Same captive-dependency idea as DI lifetimes.

---

## 8. Validating Options

Catch bad configuration **at startup**, not after midnight incidents.

```csharp
using System.ComponentModel.DataAnnotations;

public class ShopOptions
{
    public const string SectionName = "Shop";

    [Range(1, 200)]
    public int DefaultPageSize { get; set; } = 20;

    [Range(1, 500)]
    public int MaxPageSize { get; set; } = 100;

    [Required, EmailAddress]
    public string SupportEmail { get; set; } = string.Empty;
}
```

```csharp
builder.Services
    .AddOptions<ShopOptions>()
    .BindConfiguration(ShopOptions.SectionName) // binds section "Shop"
    .ValidateDataAnnotations()
    .Validate(o => o.DefaultPageSize <= o.MaxPageSize,
        "DefaultPageSize cannot exceed MaxPageSize")
    .ValidateOnStart();
```

If Production config is wrong, app fails fast with a clear options validation error.

---

## 9. Secrets, Connection Strings, and Safety

### Do NOT commit secrets
- passwords  
- API keys  
- private tokens  
- production connection strings with credentials  

### Development: User Secrets
```bash
dotnet user-secrets init
dotnet user-secrets set "ConnectionStrings:ShopDb" "Server=...;Password=...;"
```
User secrets map into configuration only on the local machine (Development workflow).

### Production: environment variables / vault
```bash
ConnectionStrings__ShopDb=...
```
Or cloud secret stores (Azure Key Vault, etc.) integrated as configuration providers.

### Safe `appsettings.json` pattern
```json
{
  "ConnectionStrings": {
    "ShopDb": "Server=localhost;Database=Shop;Trusted_Connection=True;TrustServerCertificate=True"
  }
}
```
Local sample only. Production overrides via env/secure store.

### Logging caution
Never log full connection strings or raw secrets.

---

## 10. End-to-End Example

### appsettings.json
```json
{
  "Shop": {
    "DefaultPageSize": 20,
    "MaxPageSize": 100,
    "SupportEmail": "help@shop.local"
  }
}
```

### Program.cs
```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services
    .AddOptions<ShopOptions>()
    .Bind(builder.Configuration.GetSection(ShopOptions.SectionName))
    .ValidateDataAnnotations()
    .Validate(o => o.DefaultPageSize <= o.MaxPageSize,
        "DefaultPageSize cannot exceed MaxPageSize")
    .ValidateOnStart();

builder.Services.AddScoped<IProductService, ProductService>();

var app = builder.Build();
app.MapControllers();
app.Run();
```

### Service
```csharp
public class ProductService : IProductService
{
    private readonly ShopOptions _shop;

    public ProductService(IOptions<ShopOptions> shopOptions)
    {
        _shop = shopOptions.Value;
    }

    public int ResolvePageSize(int? pageSize)
    {
        var size = pageSize is null or <= 0 ? _shop.DefaultPageSize : pageSize.Value;
        return Math.Min(size, _shop.MaxPageSize);
    }
}
```

### Controller
```csharp
[HttpGet]
public async Task<ActionResult<IEnumerable<ProductResponseDto>>> GetAll(
    [FromQuery] int? pageSize,
    CancellationToken ct)
{
    var size = _products.ResolvePageSize(pageSize);
    var items = await _products.GetPageAsync(size, ct);
    return Ok(items);
}
```

Typed settings + DI + controller query params = clean, environment-aware API behavior.

---

## 11. Knowledge Check

**Q1.** What file holds base settings for all environments?  
**Q2.** How does `appsettings.Development.json` interact with `appsettings.json`?  
**Q3.** How do nested keys appear as environment variables?  
**Q4.** Why prefer Options pattern over scattering `_config["a:b"]` everywhere?  
**Q5.** `IOptions<T>` vs `IOptionsSnapshot<T>` — when would snapshot help?  
**Q6.** What does `ValidateOnStart()` buy you?  
**Q7.** Where should production database passwords live?

### Mini practice
1. Add a `Shop` section to appsettings  
2. Create `ShopOptions` with DataAnnotations  
3. Bind + validate on start  
4. Inject `IOptions<ShopOptions>` into a service  
5. Override `DefaultPageSize` in Development file and confirm runtime value  
6. Set an env var override and confirm it wins  

### Answers (short)
1. `appsettings.json`  
2. Overrides matching keys for Development  
3. `Section__Key` double underscores  
4. Typed, validated, testable, refactor-safe settings  
5. Per-request updated values when config reloads  
6. Fail fast if configuration is invalid  
7. Environment variables / secret manager / vault — not git  

---

## ✅ What You Should Feel Confident About

- [ ] Structure `appsettings.json` sections cleanly  
- [ ] Use environment-specific overrides  
- [ ] Read config via `IConfiguration` when needed  
- [ ] Bind sections with the Options pattern  
- [ ] Choose among `IOptions` / `IOptionsSnapshot` at a basic level  
- [ ] Keep secrets out of source control  

**Previous:** [05-middleware-and-request-pipeline.md](./05-middleware-and-request-pipeline.md)

---

## 🚀 Module 3 Wrap-Up

You can now build a **structured ASP.NET Core Web API** with:

| Skill | Where |
|-------|-------|
| Project startup & controllers | 01 |
| Routing & result status codes | 02 |
| DTOs, binding, validation | 03 |
| DI + service layer | 04 |
| Middleware pipeline | 05 |
| Configuration & Options | 06 |

### Production-ready habits checklist
- [ ] Controllers stay thin  
- [ ] DTOs at HTTP boundary; domain rules inside  
- [ ] Validate inputs server-side  
- [ ] Register services with correct lifetimes  
- [ ] Middleware ordered intentionally  
- [ ] Settings typed + environment-aware  
- [ ] Secrets never committed  

**Suggested next module:** Data access with EF Core — DbContext, entities, migrations, repositories/query patterns, and wiring SQL into your service layer.
