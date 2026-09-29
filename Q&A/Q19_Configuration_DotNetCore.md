# Question 19: What is the configuration file in .NET Core? Why do we use it and how do you access configuration values?

## Answer

### What is Configuration in .NET Core?

**Configuration** in .NET Core is a flexible system for managing application settings from various sources like JSON files, environment variables, command-line arguments, and more.

Unlike .NET Framework's rigid `web.config`, .NET Core uses a modern, hierarchical configuration system.

---

## Configuration Sources (in order of precedence)

```
1. Command-line arguments (highest priority)
    ↓
2. Environment variables
    ↓
3. User secrets (Development only)
    ↓
4. appsettings.{Environment}.json
    ↓
5. appsettings.json (lowest priority)
```

**Later sources override earlier ones!**

---

## Main Configuration Files

### 1. `appsettings.json` (Base configuration)

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning"
    }
  },
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=MyDB;User Id=sa;Password=***;"
  },
  "AppSettings": {
    "ApplicationName": "My E-Commerce API",
    "MaxItemsPerPage": 50,
    "EnableCache": true
  },
  "Jwt": {
    "Key": "MySecretKey123456789",
    "Issuer": "MyApp",
    "Audience": "MyAppUsers",
    "ExpiryMinutes": 60
  },
  "EmailSettings": {
    "SmtpServer": "smtp.gmail.com",
    "Port": 587,
    "SenderEmail": "noreply@example.com",
    "SenderName": "My App"
  },
  "AllowedHosts": "*"
}
```

### 2. `appsettings.Development.json` (Development environment)

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Debug"
    }
  },
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=MyDB_Dev;User Id=sa;Password=dev123;"
  },
  "AppSettings": {
    "EnableCache": false
  }
}
```

### 3. `appsettings.Production.json` (Production environment)

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Warning"
    }
  },
  "ConnectionStrings": {
    "DefaultConnection": "Server=prod-server;Database=MyDB_Prod;User Id=sa;Password=***;"
  },
  "AppSettings": {
    "EnableCache": true
  }
}
```

---

## How to Access Configuration Values

### Method 1: Direct Access via IConfiguration

```csharp
public class ProductController : ControllerBase
{
    private readonly IConfiguration _configuration;
    
    public ProductController(IConfiguration configuration)
    {
        _configuration = configuration;
    }
    
    [HttpGet]
    public IActionResult GetSettings()
    {
        // Simple value
        var appName = _configuration["AppSettings:ApplicationName"];
        
        // Nested value
        var smtpServer = _configuration["EmailSettings:SmtpServer"];
        
        // Connection string
        var connString = _configuration.GetConnectionString("DefaultConnection");
        
        // With default value
        var maxItems = _configuration.GetValue<int>("AppSettings:MaxItemsPerPage", 10);
        
        return Ok(new
        {
            AppName = appName,
            SmtpServer = smtpServer,
            ConnectionString = connString,
            MaxItems = maxItems
        });
    }
}
```

### Method 2: Strongly-Typed Configuration (Recommended)

```csharp
// 1. Create configuration classes
public class AppSettings
{
    public string ApplicationName { get; set; }
    public int MaxItemsPerPage { get; set; }
    public bool EnableCache { get; set; }
}

public class JwtSettings
{
    public string Key { get; set; }
    public string Issuer { get; set; }
    public string Audience { get; set; }
    public int ExpiryMinutes { get; set; }
}

public class EmailSettings
{
    public string SmtpServer { get; set; }
    public int Port { get; set; }
    public string SenderEmail { get; set; }
    public string SenderName { get; set; }
}

// 2. Register in Startup.cs
public void ConfigureServices(IServiceCollection services)
{
    // Bind configuration sections to classes
    services.Configure<AppSettings>(Configuration.GetSection("AppSettings"));
    services.Configure<JwtSettings>(Configuration.GetSection("Jwt"));
    services.Configure<EmailSettings>(Configuration.GetSection("EmailSettings"));
    
    services.AddControllers();
}

// 3. Inject into controllers/services
public class ProductController : ControllerBase
{
    private readonly AppSettings _appSettings;
    private readonly JwtSettings _jwtSettings;
    
    public ProductController(
        IOptions<AppSettings> appSettings,
        IOptions<JwtSettings> jwtSettings)
    {
        _appSettings = appSettings.Value;
        _jwtSettings = jwtSettings.Value;
    }
    
    [HttpGet]
    public IActionResult GetConfig()
    {
        return Ok(new
        {
            AppName = _appSettings.ApplicationName,
            MaxItems = _appSettings.MaxItemsPerPage,
            CacheEnabled = _appSettings.EnableCache,
            JwtIssuer = _jwtSettings.Issuer
        });
    }
}
```

---

## Real-World Example: Database Configuration

```csharp
// appsettings.json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=ECommerce;Trusted_Connection=true;",
    "RedisConnection": "localhost:6379"
  },
  "Database": {
    "CommandTimeout": 30,
    "EnableRetryOnFailure": true,
    "MaxRetryCount": 3
  }
}

// Configuration class
public class DatabaseSettings
{
    public int CommandTimeout { get; set; }
    public bool EnableRetryOnFailure { get; set; }
    public int MaxRetryCount { get; set; }
}

// Startup.cs
public void ConfigureServices(IServiceCollection services)
{
    // Read connection string
    var connectionString = Configuration.GetConnectionString("DefaultConnection");
    
    // Bind database settings
    services.Configure<DatabaseSettings>(Configuration.GetSection("Database"));
    
    // Use in DbContext configuration
    services.AddDbContext<AppDbContext>((serviceProvider, options) =>
    {
        var dbSettings = serviceProvider.GetRequiredService<IOptions<DatabaseSettings>>().Value;
        
        options.UseSqlServer(connectionString, sqlOptions =>
        {
            sqlOptions.CommandTimeout(dbSettings.CommandTimeout);
            if (dbSettings.EnableRetryOnFailure)
            {
                sqlOptions.EnableRetryOnFailure(dbSettings.MaxRetryCount);
            }
        });
    });
}
```

---

## Environment-Specific Configuration

```csharp
// Program.cs or Startup.cs
public static IHostBuilder CreateHostBuilder(string[] args) =>
    Host.CreateDefaultBuilder(args)
        .ConfigureAppConfiguration((hostingContext, config) =>
        {
            var env = hostingContext.HostingEnvironment;
            
            config.AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
                  .AddJsonFile($"appsettings.{env.EnvironmentName}.json", optional: true, reloadOnChange: true)
                  .AddEnvironmentVariables()
                  .AddCommandLine(args);
            
            if (env.IsDevelopment())
            {
                config.AddUserSecrets<Program>(); // Secrets for development
            }
        })
        .ConfigureWebHostDefaults(webBuilder =>
        {
            webBuilder.UseStartup<Startup>();
        });
```

### Set Environment

```bash
# Windows
set ASPNETCORE_ENVIRONMENT=Development
set ASPNETCORE_ENVIRONMENT=Production

# Linux/Mac
export ASPNETCORE_ENVIRONMENT=Development

# In launchSettings.json
{
  "profiles": {
    "Development": {
      "environmentVariables": {
        "ASPNETCORE_ENVIRONMENT": "Development"
      }
    },
    "Production": {
      "environmentVariables": {
        "ASPNETCORE_ENVIRONMENT": "Production"
      }
    }
  }
}
```

---

## User Secrets (Development Only)

**Never store sensitive data in appsettings.json!**

### Initialize User Secrets

```bash
# In project directory
dotnet user-secrets init
dotnet user-secrets set "Jwt:Key" "MySecretKey123456"
dotnet user-secrets set "ConnectionStrings:DefaultConnection" "Server=localhost;..."
```

### Access in Code

```csharp
// Same as regular configuration
var jwtKey = _configuration["Jwt:Key"];
// In Development, reads from user secrets
// In Production, reads from environment variables or Azure Key Vault
```

---

## Environment Variables

```bash
# Set environment variable
set AppSettings__ApplicationName="My App"
set ConnectionStrings__DefaultConnection="Server=..."

# Note: Use double underscore (__) for nested values
```

```csharp
// Access in code (same way)
var appName = _configuration["AppSettings:ApplicationName"];
// Reads from environment variable if set, otherwise from appsettings.json
```

---

## Azure Key Vault (Production Secrets)

```csharp
public static IHostBuilder CreateHostBuilder(string[] args) =>
    Host.CreateDefaultBuilder(args)
        .ConfigureAppConfiguration((context, config) =>
        {
            if (context.HostingEnvironment.IsProduction())
            {
                var builtConfig = config.Build();
                var keyVaultEndpoint = builtConfig["KeyVault:Endpoint"];
                
                if (!string.IsNullOrEmpty(keyVaultEndpoint))
                {
                    var credential = new DefaultAzureCredential();
                    config.AddAzureKeyVault(new Uri(keyVaultEndpoint), credential);
                }
            }
        });
```

---

## Configuration Reload

```csharp
// appsettings.json changes are automatically reloaded
public void ConfigureServices(IServiceCollection services)
{
    services.Configure<AppSettings>(Configuration.GetSection("AppSettings"));
    
    // If you need to react to changes
    services.AddSingleton<IOptionsMonitor<AppSettings>>();
}

public class MyService
{
    private readonly IOptionsMonitor<AppSettings> _settings;
    
    public MyService(IOptionsMonitor<AppSettings> settings)
    {
        _settings = settings;
        
        // React to configuration changes
        _settings.OnChange(newSettings =>
        {
            Console.WriteLine($"Configuration changed: {newSettings.ApplicationName}");
        });
    }
    
    public void DoSomething()
    {
        // Always gets current value (even if appsettings.json changed)
        var currentSettings = _settings.CurrentValue;
    }
}
```

---

## IOptions vs IOptionsSnapshot vs IOptionsMonitor

```csharp
// IOptions<T> - Singleton, doesn't reload
services.Configure<AppSettings>(Configuration.GetSection("AppSettings"));
public MyService(IOptions<AppSettings> options)
{
    var settings = options.Value; // Same value throughout app lifetime
}

// IOptionsSnapshot<T> - Scoped, reloads per request
public MyController(IOptionsSnapshot<AppSettings> options)
{
    var settings = options.Value; // Reloaded for each HTTP request
}

// IOptionsMonitor<T> - Singleton, supports change notifications
public MyService(IOptionsMonitor<AppSettings> options)
{
    var settings = options.CurrentValue; // Always current value
    options.OnChange(s => { /* React to changes */ });
}
```

---

## Best Practices

1. ✅ **Use strongly-typed configuration** (`IOptions<T>`)
2. ✅ **Store sensitive data in User Secrets** (dev) or **Azure Key Vault** (prod)
3. ✅ **Use environment-specific files** (appsettings.Development.json)
4. ✅ **Never commit secrets** to source control
5. ✅ **Use environment variables** for deployment-specific settings
6. ✅ **Enable reloadOnChange** for appsettings.json
7. ❌ **Don't hardcode configuration** in code
8. ❌ **Don't store passwords** in appsettings.json

---

## Summary

**Configuration in .NET Core:**
- 📄 `appsettings.json` - Base configuration
- 📄 `appsettings.{Environment}.json` - Environment-specific
- 🔐 User Secrets - Development secrets
- 🌍 Environment Variables - Deployment settings
- ☁️ Azure Key Vault - Production secrets

**Access Methods:**
- Direct: `IConfiguration["Section:Key"]`
- Strongly-typed: `IOptions<T>`, `IOptionsSnapshot<T>`, `IOptionsMonitor<T>`

Configuration makes your application flexible, secure, and environment-aware!
