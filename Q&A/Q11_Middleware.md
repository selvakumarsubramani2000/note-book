# Question 11: What are middleware components in .NET? Explain one you've used.

## Answer

### What is Middleware?

**Middleware** are software components that are assembled into an application pipeline to handle requests and responses. Each middleware component:
- Chooses whether to pass the request to the next component
- Can perform work before and after the next component

Think of middleware as a **chain of components** that process every HTTP request and response.

---

## The Middleware Pipeline

```
HTTP Request
    ↓
┌─────────────────────────────────┐
│  Middleware 1 (e.g., Logging)   │ ─┐
└─────────────────────────────────┘  │
    ↓                                │ Before
┌─────────────────────────────────┐  │
│  Middleware 2 (e.g., Auth)      │ ─┤
└─────────────────────────────────┘  │
    ↓                                │
┌─────────────────────────────────┐  │
│  Middleware 3 (e.g., Routing)   │ ─┘
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  Endpoint (Controller Action)   │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐  ┐
│  Middleware 3                   │ ─┤
└─────────────────────────────────┘  │ After
    ↓                                │ (response)
┌─────────────────────────────────┐  │
│  Middleware 2                   │ ─┤
└─────────────────────────────────┘  │
    ↓                                │
┌─────────────────────────────────┐  │
│  Middleware 1                   │ ─┘
└─────────────────────────────────┘
    ↓
HTTP Response
```

Each middleware can:
1. Execute code **before** calling the next middleware
2. Call the **next** middleware in the pipeline
3. Execute code **after** the next middleware returns

---

## How Middleware is Configured

### In `Startup.cs` (or `Program.cs` in .NET 6+)

```csharp
public class Startup
{
    public void Configure(IApplicationBuilder app)
    {
        // Middleware are executed in the order they are added!
        
        app.UseHttpsRedirection();    // 1. Redirects HTTP to HTTPS
        app.UseStaticFiles();         // 2. Serves static files
        app.UseRouting();             // 3. Routing
        app.UseAuthentication();      // 4. Authentication
        app.UseAuthorization();       // 5. Authorization
        app.UseEndpoints(endpoints => // 6. Endpoints
        {
            endpoints.MapControllers();
        });
    }
}
```

**⚠️ Order Matters!** Middleware are executed in the order they are added.

---

## Built-in Middleware Examples

### 1. **Authentication Middleware** (Most Commonly Used)

**Purpose**: Authenticates users before they access protected resources

**Configuration:**
```csharp
// In ConfigureServices
public void ConfigureServices(IServiceCollection services)
{
    services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
        .AddJwtBearer(options =>
        {
            options.TokenValidationParameters = new TokenValidationParameters
            {
                ValidateIssuer = true,
                ValidateAudience = true,
                ValidateLifetime = true,
                ValidateIssuerSigningKey = true,
                ValidIssuer = Configuration["Jwt:Issuer"],
                ValidAudience = Configuration["Jwt:Audience"],
                IssuerSigningKey = new SymmetricSecurityKey(
                    Encoding.UTF8.GetBytes(Configuration["Jwt:Key"]))
            };
        });
}

// In Configure
public void Configure(IApplicationBuilder app)
{
    app.UseRouting();
    
    app.UseAuthentication(); // Must come before UseAuthorization
    app.UseAuthorization();
    
    app.UseEndpoints(endpoints => endpoints.MapControllers());
}
```

**How it works:**
1. Request comes in with Authorization header: `Bearer eyJhbGciOiJIUzI1...`
2. Authentication middleware validates the JWT token
3. If valid, sets `HttpContext.User` with user claims
4. If invalid, returns 401 Unauthorized
5. Next middleware (Authorization) checks if user has required permissions

**Usage in Controller:**
```csharp
[Authorize] // Requires authentication
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    [HttpGet]
    public IActionResult GetProducts()
    {
        var username = User.Identity.Name; // Set by authentication middleware
        return Ok("Products retrieved");
    }
    
    [Authorize(Roles = "Admin")] // Requires Admin role
    [HttpDelete("{id}")]
    public IActionResult DeleteProduct(int id)
    {
        return Ok("Product deleted");
    }
}
```

---

### 2. **Exception Handling Middleware**

**Purpose**: Catches exceptions globally and returns appropriate error responses

```csharp
public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
{
    if (env.IsDevelopment())
    {
        app.UseDeveloperExceptionPage(); // Detailed error page for dev
    }
    else
    {
        app.UseExceptionHandler("/error"); // Production error handling
    }
    
    // Rest of middleware
    app.UseRouting();
    app.UseEndpoints(endpoints => endpoints.MapControllers());
}
```

**Creating a global error controller:**
```csharp
[ApiController]
public class ErrorController : ControllerBase
{
    [Route("/error")]
    [ApiExplorerSettings(IgnoreApi = true)]
    public IActionResult HandleError()
    {
        return Problem(); // Returns standardized error response
    }
}
```

---

### 3. **CORS Middleware**

**Purpose**: Enables Cross-Origin Resource Sharing for frontend applications

```csharp
public void ConfigureServices(IServiceCollection services)
{
    services.AddCors(options =>
    {
        options.AddPolicy("AllowReactApp", builder =>
        {
            builder.WithOrigins("http://localhost:3000")
                   .AllowAnyHeader()
                   .AllowAnyMethod()
                   .AllowCredentials();
        });
    });
}

public void Configure(IApplicationBuilder app)
{
    app.UseCors("AllowReactApp"); // Must come before UseRouting
    
    app.UseRouting();
    app.UseAuthentication();
    app.UseAuthorization();
    app.UseEndpoints(endpoints => endpoints.MapControllers());
}
```

---

### 4. **Static Files Middleware**

**Purpose**: Serves static files (HTML, CSS, JS, images) from wwwroot folder

```csharp
public void Configure(IApplicationBuilder app)
{
    app.UseStaticFiles(); // Serves files from wwwroot
    
    // Serve files from custom directory
    app.UseStaticFiles(new StaticFileOptions
    {
        FileProvider = new PhysicalFileProvider(
            Path.Combine(Directory.GetCurrentDirectory(), "MyStaticFiles")),
        RequestPath = "/StaticFiles"
    });
    
    app.UseRouting();
    app.UseEndpoints(endpoints => endpoints.MapControllers());
}
```

---

### 5. **Request Logging Middleware** (Common Real-World Example)

**Purpose**: Log every HTTP request for monitoring and debugging

```csharp
public void Configure(IApplicationBuilder app)
{
    // Built-in request logging
    app.Use(async (context, next) =>
    {
        Console.WriteLine($"[{DateTime.Now}] {context.Request.Method} {context.Request.Path}");
        
        await next(); // Call next middleware
        
        Console.WriteLine($"[{DateTime.Now}] Response: {context.Response.StatusCode}");
    });
    
    app.UseRouting();
    app.UseEndpoints(endpoints => endpoints.MapControllers());
}
```

**Output:**
```
[2026-05-26 10:30:15] GET /api/products
[2026-05-26 10:30:15] Response: 200

[2026-05-26 10:30:20] POST /api/products
[2026-05-26 10:30:20] Response: 201
```

---

## Real-World Example I've Used: Request/Response Logging Middleware

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
        // Log request
        _logger.LogInformation($"Incoming Request: {context.Request.Method} {context.Request.Path}");
        _logger.LogInformation($"Query String: {context.Request.QueryString}");
        
        // Read request body
        context.Request.EnableBuffering();
        var requestBody = await ReadBodyAsync(context.Request.Body);
        _logger.LogInformation($"Request Body: {requestBody}");
        context.Request.Body.Position = 0; // Reset for next middleware
        
        // Capture response
        var originalBodyStream = context.Response.Body;
        using var responseBody = new MemoryStream();
        context.Response.Body = responseBody;
        
        // Call next middleware
        await _next(context);
        
        // Log response
        responseBody.Seek(0, SeekOrigin.Begin);
        var responseBodyText = await new StreamReader(responseBody).ReadToEndAsync();
        _logger.LogInformation($"Response Status: {context.Response.StatusCode}");
        _logger.LogInformation($"Response Body: {responseBodyText}");
        
        // Copy response back
        responseBody.Seek(0, SeekOrigin.Begin);
        await responseBody.CopyToAsync(originalBodyStream);
    }
    
    private async Task<string> ReadBodyAsync(Stream body)
    {
        using var reader = new StreamReader(body, leaveOpen: true);
        var bodyText = await reader.ReadToEndAsync();
        body.Position = 0;
        return bodyText;
    }
}

// Extension method for easy registration
public static class RequestResponseLoggingMiddlewareExtensions
{
    public static IApplicationBuilder UseRequestResponseLogging(this IApplicationBuilder builder)
    {
        return builder.UseMiddleware<RequestResponseLoggingMiddleware>();
    }
}

// Usage in Startup.cs
public void Configure(IApplicationBuilder app)
{
    app.UseRequestResponseLogging(); // Our custom middleware
    
    app.UseRouting();
    app.UseAuthentication();
    app.UseAuthorization();
    app.UseEndpoints(endpoints => endpoints.MapControllers());
}
```

---

## Summary

**Middleware = Components in the request/response pipeline**

**Key Points:**
- ✅ Process requests before they reach the endpoint
- ✅ Process responses after the endpoint returns
- ✅ Order matters - add middleware in the correct sequence
- ✅ Can short-circuit the pipeline (stop further processing)
- ✅ Each middleware calls `next()` to continue the chain

**Common Middleware Used:**
1. Authentication/Authorization
2. Exception Handling
3. CORS
4. Request Logging
5. Static Files
6. Routing

Middleware makes cross-cutting concerns (logging, auth, error handling) clean and reusable!
