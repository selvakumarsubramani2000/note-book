# Clean Architecture in .NET: From Theory to Production

> **Real-world guide** to implementing Clean Architecture in ASP.NET Core applications  
> **Focus**: Practical folder structure, dependency flow, and integration with authentication

## Real-World Scenario

**The Problem**:
You're building an e-commerce platform. Initially, you put everything in Controllers:
- Business logic mixed with HTTP concerns
- Direct database calls from controllers
- Authentication logic scattered everywhere
- Impossible to test without spinning up the entire app
- Changing from SQL Server to PostgreSQL requires touching 50+ files

**The Impact**:
- New features take weeks instead of days
- Bugs in one area break unrelated features
- Testing is a nightmare
- Team members step on each other's toes
- Technical debt is crushing velocity

**The Solution**: Clean Architecture

---

## Table of Contents

1. [What is Clean Architecture?](#what-is-clean-architecture)
2. [The Dependency Rule](#the-dependency-rule)
3. [Layer Breakdown](#layer-breakdown)
4. [Folder Structure](#folder-structure)
5. [Practical Implementation](#practical-implementation)
6. [Integration with Authentication](#integration-with-authentication)
7. [Common Pitfalls](#common-pitfalls)
8. [Migration Strategy](#migration-strategy)
9. [When NOT to Use Clean Architecture](#when-not-to-use-clean-architecture)

---

## What is Clean Architecture?

**Clean Architecture** (also called Onion Architecture or Hexagonal Architecture) is a software design pattern that separates concerns into layers, with dependencies pointing inward toward the core business logic.

### The Core Principle

**"Business logic should not depend on infrastructure"**

Your business rules shouldn't care:
- What database you use (SQL Server, PostgreSQL, MongoDB)
- What web framework you use (ASP.NET Core, gRPC, Azure Functions)
- What external services you integrate with (SendGrid, Stripe, AWS)

### The Layers (From Inside Out)

```
┌─────────────────────────────────────────────┐
│         Infrastructure Layer                │  ← External concerns
│  (Database, Email, File System, APIs)       │
├─────────────────────────────────────────────┤
│         Presentation Layer                  │  ← HTTP, gRPC, CLI
│  (Controllers, SignalR Hubs, Minimal APIs)  │
├─────────────────────────────────────────────┤
│         Application Layer                   │  ← Use cases
│  (Services, Commands, Queries, DTOs)        │
├─────────────────────────────────────────────┤
│         Domain Layer                        │  ← Business logic
│  (Entities, Value Objects, Domain Events)   │  ← CORE (no dependencies)
└─────────────────────────────────────────────┘
```

**Key**: Dependencies point INWARD. Domain has zero dependencies. Application depends on Domain. Infrastructure depends on Application.

---

## The Dependency Rule

### ✅ Allowed Dependencies

```
Infrastructure → Application → Domain
Presentation → Application → Domain
```

### ❌ Forbidden Dependencies

```
Domain → Application  ❌
Domain → Infrastructure  ❌
Application → Infrastructure  ❌ (use interfaces!)
```

### How It Works in Practice

**Domain Layer** (Core):
```csharp
// Domain/Entities/Order.cs
// NO dependencies on anything!
public class Order
{
    public int Id { get; private set; }
    public decimal Total { get; private set; }
    public OrderStatus Status { get; private set; }
    
    // Business logic lives here
    public void MarkAsShipped()
    {
        if (Status != OrderStatus.Paid)
            throw new InvalidOperationException("Cannot ship unpaid order");
        
        Status = OrderStatus.Shipped;
    }
}
```

**Application Layer** (Use Cases):
```csharp
// Application/Orders/Commands/ShipOrderCommand.cs
// Depends on Domain, but NOT on Infrastructure
public class ShipOrderCommand : IRequest<Result>
{
    public int OrderId { get; set; }
}

public class ShipOrderCommandHandler : IRequestHandler<ShipOrderCommand, Result>
{
    private readonly IOrderRepository _orderRepository; // Interface!
    
    public ShipOrderCommandHandler(IOrderRepository orderRepository)
    {
        _orderRepository = orderRepository;
    }
    
    public async Task<Result> Handle(ShipOrderCommand request, CancellationToken ct)
    {
        var order = await _orderRepository.GetByIdAsync(request.OrderId);
        if (order == null) return Result.NotFound();
        
        order.MarkAsShipped(); // Business logic in domain
        await _orderRepository.UpdateAsync(order);
        
        return Result.Success();
    }
}
```

**Infrastructure Layer** (Implementation):
```csharp
// Infrastructure/Persistence/OrderRepository.cs
// Implements interface from Application layer
public class OrderRepository : IOrderRepository
{
    private readonly ApplicationDbContext _context;
    
    public OrderRepository(ApplicationDbContext context)
    {
        _context = context;
    }
    
    public async Task<Order> GetByIdAsync(int id)
    {
        return await _context.Orders.FindAsync(id);
    }
    
    public async Task UpdateAsync(Order order)
    {
        _context.Orders.Update(order);
        await _context.SaveChangesAsync();
    }
}
```

**Presentation Layer** (API):
```csharp
// API/Controllers/OrdersController.cs
// Depends on Application layer (via MediatR)
[ApiController]
[Route("api/[controller]")]
public class OrdersController : ControllerBase
{
    private readonly IMediator _mediator;
    
    public OrdersController(IMediator mediator)
    {
        _mediator = mediator;
    }
    
    [HttpPost("{id}/ship")]
    public async Task<IActionResult> ShipOrder(int id)
    {
        var result = await _mediator.Send(new ShipOrderCommand { OrderId = id });
        return result.IsSuccess ? Ok() : NotFound();
    }
}
```

**Notice**: 
- Controller doesn't know about database
- Application layer doesn't know about EF Core
- Domain has pure business logic
- Infrastructure is pluggable (swap SQL for Cosmos DB without touching business logic)

---

## Layer Breakdown

### 1. Domain Layer (Core)

**Purpose**: Contains business logic and rules

**What goes here**:
- ✅ Entities (Order, Product, User)
- ✅ Value Objects (Money, Address, Email)
- ✅ Domain Events (OrderPlaced, PaymentReceived)
- ✅ Enums (OrderStatus, PaymentMethod)
- ✅ Exceptions (DomainException, InvalidOrderException)
- ✅ Interfaces for domain services

**What DOESN'T go here**:
- ❌ Database code (EF Core, Dapper)
- ❌ HTTP code (controllers, middleware)
- ❌ External service calls (email, payment gateways)
- ❌ DTOs (those are in Application layer)

**Example Entity**:
```csharp
// Domain/Entities/Product.cs
public class Product
{
    public int Id { get; private set; }
    public string Name { get; private set; }
    public Money Price { get; private set; } // Value Object
    public int StockQuantity { get; private set; }
    
    // Factory method
    public static Product Create(string name, Money price, int initialStock)
    {
        if (string.IsNullOrWhiteSpace(name))
            throw new DomainException("Product name is required");
        
        if (price.Amount <= 0)
            throw new DomainException("Price must be positive");
        
        return new Product
        {
            Name = name,
            Price = price,
            StockQuantity = initialStock
        };
    }
    
    // Business logic
    public void ReduceStock(int quantity)
    {
        if (quantity > StockQuantity)
            throw new InsufficientStockException($"Only {StockQuantity} items available");
        
        StockQuantity -= quantity;
    }
    
    public void IncreaseStock(int quantity)
    {
        if (quantity <= 0)
            throw new DomainException("Quantity must be positive");
        
        StockQuantity += quantity;
    }
}
```

**Example Value Object**:
```csharp
// Domain/ValueObjects/Money.cs
public class Money : ValueObject
{
    public decimal Amount { get; private set; }
    public string Currency { get; private set; }
    
    public Money(decimal amount, string currency)
    {
        if (amount < 0)
            throw new DomainException("Amount cannot be negative");
        
        Amount = amount;
        Currency = currency ?? "USD";
    }
    
    public Money Add(Money other)
    {
        if (Currency != other.Currency)
            throw new DomainException("Cannot add different currencies");
        
        return new Money(Amount + other.Amount, Currency);
    }
    
    protected override IEnumerable<object> GetEqualityComponents()
    {
        yield return Amount;
        yield return Currency;
    }
}
```

### 2. Application Layer (Use Cases)

**Purpose**: Orchestrates business logic, defines use cases

**What goes here**:
- ✅ Commands (CreateOrderCommand, UpdateProductCommand)
- ✅ Queries (GetOrderByIdQuery, GetProductsQuery)
- ✅ Command/Query Handlers (using MediatR)
- ✅ DTOs (OrderDto, ProductDto)
- ✅ Interfaces for infrastructure (IOrderRepository, IEmailService)
- ✅ Validators (FluentValidation)
- ✅ Mappers (AutoMapper profiles)

**What DOESN'T go here**:
- ❌ HTTP concerns (status codes, routing)
- ❌ Database implementation (EF Core DbContext)
- ❌ External service implementation

**Example Command**:
```csharp
// Application/Orders/Commands/CreateOrder/CreateOrderCommand.cs
public class CreateOrderCommand : IRequest<Result<int>>
{
    public int UserId { get; set; }
    public List<OrderItemDto> Items { get; set; }
}

public class OrderItemDto
{
    public int ProductId { get; set; }
    public int Quantity { get; set; }
}
```

**Example Command Handler**:
```csharp
// Application/Orders/Commands/CreateOrder/CreateOrderCommandHandler.cs
public class CreateOrderCommandHandler : IRequestHandler<CreateOrderCommand, Result<int>>
{
    private readonly IOrderRepository _orderRepository;
    private readonly IProductRepository _productRepository;
    private readonly ICurrentUserService _currentUserService;
    
    public CreateOrderCommandHandler(
        IOrderRepository orderRepository,
        IProductRepository productRepository,
        ICurrentUserService currentUserService)
    {
        _orderRepository = orderRepository;
        _productRepository = productRepository;
        _currentUserService = currentUserService;
    }
    
    public async Task<Result<int>> Handle(CreateOrderCommand request, CancellationToken ct)
    {
        // 1. Validate user
        var userId = _currentUserService.UserId;
        if (userId != request.UserId)
            return Result<int>.Forbidden();
        
        // 2. Get products and validate stock
        var productIds = request.Items.Select(i => i.ProductId).ToList();
        var products = await _productRepository.GetByIdsAsync(productIds);
        
        foreach (var item in request.Items)
        {
            var product = products.FirstOrDefault(p => p.Id == item.ProductId);
            if (product == null)
                return Result<int>.NotFound($"Product {item.ProductId} not found");
            
            if (product.StockQuantity < item.Quantity)
                return Result<int>.BadRequest($"Insufficient stock for {product.Name}");
        }
        
        // 3. Create order (domain logic)
        var order = Order.Create(userId);
        foreach (var item in request.Items)
        {
            var product = products.First(p => p.Id == item.ProductId);
            order.AddItem(product, item.Quantity);
            product.ReduceStock(item.Quantity); // Domain logic
        }
        
        // 4. Save
        await _orderRepository.AddAsync(order);
        await _productRepository.UpdateRangeAsync(products);
        
        return Result<int>.Success(order.Id);
    }
}
```

**Example Query**:
```csharp
// Application/Orders/Queries/GetOrderById/GetOrderByIdQuery.cs
public class GetOrderByIdQuery : IRequest<Result<OrderDto>>
{
    public int OrderId { get; set; }
}

public class GetOrderByIdQueryHandler : IRequestHandler<GetOrderByIdQuery, Result<OrderDto>>
{
    private readonly IOrderRepository _orderRepository;
    private readonly IMapper _mapper;
    
    public GetOrderByIdQueryHandler(IOrderRepository orderRepository, IMapper mapper)
    {
        _orderRepository = orderRepository;
        _mapper = mapper;
    }
    
    public async Task<Result<OrderDto>> Handle(GetOrderByIdQuery request, CancellationToken ct)
    {
        var order = await _orderRepository.GetByIdAsync(request.OrderId);
        if (order == null)
            return Result<OrderDto>.NotFound();
        
        var dto = _mapper.Map<OrderDto>(order);
        return Result<OrderDto>.Success(dto);
    }
}
```

**Example Validator**:
```csharp
// Application/Orders/Commands/CreateOrder/CreateOrderCommandValidator.cs
public class CreateOrderCommandValidator : AbstractValidator<CreateOrderCommand>
{
    public CreateOrderCommandValidator()
    {
        RuleFor(x => x.UserId)
            .GreaterThan(0).WithMessage("User ID is required");

        RuleFor(x => x.Items)
            .NotEmpty().WithMessage("Order must have at least one item");

        RuleForEach(x => x.Items).ChildRules(item =>
        {
            item.RuleFor(x => x.ProductId)
                .GreaterThan(0).WithMessage("Product ID is required");

            item.RuleFor(x => x.Quantity)
                .GreaterThan(0).WithMessage("Quantity must be positive");
        });
    }
}
```

### 3. Infrastructure Layer (External Concerns)

**Purpose**: Implements interfaces defined in Application layer

**What goes here**:
- ✅ Database implementation (EF Core DbContext, repositories)
- ✅ External services (email, SMS, payment gateways)
- ✅ File system access
- ✅ Caching implementation (Redis)
- ✅ Message queue implementation (RabbitMQ, Azure Service Bus)
- ✅ Identity/Authentication implementation

**What DOESN'T go here**:
- ❌ Business logic (that's in Domain)
- ❌ Use case orchestration (that's in Application)

**Example DbContext**:
```csharp
// Infrastructure/Persistence/ApplicationDbContext.cs
public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    public DbSet<Order> Orders { get; set; }
    public DbSet<Product> Products { get; set; }
    public DbSet<User> Users { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Apply all configurations from assembly
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(ApplicationDbContext).Assembly);
    }
}
```

**Example Entity Configuration**:
```csharp
// Infrastructure/Persistence/Configurations/OrderConfiguration.cs
public class OrderConfiguration : IEntityTypeConfiguration<Order>
{
    public void Configure(EntityTypeBuilder<Order> builder)
    {
        builder.ToTable("Orders");

        builder.HasKey(o => o.Id);

        builder.Property(o => o.Status)
            .HasConversion<string>(); // Store enum as string

        // Value object mapping
        builder.OwnsOne(o => o.Total, money =>
        {
            money.Property(m => m.Amount).HasColumnName("TotalAmount");
            money.Property(m => m.Currency).HasColumnName("Currency");
        });

        // Relationships
        builder.HasMany(o => o.Items)
            .WithOne()
            .HasForeignKey("OrderId");
    }
}
```

**Example Repository Implementation**:
```csharp
// Infrastructure/Persistence/Repositories/OrderRepository.cs
public class OrderRepository : IOrderRepository
{
    private readonly ApplicationDbContext _context;

    public OrderRepository(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<Order?> GetByIdAsync(int id)
    {
        return await _context.Orders
            .Include(o => o.Items)
            .ThenInclude(i => i.Product)
            .FirstOrDefaultAsync(o => o.Id == id);
    }

    public async Task<List<Order>> GetByUserIdAsync(int userId)
    {
        return await _context.Orders
            .Where(o => o.UserId == userId)
            .Include(o => o.Items)
            .OrderByDescending(o => o.CreatedAt)
            .ToListAsync();
    }

    public async Task AddAsync(Order order)
    {
        await _context.Orders.AddAsync(order);
        await _context.SaveChangesAsync();
    }

    public async Task UpdateAsync(Order order)
    {
        _context.Orders.Update(order);
        await _context.SaveChangesAsync();
    }
}
```

**Example External Service**:
```csharp
// Infrastructure/Services/EmailService.cs
public class EmailService : IEmailService
{
    private readonly IConfiguration _configuration;
    private readonly ILogger<EmailService> _logger;

    public EmailService(IConfiguration configuration, ILogger<EmailService> logger)
    {
        _configuration = configuration;
        _logger = logger;
    }

    public async Task SendOrderConfirmationAsync(int orderId, string email)
    {
        try
        {
            // Implementation using SendGrid, SMTP, etc.
            var apiKey = _configuration["SendGrid:ApiKey"];
            var client = new SendGridClient(apiKey);

            var message = new SendGridMessage
            {
                From = new EmailAddress("noreply@myapp.com", "My App"),
                Subject = $"Order #{orderId} Confirmed",
                PlainTextContent = $"Your order #{orderId} has been confirmed."
            };
            message.AddTo(email);

            await client.SendEmailAsync(message);

            _logger.LogInformation("Order confirmation email sent for order {OrderId}", orderId);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to send order confirmation email for order {OrderId}", orderId);
            throw;
        }
    }
}
```

### 4. Presentation Layer (API)

**Purpose**: Handles HTTP concerns, routes requests to Application layer

**What goes here**:
- ✅ Controllers (or Minimal APIs)
- ✅ Middleware
- ✅ Filters
- ✅ SignalR Hubs
- ✅ gRPC services
- ✅ Request/Response models (different from DTOs!)

**What DOESN'T go here**:
- ❌ Business logic
- ❌ Database access
- ❌ Complex validation (use FluentValidation in Application layer)

**Example Controller**:
```csharp
// API/Controllers/OrdersController.cs
[ApiController]
[Route("api/[controller]")]
[Authorize] // Authentication from our previous guide!
public class OrdersController : ControllerBase
{
    private readonly IMediator _mediator;

    public OrdersController(IMediator mediator)
    {
        _mediator = mediator;
    }

    // POST: api/orders
    [HttpPost]
    public async Task<IActionResult> CreateOrder([FromBody] CreateOrderRequest request)
    {
        var command = new CreateOrderCommand
        {
            UserId = request.UserId,
            Items = request.Items.Select(i => new OrderItemDto
            {
                ProductId = i.ProductId,
                Quantity = i.Quantity
            }).ToList()
        };

        var result = await _mediator.Send(command);

        if (!result.IsSuccess)
            return result.ToActionResult(); // Extension method

        return CreatedAtAction(nameof(GetOrder), new { id = result.Value }, result.Value);
    }

    // GET: api/orders/{id}
    [HttpGet("{id}")]
    public async Task<IActionResult> GetOrder(int id)
    {
        var query = new GetOrderByIdQuery { OrderId = id };
        var result = await _mediator.Send(query);

        return result.ToActionResult();
    }

    // GET: api/orders/my-orders
    [HttpGet("my-orders")]
    public async Task<IActionResult> GetMyOrders()
    {
        var userId = User.GetUserId(); // Extension method from auth
        var query = new GetOrdersByUserIdQuery { UserId = userId };
        var result = await _mediator.Send(query);

        return result.ToActionResult();
    }

    // POST: api/orders/{id}/ship
    [HttpPost("{id}/ship")]
    [Authorize(Roles = "Admin")] // Admin only
    public async Task<IActionResult> ShipOrder(int id)
    {
        var command = new ShipOrderCommand { OrderId = id };
        var result = await _mediator.Send(command);

        return result.ToActionResult();
    }
}
```

**Notice**: Controller is thin! It just:
1. Maps HTTP request to Command/Query
2. Sends to MediatR
3. Maps result to HTTP response

All business logic is in Application/Domain layers.

---

## Folder Structure

### Complete Project Structure

```
MyApp/
├── src/
│   ├── MyApp.Domain/                    # Core business logic
│   │   ├── Entities/
│   │   │   ├── Order.cs
│   │   │   ├── Product.cs
│   │   │   └── User.cs
│   │   ├── ValueObjects/
│   │   │   ├── Money.cs
│   │   │   ├── Address.cs
│   │   │   └── Email.cs
│   │   ├── Enums/
│   │   │   ├── OrderStatus.cs
│   │   │   └── PaymentMethod.cs
│   │   ├── Events/
│   │   │   ├── OrderPlacedEvent.cs
│   │   │   └── PaymentReceivedEvent.cs
│   │   ├── Exceptions/
│   │   │   ├── DomainException.cs
│   │   │   └── InsufficientStockException.cs
│   │   └── MyApp.Domain.csproj
│   │
│   ├── MyApp.Application/               # Use cases
│   │   ├── Common/
│   │   │   ├── Interfaces/
│   │   │   │   ├── IOrderRepository.cs
│   │   │   │   ├── IProductRepository.cs
│   │   │   │   ├── IEmailService.cs
│   │   │   │   └── ICurrentUserService.cs
│   │   │   ├── Models/
│   │   │   │   └── Result.cs
│   │   │   ├── Behaviors/
│   │   │   │   ├── ValidationBehavior.cs
│   │   │   │   └── LoggingBehavior.cs
│   │   │   └── Mappings/
│   │   │       └── MappingProfile.cs
│   │   ├── Orders/
│   │   │   ├── Commands/
│   │   │   │   ├── CreateOrder/
│   │   │   │   │   ├── CreateOrderCommand.cs
│   │   │   │   │   ├── CreateOrderCommandHandler.cs
│   │   │   │   │   └── CreateOrderCommandValidator.cs
│   │   │   │   └── ShipOrder/
│   │   │   │       ├── ShipOrderCommand.cs
│   │   │   │       └── ShipOrderCommandHandler.cs
│   │   │   ├── Queries/
│   │   │   │   ├── GetOrderById/
│   │   │   │   │   ├── GetOrderByIdQuery.cs
│   │   │   │   │   └── GetOrderByIdQueryHandler.cs
│   │   │   │   └── GetOrdersByUserId/
│   │   │   │       ├── GetOrdersByUserIdQuery.cs
│   │   │   │       └── GetOrdersByUserIdQueryHandler.cs
│   │   │   └── DTOs/
│   │   │       ├── OrderDto.cs
│   │   │       └── OrderItemDto.cs
│   │   ├── Products/
│   │   │   ├── Commands/
│   │   │   ├── Queries/
│   │   │   └── DTOs/
│   │   └── MyApp.Application.csproj
│   │
│   ├── MyApp.Infrastructure/            # External concerns
│   │   ├── Persistence/
│   │   │   ├── ApplicationDbContext.cs
│   │   │   ├── Configurations/
│   │   │   │   ├── OrderConfiguration.cs
│   │   │   │   └── ProductConfiguration.cs
│   │   │   ├── Repositories/
│   │   │   │   ├── OrderRepository.cs
│   │   │   │   └── ProductRepository.cs
│   │   │   └── Migrations/
│   │   ├── Services/
│   │   │   ├── EmailService.cs
│   │   │   ├── CurrentUserService.cs
│   │   │   └── DateTimeService.cs
│   │   ├── Identity/
│   │   │   ├── IdentityService.cs
│   │   │   └── JwtService.cs
│   │   ├── Caching/
│   │   │   └── RedisCacheService.cs
│   │   └── MyApp.Infrastructure.csproj
│   │
│   └── MyApp.API/                       # Presentation
│       ├── Controllers/
│       │   ├── OrdersController.cs
│       │   ├── ProductsController.cs
│       │   └── AuthController.cs
│       ├── Middleware/
│       │   ├── ExceptionHandlingMiddleware.cs
│       │   └── RequestLoggingMiddleware.cs
│       ├── Filters/
│       │   └── ValidationFilter.cs
│       ├── Extensions/
│       │   ├── ResultExtensions.cs
│       │   └── UserExtensions.cs
│       ├── Program.cs
│       ├── appsettings.json
│       └── MyApp.API.csproj
│
└── tests/
    ├── MyApp.Domain.Tests/
    ├── MyApp.Application.Tests/
    ├── MyApp.Infrastructure.Tests/
    └── MyApp.API.Tests/
```

### Project Dependencies

```
MyApp.API
  ├─> MyApp.Application
  └─> MyApp.Infrastructure

MyApp.Infrastructure
  └─> MyApp.Application

MyApp.Application
  └─> MyApp.Domain

MyApp.Domain
  └─> (no dependencies!)
```

**Verify with**:
```bash
dotnet list package --include-transitive
```

---

## Practical Implementation

### Step 1: Create Projects

```bash
# Create solution
dotnet new sln -n MyApp

# Create projects
dotnet new classlib -n MyApp.Domain
dotnet new classlib -n MyApp.Application
dotnet new classlib -n MyApp.Infrastructure
dotnet new webapi -n MyApp.API

# Add to solution
dotnet sln add MyApp.Domain/MyApp.Domain.csproj
dotnet sln add MyApp.Application/MyApp.Application.csproj
dotnet sln add MyApp.Infrastructure/MyApp.Infrastructure.csproj
dotnet sln add MyApp.API/MyApp.API.csproj

# Set up dependencies
cd MyApp.Application
dotnet add reference ../MyApp.Domain/MyApp.Domain.csproj

cd ../MyApp.Infrastructure
dotnet add reference ../MyApp.Application/MyApp.Application.csproj

cd ../MyApp.API
dotnet add reference ../MyApp.Application/MyApp.Application.csproj
dotnet add reference ../MyApp.Infrastructure/MyApp.Infrastructure.csproj
```

### Step 2: Install NuGet Packages

**MyApp.Application**:
```bash
dotnet add package MediatR
dotnet add package FluentValidation
dotnet add package AutoMapper
```

**MyApp.Infrastructure**:
```bash
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
dotnet add package Microsoft.EntityFrameworkCore.Tools
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
```

**MyApp.API**:
```bash
dotnet add package MediatR.Extensions.Microsoft.DependencyInjection
dotnet add package FluentValidation.AspNetCore
dotnet add package Serilog.AspNetCore
```

### Step 3: Configure Dependency Injection

**Program.cs**:
```csharp
using MyApp.Application;
using MyApp.Infrastructure;

var builder = WebApplication.CreateBuilder(args);

// Add services
builder.Services.AddControllers();

// Application layer
builder.Services.AddApplication(); // Extension method

// Infrastructure layer
builder.Services.AddInfrastructure(builder.Configuration); // Extension method

// API layer
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Middleware pipeline
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

**Application Layer DI** (`MyApp.Application/DependencyInjection.cs`):
```csharp
using System.Reflection;
using FluentValidation;
using MediatR;
using Microsoft.Extensions.DependencyInjection;

namespace MyApp.Application;

public static class DependencyInjection
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        // MediatR
        services.AddMediatR(cfg => cfg.RegisterServicesFromAssembly(Assembly.GetExecutingAssembly()));

        // FluentValidation
        services.AddValidatorsFromAssembly(Assembly.GetExecutingAssembly());

        // AutoMapper
        services.AddAutoMapper(Assembly.GetExecutingAssembly());

        // Pipeline behaviors
        services.AddTransient(typeof(IPipelineBehavior<,>), typeof(ValidationBehavior<,>));
        services.AddTransient(typeof(IPipelineBehavior<,>), typeof(LoggingBehavior<,>));

        return services;
    }
}
```

**Infrastructure Layer DI** (`MyApp.Infrastructure/DependencyInjection.cs`):
```csharp
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using MyApp.Application.Common.Interfaces;
using MyApp.Infrastructure.Persistence;
using MyApp.Infrastructure.Persistence.Repositories;
using MyApp.Infrastructure.Services;

namespace MyApp.Infrastructure;

public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        // Database
        services.AddDbContext<ApplicationDbContext>(options =>
            options.UseSqlServer(configuration.GetConnectionString("DefaultConnection")));

        // Repositories
        services.AddScoped<IOrderRepository, OrderRepository>();
        services.AddScoped<IProductRepository, ProductRepository>();

        // Services
        services.AddScoped<IEmailService, EmailService>();
        services.AddScoped<ICurrentUserService, CurrentUserService>();
        services.AddSingleton<IDateTimeService, DateTimeService>();

        // Caching
        services.AddStackExchangeRedisCache(options =>
        {
            options.Configuration = configuration.GetConnectionString("Redis");
        });

        // Authentication (from our previous guide!)
        services.AddAuthentication(/* JWT config */);

        return services;
    }
}
```

### Step 4: Implement Result Pattern

**Common/Models/Result.cs**:
```csharp
// Application/Common/Models/Result.cs
public class Result
{
    public bool IsSuccess { get; }
    public string Error { get; }
    public int StatusCode { get; }

    protected Result(bool isSuccess, string error, int statusCode = 200)
    {
        IsSuccess = isSuccess;
        Error = error;
        StatusCode = statusCode;
    }

    public static Result Success() => new Result(true, string.Empty, 200);
    public static Result NotFound(string message = "Resource not found")
        => new Result(false, message, 404);
    public static Result BadRequest(string message)
        => new Result(false, message, 400);
    public static Result Forbidden(string message = "Forbidden")
        => new Result(false, message, 403);
    public static Result Unauthorized(string message = "Unauthorized")
        => new Result(false, message, 401);
}

public class Result<T> : Result
{
    public T Value { get; }

    private Result(bool isSuccess, T value, string error, int statusCode)
        : base(isSuccess, error, statusCode)
    {
        Value = value;
    }

    public static Result<T> Success(T value)
        => new Result<T>(true, value, string.Empty, 200);
    public static new Result<T> NotFound(string message = "Resource not found")
        => new Result<T>(false, default, message, 404);
    public static new Result<T> BadRequest(string message)
        => new Result<T>(false, default, message, 400);
    public static new Result<T> Forbidden(string message = "Forbidden")
        => new Result<T>(false, default, message, 403);
}
```

**Extension for Controllers**:
```csharp
// API/Extensions/ResultExtensions.cs
public static class ResultExtensions
{
    public static IActionResult ToActionResult(this Result result)
    {
        if (result.IsSuccess)
            return new OkResult();

        return result.StatusCode switch
        {
            404 => new NotFoundObjectResult(new { error = result.Error }),
            400 => new BadRequestObjectResult(new { error = result.Error }),
            403 => new ObjectResult(new { error = result.Error }) { StatusCode = 403 },
            401 => new UnauthorizedObjectResult(new { error = result.Error }),
            _ => new ObjectResult(new { error = result.Error }) { StatusCode = result.StatusCode }
        };
    }

    public static IActionResult ToActionResult<T>(this Result<T> result)
    {
        if (result.IsSuccess)
            return new OkObjectResult(result.Value);

        return ((Result)result).ToActionResult();
    }
}
```

---

## Integration with Authentication

Clean Architecture integrates beautifully with the authentication system we built earlier. Here's how:

### 1. Current User Service

**Interface** (in Application layer):
```csharp
// Application/Common/Interfaces/ICurrentUserService.cs
public interface ICurrentUserService
{
    int? UserId { get; }
    string? Email { get; }
    string? Role { get; }
    bool IsAuthenticated { get; }
    bool IsAdmin { get; }
}
```

**Implementation** (in Infrastructure layer):
```csharp
// Infrastructure/Services/CurrentUserService.cs
public class CurrentUserService : ICurrentUserService
{
    private readonly IHttpContextAccessor _httpContextAccessor;

    public CurrentUserService(IHttpContextAccessor httpContextAccessor)
    {
        _httpContextAccessor = httpContextAccessor;
    }

    public int? UserId
    {
        get
        {
            var userIdClaim = _httpContextAccessor.HttpContext?.User
                .FindFirst(ClaimTypes.NameIdentifier)?.Value;

            return int.TryParse(userIdClaim, out var userId) ? userId : null;
        }
    }

    public string? Email => _httpContextAccessor.HttpContext?.User
        .FindFirst(ClaimTypes.Email)?.Value;

    public string? Role => _httpContextAccessor.HttpContext?.User
        .FindFirst(ClaimTypes.Role)?.Value;

    public bool IsAuthenticated => _httpContextAccessor.HttpContext?.User?.Identity?.IsAuthenticated ?? false;

    public bool IsAdmin => Role == "Admin";
}
```

**Usage in Command Handler**:
```csharp
public class CreateOrderCommandHandler : IRequestHandler<CreateOrderCommand, Result<int>>
{
    private readonly IOrderRepository _orderRepository;
    private readonly ICurrentUserService _currentUserService;

    public async Task<Result<int>> Handle(CreateOrderCommand request, CancellationToken ct)
    {
        // Ensure user can only create orders for themselves
        if (_currentUserService.UserId != request.UserId)
            return Result<int>.Forbidden("Cannot create order for another user");

        // ... rest of logic
    }
}
```

### 2. Authorization in Application Layer

**Policy-based authorization**:
```csharp
// Application/Orders/Commands/DeleteOrder/DeleteOrderCommand.cs
public class DeleteOrderCommandHandler : IRequestHandler<DeleteOrderCommand, Result>
{
    private readonly IOrderRepository _orderRepository;
    private readonly ICurrentUserService _currentUserService;

    public async Task<Result> Handle(DeleteOrderCommand request, CancellationToken ct)
    {
        var order = await _orderRepository.GetByIdAsync(request.OrderId);
        if (order == null)
            return Result.NotFound();

        // Resource-based authorization: Users can only delete their own orders
        // OR admins can delete any order
        if (order.UserId != _currentUserService.UserId && !_currentUserService.IsAdmin)
            return Result.Forbidden("You can only delete your own orders");

        await _orderRepository.DeleteAsync(order);
        return Result.Success();
    }
}
```

### 3. Authentication in Infrastructure

**JWT Service** (from our auth guide, now in Infrastructure):
```csharp
// Infrastructure/Identity/JwtService.cs
public class JwtService : IJwtService
{
    // Implementation from authentication guide
    public string GenerateToken(User user) { /* ... */ }
}
```

**Register in DI**:
```csharp
// Infrastructure/DependencyInjection.cs
services.AddScoped<IJwtService, JwtService>();
services.AddScoped<ICurrentUserService, CurrentUserService>();
services.AddHttpContextAccessor(); // Required for CurrentUserService
```

---

## Common Pitfalls

### 1. ❌ Putting Business Logic in Controllers

**Wrong**:
```csharp
[HttpPost]
public async Task<IActionResult> CreateOrder([FromBody] CreateOrderRequest request)
{
    // ❌ Business logic in controller!
    var order = new Order
    {
        UserId = request.UserId,
        Total = 0
    };

    foreach (var item in request.Items)
    {
        var product = await _context.Products.FindAsync(item.ProductId);
        if (product.StockQuantity < item.Quantity)
            return BadRequest("Insufficient stock");

        order.Total += product.Price * item.Quantity;
        product.StockQuantity -= item.Quantity;
    }

    _context.Orders.Add(order);
    await _context.SaveChangesAsync();

    return Ok(order.Id);
}
```

**Right**:
```csharp
[HttpPost]
public async Task<IActionResult> CreateOrder([FromBody] CreateOrderRequest request)
{
    // ✅ Delegate to Application layer
    var command = new CreateOrderCommand { /* ... */ };
    var result = await _mediator.Send(command);
    return result.ToActionResult();
}
```

### 2. ❌ Application Layer Depending on Infrastructure

**Wrong**:
```csharp
// Application/Orders/Commands/CreateOrderCommandHandler.cs
public class CreateOrderCommandHandler
{
    private readonly ApplicationDbContext _context; // ❌ Direct dependency on EF Core!

    public async Task<Result> Handle(CreateOrderCommand request)
    {
        var order = new Order();
        _context.Orders.Add(order); // ❌ Application knows about DbContext
        await _context.SaveChangesAsync();
    }
}
```

**Right**:
```csharp
// Application/Orders/Commands/CreateOrderCommandHandler.cs
public class CreateOrderCommandHandler
{
    private readonly IOrderRepository _orderRepository; // ✅ Depends on interface

    public async Task<Result> Handle(CreateOrderCommand request)
    {
        var order = new Order();
        await _orderRepository.AddAsync(order); // ✅ Application doesn't know about EF Core
    }
}
```

### 3. ❌ Anemic Domain Model

**Wrong**:
```csharp
// ❌ Anemic: Just a data container, no behavior
public class Order
{
    public int Id { get; set; }
    public decimal Total { get; set; }
    public OrderStatus Status { get; set; }
}

// Business logic in service instead of domain
public class OrderService
{
    public void ShipOrder(Order order)
    {
        if (order.Status != OrderStatus.Paid)
            throw new Exception("Cannot ship unpaid order");

        order.Status = OrderStatus.Shipped;
    }
}
```

**Right**:
```csharp
// ✅ Rich domain model: Behavior lives with data
public class Order
{
    public int Id { get; private set; }
    public decimal Total { get; private set; }
    public OrderStatus Status { get; private set; }

    // Business logic in domain
    public void MarkAsShipped()
    {
        if (Status != OrderStatus.Paid)
            throw new InvalidOperationException("Cannot ship unpaid order");

        Status = OrderStatus.Shipped;
    }
}
```

### 4. ❌ Over-Engineering Simple Apps

**When NOT to use Clean Architecture**:
- ✅ Simple CRUD apps with no business logic
- ✅ Prototypes or MVPs
- ✅ Internal tools with < 10 endpoints
- ✅ Apps that will never scale or change

**Use Clean Architecture when**:
- ✅ Complex business rules
- ✅ Long-term maintenance expected
- ✅ Multiple teams working on codebase
- ✅ Need to swap infrastructure (database, external services)
- ✅ High testability requirements

### 5. ❌ Not Using MediatR Properly

**Wrong**:
```csharp
// ❌ Injecting multiple handlers directly
public class OrdersController
{
    private readonly CreateOrderCommandHandler _createHandler;
    private readonly GetOrderQueryHandler _getHandler;
    private readonly UpdateOrderCommandHandler _updateHandler;
    // ... 20 more handlers
}
```

**Right**:
```csharp
// ✅ Use MediatR to decouple
public class OrdersController
{
    private readonly IMediator _mediator;

    public OrdersController(IMediator mediator)
    {
        _mediator = mediator;
    }

    public async Task<IActionResult> CreateOrder(CreateOrderRequest request)
    {
        var result = await _mediator.Send(new CreateOrderCommand { /* ... */ });
        return result.ToActionResult();
    }
}
```

---

## Migration Strategy

### Migrating from Monolithic to Clean Architecture

**Scenario**: You have an existing ASP.NET Core app with everything in Controllers. How do you migrate?

### Step 1: Create New Projects (Don't Touch Existing Code Yet)

```bash
dotnet new classlib -n MyApp.Domain
dotnet new classlib -n MyApp.Application
dotnet new classlib -n MyApp.Infrastructure
```

### Step 2: Extract Domain Entities

**Before** (in Controllers):
```csharp
public class Order
{
    public int Id { get; set; }
    public decimal Total { get; set; }
    // ... mixed with EF Core attributes
}
```

**After** (move to Domain):
```csharp
// MyApp.Domain/Entities/Order.cs
public class Order
{
    public int Id { get; private set; }
    public decimal Total { get; private set; }

    public void CalculateTotal(List<OrderItem> items)
    {
        Total = items.Sum(i => i.Price * i.Quantity);
    }
}
```

### Step 3: Create Interfaces in Application Layer

```csharp
// MyApp.Application/Common/Interfaces/IOrderRepository.cs
public interface IOrderRepository
{
    Task<Order?> GetByIdAsync(int id);
    Task AddAsync(Order order);
    Task UpdateAsync(Order order);
}
```

### Step 4: Implement Repositories in Infrastructure

```csharp
// MyApp.Infrastructure/Persistence/Repositories/OrderRepository.cs
public class OrderRepository : IOrderRepository
{
    private readonly ApplicationDbContext _context;

    // Move existing DbContext code here
    public async Task<Order?> GetByIdAsync(int id)
    {
        return await _context.Orders.FindAsync(id);
    }
}
```

### Step 5: Create Commands/Queries (One Endpoint at a Time)

**Before**:
```csharp
[HttpPost]
public async Task<IActionResult> CreateOrder(CreateOrderRequest request)
{
    // 100 lines of code in controller
}
```

**After**:
```csharp
// 1. Create command
public class CreateOrderCommand : IRequest<Result<int>>
{
    public int UserId { get; set; }
    public List<OrderItemDto> Items { get; set; }
}

// 2. Create handler
public class CreateOrderCommandHandler : IRequestHandler<CreateOrderCommand, Result<int>>
{
    // Move logic from controller here
}

// 3. Update controller
[HttpPost]
public async Task<IActionResult> CreateOrder(CreateOrderRequest request)
{
    var command = new CreateOrderCommand { /* ... */ };
    var result = await _mediator.Send(command);
    return result.ToActionResult();
}
```

### Step 6: Migrate Incrementally

**Don't rewrite everything at once!** Migrate one feature at a time:

1. Week 1: Migrate Orders module
2. Week 2: Migrate Products module
3. Week 3: Migrate Users module
4. etc.

**Both old and new code can coexist**:
```csharp
// Old endpoint (not migrated yet)
[HttpGet("old-way")]
public async Task<IActionResult> GetProductsOldWay()
{
    var products = await _context.Products.ToListAsync();
    return Ok(products);
}

// New endpoint (migrated to Clean Architecture)
[HttpGet("new-way")]
public async Task<IActionResult> GetProductsNewWay()
{
    var result = await _mediator.Send(new GetProductsQuery());
    return result.ToActionResult();
}
```

---

## When NOT to Use Clean Architecture

### ❌ Don't Use Clean Architecture If:

1. **Simple CRUD app with no business logic**
   - Example: Admin panel to manage database records
   - Better approach: Use ASP.NET Core with EF Core directly

2. **Prototype or MVP**
   - Speed is more important than architecture
   - You're validating an idea, not building for production

3. **Very small team (1-2 developers)**
   - Overhead might not be worth it
   - Consider simpler layered architecture

4. **App will never change or scale**
   - Internal tool used by 5 people
   - No plans for new features

5. **Tight deadline**
   - Clean Architecture has upfront cost
   - Pay off comes over time

### ✅ Use Clean Architecture If:

1. **Complex business rules**
   - E-commerce, banking, healthcare
   - Domain logic is core value

2. **Long-term maintenance**
   - App will be maintained for years
   - Multiple teams will work on it

3. **Need to swap infrastructure**
   - Might change database
   - Might change external services

4. **High testability requirements**
   - Need unit tests for business logic
   - Integration tests for infrastructure

5. **Multiple clients**
   - Web API, mobile app, desktop app
   - Business logic shared across clients

---

## Summary

### Key Takeaways

1. **Clean Architecture separates concerns** into layers: Domain, Application, Infrastructure, Presentation

2. **Dependencies point inward**: Domain has no dependencies, Application depends on Domain, Infrastructure implements Application interfaces

3. **Domain layer** contains business logic and has zero dependencies

4. **Application layer** orchestrates use cases using Commands/Queries (CQRS pattern)

5. **Infrastructure layer** implements interfaces defined in Application (repositories, external services)

6. **Presentation layer** is thin - just maps HTTP to Commands/Queries

7. **Use MediatR** to decouple controllers from handlers

8. **Integrate with authentication** via ICurrentUserService interface

9. **Migrate incrementally** - don't rewrite everything at once

10. **Don't over-engineer** - Clean Architecture has overhead, use it when benefits outweigh costs

### Benefits

✅ **Testability**: Business logic can be tested without database or HTTP
✅ **Maintainability**: Changes are localized to specific layers
✅ **Flexibility**: Easy to swap infrastructure (database, external services)
✅ **Scalability**: Clear separation makes it easier to scale teams
✅ **Independence**: Business logic doesn't depend on frameworks

### Costs

❌ **More files**: More projects, folders, interfaces
❌ **Learning curve**: Team needs to understand the pattern
❌ **Upfront time**: Takes longer to set up initially
❌ **Overkill for simple apps**: Not worth it for basic CRUD

---

## Next Steps

1. **Implement a sample project** using the folder structure above
2. **Read about SOLID principles** to understand why Clean Architecture works
3. **Learn CQRS pattern** (Commands vs Queries) in depth
4. **Explore MediatR** pipeline behaviors for cross-cutting concerns
5. **Study Domain-Driven Design** for complex domain modeling

### Related Guides

- **SOLID Principles in Practice** - Deep dive into SOLID with .NET examples
- **CQRS & Event Sourcing** - When and how to implement
- **Repository Pattern vs Direct EF Core** - Pros and cons
- **Dependency Injection Best Practices** - Service lifetimes and common pitfalls

---

**Remember**: Clean Architecture is a tool, not a religion. Use it when it makes sense, skip it when it doesn't. The goal is to build maintainable software, not to follow patterns blindly. 🏗️
```
```
