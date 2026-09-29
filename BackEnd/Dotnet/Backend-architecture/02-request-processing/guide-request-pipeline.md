# Request Processing Architecture in ASP.NET Core

> **Production-ready guide** to middleware pipeline, filters, and request processing  
> **Focus**: Middleware ordering, custom middleware, filters, model binding, and CORS

## Real-World Scenario

**The Problem**:
Your API is experiencing issues:
- Unhandled exceptions crash the app
- CORS errors block frontend requests
- Authentication fails randomly
- Request logging is inconsistent
- Validation errors return 500 instead of 400

**The Root Cause**: Incorrect middleware ordering and missing filters

**The Impact**:
- Poor error messages for clients
- Security vulnerabilities
- Difficult debugging
- Inconsistent API behavior

**The Solution**: Proper middleware pipeline and filter configuration

---

## Table of Contents

1. [Middleware Pipeline](#middleware-pipeline)
2. [Custom Middleware](#custom-middleware)
3. [Filters](#filters)
4. [Model Binding & Validation](#model-binding--validation)
5. [CORS Configuration](#cors-configuration)
6. [Request/Response Interception](#requestresponse-interception)

---

## Middleware Pipeline

### What is Middleware?

**Middleware** = Software that sits between the HTTP request and your application code

Each middleware:
1. Receives the HTTP request
2. Does some processing
3. Either:
   - Passes request to next middleware (`await next(context)`)
   - Short-circuits and returns response

### The Pipeline Flow

```
HTTP Request
    ↓
[Exception Handling Middleware]  ← Catches all exceptions
    ↓
[Request Logging Middleware]     ← Logs incoming requests
    ↓
[CORS Middleware]                ← Handles CORS preflight
    ↓
[Authentication Middleware]      ← Validates JWT token
    ↓
[Authorization Middleware]       ← Checks permissions
    ↓
[Response Compression]           ← Compresses response
    ↓
[Routing Middleware]             ← Matches route
    ↓
[Endpoint Middleware]            ← Executes controller action
    ↓
HTTP Response (flows back up)
```

### Middleware Ordering (Critical!)

**Order matters!** Wrong order = broken app.

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// Configure services
builder.Services.AddControllers();
builder.Services.AddAuthentication(/* ... */);
builder.Services.AddAuthorization();
builder.Services.AddCors();

var app = builder.Build();

// ⚠️ ORDER IS CRITICAL! ⚠️

// 1. Exception handling (MUST be first to catch all errors)
app.UseExceptionHandler("/error");
// OR custom middleware
app.UseMiddleware<ExceptionHandlingMiddleware>();

// 2. HTTPS redirection (before any other middleware)
app.UseHttpsRedirection();

// 3. Static files (if serving static content)
app.UseStaticFiles();

// 4. Routing (MUST be before CORS, Auth, Authorization)
app.UseRouting();

// 5. CORS (MUST be after UseRouting, before UseAuthentication)
app.UseCors("AllowReactApp");

// 6. Authentication (MUST be before Authorization)
app.UseAuthentication();

// 7. Authorization (MUST be after Authentication)
app.UseAuthorization();

// 8. Response compression (optional, before endpoints)
app.UseResponseCompression();

// 9. Custom middleware (business logic)
app.UseMiddleware<RequestLoggingMiddleware>();
app.UseMiddleware<PerformanceMonitoringMiddleware>();

// 10. Endpoints (MUST be last)
app.MapControllers();

app.Run();
```

### Why Order Matters

**❌ Wrong Order**:
```csharp
app.UseAuthentication();  // Tries to authenticate
app.UseCors();            // CORS runs AFTER auth
// Result: CORS preflight requests fail (no auth token in preflight)
```

**✅ Correct Order**:
```csharp
app.UseCors();            // CORS runs first
app.UseAuthentication();  // Then authenticate
// Result: CORS preflight succeeds, then auth runs on actual request
```

---

## Custom Middleware

### Creating Custom Middleware

**Scenario**: Log every incoming request with duration

**Method 1: Inline Middleware**
```csharp
app.Use(async (context, next) =>
{
    var stopwatch = Stopwatch.StartNew();
    
    // Before request
    Console.WriteLine($"Request: {context.Request.Method} {context.Request.Path}");
    
    await next(context); // Call next middleware
    
    // After request
    stopwatch.Stop();
    Console.WriteLine($"Response: {context.Response.StatusCode} in {stopwatch.ElapsedMilliseconds}ms");
});
```

**Method 2: Middleware Class (Recommended)**
```csharp
// Middleware/RequestLoggingMiddleware.cs
public class RequestLoggingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestLoggingMiddleware> _logger;
    
    public RequestLoggingMiddleware(
        RequestDelegate next,
        ILogger<RequestLoggingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }
    
    public async Task InvokeAsync(HttpContext context)
    {
        var stopwatch = Stopwatch.StartNew();
        var requestPath = context.Request.Path;
        var requestMethod = context.Request.Method;
        
        try
        {
            // Log incoming request
            _logger.LogInformation(
                "Incoming {Method} request to {Path}",
                requestMethod,
                requestPath);
            
            // Call next middleware
            await _next(context);
            
            // Log response
            stopwatch.Stop();
            _logger.LogInformation(
                "Completed {Method} {Path} with status {StatusCode} in {Duration}ms",
                requestMethod,
                requestPath,
                context.Response.StatusCode,
                stopwatch.ElapsedMilliseconds);
        }
        catch (Exception ex)
        {
            stopwatch.Stop();
            _logger.LogError(
                ex,
                "Request {Method} {Path} failed after {Duration}ms",
                requestMethod,
                requestPath,
                stopwatch.ElapsedMilliseconds);
            
            throw; // Re-throw to be caught by exception handling middleware
        }
    }
}

// Extension method for clean registration
public static class RequestLoggingMiddlewareExtensions
{
    public static IApplicationBuilder UseRequestLogging(this IApplicationBuilder builder)
    {
        return builder.UseMiddleware<RequestLoggingMiddleware>();
    }
}

// Program.cs
app.UseRequestLogging();
```

### Exception Handling Middleware

**Production-ready exception handler**:
```csharp
// Middleware/ExceptionHandlingMiddleware.cs
public class ExceptionHandlingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<ExceptionHandlingMiddleware> _logger;
    private readonly IHostEnvironment _environment;
    
    public ExceptionHandlingMiddleware(
        RequestDelegate next,
        ILogger<ExceptionHandlingMiddleware> logger,
        IHostEnvironment environment)
    {
        _next = next;
        _logger = logger;
        _environment = environment;
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
    
    private async Task HandleExceptionAsync(HttpContext context, Exception exception)
    {
        context.Response.ContentType = "application/json";
        
        var response = exception switch
        {
            NotFoundException notFoundEx => new
            {
                status = StatusCodes.Status404NotFound,
                title = "Resource not found",
                detail = notFoundEx.Message,
                traceId = context.TraceIdentifier
            },
            ValidationException validationEx => new
            {
                status = StatusCodes.Status400BadRequest,
                title = "Validation failed",
                detail = validationEx.Message,
                errors = validationEx.Errors,
                traceId = context.TraceIdentifier
            },
            UnauthorizedAccessException => new
            {
                status = StatusCodes.Status403Forbidden,
                title = "Forbidden",
                detail = "You don't have permission to access this resource",
                traceId = context.TraceIdentifier
            },
            _ => new
            {
                status = StatusCodes.Status500InternalServerError,
                title = "Internal server error",
                detail = _environment.IsDevelopment() 
                    ? exception.Message 
                    : "An unexpected error occurred",
                stackTrace = _environment.IsDevelopment() 
                    ? exception.StackTrace 
                    : null,
                traceId = context.TraceIdentifier
            }
        };
        
        context.Response.StatusCode = response.status;
        await context.Response.WriteAsJsonAsync(response);
    }
}
```

### Performance Monitoring Middleware

```csharp
public class PerformanceMonitoringMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<PerformanceMonitoringMiddleware> _logger;
    private const int SlowRequestThresholdMs = 500;

    public PerformanceMonitoringMiddleware(
        RequestDelegate next,
        ILogger<PerformanceMonitoringMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        var stopwatch = Stopwatch.StartNew();

        await _next(context);

        stopwatch.Stop();

        if (stopwatch.ElapsedMilliseconds > SlowRequestThresholdMs)
        {
            _logger.LogWarning(
                "Slow request detected: {Method} {Path} took {Duration}ms",
                context.Request.Method,
                context.Request.Path,
                stopwatch.ElapsedMilliseconds);
        }
    }
}
```

---

## Filters

### What are Filters?

**Filters** = Code that runs before or after specific stages in the request processing pipeline

**Middleware vs Filters**:
- **Middleware**: Runs for ALL requests, works at HTTP level
- **Filters**: Runs for specific controllers/actions, works at MVC level

### Filter Types & Execution Order

```
HTTP Request
    ↓
[Middleware Pipeline]
    ↓
[Authorization Filters]      ← Check permissions
    ↓
[Resource Filters (Before)]  ← Short-circuit for caching
    ↓
[Model Binding]              ← Bind request data to parameters
    ↓
[Action Filters (Before)]    ← Modify action arguments
    ↓
[Action Method Execution]    ← Your controller action
    ↓
[Action Filters (After)]     ← Modify action result
    ↓
[Exception Filters]          ← Handle exceptions
    ↓
[Result Filters (Before)]    ← Modify result before execution
    ↓
[Result Execution]           ← Execute result (serialize to JSON)
    ↓
[Result Filters (After)]     ← Modify response
    ↓
[Resource Filters (After)]   ← Cache response
    ↓
HTTP Response
```

### 1. Action Filters

**Use Case**: Logging, modifying action arguments/results

```csharp
// Filters/LogActionFilter.cs
public class LogActionFilter : IAsyncActionFilter
{
    private readonly ILogger<LogActionFilter> _logger;

    public LogActionFilter(ILogger<LogActionFilter> logger)
    {
        _logger = logger;
    }

    public async Task OnActionExecutionAsync(
        ActionExecutingContext context,
        ActionExecutionDelegate next)
    {
        // Before action execution
        _logger.LogInformation(
            "Executing action {ActionName} on controller {ControllerName}",
            context.ActionDescriptor.DisplayName,
            context.Controller.GetType().Name);

        // Log action arguments
        foreach (var arg in context.ActionArguments)
        {
            _logger.LogDebug("Argument: {Key} = {Value}", arg.Key, arg.Value);
        }

        // Execute action
        var result = await next();

        // After action execution
        if (result.Exception != null)
        {
            _logger.LogError(
                result.Exception,
                "Action {ActionName} threw an exception",
                context.ActionDescriptor.DisplayName);
        }
        else
        {
            _logger.LogInformation(
                "Action {ActionName} completed successfully",
                context.ActionDescriptor.DisplayName);
        }
    }
}

// Register globally
builder.Services.AddControllers(options =>
{
    options.Filters.Add<LogActionFilter>();
});

// OR apply to specific controller/action
[ServiceFilter(typeof(LogActionFilter))]
public class ProductsController : ControllerBase
{
    // ...
}
```

### 2. Authorization Filters

**Use Case**: Custom authorization logic beyond `[Authorize]`

```csharp
// Filters/RequireAdminOrOwnerFilter.cs
public class RequireAdminOrOwnerFilter : IAsyncAuthorizationFilter
{
    private readonly ICurrentUserService _currentUserService;

    public RequireAdminOrOwnerFilter(ICurrentUserService currentUserService)
    {
        _currentUserService = currentUserService;
    }

    public async Task OnAuthorizationAsync(AuthorizationFilterContext context)
    {
        // Get resource ID from route
        if (!context.RouteData.Values.TryGetValue("id", out var idValue))
        {
            context.Result = new BadRequestObjectResult("Resource ID is required");
            return;
        }

        var resourceId = int.Parse(idValue.ToString()!);

        // Check if user is admin
        if (_currentUserService.IsInRole("Admin"))
        {
            return; // Allow
        }

        // Check if user owns the resource
        var dbContext = context.HttpContext.RequestServices
            .GetRequiredService<ApplicationDbContext>();

        var resource = await dbContext.Orders
            .FirstOrDefaultAsync(o => o.Id == resourceId);

        if (resource == null)
        {
            context.Result = new NotFoundResult();
            return;
        }

        if (resource.UserId != _currentUserService.UserId)
        {
            context.Result = new ForbidResult();
            return;
        }

        // User is owner, allow
    }
}

// Usage
[ServiceFilter(typeof(RequireAdminOrOwnerFilter))]
[HttpGet("{id}")]
public async Task<IActionResult> GetOrder(int id)
{
    // Filter already verified user can access this order
    var order = await _context.Orders.FindAsync(id);
    return Ok(order);
}
```

### 3. Exception Filters

**Use Case**: Handle exceptions at controller/action level

```csharp
// Filters/ApiExceptionFilter.cs
public class ApiExceptionFilter : IExceptionFilter
{
    private readonly ILogger<ApiExceptionFilter> _logger;
    private readonly IHostEnvironment _environment;

    public ApiExceptionFilter(
        ILogger<ApiExceptionFilter> logger,
        IHostEnvironment environment)
    {
        _logger = logger;
        _environment = environment;
    }

    public void OnException(ExceptionContext context)
    {
        _logger.LogError(
            context.Exception,
            "Exception occurred in {ActionName}",
            context.ActionDescriptor.DisplayName);

        var problemDetails = context.Exception switch
        {
            NotFoundException ex => new ProblemDetails
            {
                Status = StatusCodes.Status404NotFound,
                Title = "Resource not found",
                Detail = ex.Message,
                Instance = context.HttpContext.Request.Path
            },
            ValidationException ex => new ValidationProblemDetails(ex.Errors)
            {
                Status = StatusCodes.Status400BadRequest,
                Title = "Validation failed",
                Instance = context.HttpContext.Request.Path
            },
            _ => new ProblemDetails
            {
                Status = StatusCodes.Status500InternalServerError,
                Title = "Internal server error",
                Detail = _environment.IsDevelopment()
                    ? context.Exception.Message
                    : "An unexpected error occurred",
                Instance = context.HttpContext.Request.Path
            }
        };

        context.Result = new ObjectResult(problemDetails)
        {
            StatusCode = problemDetails.Status
        };

        context.ExceptionHandled = true;
    }
}

// Register globally
builder.Services.AddControllers(options =>
{
    options.Filters.Add<ApiExceptionFilter>();
});
```

### 4. Result Filters

**Use Case**: Modify response before serialization

```csharp
// Filters/AddVersionHeaderFilter.cs
public class AddVersionHeaderFilter : IResultFilter
{
    public void OnResultExecuting(ResultExecutingContext context)
    {
        // Add custom header to response
        context.HttpContext.Response.Headers.Add("X-API-Version", "1.0");
        context.HttpContext.Response.Headers.Add("X-Powered-By", "ASP.NET Core");
    }

    public void OnResultExecuted(ResultExecutedContext context)
    {
        // After result execution (response already sent)
    }
}

// Filters/FormatResponseFilter.cs
public class FormatResponseFilter : IAsyncResultFilter
{
    public async Task OnResultExecutionAsync(
        ResultExecutingContext context,
        ResultExecutionDelegate next)
    {
        // Wrap all responses in standard format
        if (context.Result is ObjectResult objectResult)
        {
            var wrappedResponse = new
            {
                success = true,
                data = objectResult.Value,
                timestamp = DateTime.UtcNow
            };

            context.Result = new ObjectResult(wrappedResponse)
            {
                StatusCode = objectResult.StatusCode
            };
        }

        await next();
    }
}
```

### 5. Resource Filters

**Use Case**: Short-circuit pipeline for caching

```csharp
// Filters/CacheResourceFilter.cs
public class CacheResourceFilter : IAsyncResourceFilter
{
    private readonly IMemoryCache _cache;

    public CacheResourceFilter(IMemoryCache cache)
    {
        _cache = cache;
    }

    public async Task OnResourceExecutionAsync(
        ResourceExecutingContext context,
        ResourceExecutionDelegate next)
    {
        var cacheKey = $"{context.HttpContext.Request.Path}_{context.HttpContext.Request.QueryString}";

        // Try to get from cache
        if (_cache.TryGetValue(cacheKey, out ObjectResult? cachedResult))
        {
            context.Result = cachedResult;
            return; // Short-circuit (don't execute action)
        }

        // Execute action
        var executedContext = await next();

        // Cache the result
        if (executedContext.Result is ObjectResult result)
        {
            _cache.Set(cacheKey, result, TimeSpan.FromMinutes(5));
        }
    }
}

// Usage
[ServiceFilter(typeof(CacheResourceFilter))]
[HttpGet]
public async Task<IActionResult> GetProducts()
{
    var products = await _context.Products.ToListAsync();
    return Ok(products);
}
```

### Filter Scope

Filters can be applied at different levels:

```csharp
// 1. Global (all controllers/actions)
builder.Services.AddControllers(options =>
{
    options.Filters.Add<LogActionFilter>();
    options.Filters.Add<ApiExceptionFilter>();
});

// 2. Controller level
[ServiceFilter(typeof(LogActionFilter))]
public class ProductsController : ControllerBase
{
    // All actions in this controller
}

// 3. Action level
public class ProductsController : ControllerBase
{
    [ServiceFilter(typeof(CacheResourceFilter))]
    [HttpGet]
    public async Task<IActionResult> GetProducts()
    {
        // Only this action
    }
}

// 4. Using attributes (no DI)
[TypeFilter(typeof(LogActionFilter))]
public class ProductsController : ControllerBase { }
```

---

## Model Binding & Validation

### What is Model Binding?

**Model Binding** = Automatically maps HTTP request data to action method parameters

### Binding Sources

```csharp
[HttpPost("{id}")]
public async Task<IActionResult> UpdateProduct(
    [FromRoute] int id,              // From URL path
    [FromBody] UpdateProductDto dto, // From request body (JSON)
    [FromQuery] string? filter,      // From query string (?filter=active)
    [FromHeader] string apiKey,      // From HTTP header
    [FromForm] IFormFile file)       // From form data (file upload)
{
    // All parameters are automatically bound
}
```

### Model Validation with Data Annotations

```csharp
// DTOs/CreateProductDto.cs
public class CreateProductDto
{
    [Required(ErrorMessage = "Product name is required")]
    [StringLength(100, MinimumLength = 3, ErrorMessage = "Name must be between 3 and 100 characters")]
    public string Name { get; set; } = string.Empty;

    [Required]
    [Range(0.01, 999999.99, ErrorMessage = "Price must be between 0.01 and 999999.99")]
    public decimal Price { get; set; }

    [StringLength(500, ErrorMessage = "Description cannot exceed 500 characters")]
    public string? Description { get; set; }

    [Required]
    [EmailAddress(ErrorMessage = "Invalid email format")]
    public string ContactEmail { get; set; } = string.Empty;

    [Url(ErrorMessage = "Invalid URL format")]
    public string? Website { get; set; }

    [Range(0, int.MaxValue, ErrorMessage = "Stock must be non-negative")]
    public int Stock { get; set; }
}

// Controller
[HttpPost]
public async Task<IActionResult> CreateProduct([FromBody] CreateProductDto dto)
{
    // ModelState.IsValid is automatically checked if you add [ApiController]
    if (!ModelState.IsValid)
    {
        return BadRequest(ModelState);
    }

    // Validation passed, create product
    var product = new Product
    {
        Name = dto.Name,
        Price = dto.Price,
        Description = dto.Description,
        Stock = dto.Stock
    };

    await _context.Products.AddAsync(product);
    await _context.SaveChangesAsync();

    return CreatedAtAction(nameof(GetProduct), new { id = product.Id }, product);
}
```

### FluentValidation (Recommended for Complex Validation)

**Why FluentValidation?**
- ✅ More readable than data annotations
- ✅ Supports complex validation logic
- ✅ Easier to test
- ✅ Separation of concerns

```bash
dotnet add package FluentValidation.AspNetCore
```

```csharp
// Validators/CreateProductDtoValidator.cs
using FluentValidation;

public class CreateProductDtoValidator : AbstractValidator<CreateProductDto>
{
    public CreateProductDtoValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Product name is required")
            .Length(3, 100).WithMessage("Name must be between 3 and 100 characters")
            .Must(BeValidProductName).WithMessage("Product name contains invalid characters");

        RuleFor(x => x.Price)
            .GreaterThan(0).WithMessage("Price must be greater than 0")
            .LessThan(1000000).WithMessage("Price must be less than 1,000,000");

        RuleFor(x => x.Description)
            .MaximumLength(500).WithMessage("Description cannot exceed 500 characters")
            .When(x => !string.IsNullOrEmpty(x.Description));

        RuleFor(x => x.ContactEmail)
            .NotEmpty().WithMessage("Contact email is required")
            .EmailAddress().WithMessage("Invalid email format");

        RuleFor(x => x.Stock)
            .GreaterThanOrEqualTo(0).WithMessage("Stock cannot be negative");

        // Complex validation
        RuleFor(x => x)
            .Must(HaveValidPriceForCategory)
            .WithMessage("Price is too high for this category");
    }

    private bool BeValidProductName(string name)
    {
        // Custom validation logic
        return !name.Contains("@") && !name.Contains("#");
    }

    private bool HaveValidPriceForCategory(CreateProductDto dto)
    {
        // Complex business rule
        if (dto.Category == "Electronics" && dto.Price > 10000)
            return false;

        return true;
    }
}

// Program.cs
builder.Services.AddValidatorsFromAssemblyContaining<CreateProductDtoValidator>();
builder.Services.AddFluentValidationAutoValidation();

// Controller (validation happens automatically)
[HttpPost]
public async Task<IActionResult> CreateProduct([FromBody] CreateProductDto dto)
{
    // FluentValidation runs automatically
    // If validation fails, returns 400 with error details

    var product = new Product { /* ... */ };
    await _context.Products.AddAsync(product);
    await _context.SaveChangesAsync();

    return CreatedAtAction(nameof(GetProduct), new { id = product.Id }, product);
}
```

### Custom Model Binder

**Use Case**: Bind complex types from query string

```csharp
// Models/DateRangeFilter.cs
public class DateRangeFilter
{
    public DateTime? StartDate { get; set; }
    public DateTime? EndDate { get; set; }
}

// ModelBinders/DateRangeFilterBinder.cs
public class DateRangeFilterBinder : IModelBinder
{
    public Task BindModelAsync(ModelBindingContext bindingContext)
    {
        var startDateValue = bindingContext.ValueProvider.GetValue("startDate");
        var endDateValue = bindingContext.ValueProvider.GetValue("endDate");

        var filter = new DateRangeFilter();

        if (startDateValue != ValueProviderResult.None)
        {
            if (DateTime.TryParse(startDateValue.FirstValue, out var startDate))
            {
                filter.StartDate = startDate;
            }
        }

        if (endDateValue != ValueProviderResult.None)
        {
            if (DateTime.TryParse(endDateValue.FirstValue, out var endDate))
            {
                filter.EndDate = endDate;
            }
        }

        bindingContext.Result = ModelBindingResult.Success(filter);
        return Task.CompletedTask;
    }
}

// Usage
[HttpGet]
public async Task<IActionResult> GetOrders(
    [ModelBinder(typeof(DateRangeFilterBinder))] DateRangeFilter dateRange)
{
    var query = _context.Orders.AsQueryable();

    if (dateRange.StartDate.HasValue)
        query = query.Where(o => o.CreatedAt >= dateRange.StartDate.Value);

    if (dateRange.EndDate.HasValue)
        query = query.Where(o => o.CreatedAt <= dateRange.EndDate.Value);

    var orders = await query.ToListAsync();
    return Ok(orders);
}

// Request: GET /api/orders?startDate=2024-01-01&endDate=2024-12-31
```

### Validation Error Response Format

```csharp
// Filters/ValidationFilter.cs
public class ValidationFilter : IAsyncActionFilter
{
    public async Task OnActionExecutionAsync(
        ActionExecutingContext context,
        ActionExecutionDelegate next)
    {
        if (!context.ModelState.IsValid)
        {
            var errors = context.ModelState
                .Where(x => x.Value?.Errors.Count > 0)
                .ToDictionary(
                    kvp => kvp.Key,
                    kvp => kvp.Value!.Errors.Select(e => e.ErrorMessage).ToArray()
                );

            var response = new
            {
                type = "https://tools.ietf.org/html/rfc7231#section-6.5.1",
                title = "One or more validation errors occurred",
                status = 400,
                errors = errors,
                traceId = context.HttpContext.TraceIdentifier
            };

            context.Result = new BadRequestObjectResult(response);
            return;
        }

        await next();
    }
}

// Register globally
builder.Services.AddControllers(options =>
{
    options.Filters.Add<ValidationFilter>();
});

// Example error response:
// {
//   "type": "https://tools.ietf.org/html/rfc7231#section-6.5.1",
//   "title": "One or more validation errors occurred",
//   "status": 400,
//   "errors": {
//     "Name": ["Product name is required"],
//     "Price": ["Price must be greater than 0"]
//   },
//   "traceId": "00-abc123-def456-00"
// }
```

---

## CORS Configuration

### What is CORS?

**CORS (Cross-Origin Resource Sharing)** = Security feature that allows/blocks requests from different origins

**Origin** = Protocol + Domain + Port
- `https://localhost:3000` (React app)
- `https://localhost:5001` (API)
- Different origins = CORS required

### The Problem

```
React App (https://localhost:3000)
    ↓ HTTP Request
API (https://localhost:5001)
    ↓ Response
❌ CORS Error: "No 'Access-Control-Allow-Origin' header is present"
```

### Basic CORS Configuration

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// 1. Add CORS service
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowReactApp", policy =>
    {
        policy.WithOrigins("https://localhost:3000") // React app URL
              .AllowAnyMethod()                       // GET, POST, PUT, DELETE, etc.
              .AllowAnyHeader()                       // Content-Type, Authorization, etc.
              .AllowCredentials();                    // Allow cookies/auth headers
    });
});

var app = builder.Build();

// 2. Use CORS middleware (MUST be after UseRouting, before UseAuthentication)
app.UseRouting();
app.UseCors("AllowReactApp");
app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();
app.Run();
```

### Multiple CORS Policies

```csharp
builder.Services.AddCors(options =>
{
    // Policy 1: React app (development)
    options.AddPolicy("AllowReactDev", policy =>
    {
        policy.WithOrigins("https://localhost:3000", "http://localhost:3000")
              .AllowAnyMethod()
              .AllowAnyHeader()
              .AllowCredentials();
    });

    // Policy 2: Production frontend
    options.AddPolicy("AllowProduction", policy =>
    {
        policy.WithOrigins("https://myapp.com", "https://www.myapp.com")
              .AllowAnyMethod()
              .AllowAnyHeader()
              .AllowCredentials();
    });

    // Policy 3: Public API (no credentials)
    options.AddPolicy("AllowPublicAPI", policy =>
    {
        policy.AllowAnyOrigin()  // ⚠️ Use with caution!
              .AllowAnyMethod()
              .AllowAnyHeader();
        // Note: Cannot use AllowCredentials() with AllowAnyOrigin()
    });

    // Policy 4: Specific methods only
    options.AddPolicy("ReadOnly", policy =>
    {
        policy.WithOrigins("https://partner.com")
              .WithMethods("GET", "HEAD")  // Only read operations
              .WithHeaders("Content-Type");
    });
});

// Apply different policies to different controllers
[ApiController]
[Route("api/[controller]")]
[EnableCors("AllowReactDev")]  // Apply to entire controller
public class ProductsController : ControllerBase
{
    [HttpGet]
    [EnableCors("AllowPublicAPI")]  // Override for specific action
    public async Task<IActionResult> GetProducts()
    {
        // This action allows any origin
    }
}
```

### Environment-Specific CORS

```csharp
// appsettings.Development.json
{
  "Cors": {
    "AllowedOrigins": ["https://localhost:3000", "http://localhost:3000"]
  }
}

// appsettings.Production.json
{
  "Cors": {
    "AllowedOrigins": ["https://myapp.com", "https://www.myapp.com"]
  }
}

// Program.cs
var allowedOrigins = builder.Configuration
    .GetSection("Cors:AllowedOrigins")
    .Get<string[]>() ?? Array.Empty<string>();

builder.Services.AddCors(options =>
{
    options.AddPolicy("DynamicPolicy", policy =>
    {
        policy.WithOrigins(allowedOrigins)
              .AllowAnyMethod()
              .AllowAnyHeader()
              .AllowCredentials();
    });
});
```

### CORS Preflight Requests

**What is a preflight request?**
- Browser sends OPTIONS request before actual request
- Checks if server allows the cross-origin request
- Happens for "non-simple" requests (POST with JSON, custom headers, etc.)

```
Browser → OPTIONS /api/products (Preflight)
          Headers:
            Origin: https://localhost:3000
            Access-Control-Request-Method: POST
            Access-Control-Request-Headers: Content-Type, Authorization

Server  → 204 No Content
          Headers:
            Access-Control-Allow-Origin: https://localhost:3000
            Access-Control-Allow-Methods: GET, POST, PUT, DELETE
            Access-Control-Allow-Headers: Content-Type, Authorization
            Access-Control-Max-Age: 86400 (cache preflight for 24 hours)

Browser → POST /api/products (Actual request)
```

**Configure preflight caching**:
```csharp
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowReactApp", policy =>
    {
        policy.WithOrigins("https://localhost:3000")
              .AllowAnyMethod()
              .AllowAnyHeader()
              .AllowCredentials()
              .SetPreflightMaxAge(TimeSpan.FromHours(24)); // Cache preflight for 24 hours
    });
});
```

### Common CORS Issues & Solutions

**Issue 1: "CORS policy: No 'Access-Control-Allow-Origin' header"**
```csharp
// ❌ WRONG: CORS middleware after UseAuthentication
app.UseAuthentication();
app.UseCors("AllowReactApp");

// ✅ CORRECT: CORS before UseAuthentication
app.UseCors("AllowReactApp");
app.UseAuthentication();
```

**Issue 2: "Credentials flag is true, but Access-Control-Allow-Credentials is not"**
```csharp
// ❌ WRONG: AllowAnyOrigin with AllowCredentials
policy.AllowAnyOrigin()
      .AllowCredentials(); // ERROR!

// ✅ CORRECT: Specify origins when using credentials
policy.WithOrigins("https://localhost:3000")
      .AllowCredentials();
```

**Issue 3: "Method not allowed by Access-Control-Allow-Methods"**
```csharp
// ❌ WRONG: Forgot to allow specific method
policy.WithMethods("GET", "POST"); // PUT not allowed!

// ✅ CORRECT: Allow all methods or specify PUT
policy.AllowAnyMethod();
// OR
policy.WithMethods("GET", "POST", "PUT", "DELETE", "PATCH");
```

**Issue 4: Custom headers not allowed**
```csharp
// React sends custom header
axios.get('/api/products', {
  headers: { 'X-Custom-Header': 'value' }
});

// ❌ WRONG: Didn't allow custom header
policy.WithHeaders("Content-Type", "Authorization");

// ✅ CORRECT: Allow custom header
policy.WithHeaders("Content-Type", "Authorization", "X-Custom-Header");
// OR allow all headers
policy.AllowAnyHeader();
```

---

## Request/Response Interception

### Reading Request Body

**Problem**: Request body can only be read once

```csharp
// Middleware/RequestBodyLoggingMiddleware.cs
public class RequestBodyLoggingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestBodyLoggingMiddleware> _logger;

    public RequestBodyLoggingMiddleware(
        RequestDelegate next,
        ILogger<RequestBodyLoggingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        // Enable buffering to allow multiple reads
        context.Request.EnableBuffering();

        // Read request body
        using var reader = new StreamReader(
            context.Request.Body,
            encoding: Encoding.UTF8,
            detectEncodingFromByteOrderMarks: false,
            leaveOpen: true);

        var body = await reader.ReadToEndAsync();

        // Log request body
        _logger.LogInformation("Request Body: {Body}", body);

        // Reset stream position for next middleware
        context.Request.Body.Position = 0;

        await _next(context);
    }
}
```

### Modifying Response

```csharp
// Middleware/ResponseModificationMiddleware.cs
public class ResponseModificationMiddleware
{
    private readonly RequestDelegate _next;

    public ResponseModificationMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        // Save original response body stream
        var originalBodyStream = context.Response.Body;

        // Create new memory stream to capture response
        using var responseBody = new MemoryStream();
        context.Response.Body = responseBody;

        // Execute next middleware
        await _next(context);

        // Read response
        context.Response.Body.Seek(0, SeekOrigin.Begin);
        var responseText = await new StreamReader(context.Response.Body).ReadToEndAsync();
        context.Response.Body.Seek(0, SeekOrigin.Begin);

        // Modify response (e.g., wrap in standard format)
        if (context.Response.ContentType?.Contains("application/json") == true)
        {
            var modifiedResponse = new
            {
                success = context.Response.StatusCode < 400,
                data = JsonSerializer.Deserialize<object>(responseText),
                timestamp = DateTime.UtcNow,
                requestId = context.TraceIdentifier
            };

            var modifiedJson = JsonSerializer.Serialize(modifiedResponse);
            var modifiedBytes = Encoding.UTF8.GetBytes(modifiedJson);

            // Write modified response
            context.Response.ContentLength = modifiedBytes.Length;
            await originalBodyStream.WriteAsync(modifiedBytes);
        }
        else
        {
            // Copy original response
            await responseBody.CopyToAsync(originalBodyStream);
        }
    }
}
```

### Adding Custom Response Headers

```csharp
// Middleware/CustomHeadersMiddleware.cs
public class CustomHeadersMiddleware
{
    private readonly RequestDelegate _next;

    public CustomHeadersMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        // Add security headers
        context.Response.Headers.Add("X-Content-Type-Options", "nosniff");
        context.Response.Headers.Add("X-Frame-Options", "DENY");
        context.Response.Headers.Add("X-XSS-Protection", "1; mode=block");
        context.Response.Headers.Add("Referrer-Policy", "no-referrer");
        context.Response.Headers.Add("Permissions-Policy", "geolocation=(), microphone=(), camera=()");

        // Add custom headers
        context.Response.Headers.Add("X-API-Version", "1.0");
        context.Response.Headers.Add("X-Request-ID", context.TraceIdentifier);

        await _next(context);
    }
}
```

---

## Summary & Best Practices

### Middleware Best Practices

✅ **DO**:
- Order middleware correctly (Exception → HTTPS → Routing → CORS → Auth → Authorization → Endpoints)
- Use `ILogger` for structured logging
- Handle exceptions gracefully
- Use `async/await` for I/O operations
- Enable request buffering if you need to read body multiple times

❌ **DON'T**:
- Block async code with `.Result` or `.Wait()`
- Forget to call `await next(context)` (pipeline will break)
- Put CORS after Authentication
- Read request body without enabling buffering
- Modify response without buffering

### Filter Best Practices

✅ **DO**:
- Use filters for cross-cutting concerns (logging, validation, caching)
- Register filters globally when they apply to all actions
- Use `IAsyncActionFilter` for async operations
- Inject dependencies via constructor

❌ **DON'T**:
- Put business logic in filters (use handlers/services instead)
- Create filters with heavy dependencies (keep them lightweight)
- Forget to handle exceptions in filters

### Validation Best Practices

✅ **DO**:
- Use FluentValidation for complex validation
- Return consistent error format (Problem Details RFC 7807)
- Validate at the API boundary (DTOs)
- Use custom validators for business rules

❌ **DON'T**:
- Validate domain entities directly (use DTOs)
- Return generic error messages
- Skip validation for "trusted" inputs
- Mix validation with business logic

### CORS Best Practices

✅ **DO**:
- Specify exact origins in production (avoid `AllowAnyOrigin()`)
- Use environment-specific configuration
- Cache preflight requests (`SetPreflightMaxAge`)
- Test CORS in development with actual frontend

❌ **DON'T**:
- Use `AllowAnyOrigin()` with `AllowCredentials()`
- Put CORS middleware in wrong order
- Forget to allow custom headers
- Allow all origins in production

---

## Complete Example: Production-Ready Setup

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// Services
builder.Services.AddControllers(options =>
{
    options.Filters.Add<ApiExceptionFilter>();
    options.Filters.Add<ValidationFilter>();
});

builder.Services.AddAuthentication(/* ... */);
builder.Services.AddAuthorization();

// CORS
var allowedOrigins = builder.Configuration
    .GetSection("Cors:AllowedOrigins")
    .Get<string[]>() ?? Array.Empty<string>();

builder.Services.AddCors(options =>
{
    options.AddPolicy("AppPolicy", policy =>
    {
        policy.WithOrigins(allowedOrigins)
              .AllowAnyMethod()
              .AllowAnyHeader()
              .AllowCredentials()
              .SetPreflightMaxAge(TimeSpan.FromHours(24));
    });
});

// FluentValidation
builder.Services.AddValidatorsFromAssemblyContaining<Program>();
builder.Services.AddFluentValidationAutoValidation();

var app = builder.Build();

// Middleware Pipeline (ORDER IS CRITICAL!)
app.UseMiddleware<ExceptionHandlingMiddleware>();  // 1. Exception handling
app.UseHttpsRedirection();                         // 2. HTTPS
app.UseStaticFiles();                              // 3. Static files
app.UseRouting();                                  // 4. Routing
app.UseCors("AppPolicy");                          // 5. CORS
app.UseAuthentication();                           // 6. Authentication
app.UseAuthorization();                            // 7. Authorization
app.UseMiddleware<RequestLoggingMiddleware>();     // 8. Logging
app.UseMiddleware<PerformanceMonitoringMiddleware>(); // 9. Performance
app.UseMiddleware<CustomHeadersMiddleware>();      // 10. Security headers
app.MapControllers();                              // 11. Endpoints

app.Run();
```

---

**Next Steps**:
1. Review your middleware ordering
2. Implement global exception handling
3. Add FluentValidation for complex DTOs
4. Configure CORS for your frontend
5. Add custom filters for logging and monitoring

**Related Guides**:
- [Clean Architecture](../03-architecture-patterns/guide-clean-architecture.md)
- [API Design](../01-api-design/guide-api-design.md)
- [Performance & Scalability](../05-performance/guide-performance-scalability.md)
```
