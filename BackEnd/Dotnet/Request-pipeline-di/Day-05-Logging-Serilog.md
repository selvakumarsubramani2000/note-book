# Day 5 — Logging (Serilog & Structured Logging)

> **Goal:** Master the built-in `ILogger<T>` API, understand **structured logging**, and add Serilog for production-grade logging with sinks, enrichers, and request correlation.

**Prerequisites:** [Day 1](./Day-01-Middleware-Pipeline.md) → [Day 4](./Day-04-JWT-Authentication-Role-Authorization.md)

---

## 📑 Table of Contents

1. [Why Logging Matters](#1-why-logging-matters)
2. [The Built-in `ILogger<T>`](#2-the-built-in-iloggert)
3. [Log Levels](#3-log-levels)
4. [Structured Logging — the big idea](#4-structured-logging--the-big-idea)
5. [Log Categories & Filtering](#5-log-categories--filtering)
6. [Scopes — correlate logs across a request](#6-scopes--correlate-logs-across-a-request)
7. [Serilog — Setup](#7-serilog--setup)
8. [Serilog Sinks (Console / File / Seq / Elastic)](#8-serilog-sinks-console--file--seq--elastic)
9. [Enrichers — add context automatically](#9-enrichers--add-context-automatically)
10. [Request Logging Middleware](#10-request-logging-middleware)
11. [Logging Exceptions Properly](#11-logging-exceptions-properly)
12. [Performance & Best Practices](#12-performance--best-practices)
13. [Key Takeaways & Exercises](#13-key-takeaways--exercises)

---

## 1. Why Logging Matters

Production code runs where you can't attach a debugger. Logs are **the** diagnostic tool for:

- **Troubleshooting** — "why did vendor 42 fail to save?"
- **Auditing** — who did what, and when
- **Monitoring** — error rates, latency, saturation
- **Security** — failed logins, permission denied events
- **Business insights** — feature usage, conversion funnels

A well-logged app is observable. A poorly logged app is a black box.

---

## 2. The Built-in `ILogger<T>`

ASP.NET Core ships with `Microsoft.Extensions.Logging` out of the box. Inject `ILogger<T>` anywhere.

```csharp
public class VendorService(ILogger<VendorService> logger) : IVendorService
{
    public async Task<Vendor?> GetAsync(int id)
    {
        logger.LogInformation("Fetching vendor {VendorId}", id);

        var vendor = await _repo.FindAsync(id);
        if (vendor is null)
        {
            logger.LogWarning("Vendor {VendorId} not found", id);
            return null;
        }

        logger.LogInformation("Vendor {VendorId} loaded: {VendorName}", vendor.Id, vendor.Name);
        return vendor;
    }
}
```

- `T` is the **category** — usually the class type.
- Default providers are Console, Debug, EventSource, EventLog (Windows).
- Logger is **Singleton** — safe to use from any lifetime.

---

## 3. Log Levels

Every log message has a **severity**. Six levels, from chatty to critical:

| Level | Method | When to use | Example |
|-------|--------|-------------|---------|
| Trace | `LogTrace` | Ultra-verbose — variable dumps | `"SQL: SELECT * FROM Vendors WHERE Id = @id"` |
| Debug | `LogDebug` | Dev diagnostics | `"Cache miss for vendor-42"` |
| Information | `LogInformation` | Normal flow events | `"Vendor 42 created"` |
| Warning | `LogWarning` | Unexpected but recoverable | `"Rate limit reached, backing off"` |
| Error | `LogError` | Operation failed, user-visible | `"Failed to save vendor"` |
| Critical | `LogCritical` | App-level disaster | `"Database unreachable"` |

### Rule of thumb
- **Trace / Debug** → off in production (noisy)
- **Information** → normal operations
- **Warning / Error / Critical** → always on, alert on these

### Configuration (`appsettings.json`)
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning",
      "VendorDirectory.Services": "Debug"
    }
  }
}
```

---

## 4. Structured Logging — the big idea

This is the single most important concept in modern logging. **Don't interpolate — templatize.**

### ❌ Traditional (string interpolation)
```csharp
logger.LogInformation($"Vendor {vendor.Id} loaded by user {userId}");
```
Stored as: `"Vendor 42 loaded by user selva"`

Problem: the numbers `42` and `selva` are **baked into the string**. You can't later query:
> *"show me all logs where vendor id = 42"*

### ✅ Structured (message templates)
```csharp
logger.LogInformation("Vendor {VendorId} loaded by user {UserId}", vendor.Id, userId);
```
Stored as (JSON-ish):
```json
{
  "MessageTemplate": "Vendor {VendorId} loaded by user {UserId}",
  "Message":         "Vendor 42 loaded by user selva",
  "VendorId":        42,
  "UserId":          "selva",
  "Timestamp":       "2025-01-05T10:42:11Z",
  "Level":           "Information"
}
```

Now your log aggregator (Seq, ELK, Datadog) can **index** `VendorId` and `UserId` as first-class fields. You can query, filter, chart — log messages become **data**.

### Rules for templates
1. **Use PascalCase property names** — `{VendorId}`, not `{vendorId}`.
2. **Positional order matters** — args map to placeholders left-to-right.
3. **Never interpolate/concatenate the message**:
   ```csharp
   logger.LogInformation("Hi " + name);        // ❌ loses structure
   logger.LogInformation($"Hi {name}");         // ❌ loses structure
   logger.LogInformation("Hi {Name}", name);    // ✅ structured
   ```
4. **Destructure complex objects with `@`:**
   ```csharp
   logger.LogInformation("Created {@Vendor}", vendor);
   // serializes the object's properties as structured data
   ```

### Real-world comparison

| Scenario | Interpolation | Structured |
|----------|---------------|------------|
| Find all errors for vendor 42 | grep string | `VendorId = 42` query |
| Count today's logins per user | regex mayhem | `GROUP BY UserId` |
| Alert if 500 errors > 10/min | brittle | exact field match |

---

## 5. Log Categories & Filtering

The category is the string version of `T` in `ILogger<T>`. Configure per-category minimum levels.

```json
{
  "Logging": {
    "LogLevel": {
      "Default":                            "Information",
      "Microsoft":                          "Warning",
      "Microsoft.EntityFrameworkCore":      "Information",
      "Microsoft.EntityFrameworkCore.Database.Command": "Information",
      "Microsoft.AspNetCore.Hosting":       "Warning",
      "System.Net.Http.HttpClient":         "Warning",
      "VendorDirectory":                    "Debug"
    }
  }
}
```

- Keys are **matched by prefix**. `Microsoft` covers `Microsoft.AspNetCore.*`, `Microsoft.EntityFrameworkCore.*`, etc.
- The **most specific** matching key wins.

### Per-provider overrides
```json
{
  "Logging": {
    "Console": { "LogLevel": { "Default": "Warning" } },
    "Debug":   { "LogLevel": { "Default": "Information" } }
  }
}
```

---

## 6. Scopes — correlate logs across a request

A **scope** attaches properties to every log written inside a `using` block.

```csharp
using (logger.BeginScope(new Dictionary<string, object>
{
    ["CorrelationId"] = ctx.TraceIdentifier,
    ["UserId"]        = ctx.User.FindFirstValue("sub") ?? "anonymous"
}))
{
    logger.LogInformation("Handling request");
    await next();
    logger.LogInformation("Request complete");
}
```

Every log emitted inside the `using` carries `CorrelationId` and `UserId` automatically — without repeating yourself.

### Enable scopes on the Console provider
```json
{
  "Logging": {
    "Console": { "IncludeScopes": true }
  }
}
```

### Use case: request correlation
In a middleware you can begin a scope at the very start of a request so every subsequent log — controller, service, repository — is tagged with the same `CorrelationId`.

---
## 7. Serilog — Setup

The built-in logger is good. **Serilog** is better for structured output, rich sinks, and flexible configuration.

### Install packages
```bash
dotnet add package Serilog.AspNetCore
dotnet add package Serilog.Sinks.Console
dotnet add package Serilog.Sinks.File
dotnet add package Serilog.Enrichers.Environment
dotnet add package Serilog.Enrichers.Thread
```

### Wire it up in `Program.cs`
```csharp
using Serilog;

var builder = WebApplication.CreateBuilder(args);

// Replace the default logging providers with Serilog
builder.Host.UseSerilog((ctx, services, config) => config
    .ReadFrom.Configuration(ctx.Configuration)   // reads the "Serilog" section
    .ReadFrom.Services(services)
    .Enrich.FromLogContext()
    .Enrich.WithMachineName()
    .Enrich.WithThreadId()
    .WriteTo.Console()
    .WriteTo.File("logs/app-.log",
        rollingInterval: RollingInterval.Day,
        retainedFileCountLimit: 14));

var app = builder.Build();

app.UseSerilogRequestLogging();    // one-line request logger (section 10)

app.MapControllers();
app.Run();
```

### Configure from `appsettings.json`
```json
{
  "Serilog": {
    "MinimumLevel": {
      "Default": "Information",
      "Override": {
        "Microsoft.AspNetCore": "Warning",
        "Microsoft.EntityFrameworkCore.Database.Command": "Information"
      }
    },
    "WriteTo": [
      { "Name": "Console" },
      {
        "Name": "File",
        "Args": {
          "path": "logs/app-.log",
          "rollingInterval": "Day",
          "retainedFileCountLimit": 14,
          "outputTemplate": "[{Timestamp:HH:mm:ss} {Level:u3}] {Message:lj} {Properties:j}{NewLine}{Exception}"
        }
      }
    ],
    "Enrich": [ "FromLogContext", "WithMachineName", "WithThreadId" ],
    "Properties": {
      "Application": "VendorDirectory.Api"
    }
  }
}
```

Your code **doesn't change** — you still inject `ILogger<T>`. Serilog slots in underneath.

---

## 8. Serilog Sinks (Console / File / Seq / Elastic)

A **sink** is a destination that receives log events. Mix and match as many as you need.

| Sink | Package | Use for |
|------|---------|---------|
| Console | `Serilog.Sinks.Console` | Local dev, container stdout |
| File | `Serilog.Sinks.File` | Rolling files on disk |
| Seq | `Serilog.Sinks.Seq` | Dev/staging log server (amazing UI for structured logs) |
| ElasticSearch | `Serilog.Sinks.Elasticsearch` | Centralized search + Kibana |
| Azure App Insights | `Serilog.Sinks.ApplicationInsights` | Azure-native APM |
| Seq + JSON file | both | Local + prod concurrently |

### Seq (recommended for learning)
Seq is a free-for-one-user log server that renders structured logs beautifully.

```bash
dotnet add package Serilog.Sinks.Seq
```

```json
{
  "Serilog": {
    "WriteTo": [
      { "Name": "Seq", "Args": { "serverUrl": "http://localhost:5341" } }
    ]
  }
}
```

Run Seq locally (Docker):
```bash
docker run -d --name seq -e ACCEPT_EULA=Y -p 5341:80 datalust/seq
```

Open `http://localhost:5341` → see structured logs with property-based filtering.

### Example: JSON file for prod, Console for dev
```csharp
.WriteTo.Conditional(
    _ => builder.Environment.IsDevelopment(),
    wt => wt.Console())
.WriteTo.Conditional(
    _ => !builder.Environment.IsDevelopment(),
    wt => wt.File(new CompactJsonFormatter(),
        "logs/app-.json", rollingInterval: RollingInterval.Day));
```

---
## 9. Enrichers — add context automatically

An **enricher** attaches a property to every log event. No need to pass it on each call.

### Built-in enrichers
```csharp
.Enrich.FromLogContext()        // honors Serilog.Context.LogContext.PushProperty
.Enrich.WithMachineName()       // MachineName = "API-PROD-01"
.Enrich.WithEnvironmentName()   // EnvironmentName = "Production"
.Enrich.WithThreadId()          // ThreadId = 42
.Enrich.WithProcessId()         // ProcessId = 12345
.Enrich.WithCorrelationId()     // via Serilog.Enrichers.CorrelationId
```

### Custom enricher — add the current user
```csharp
public class UserEnricher(IHttpContextAccessor accessor) : ILogEventEnricher
{
    public void Enrich(LogEvent logEvent, ILogEventPropertyFactory pf)
    {
        var user = accessor.HttpContext?.User;
        if (user?.Identity?.IsAuthenticated != true) return;

        logEvent.AddPropertyIfAbsent(pf.CreateProperty(
            "UserId", user.FindFirst(ClaimTypes.NameIdentifier)?.Value));
        logEvent.AddPropertyIfAbsent(pf.CreateProperty(
            "UserName", user.Identity.Name));
    }
}
```
Register:
```csharp
builder.Services.AddHttpContextAccessor();
builder.Services.AddSingleton<ILogEventEnricher, UserEnricher>();
```

### Push ad-hoc properties for a block of code
```csharp
using (LogContext.PushProperty("OrderId", order.Id))
using (LogContext.PushProperty("CustomerId", order.CustomerId))
{
    logger.LogInformation("Processing order");
    // every log in this block includes OrderId & CustomerId
}
```

---

## 10. Request Logging Middleware

Serilog ships a middleware that logs every HTTP request with timing, status, and route info.

```csharp
app.UseSerilogRequestLogging(opts =>
{
    opts.MessageTemplate =
        "HTTP {RequestMethod} {RequestPath} responded {StatusCode} in {Elapsed:0.0000} ms";

    opts.EnrichDiagnosticContext = (diag, ctx) =>
    {
        diag.Set("UserId",    ctx.User.FindFirstValue("sub") ?? "anonymous");
        diag.Set("ClientIp",  ctx.Connection.RemoteIpAddress?.ToString() ?? "?");
        diag.Set("UserAgent", ctx.Request.Headers.UserAgent.ToString());
    };
});
```

Every request produces **one** log line like:
```
HTTP GET /api/vendors/42 responded 200 in 18.3421 ms
  { "RequestMethod":"GET", "StatusCode":200, "UserId":"selva", "ClientIp":"::1", ... }
```

Place it **after** `UseAuthentication()` so `User` claims are available.

---

## 11. Logging Exceptions Properly

### ✅ Right way — exception as first argument
```csharp
try
{
    await _repo.SaveAsync(vendor);
}
catch (Exception ex)
{
    logger.LogError(ex, "Failed to save vendor {VendorId}", vendor.Id);
    throw;
}
```
The full stack trace is preserved and indexed separately.

### ❌ Wrong way
```csharp
logger.LogError("Error: " + ex.Message);      // loses stack trace
logger.LogError($"Error: {ex}");              // stack trace buried in a string
```

### Don't log **and** throw (usually)
Logging every exception at every level creates duplicate noise. Pattern:
- **Log** where you **handle** (global exception handler — Day 3).
- **Throw** everywhere else.

If you must log mid-stack for diagnostics, use **Debug** level.

---

## 12. Performance & Best Practices

### Avoid expensive args for low levels
```csharp
// ❌ SerializeBigObject runs even if Debug is OFF
logger.LogDebug("Payload: {Payload}", SerializeBigObject(x));

// ✅ guard cheaply
if (logger.IsEnabled(LogLevel.Debug))
    logger.LogDebug("Payload: {Payload}", SerializeBigObject(x));
```

### Use `LoggerMessage` source generator for hot paths (.NET 6+)
```csharp
public static partial class Log
{
    [LoggerMessage(Level = LogLevel.Information,
                   Message = "Vendor {VendorId} created by {UserId}")]
    public static partial void VendorCreated(
        this ILogger logger, int vendorId, string userId);
}

// Usage — zero allocations, compile-time safety
logger.VendorCreated(vendor.Id, userId);
```

### Do's & Don'ts
| ✅ Do | ❌ Don't |
|-------|---------|
| Use message templates `{VendorId}` | Interpolate `$"{id}"` |
| Log exceptions as first arg | Log `ex.Message` as string |
| Use scopes for cross-cutting context | Repeat `userId` on every call |
| Log at the right level | Everything as Information |
| Tune categories per namespace | Leave EF SQL spam at Information |
| Keep sensitive data OUT | Log passwords, tokens, full PII |

---
## 13. Key Takeaways & Exercises

### 🎯 Summary Table
| Concept | Remember |
|---------|----------|
| **`ILogger<T>`** | Inject by category type, built-in Singleton |
| **Levels** | Trace/Debug < Information < Warning/Error/Critical |
| **Structured logging** | `"Msg {Prop}"` + args — never `$"..."` |
| **`@` operator** | `{@Vendor}` destructures object properties |
| **Categories** | Configure per-namespace in `Logging:LogLevel` |
| **Scopes** | `BeginScope` / `PushProperty` add context to a block |
| **Serilog** | Richer sinks, enrichers, request logging |
| **Sinks** | Destinations — Console, File, Seq, Elastic |
| **Enrichers** | Attach MachineName, UserId, ThreadId automatically |
| **`UseSerilogRequestLogging`** | Single-line HTTP log per request |
| **Exceptions** | `LogError(ex, "msg {P}", p)` — `ex` is first arg |

### Exercises

**Exercise 1 — Structured vs Interpolated**
Write two log lines for the same event — one interpolated, one templated. Run the app, find the lines in the JSON file sink, and confirm only the templated one exposes `VendorId` as a searchable field.

**Exercise 2 — Add Serilog to the Vendor API**
- Install the packages in section 7
- Configure Console + File sinks via `appsettings.json`
- Add `app.UseSerilogRequestLogging()`
- Hit `GET /api/vendors` three times and inspect `logs/app-YYYYMMDD.log`

**Exercise 3 — Request Correlation**
Create a `CorrelationIdMiddleware` that:
1. Reads the `X-Correlation-Id` header (or generates one).
2. Pushes it into `LogContext` so **every** log in the request carries it.
3. Adds it back to the response as `X-Correlation-Id`.

<details>
<summary>💡 Skeleton</summary>

```csharp
public class CorrelationIdMiddleware(RequestDelegate next)
{
    public async Task InvokeAsync(HttpContext ctx)
    {
        var id = ctx.Request.Headers["X-Correlation-Id"].FirstOrDefault()
                 ?? Guid.NewGuid().ToString();

        ctx.Response.Headers["X-Correlation-Id"] = id;
        using (LogContext.PushProperty("CorrelationId", id))
            await next(ctx);
    }
}
```
</details>

**Exercise 4 — Custom User Enricher**
Implement the `UserEnricher` from section 9 and verify that all logs after login show `UserId` and `UserName` without passing them explicitly.

**Exercise 5 — Seq Locally**
Spin up Seq via Docker, add the Seq sink, re-run the app, and filter the live stream in the Seq UI by `VendorId = 42` after hitting `GET /api/vendors/42`.

**Exercise 6 — Source-Generated Log**
Convert a hot-path log (e.g., vendor creation) to the `[LoggerMessage]` source-generator pattern. Confirm the output is identical but allocations are lower.

---

## ➡️ Next: [Day 6 — Configuration & Environment Settings](./Day-06-Configuration-Environments.md)

Tomorrow you'll learn:
- `IConfiguration` and the configuration hierarchy
- `appsettings.Development.json`, `appsettings.Production.json`
- Environment variables and `DOTNET_ENVIRONMENT`
- Strongly-typed `IOptions<T>`, `IOptionsSnapshot<T>`, `IOptionsMonitor<T>`
- User Secrets & Azure Key Vault






