# Question 14: What are ASP.NET filters? Explain with a real-time example from your project.

## Answer

### What are Filters?

**Filters** are attributes that allow you to run code before or after specific stages in the request processing pipeline. They provide a way to inject cross-cutting concerns (like logging, caching, authorization) without cluttering your controller actions.

Think of filters as **checkpoints** in your request pipeline where you can execute custom logic.

---

## Types of Filters (in execution order)

```
HTTP Request
    ↓
1. Authorization Filters (first)
    ↓
2. Resource Filters
    ↓
3. Action Filters
    ↓
4. Exception Filters
    ↓
5. Result Filters (last)
    ↓
HTTP Response
```

---

## 1. Authorization Filters

**Purpose**: Determine if the user is authorized to access the resource  
**Runs**: First, before all other filters  
**Interface**: `IAuthorizationFilter`

### Example: Custom Role Check

```csharp
public class CustomAuthorizeAttribute : Attribute, IAuthorizationFilter
{
    private readonly string[] _roles;
    
    public CustomAuthorizeAttribute(params string[] roles)
    {
        _roles = roles;
    }
    
    public void OnAuthorization(AuthorizationFilterContext context)
    {
        var user = context.HttpContext.User;
        
        if (!user.Identity.IsAuthenticated)
        {
            context.Result = new UnauthorizedResult();
            return;
        }
        
        if (_roles.Any() && !_roles.Any(role => user.IsInRole(role)))
        {
            context.Result = new ForbidResult();
        }
    }
}

// Usage
[CustomAuthorize("Admin", "Manager")]
[HttpDelete("{id}")]
public IActionResult DeleteProduct(int id)
{
    return Ok("Product deleted");
}
```

---

## 2. Resource Filters

**Purpose**: Execute code before and after the rest of the pipeline  
**Use Cases**: Short-circuiting, caching  
**Interface**: `IResourceFilter`, `IAsyncResourceFilter`

### Example: Response Caching Filter

```csharp
public class CacheResourceFilter : Attribute, IResourceFilter
{
    private readonly int _durationSeconds;
    private static readonly Dictionary<string, (DateTime, object)> _cache = new();
    
    public CacheResourceFilter(int durationSeconds = 60)
    {
        _durationSeconds = durationSeconds;
    }
    
    public void OnResourceExecuting(ResourceExecutingContext context)
    {
        var cacheKey = context.HttpContext.Request.Path.ToString();
        
        if (_cache.TryGetValue(cacheKey, out var cached))
        {
            if (cached.Item1 > DateTime.UtcNow)
            {
                // Return cached response
                context.Result = new ObjectResult(cached.Item2);
                return; // Short-circuit the pipeline
            }
        }
    }
    
    public void OnResourceExecuted(ResourceExecutedContext context)
    {
        var cacheKey = context.HttpContext.Request.Path.ToString();
        
        if (context.Result is ObjectResult result)
        {
            var expiresAt = DateTime.UtcNow.AddSeconds(_durationSeconds);
            _cache[cacheKey] = (expiresAt, result.Value);
        }
    }
}

// Usage
[CacheResourceFilter(60)] // Cache for 60 seconds
[HttpGet]
public IActionResult GetProducts()
{
    var products = _productService.GetAll();
    return Ok(products);
}
```

---

## 3. Action Filters (Most Commonly Used)

**Purpose**: Execute code before and after action method execution  
**Use Cases**: Logging, validation, modification of arguments  
**Interface**: `IActionFilter`, `IAsyncActionFilter`

### Example 1: Request/Response Logging

```csharp
public class LogActionFilter : IActionFilter
{
    private readonly ILogger<LogActionFilter> _logger;
    
    public LogActionFilter(ILogger<LogActionFilter> logger)
    {
        _logger = logger;
    }
    
    // Executes BEFORE the action method
    public void OnActionExecuting(ActionExecutingContext context)
    {
        var controllerName = context.RouteData.Values["controller"];
        var actionName = context.RouteData.Values["action"];
        
        _logger.LogInformation(
            "Executing {Controller}.{Action} with arguments: {@Arguments}",
            controllerName,
            actionName,
            context.ActionArguments);
    }
    
    // Executes AFTER the action method
    public void OnActionExecuted(ActionExecutedContext context)
    {
        var controllerName = context.RouteData.Values["controller"];
        var actionName = context.RouteData.Values["action"];
        
        if (context.Exception != null)
        {
            _logger.LogError(
                context.Exception,
                "Error in {Controller}.{Action}",
                controllerName,
                actionName);
        }
        else
        {
            _logger.LogInformation(
                "Executed {Controller}.{Action} successfully",
                controllerName,
                actionName);
        }
    }
}

// Register globally in Startup.cs
public void ConfigureServices(IServiceCollection services)
{
    services.AddControllers(options =>
    {
        options.Filters.Add<LogActionFilter>(); // Apply to all actions
    });
}

// Or use on specific actions
[ServiceFilter(typeof(LogActionFilter))]
[HttpPost]
public IActionResult CreateProduct([FromBody] Product product)
{
    return Ok("Product created");
}
```

### Example 2: Model Validation Filter

```csharp
public class ValidateModelAttribute : ActionFilterAttribute
{
    public override void OnActionExecuting(ActionExecutingContext context)
    {
        if (!context.ModelState.IsValid)
        {
            var errors = context.ModelState
                .Where(e => e.Value.Errors.Count > 0)
                .Select(e => new
                {
                    Field = e.Key,
                    Errors = e.Value.Errors.Select(x => x.ErrorMessage)
                });
            
            context.Result = new BadRequestObjectResult(new
            {
                Message = "Validation failed",
                Errors = errors
            });
        }
    }
}

// Usage
[ValidateModel]
[HttpPost]
public IActionResult CreateUser([FromBody] CreateUserRequest request)
{
    // If we reach here, model is valid
    return Ok("User created");
}
```

### Example 3: Performance Monitoring Filter

```csharp
public class PerformanceFilter : IAsyncActionFilter
{
    private readonly ILogger<PerformanceFilter> _logger;
    
    public PerformanceFilter(ILogger<PerformanceFilter> logger)
    {
        _logger = logger;
    }
    
    public async Task OnActionExecutionAsync(
        ActionExecutingContext context,
        ActionExecutionDelegate next)
    {
        var stopwatch = System.Diagnostics.Stopwatch.StartNew();
        
        // Execute the action
        var resultContext = await next();
        
        stopwatch.Stop();
        
        var controllerName = context.RouteData.Values["controller"];
        var actionName = context.RouteData.Values["action"];
        var elapsedMs = stopwatch.ElapsedMilliseconds;
        
        if (elapsedMs > 1000) // Slow request threshold
        {
            _logger.LogWarning(
                "SLOW: {Controller}.{Action} took {Elapsed}ms",
                controllerName,
                actionName,
                elapsedMs);
        }
        else
        {
            _logger.LogInformation(
                "{Controller}.{Action} took {Elapsed}ms",
                controllerName,
                actionName,
                elapsedMs);
        }
    }
}
```

---

## 4. Exception Filters

**Purpose**: Handle exceptions thrown during action execution  
**Interface**: `IExceptionFilter`, `IAsyncExceptionFilter`

### Example: Global Exception Handler

```csharp
public class GlobalExceptionFilter : IExceptionFilter
{
    private readonly ILogger<GlobalExceptionFilter> _logger;
    
    public GlobalExceptionFilter(ILogger<GlobalExceptionFilter> logger)
    {
        _logger = logger;
    }
    
    public void OnException(ExceptionContext context)
    {
        _logger.LogError(context.Exception, "An unhandled exception occurred");
        
        var statusCode = context.Exception switch
        {
            NotFoundException => StatusCodes.Status404NotFound,
            UnauthorizedAccessException => StatusCodes.Status401Unauthorized,
            ArgumentException => StatusCodes.Status400BadRequest,
            _ => StatusCodes.Status500InternalServerError
        };
        
        context.Result = new ObjectResult(new
        {
            Error = context.Exception.Message,
            StatusCode = statusCode,
            Timestamp = DateTime.UtcNow
        })
        {
            StatusCode = statusCode
        };
        
        context.ExceptionHandled = true; // Mark as handled
    }
}

// Register globally
public void ConfigureServices(IServiceCollection services)
{
    services.AddControllers(options =>
    {
        options.Filters.Add<GlobalExceptionFilter>();
    });
}
```

---

## 5. Result Filters

**Purpose**: Execute code before and after execution of action results  
**Interface**: `IResultFilter`, `IAsyncResultFilter`

### Example: Add Custom Headers

```csharp
public class AddHeaderFilter : IResultFilter
{
    private readonly string _name;
    private readonly string _value;
    
    public AddHeaderFilter(string name, string value)
    {
        _name = name;
        _value = value;
    }
    
    public void OnResultExecuting(ResultExecutingContext context)
    {
        context.HttpContext.Response.Headers.Add(_name, _value);
    }
    
    public void OnResultExecuted(ResultExecutedContext context)
    {
        // Can log or modify response after it's been executed
    }
}

// Usage
[TypeFilter(typeof(AddHeaderFilter), Arguments = new object[] { "X-Custom-Header", "MyValue" })]
[HttpGet]
public IActionResult GetProducts()
{
    return Ok("Products");
}
```

---

## Real-World Project Example: E-Commerce API

```csharp
// 1. API Key Authorization Filter
public class ApiKeyAuthFilter : IAuthorizationFilter
{
    private readonly IConfiguration _configuration;
    
    public ApiKeyAuthFilter(IConfiguration configuration)
    {
        _configuration = configuration;
    }
    
    public void OnAuthorization(AuthorizationFilterContext context)
    {
        if (!context.HttpContext.Request.Headers.TryGetValue("X-API-Key", out var apiKey))
        {
            context.Result = new UnauthorizedResult();
            return;
        }
        
        var validKey = _configuration["ApiKey"];
        if (apiKey != validKey)
        {
            context.Result = new UnauthorizedResult();
        }
    }
}

// 2. Request Throttling Filter
public class ThrottleFilter : IActionFilter
{
    private static readonly Dictionary<string, (int count, DateTime resetTime)> _requests = new();
    private readonly int _maxRequests = 100;
    private readonly int _timeWindowMinutes = 1;
    
    public void OnActionExecuting(ActionExecutingContext context)
    {
        var ipAddress = context.HttpContext.Connection.RemoteIpAddress.ToString();
        var now = DateTime.UtcNow;
        
        if (_requests.TryGetValue(ipAddress, out var requestData))
        {
            if (requestData.resetTime > now)
            {
                if (requestData.count >= _maxRequests)
                {
                    context.Result = new StatusCodeResult(429); // Too Many Requests
                    return;
                }
                _requests[ipAddress] = (requestData.count + 1, requestData.resetTime);
            }
            else
            {
                _requests[ipAddress] = (1, now.AddMinutes(_timeWindowMinutes));
            }
        }
        else
        {
            _requests[ipAddress] = (1, now.AddMinutes(_timeWindowMinutes));
        }
    }
    
    public void OnActionExecuted(ActionExecutedContext context) { }
}

// Usage in Controller
[ApiController]
[Route("api/[controller]")]
[ServiceFilter(typeof(ApiKeyAuthFilter))] // Applied to all actions
public class ProductsController : ControllerBase
{
    [HttpGet]
    [ServiceFilter(typeof(ThrottleFilter))] // Rate limiting
    [ServiceFilter(typeof(PerformanceFilter))] // Performance monitoring
    public IActionResult GetAll()
    {
        return Ok("Products");
    }
    
    [HttpPost]
    [ValidateModel] // Model validation
    [ServiceFilter(typeof(LogActionFilter))] // Logging
    public IActionResult Create([FromBody] Product product)
    {
        return Ok("Created");
    }
}
```

---

## Filter Scope

Filters can be applied at three levels:

```csharp
// 1. Global (all controllers, all actions)
public void ConfigureServices(IServiceCollection services)
{
    services.AddControllers(options =>
    {
        options.Filters.Add<LogActionFilter>();
    });
}

// 2. Controller level (all actions in this controller)
[ServiceFilter(typeof(LogActionFilter))]
public class ProductsController : ControllerBase
{
    // All actions here will have logging
}

// 3. Action level (specific action only)
public class ProductsController : ControllerBase
{
    [ServiceFilter(typeof(LogActionFilter))]
    [HttpPost]
    public IActionResult Create()
    {
        // Only this action has logging
    }
}
```

---

## Summary

**Filters = Cross-cutting concerns applied declaratively**

**Five Types:**
1. **Authorization** - Who can access?
2. **Resource** - Short-circuiting, caching
3. **Action** - Most common, logging, validation
4. **Exception** - Error handling
5. **Result** - Modify response

**Common Uses:**
- ✅ Logging and monitoring
- ✅ Authorization and authentication
- ✅ Caching
- ✅ Exception handling
- ✅ Model validation
- ✅ Performance tracking
- ✅ Rate limiting

Filters keep your controllers clean and focused on business logic!
