# Day 3 — Filters & Global Exception Handling

> **Goal:** Understand ASP.NET Core filters (Action, Result, Exception, Authorization), how they fit alongside middleware, and how to implement robust global error handling.

**Prerequisites:** [Day 1](./Day-01-Middleware-Pipeline.md), [Day 2](./Day-02-Dependency-Injection.md)

---

## 📑 Table of Contents

1. [What are Filters?](#1-what-are-filters)
2. [Filter Types & Execution Order](#2-filter-types--execution-order)
3. [Filters vs Middleware](#3-filters-vs-middleware)
4. [Action Filters](#4-action-filters)
5. [Result Filters](#5-result-filters)
6. [Exception Filters](#6-exception-filters)
7. [Authorization Filters](#7-authorization-filters)
8. [Registering Filters (Local, Controller, Global)](#8-registering-filters-local-controller-global)
9. [Global Exception Handling](#9-global-exception-handling)
10. [ProblemDetails — RFC 7807 Errors](#10-problemdetails--rfc-7807-errors)
11. [Key Takeaways & Exercises](#11-key-takeaways--exercises)

---

## 1. What are Filters?

**Filters** run inside the MVC pipeline — **after** routing has picked a controller/action. They let you run code at specific points around action execution.

```
Middleware → Routing → [Filters] → Action → [Filters] → Result → [Filters] → Response
```

Use filters when you need to run logic that:
- Only makes sense **for controllers/actions** (e.g., model validation)
- Needs access to **action parameters** or the **result object**
- Should not run for static files, health checks, etc.

---

## 2. Filter Types & Execution Order

ASP.NET Core has **5 filter types** — each hooks into a specific stage:

```
┌──────────────────────────────────────────────────────────┐
│ 1. Authorization Filters    — Is the user allowed in?   │
│ 2. Resource Filters         — Surround model binding    │
│ 3. Action Filters           — Around the action method  │
│ 4. Exception Filters        — Handle unhandled errors   │
│ 5. Result Filters           — Around result execution   │
└──────────────────────────────────────────────────────────┘
```

### Order of execution (for a single request)
```
Authorization  → Resource (before)
                    ↓
                Model binding
                    ↓
                Action (before)
                    ↓
                [ACTION METHOD RUNS]
                    ↓
                Action (after)
                    ↓
                Result (before)
                    ↓
                [RESULT EXECUTES — writes response]
                    ↓
                Result (after)
                    ↓
                Resource (after)

If any exception is thrown → Exception filters run
```

---

## 3. Filters vs Middleware

This is a common iv question.

| Aspect | Middleware | Filter |
|--------|------------|--------|
| Runs on | **All requests** | MVC actions only |
| Knows about | `HttpContext` | `ActionContext` (action, parameters, result) |
| Can short-circuit | ✅ | ✅ |
| DI support | ✅ | ✅ (via `ServiceFilter` / `TypeFilter`) |
| Typical uses | Logging, auth, CORS, compression | Model validation, caching action results, auditing |

**Rule of thumb:** If the concern is HTTP-level → middleware. If it's controller-level → filter.

---

## 4. Action Filters

Wrap code around an action method execution.

### Sync version
```csharp
public class LogActionFilter : IActionFilter
{
    private readonly ILogger<LogActionFilter> _logger;
    public LogActionFilter(ILogger<LogActionFilter> logger) => _logger = logger;

    public void OnActionExecuting(ActionExecutingContext ctx)
    {
        _logger.LogInformation("→ Action {Name} with args: {@Args}",
            ctx.ActionDescriptor.DisplayName, ctx.ActionArguments);
    }

    public void OnActionExecuted(ActionExecutedContext ctx)
    {
        _logger.LogInformation("← Action completed, Exception? {Ex}",
            ctx.Exception?.Message ?? "none");
    }
}
```

### Async version (preferred)
```csharp
public class LogActionFilter : IAsyncActionFilter
{
    public async Task OnActionExecutionAsync(
        ActionExecutingContext ctx, ActionExecutionDelegate next)
    {
        // before action
        var executed = await next();     // 👈 runs the action
        // after action
    }
}
```

### Real-world: Model Validation Filter
```csharp
public class ValidateModelFilter : IActionFilter
{
    public void OnActionExecuting(ActionExecutingContext ctx)
    {
        if (!ctx.ModelState.IsValid)
        {
            ctx.Result = new BadRequestObjectResult(ctx.ModelState);
            // setting Result short-circuits the action
        }
    }

    public void OnActionExecuted(ActionExecutedContext ctx) { }
}
```

### Short-circuit Pattern
Setting `ctx.Result` **before** calling `next` prevents the action from running. The pipeline jumps straight to result filters.

---

## 5. Result Filters

Wrap code around **result execution** — the step that writes the response body.

```csharp
public class AddHeaderResultFilter : IAsyncResultFilter
{
    public async Task OnResultExecutionAsync(
        ResultExecutingContext ctx, ResultExecutionDelegate next)
    {
        ctx.HttpContext.Response.Headers["X-Produced-By"] = "VendorDirectory";
        await next();
    }
}
```

Use cases:
- Add custom headers
- Transform a result (e.g., wrap in an envelope `{ data, meta }`)
- Log only the final status code after serialization

---

## 6. Exception Filters

Run only when an **unhandled exception** is thrown during action or result execution.

```csharp
public class VendorExceptionFilter : IAsyncExceptionFilter
{
    private readonly ILogger<VendorExceptionFilter> _logger;
    public VendorExceptionFilter(ILogger<VendorExceptionFilter> logger) => _logger = logger;

    public Task OnExceptionAsync(ExceptionContext ctx)
    {
        _logger.LogError(ctx.Exception, "Unhandled error in {Action}",
            ctx.ActionDescriptor.DisplayName);

        ctx.Result = ctx.Exception switch
        {
            KeyNotFoundException =>
                new NotFoundObjectResult(new { error = ctx.Exception.Message }),

            ArgumentException =>
                new BadRequestObjectResult(new { error = ctx.Exception.Message }),

            UnauthorizedAccessException =>
                new ObjectResult(new { error = "Unauthorized" }) { StatusCode = 401 },

            _ =>
                new ObjectResult(new { error = "Unexpected error" }) { StatusCode = 500 }
        };

        ctx.ExceptionHandled = true;   // stop propagation
        return Task.CompletedTask;
    }
}
```

> ⚠️ Exception filters only catch exceptions from **inside the MVC pipeline**. Middleware exceptions are NOT caught by exception filters — use `UseExceptionHandler` or `IExceptionHandler` for that.

---

## 7. Authorization Filters

The earliest filter type. Usually you don't write these yourself — the built-in `[Authorize]` attribute covers 99% of cases. (Day 4 has the deep dive.)

Example of a custom one:
```csharp
public class ApiKeyAuthFilter : IAuthorizationFilter
{
    public void OnAuthorization(AuthorizationFilterContext ctx)
    {
        var key = ctx.HttpContext.Request.Headers["X-Api-Key"].ToString();
        if (key != "secret-123")
            ctx.Result = new UnauthorizedResult();
    }
}
```

---

## 8. Registering Filters (Local, Controller, Global)

You have three scopes.

### Local — per action
```csharp
[ServiceFilter(typeof(LogActionFilter))]
[HttpGet("{id}")]
public IActionResult Get(int id) => Ok(svc.Get(id));
```

### Per-controller
```csharp
[ServiceFilter(typeof(LogActionFilter))]
public class VendorsController : ControllerBase { ... }
```

### Global — every action in the app
```csharp
builder.Services.AddControllers(options =>
{
    options.Filters.Add<LogActionFilter>();
    options.Filters.Add<VendorExceptionFilter>();
    options.Filters.Add<AddHeaderResultFilter>();
});
```

### `ServiceFilter` vs `TypeFilter` vs `[Attribute]`
| Approach | When to use |
|----------|-------------|
| `[ServiceFilter(typeof(T))]` | Filter is registered in DI (Scoped/Transient) — **preferred** |
| `[TypeFilter(typeof(T))]` | Auto-instantiated per action; use if not in DI |
| `[MyFilterAttribute]` | Pure attribute, no DI (limited) |

### Registering filters in DI
```csharp
builder.Services.AddScoped<LogActionFilter>();
builder.Services.AddScoped<VendorExceptionFilter>();
```

---

## 9. Global Exception Handling

Exception **filters** only catch MVC-layer errors. For a truly global safety net covering middleware, minimal APIs, and controllers, use one of these two approaches.

### Option A — `UseExceptionHandler` middleware (classic)

```csharp
var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler(errorApp =>
    {
        errorApp.Run(async context =>
        {
            var feature = context.Features.Get<IExceptionHandlerFeature>();
            var ex = feature?.Error;

            var (status, title) = ex switch
            {
                KeyNotFoundException        => (404, "Not Found"),
                ArgumentException           => (400, "Bad Request"),
                UnauthorizedAccessException => (401, "Unauthorized"),
                _                           => (500, "Unexpected Error")
            };

            context.Response.StatusCode  = status;
            context.Response.ContentType = "application/problem+json";

            await context.Response.WriteAsJsonAsync(new ProblemDetails
            {
                Status = status,
                Title  = title,
                Detail = ex?.Message,
                Instance = context.Request.Path
            });
        });
    });
}
```

Register this **first** in the middleware pipeline so it surrounds everything after it.

### Option B — `IExceptionHandler` (.NET 8+, recommended)

Cleaner, testable, DI-friendly.

```csharp
public class GlobalExceptionHandler(ILogger<GlobalExceptionHandler> logger)
    : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(
        HttpContext httpContext,
        Exception exception,
        CancellationToken cancellationToken)
    {
        logger.LogError(exception, "Unhandled: {Message}", exception.Message);

        var (status, title) = exception switch
        {
            KeyNotFoundException        => (StatusCodes.Status404NotFound, "Not Found"),
            ArgumentException           => (StatusCodes.Status400BadRequest, "Bad Request"),
            UnauthorizedAccessException => (StatusCodes.Status401Unauthorized, "Unauthorized"),
            _                           => (StatusCodes.Status500InternalServerError, "Unexpected Error")
        };

        var problem = new ProblemDetails
        {
            Status   = status,
            Title    = title,
            Detail   = exception.Message,
            Instance = httpContext.Request.Path,
            Type     = $"https://httpstatuses.io/{status}"
        };

        httpContext.Response.StatusCode  = status;
        httpContext.Response.ContentType = "application/problem+json";

        await httpContext.Response.WriteAsJsonAsync(problem, cancellationToken);
        return true;    // handled — pipeline stops
    }
}
```

Register it:
```csharp
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();
builder.Services.AddProblemDetails();

var app = builder.Build();
app.UseExceptionHandler();     // no argument — picks up registered handlers
```

You can register **multiple** handlers; the first to return `true` wins.

```csharp
builder.Services.AddExceptionHandler<ValidationExceptionHandler>();
builder.Services.AddExceptionHandler<NotFoundExceptionHandler>();
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();   // fallback
```

### Which should I pick?

| Scenario | Recommendation |
|----------|----------------|
| .NET 8 or 9 | `IExceptionHandler` |
| Need per-exception-type classes | `IExceptionHandler` (multiple) |
| Need a catch-all at the middleware edge | `UseExceptionHandler` delegate |
| Only MVC actions, no middleware errors | Exception **filter** |

---

## 10. ProblemDetails — RFC 7807 Errors

`ProblemDetails` is the **standard** JSON shape for API errors (RFC 7807).

```json
{
  "type":     "https://httpstatuses.io/404",
  "title":    "Not Found",
  "status":   404,
  "detail":   "Vendor with id 42 was not found.",
  "instance": "/api/vendors/42"
}
```

### Enable automatically on non-2xx responses
```csharp
builder.Services.AddProblemDetails(options =>
{
    options.CustomizeProblemDetails = ctx =>
    {
        ctx.ProblemDetails.Extensions["traceId"] =
            Activity.Current?.Id ?? ctx.HttpContext.TraceIdentifier;
        ctx.ProblemDetails.Extensions["machine"] = Environment.MachineName;
    };
});
```

Now every 4xx/5xx response (including 404s from unknown routes when `UseStatusCodePages` is enabled) serializes as ProblemDetails.

### Validation Problem
Automatic model-state errors already use `ValidationProblemDetails`:
```json
{
  "type":   "https://tools.ietf.org/html/rfc7231#section-6.5.1",
  "title":  "One or more validation errors occurred.",
  "status": 400,
  "errors": {
    "Name":   ["The Name field is required."],
    "Rating": ["Rating must be between 0 and 5."]
  }
}
```

---

## 11. Key Takeaways & Exercises

### 🎯 Summary Table
| Concept | Remember |
|---------|----------|
| **Filter types** | Authorization → Resource → Action → Exception → Result |
| **Filters vs Middleware** | Filters know the action; middleware only knows `HttpContext` |
| **Action filter** | Wrap before/after action; short-circuit by setting `ctx.Result` |
| **Result filter** | Wrap response writing — good for headers, envelopes |
| **Exception filter** | Catches MVC-only errors; not middleware errors |
| **`IExceptionHandler`** | .NET 8+ — preferred global handler, multiple chainable |
| **`UseExceptionHandler`** | Middleware-based catch-all (works for non-MVC too) |
| **`ProblemDetails`** | RFC 7807 — standard JSON shape for errors |
| **Registration** | `[ServiceFilter]` per action/controller, or `options.Filters.Add<T>()` globally |

### Exercises

**Exercise 1 — Audit Action Filter**
Write an `AuditActionFilter` that logs `User`, `Action`, `Args`, and elapsed time. Register it globally. Hit `/api/vendors` and check logs.

<details>
<summary>💡 Hint</summary>

```csharp
public class AuditActionFilter : IAsyncActionFilter
{
    public async Task OnActionExecutionAsync(
        ActionExecutingContext ctx, ActionExecutionDelegate next)
    {
        var sw = Stopwatch.StartNew();
        var executed = await next();
        sw.Stop();
        // log ctx.HttpContext.User.Identity?.Name, action name, sw.ElapsedMilliseconds
    }
}
```
</details>

**Exercise 2 — Envelope Result Filter**
Build a `ResponseEnvelopeFilter` that wraps every `ObjectResult` payload in `{ success, data, timestamp }`.

**Exercise 3 — Multiple Exception Handlers**
Register two `IExceptionHandler`s:
- `ValidationExceptionHandler` — handles only `FluentValidation.ValidationException`
- `GlobalExceptionHandler` — fallback for everything else

Verify the validation one runs first by throwing a `ValidationException` from a controller.

**Exercise 4 — Vendor Not Found**
In `VendorsController.Get(int id)`, throw `new KeyNotFoundException($"Vendor {id} missing")` when not found. Confirm the global handler returns:
```json
{ "status": 404, "title": "Not Found", "detail": "Vendor 42 missing" }
```

**Exercise 5 — Middleware vs Filter**
Throw an exception from inside a custom middleware **and** from inside a controller action. Observe:
- The MVC exception filter only catches the controller one.
- `IExceptionHandler` / `UseExceptionHandler` catches both.

---

## ➡️ Next: [Day 4 — JWT Authentication & Role Authorization](./Day-04-JWT-Authentication-Role-Authorization.md)

Tomorrow you'll learn:
- How JWT tokens work (header.payload.signature)
- `AddAuthentication` + `AddJwtBearer` setup
- Issuing tokens on login
- `[Authorize]`, `[Authorize(Roles = "Admin")]`, and policy-based authorization


