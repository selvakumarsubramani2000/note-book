# Day 1 — Middleware Pipeline

> **Goal:** Understand how an HTTP request flows through ASP.NET Core internally, what middleware is, the order it runs in, and how to build your own.

**Context:** All examples use the **Vendor Directory** domain.

---

## 📑 Table of Contents

1. [What is Middleware?](#1-what-is-middleware)
2. [The Request Pipeline](#2-the-request-pipeline)
3. [How a Request Flows Internally](#3-how-a-request-flows-internally)
4. [Built-in Middleware You Use Every Day](#4-built-in-middleware-you-use-every-day)
5. [Middleware Order Matters](#5-middleware-order-matters)
6. [Creating Custom Middleware](#6-creating-custom-middleware)
7. [Short-Circuiting the Pipeline](#7-short-circuiting-the-pipeline)
8. [Map, MapWhen, UseWhen — Branching](#8-map-mapwhen-usewhen--branching)
9. [Hands-On: Build a Request Logger](#9-hands-on-build-a-request-logger)
10. [Key Takeaways](#10-key-takeaways)

---

## 1. What is Middleware?

**Middleware** is a component that sits in the HTTP pipeline. Each middleware can:
1. Inspect/modify the **incoming request**.
2. Pass control to the **next** middleware (or stop).
3. Inspect/modify the **outgoing response** on the way back.

```
      Request ──▶ [MW1] ──▶ [MW2] ──▶ [MW3] ──▶ Endpoint
                                                    │
      Response ◀── [MW1] ◀── [MW2] ◀── [MW3] ◀──────┘
```

Think of it like a chain of security guards — each one can check you, let you through to the next, or send you back.

---

## 2. The Request Pipeline

In `Program.cs` every `app.Use...()` call **adds one middleware** to the pipeline. The order you register them is the order they run.

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddControllers();

var app = builder.Build();

// ↓↓↓  This is the pipeline — runs top-to-bottom for each request
app.UseHttpsRedirection();     // 1. force HTTPS
app.UseStaticFiles();          // 2. serve static files if URL matches
app.UseRouting();              // 3. pick a route
app.UseAuthentication();       // 4. who is the user?
app.UseAuthorization();        // 5. are they allowed?
app.MapControllers();          // 6. call the controller

app.Run();
```

---

## 3. How a Request Flows Internally

Let's trace a single request: `GET /api/vendors/101`

```
┌─────────────────────────────────────────────────────────┐
│ 1. Kestrel (web server) accepts the TCP connection      │
│ 2. Parses HTTP headers & body → creates HttpContext     │
│ 3. Hands HttpContext to the middleware pipeline         │
└─────────────────────────────────────────────────────────┘
                       │
                       ▼
       ┌───────────────────────────────────┐
       │  UseHttpsRedirection              │  ← if HTTP, return 307
       ├───────────────────────────────────┤
       │  UseStaticFiles                   │  ← not a file → next
       ├───────────────────────────────────┤
       │  UseRouting                       │  ← matches route
       ├───────────────────────────────────┤
       │  UseAuthentication                │  ← reads JWT header
       ├───────────────────────────────────┤
       │  UseAuthorization                 │  ← checks role/policy
       ├───────────────────────────────────┤
       │  Endpoint: VendorsController.Get  │  ← your code runs
       └───────────────────────────────────┘
                       │
                       ▼
       ┌───────────────────────────────────┐
       │  Response passes back UP through  │
       │  each middleware (post-next code) │
       └───────────────────────────────────┘
                       │
                       ▼
              Kestrel writes response to socket
```

### The `HttpContext` Object
Every middleware receives an `HttpContext` — a single object holding:
- `HttpContext.Request`  → method, path, headers, query, body
- `HttpContext.Response` → status, headers, body writer
- `HttpContext.User`     → ClaimsPrincipal (after auth)
- `HttpContext.Items`    → per-request bag for your own data
- `HttpContext.RequestServices` → DI scope for this request

---


## 4. Built-in Middleware You Use Every Day

| Middleware | Purpose |
|------------|---------|
| `UseHttpsRedirection()` | Forces HTTP → HTTPS |
| `UseStaticFiles()` | Serves files from `wwwroot` |
| `UseRouting()` | Matches the URL to a route/endpoint |
| `UseCors(policy)` | Cross-Origin Resource Sharing |
| `UseAuthentication()` | Resolves the user from the request (JWT, cookies) |
| `UseAuthorization()` | Enforces `[Authorize]` attributes |
| `UseExceptionHandler("/error")` | Catches unhandled exceptions |
| `UseResponseCaching()` | Caches responses |
| `UseRateLimiter()` | Rate limiting (ASP.NET Core 7+) |
| `MapControllers()` | Wires up attribute-routed controllers |

---

## 5. Middleware Order Matters

This is the **#1 bug** beginners hit. Auth checks happen in the pipeline — they only work if they run **before** your endpoint.

### ❌ Wrong order
```csharp
app.UseAuthorization();        // nothing to authorize yet — no user!
app.UseAuthentication();       // too late
app.MapControllers();
```

### ✅ Correct order
```csharp
app.UseHttpsRedirection();
app.UseRouting();              // must come before Auth
app.UseAuthentication();       // sets HttpContext.User
app.UseAuthorization();        // reads HttpContext.User
app.MapControllers();
```

### The Golden Rule
**Register in the order you want it to run on the request (in), and reverse on the response (out).**

---

## 6. Creating Custom Middleware

There are **3 ways** to write custom middleware.

### Way 1 — Inline with `app.Use`
Good for quick things.

```csharp
app.Use(async (context, next) =>
{
    var sw = Stopwatch.StartNew();

    await next(context);        // 👈 call the next middleware

    sw.Stop();
    var path = context.Request.Path;
    Console.WriteLine($"{path} took {sw.ElapsedMilliseconds} ms");
});
```

### Way 2 — Convention-based class
A class with `InvokeAsync(HttpContext, RequestDelegate)`.

```csharp
public class RequestLoggingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestLoggingMiddleware> _logger;

    public RequestLoggingMiddleware(RequestDelegate next, ILogger<RequestLoggingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        _logger.LogInformation("→ {Method} {Path}", context.Request.Method, context.Request.Path);
        var sw = Stopwatch.StartNew();

        await _next(context);   // pass to next middleware

        sw.Stop();
        _logger.LogInformation("← {StatusCode} ({Ms} ms)",
            context.Response.StatusCode, sw.ElapsedMilliseconds);
    }
}

// Register
app.UseMiddleware<RequestLoggingMiddleware>();
```

### Way 3 — Factory-based (`IMiddleware`)
DI-friendly, supports **scoped** services cleanly.

```csharp
public class CorrelationIdMiddleware : IMiddleware
{
    public async Task InvokeAsync(HttpContext context, RequestDelegate next)
    {
        var id = context.Request.Headers["X-Correlation-Id"].FirstOrDefault()
                 ?? Guid.NewGuid().ToString();

        context.Items["CorrelationId"] = id;
        context.Response.Headers["X-Correlation-Id"] = id;

        await next(context);
    }
}

// Register class AND middleware
builder.Services.AddTransient<CorrelationIdMiddleware>();
app.UseMiddleware<CorrelationIdMiddleware>();
```

### Optional: Clean Extension Method
```csharp
public static class RequestLoggingExtensions
{
    public static IApplicationBuilder UseRequestLogging(this IApplicationBuilder app) =>
        app.UseMiddleware<RequestLoggingMiddleware>();
}

// Usage
app.UseRequestLogging();
```

---

## 7. Short-Circuiting the Pipeline

If a middleware **does NOT call `next`**, the request stops there — subsequent middleware and endpoints never run.

```csharp
// Example: Block requests without an API key
app.Use(async (context, next) =>
{
    if (!context.Request.Headers.TryGetValue("X-Api-Key", out var key) || key != "secret-123")
    {
        context.Response.StatusCode = StatusCodes.Status401Unauthorized;
        await context.Response.WriteAsync("Missing/invalid API key");
        return;                // 🛑 short-circuit — no next()
    }

    await next(context);       // ✅ allow through
});
```

### `app.Use` vs `app.Run`
| Method | Calls `next`? | When to use |
|--------|---------------|-------------|
| `app.Use` | Usually yes | Normal middleware |
| `app.Run` | Never — terminal | Last-resort handler / fallback |

```csharp
app.Run(async context =>
{
    context.Response.StatusCode = 404;
    await context.Response.WriteAsync("Nothing matched");
});
```

---

## 8. Map, MapWhen, UseWhen — Branching

Branch the pipeline for specific paths.

### `Map` — branch by path prefix
```csharp
app.Map("/health", healthApp =>
{
    healthApp.Run(async ctx => await ctx.Response.WriteAsync("OK"));
});
// GET /health → "OK"   (skips everything else)
```

### `MapWhen` — branch by a predicate
```csharp
app.MapWhen(
    ctx => ctx.Request.Query.ContainsKey("legacy"),
    legacyApp =>
    {
        legacyApp.Run(async ctx => await ctx.Response.WriteAsync("Legacy route"));
    });
```

### `UseWhen` — run extra middleware only for some requests (then rejoin)
```csharp
app.UseWhen(
    ctx => ctx.Request.Path.StartsWithSegments("/api"),
    apiPipeline =>
    {
        apiPipeline.UseMiddleware<ApiKeyMiddleware>();
    });
// /api/* goes through ApiKeyMiddleware, then rejoins the main pipeline
```

---

## 9. Hands-On: Build a Request Logger

Add this to your **Vendor Directory** API. It logs every request with method, path, status, duration, and a correlation id.

### Step 1 — Create the middleware
```csharp
// Middleware/RequestLoggingMiddleware.cs
public class RequestLoggingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestLoggingMiddleware> _logger;

    public RequestLoggingMiddleware(RequestDelegate next, ILogger<RequestLoggingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        // 1) Ensure correlation id
        var cid = context.Request.Headers["X-Correlation-Id"].FirstOrDefault()
                  ?? Guid.NewGuid().ToString("N")[..12];
        context.Response.Headers["X-Correlation-Id"] = cid;

        // 2) Capture request
        var sw = System.Diagnostics.Stopwatch.StartNew();
        _logger.LogInformation("[{Cid}] → {Method} {Path}",
            cid, context.Request.Method, context.Request.Path);

        try
        {
            await _next(context);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "[{Cid}] ✖ Unhandled exception", cid);
            throw;   // let exception middleware handle it
        }
        finally
        {
            sw.Stop();
            _logger.LogInformation("[{Cid}] ← {Status} ({Ms} ms)",
                cid, context.Response.StatusCode, sw.ElapsedMilliseconds);
        }
    }
}
```

### Step 2 — Register it
```csharp
// Program.cs
var app = builder.Build();

app.UseMiddleware<RequestLoggingMiddleware>();   // FIRST — captures everything

app.UseHttpsRedirection();
app.UseRouting();
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();

app.Run();
```

### Step 3 — Test it
```
GET /api/vendors → 200 OK   → console:
[a1b2c3d4e5f6] → GET /api/vendors
[a1b2c3d4e5f6] ← 200 (24 ms)
```

Every response now also carries an `X-Correlation-Id` header — invaluable for tracing bugs across services.

---
## 10. Key Takeaways

| Concept | Remember |
|---------|----------|
| **Middleware** | A chain of components that each inspect/modify request & response |
| **Order** | Register in the order you want it to run — Auth before Authz |
| **Short-circuit** | Skip `await next()` to stop the pipeline |
| **3 ways to write it** | Inline `app.Use`, convention-based class, or `IMiddleware` |
| **HttpContext** | Single object carrying request, response, user, services, items |
| **Use vs Run** | `Use` can pass through; `Run` is terminal |
| **Map / UseWhen** | Branch the pipeline by path or predicate |

### Exercises — try before Day 2
1. **API Key middleware** — Add an inline middleware that rejects requests missing `X-Api-Key: secret-123`, but **skip** the check for `/health`.
2. **Response time header** — Write a middleware that puts the elapsed ms into a response header `X-Response-Ms`.
3. **Bad request logger** — Log only 4xx/5xx responses (not successful 2xx ones).
4. **Short-circuit demo** — Create middleware that returns `503` if a static `bool _maintenance = true;` flag is set.

<details>
<summary>💡 Answer — Exercise 2</summary>

```csharp
app.Use(async (ctx, next) =>
{
    var sw = System.Diagnostics.Stopwatch.StartNew();
    ctx.Response.OnStarting(() =>
    {
        sw.Stop();
        ctx.Response.Headers["X-Response-Ms"] = sw.ElapsedMilliseconds.ToString();
        return Task.CompletedTask;
    });
    await next();
});
```
> `OnStarting` is used because headers can't be modified after the response begins streaming.
</details>

---

## ➡️ Next: [Day 2 — Dependency Injection](./Day-02-Dependency-Injection.md)

Tomorrow you'll learn:
- How the DI container works
- Constructor injection
- `Transient` vs `Scoped` vs `Singleton` — with concrete output to see the difference
- Registering interfaces, open generics, keyed services (.NET 8+)

