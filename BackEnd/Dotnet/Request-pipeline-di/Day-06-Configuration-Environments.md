# Day 6 — Configuration & Environment Settings

> **Goal:** Understand ASP.NET Core's configuration system end-to-end: how settings are loaded, how environments work, and how to use strongly-typed options safely in production.

**Prerequisites:** [Day 1](./Day-01-Middleware-Pipeline.md) → [Day 5](./Day-05-Logging-Serilog.md)

---

## 📑 Table of Contents

1. [Why Configuration Matters](#1-why-configuration-matters)
2. [The `IConfiguration` System](#2-the-iconfiguration-system)
3. [Configuration Sources & Precedence](#3-configuration-sources--precedence)
4. [Environments (`ASPNETCORE_ENVIRONMENT`)](#4-environments-aspnetcore_environment)
5. [Environment-specific `appsettings`](#5-environment-specific-appsettings)
6. [Accessing Configuration — 3 ways](#6-accessing-configuration--3-ways)
7. [Strongly-Typed Options Pattern](#7-strongly-typed-options-pattern)
8. [`IOptions` vs `IOptionsSnapshot` vs `IOptionsMonitor`](#8-ioptions-vs-ioptionssnapshot-vs-ioptionsmonitor)
9. [Validating Options](#9-validating-options)
10. [User Secrets (Local Dev)](#10-user-secrets-local-dev)
11. [Environment Variables (Prod)](#11-environment-variables-prod)
12. [Azure Key Vault & Secret Managers](#12-azure-key-vault--secret-managers)
13. [Key Takeaways & Exercises](#13-key-takeaways--exercises)

---

## 1. Why Configuration Matters

Hard-coded values break deployments. You need a way to:

- Use different connection strings per environment (dev/staging/prod)
- Store API keys and JWT secrets **outside** source control
- Tune timeouts, rate limits, feature flags per deployment
- Reload settings without rebuilding the app

ASP.NET Core's configuration system handles all of this with a single unified API: `IConfiguration`.

---

## 2. The `IConfiguration` System

Think of configuration as a **key-value dictionary** built from multiple sources. Nested JSON uses `:` as the path separator.

### Example `appsettings.json`
```json
{
  "ConnectionStrings": {
    "Default": "Server=.;Database=VendorDb;Trusted_Connection=True"
  },
  "Jwt": {
    "Issuer":   "VendorDirectory",
    "Audience": "VendorDirectoryClients",
    "ExpiryMinutes": 60
  },
  "RateLimit": {
    "PermitLimit": 100,
    "WindowSeconds": 60
  }
}
```

### Reading values
```csharp
var conn   = builder.Configuration["ConnectionStrings:Default"];
var issuer = builder.Configuration["Jwt:Issuer"];
var expiry = builder.Configuration.GetValue<int>("Jwt:ExpiryMinutes");

// Or the shortcut for connection strings:
var conn2  = builder.Configuration.GetConnectionString("Default");
```

> Note: the path is **`Jwt:Issuer`** — the colon navigates into nested objects.

---

## 3. Configuration Sources & Precedence

ASP.NET Core loads configuration from multiple sources in a specific **order**. Later sources **override** earlier ones.

```
1. appsettings.json                          (lowest)
2. appsettings.{Environment}.json
3. User Secrets                              (Development only)
4. Environment Variables
5. Command-line arguments                    (highest)
```

### Visualizing the override chain
```
appsettings.json          →  { "Jwt": { "ExpiryMinutes": 60 } }
appsettings.Development.json →  { "Jwt": { "ExpiryMinutes": 5  } }    overrides
User Secrets              →  { "Jwt:Key": "dev-secret-xxx" }
Environment Variable      →  Jwt__ExpiryMinutes=15                    overrides
Command line              →  --Jwt:ExpiryMinutes=1                    wins
```

### Note on environment variable keys
Environment variable names use `__` (double underscore) as the separator — NOT `:`. This is because some shells don't allow `:` in names.

```bash
# Windows PowerShell
$env:Jwt__Issuer = "VendorDirectory"

# Linux / macOS
export Jwt__Issuer=VendorDirectory
```

Inside the app you still read it as `"Jwt:Issuer"` — .NET translates automatically.

---

## 4. Environments (`ASPNETCORE_ENVIRONMENT`)

The **environment** tells the app which overrides to apply. Three conventional names:

| Environment | When to use |
|-------------|-------------|
| `Development` | Local development — detailed errors, Swagger UI, user-secrets |
| `Staging` | Pre-production testing — prod-like config, test data |
| `Production` | Live — minimal errors, locked-down secrets |

### Check the current environment
```csharp
var builder = WebApplication.CreateBuilder(args);

if (builder.Environment.IsDevelopment()) { /* ... */ }
if (builder.Environment.IsStaging())     { /* ... */ }
if (builder.Environment.IsProduction())  { /* ... */ }

// Or check for a custom name
if (builder.Environment.IsEnvironment("QA")) { /* ... */ }
```


### Setting the environment

**`launchSettings.json`** (for local dev — NOT deployed):
```json
{
  "profiles": {
    "VendorApi": {
      "commandName": "Project",
      "environmentVariables": {
        "ASPNETCORE_ENVIRONMENT": "Development"
      }
    }
  }
}
```

**Command line**:
```bash
dotnet run --environment Staging
```

**OS environment variable**:
```bash
# PowerShell
$env:ASPNETCORE_ENVIRONMENT = "Production"

# Linux
export ASPNETCORE_ENVIRONMENT=Production
```

> ⚠️ If the variable isn't set, ASP.NET Core defaults to `Production`. Always set it explicitly in every environment.

---

## 5. Environment-specific `appsettings`

Create one file per environment next to the base file:

```
📁 VendorApi/
├── appsettings.json
├── appsettings.Development.json
├── appsettings.Staging.json
└── appsettings.Production.json
```

### Only override what differs
`appsettings.json` (base):
```json
{
  "Jwt": {
    "Issuer":   "VendorDirectory",
    "Audience": "VendorDirectoryClients",
    "ExpiryMinutes": 60
  },
  "ConnectionStrings": {
    "Default": "Server=.;Database=VendorDb;Trusted_Connection=True"
  }
}
```

`appsettings.Development.json` — only developer-specific bits:
```json
{
  "Jwt": { "ExpiryMinutes": 5 },
  "Logging": { "LogLevel": { "Default": "Debug" } }
}
```

`appsettings.Production.json` — prod overrides:
```json
{
  "ConnectionStrings": {
    "Default": "Server=prod-sql;Database=VendorDb;User=app;Password=__FROM_SECRETS__"
  },
  "Logging": { "LogLevel": { "Default": "Warning" } }
}
```

> **Rule:** put _non-secret_ values here. Secrets go in User Secrets or Key Vault.

---

## 6. Accessing Configuration — 3 ways

### Way 1 — `IConfiguration` directly
Lowest-level API. Returns strings.
```csharp
public class VendorsController(IConfiguration config) : ControllerBase
{
    [HttpGet("info")]
    public IActionResult Info()
    {
        var issuer = config["Jwt:Issuer"];
        return Ok(new { issuer });
    }
}
```
Downsides: stringly-typed, no validation, no IntelliSense.

### Way 2 — `GetSection(...).Get<T>()`
One-shot binding into a POCO:
```csharp
var jwt = builder.Configuration.GetSection("Jwt").Get<JwtOptions>()!;
builder.Services.AddSingleton(jwt);
```
Good for simple one-time reads at startup.

### Way 3 — Strongly-Typed Options (**preferred**)
Register once, inject `IOptions<T>` anywhere — see section 7.

---

## 7. Strongly-Typed Options Pattern

This is the idiomatic ASP.NET Core way.

### Step 1 — POCO that mirrors the JSON section
```csharp
public class JwtOptions
{
    public const string SectionName = "Jwt";

    public string Issuer         { get; set; } = default!;
    public string Audience       { get; set; } = default!;
    public string Key            { get; set; } = default!;
    public int    ExpiryMinutes  { get; set; } = 60;
}
```

### Step 2 — Bind the section
```csharp
builder.Services.Configure<JwtOptions>(
    builder.Configuration.GetSection(JwtOptions.SectionName));
```

### Step 3 — Inject wherever you need it
```csharp
public class TokenService(IOptions<JwtOptions> opts) : ITokenService
{
    private readonly JwtOptions _jwt = opts.Value;

    public string CreateToken(User user) { /* use _jwt.Issuer, etc. */ }
}
```

Type-safe. IntelliSense. Refactoring-friendly. Centrally validated (section 9).

---
## 8. `IOptions` vs `IOptionsSnapshot` vs `IOptionsMonitor`

Three interfaces inject options — each with different reload & lifetime semantics.

| Interface | Lifetime | Reloads on config change? | Use for |
|-----------|----------|---------------------------|---------|
| **`IOptions<T>`** | Singleton | ❌ No — captured once at app start | 99% of cases; stable settings |
| **`IOptionsSnapshot<T>`** | Scoped | ✅ Yes — new value per request | Per-request tweaks, dev hot-reload |
| **`IOptionsMonitor<T>`** | Singleton | ✅ Yes — push notifications | Long-lived singletons (background services) |

### `IOptions<T>` — the default
```csharp
public class TokenService(IOptions<JwtOptions> opts)
{
    private readonly JwtOptions _jwt = opts.Value;   // captured once
}
```

### `IOptionsSnapshot<T>` — per-request freshness
```csharp
public class FeatureFlagsService(IOptionsSnapshot<FeatureFlags> snapshot)
{
    public bool IsEnabled(string flag) => snapshot.Value.Enabled.Contains(flag);
    // Value re-binds if appsettings changes between requests
}
```
Cannot be injected into Singletons (it's Scoped).

### `IOptionsMonitor<T>` — live updates + change callbacks
```csharp
public class HealthCheckBackgroundService(
    IOptionsMonitor<HealthSettings> monitor,
    ILogger<HealthCheckBackgroundService> logger) : BackgroundService
{
    public HealthCheckBackgroundService(/*…*/)
    {
        monitor.OnChange((newValue, name) =>
            logger.LogInformation("Health settings reloaded: {@Settings}", newValue));
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            var current = monitor.CurrentValue;          // fresh each loop
            await Task.Delay(current.IntervalMs, stoppingToken);
        }
    }
}
```

### When to pick which
```
Is the consumer a Singleton or BackgroundService?
├─ Yes → needs live updates? → IOptionsMonitor<T>
│                 ↳ No          → IOptions<T>
└─ No (Scoped/Transient)        → IOptionsSnapshot<T> (if you want per-request freshness)
                                   or IOptions<T> (if not)
```

---

## 9. Validating Options

Catch bad config at startup instead of crashing in production.

### Data Annotations approach
```csharp
public class JwtOptions
{
    public const string SectionName = "Jwt";

    [Required] [MinLength(1)]
    public string Issuer { get; set; } = default!;

    [Required] [MinLength(1)]
    public string Audience { get; set; } = default!;

    [Required] [MinLength(32, ErrorMessage = "Jwt:Key must be at least 32 chars")]
    public string Key { get; set; } = default!;

    [Range(1, 1440)]
    public int ExpiryMinutes { get; set; } = 60;
}
```

### Register with validation
```csharp
builder.Services
    .AddOptions<JwtOptions>()
    .Bind(builder.Configuration.GetSection(JwtOptions.SectionName))
    .ValidateDataAnnotations()
    .ValidateOnStart();     // 👈 fail at startup, not on first use
```

If config is invalid, the app **refuses to start** — you see the error immediately. This is exactly what you want.

### Custom validation logic
```csharp
builder.Services
    .AddOptions<JwtOptions>()
    .Bind(builder.Configuration.GetSection("Jwt"))
    .Validate(opts => opts.ExpiryMinutes > 0, "ExpiryMinutes must be positive")
    .Validate(opts => !opts.Key.Contains("CHANGE_ME"), "Default placeholder key is not allowed in production")
    .ValidateOnStart();
```

### `IValidateOptions<T>` for complex rules
```csharp
public class JwtOptionsValidator : IValidateOptions<JwtOptions>
{
    public ValidateOptionsResult Validate(string? name, JwtOptions opts)
    {
        var errors = new List<string>();
        if (string.IsNullOrWhiteSpace(opts.Key))       errors.Add("Key required");
        if (opts.Key.Length < 32)                       errors.Add("Key < 32 chars");
        if (opts.Issuer == opts.Audience)               errors.Add("Issuer and Audience must differ");

        return errors.Count == 0
            ? ValidateOptionsResult.Success
            : ValidateOptionsResult.Fail(errors);
    }
}

builder.Services.AddSingleton<IValidateOptions<JwtOptions>, JwtOptionsValidator>();
```

---
## 10. User Secrets (Local Dev)

**Never** commit JWT keys, DB passwords, or API keys to Git. In `Development`, use the .NET **Secret Manager**.

### Initialize
```bash
cd VendorApi
dotnet user-secrets init
```
This adds a `UserSecretsId` GUID to your `.csproj` and points at a machine-local JSON file:
- Windows: `%APPDATA%\Microsoft\UserSecrets\<id>\secrets.json`
- Linux/macOS: `~/.microsoft/usersecrets/<id>/secrets.json`

The file lives **outside** your project folder, so it can never be committed accidentally.

### Set a secret
```bash
dotnet user-secrets set "Jwt:Key" "super-secret-at-least-32-chars-xxxxx"
dotnet user-secrets set "ConnectionStrings:Default" "Server=.;Database=VendorDb;Integrated Security=true"
```

### List / remove
```bash
dotnet user-secrets list
dotnet user-secrets remove "Jwt:Key"
dotnet user-secrets clear
```

### Usage in code — no changes!
`builder.Configuration["Jwt:Key"]` automatically reads from user secrets when running in `Development`. The configuration chain handles it.

> 🔒 User secrets are **only** loaded in `Development`. In other environments they're skipped entirely.

---

## 11. Environment Variables (Prod)

In staging/production, secrets come from **environment variables** set by your deployment platform.

### Docker
```dockerfile
# Dockerfile
ENV ASPNETCORE_ENVIRONMENT=Production
```
```bash
docker run \
  -e Jwt__Key="real-prod-secret-xxxxx" \
  -e ConnectionStrings__Default="Server=prod-sql;..." \
  my-vendor-api
```

### Kubernetes
```yaml
env:
  - name: ASPNETCORE_ENVIRONMENT
    value: "Production"
  - name: Jwt__Key
    valueFrom:
      secretKeyRef:
        name: vendor-secrets
        key: jwt-key
```

### Azure App Service / Linux VM
```bash
az webapp config appsettings set \
  --name VendorApi --resource-group prod \
  --settings Jwt__Key="..." ConnectionStrings__Default="..."
```

All of these surface as `IConfiguration["Jwt:Key"]` — same code, different sources.

### Environment variable prefixes
By default the `EnvironmentVariablesConfigurationSource` reads **all** env vars. You can filter with a prefix:
```csharp
builder.Configuration.AddEnvironmentVariables(prefix: "VENDOR_");
// VENDOR_Jwt__Issuer=... → Configuration["Jwt:Issuer"]
```

Useful when running multiple apps on the same host.

---

## 12. Azure Key Vault & Secret Managers

For real production systems, centralize secrets in a vault.

### Azure Key Vault
```bash
dotnet add package Azure.Extensions.AspNetCore.Configuration.Secrets
dotnet add package Azure.Identity
```

```csharp
if (builder.Environment.IsProduction())
{
    builder.Configuration.AddAzureKeyVault(
        new Uri("https://vendor-kv.vault.azure.net/"),
        new DefaultAzureCredential());
}
```

Secrets stored in Key Vault become configuration entries. `Jwt--Key` in the vault surfaces as `Jwt:Key` in code (dashes translate).

### Other managers
- **AWS Secrets Manager** — `Amazon.Extensions.Configuration.SystemsManager`
- **HashiCorp Vault** — `VaultSharp.Extensions.Configuration`
- **Google Secret Manager** — `Google.Cloud.SecretManager.V1`

All follow the same pattern: register a provider that populates `IConfiguration` from the vault.

### Rule of thumb
| Environment | Where secrets live |
|-------------|-------------------|
| `Development` | User Secrets (local machine) |
| `Staging` | Vault or env vars (managed platform) |
| `Production` | Vault — always |

---

## 13. Key Takeaways & Exercises

### 🎯 Summary Table
| Concept | Remember |
|---------|----------|
| **`IConfiguration`** | Unified key-value store; path uses `:` (or `__` in env vars) |
| **Source order** | JSON → env-specific JSON → user secrets → env vars → CLI |
| **Environment** | Set via `ASPNETCORE_ENVIRONMENT`; defaults to `Production` |
| **env-specific JSON** | Only override what differs; never commit secrets |
| **Options Pattern** | `Configure<T>` + inject `IOptions<T>` — type-safe |
| **`IOptions<T>`** | Singleton, captured once — default choice |
| **`IOptionsSnapshot<T>`** | Scoped, reloads per request |
| **`IOptionsMonitor<T>`** | Singleton, live updates via `OnChange` |
| **Validation** | `ValidateDataAnnotations().ValidateOnStart()` — fail fast |
| **User Secrets** | `dotnet user-secrets` — dev only, never committed |
| **Env vars** | `__` separator; used in prod/containers |
| **Key Vault** | Centralized, auditable secret storage for prod |

### Exercises

**Exercise 1 — Bind Options**
Create `JwtOptions` (section 7) and bind to the `Jwt` section. Inject `IOptions<JwtOptions>` into `TokenService`. Print `_jwt.Issuer` at startup to verify.

**Exercise 2 — Environment Override**
Set `Jwt:ExpiryMinutes = 60` in `appsettings.json` and `5` in `appsettings.Development.json`. Run with `ASPNETCORE_ENVIRONMENT=Development` → confirm value is 5. Run with `Production` → confirm value is 60.

**Exercise 3 — User Secrets**
Move `Jwt:Key` out of `appsettings.json` into user secrets:
```bash
dotnet user-secrets set "Jwt:Key" "dev-super-secret-key-at-least-32-chars"
```
Remove the key from the JSON file. App should still start in Development; should **fail validation** in Production (by design).

**Exercise 4 — Validation**
Add `[Required]` + `[MinLength(32)]` to `JwtOptions.Key`. Set a 10-char key. Start the app — confirm it throws on startup with a clear error.

**Exercise 5 — `IOptionsMonitor` Live Reload**
Inject `IOptionsMonitor<FeatureFlags>` into a background service. Start the app. Edit `appsettings.Development.json`. Observe the `OnChange` callback fires without restart.

**Exercise 6 — Environment Variable Override**
Set `Jwt__ExpiryMinutes=1` in your shell before running `dotnet run`. Confirm it wins over both JSON files.

---

## ➡️ Next: [Day 7 — User Management API Project](./Day-07-User-Management-API-Project.md)

Tomorrow you'll combine everything from days 1–6 into a single small project:
- Controllers + middleware pipeline
- JWT auth with roles
- Structured logging via Serilog
- Config via user secrets + `IOptions<T>`
- Global exception handling with `IExceptionHandler`
- End-to-end manual test with Postman / `curl`




