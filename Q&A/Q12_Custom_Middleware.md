# Question 12: What is custom middleware? Explain in detail with a use case.

## Answer

### What is Custom Middleware?

**Custom middleware** is middleware that you create yourself to handle specific cross-cutting concerns in your application. Unlike built-in middleware (like UseAuthentication, UseCors), you write custom middleware when you have unique requirements.

---

## Structure of Custom Middleware

### Basic Template

```csharp
public class MyCustomMiddleware
{
    private readonly RequestDelegate _next;
    
    // Constructor - receives the next middleware in the pipeline
    public MyCustomMiddleware(RequestDelegate next)
    {
        _next = next;
    }
    
    // InvokeAsync or Invoke - must be present
    public async Task InvokeAsync(HttpContext context)
    {
        // Code BEFORE calling next middleware
        // (executes on the way IN)
        
        await _next(context); // Call next middleware
        
        // Code AFTER next middleware returns
        // (executes on the way OUT)
    }
}
```

### Extension Method for Registration

```csharp
public static class MyCustomMiddlewareExtensions
{
    public static IApplicationBuilder UseMyCustomMiddleware(
        this IApplicationBuilder builder)
    {
        return builder.UseMiddleware<MyCustomMiddleware>();
    }
}
```

### Registration in Startup.cs

```csharp
public void Configure(IApplicationBuilder app)
{
    app.UseMyCustomMiddleware(); // Use our custom middleware
    
    app.UseRouting();
    app.UseEndpoints(endpoints => endpoints.MapControllers());
}
```

---

## Real-World Use Case 1: API Key Authentication Middleware

### Scenario
You want to protect your API with an API key that clients must send in the request header.

### Implementation

```csharp
public class ApiKeyAuthenticationMiddleware
{
    private readonly RequestDelegate _next;
    private readonly IConfiguration _configuration;
    private const string API_KEY_HEADER = "X-API-Key";
    
    public ApiKeyAuthenticationMiddleware(
        RequestDelegate next, 
        IConfiguration configuration)
    {
        _next = next;
        _configuration = configuration;
    }
    
    public async Task InvokeAsync(HttpContext context)
    {
        // Check if API key is present in header
        if (!context.Request.Headers.TryGetValue(API_KEY_HEADER, out var receivedApiKey))
        {
            context.Response.StatusCode = 401; // Unauthorized
            await context.Response.WriteAsync("API Key is missing");
            return; // Short-circuit - don't call next middleware
        }
        
        // Validate API key
        var validApiKey = _configuration["ApiKey"];
        if (!receivedApiKey.Equals(validApiKey))
        {
            context.Response.StatusCode = 401; // Unauthorized
            await context.Response.WriteAsync("Invalid API Key");
            return; // Short-circuit
        }
        
        // API key is valid - continue to next middleware
        await _next(context);
    }
}

// Extension method
public static class ApiKeyAuthenticationMiddlewareExtensions
{
    public static IApplicationBuilder UseApiKeyAuthentication(
        this IApplicationBuilder builder)
    {
        return builder.UseMiddleware<ApiKeyAuthenticationMiddleware>();
    }
}

// In appsettings.json
{
  "ApiKey": "MySecretApiKey123456"
}

// In Startup.cs
public void Configure(IApplicationBuilder app)
{
    app.UseApiKeyAuthentication(); // Apply to all routes
    
    app.UseRouting();
    app.UseEndpoints(endpoints => endpoints.MapControllers());
}
```

**Usage:**
```
// Valid request:
GET /api/products
Headers: X-API-Key: MySecretApiKey123456
Response: 200 OK

// Invalid request:
GET /api/products
Headers: (no API key)
Response: 401 Unauthorized - "API Key is missing"
```

---

## Real-World Use Case 2: Request Timing/Performance Monitoring Middleware

### Scenario
You want to measure how long each request takes and log slow requests for performance monitoring.

### Implementation

```csharp
public class PerformanceMonitoringMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<PerformanceMonitoringMiddleware> _logger;
    private const int SLOW_REQUEST_THRESHOLD_MS = 1000; // 1 second
    
    public PerformanceMonitoringMiddleware(
        RequestDelegate next, 
        ILogger<PerformanceMonitoringMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }
    
    public async Task InvokeAsync(HttpContext context)
    {
        var stopwatch = System.Diagnostics.Stopwatch.StartNew();
        var requestPath = context.Request.Path;
        var requestMethod = context.Request.Method;
        
        try
        {
            // Call next middleware
            await _next(context);
        }
        finally
        {
            stopwatch.Stop();
            var elapsedMs = stopwatch.ElapsedMilliseconds;
            
            if (elapsedMs > SLOW_REQUEST_THRESHOLD_MS)
            {
                _logger.LogWarning(
                    "SLOW REQUEST: {Method} {Path} took {ElapsedMs}ms - Status: {StatusCode}",
                    requestMethod,
                    requestPath,
                    elapsedMs,
                    context.Response.StatusCode);
            }
            else
            {
                _logger.LogInformation(
                    "{Method} {Path} took {ElapsedMs}ms - Status: {StatusCode}",
                    requestMethod,
                    requestPath,
                    elapsedMs,
                    context.Response.StatusCode);
            }
        }
    }
}

// Extension method
public static class PerformanceMonitoringMiddlewareExtensions
{
    public static IApplicationBuilder UsePerformanceMonitoring(
        this IApplicationBuilder builder)
    {
        return builder.UseMiddleware<PerformanceMonitoringMiddleware>();
    }
}

// In Startup.cs
public void Configure(IApplicationBuilder app)
{
    app.UsePerformanceMonitoring(); // First in pipeline
    
    app.UseRouting();
    app.UseAuthentication();
    app.UseAuthorization();
    app.UseEndpoints(endpoints => endpoints.MapControllers());
}
```

**Output:**
```
[INFO] GET /api/products took 234ms - Status: 200
[INFO] POST /api/orders took 456ms - Status: 201
[WARNING] SLOW REQUEST: GET /api/reports took 2345ms - Status: 200
```

---

## Real-World Use Case 3: Request/Response Logging Middleware

### Scenario
Log all incoming requests and outgoing responses for debugging and audit trails.

```csharp
public class RequestResponseLoggingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestResponseLoggingMiddleware> _logger;
    
    public RequestResponseLoggingMiddleware(
        RequestDelegate next,
        ILogger<RequestResponseLoggingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }
    
    public async Task InvokeAsync(HttpContext context)
    {
        // Log incoming request
        await LogRequest(context);
        
        // Capture original response body stream
        var originalBodyStream = context.Response.Body;
        
        using var responseBody = new MemoryStream();
        context.Response.Body = responseBody;
        
        // Execute the rest of the pipeline
        await _next(context);
        
        // Log outgoing response
        await LogResponse(context);
        
        // Copy response to original stream
        await responseBody.CopyToAsync(originalBodyStream);
    }
    
    private async Task LogRequest(HttpContext context)
    {
        context.Request.EnableBuffering(); // Allow reading body multiple times
        
        var requestInfo = new
        {
            Timestamp = DateTime.UtcNow,
            Method = context.Request.Method,
            Path = context.Request.Path,
            QueryString = context.Request.QueryString.ToString(),
            Headers = context.Request.Headers
                .Where(h => !h.Key.Equals("Authorization", StringComparison.OrdinalIgnoreCase))
                .ToDictionary(h => h.Key, h => h.Value.ToString()),
            Body = await ReadBodyAsync(context.Request.Body)
        };
        
        _logger.LogInformation("Incoming Request: {@RequestInfo}", requestInfo);
        
        context.Request.Body.Position = 0; // Reset for next middleware
    }
    
    private async Task LogResponse(HttpContext context)
    {
        context.Response.Body.Seek(0, SeekOrigin.Begin);
        var responseBody = await new StreamReader(context.Response.Body).ReadToEndAsync();
        context.Response.Body.Seek(0, SeekOrigin.Begin);
        
        var responseInfo = new
        {
            Timestamp = DateTime.UtcNow,
            StatusCode = context.Response.StatusCode,
            Headers = context.Response.Headers.ToDictionary(h => h.Key, h => h.Value.ToString()),
            Body = responseBody
        };
        
        _logger.LogInformation("Outgoing Response: {@ResponseInfo}", responseInfo);
    }
    
    private async Task<string> ReadBodyAsync(Stream body)
    {
        using var reader = new StreamReader(body, leaveOpen: true);
        var bodyText = await reader.ReadToEndAsync();
        body.Position = 0;
        return bodyText;
    }
}
```

---

## Real-World Use Case 4: Global Exception Handling Middleware

### Scenario
Catch all unhandled exceptions and return consistent error responses.

```csharp
public class GlobalExceptionHandlingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<GlobalExceptionHandlingMiddleware> _logger;
    
    public GlobalExceptionHandlingMiddleware(
        RequestDelegate next,
        ILogger<GlobalExceptionHandlingMiddleware> logger)
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
            _logger.LogError(ex, "An unhandled exception occurred");
            await HandleExceptionAsync(context, ex);
        }
    }
    
    private static async Task HandleExceptionAsync(HttpContext context, Exception exception)
    {
        context.Response.ContentType = "application/json";
        
        var (statusCode, message) = exception switch
        {
            NotFoundException => (StatusCodes.Status404NotFound, exception.Message),
            UnauthorizedAccessException => (StatusCodes.Status401Unauthorized, "Unauthorized"),
            ArgumentException => (StatusCodes.Status400BadRequest, exception.Message),
            _ => (StatusCodes.Status500InternalServerError, "An internal server error occurred")
        };
        
        context.Response.StatusCode = statusCode;
        
        var response = new
        {
            StatusCode = statusCode,
            Message = message,
            Timestamp = DateTime.UtcNow
        };
        
        await context.Response.WriteAsJsonAsync(response);
    }
}

// Custom exception
public class NotFoundException : Exception
{
    public NotFoundException(string message) : base(message) { }
}
```

**Usage in Controller:**
```csharp
[HttpGet("{id}")]
public IActionResult GetProduct(int id)
{
    var product = _repository.GetById(id);
    if (product == null)
    {
        throw new NotFoundException($"Product with ID {id} not found");
    }
    return Ok(product);
}

// Response (automatically handled by middleware):
// Status: 404 Not Found
// {
//   "statusCode": 404,
//   "message": "Product with ID 5 not found",
//   "timestamp": "2026-05-26T10:30:00Z"
// }
```

---

## Advanced: Conditional Middleware

Apply middleware only to specific routes:

```csharp
public void Configure(IApplicationBuilder app)
{
    // Apply only to /api/* routes
    app.UseWhen(context => context.Request.Path.StartsWithSegments("/api"), 
        appBuilder =>
        {
            appBuilder.UseApiKeyAuthentication();
            appBuilder.UsePerformanceMonitoring();
        });
    
    app.UseRouting();
    app.UseEndpoints(endpoints => endpoints.MapControllers());
}
```

---

## Summary

**Custom Middleware = Your own request/response processing logic**

**Common Use Cases:**
1. ✅ Custom authentication (API keys, tokens)
2. ✅ Performance monitoring
3. ✅ Request/response logging
4. ✅ Global exception handling
5. ✅ Rate limiting
6. ✅ Request validation
7. ✅ Custom headers injection

**Key Takeaways:**
- Must have `InvokeAsync` or `Invoke` method
- Receives `RequestDelegate next` in constructor
- Can short-circuit pipeline by not calling `next()`
- Can inject services via constructor
- Order matters - register carefully in `Configure()`

Custom middleware keeps cross-cutting concerns clean and reusable!
