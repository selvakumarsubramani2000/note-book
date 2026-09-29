# Backend Architecture Quick Reference

> **Cheat sheet** for making architectural decisions quickly  
> **Focus**: Decision matrices, common patterns, and quick answers

---

## Decision Trees

### 1. Which Architecture Pattern?

```
Do you have complex business logic?
├─ YES → Clean Architecture
│   └─ Multiple teams? → Yes: Clean Architecture with CQRS
│       └─ No: Clean Architecture (simpler)
└─ NO → Simple CRUD?
    ├─ YES → Layered Architecture (Controller → Service → Repository)
    └─ NO → Minimal API with direct EF Core
```

### 2. Which API Style?

```
What type of API are you building?
├─ Public API for third parties → REST
├─ Mobile app with varying data needs → GraphQL or REST
├─ Microservices communication → gRPC
├─ Real-time updates → SignalR/WebSockets
└─ Simple CRUD → REST
```

### 3. Which Caching Strategy?

```
What are you caching?
├─ Static configuration (rarely changes)
│   └─ In-Memory Cache (1 hour expiration)
├─ User session data
│   └─ Redis (20 min expiration)
├─ Product catalog
│   └─ Redis (30 min expiration)
├─ Search results
│   └─ Redis (5 min expiration)
└─ User-specific data
    └─ No cache (or very short expiration)
```

### 4. Which Service Lifetime?

```
What is the service?
├─ DbContext → ALWAYS Scoped
├─ Repository → Scoped (matches DbContext)
├─ MediatR Handler → Transient (default)
├─ Cache Service → Singleton
├─ Logger → Singleton
├─ Current User Service → Scoped
├─ Email Service
│   ├─ Lightweight (creates SMTP client) → Transient
│   └─ Uses connection pool (SendGrid) → Singleton
└─ Configuration → Singleton
```

---

## Common Patterns Cheat Sheet

### Clean Architecture Layers

| Layer | Purpose | Dependencies | Examples |
|-------|---------|--------------|----------|
| **Domain** | Business logic | None | Entities, Value Objects, Domain Events |
| **Application** | Use cases | Domain | Commands, Queries, DTOs, Interfaces |
| **Infrastructure** | External concerns | Application | Repositories, DbContext, External APIs |
| **Presentation** | HTTP/UI | Application | Controllers, Middleware |

**Dependency Rule**: Dependencies point INWARD (Infrastructure → Application → Domain)

### Repository Pattern

**When to use**:
- ✅ Need to abstract database implementation
- ✅ Want to unit test without database
- ✅ Multiple data sources (SQL + NoSQL)

**When NOT to use**:
- ❌ Simple CRUD with no business logic
- ❌ Using EF Core (already a repository pattern)
- ❌ Over-engineering small apps

**Example**:
```csharp
// Interface in Application layer
public interface IOrderRepository
{
    Task<Order?> GetByIdAsync(int id);
    Task AddAsync(Order order);
    Task UpdateAsync(Order order);
}

// Implementation in Infrastructure layer
public class OrderRepository : IOrderRepository
{
    private readonly ApplicationDbContext _context;
    
    public async Task<Order?> GetByIdAsync(int id)
    {
        return await _context.Orders
            .Include(o => o.Items)
            .FirstOrDefaultAsync(o => o.Id == id);
    }
}
```

### CQRS Pattern

**When to use**:
- ✅ Different read and write models
- ✅ Complex business logic
- ✅ Need to scale reads and writes independently

**When NOT to use**:
- ❌ Simple CRUD operations
- ❌ Small applications

**Example**:
```csharp
// Command (write)
public class CreateOrderCommand : IRequest<Result<int>>
{
    public int UserId { get; set; }
    public List<OrderItemDto> Items { get; set; }
}

// Query (read)
public class GetOrderByIdQuery : IRequest<Result<OrderDto>>
{
    public int OrderId { get; set; }
}
```

---

## Performance Optimization Checklist

### Database

- [ ] **Fix N+1 queries**: Use `.Include()` for related data
- [ ] **Use AsNoTracking**: For read-only queries (30-40% faster)
- [ ] **Project only needed columns**: Use `.Select()` instead of fetching entire entity
- [ ] **Implement pagination**: Don't fetch all records at once
- [ ] **Add indexes**: On columns used in WHERE, JOIN, ORDER BY
- [ ] **Use compiled queries**: For frequently executed queries
- [ ] **Batch operations**: Use `AddRange()` instead of multiple `Add()` calls

### Caching

- [ ] **Cache static data**: Categories, configuration (1 hour)
- [ ] **Cache product catalog**: Redis (30 minutes)
- [ ] **Cache search results**: Redis (5 minutes)
- [ ] **Use response caching**: For public GET endpoints
- [ ] **Invalidate cache on updates**: Remove stale data

### Async/Await

- [ ] **Use async for I/O**: Database, HTTP, file operations
- [ ] **Avoid async void**: Use `async Task` instead
- [ ] **Don't block on async**: Never use `.Result` or `.Wait()`
- [ ] **Run independent operations in parallel**: Use `Task.WhenAll()`
- [ ] **Limit concurrency**: Use `SemaphoreSlim` to avoid overwhelming resources

### Infrastructure

- [ ] **Enable response compression**: Brotli or Gzip
- [ ] **Use connection pooling**: Default in EF Core, verify settings
- [ ] **Configure HTTP/2**: For better performance
- [ ] **Use CDN**: For static assets

---

## HTTP Status Codes Quick Reference

| Code | Name | When to Use | Example |
|------|------|-------------|---------|
| **200** | OK | Successful GET, PUT, PATCH | Get product details |
| **201** | Created | Successful POST | Create new order |
| **204** | No Content | Successful DELETE | Delete product |
| **400** | Bad Request | Validation failed | Invalid input |
| **401** | Unauthorized | Not authenticated | Missing/invalid token |
| **403** | Forbidden | Not authorized | User not admin |
| **404** | Not Found | Resource doesn't exist | Product not found |
| **409** | Conflict | Duplicate resource | Email already exists |
| **422** | Unprocessable Entity | Semantic validation failed | Invalid business rule |
| **500** | Internal Server Error | Unexpected error | Database down |
| **503** | Service Unavailable | Service temporarily down | Maintenance mode |

---

## API Versioning Quick Reference

### URL Versioning (Recommended)

```csharp
[Route("api/v1/products")]
public class ProductsV1Controller { }

[Route("api/v2/products")]
public class ProductsV2Controller { }
```

**Pros**: Explicit, easy to test, cacheable  
**Cons**: URL changes between versions

### Header Versioning

```http
GET /api/products/123
X-API-Version: 2.0
```

**Pros**: URL stays same  
**Cons**: Not visible, harder to test

### Query String Versioning

```http
GET /api/products/123?api-version=2.0
```

**Pros**: Visible in URL  
**Cons**: Pollutes query string

---

## Dependency Injection Lifetime Rules

### The Golden Rules

1. **DbContext is ALWAYS Scoped** - Never Transient or Singleton
2. **Repositories match DbContext** - Scoped
3. **Singleton can't depend on Scoped** - Captive dependency!
4. **Don't dispose Scoped services manually** - Let DI container handle it

### Lifetime Comparison

| Lifetime | Created | Disposed | Memory | Use Case |
|----------|---------|----------|--------|----------|
| **Transient** | Every request | Immediately | Low | Lightweight, stateless |
| **Scoped** | Once per HTTP request | End of request | Medium | DbContext, repositories |
| **Singleton** | Once per app | App shutdown | High | Cache, logger, config |

### Common Mistakes

❌ **Singleton → Scoped** (Captive dependency)
```csharp
// WRONG
services.AddSingleton<IOrderService, OrderService>();
public class OrderService
{
    private readonly ApplicationDbContext _context; // Scoped!
}
```

✅ **Fix**: Make OrderService Scoped
```csharp
services.AddScoped<IOrderService, OrderService>();
```

---

## Pagination Patterns

### Offset-Based (Simple)

```csharp
GET /api/products?page=2&pageSize=20

// Response
{
  "items": [...],
  "page": 2,
  "pageSize": 20,
  "totalCount": 1000,
  "totalPages": 50
}
```

**Pros**: Simple, supports page numbers  
**Cons**: Slow for large offsets, inconsistent with real-time data

### Cursor-Based (Scalable)

```csharp
GET /api/products?cursor=eyJpZCI6MTIzfQ==&limit=20

// Response
{
  "items": [...],
  "nextCursor": "eyJpZCI6MTQzfQ==",
  "hasMore": true
}
```

**Pros**: Fast, consistent with real-time data  
**Cons**: No page numbers, more complex

---

## Error Handling Patterns

### Problem Details (RFC 7807)

```json
{
  "type": "https://tools.ietf.org/html/rfc7231#section-6.5.4",
  "title": "Resource not found",
  "status": 404,
  "detail": "Product with ID 123 was not found",
  "traceId": "00-abc123-def456-00"
}
```

### Custom Error Response

```json
{
  "error": {
    "code": "PRODUCT_NOT_FOUND",
    "message": "Product with ID 123 was not found",
    "details": {
      "productId": 123
    }
  }
}
```

---

## REST vs GraphQL vs gRPC

| Feature | REST | GraphQL | gRPC |
|---------|------|---------|------|
| **Protocol** | HTTP/1.1 | HTTP/1.1 | HTTP/2 |
| **Format** | JSON | JSON | Protobuf (binary) |
| **Performance** | Good | Good | Excellent |
| **Browser support** | ✅ | ✅ | ⚠️ |
| **Learning curve** | Low | Medium | High |
| **Caching** | Easy | Complex | N/A |
| **Over-fetching** | Common | Solved | N/A |
| **Versioning** | Explicit | Implicit | Explicit |
| **Public API** | ✅ | ⚠️ | ❌ |
| **Microservices** | ⚠️ | ❌ | ✅ |
| **Mobile app** | ✅ | ✅ | ⚠️ |

---

## Common EF Core Patterns

### Eager Loading (Prevent N+1)

```csharp
// ❌ BAD: N+1 queries
var orders = await _context.Orders.ToListAsync();
foreach (var order in orders)
{
    var user = await _context.Users.FindAsync(order.UserId); // N queries!
}

// ✅ GOOD: 1 query with JOIN
var orders = await _context.Orders
    .Include(o => o.User)
    .ToListAsync();
```

### Projection (Fetch Only Needed Columns)

```csharp
// ❌ BAD: Fetch all columns
var products = await _context.Products.ToListAsync();
var names = products.Select(p => p.Name).ToList();

// ✅ GOOD: Fetch only needed columns
var names = await _context.Products
    .Select(p => p.Name)
    .ToListAsync();
```

### AsNoTracking (Read-Only Queries)

```csharp
// ❌ SLOW: Change tracking overhead
var products = await _context.Products.ToListAsync();

// ✅ FAST: No change tracking (30-40% faster)
var products = await _context.Products
    .AsNoTracking()
    .ToListAsync();
```

---

## Authentication & Authorization Quick Reference

### JWT Token Flow

```
1. User logs in with credentials
2. Server validates credentials
3. Server generates JWT token
4. Client stores token (localStorage/cookie)
5. Client sends token in Authorization header
6. Server validates token on each request
```

### Authorization Patterns

**Role-Based**:
```csharp
[Authorize(Roles = "Admin")]
public async Task<IActionResult> DeleteProduct(int id) { }
```

**Policy-Based**:
```csharp
[Authorize(Policy = "RequireAdminRole")]
public async Task<IActionResult> DeleteProduct(int id) { }
```

**Resource-Based** (in handler):
```csharp
if (order.UserId != _currentUserService.UserId && !_currentUserService.IsAdmin)
    return Result.Forbidden();
```

---

## Load Testing Quick Commands

### k6 (Recommended)

```bash
# Install
choco install k6  # Windows
brew install k6   # macOS

# Run test
k6 run load-test.js

# Run with 100 virtual users for 30 seconds
k6 run --vus 100 --duration 30s load-test.js
```

### Apache Bench

```bash
# 1000 requests, 10 concurrent
ab -n 1000 -c 10 https://localhost:5001/api/products
```

---

## Monitoring Checklist

- [ ] **Application Insights** - Track requests, exceptions, dependencies
- [ ] **Structured logging** - Use Serilog with structured data
- [ ] **Health checks** - `/health` endpoint for monitoring
- [ ] **Metrics** - Track custom business metrics
- [ ] **Alerts** - Set up alerts for errors, slow requests
- [ ] **Distributed tracing** - Track requests across microservices

---

## Summary: When to Use What

### Architecture

- **Clean Architecture**: Complex business logic, long-term maintenance
- **Layered Architecture**: Simple CRUD, small teams
- **Minimal API**: Prototypes, microservices, simple endpoints

### API Style

- **REST**: Public APIs, simple CRUD, standard use cases
- **GraphQL**: Mobile apps, varying data needs, rapid iteration
- **gRPC**: Microservices, high performance, internal APIs

### Caching

- **In-Memory**: Single server, small data, static config
- **Redis**: Multi-server, large data, session state
- **Response Cache**: Public GET endpoints, static content

### Service Lifetime

- **Transient**: Lightweight, stateless services
- **Scoped**: DbContext, repositories, request-specific services
- **Singleton**: Cache, logger, configuration, expensive to create

---

**Remember**: These are guidelines, not rules. Always consider your specific context and requirements! 🎯
