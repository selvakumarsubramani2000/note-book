# 📋 Models & DTOs — Shapes of Data In and Out

> **Trainer's Note:** Bad APIs leak database tables straight to the client. Good APIs use **DTOs** at the boundary, **domain models** inside, and **validation** before business logic runs. This file makes that separation practical.

---

## 📑 Table of Contents
1. [Why Models Matter at the API Boundary](#1-why-models-matter-at-the-api-boundary)
2. [Domain Models vs DTOs](#2-domain-models-vs-dtos)
3. [Designing Request and Response DTOs](#3-designing-request-and-response-dtos)
4. [DataAnnotations Validation](#4-dataannotations-validation)
5. [Model Binding Basics](#5-model-binding-basics)
6. [`[FromBody]`, `[FromQuery]`, `[FromRoute]`, and Friends](#6-frombody-fromquery-fromroute-and-friends)
7. [Automatic Model Validation with `[ApiController]`](#7-automatic-model-validation-with-apicontroller)
8. [Manual Validation and ModelState](#8-manual-validation-and-modelstate)
9. [Mapping Between Domain and DTO](#9-mapping-between-domain-and-dto)
10. [Common Pitfalls](#10-common-pitfalls)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. Why Models Matter at the API Boundary

JSON in/out must become C# objects. Those objects should be **intentional contracts**, not accidental dumps of everything you store.

```
Client JSON
    → Model binding
    → Validation
    → Map to domain / call service
    → Map to response DTO
    → JSON out
```

| Goal | Practice |
|------|----------|
| Stability | Clients depend on DTO shape, not DB schema |
| Security | Hide internal fields (password hashes, tokens) |
| Clarity | Separate create-request from full entity |
| Validation | Reject junk before business rules |

---

## 2. Domain Models vs DTOs

| | Domain model | DTO (Data Transfer Object) |
|--|--------------|----------------------------|
| Lives | Core / business layer | API boundary |
| Purpose | Business meaning & rules | Carry data across process boundary |
| Contains behavior? | Often yes (methods, invariants) | Usually little/no behavior |
| Exposed on HTTP? | Prefer **no** | **Yes** |
| Changes when | Business rules change | API contract needs change |

### Domain example
```csharp
public class Product
{
    public int Id { get; private set; }
    public string Name { get; private set; }
    public decimal Price { get; private set; }
    public bool IsArchived { get; private set; }

    public Product(string name, decimal price)
    {
        Rename(name);
        SetPrice(price);
    }

    public void SetPrice(decimal price)
    {
        if (price < 0) throw new ArgumentOutOfRangeException(nameof(price));
        Price = price;
    }

    public void Rename(string name)
    {
        if (string.IsNullOrWhiteSpace(name)) throw new ArgumentException("Name required");
        Name = name.Trim();
    }

    public void Archive() => IsArchived = true;
}
```

### DTO examples
```csharp
public record ProductResponseDto(int Id, string Name, decimal Price);

public record CreateProductRequestDto(string Name, decimal Price);

public record UpdateProductPriceRequestDto(decimal Price);
```

### Why not return domain entities directly?
1. Over-exposes fields (`IsArchived`, navigation collections, persistence flags)  
2. Serialization can blow up on cycles (entity graphs)  
3. Breaking DB changes break API clients  
4. Harder to version contracts  

```
❌ Controller → returns EF entity graph
✅ Controller → returns ProductResponseDto
```

---

## 3. Designing Request and Response DTOs

### Split by use-case
| DTO | Fields |
|-----|--------|
| `CreateProductRequestDto` | Name, Price (no Id) |
| `UpdateProductRequestDto` | Name, Price |
| `ProductResponseDto` | Id, Name, Price |
| `ProductListItemDto` | Id, Name (lighter list shape) |

### Records work great for DTOs
```csharp
public record CreateProductRequestDto(string Name, decimal Price);
```

### Classes are fine too
```csharp
public class CreateProductRequestDto
{
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }
}
```

### Naming conventions (pick one and stay consistent)
```
CreateProductRequest / CreateProductRequestDto
ProductResponse / ProductDto
ProductDetailsDto
```

---

## 4. DataAnnotations Validation

Namespace: `System.ComponentModel.DataAnnotations`

Attach attributes to DTO properties so ASP.NET Core can validate automatically.

```csharp
using System.ComponentModel.DataAnnotations;

public class CreateProductRequestDto
{
    [Required(ErrorMessage = "Name is required")]
    [StringLength(100, MinimumLength = 2)]
    public string Name { get; set; } = string.Empty;

    [Range(0.01, 1_000_000)]
    public decimal Price { get; set; }

    [EmailAddress]
    public string? SupportEmail { get; set; }
}
```

### Common attributes
| Attribute | Validates |
|-----------|-----------|
| `[Required]` | Not null / missing (strings: not null; combine with min length for non-empty) |
| `[StringLength(max, MinimumLength = min)]` | Text length |
| `[MinLength]` / `[MaxLength]` | Length for strings/collections |
| `[Range(min, max)]` | Numeric bounds |
| `[EmailAddress]` | Email format |
| `[Phone]` | Phone format |
| `[Url]` | URL format |
| `[RegularExpression(pattern)]` | Custom pattern |
| `[Compare("OtherProp")]` | Match another property (e.g., password confirm) |

### On record positional DTOs
```csharp
public record CreateProductRequestDto(
    [property: Required, StringLength(100, MinimumLength = 2)] string Name,
    [property: Range(0.01, 1_000_000)] decimal Price);
```

### Validation is not full business logic
```
DataAnnotations  → shape/format/required field checks
Domain/service   → "price cannot exceed category cap", "SKU unique", etc.
```

---

## 5. Model Binding Basics

**Model binding** = convert request data into action parameters / objects.

```
Route values    ─┐
Query string    ─┼→  C# parameters
Headers         ─┤
Body (JSON)     ─┘
```

```csharp
[HttpGet("{id:int}")]
public ActionResult<ProductResponseDto> Get(
    int id,                          // from route
    [FromQuery] bool includeDetails  // from query
)
```

```csharp
[HttpPost]
public ActionResult<ProductResponseDto> Create(
    CreateProductRequestDto request  // from body (JSON) typically
)
```

If binding fails type conversion, model state becomes invalid (e.g., `id=abc` for `int`).

---

## 6. `[FromBody]`, `[FromQuery]`, `[FromRoute]`, and Friends

| Attribute | Reads from | Typical use |
|-----------|------------|-------------|
| `[FromRoute]` | URL path tokens | `id`, guids |
| `[FromQuery]` | Query string | filters, paging |
| `[FromBody]` | Request body | JSON payloads on POST/PUT/PATCH |
| `[FromHeader]` | Headers | custom header values |
| `[FromForm]` | Form fields | `multipart/form-data` uploads |
| `[FromServices]` | DI container | rare parameter injection |

```csharp
[HttpPut("{id:int}")]
public IActionResult Update(
    [FromRoute] int id,
    [FromBody] UpdateProductRequestDto body)
{
    if (id <= 0) return BadRequest();
    return NoContent();
}
```

```csharp
[HttpGet]
public IActionResult Search(
    [FromQuery] string? q,
    [FromQuery] int page = 1,
    [FromHeader(Name = "X-Correlation-Id")] string? correlationId = null)
    => Ok(new { q, page, correlationId });
```

### `[ApiController]` inference (helpful defaults)
For API controllers, complex types often default to **body**, simple types to **route/query**.  
Explicit attributes still improve readability — especially for teammates new to the stack.

### Only one body
You cannot bind two `[FromBody]` parameters to two separate JSON objects easily. Use **one** DTO that holds all body fields.

---

## 7. Automatic Model Validation with `[ApiController]`

When the controller has `[ApiController]`:
1. Binding + DataAnnotations run  
2. If `ModelState` is invalid → framework short-circuits with **400**  
3. Response often uses **ProblemDetails / validation problem** format  

```csharp
[ApiController]
[Route("api/products")]
public class ProductsController : ControllerBase
{
    [HttpPost]
    public ActionResult<ProductResponseDto> Create(CreateProductRequestDto request)
    {
        // If Name missing → you usually never enter here; 400 already returned
        var product = new Product(request.Name, request.Price);
        // save...
        var response = new ProductResponseDto(product.Id, product.Name, product.Price);
        return CreatedAtAction(nameof(GetById), new { id = response.Id }, response);
    }
}
```

### Example invalid POST body
```json
{
  "name": "",
  "price": -5
}
```
Client receives **400** with field error details — without manual `if` checks for every attribute.

---

## 8. Manual Validation and ModelState

Sometimes you still check `ModelState` or add custom errors:

```csharp
[HttpPost]
public IActionResult Create(CreateProductRequestDto request)
{
    if (request.Name.Equals("test", StringComparison.OrdinalIgnoreCase))
        ModelState.AddModelError(nameof(request.Name), "Name 'test' is reserved");

    if (!ModelState.IsValid)
        return ValidationProblem(ModelState);

    return Ok();
}
```

Useful when:
- Cross-field rules not expressible by one attribute  
- Rules need database lookup (often better in service layer returning a result)  

---

## 9. Mapping Between Domain and DTO

### Manual mapping (best for learning)
```csharp
public static class ProductMapper
{
    public static ProductResponseDto ToResponse(Product product) =>
        new(product.Id, product.Name, product.Price);

    public static Product ToDomain(CreateProductRequestDto dto) =>
        new(dto.Name, dto.Price);
}
```

### In controller (thin)
```csharp
[HttpPost]
public ActionResult<ProductResponseDto> Create(CreateProductRequestDto request)
{
    var product = ProductMapper.ToDomain(request);
    _service.Add(product);
    return CreatedAtAction(nameof(GetById), new { id = product.Id }, ProductMapper.ToResponse(product));
}
```

### Later tools (awareness)
- AutoMapper, Mapperly, Mapster — reduce boilerplate once patterns are clear  
- Learn manual mapping first so you understand what libraries hide  

---

## 10. Common Pitfalls

| Pitfall | Better approach |
|---------|-----------------|
| Expose EF entities on endpoints | Return DTOs |
| One giant `ProductDto` for all verbs | Split create/update/response |
| Validate only on client UI | Always validate on server |
| Put DB attributes on API DTOs carelessly | Keep persistence concerns in infrastructure entities |
| Accept more fields than you need | Prefer explicit request DTOs (mass-assignment safety) |
| Over-nest huge graphs in responses | Flatten or paginate |

### Over-posting awareness
If update DTO includes `IsAdmin` and you bind straight onto a domain/user entity, clients might set privileges. Separate DTOs prevent whole classes of bugs.

---

## 11. Knowledge Check

**Q1.** What does DTO stand for, and where does it live architecturally?  
**Q2.** Why is returning EF entities from controllers risky?  
**Q3.** Which attribute ensures a string property must be present?  
**Q4.** `[FromRoute]` vs `[FromQuery]` vs `[FromBody]` — one example each.  
**Q5.** What happens to invalid DataAnnotations under `[ApiController]`?  
**Q6.** Should uniqueness of email be only a `[Required]` check? Why/why not?  
**Q7.** Why prefer separate Create and Response DTOs?

### Mini practice
1. Create `Customer` domain model with guarded email/name  
2. Create `CreateCustomerRequestDto` with `[Required]`, `[EmailAddress]`, `[StringLength]`  
3. Create `CustomerResponseDto`  
4. POST endpoint binds body, validates, maps to domain, returns `201` + response DTO  
5. Send invalid JSON in Swagger and inspect 400 payload  

### Answers (short)
1. Data Transfer Object — API boundary contract  
2. Leaks internals, cycles, coupling, security fields  
3. `[Required]`  
4. Route id; `?page=1`; JSON body on POST  
5. Automatic 400 validation response  
6. No — uniqueness needs store/service check  
7. Different fields and lifecycle; cleaner contracts; safer binding  

---

## ✅ What You Should Feel Confident About

- [ ] Explain domain model vs DTO  
- [ ] Design request/response DTOs per use-case  
- [ ] Apply DataAnnotations for input validation  
- [ ] Use `[FromBody]` / `[FromQuery]` / `[FromRoute]` deliberately  
- [ ] Rely on `[ApiController]` validation behavior  
- [ ] Map DTO ↔ domain without leaking persistence details  

**Previous:** [02-routing-and-endpoints.md](./02-routing-and-endpoints.md)  
**Next:** [04-dependency-injection.md](./04-dependency-injection.md) — services, lifetimes, and clean controllers.
