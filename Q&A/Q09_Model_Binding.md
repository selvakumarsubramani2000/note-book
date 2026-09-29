# Question 9: How does model binding work in Web API?

## Answer

### What is Model Binding?

**Model Binding** is the process of automatically mapping HTTP request data (from query strings, route data, form data, or request body) to action method parameters in your controller.

Think of it as: **"Automatic translation from HTTP request to C# objects"**

---

## How Model Binding Works

### The Flow

```
HTTP Request
    ↓
1. Client sends data (JSON, query string, form, etc.)
    ↓
2. ASP.NET Core examines action parameters
    ↓
3. Model binder searches for data in various sources
    ↓
4. Maps data to C# objects
    ↓
5. Validates the model (if validation attributes present)
    ↓
6. Passes object to action method
```

---

## Sources of Model Binding (in order of precedence)

1. **Form values** - Posted form data
2. **Route values** - From route template `{id}`
3. **Query strings** - `?name=John&age=25`
4. **Request body** - JSON/XML in request body

---

## Types of Model Binding

### 1. Simple Type Binding (Primitives)

**From Query String:**

```csharp
[HttpGet("search")]
public IActionResult Search(string query, int page, int pageSize)
{
    // URL: /api/products/search?query=laptop&page=1&pageSize=10
    // query = "laptop"
    // page = 1
    // pageSize = 10
    
    return Ok($"Searching for {query}, page {page}, size {pageSize}");
}
```

**From Route:**

```csharp
[HttpGet("{id}")]
public IActionResult GetProduct(int id)
{
    // URL: /api/products/5
    // id = 5
    
    return Ok($"Getting product {id}");
}

[HttpGet("{category}/{id}")]
public IActionResult GetProductByCategory(string category, int id)
{
    // URL: /api/products/electronics/5
    // category = "electronics"
    // id = 5
    
    return Ok($"Category: {category}, ID: {id}");
}
```

---

### 2. Complex Type Binding (Objects)

**From Request Body (JSON):**

```csharp
// Model class
public class Product
{
    public string Name { get; set; }
    public decimal Price { get; set; }
    public string Category { get; set; }
}

[HttpPost]
public IActionResult CreateProduct([FromBody] Product product)
{
    // Request Body (JSON):
    // {
    //   "name": "Laptop",
    //   "price": 999.99,
    //   "category": "Electronics"
    // }
    
    // Model binder automatically creates Product object
    // product.Name = "Laptop"
    // product.Price = 999.99
    // product.Category = "Electronics"
    
    return Ok($"Created product: {product.Name}");
}
```

**From Query String (Complex Object):**

```csharp
public class SearchFilter
{
    public string Keyword { get; set; }
    public decimal MinPrice { get; set; }
    public decimal MaxPrice { get; set; }
    public string Category { get; set; }
}

[HttpGet("filter")]
public IActionResult FilterProducts([FromQuery] SearchFilter filter)
{
    // URL: /api/products/filter?keyword=laptop&minPrice=100&maxPrice=1000&category=electronics
    
    // Model binder creates SearchFilter object:
    // filter.Keyword = "laptop"
    // filter.MinPrice = 100
    // filter.MaxPrice = 1000
    // filter.Category = "electronics"
    
    return Ok(filter);
}
```

---

## Model Binding Attributes

### Common Binding Source Attributes

#### 1. `[FromBody]` - From Request Body

```csharp
[HttpPost]
public IActionResult Create([FromBody] Product product)
{
    // Expects JSON/XML in request body
    return Ok();
}
```

#### 2. `[FromQuery]` - From Query String

```csharp
[HttpGet]
public IActionResult GetProducts([FromQuery] string search, [FromQuery] int page = 1)
{
    // URL: /api/products?search=laptop&page=2
    return Ok();
}
```

#### 3. `[FromRoute]` - From Route Parameters

```csharp
[HttpGet("{id}/{name}")]
public IActionResult GetProduct([FromRoute] int id, [FromRoute] string name)
{
    // URL: /api/products/5/laptop
    return Ok();
}
```

#### 4. `[FromForm]` - From Form Data

```csharp
[HttpPost("upload")]
public IActionResult Upload([FromForm] IFormFile file, [FromForm] string description)
{
    // Expects multipart/form-data
    // Used for file uploads and form submissions
    return Ok();
}
```

#### 5. `[FromHeader]` - From HTTP Headers

```csharp
[HttpGet]
public IActionResult GetData([FromHeader(Name = "X-API-Key")] string apiKey)
{
    // Reads from HTTP header: X-API-Key
    return Ok();
}
```

#### 6. `[FromServices]` - From Dependency Injection

```csharp
[HttpGet]
public IActionResult GetProducts([FromServices] IProductService productService)
{
    // Injected from DI container
    var products = productService.GetAll();
    return Ok(products);
}
```

---

## Complex Binding Scenarios

### 1. Multiple Sources

```csharp
[HttpPut("{id}")]
public IActionResult UpdateProduct(
    [FromRoute] int id,                    // From URL
    [FromBody] Product product,            // From request body
    [FromQuery] bool notify = false)       // From query string
{
    // URL: /api/products/5?notify=true
    // Body: { "name": "Updated Product", "price": 199.99 }
    
    // id = 5 (from route)
    // product = Product object (from body)
    // notify = true (from query string)
    
    return Ok();
}
```

### 2. Nested Objects

```csharp
public class CreateOrderRequest
{
    public Customer Customer { get; set; }
    public List<OrderItem> Items { get; set; }
    public ShippingAddress ShippingAddress { get; set; }
}

public class Customer
{
    public string Name { get; set; }
    public string Email { get; set; }
}

public class OrderItem
{
    public int ProductId { get; set; }
    public int Quantity { get; set; }
}

[HttpPost("orders")]
public IActionResult CreateOrder([FromBody] CreateOrderRequest request)
{
    // Request Body:
    // {
    //   "customer": { "name": "John", "email": "john@example.com" },
    //   "items": [
    //     { "productId": 1, "quantity": 2 },
    //     { "productId": 5, "quantity": 1 }
    //   ],
    //   "shippingAddress": { "street": "123 Main St", "city": "NYC" }
    // }
    
    // All nested objects are automatically bound!
    return Ok(request);
}
```

### 3. Collections/Arrays

```csharp
[HttpPost("bulk")]
public IActionResult BulkCreate([FromBody] List<Product> products)
{
    // Request Body:
    // [
    //   { "name": "Product 1", "price": 10.00 },
    //   { "name": "Product 2", "price": 20.00 },
    //   { "name": "Product 3", "price": 30.00 }
    // ]
    
    return Ok($"Created {products.Count} products");
}

[HttpGet]
public IActionResult GetProductsByIds([FromQuery] int[] ids)
{
    // URL: /api/products?ids=1&ids=2&ids=3
    // or: /api/products?ids=1,2,3
    
    // ids = [1, 2, 3]
    return Ok();
}
```

---

## Model Validation with Binding

```csharp
using System.ComponentModel.DataAnnotations;

public class CreateProductRequest
{
    [Required(ErrorMessage = "Product name is required")]
    [StringLength(100, MinimumLength = 3)]
    public string Name { get; set; }
    
    [Required]
    [Range(0.01, 10000.00)]
    public decimal Price { get; set; }
    
    [EmailAddress]
    public string ContactEmail { get; set; }
}

[HttpPost]
public IActionResult CreateProduct([FromBody] CreateProductRequest request)
{
    // Model binding happens first
    // Then validation runs automatically
    
    if (!ModelState.IsValid)
    {
        // Return validation errors
        return BadRequest(ModelState);
    }
    
    // If we reach here, model is valid
    return Ok("Product created successfully");
}
```

**Invalid Request Response:**
```json
{
  "errors": {
    "Name": ["Product name is required"],
    "Price": ["The field Price must be between 0.01 and 10000."]
  }
}
```

---

## Custom Model Binding

Sometimes you need custom logic for binding:

```csharp
public class CustomDateTimeBinder : IModelBinder
{
    public Task BindModelAsync(ModelBindingContext bindingContext)
    {
        var value = bindingContext.ValueProvider.GetValue("customDate");
        
        if (value == ValueProviderResult.None)
            return Task.CompletedTask;
        
        // Custom parsing logic
        if (DateTime.TryParseExact(value.FirstValue, "dd-MM-yyyy", 
            null, System.Globalization.DateTimeStyles.None, out var date))
        {
            bindingContext.Result = ModelBindingResult.Success(date);
        }
        
        return Task.CompletedTask;
    }
}

// Usage
[HttpGet]
public IActionResult GetOrders([ModelBinder(typeof(CustomDateTimeBinder))] DateTime customDate)
{
    return Ok($"Date: {customDate:dd-MM-yyyy}");
}
```

---

## Best Practices

1. ✅ **Use `[FromBody]` for complex objects** (POST, PUT requests)
2. ✅ **Use `[FromQuery]` for filtering and search parameters**
3. ✅ **Use `[FromRoute]` for resource identifiers**
4. ✅ **Always validate models** with data annotations
5. ✅ **Check `ModelState.IsValid`** before processing
6. ✅ **Use DTOs (Data Transfer Objects)** instead of domain entities
7. ❌ **Don't mix `[FromBody]` with other sources** in the same model
8. ❌ **Don't have multiple `[FromBody]` parameters** (only one allowed)

---

## Common Mistakes

### ❌ Multiple [FromBody] Parameters
```csharp
// WRONG - Only one [FromBody] allowed!
[HttpPost]
public IActionResult Create([FromBody] Product product, [FromBody] User user)
{
    return Ok();
}
```

### ✅ Use a wrapper class instead
```csharp
public class CreateRequest
{
    public Product Product { get; set; }
    public User User { get; set; }
}

[HttpPost]
public IActionResult Create([FromBody] CreateRequest request)
{
    return Ok();
}
```

---

## Summary

**Model Binding automatically converts HTTP request data into C# objects**

- Use appropriate `[From*]` attributes to specify the source
- Validate models using data annotations
- Check `ModelState.IsValid` before processing
- Keep models simple and focused (DTOs)

Model binding makes your API code clean and maintainable!
