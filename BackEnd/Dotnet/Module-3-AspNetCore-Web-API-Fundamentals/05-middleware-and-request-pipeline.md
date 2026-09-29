# 🔁 Middleware & the Request Pipeline — The Path of Every HTTP Call

> **Trainer's Note:** Controllers do not see requests first. **Middleware** runs as a pipeline — like airport security lanes — before and after your endpoint. Order is everything. Learn this well and logging, auth, errors, and cross-cutting concerns become clean.

---

## 📑 Table of Contents
1. [What Is Middleware?](#1-what-is-middleware)
2. [The Request Pipeline Mental Model](#2-the-request-pipeline-mental-model)
3. [How Middleware Is Added in Program.cs](#3-how-middleware-is-added-in-programcs)
4. [Built-in Middleware You Will Use](#4-built-in-middleware-you-will-use)
5. [Execution Order and Why It Matters](#5-execution-order-and-why-it-matters)
6. [Creating Custom Middleware](#6-creating-custom-middleware)
7. [Inline Middleware with `Use`](#7-inline-middleware-with-use)
8. [Short-Circuiting the Pipeline](#8-short-circuiting-the-pipeline)
9. [Exception Handling Middleware](#9-exception-handling-middleware)
10. [Request Timing / Logging Example](#10-request-timing--logging-example)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. What Is Middleware?

**Middleware** = a component that sits in the HTTP pipeline and can:
- inspect/modify the **request**
- do work
- call the **next** middleware
- inspect/modify the **response** on the way back
- or **stop** the pipeline (short-circuit)

```
Each middleware is a station:

 Request  →  [A] → [B] → [C] → endpoint  →  [C] → [B] → [A]  → Response
```

Cross-cutting concerns belong here when they apply to many endpoints:
- logging
- authentication / authorization
- exception handling
- HTTPS redirection
- CORS
- correlation IDs

---

## 2. The Request Pipeline Mental Model

```
                    HTTP REQUEST
                         │
                         ▼
              ┌─────────────────────┐
              │ Exception handler   │  (outermost often)
              └─────────┬───────────┘
                        ▼
              ┌─────────────────────┐
              │ HTTPS redirection   │
              └─────────┬───────────┘
                        ▼
              ┌─────────────────────┐
              │ Routing             │
              └─────────┬───────────┘
                        ▼
              ┌─────────────────────┐
              │ CORS / AuthN / AuthZ│
              └─────────┬───────────┘
                        ▼
              ┌─────────────────────┐
              │ Endpoint (controller│
              │ action / minimal)   │
              └─────────┬───────────┘
                        ▼
                    HTTP RESPONSE
                 (unwinds outward)
```

Middleware forms a **nested** call stack:
1. Outer middleware runs first on the way in  
2. Endpoint runs at the center  
3. Outer middleware finishes last on the way out  

---

## 3. How Middleware Is Added in Program.cs

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddControllers();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthentication();   // if configured
app.UseAuthorization();
app.MapControllers();

app.Run();
```

| API | Meaning |
|-----|---------|
| `app.UseX()` | Add middleware to pipeline |
| `app.MapX()` | Add endpoint routing terminal branches |
| `app.Run(handler)` | Terminal middleware (doesn’t call next) — don’t confuse with `app.Run()` host start |

> Host start `app.Run()` with **no args** starts the server.  
> `app.Run(async ctx => ...)` (with a delegate) adds terminal middleware. Different overloads — naming can confuse beginners.

---

## 4. Built-in Middleware You Will Use

| Middleware | Typical call | Job |
|------------|--------------|-----|
| Exception handler / developer exception page | `UseExceptionHandler` / `UseDeveloperExceptionPage` | Catch unhandled errors |
| HTTPS redirection | `UseHttpsRedirection` | HTTP → HTTPS |
| Static files | `UseStaticFiles` | Serve wwwroot files (less central for pure APIs) |
| Routing | `UseRouting` | Match endpoints (often implicit in minimal hosting) |
| CORS | `UseCors` | Allow browser cross-origin calls |
| Authentication | `UseAuthentication` | Who is the user? |
| Authorization | `UseAuthorization` | Is user allowed? |
| Rate limiting | `UseRateLimiter` | Throttle abuse (modern .NET) |
| Controllers / endpoints | `MapControllers` / `MapGet` | Your API surface |
| Swagger | `UseSwagger` / `UseSwaggerUI` | API docs UI (dev) |

### Routing note (modern templates)
In modern minimal hosting, routing integration is simplified. You still must place **auth middleware in the correct relative order** with endpoints.

Common recommended shape for APIs with auth:
```csharp
app.UseHttpsRedirection();
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();
```

---

## 5. Execution Order and Why It Matters

**Order of `Use...` calls = order of pipeline.**

### Example bug
```csharp
// ❌ Authorization before Authentication
app.UseAuthorization();
app.UseAuthentication();
```
Authorization may run without a user being set.

### Correct relationship
```csharp
app.UseAuthentication(); // sets HttpContext.User
app.UseAuthorization();  // checks policies/roles against User
app.MapControllers();
```

### Exception handler should be early
```csharp
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/error");
}
// other middleware...
```
Outer exception middleware can catch errors from inner components.

### CORS and auth ordering
Browser preflight + authenticated APIs need careful CORS placement (usually before auth). Follow current ASP.NET Core guidance when enabling CORS for SPA frontends.

### Golden rule
```
Write pipeline order intentionally.
Never randomly insert UseX() at the bottom "because it compiles".
```

---

## 6. Creating Custom Middleware

### Class-based middleware (preferred for real code)
```csharp
public class RequestTimingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestTimingMiddleware> _logger;

    public RequestTimingMiddleware(RequestDelegate next, ILogger<RequestTimingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        var sw = System.Diagnostics.Stopwatch.StartNew();

        // before endpoint
        await _next(context);
        // after endpoint

        sw.Stop();
        _logger.LogInformation(
            "HTTP {Method} {Path} responded {StatusCode} in {Elapsed} ms",
            context.Request.Method,
            context.Request.Path,
            context.Response.StatusCode,
            sw.ElapsedMilliseconds);
    }
}

public static class RequestTimingMiddlewareExtensions
{
    public static IApplicationBuilder UseRequestTiming(this IApplicationBuilder app)
        => app.UseMiddleware<RequestTimingMiddleware>();
}
```

### Register in pipeline
```csharp
app.UseRequestTiming();
```

### Constructor injection rules
- Middleware is usually constructed as singleton-like by the pipeline  
- Inject **singleton-safe** services in middleware constructor  
- Inject **scoped** services via `InvokeAsync` method parameters  

```csharp
public async Task InvokeAsync(HttpContext context, IProductService products)
{
    // products can be scoped — resolved per request
    await _next(context);
}
```

---

## 7. Inline Middleware with `Use`

Great for learning and tiny experiments:

```csharp
app.Use(async (context, next) =>
{
    // Code before next middleware/endpoint
    context.Response.Headers["X-Correlation-Id"] =
        Guid.NewGuid().ToString("N");

    await next();

    // Code after
});
```

For production features, prefer a named class + extension method (testable, discoverable).

---

## 8. Short-Circuiting the Pipeline

Not calling `next` stops the rest of the pipeline — including the controller.

```csharp
app.Use(async (context, next) =>
{
    if (context.Request.Path.StartsWithSegments("/blocked"))
    {
        context.Response.StatusCode = StatusCodes.Status403Forbidden;
        await context.Response.WriteAsync("Blocked by middleware");
        return; // short-circuit — do not call next
    }

    await next();
});
```

### When short-circuiting is correct
- Reject unauthenticated calls early (auth middleware patterns)  
- Health/maintenance lockout  
- Invalid host filtering  

### When not to reinvent
Prefer built-in Authentication/Authorization middleware rather than hand-rolling security gates everywhere.

---

## 9. Exception Handling Middleware

Unhandled exceptions should become controlled API responses — not crash the process randomly for each request.

### Developer-friendly (dev only)
```csharp
if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
}
```

### Production-style API pattern (concept)
```csharp
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler();
}

// or custom middleware that catches exceptions and writes ProblemDetails JSON
```

### Custom exception middleware sketch
```csharp
public class ExceptionHandlingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<ExceptionHandlingMiddleware> _logger;

    public ExceptionHandlingMiddleware(RequestDelegate next, ILogger<ExceptionHandlingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await _next(context);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unhandled exception");
            context.Response.StatusCode = StatusCodes.Status500InternalServerError;
            context.Response.ContentType = "application/problem+json";
            await context.Response.WriteAsJsonAsync(new
            {
                type = "https://httpstatuses.com/500",
                title = "An unexpected error occurred",
                status = 500,
                traceId = context.TraceIdentifier
            });
        }
    }
}
```

Place it **early** in the pipeline so it wraps nearly everything.

---

## 10. Request Timing / Logging Example

End-to-end teaching pipeline:

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddControllers();
builder.Services.AddShopApplication(); // your DI extension

var app = builder.Build();

app.UseMiddleware<ExceptionHandlingMiddleware>();
app.UseRequestTiming();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();
app.Run();
```

### What a single GET looks like
```
Request timing: start stopwatch
  Exception middleware: try
    HTTPS middleware
      Authorization
        ProductsController.GetById
      Authorization end
    HTTPS end
  catch if needed
Request timing: log elapsed + status
```

This is the real shape of production ASP.NET Core apps.

---

## 11. Knowledge Check

**Q1.** What is middleware in one sentence?  
**Q2.** Does middleware only run before the controller, or also after?  
**Q3.** Why must `UseAuthentication` come before `UseAuthorization`?  
**Q4.** How do you short-circuit the pipeline?  
**Q5.** Why should exception handling middleware be early?  
**Q6.** How should a middleware receive a **scoped** service safely?  
**Q7.** Name three built-in middleware components common in APIs.

### Mini practice
1. Create `RequestTimingMiddleware` and log method, path, status, ms  
2. Create `CorrelationIdMiddleware` that assigns `X-Correlation-Id` if missing  
3. Register both in `Program.cs` in a sensible order  
4. Hit an endpoint and confirm headers/logs  
5. Throw an exception in a controller and catch it with exception middleware returning JSON  

### Answers (short)
1. A pipeline component that processes HTTP requests/responses and calls next  
2. Both — before calling next and after it returns  
3. AuthZ needs identity established by AuthN  
4. Handle response and do not call `next`  
5. So it can catch exceptions from later middleware/endpoints  
6. Inject via `InvokeAsync` parameter, not constructor  
7. HTTPS redirection, authentication, authorization, routing, exception handler, swagger…  

---

## ✅ What You Should Feel Confident About

- [ ] Draw the request pipeline in/out flow  
- [ ] Order common middleware correctly  
- [ ] Write class-based custom middleware  
- [ ] Short-circuit intentionally  
- [ ] Add request timing/logging middleware  
- [ ] Place exception handling where it can actually catch errors  

**Previous:** [04-dependency-injection.md](./04-dependency-injection.md)  
**Next:** [06-configuration-and-options.md](./06-configuration-and-options.md) — appsettings, environments, and the Options pattern.
