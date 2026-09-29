# 🚨 Error Handling — Consistent Failures, Safe Logs, Problem Details

> **Trainer's Note:** Happy paths are easy. Production reputation is won on **bad days**: clear errors for clients, rich logs for you, zero secret leakage. Centralize exception handling and standardize on **RFC 7807 Problem Details**.

---

## 📑 Table of Contents
1. [Why Global Error Handling?](#1-why-global-error-handling)
2. [RFC 7807 Problem Details](#2-rfc-7807-problem-details)
3. [Built-in ASP.NET Core Support](#3-built-in-aspnet-core-support)
4. [IExceptionHandler (Modern Approach)](#4-iexceptionhandler-modern-approach)
5. [Custom Exception Middleware](#5-custom-exception-middleware)
6. [Domain Exceptions vs Unknown Errors](#6-domain-exceptions-vs-unknown-errors)
7. [Not Found, Validation, Conflict](#7-not-found-validation-conflict)
8. [Secure Logging Practices](#8-secure-logging-practices)
9. [What Clients Should Receive](#9-what-clients-should-receive)
10. [End-to-End Wiring](#10-end-to-end-wiring)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. Why Global Error Handling?

Without a central strategy:

```
Controller A → try/catch → random JSON
Controller B → throws → yellow stack page / bare 500
Service C → returns null → mystery 204
```

With a central strategy:

```
Any unhandled exception
        │
        ▼
 Exception handler / middleware
        │
        ├── log safe details + correlation id
        └── return consistent Problem Details JSON
```

| Goal | Result |
|------|--------|
| Consistency | All errors look alike |
| Security | No stack traces to strangers |
| Operability | Logs have what engineers need |
| Client UX | Machine-readable `type/title/status/detail` |

---

## 2. RFC 7807 Problem Details

**Problem Details** is a standard JSON error shape for HTTP APIs.

```json
{
  "type": "https://httpstatuses.tr/404",
  "title": "Not Found",
  "status": 404,
  "detail": "Product 42 was not found.",
  "instance": "/api/products/42",
  "traceId": "00-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-bbbbbbbbbbbbbbbb-00"
}
```

| Field | Meaning |
|-------|---------|
| `type` | URI identifying the problem kind |
| `title` | Short human summary |
| `status` | HTTP status code |
| `detail` | Occurrence-specific explanation (safe) |
| `instance` | This request path/occurrence |
| extensions | e.g. `traceId`, `errors` for validation |

Content-Type is often:
```
application/problem+json
```

ASP.NET Core types: `ProblemDetails`, `ValidationProblemDetails`.

---

## 3. Built-in ASP.NET Core Support

### Controller helpers
```csharp
return NotFound();                 // 404 problem (with ApiBehavior)
return ValidationProblem(ModelState); // 400 validation problem
return Problem(
    detail: "Inventory service unavailable",
    statusCode: StatusCodes.Status503ServiceUnavailable,
    title: "Dependency failure");
```

### Developer exception page (DEV ONLY)
```csharp
if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
}
```
Never enable full stack pages for anonymous production users.

### Exception handler pipeline
```csharp
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler(); // or with path / custom handler
}
```

Modern .NET prefers `IExceptionHandler` registration (next section).

---

## 4. IExceptionHandler (Modern Approach)

```csharp
public class GlobalExceptionHandler : IExceptionHandler
{
    private readonly ILogger<GlobalExceptionHandler> _logger;
    private readonly IHostEnvironment _env;

    public GlobalExceptionHandler(
        ILogger<GlobalExceptionHandler> logger,
        IHostEnvironment env)
    {
        _logger = logger;
        _env = env;
    }

    public async ValueTask<bool> TryHandleAsync(
        HttpContext httpContext,
        Exception exception,
        CancellationToken cancellationToken)
    {
        var (status, title, detail) = Map(exception);

        _logger.LogError(exception,
            "Request {Method} {Path} failed with {StatusCode}",
            httpContext.Request.Method,
            httpContext.Request.Path,
            status);

        var problem = new ProblemDetails
        {
            Status = status,
            Title = title,
            Detail = detail,
            Instance = httpContext.Request.Path,
            Type = $"https://httpstatuses.com/{status}"
        };

        problem.Extensions["traceId"] = httpContext.TraceIdentifier;

        // Optional: more detail only in Development
        if (_env.IsDevelopment())
            problem.Extensions["exception"] = exception.GetType().Name;

        httpContext.Response.StatusCode = status;
        httpContext.Response.ContentType = "application/problem+json";
        await httpContext.Response.WriteAsJsonAsync(problem, cancellationToken);
        return true; // handled
    }

    private static (int status, string title, string detail) Map(Exception ex) => ex switch
    {
        NotFoundException nf => (StatusCodes.Status404NotFound, "Not Found", nf.Message),
        ValidationException ve => (StatusCodes.Status400BadRequest, "Validation failed", ve.Message),
        ConflictException ce => (StatusCodes.Status409Conflict, "Conflict", ce.Message),
        UnauthorizedAccessException => (StatusCodes.Status403Forbidden, "Forbidden", "You are not allowed to perform this action."),
        _ => (StatusCodes.Status500InternalServerError, "Server error",
              "An unexpected error occurred. Please try again later.")
    };
}
```

### Register
```csharp
builder.Services.AddProblemDetails();
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();

var app = builder.Build();
app.UseExceptionHandler();
// ...
app.Run();
```

---

## 5. Custom Exception Middleware

If you prefer classic middleware (works everywhere, easy to teach):

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
            await WriteProblemAsync(context, ex);
        }
    }

    private async Task WriteProblemAsync(HttpContext context, Exception ex)
    {
        var status = ex switch
        {
            NotFoundException => StatusCodes.Status404NotFound,
            ConflictException => StatusCodes.Status409Conflict,
            _ => StatusCodes.Status500InternalServerError
        };

        _logger.LogError(ex, "Unhandled exception for {TraceId}", context.TraceIdentifier);

        context.Response.StatusCode = status;
        context.Response.ContentType = "application/problem+json";

        var problem = new ProblemDetails
        {
            Status = status,
            Title = status == 500 ? "Server error" : ex.GetType().Name,
            Detail = status == 500
                ? "An unexpected error occurred."
                : ex.Message,
            Instance = context.Request.Path
        };
        problem.Extensions["traceId"] = context.TraceIdentifier;

        await context.Response.WriteAsJsonAsync(problem);
    }
}
```

Place **early** in the pipeline so it wraps the rest:

```csharp
app.UseMiddleware<ExceptionHandlingMiddleware>();
```

---

## 6. Domain Exceptions vs Unknown Errors

Create small exception types for expected failures:

```csharp
public class NotFoundException : Exception
{
    public NotFoundException(string message) : base(message) { }
}

public class ConflictException : Exception
{
    public ConflictException(string message) : base(message) { }
}

public class ValidationException : Exception
{
    public ValidationException(string message) : base(message) { }
}
```

### Service usage
```csharp
public async Task<ProductDto> GetAsync(int id, CancellationToken ct)
{
    var product = await _db.Products.AsNoTracking()
        .FirstOrDefaultAsync(p => p.Id == id, ct);

    if (product is null)
        throw new NotFoundException($"Product {id} was not found.");

    return Map(product);
}
```

Controllers stay thin; handler maps exception → status.

```
Expected business miss → typed exception → 404/409/400
Unknown bug           → Exception       → 500 + log stack
```

Don’t throw `Exception` for routine not-found cases.

---

## 7. Not Found, Validation, Conflict

### Not Found — 404
```csharp
var order = await _orders.GetAsync(id, ct);
if (order is null) return NotFound();
// or throw new NotFoundException(...)
```

### Invalid input — 400
Prefer model validation (file 02). For late discovery:

```csharp
return ValidationProblem(new ValidationProblemDetails(new Dictionary<string, string[]>
{
    ["quantity"] = ["Quantity must be greater than zero"]
}));
```

### Concurrency / conflict — 409
Examples:
- Email already registered  
- Order already cancelled  
- EF Core concurrency token mismatch (`DbUpdateConcurrencyException`)  

```csharp
try
{
    await _db.SaveChangesAsync(ct);
}
catch (DbUpdateConcurrencyException)
{
    throw new ConflictException(
        "This record was modified by someone else. Refresh and retry.");
}
```

```csharp
if (await _users.EmailExistsAsync(email, ct))
    throw new ConflictException("Email is already registered.");
```

### Mapping table
| Scenario | Status | Body |
|----------|--------|------|
| Bad DTO fields | 400 | `ValidationProblemDetails` |
| Missing entity | 404 | `ProblemDetails` |
| Duplicate / version clash | 409 | `ProblemDetails` |
| Unauthenticated | 401 | auth challenge/problem |
| Forbidden | 403 | problem/forbid |
| Unhandled bug | 500 | generic problem |

---

## 8. Secure Logging Practices

### Do log
- Exception type + message + **stack** (server logs only)  
- `TraceIdentifier` / correlation id  
- Request method + path  
- User id **if available** (not secrets)  
- Business identifiers (order id) when safe  

### Do NOT log
| Never | Why |
|-------|-----|
| Passwords | Credential leak |
| JWT access tokens / refresh tokens | Session hijack |
| Full credit card / CVV | Compliance nightmare |
| Connection strings | Key material |
| National IDs / health data without controls | PII/PHI |
| Entire request body blindly | May contain secrets |

### Examples
```csharp
// ✅
_logger.LogError(ex, "Failed to place order {OrderId} for user {UserId}", orderId, userId);

// ❌
_logger.LogError("Login failed for password {Password}", password);
_logger.LogError("Token was {Token}", accessToken);
```

### Client vs log detail
```
Client detail:  "An unexpected error occurred. Reference: 00-abc..."
Log detail:     full exception + SQL failure + stack
```

Use the same `traceId` in both so support can find the log line.

### Log levels
| Level | Use |
|-------|-----|
| Information | Normal milestones |
| Warning | Handled anomalies |
| Error | Failures needing attention |
| Critical | System-wide outages |

---

## 9. What Clients Should Receive

| Environment | Client sees |
|-------------|-------------|
| Production | Title, status, safe detail, traceId |
| Development | Optionally exception type / richer detail |

Never return:
```json
{
  "stackTrace": " at Shop.Infrastructure.Sql... password=...",
  "inner": { }
}
```
to public clients.

### Stable error catalog (optional advanced)
Document custom `type` URIs:
```
https://api.shop.local/errors/product-not-found
https://api.shop.local/errors/duplicate-email
```
Clients can branch on `type` when needed.

---

## 10. End-to-End Wiring

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddProblemDetails();
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();
// auth, db, etc.

var app = builder.Build();

app.UseExceptionHandler();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();
app.Run();
```

### Flow
```
Request
  → Exception handler (outer)
     → authz
        → controller
           → service throws NotFoundException
        ←
     ←
  → maps to 404 Problem Details + LogError with stack
Response application/problem+json
```

---

## 11. Knowledge Check

**Q1.** What problem does global error handling solve?  
**Q2.** Name five common Problem Details fields.  
**Q3.** Why hide stack traces from production API clients?  
**Q4.** Which status fits “product id not found”?  
**Q5.** Which status fits “email already registered”?  
**Q6.** What should accompany a 500 in logs vs response body?  
**Q7.** List three things you must never log.

### Mini practice
1. Create `NotFoundException` and `ConflictException`  
2. Implement `IExceptionHandler` or middleware returning `problem+json`  
3. Throw not-found from a service; verify 404 body + traceId  
4. Force an unexpected exception; verify generic 500 detail  
5. Confirm stack is in logs only, not response  
6. Convert a duplicate key case to 409  

### Answers (short)
1. Consistent, safe, operable failure responses  
2. type, title, status, detail, instance (+ extensions)  
3. Info disclosure / security / noise for clients  
4. 404  
5. 409  
6. Logs: full exception; body: generic message + traceId  
7. Passwords, tokens, card data (and similar secrets/PII)  

---

## ✅ What You Should Feel Confident About

- [ ] Return RFC 7807-style problem responses  
- [ ] Implement global exception handling (`IExceptionHandler` or middleware)  
- [ ] Map not found / validation / conflict intentionally  
- [ ] Log exceptions with correlation ids safely  
- [ ] Keep production responses free of stacks and secrets  
- [ ] Use typed domain exceptions for expected failures  

**Previous:** [02-validation.md](./02-validation.md)  
**Next:** [04-api-versioning.md](./04-api-versioning.md) — evolve APIs without breaking clients.
