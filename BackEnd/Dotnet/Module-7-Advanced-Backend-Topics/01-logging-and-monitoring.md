# 📝 Logging & Monitoring — See What Your API Does in Production

> **Trainer's Note:** When production breaks at 2 AM, logs are your flashlight. Good logging is **structured**, **leveled**, and **safe** (no passwords/tokens). This file covers ASP.NET Core’s built-in logging, Serilog-style structured logs, sinks, and PII-safe habits.

---

## 📑 Table of Contents
1. [Why Logging Matters](#1-why-logging-matters)
2. [Built-in ASP.NET Core Logging](#2-built-in-aspnet-core-logging)
3. [Log Levels](#3-log-levels)
4. [Using ILogger in Practice](#4-using-ilogger-in-practice)
5. [Structured Logging Concepts](#5-structured-logging-concepts)
6. [Serilog Overview](#6-serilog-overview)
7. [Sinks and Targets](#7-sinks-and-targets)
8. [Safe Logging — No PII or Secrets](#8-safe-logging--no-pii-or-secrets)
9. [Monitoring vs Logging (Big Picture)](#9-monitoring-vs-logging-big-picture)
10. [Configuration Tips](#10-configuration-tips)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. Why Logging Matters

```
Without logs:
  "API is slow / failing" → guesswork

With logs:
  traceId + userId + orderId + elapsed ms + exception
  → find root cause in minutes
```

| Goal | How logs help |
|------|----------------|
| Debugging | Reconstruct what happened |
| Auditing | Who did what (carefully) |
| Ops alerts | Error rate spikes |
| Performance | Slow request patterns |

Logging ≠ `Console.WriteLine` forever. Use `ILogger` so levels, filters, and providers work.

---

## 2. Built-in ASP.NET Core Logging

ASP.NET Core includes a logging abstraction: `ILogger<T>` / `ILogger`.

### Default providers (common)
| Provider | Writes to |
|----------|-----------|
| Console | Terminal / container stdout |
| Debug | IDE debug output |
| EventSource | Advanced diagnostics |
| EventLog | Windows Event Log (when enabled) |

`WebApplication.CreateBuilder` wires logging automatically.

```csharp
var builder = WebApplication.CreateBuilder(args);
// builder.Logging already configured from appsettings + defaults
```

### Inject and use
```csharp
public class ProductsController : ControllerBase
{
    private readonly ILogger<ProductsController> _logger;

    public ProductsController(ILogger<ProductsController> logger)
        => _logger = logger;

    [HttpGet("{id:int}")]
    public async Task<ActionResult<ProductDto>> Get(int id)
    {
        _logger.LogInformation("Fetching product {ProductId}", id);
        // ...
    }
}
```

Category is usually the generic type name (`ProductsController`) — great for filtering.

---

## 3. Log Levels

| Level | Typical use |
|-------|-------------|
| **Trace** | Extremely detailed; rarely on in prod |
| **Debug** | Dev diagnostics, verbose flow |
| **Information** | Notable healthy events (started, completed) |
| **Warning** | Unexpected but handled (retry, fallback) |
| **Error** | Failures that need attention |
| **Critical** | App/system in serious trouble |

```
Volume usually:

  Trace > Debug > Information > Warning > Error > Critical
  (more noisy)                              (more severe)
```

### appsettings example
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning",
      "Microsoft.EntityFrameworkCore": "Warning",
      "Shop.Api": "Debug"
    }
  }
}
```

Production tip: keep Microsoft framework noise lower; keep **your** app namespaces informative.

---

## 4. Using ILogger in Practice

### Message templates (preferred)
```csharp
// ✅ structured template with named holes
_logger.LogInformation(
    "Order {OrderId} placed by {UserId} in {ElapsedMs} ms",
    orderId, userId, sw.ElapsedMilliseconds);

// ❌ string interpolation loses structure for many providers
_logger.LogInformation($"Order {orderId} placed by {userId}");
```

### Levels in code
```csharp
_logger.LogDebug("Cache miss for {Key}", key);
_logger.LogInformation("User {UserId} logged in", userId);
_logger.LogWarning("Retrying payment provider, attempt {Attempt}", attempt);
_logger.LogError(ex, "Failed to charge order {OrderId}", orderId);
_logger.LogCritical(ex, "Database unreachable — failing readiness");
```

Pass the **exception as first arg** to `LogError`/`LogCritical` so stacks are captured properly.

### Scopes (optional context)
```csharp
using (_logger.BeginScope(new Dictionary<string, object>
{
    ["TraceId"] = HttpContext.TraceIdentifier,
    ["UserId"] = userId
}))
{
    _logger.LogInformation("Processing checkout");
}
```

---

## 5. Structured Logging Concepts

**Structured logging** stores fields as data, not only plain text.

```
Unstructured:
  "Order 99 failed for user 7"

Structured:
  Message: Order {OrderId} failed for {UserId}
  OrderId: 99
  UserId: 7
  Level: Error
  Timestamp: ...
```

### Why structure wins
| Benefit | Example query in a log platform |
|---------|----------------------------------|
| Search by field | `OrderId = 99` |
| Aggregate | count errors by `Path` |
| Dashboards | p95 duration by endpoint |
| Alerting | error rate where `StatusCode >= 500` |

Even the built-in logger supports template semantics; Serilog specializes in rich structured pipelines.

---

## 6. Serilog Overview

**Serilog** is a popular structured logging library for .NET.

> Install only with your permission if not already in the project, for example:
```bash
dotnet add package Serilog.AspNetCore
```

### Minimal setup idea
```csharp
using Serilog;

Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Information()
    .Enrich.FromLogContext()
    .WriteTo.Console()
    .CreateLogger();

var builder = WebApplication.CreateBuilder(args);
builder.Host.UseSerilog(); // replace default host logging

var app = builder.Build();
app.UseSerilogRequestLogging(); // optional HTTP request log line
app.MapControllers();
try
{
    Log.Information("Starting Shop.Api");
    app.Run();
}
catch (Exception ex)
{
    Log.Fatal(ex, "Host terminated unexpectedly");
}
finally
{
    Log.CloseAndFlush();
}
```

### Enrichers (context fields)
Common enrichments: machine name, environment, application name, correlation id.

```csharp
.Enrich.WithProperty("Application", "Shop.Api")
.Enrich.WithEnvironmentName()
```

---

## 7. Sinks and Targets

A **sink** is where logs go.

| Sink / target | Use case |
|---------------|----------|
| **Console** | Local dev, containers (stdout collected by platform) |
| **File** | Simple servers, short retention files |
| **Seq / Elasticsearch / CloudWatch / App Insights** | Centralized search & alerts |
| **Database** | Sometimes audit tables (careful with volume) |

```
App ──► Serilog / ILogger
           ├── Console sink
           ├── File sink
           └── Central sink (prod)
```

### File sink idea (Serilog)
```csharp
.WriteTo.File("logs/shop-.log", rollingInterval: RollingInterval.Day)
```

### Centralized logging
In production, prefer shipping logs to one place:
- Azure Monitor / Application Insights  
- AWS CloudWatch  
- Grafana Loki / ELK  
- Seq (great for smaller teams)  

### Volume & cost
Logs cost storage and money. Set levels wisely; sample debug traffic; retain based on policy.

---

## 8. Safe Logging — No PII or Secrets

### Never log
| Data | Risk |
|------|------|
| Passwords | Credential leak |
| JWT / refresh tokens | Account takeover |
| Credit card / CVV | Compliance incident |
| Connection strings | Full DB access |
| Full government IDs / health data | PII/PHI exposure |
| Raw auth headers | Token leak |

### Be careful with
| Data | Guidance |
|------|----------|
| Email | Often OK in internal logs; mask if required |
| Names | Policy-dependent |
| Request bodies | May contain secrets — don’t log blindly |
| Query strings | May contain tokens |

```csharp
// ✅
_logger.LogInformation("Password reset requested for user {UserId}", userId);

// ❌
_logger.LogInformation("Password reset token {Token}", rawToken);
_logger.LogDebug("Login payload {@Request}", loginRequest); // may include password
```

### Healthier habits
1. Log **identifiers** (order id, user id), not secrets  
2. Prefer allow-lists of safe properties over dumping objects  
3. Use correlation/`traceId` for support  
4. Redact known sensitive fields in middleware if you log requests  
5. Restrict who can read production log stores  

---

## 9. Monitoring vs Logging (Big Picture)

| | Logging | Monitoring / metrics / traces |
|--|---------|-------------------------------|
| Shape | Events with messages/fields | Numbers + distributed spans |
| Example | “Order 99 failed: timeout” | request rate, error %, p95 latency |
| Good for | Root cause narratives | Health dashboards & alerts |

Production systems often combine:
```
Logs   → what happened (details)
Metrics→ is it healthy (rates/latency)
Traces → request journey across services
```

Beginner path: solid structured logs + basic health checks, then add Application Insights/OpenTelemetry.

### Health checks (related)
```csharp
builder.Services.AddHealthChecks()
    .AddDbContextCheck<AppDbContext>();
app.MapHealthChecks("/health");
```

---

## 10. Configuration Tips

### Per-environment levels
```json
// appsettings.Development.json
{
  "Logging": {
    "LogLevel": {
      "Default": "Debug"
    }
  }
}
```

```json
// appsettings.Production.json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  }
}
```

### HTTP request logging noise
Framework request logs can be chatty — raise `Microsoft.AspNetCore` to `Warning` and use Serilog request logging for one clean line per request if desired.

### Correlation
Include `HttpContext.TraceIdentifier` (or your `X-Correlation-Id`) in error responses (Module 6) **and** logs so support can pivot quickly.

---

## 11. Knowledge Check

**Q1.** Why prefer `ILogger` over `Console.WriteLine`?  
**Q2.** Which level for an unexpected exception that failed a request?  
**Q3.** What is structured logging in one sentence?  
**Q4.** Why are message templates better than string interpolation?  
**Q5.** Name three sinks you might use.  
**Q6.** List four things you should never log.  
**Q7.** Logging vs metrics — which answers “are we down right now?” better?

### Mini practice
1. Inject `ILogger<T>` into a service and log start/finish/failure of `CreateOrder`  
2. Configure different levels for Development vs Production  
3. (Optional) Add Serilog console + file sinks  
4. Add a deliberate bad log line with a fake password, then rewrite it safely  
5. Log `traceId` alongside an intentional error  

### Answers (short)
1. Levels, filtering, providers, testability, prod plumbing  
2. Error (or Critical if system-wide)  
3. Logs as queryable fields + message template, not only text blobs  
4. Providers can capture property values as structure  
5. Console, file, Seq/ELK/App Insights/CloudWatch…  
6. Passwords, tokens, card data, connection strings (etc.)  
7. Metrics/monitoring dashboards (logs still help diagnose)  

---

## ✅ What You Should Feel Confident About

- [ ] Use `ILogger<T>` with the right levels  
- [ ] Configure log levels per namespace/environment  
- [ ] Write structured message templates  
- [ ] Explain Serilog + sinks at a high level  
- [ ] Keep secrets/PII out of logs  
- [ ] Connect logs to correlation ids for support  

**Next:** [02-caching.md](./02-caching.md) — memory cache, Redis, and invalidation patterns.
