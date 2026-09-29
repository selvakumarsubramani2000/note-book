# API Design in .NET: REST, GraphQL, and gRPC

> **Production-ready guide** to designing scalable, maintainable APIs  
> **Focus**: RESTful principles, API versioning, when to use GraphQL vs gRPC, and real-world trade-offs

## Real-World Scenario

**The Problem**:
You're building an e-commerce platform. You need to decide:
- Should you use REST, GraphQL, or gRPC?
- How do you version your API without breaking existing clients?
- How do you handle pagination, filtering, and sorting?
- What HTTP status codes should you use?
- How do you design endpoints that are intuitive and consistent?

**The Impact of Poor API Design**:
- Breaking changes force clients to update immediately
- Inconsistent endpoints confuse developers
- Over-fetching wastes bandwidth
- Under-fetching requires multiple requests
- Poor error messages make debugging impossible

**The Goal**: Design an API that is intuitive, consistent, versioned, and performant

---

## Table of Contents

1. [RESTful API Design](#restful-api-design)
2. [API Versioning Strategies](#api-versioning-strategies)
3. [Pagination, Filtering, Sorting](#pagination-filtering-sorting)
4. [Error Handling](#error-handling)
5. [GraphQL vs REST](#graphql-vs-rest)
6. [gRPC for Microservices](#grpc-for-microservices)
7. [API Documentation](#api-documentation)

---

## RESTful API Design

### REST Principles

**REST** = Representational State Transfer

**Core principles**:
1. **Resources** - Everything is a resource (Product, Order, User)
2. **HTTP Methods** - Use standard methods (GET, POST, PUT, DELETE)
3. **Stateless** - Each request contains all information needed
4. **Uniform Interface** - Consistent naming and structure

### Resource Naming

**✅ Good naming**:
```
GET    /api/products              # Get all products
GET    /api/products/{id}         # Get single product
POST   /api/products              # Create product
PUT    /api/products/{id}         # Update product
DELETE /api/products/{id}         # Delete product

GET    /api/products/{id}/reviews # Get reviews for product
POST   /api/products/{id}/reviews # Add review to product
```

**❌ Bad naming**:
```
GET    /api/getAllProducts        # Don't use verbs in URL
GET    /api/product/{id}          # Use plural (products, not product)
POST   /api/createProduct         # HTTP method already indicates action
GET    /api/products/delete/{id}  # Use DELETE method, not GET
```

### HTTP Methods

| Method | Purpose | Idempotent | Safe | Example |
|--------|---------|------------|------|---------|
| **GET** | Retrieve resource | ✅ | ✅ | Get product details |
| **POST** | Create resource | ❌ | ❌ | Create new order |
| **PUT** | Update/Replace resource | ✅ | ❌ | Update entire product |
| **PATCH** | Partial update | ❌ | ❌ | Update product price |
| **DELETE** | Delete resource | ✅ | ❌ | Delete product |

**Idempotent**: Multiple identical requests have same effect as single request  
**Safe**: Doesn't modify resource

### HTTP Status Codes

**Success (2xx)**:
- **200 OK** - Request succeeded (GET, PUT, PATCH)
- **201 Created** - Resource created (POST)
- **204 No Content** - Success but no response body (DELETE)

**Client Errors (4xx)**:
- **400 Bad Request** - Invalid request (validation failed)
- **401 Unauthorized** - Not authenticated
- **403 Forbidden** - Authenticated but not authorized
- **404 Not Found** - Resource doesn't exist
- **409 Conflict** - Conflict with current state (duplicate)
- **422 Unprocessable Entity** - Validation failed

**Server Errors (5xx)**:
- **500 Internal Server Error** - Unexpected error
- **503 Service Unavailable** - Service temporarily down

### Example: Products API

```csharp
[ApiController]
[Route("api/v1/products")]
public class ProductsController : ControllerBase
{
    private readonly IMediator _mediator;
    
    public ProductsController(IMediator mediator)
    {
        _mediator = mediator;
    }
    
    // GET: api/v1/products
    [HttpGet]
    [ProducesResponseType(typeof(PagedResult<ProductDto>), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetProducts(
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 20,
        [FromQuery] string? category = null,
        [FromQuery] decimal? minPrice = null,
        [FromQuery] decimal? maxPrice = null,
        [FromQuery] string? sortBy = "name",
        [FromQuery] string? sortOrder = "asc")
    {
        var query = new GetProductsQuery
        {
            Page = page,
            PageSize = pageSize,
            Category = category,
            MinPrice = minPrice,
            MaxPrice = maxPrice,
            SortBy = sortBy,
            SortOrder = sortOrder
        };
        
        var result = await _mediator.Send(query);
        return Ok(result);
    }
    
    // GET: api/v1/products/{id}
    [HttpGet("{id}")]
    [ProducesResponseType(typeof(ProductDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetProduct(int id)
    {
        var query = new GetProductByIdQuery { ProductId = id };
        var result = await _mediator.Send(query);
        
        if (result == null)
            return NotFound(new { error = $"Product {id} not found" });
        
        return Ok(result);
    }
    
    // POST: api/v1/products
    [HttpPost]
    [Authorize(Roles = "Admin")]
    [ProducesResponseType(typeof(ProductDto), StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> CreateProduct([FromBody] CreateProductRequest request)
    {
        var command = new CreateProductCommand
        {
            Name = request.Name,
            Description = request.Description,
            Price = request.Price,
            CategoryId = request.CategoryId
        };
        
        var result = await _mediator.Send(command);
        
        if (!result.IsSuccess)
            return BadRequest(new { error = result.Error });
        
        return CreatedAtAction(
            nameof(GetProduct),
            new { id = result.Value.Id },
            result.Value
        );
    }
    
    // PUT: api/v1/products/{id}
    [HttpPut("{id}")]
    [Authorize(Roles = "Admin")]
    [ProducesResponseType(typeof(ProductDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> UpdateProduct(int id, [FromBody] UpdateProductRequest request)
    {
        var command = new UpdateProductCommand
        {
            ProductId = id,
            Name = request.Name,
            Description = request.Description,
            Price = request.Price
        };
        
        var result = await _mediator.Send(command);
        
        if (!result.IsSuccess)
        {
            return result.StatusCode switch
            {
                404 => NotFound(new { error = result.Error }),
                400 => BadRequest(new { error = result.Error }),
                _ => StatusCode(result.StatusCode, new { error = result.Error })
            };
        }
        
        return Ok(result.Value);
    }
    
    // PATCH: api/v1/products/{id}/price
    [HttpPatch("{id}/price")]
    [Authorize(Roles = "Admin")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> UpdateProductPrice(int id, [FromBody] UpdatePriceRequest request)
    {
        var command = new UpdateProductPriceCommand
        {
            ProductId = id,
            NewPrice = request.Price
        };
        
        var result = await _mediator.Send(command);
        
        if (!result.IsSuccess)
            return NotFound(new { error = result.Error });
        
        return NoContent();
    }
    
    // DELETE: api/v1/products/{id}
    [HttpDelete("{id}")]
    [Authorize(Roles = "Admin")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> DeleteProduct(int id)
    {
        var command = new DeleteProductCommand { ProductId = id };
        var result = await _mediator.Send(command);
        
        if (!result.IsSuccess)
            return NotFound(new { error = result.Error });
        
        return NoContent();
    }
    
    // GET: api/v1/products/{id}/reviews
    [HttpGet("{id}/reviews")]
    [ProducesResponseType(typeof(List<ReviewDto>), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetProductReviews(int id)
    {
        var query = new GetProductReviewsQuery { ProductId = id };
        var result = await _mediator.Send(query);
        return Ok(result);
    }
    
    // POST: api/v1/products/{id}/reviews
    [HttpPost("{id}/reviews")]
    [Authorize]
    [ProducesResponseType(typeof(ReviewDto), StatusCodes.Status201Created)]
    public async Task<IActionResult> AddProductReview(int id, [FromBody] AddReviewRequest request)
    {
        var command = new AddProductReviewCommand
        {
            ProductId = id,
            Rating = request.Rating,
            Comment = request.Comment
        };
        
        var result = await _mediator.Send(command);
        
        return CreatedAtAction(
            nameof(GetProductReviews),
            new { id },
            result.Value
        );
    }
}
```

---

## API Versioning Strategies

### Why Version Your API?

**Scenario**: You need to change the response format, but existing mobile apps depend on the old format.

**Without versioning**:
- Change breaks existing clients
- Clients must update immediately
- Angry users, bad reviews

**With versioning**:
- Old clients use v1
- New clients use v2
- Gradual migration

### Strategy 1: URL Versioning (Recommended)

**Most common and explicit**:
```csharp
// Version in URL
[Route("api/v1/products")]
public class ProductsV1Controller : ControllerBase { }

[Route("api/v2/products")]
public class ProductsV2Controller : ControllerBase { }
```

**Pros**:
- ✅ Explicit and visible
- ✅ Easy to test (just change URL)
- ✅ Works with all HTTP clients
- ✅ Cacheable

**Cons**:
- ❌ URL changes between versions
- ❌ More controllers to maintain

**Example**:
```
GET /api/v1/products/123  # Old version
GET /api/v2/products/123  # New version
```

### Strategy 2: Header Versioning

**Version in custom header**:
```csharp
// Program.cs
builder.Services.AddApiVersioning(options =>
{
    options.ApiVersionReader = new HeaderApiVersionReader("X-API-Version");
    options.DefaultApiVersion = new ApiVersion(1, 0);
    options.AssumeDefaultVersionWhenUnspecified = true;
});

// Controller
[ApiController]
[Route("api/products")]
[ApiVersion("1.0")]
public class ProductsV1Controller : ControllerBase { }

[ApiController]
[Route("api/products")]
[ApiVersion("2.0")]
public class ProductsV2Controller : ControllerBase { }
```

**Request**:
```http
GET /api/products/123
X-API-Version: 2.0
```

**Pros**:
- ✅ URL stays the same
- ✅ Clean URLs

**Cons**:
- ❌ Not visible in URL
- ❌ Harder to test (need to set header)
- ❌ Not cacheable by default

### Strategy 3: Query String Versioning

```csharp
builder.Services.AddApiVersioning(options =>
{
    options.ApiVersionReader = new QueryStringApiVersionReader("api-version");
});
```

**Request**:
```
GET /api/products/123?api-version=2.0
```

**Pros**:
- ✅ Visible in URL
- ✅ Easy to test

**Cons**:
- ❌ Pollutes query string
- ❌ Ugly URLs

### Strategy 4: Content Negotiation (Accept Header)

```http
GET /api/products/123
Accept: application/vnd.myapp.v2+json
```

**Pros**:
- ✅ RESTful purist approach

**Cons**:
- ❌ Complex
- ❌ Not intuitive
- ❌ Rarely used in practice

### Recommended Approach: URL Versioning

**Implementation**:
```csharp
// V1 Controller
[ApiController]
[Route("api/v1/products")]
public class ProductsV1Controller : ControllerBase
{
    [HttpGet("{id}")]
    public async Task<IActionResult> GetProduct(int id)
    {
        // Old response format
        return Ok(new
        {
            id = 123,
            name = "Product Name",
            price = 99.99
        });
    }
}

// V2 Controller (breaking change: price is now an object)
[ApiController]
[Route("api/v2/products")]
public class ProductsV2Controller : ControllerBase
{
    [HttpGet("{id}")]
    public async Task<IActionResult> GetProduct(int id)
    {
        // New response format
        return Ok(new
        {
            id = 123,
            name = "Product Name",
            price = new
            {
                amount = 99.99,
                currency = "USD"
            }
        });
    }
}
```

**Deprecation strategy**:
```csharp
[ApiController]
[Route("api/v1/products")]
[Obsolete("This API version is deprecated. Please use v2.")]
public class ProductsV1Controller : ControllerBase
{
    [HttpGet("{id}")]
    public async Task<IActionResult> GetProduct(int id)
    {
        // Add deprecation header
        Response.Headers.Add("X-API-Deprecated", "true");
        Response.Headers.Add("X-API-Sunset-Date", "2024-12-31");
        Response.Headers.Add("X-API-Replacement", "/api/v2/products/{id}");

        // Return old format
        return Ok(/* ... */);
    }
}
```

---

## Pagination, Filtering, Sorting

### Pagination

**Why**: Don't return 1 million products in a single request!

**Offset-based pagination** (simple):
```csharp
// Request
GET /api/products?page=2&pageSize=20

// Response
{
  "items": [ /* 20 products */ ],
  "page": 2,
  "pageSize": 20,
  "totalCount": 1000,
  "totalPages": 50,
  "hasNextPage": true,
  "hasPreviousPage": true
}

// Implementation
public class PagedResult<T>
{
    public List<T> Items { get; set; }
    public int Page { get; set; }
    public int PageSize { get; set; }
    public int TotalCount { get; set; }
    public int TotalPages { get; set; }
    public bool HasNextPage => Page < TotalPages;
    public bool HasPreviousPage => Page > 1;
}

[HttpGet]
public async Task<IActionResult> GetProducts(
    [FromQuery] int page = 1,
    [FromQuery] int pageSize = 20)
{
    var query = _context.Products.AsNoTracking();

    var totalCount = await query.CountAsync();

    var products = await query
        .OrderBy(p => p.Id)
        .Skip((page - 1) * pageSize)
        .Take(pageSize)
        .ToListAsync();

    var result = new PagedResult<Product>
    {
        Items = products,
        Page = page,
        PageSize = pageSize,
        TotalCount = totalCount,
        TotalPages = (int)Math.Ceiling(totalCount / (double)pageSize)
    };

    return Ok(result);
}
```

**Cursor-based pagination** (better for large datasets):
```csharp
// Request
GET /api/products?cursor=eyJpZCI6MTIzfQ==&limit=20

// Response
{
  "items": [ /* 20 products */ ],
  "nextCursor": "eyJpZCI6MTQzfQ==",
  "hasMore": true
}

// Implementation
[HttpGet]
public async Task<IActionResult> GetProducts(
    [FromQuery] string? cursor = null,
    [FromQuery] int limit = 20)
{
    var query = _context.Products.AsNoTracking();

    if (!string.IsNullOrEmpty(cursor))
    {
        var decodedCursor = DecodeBase64(cursor);
        var lastId = int.Parse(decodedCursor);
        query = query.Where(p => p.Id > lastId);
    }

    var products = await query
        .OrderBy(p => p.Id)
        .Take(limit + 1) // Fetch one extra to check if there's more
        .ToListAsync();

    var hasMore = products.Count > limit;
    if (hasMore)
        products = products.Take(limit).ToList();

    var nextCursor = hasMore
        ? EncodeBase64(products.Last().Id.ToString())
        : null;

    return Ok(new
    {
        items = products,
        nextCursor,
        hasMore
    });
}
```

**When to use each**:
- **Offset-based**: Simple use cases, need page numbers, small datasets
- **Cursor-based**: Large datasets, real-time data, infinite scroll

### Filtering

```csharp
// Request
GET /api/products?category=electronics&minPrice=100&maxPrice=500&inStock=true

// Implementation
[HttpGet]
public async Task<IActionResult> GetProducts(
    [FromQuery] string? category = null,
    [FromQuery] decimal? minPrice = null,
    [FromQuery] decimal? maxPrice = null,
    [FromQuery] bool? inStock = null)
{
    var query = _context.Products.AsNoTracking();

    if (!string.IsNullOrEmpty(category))
        query = query.Where(p => p.Category == category);

    if (minPrice.HasValue)
        query = query.Where(p => p.Price >= minPrice.Value);

    if (maxPrice.HasValue)
        query = query.Where(p => p.Price <= maxPrice.Value);

    if (inStock.HasValue)
        query = query.Where(p => p.StockQuantity > 0 == inStock.Value);

    var products = await query.ToListAsync();
    return Ok(products);
}
```

### Sorting

```csharp
// Request
GET /api/products?sortBy=price&sortOrder=desc

// Implementation
[HttpGet]
public async Task<IActionResult> GetProducts(
    [FromQuery] string sortBy = "name",
    [FromQuery] string sortOrder = "asc")
{
    var query = _context.Products.AsNoTracking();

    // Dynamic sorting
    query = sortBy.ToLower() switch
    {
        "name" => sortOrder == "desc"
            ? query.OrderByDescending(p => p.Name)
            : query.OrderBy(p => p.Name),
        "price" => sortOrder == "desc"
            ? query.OrderByDescending(p => p.Price)
            : query.OrderBy(p => p.Price),
        "created" => sortOrder == "desc"
            ? query.OrderByDescending(p => p.CreatedAt)
            : query.OrderBy(p => p.CreatedAt),
        _ => query.OrderBy(p => p.Name) // Default
    };

    var products = await query.ToListAsync();
    return Ok(products);
}
```

**Or use a library** (System.Linq.Dynamic.Core):
```csharp
dotnet add package System.Linq.Dynamic.Core

[HttpGet]
public async Task<IActionResult> GetProducts(
    [FromQuery] string sortBy = "Name",
    [FromQuery] string sortOrder = "asc")
{
    var query = _context.Products.AsNoTracking();

    // Dynamic sorting with string
    var orderBy = $"{sortBy} {sortOrder}";
    query = query.OrderBy(orderBy);

    var products = await query.ToListAsync();
    return Ok(products);
}
```

---

## Error Handling

### Consistent Error Response Format

**Problem Details (RFC 7807)**:
```csharp
// Install package
dotnet add package Hellang.Middleware.ProblemDetails

// Program.cs
builder.Services.AddProblemDetails(options =>
{
    options.IncludeExceptionDetails = (ctx, ex) => builder.Environment.IsDevelopment();

    options.Map<NotFoundException>(ex => new ProblemDetails
    {
        Title = "Resource not found",
        Status = StatusCodes.Status404NotFound,
        Detail = ex.Message
    });

    options.Map<ValidationException>(ex => new ValidationProblemDetails(ex.Errors)
    {
        Title = "Validation failed",
        Status = StatusCodes.Status400BadRequest
    });
});

var app = builder.Build();
app.UseProblemDetails();
```

**Error response**:
```json
{
  "type": "https://tools.ietf.org/html/rfc7231#section-6.5.4",
  "title": "Resource not found",
  "status": 404,
  "detail": "Product with ID 123 was not found",
  "traceId": "00-abc123-def456-00"
}
```

### Custom Error Handling Middleware

```csharp
public class ExceptionHandlingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<ExceptionHandlingMiddleware> _logger;

    public ExceptionHandlingMiddleware(
        RequestDelegate next,
        ILogger<ExceptionHandlingMiddleware> logger)
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
        var response = exception switch
        {
            NotFoundException => new
            {
                status = StatusCodes.Status404NotFound,
                title = "Resource not found",
                detail = exception.Message
            },
            ValidationException validationEx => new
            {
                status = StatusCodes.Status400BadRequest,
                title = "Validation failed",
                detail = exception.Message,
                errors = validationEx.Errors
            },
            UnauthorizedAccessException => new
            {
                status = StatusCodes.Status403Forbidden,
                title = "Forbidden",
                detail = "You don't have permission to access this resource"
            },
            _ => new
            {
                status = StatusCodes.Status500InternalServerError,
                title = "Internal server error",
                detail = "An unexpected error occurred"
            }
        };

        context.Response.ContentType = "application/json";
        context.Response.StatusCode = response.status;

        await context.Response.WriteAsJsonAsync(response);
    }
}

// Register middleware
app.UseMiddleware<ExceptionHandlingMiddleware>();
```

---

## GraphQL vs REST

### When to Use GraphQL

**✅ Use GraphQL when**:
- Multiple clients with different data needs (web, mobile, desktop)
- Clients need to fetch related data in single request
- Over-fetching is a problem (mobile apps on slow networks)
- Under-fetching requires multiple requests
- Rapid frontend iteration (no backend changes needed)

**❌ Don't use GraphQL when**:
- Simple CRUD operations
- File uploads/downloads
- Caching is critical (REST caching is easier)
- Team unfamiliar with GraphQL
- Real-time updates (use SignalR/WebSockets instead)

### GraphQL Example

**Install**:
```bash
dotnet add package HotChocolate.AspNetCore
dotnet add package HotChocolate.Data.EntityFramework
```

**Setup**:
```csharp
// Program.cs
builder.Services
    .AddGraphQLServer()
    .AddQueryType<Query>()
    .AddMutationType<Mutation>()
    .AddFiltering()
    .AddSorting()
    .AddProjections();

var app = builder.Build();
app.MapGraphQL();
```

**Query Type**:
```csharp
public class Query
{
    [UseProjection]
    [UseFiltering]
    [UseSorting]
    public IQueryable<Product> GetProducts([Service] ApplicationDbContext context)
    {
        return context.Products;
    }

    public async Task<Product?> GetProduct(
        int id,
        [Service] ApplicationDbContext context)
    {
        return await context.Products.FindAsync(id);
    }
}
```

**Mutation Type**:
```csharp
public class Mutation
{
    public async Task<Product> CreateProduct(
        CreateProductInput input,
        [Service] ApplicationDbContext context)
    {
        var product = new Product
        {
            Name = input.Name,
            Price = input.Price
        };

        context.Products.Add(product);
        await context.SaveChangesAsync();

        return product;
    }
}

public record CreateProductInput(string Name, decimal Price);
```

**GraphQL Query**:
```graphql
# Fetch only needed fields
query {
  products(where: { price: { gte: 100 } }) {
    id
    name
    price
  }
}

# Fetch related data in single request
query {
  product(id: 123) {
    id
    name
    price
    reviews {
      rating
      comment
      user {
        name
      }
    }
  }
}
```

### REST vs GraphQL Comparison

| Feature | REST | GraphQL |
|---------|------|---------|
| **Learning curve** | Low | High |
| **Caching** | Easy (HTTP cache) | Complex |
| **Over-fetching** | Common | Solved |
| **Under-fetching** | Common (N+1 requests) | Solved |
| **Versioning** | Explicit (v1, v2) | Implicit (add fields) |
| **Tooling** | Mature | Growing |
| **File uploads** | Easy | Complex |
| **Real-time** | WebSockets/SignalR | Subscriptions |
| **Mobile apps** | Good | Excellent |
| **Public APIs** | Excellent | Good |

---

## gRPC for Microservices

### When to Use gRPC

**✅ Use gRPC when**:
- Microservices communication (internal APIs)
- High performance required
- Strongly-typed contracts needed
- Bi-directional streaming
- Polyglot environments (multiple languages)

**❌ Don't use gRPC when**:
- Browser clients (limited support)
- Public APIs (REST is more accessible)
- Human-readable format needed
- Debugging ease is priority

### gRPC Example

**Install**:
```bash
dotnet add package Grpc.AspNetCore
dotnet add package Google.Protobuf
dotnet add package Grpc.Tools
```

**Define proto file** (`Protos/products.proto`):
```protobuf
syntax = "proto3";

option csharp_namespace = "MyApp.Grpc";

service ProductService {
  rpc GetProduct (GetProductRequest) returns (ProductResponse);
  rpc GetProducts (GetProductsRequest) returns (stream ProductResponse);
  rpc CreateProduct (CreateProductRequest) returns (ProductResponse);
}

message GetProductRequest {
  int32 id = 1;
}

message GetProductsRequest {
  string category = 1;
}

message CreateProductRequest {
  string name = 1;
  double price = 2;
}

message ProductResponse {
  int32 id = 1;
  string name = 2;
  double price = 3;
}
```

**Implement service**:
```csharp
public class ProductService : Grpc.ProductService.ProductServiceBase
{
    private readonly IProductRepository _productRepository;

    public ProductService(IProductRepository productRepository)
    {
        _productRepository = productRepository;
    }

    public override async Task<ProductResponse> GetProduct(
        GetProductRequest request,
        ServerCallContext context)
    {
        var product = await _productRepository.GetByIdAsync(request.Id);

        if (product == null)
            throw new RpcException(new Status(StatusCode.NotFound, "Product not found"));

        return new ProductResponse
        {
            Id = product.Id,
            Name = product.Name,
            Price = (double)product.Price
        };
    }

    public override async Task GetProducts(
        GetProductsRequest request,
        IServerStreamWriter<ProductResponse> responseStream,
        ServerCallContext context)
    {
        var products = await _productRepository.GetByCategoryAsync(request.Category);

        foreach (var product in products)
        {
            await responseStream.WriteAsync(new ProductResponse
            {
                Id = product.Id,
                Name = product.Name,
                Price = (double)product.Price
            });
        }
    }
}
```

**Register service**:
```csharp
// Program.cs
builder.Services.AddGrpc();

var app = builder.Build();
app.MapGrpcService<ProductService>();
```

**Client usage**:
```csharp
var channel = GrpcChannel.ForAddress("https://localhost:5001");
var client = new ProductService.ProductServiceClient(channel);

// Unary call
var response = await client.GetProductAsync(new GetProductRequest { Id = 123 });

// Server streaming
var call = client.GetProducts(new GetProductsRequest { Category = "Electronics" });
await foreach (var product in call.ResponseStream.ReadAllAsync())
{
    Console.WriteLine($"{product.Name}: ${product.Price}");
}
```

### REST vs gRPC Comparison

| Feature | REST | gRPC |
|---------|------|------|
| **Protocol** | HTTP/1.1 | HTTP/2 |
| **Format** | JSON (text) | Protobuf (binary) |
| **Performance** | Good | Excellent (5-10x faster) |
| **Browser support** | Excellent | Limited |
| **Human-readable** | Yes | No |
| **Streaming** | Limited | Excellent |
| **Code generation** | Optional | Built-in |
| **Use case** | Public APIs | Microservices |

---

## API Documentation

### Swagger/OpenAPI

**Install**:
```bash
dotnet add package Swashbuckle.AspNetCore
```

**Setup**:
```csharp
// Program.cs
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "My API",
        Version = "v1",
        Description = "E-commerce API",
        Contact = new OpenApiContact
        {
            Name = "Support",
            Email = "support@myapp.com"
        }
    });

    // Include XML comments
    var xmlFile = $"{Assembly.GetExecutingAssembly().GetName().Name}.xml";
    var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
    options.IncludeXmlComments(xmlPath);

    // Add JWT authentication
    options.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Description = "JWT Authorization header using the Bearer scheme",
        Name = "Authorization",
        In = ParameterLocation.Header,
        Type = SecuritySchemeType.ApiKey,
        Scheme = "Bearer"
    });

    options.AddSecurityRequirement(new OpenApiSecurityRequirement
    {
        {
            new OpenApiSecurityScheme
            {
                Reference = new OpenApiReference
                {
                    Type = ReferenceType.SecurityScheme,
                    Id = "Bearer"
                }
            },
            Array.Empty<string>()
        }
    });
});

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(options =>
    {
        options.SwaggerEndpoint("/swagger/v1/swagger.json", "My API V1");
        options.RoutePrefix = string.Empty; // Serve at root
    });
}
```

**XML comments**:
```csharp
/// <summary>
/// Gets a product by ID
/// </summary>
/// <param name="id">The product ID</param>
/// <returns>The product details</returns>
/// <response code="200">Returns the product</response>
/// <response code="404">Product not found</response>
[HttpGet("{id}")]
[ProducesResponseType(typeof(ProductDto), StatusCodes.Status200OK)]
[ProducesResponseType(StatusCodes.Status404NotFound)]
public async Task<IActionResult> GetProduct(int id)
{
    // ...
}
```

---

## Summary

### API Design Checklist

**REST API**:
- [ ] Use plural nouns for resources (`/products`, not `/product`)
- [ ] Use HTTP methods correctly (GET, POST, PUT, DELETE)
- [ ] Return appropriate status codes (200, 201, 400, 404, 500)
- [ ] Implement pagination for large datasets
- [ ] Support filtering and sorting
- [ ] Version your API (URL versioning recommended)
- [ ] Document with Swagger/OpenAPI
- [ ] Implement consistent error handling

**Performance**:
- [ ] Use async/await for I/O operations
- [ ] Implement caching where appropriate
- [ ] Use `AsNoTracking` for read-only queries
- [ ] Avoid N+1 queries with `Include`
- [ ] Implement response compression

**Security**:
- [ ] Require authentication for sensitive endpoints
- [ ] Implement authorization (role-based, policy-based)
- [ ] Validate all inputs
- [ ] Use HTTPS
- [ ] Implement rate limiting

### Decision Matrix

| Scenario | Use REST | Use GraphQL | Use gRPC |
|----------|----------|-------------|----------|
| Public API | ✅ | ⚠️ | ❌ |
| Mobile app | ✅ | ✅ | ❌ |
| Web app | ✅ | ✅ | ❌ |
| Microservices | ⚠️ | ❌ | ✅ |
| Real-time | ❌ | ⚠️ | ✅ |
| Simple CRUD | ✅ | ❌ | ❌ |
| Complex queries | ⚠️ | ✅ | ❌ |
| High performance | ⚠️ | ⚠️ | ✅ |

---

**Remember**: Good API design is about consistency, clarity, and developer experience. Make it easy for others to use your API! 🚀
```
