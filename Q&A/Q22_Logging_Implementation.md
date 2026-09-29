# Question 22: How is logging implemented? What packages do you use, how do you register them, what are the lifetimes, and where are logs stored?

## Answer

### What is Logging?

**Logging** is the practice of recording application events, errors, and information for monitoring, debugging, and auditing purposes.

---

## Built-in Logging in .NET Core

.NET Core has **built-in logging** that works out of the box!

### Log Levels (in order of severity)

```csharp
LogLevel.Trace       // 0 - Most detailed (rarely used)
LogLevel.Debug       // 1 - Debugging information
LogLevel.Information // 2 - General informational messages
LogLevel.Warning     // 3 - Warning messages
LogLevel.Error       // 4 - Error messages
LogLevel.Critical    // 5 - Critical failures
LogLevel.None        // 6 - Logging disabled
```

---

## Configuration in appsettings.json

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning",
      "Microsoft.Hosting.Lifetime": "Information"
    }
  }
}
```

---

## Basic Usage with Built-in ILogger

```csharp
public class ProductService
{
    private readonly ILogger<ProductService> _logger;
    
    public ProductService(ILogger<ProductService> logger)
    {
        _logger = logger;
    }
    
    public async Task<Product> GetProductAsync(int id)
    {
        _logger.LogInformation("Getting product with ID: {ProductId}", id);
        
        try
        {
            var product = await _repository.GetByIdAsync(id);
            
            if (product == null)
            {
                _logger.LogWarning("Product with ID {ProductId} not found", id);
                return null;
            }
            
            _logger.LogDebug("Product details: {@Product}", product);
            return product;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving product with ID {ProductId}", id);
            throw;
        }
    }
    
    public async Task<bool> DeleteProductAsync(int id)
    {
        _logger.LogInformation("Attempting to delete product {ProductId}", id);
        
        try
        {
            await _repository.DeleteAsync(id);
            _logger.LogInformation("Successfully deleted product {ProductId}", id);
            return true;
        }
        catch (Exception ex)
        {
            _logger.LogCritical(ex, "Critical error deleting product {ProductId}", id);
            throw;
        }
    }
}
```

---

## Popular Logging Packages

### 1. Serilog (Most Popular) ⭐

**Why use Serilog?**
- Structured logging
- Multiple output sinks (file, database, cloud)
- Rich formatting
- Excellent performance

#### Installation

```bash
dotnet add package Serilog.AspNetCore
dotnet add package Serilog.Sinks.Console
dotnet add package Serilog.Sinks.File
dotnet add package Serilog.Sinks.Seq
```

#### Configuration in Program.cs

```csharp
using Serilog;

public class Program
{
    public static void Main(string[] args)
    {
        // Configure Serilog
        Log.Logger = new LoggerConfiguration()
            .MinimumLevel.Information()
            .MinimumLevel.Override("Microsoft", LogEventLevel.Warning)
            .Enrich.FromLogContext()
            .Enrich.WithMachineName()
            .Enrich.WithThreadId()
            .WriteTo.Console()
            .WriteTo.File(
                path: "logs/app-.txt",
                rollingInterval: RollingInterval.Day,
                outputTemplate: "{Timestamp:yyyy-MM-dd HH:mm:ss} [{Level}] {Message}{NewLine}{Exception}")
            .WriteTo.Seq("http://localhost:5341") // Optional: Seq server
            .CreateLogger();
        
        try
        {
            Log.Information("Starting web application");
            CreateHostBuilder(args).Build().Run();
        }
        catch (Exception ex)
        {
            Log.Fatal(ex, "Application terminated unexpectedly");
        }
        finally
        {
            Log.CloseAndFlush();
        }
    }
    
    public static IHostBuilder CreateHostBuilder(string[] args) =>
        Host.CreateDefaultBuilder(args)
            .UseSerilog() // Use Serilog instead of built-in logging
            .ConfigureWebHostDefaults(webBuilder =>
            {
                webBuilder.UseStartup<Startup>();
            });
}
```

#### appsettings.json for Serilog

```json
{
  "Serilog": {
    "Using": [ "Serilog.Sinks.Console", "Serilog.Sinks.File" ],
    "MinimumLevel": {
      "Default": "Information",
      "Override": {
        "Microsoft": "Warning",
        "System": "Warning"
      }
    },
    "WriteTo": [
      {
        "Name": "Console"
      },
      {
        "Name": "File",
        "Args": {
          "path": "logs/app-.txt",
          "rollingInterval": "Day",
          "outputTemplate": "{Timestamp:yyyy-MM-dd HH:mm:ss} [{Level}] {Message}{NewLine}{Exception}"
        }
      }
    ],
    "Enrich": [ "FromLogContext", "WithMachineName", "WithThreadId" ]
  }
}
```

#### Usage in Controller

```csharp
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    private readonly ILogger<ProductsController> _logger;
    private readonly IProductService _productService;
    
    public ProductsController(
        ILogger<ProductsController> logger,
        IProductService productService)
    {
        _logger = logger;
        _productService = productService;
    }
    
    [HttpGet("{id}")]
    public async Task<IActionResult> Get(int id)
    {
        _logger.LogInformation("GET request for product {ProductId} from {IpAddress}", 
            id, 
            HttpContext.Connection.RemoteIpAddress);
        
        try
        {
            var product = await _productService.GetProductAsync(id);
            
            if (product == null)
            {
                _logger.LogWarning("Product {ProductId} not found", id);
                return NotFound();
            }
            
            // Structured logging - logs the entire object
            _logger.LogInformation("Retrieved product: {@Product}", product);
            return Ok(product);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving product {ProductId}", id);
            return StatusCode(500, "Internal server error");
        }
    }
    
    [HttpPost]
    public async Task<IActionResult> Create([FromBody] CreateProductRequest request)
    {
        using (_logger.BeginScope("Creating product {ProductName}", request.Name))
        {
            _logger.LogInformation("Starting product creation");
            
            try
            {
                var product = await _productService.CreateAsync(request);
                _logger.LogInformation("Product created successfully with ID {ProductId}", product.Id);
                return CreatedAtAction(nameof(Get), new { id = product.Id }, product);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to create product");
                throw;
            }
        }
    }
}
```

---

### 2. NLog

#### Installation

```bash
dotnet add package NLog.Web.AspNetCore
```

#### nlog.config

```xml
<?xml version="1.0" encoding="utf-8" ?>
<nlog xmlns="http://www.nlog-project.org/schemas/NLog.xsd"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  
  <targets>
    <target name="logfile" xsi:type="File"
            fileName="logs/app-${shortdate}.log"
            layout="${longdate} ${level} ${message} ${exception}" />
    
    <target name="console" xsi:type="Console"
            layout="${longdate} ${level} ${message}" />
  </targets>
  
  <rules>
    <logger name="*" minlevel="Info" writeTo="logfile,console" />
  </rules>
</nlog>
```

#### Program.cs

```csharp
public static IHostBuilder CreateHostBuilder(string[] args) =>
    Host.CreateDefaultBuilder(args)
        .ConfigureLogging(logging =>
        {
            logging.ClearProviders();
            logging.SetMinimumLevel(LogLevel.Trace);
        })
        .UseNLog()
        .ConfigureWebHostDefaults(webBuilder =>
        {
            webBuilder.UseStartup<Startup>();
        });
```

---

## Logger Lifetime

```csharp
// In Startup.cs / Program.cs
public void ConfigureServices(IServiceCollection services)
{
    // ILogger<T> is registered as SINGLETON by default
    // You don't need to register it manually - it's built-in!
    
    // When you inject ILogger<T>, the DI container provides it automatically
}

// Usage
public class MyService
{
    private readonly ILogger<MyService> _logger;
    
    // ILogger is injected automatically
    public MyService(ILogger<MyService> logger)
    {
        _logger = logger; // This is a singleton instance
    }
}
```

**Lifetime: SINGLETON** - One logger instance per type throughout the application lifetime.

---

## Where Logs are Stored

### 1. Console Output
```csharp
.WriteTo.Console()
```
**Storage**: Terminal/Console window (not persisted)

### 2. File System
```csharp
.WriteTo.File(
    path: "logs/app-.txt",
    rollingInterval: RollingInterval.Day)
```
**Storage**: `logs/app-2026-05-26.txt`

### 3. Database (SQL Server)
```bash
dotnet add package Serilog.Sinks.MSSqlServer
```

```csharp
.WriteTo.MSSqlServer(
    connectionString: Configuration.GetConnectionString("DefaultConnection"),
    tableName: "Logs",
    autoCreateSqlTable: true)
```

### 4. Seq (Log Server)
```csharp
.WriteTo.Seq("http://localhost:5341")
```
**Storage**: Centralized log server with UI

### 5. Azure Application Insights
```bash
dotnet add package Serilog.Sinks.ApplicationInsights
```

```csharp
.WriteTo.ApplicationInsights(
    telemetryConfiguration: TelemetryConfiguration.CreateDefault(),
    telemetryConverter: TelemetryConverter.Traces)
```

### 6. Elasticsearch
```bash
dotnet add package Serilog.Sinks.Elasticsearch
```

```csharp
.WriteTo.Elasticsearch(new ElasticsearchSinkOptions(new Uri("http://localhost:9200"))
{
    AutoRegisterTemplate = true,
    IndexFormat = "applogs-{0:yyyy.MM}"
})
```

---

## Real-World Example: Complete Logging Setup

```csharp
// Program.cs
public class Program
{
    public static void Main(string[] args)
    {
        var configuration = new ConfigurationBuilder()
            .SetBasePath(Directory.GetCurrentDirectory())
            .AddJsonFile("appsettings.json")
            .Build();
        
        Log.Logger = new LoggerConfiguration()
            .ReadFrom.Configuration(configuration)
            .Enrich.WithProperty("Application", "ECommerceAPI")
            .Enrich.WithMachineName()
            .Enrich.WithEnvironmentName()
            .WriteTo.Console(
                outputTemplate: "[{Timestamp:HH:mm:ss} {Level:u3}] {Message:lj}{NewLine}{Exception}")
            .WriteTo.File(
                path: "logs/app-.txt",
                rollingInterval: RollingInterval.Day,
                retainedFileCountLimit: 30,
                outputTemplate: "{Timestamp:yyyy-MM-dd HH:mm:ss} [{Level}] [{SourceContext}] {Message}{NewLine}{Exception}")
            .WriteTo.MSSqlServer(
                connectionString: configuration.GetConnectionString("DefaultConnection"),
                tableName: "ApplicationLogs",
                autoCreateSqlTable: true)
            .CreateLogger();
        
        try
        {
            Log.Information("Application Starting");
            CreateHostBuilder(args).Build().Run();
        }
        catch (Exception ex)
        {
            Log.Fatal(ex, "Application failed to start");
        }
        finally
        {
            Log.CloseAndFlush();
        }
    }
}

// Service with logging
public class OrderService
{
    private readonly ILogger<OrderService> _logger;
    
    public async Task<Order> CreateOrderAsync(CreateOrderRequest request)
    {
        using (_logger.BeginScope(new Dictionary<string, object>
        {
            ["UserId"] = request.UserId,
            ["OrderTotal"] = request.Total
        }))
        {
            _logger.LogInformation("Creating order for user {UserId} with total {Total:C}", 
                request.UserId, 
                request.Total);
            
            // Business logic...
            
            _logger.LogInformation("Order {OrderId} created successfully", order.Id);
            return order;
        }
    }
}
```

---

## Best Practices

1. ✅ **Use structured logging** - `_logger.LogInformation("User {UserId}", userId)`
2. ✅ **Use appropriate log levels** - Don't log everything as Information
3. ✅ **Log exceptions properly** - `_logger.LogError(ex, "Message")`
4. ✅ **Use log scopes** for related operations
5. ✅ **Don't log sensitive data** (passwords, credit cards)
6. ✅ **Use rolling files** to prevent disk space issues
7. ✅ **Configure different levels** for dev vs production
8. ❌ **Don't overlog** - impacts performance
9. ❌ **Don't use string concatenation** - use structured logging

---

## Summary

**Logging Setup:**
1. Choose package: Serilog (recommended), NLog, or built-in
2. Configure in Program.cs
3. Inject `ILogger<T>` into classes
4. Use appropriate log levels
5. Store logs: File, Database, Cloud

**Logger Lifetime: SINGLETON**

**Common Sinks:**
- Console, File, Database, Seq, Application Insights, Elasticsearch

Proper logging is essential for monitoring, debugging, and maintaining production applications!
