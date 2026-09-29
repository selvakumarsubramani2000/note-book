# ⚙️ Configuration for Environments — Dev, Staging, Production

> **Trainer's Note:** The same API binary should run in **Development**, **Staging**, and **Production** with different settings — URLs, logging, connection strings, feature flags. ASP.NET Core’s configuration system layers files and environment variables. Secrets never belong in git.

---

## 📑 Table of Contents
1. [Why Environments Exist](#1-why-environments-exist)
2. [ASPNETCORE_ENVIRONMENT](#2-aspnetcore_environment)
3. [Configuration Files](#3-configuration-files)
4. [How Settings Merge (Priority)](#4-how-settings-merge-priority)
5. [Reading Configuration in Code](#5-reading-configuration-in-code)
6. [Environment-Specific Behavior in Program.cs](#6-environment-specific-behavior-in-programcs)
7. [launchSettings vs Real Servers](#7-launchsettings-vs-real-servers)
8. [Secret Management Principles](#8-secret-management-principles)
9. [User Secrets and Environment Variables](#9-user-secrets-and-environment-variables)
10. [Practical Environment Checklist](#10-practical-environment-checklist)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. Why Environments Exist

| Environment | Purpose |
|-------------|---------|
| **Development** | Local machine; verbose logs; Swagger on; test data |
| **Staging** | Production-like rehearsal; real integrations (sandbox) |
| **Production** | Live users; strict security; minimal noise; real secrets |

```
Same code ──► different config ──► different behavior
```

| What changes by environment | What should stay the same |
|-----------------------------|---------------------------|
| Connection strings | Business rules (mostly) |
| Log levels | Route design |
| CORS origins | Domain logic |
| Feature flags | Tested code path |
| Swagger on/off | Auth algorithms (keys differ) |

Never “special-case production” with random `if` hacks when configuration can express it.

---

## 2. ASPNETCORE_ENVIRONMENT

The host reads the environment name from:

| Source | Example |
|--------|---------|
| Environment variable | `ASPNETCORE_ENVIRONMENT=Production` |
| `launchSettings.json` (local) | `"ASPNETCORE_ENVIRONMENT": "Development"` |
| Hosting settings | Azure App Setting, container env, IIS |

```bash
# PowerShell session example
$env:ASPNETCORE_ENVIRONMENT = "Staging"
dotnet run
```

```csharp
if (app.Environment.IsDevelopment()) { /* ... */ }
if (app.Environment.IsStaging()) { /* ... */ }
if (app.Environment.IsProduction()) { /* ... */ }
if (app.Environment.IsEnvironment("Qa")) { /* custom */ }
```

Default when unset is often **Production** on deployed hosts — verify explicitly.

---

## 3. Configuration Files

| File | Role |
|------|------|
| `appsettings.json` | Base settings for all environments |
| `appsettings.Development.json` | Local/dev overrides |
| `appsettings.Staging.json` | Staging overrides (optional) |
| `appsettings.Production.json` | Production overrides (non-secret preferred) |
| `appsettings.{Environment}.json` | Any custom environment name |

### Base `appsettings.json`
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
    "MaxPageSize": 100
  },
  "ConnectionStrings": {
    "ShopDb": "SET_VIA_ENV_OR_SECRETS"
  }
}
```

### `appsettings.Development.json`
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Debug",
      "Shop": "Debug"
    }
  },
  "Shop": {
    "DefaultPageSize": 5
  },
  "Cors": {
    "Origins": [ "http://localhost:3000", "http://localhost:4200" ]
  }
}
```

### `appsettings.Production.json`
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "api.shop.com;shop.com",
  "Cors": {
    "Origins": [ "https://app.shop.com" ]
  }
}
```

**Tip:** Keep structure in git; inject **secret values** at runtime.

---

## 4. How Settings Merge (Priority)

`WebApplication.CreateBuilder` loads providers roughly like this (later wins):

```
1. appsettings.json
2. appsettings.{Environment}.json
3. User secrets          (Development commonly)
4. Environment variables
5. Command-line args
```

```
Shop:DefaultPageSize

appsettings.json             = 20
appsettings.Development.json = 5
env Shop__DefaultPageSize    = 50   ← wins if set
```

### Nested keys as environment variables
Use double underscore `__`:

```bash
ConnectionStrings__ShopDb=Server=...;Password=...;
Jwt__Key=super-long-secret
Shop__DefaultPageSize=50
```

---

## 5. Reading Configuration in Code

### IConfiguration
```csharp
var pageSize = builder.Configuration.GetValue<int>("Shop:DefaultPageSize");
var cs = builder.Configuration.GetConnectionString("ShopDb");
var origins = builder.Configuration.GetSection("Cors:Origins").Get<string[]>();
```

### Options pattern (preferred for structured settings)
```csharp
public class ShopOptions
{
    public const string SectionName = "Shop";
    public int DefaultPageSize { get; set; } = 20;
    public int MaxPageSize { get; set; } = 100;
}

builder.Services.Configure<ShopOptions>(
    builder.Configuration.GetSection(ShopOptions.SectionName));

// inject IOptions<ShopOptions>
```

Strongly typed options + validation (Module 3/6 habits) beat scattered string keys.

---

## 6. Environment-Specific Behavior in Program.cs

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddControllers();
builder.Services.AddDbContext<AppDbContext>(/* connection from config */);

if (builder.Environment.IsDevelopment())
{
    builder.Services.AddSwaggerGen();
}

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}
else
{
    app.UseExceptionHandler();
    app.UseHsts();
}

app.UseHttpsRedirection();

var corsOrigins = app.Configuration.GetSection("Cors:Origins").Get<string[]>() ?? [];
app.UseCors(policy => policy.WithOrigins(corsOrigins).AllowAnyHeader().AllowAnyMethod());

app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();
app.Run();
```

| Feature | Dev | Prod |
|---------|-----|------|
| Swagger | Often on | Off / locked |
| Detailed errors | Developer page | Problem Details generic |
| HSTS | Off usually | On |
| Log level | Debug | Information/Warning |
| HTTPS cert | Dev cert | Real cert |

---

## 7. launchSettings vs Real Servers

`Properties/launchSettings.json` affects **local** `dotnet run` / IDE F5 only.

```json
{
  "profiles": {
    "https": {
      "commandName": "Project",
      "applicationUrl": "https://localhost:7xxx;http://localhost:5xxx",
      "environmentVariables": {
        "ASPNETCORE_ENVIRONMENT": "Development"
      }
    }
  }
}
```

| launchSettings | Production host |
|----------------|-----------------|
| Convenience for dev | Env vars / platform config |
| Not used in published containers by default | You set `ASPNETCORE_ENVIRONMENT` |
| May include free ports | Real domains and TLS |

Do not rely on `launchSettings.json` for deployed behavior.

---

## 8. Secret Management Principles

### Never commit
- DB passwords  
- JWT signing keys  
- Third-party API keys  
- Private certificates  
- Client secrets  

### Store secrets where?
| Stage | Common tool |
|-------|-------------|
| Local Development | .NET **User Secrets** |
| CI | Pipeline secret variables |
| Production | Env vars, Key Vault, cloud secret manager |
| Containers | Orchestrator secrets / env injection |

```
Git repo:
  ✅ appsettings structure, non-secret defaults
  ❌ real production passwords
```

### Rotation mindset
Assume secrets leak eventually — design for rotation (new JWT key, new DB password) with minimal downtime.

---

## 9. User Secrets and Environment Variables

### User Secrets (Development)
```bash
dotnet user-secrets init
dotnet user-secrets set "ConnectionStrings:ShopDb" "Server=localhost;Database=Shop;..."
dotnet user-secrets set "Jwt:Key" "LOCAL_ONLY_LONG_RANDOM_KEY_1234567890"
dotnet user-secrets list
```

Secrets live outside the project folder (user profile) and map into configuration when environment is Development.

### Production environment variables
Azure App Service example (concept):
```
ASPNETCORE_ENVIRONMENT = Production
ConnectionStrings__ShopDb = ...
Jwt__Key = ...
```

Docker:
```bash
docker run -e ASPNETCORE_ENVIRONMENT=Production -e Jwt__Key=... shop-api:latest
```

### Layered mental model
```
Code requests IConfiguration["Jwt:Key"]
        ▲
        │ merged view
 providers: files → user secrets → env → vault provider
```

---

## 10. Practical Environment Checklist

| Item | Dev | Staging | Prod |
|------|-----|---------|------|
| `ASPNETCORE_ENVIRONMENT` set | Development | Staging | Production |
| Swagger | On | Optional locked | Off/locked |
| Secrets source | User secrets | Vault/env | Vault/env |
| DB | Local/docker | Prod-like | Real HA DB |
| CORS origins | localhost UI | staging UI host | real UI host |
| Log level | Debug/Info | Info | Info/Warn |
| HTTPS | Dev cert | Real/test cert | Real cert |
| Error detail | Rich | Controlled | Safe only |
| Seed data | OK | Careful | No casual seeds |

---

## 11. Knowledge Check

**Q1.** What environment variable selects `appsettings.Production.json`?  
**Q2.** Which wins if both appsettings and env define the same key?  
**Q3.** How is nested JSON expressed as an environment variable?  
**Q4.** Why is `launchSettings.json` not enough for production?  
**Q5.** Where should JWT signing keys live in Development vs Production?  
**Q6.** Name three settings that commonly differ per environment.  
**Q7.** Why keep secret *values* out of git while still committing `appsettings` structure?

### Mini practice
1. Add `Shop` section with page sizes in base + Development override  
2. Read via `IOptions<ShopOptions>`  
3. Set user secret for connection string  
4. Run with `ASPNETCORE_ENVIRONMENT=Staging` and observe which file loads  
5. Write a short table of your project’s per-env differences  

### Answers (short)
1. `ASPNETCORE_ENVIRONMENT=Production`  
2. Environment variable (later provider) typically  
3. `Section__Key` double underscores  
4. It only applies to local launch profiles  
5. User secrets vs vault/env/managed identity  
6. Connection strings, log levels, CORS, Swagger…  
7. Structure documents shape; values are credentials  

---

## ✅ What You Should Feel Confident About

- [ ] Explain Dev/Staging/Prod purpose  
- [ ] Use `ASPNETCORE_ENVIRONMENT` and env-specific appsettings  
- [ ] Predict configuration merge order  
- [ ] Read config via `IConfiguration` / Options  
- [ ] Keep secrets out of source control  
- [ ] Apply user secrets locally and env vars on servers  

**Next:** [02-building-and-publishing.md](./02-building-and-publishing.md) — `dotnet publish` and deployment models.
