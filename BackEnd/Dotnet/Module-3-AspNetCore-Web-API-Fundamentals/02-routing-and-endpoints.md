# 🧭 Routing & Endpoints — Mapping URLs to Actions

> **Trainer's Note:** Routing is how ASP.NET Core decides **which method** handles **which URL + HTTP verb**. Master parameters and return types here, and your APIs become predictable for frontend teammates.

---

## 📑 Table of Contents
1. [What Routing Means](#1-what-routing-means)
2. [Attribute Routing vs Conventional Routing](#2-attribute-routing-vs-conventional-routing)
3. [Building Routes with Attributes](#3-building-routes-with-attributes)
4. [Route Parameters](#4-route-parameters)
5. [Query Parameters](#5-query-parameters)
6. [Route Constraints and Defaults](#6-route-constraints-and-defaults)
7. [Returning Data from Actions](#7-returning-data-from-actions)
8. [IActionResult vs ActionResult&lt;T&gt; vs Raw Types](#8-iactionresult-vs-actionresultt-vs-raw-types)
9. [Status Helpers Deep Dive](#9-status-helpers-deep-dive)
10. [Multiple Match Pitfalls](#10-multiple-match-pitfalls)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. What Routing Means

```
Incoming request:
  GET /api/products/42?includeReviews=true

Routing answers:
  Controller = ProductsController
  Action     = GetById
  Route values: id=42
  Query: includeReviews=true
```

```
HTTP request
    → endpoint routing middleware
    → picks endpoint (controller action / minimal route)
    → model binding fills parameters
    → action runs
    → result → HTTP response
```

Without a matching route → usually **404**.

---

## 2. Attribute Routing vs Conventional Routing

### Attribute routing (API default / preferred)
Routes are declared on controllers and actions with attributes.

```csharp
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    [HttpGet("{id:int}")]
    public IActionResult Get(int id) => Ok();
}
```

### Conventional routing (classic MVC style)
Routes are defined centrally as patterns:

```csharp
app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");
```

### Comparison
| | Attribute routing | Conventional routing |
|--|-------------------|----------------------|
| Where defined | On controller/action | Central route table |
| REST APIs | **Best fit** | Rare for modern APIs |
| Readability at endpoint | Excellent | Must know global patterns |
| Fine-grained URLs | Easy | Awkward for nested REST |
| MVC HTML apps | Also used | Traditional default |

> For Web APIs: use **attribute routing** + `[ApiController]`.

`app.MapControllers()` enables attribute-routed controllers.

---

## 3. Building Routes with Attributes

### Tokens
| Token | Expands to |
|-------|------------|
| `[controller]` | Controller name without `Controller` suffix |
| `[action]` | Action method name (less common in REST) |

```csharp
[Route("api/[controller]")]  // ProductsController → api/products
```

### Absolute vs relative action routes
```csharp
[Route("api/products")]
public class ProductsController : ControllerBase
{
    [HttpGet]                 // api/products
    public IActionResult Get() => Ok();

    [HttpGet("featured")]     // api/products/featured
    public IActionResult Featured() => Ok();

    [HttpGet("/health/products")] // absolute from root: /health/products
    public IActionResult Health() => Ok();
}
```

Leading `/` on an action route resets to the site root (use sparingly).

### Verb + template together
```csharp
[HttpPost("import")]                 // POST api/products/import
[HttpDelete("{id:int}")]             // DELETE api/products/5
[HttpPut("{id:int}")]                // PUT api/products/5
[HttpGet("{productId:int}/reviews")] // nested resource style
```

---

## 4. Route Parameters

**Route parameters** are pieces of the path.

```csharp
// GET /api/products/15
[HttpGet("{id}")]
public ActionResult<ProductDto> GetById(int id)
{
    // id is bound from the URL segment
}
```

### Multiple route parameters
```csharp
// GET /api/stores/3/products/15
[HttpGet("/api/stores/{storeId:int}/products/{productId:int}")]
public IActionResult GetForStore(int storeId, int productId) => Ok();
```

### Optional route parameter
```csharp
[HttpGet("{category?}")]
public IActionResult List(string? category) => Ok(category);
```

### Catch-all parameter (rare in APIs)
```csharp
[HttpGet("files/{*path}")]
public IActionResult File(string path) => Ok(path);
```

### Naming tip
Match parameter names to route tokens:
```csharp
[HttpGet("{id}")]
public IActionResult Get(int id)   // name "id" matches {id}
```
If names differ, use `[FromRoute(Name = "id")] int productId`.

---

## 5. Query Parameters

**Query parameters** appear after `?` and are not part of the path template.

```
GET /api/products?page=2&pageSize=20&search=board
```

```csharp
[HttpGet]
public ActionResult<IEnumerable<ProductDto>> GetAll(
    [FromQuery] int page = 1,
    [FromQuery] int pageSize = 20,
    [FromQuery] string? search = null)
{
    return Ok(new { page, pageSize, search });
}
```

With `[ApiController]`, simple types often bind from query automatically for GET actions — still, `[FromQuery]` makes intent obvious.

### Route vs query — when to use which
| Use route param when | Use query param when |
|----------------------|----------------------|
| Identifies a resource (`/products/5`) | Filtering, sorting, paging |
| Required hierarchical id | Optional modifiers |
| Part of resource identity | Does not change which resource kind |

```
Good:
  GET /api/products/5
  GET /api/products?page=2&sort=price

Weak:
  GET /api/products?id=5          (id belongs in route for a single resource)
  GET /api/getProductsByPage/2    (page is not usually a resource id)
```

---

## 6. Route Constraints and Defaults

### Common constraints
| Constraint | Example | Accepts |
|------------|---------|---------|
| `int` | `{id:int}` | integers |
| `long` | `{id:long}` | long integers |
| `bool` | `{active:bool}` | true/false |
| `guid` | `{id:guid}` | GUIDs |
| `alpha` | `{name:alpha}` | letters only |
| `length(n)` | `{code:length(3)}` | exact length |
| `min(n)` / `max(n)` | `{qty:min(1)}` | bounds |
| `regex(...)` | `{sku:regex(^A\\d{{4}}$)}` | pattern |

```csharp
[HttpGet("{id:int:min(1)}")]
public IActionResult Get(int id) => Ok(id);
```

If constraint fails, routing often **skips** this endpoint (may become 404), instead of calling the action with a bad value.

### Defaults in conventional routes
```csharp
pattern: "{controller=Home}/{action=Index}/{id?}"
```
APIs usually prefer explicit attribute templates over heavy defaults.

---

## 7. Returning Data from Actions

An action can return:
1. A **raw object** → framework wraps as `200 OK` + JSON  
2. An **`IActionResult`** → you choose status + body  
3. **`ActionResult<T>`** → best of both: typed success + status helpers  

```csharp
// Raw object (always 200 if no exception)
public ProductDto Get() => new(1, "Keyboard", 1499m);

// IActionResult
public IActionResult Get(int id)
{
    var item = Find(id);
    if (item is null) return NotFound();
    return Ok(item);
}

// ActionResult<T> (recommended for APIs)
public ActionResult<ProductDto> GetTyped(int id)
{
    var item = Find(id);
    if (item is null) return NotFound();
    return item; // or return Ok(item);
}
```

---

## 8. IActionResult vs ActionResult&lt;T&gt; vs Raw Types

| Return type | Pros | Cons |
|-------------|------|------|
| `ProductDto` | Simple | Hard to return 404/400 cleanly |
| `IActionResult` | Full status control | Weaker compile-time type info for OpenAPI |
| `ActionResult<ProductDto>` | Status control **and** swagger type | Slightly more verbose |
| `Task<ActionResult<T>>` | Async APIs | Must understand async (next skills) |

### Recommended default for public APIs
```csharp
public ActionResult<ProductDto> GetById(int id) { ... }
public async Task<ActionResult<ProductDto>> GetByIdAsync(int id) { ... }
```

---

## 9. Status Helpers Deep Dive

### Ok — 200
```csharp
return Ok(product);
return Ok(new { message = "done" });
```

### NotFound — 404
```csharp
if (product is null) return NotFound();
return NotFound(new { message = $"Product {id} not found" });
```

### BadRequest — 400
```csharp
if (input.Price < 0) return BadRequest(new { error = "Price must be >= 0" });
```

### CreatedAtAction — 201 + Location
```csharp
return CreatedAtAction(
    nameof(GetById),
    new { id = created.Id },
    created);
// Location: /api/products/17
```

### CreatedAtRoute / Created
```csharp
return Created($"/api/products/{created.Id}", created);
```

### NoContent — 204
```csharp
// typical successful DELETE or PUT with no body
return NoContent();
```

### Conflict / Unauthorized / Forbid
```csharp
return Conflict(new { error = "Duplicate email" }); // 409
return Unauthorized();                               // 401
return Forbid();                                     // 403
```

### Complete CRUD sketch
```csharp
[HttpGet("{id:int}")]
public ActionResult<ProductDto> GetById(int id)
{
    var product = _store.Find(id);
    return product is null ? NotFound() : Ok(product);
}

[HttpPost]
public ActionResult<ProductDto> Create(ProductDto input)
{
    var created = _store.Add(input);
    return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
}

[HttpPut("{id:int}")]
public IActionResult Replace(int id, ProductDto input)
{
    if (id != input.Id) return BadRequest("Route id does not match body id");
    if (!_store.Exists(id)) return NotFound();
    _store.Update(input);
    return NoContent();
}

[HttpDelete("{id:int}")]
public IActionResult Delete(int id)
{
    if (!_store.Remove(id)) return NotFound();
    return NoContent();
}
```

---

## 10. Multiple Match Pitfalls

Ambiguous routes confuse runtime and teammates.

```csharp
// Risky pair:
[HttpGet("{id}")]     // matches "featured" as id string
[HttpGet("featured")]
```

**Fix:** put static segments first and/or constrain `{id:int}`:
```csharp
[HttpGet("featured")]
[HttpGet("{id:int}")]
```

### Order intuition
More **specific** routes should not be shadowed by greedy parameter routes. Constraints help the selector.

### Debugging routes
- Swagger lists mapped endpoints  
- `app.MapControllers()` missing → no controller endpoints  
- Wrong verb attribute → `405 Method Not Allowed` sometimes  
- Typo in template → `404`  

---

## 11. Knowledge Check

**Q1.** For a modern Web API, prefer attribute or conventional routing?  
**Q2.** In `/api/products/9?sort=price`, what is route vs query data?  
**Q3.** What does `{id:int}` do beyond naming the parameter?  
**Q4.** When should you return `NotFound()` instead of `Ok(null)`?  
**Q5.** Why is `ActionResult<T>` often better than raw `T`?  
**Q6.** What status does `CreatedAtAction` produce?  
**Q7.** Why can `[HttpGet("{id}")]` fight with `[HttpGet("featured")]`?

### Mini practice
Build `OrdersController`:
- `GET /api/orders` with `status` and `page` query params  
- `GET /api/orders/{id:guid}`  
- `POST /api/orders` → `201 CreatedAtAction`  
- `DELETE /api/orders/{id:guid}` → `204` or `404`  

### Answers (short)
1. Attribute routing  
2. Route: `9`; query: `sort=price`  
3. Constrains matching to integers  
4. Missing resource should be 404, not fake 200  
5. Can return proper error statuses while documenting success type  
6. 201 Created  
7. `featured` can bind as `{id}` if unconstrained — order/constraints matter  

---

## ✅ What You Should Feel Confident About

- [ ] Explain attribute vs conventional routing  
- [ ] Design clean REST paths with route + query params  
- [ ] Use constraints like `{id:int}`  
- [ ] Choose among `IActionResult`, `ActionResult<T>`, raw returns  
- [ ] Apply `Ok`, `NotFound`, `BadRequest`, `CreatedAtAction`, `NoContent`  
- [ ] Avoid ambiguous route templates  

**Previous:** [01-first-web-api.md](./01-first-web-api.md)  
**Next:** [03-models-and-dtos.md](./03-models-and-dtos.md) — models, DTOs, validation, and model binding.
