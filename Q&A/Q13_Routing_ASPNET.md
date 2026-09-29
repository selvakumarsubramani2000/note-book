# Question 13: What is routing in ASP.NET? Provide a real-time code base example.

## Answer

### What is Routing?

**Routing** is the mechanism that maps incoming HTTP requests (URLs) to specific controller actions in your ASP.NET application. It determines which controller and action method should handle a particular request.

Think of it as a **GPS for HTTP requests** - it tells the framework where to send the request based on the URL pattern.

---

## How Routing Works

```
HTTP Request
    ↓
URL: https://api.example.com/api/products/5
    ↓
Routing Engine analyzes the URL
    ↓
Matches route template: "api/{controller}/{id}"
    ↓
Determines:
  - Controller: ProductsController
  - Action: Get(int id)
  - Parameter: id = 5
    ↓
Executes: ProductsController.Get(5)
    ↓
Returns Response
```

---

## Types of Routing in ASP.NET Core

### 1. **Conventional Routing** (Rarely used in Web APIs)

Defined in `Startup.cs` using a template:

```csharp
public void Configure(IApplicationBuilder app)
{
    app.UseRouting();
    
    app.UseEndpoints(endpoints =>
    {
        endpoints.MapControllerRoute(
            name: "default",
            pattern: "{controller=Home}/{action=Index}/{id?}");
    });
}

// This means:
// /Products/Details/5 → ProductsController.Details(id: 5)
// /Home/Index → HomeController.Index()
```

---

### 2. **Attribute Routing** (Preferred for Web APIs) ⭐

Routes are defined directly on controllers and actions using attributes.

#### Basic Example

```csharp
[ApiController]
[Route("api/[controller]")] // [controller] is replaced with "products"
public class ProductsController : ControllerBase
{
    // GET: api/products
    [HttpGet]
    public IActionResult GetAll()
    {
        return Ok("All products");
    }
    
    // GET: api/products/5
    [HttpGet("{id}")]
    public IActionResult GetById(int id)
    {
        return Ok($"Product with ID: {id}");
    }
    
    // POST: api/products
    [HttpPost]
    public IActionResult Create([FromBody] Product product)
    {
        return CreatedAtAction(nameof(GetById), new { id = product.Id }, product);
    }
    
    // PUT: api/products/5
    [HttpPut("{id}")]
    public IActionResult Update(int id, [FromBody] Product product)
    {
        return Ok($"Updated product {id}");
    }
    
    // DELETE: api/products/5
    [HttpDelete("{id}")]
    public IActionResult Delete(int id)
    {
        return Ok($"Deleted product {id}");
    }
}
```

---

## Real-Time Code Base Examples

### Example 1: E-Commerce Product API

```csharp
[ApiController]
[Route("api/products")]
public class ProductsController : ControllerBase
{
    private readonly IProductService _productService;
    
    public ProductsController(IProductService productService)
    {
        _productService = productService;
    }
    
    // GET: api/products
    [HttpGet]
    public async Task<IActionResult> GetAllProducts()
    {
        var products = await _productService.GetAllAsync();
        return Ok(products);
    }
    
    // GET: api/products/5
    [HttpGet("{id:int}")] // :int is a route constraint
    public async Task<IActionResult> GetProduct(int id)
    {
        var product = await _productService.GetByIdAsync(id);
        if (product == null)
            return NotFound($"Product with ID {id} not found");
        
        return Ok(product);
    }
    
    // GET: api/products/category/electronics
    [HttpGet("category/{categoryName}")]
    public async Task<IActionResult> GetByCategory(string categoryName)
    {
        var products = await _productService.GetByCategoryAsync(categoryName);
        return Ok(products);
    }
    
    // GET: api/products/search?keyword=laptop&minPrice=100&maxPrice=1000
    [HttpGet("search")]
    public async Task<IActionResult> Search(
        [FromQuery] string keyword,
        [FromQuery] decimal? minPrice,
        [FromQuery] decimal? maxPrice)
    {
        var products = await _productService.SearchAsync(keyword, minPrice, maxPrice);
        return Ok(products);
    }
    
    // POST: api/products
    [HttpPost]
    public async Task<IActionResult> CreateProduct([FromBody] CreateProductRequest request)
    {
        if (!ModelState.IsValid)
            return BadRequest(ModelState);
        
        var product = await _productService.CreateAsync(request);
        return CreatedAtAction(nameof(GetProduct), new { id = product.Id }, product);
    }
    
    // PUT: api/products/5
    [HttpPut("{id}")]
    public async Task<IActionResult> UpdateProduct(int id, [FromBody] UpdateProductRequest request)
    {
        var success = await _productService.UpdateAsync(id, request);
        if (!success)
            return NotFound();
        
        return NoContent();
    }
    
    // DELETE: api/products/5
    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteProduct(int id)
    {
        var success = await _productService.DeleteAsync(id);
        if (!success)
            return NotFound();
        
        return NoContent();
    }
    
    // GET: api/products/5/reviews
    [HttpGet("{productId}/reviews")]
    public async Task<IActionResult> GetProductReviews(int productId)
    {
        var reviews = await _productService.GetReviewsAsync(productId);
        return Ok(reviews);
    }
}
```

**URLs this controller handles:**
```
GET    /api/products                          → GetAllProducts()
GET    /api/products/5                        → GetProduct(5)
GET    /api/products/category/electronics     → GetByCategory("electronics")
GET    /api/products/search?keyword=laptop    → Search("laptop", null, null)
POST   /api/products                          → CreateProduct(...)
PUT    /api/products/5                        → UpdateProduct(5, ...)
DELETE /api/products/5                        → DeleteProduct(5)
GET    /api/products/5/reviews                → GetProductReviews(5)
```

---

### Example 2: User Management API with Multiple Routes

```csharp
[ApiController]
[Route("api/users")]
public class UsersController : ControllerBase
{
    // GET: api/users
    [HttpGet]
    public IActionResult GetAllUsers()
    {
        return Ok("All users");
    }
    
    // GET: api/users/5
    [HttpGet("{id}")]
    public IActionResult GetUserById(int id)
    {
        return Ok($"User {id}");
    }
    
    // GET: api/users/username/john.doe
    [HttpGet("username/{username}")]
    public IActionResult GetByUsername(string username)
    {
        return Ok($"User: {username}");
    }
    
    // GET: api/users/email/john@example.com
    [HttpGet("email/{email}")]
    public IActionResult GetByEmail(string email)
    {
        return Ok($"User with email: {email}");
    }
    
    // GET: api/users/5/orders
    [HttpGet("{userId}/orders")]
    public IActionResult GetUserOrders(int userId)
    {
        return Ok($"Orders for user {userId}");
    }
    
    // POST: api/users/register
    [HttpPost("register")]
    public IActionResult Register([FromBody] RegisterRequest request)
    {
        return Ok("User registered");
    }
    
    // POST: api/users/login
    [HttpPost("login")]
    public IActionResult Login([FromBody] LoginRequest request)
    {
        return Ok("User logged in");
    }
    
    // PUT: api/users/5/password
    [HttpPut("{id}/password")]
    public IActionResult ChangePassword(int id, [FromBody] ChangePasswordRequest request)
    {
        return Ok($"Password changed for user {id}");
    }
}
```

---

### Example 3: Order Management with Complex Routing

```csharp
[ApiController]
[Route("api/orders")]
public class OrdersController : ControllerBase
{
    // GET: api/orders
    [HttpGet]
    public IActionResult GetOrders()
    {
        return Ok("All orders");
    }
    
    // GET: api/orders/5
    [HttpGet("{id:int}")]
    public IActionResult GetOrder(int id)
    {
        return Ok($"Order {id}");
    }
    
    // GET: api/orders/ORD-2024-001 (string ID)
    [HttpGet("{orderNumber:alpha}")]
    public IActionResult GetOrderByNumber(string orderNumber)
    {
        return Ok($"Order number: {orderNumber}");
    }
    
    // GET: api/orders/user/5
    [HttpGet("user/{userId}")]
    public IActionResult GetOrdersByUser(int userId)
    {
        return Ok($"Orders for user {userId}");
    }
    
    // GET: api/orders/status/pending
    [HttpGet("status/{status}")]
    public IActionResult GetOrdersByStatus(string status)
    {
        return Ok($"Orders with status: {status}");
    }
    
    // GET: api/orders/date-range?from=2024-01-01&to=2024-12-31
    [HttpGet("date-range")]
    public IActionResult GetOrdersByDateRange(
        [FromQuery] DateTime from,
        [FromQuery] DateTime to)
    {
        return Ok($"Orders from {from:yyyy-MM-dd} to {to:yyyy-MM-dd}");
    }
    
    // POST: api/orders
    [HttpPost]
    public IActionResult CreateOrder([FromBody] CreateOrderRequest request)
    {
        return CreatedAtAction(nameof(GetOrder), new { id = 123 }, request);
    }
    
    // PUT: api/orders/5/status
    [HttpPut("{id}/status")]
    public IActionResult UpdateOrderStatus(int id, [FromBody] UpdateStatusRequest request)
    {
        return Ok($"Status updated for order {id}");
    }
    
    // POST: api/orders/5/cancel
    [HttpPost("{id}/cancel")]
    public IActionResult CancelOrder(int id)
    {
        return Ok($"Order {id} cancelled");
    }
}
```

---

## Route Constraints

Ensure parameters match specific patterns:

```csharp
[HttpGet("{id:int}")]          // id must be integer
[HttpGet("{id:min(1)}")]       // id must be >= 1
[HttpGet("{id:range(1,100)}")] // id must be between 1 and 100
[HttpGet("{name:alpha}")]      // name must contain only letters
[HttpGet("{name:minlength(3)}")]  // name must be at least 3 characters
[HttpGet("{price:decimal}")]   // price must be decimal
[HttpGet("{active:bool}")]     // active must be boolean
```

**Example:**
```csharp
// GET: api/products/5 → Works (5 is an integer)
// GET: api/products/abc → 404 Not Found (abc is not an integer)
[HttpGet("{id:int}")]
public IActionResult Get(int id)
{
    return Ok($"Product {id}");
}
```

---

## Multiple Routes on Same Action

```csharp
[HttpGet]
[Route("api/products")]
[Route("api/items")] // Alternative route
public IActionResult GetAll()
{
    return Ok("Products");
}

// Both work:
// GET: api/products → Works
// GET: api/items → Works (same action)
```

---

## Route with Optional Parameters

```csharp
// id is optional (note the ?)
[HttpGet("{id?}")]
public IActionResult Get(int? id)
{
    if (id.HasValue)
        return Ok($"Product {id}");
    else
        return Ok("All products");
}

// Both work:
// GET: api/products → "All products"
// GET: api/products/5 → "Product 5"
```

---

## Best Practices

1. ✅ **Use attribute routing** for Web APIs (clearer, more explicit)
2. ✅ **Use route constraints** to validate parameters
3. ✅ **Be consistent** with naming conventions
4. ✅ **Version your APIs**: `api/v1/products`, `api/v2/products`
5. ✅ **Use meaningful route names**
6. ❌ **Avoid overlapping routes** (causes ambiguity)
7. ❌ **Don't put business logic in routes**

---

## Summary

**Routing = Mapping URLs to Controller Actions**

**Key Components:**
- `[Route]` - Defines the route template
- `[HttpGet]`, `[HttpPost]`, etc. - HTTP verb + optional route
- Route parameters - `{id}`, `{name}`, etc.
- Route constraints - `:int`, `:alpha`, `:min(1)`, etc.

Routing makes your API clean, predictable, and RESTful!
