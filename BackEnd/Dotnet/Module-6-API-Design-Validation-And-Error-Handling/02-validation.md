# ✅ Validation — Stop Bad Data Before Business Logic

> **Trainer's Note:** Every public API is attacked by accident (typos) and on purpose (malicious payloads). Validation is your first gate: reject bad input early with **clear field errors**. Start with DataAnnotations; add FluentValidation when rules grow complex.

---

## 📑 Table of Contents
1. [Why Validation Belongs on the Server](#1-why-validation-belongs-on-the-server)
2. [DataAnnotations on Request DTOs](#2-dataannotations-on-request-dtos)
3. [`[ApiController]` Automatic 400 Behavior](#3-apicontroller-automatic-400-behavior)
4. [Structured Validation Problems](#4-structured-validation-problems)
5. [Custom Validation Attributes](#5-custom-validation-attributes)
6. [IValidatableObject for Cross-Field Rules](#6-ivalidatableobject-for-cross-field-rules)
7. [FluentValidation Overview](#7-fluentvalidation-overview)
8. [FluentValidation in ASP.NET Core](#8-fluentvalidation-in-aspnet-core)
9. [DataAnnotations vs FluentValidation](#9-dataannotations-vs-fluentvalidation)
10. [What Not to Validate Only with Attributes](#10-what-not-to-validate-only-with-attributes)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. Why Validation Belongs on the Server

```
UI validation   → good UX (optional helpers)
API validation  → mandatory trust boundary
Domain checks   → business invariants (stock, unique SKU…)
```

| Threat | Example |
|--------|---------|
| Missing fields | `{}` posted to create product |
| Wrong types | `"price": "cheap"` |
| Out of range | `quantity: -5` |
| Over-posting | Extra properties attacker hopes you bind |
| Bypass UI | curl/Postman without frontend checks |

**Never** rely on the client alone.

---

## 2. DataAnnotations on Request DTOs

Namespace: `System.ComponentModel.DataAnnotations`

```csharp
using System.ComponentModel.DataAnnotations;

public class CreateProductRequest
{
    [Required(ErrorMessage = "Name is required")]
    [StringLength(200, MinimumLength = 2)]
    public string Name { get; set; } = string.Empty;

    [Range(0.01, 1_000_000)]
    public decimal Price { get; set; }

    [Range(1, int.MaxValue)]
    public int CategoryId { get; set; }

    [EmailAddress]
    public string? SupportEmail { get; set; }

    [RegularExpression(@"^[A-Z]{3}-\d{4}$",
        ErrorMessage = "SKU must look like ABC-1234")]
    public string? Sku { get; set; }
}
```

### Common attributes
| Attribute | Use |
|-----------|-----|
| `[Required]` | Must be present |
| `[StringLength]` / `[MinLength]` / `[MaxLength]` | Text length |
| `[Range]` | Numeric bounds |
| `[EmailAddress]` | Email format |
| `[Phone]` / `[Url]` | Format helpers |
| `[RegularExpression]` | Custom pattern |
| `[Compare]` | Match another property |
| `[CreditCard]` | Basic card format (not full payment security!) |

### Record style
```csharp
public record CreateProductRequest(
    [property: Required, StringLength(200, MinimumLength = 2)] string Name,
    [property: Range(0.01, 1_000_000)] decimal Price);
```

---

## 3. `[ApiController]` Automatic 400 Behavior

```csharp
[ApiController]
[Route("api/products")]
public class ProductsController : ControllerBase
{
    [HttpPost]
    public ActionResult<ProductDto> Create(CreateProductRequest request)
    {
        // If annotations fail, you typically never enter here
        // ASP.NET Core returns 400 automatically
        return Ok();
    }
}
```

With `[ApiController]`:
1. Model binding runs  
2. Validation attributes run  
3. Invalid `ModelState` → **400** short-circuit  
4. Body often follows validation problem format  

Disable or customize only when you have a deliberate reason.

---

## 4. Structured Validation Problems

Clients need **field → error messages**, not a single vague string.

### Typical validation problem shape (ProblemDetails family)
```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.1",
  "title": "One or more validation errors occurred.",
  "status": 400,
  "errors": {
    "Name": ["Name is required"],
    "Price": ["The field Price must be between 0.01 and 1000000."]
  },
  "traceId": "00-abc..."
}
```

### Manual check when needed
```csharp
if (!ModelState.IsValid)
    return ValidationProblem(ModelState);
```

### Adding a custom model error
```csharp
ModelState.AddModelError(nameof(request.Name), "Name 'test' is reserved");
return ValidationProblem(ModelState);
```

### Consistent API habit
```
400 + validation problem  → input shape/format/rules failed
404                       → resource missing
409                       → business conflict
```

---

## 5. Custom Validation Attributes

When built-ins aren’t enough, create an attribute.

```csharp
public sealed class NoHtmlAttribute : ValidationAttribute
{
    protected override ValidationResult? IsValid(object? value, ValidationContext context)
    {
        if (value is null) return ValidationResult.Success;

        var text = value.ToString() ?? string.Empty;
        if (text.Contains('<') || text.Contains('>'))
        {
            return new ValidationResult(
                ErrorMessage ?? $"{context.DisplayName} must not contain HTML.");
        }

        return ValidationResult.Success;
    }
}
```

Usage:
```csharp
[Required, NoHtml]
public string Name { get; set; } = string.Empty;
```

### Another example — future date forbidden
```csharp
public sealed class NotInFutureAttribute : ValidationAttribute
{
    protected override ValidationResult? IsValid(object? value, ValidationContext context)
    {
        if (value is null) return ValidationResult.Success;
        if (value is DateTime dt && dt.Date > DateTime.UtcNow.Date)
            return new ValidationResult($"{context.DisplayName} cannot be in the future.");
        return ValidationResult.Success;
    }
}
```

Keep attributes **pure and fast**. Don’t hit the database inside attributes if you can help it — that belongs in services / FluentValidation with DI.

---

## 6. IValidatableObject for Cross-Field Rules

```csharp
public class CreateDiscountRequest : IValidatableObject
{
    [Required]
    public DateTime StartUtc { get; set; }

    [Required]
    public DateTime EndUtc { get; set; }

    [Range(1, 90)]
    public int PercentOff { get; set; }

    public IEnumerable<ValidationResult> Validate(ValidationContext validationContext)
    {
        if (EndUtc <= StartUtc)
        {
            yield return new ValidationResult(
                "EndUtc must be after StartUtc",
                new[] { nameof(EndUtc), nameof(StartUtc) });
        }
    }
}
```

Good for multi-property rules without a new attribute type.

---

## 7. FluentValidation Overview

**FluentValidation** is a popular library for expressing rules in dedicated **validator classes** with a fluent English-like API.

```csharp
public class CreateProductRequestValidator : AbstractValidator<CreateProductRequest>
{
    public CreateProductRequestValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Name is required")
            .Length(2, 200);

        RuleFor(x => x.Price)
            .InclusiveBetween(0.01m, 1_000_000m);

        RuleFor(x => x.CategoryId)
            .GreaterThan(0);

        RuleFor(x => x.Sku)
            .Matches(@"^[A-Z]{3}-\d{4}$")
            .When(x => !string.IsNullOrWhiteSpace(x.Sku));
    }
}
```

### Why teams adopt it
| Benefit | Detail |
|---------|--------|
| Complex rules | Conditional, dependent properties, collections |
| Testable | Validator unit tests without MVC pipeline |
| Clean DTOs | No attribute clutter on models |
| DI access | Can inject services for uniqueness checks carefully |

---

## 8. FluentValidation in ASP.NET Core

> Package install requires your approval if not already in the project. Example command:

```bash
dotnet add package FluentValidation.DependencyInjectionExtensions
```

(That meta-package commonly pulls FluentValidation core + DI extensions. Confirm current package names for your target framework.)

### Register validators
```csharp
using FluentValidation;
using FluentValidation.AspNetCore;

builder.Services.AddControllers();

// Register all validators from assembly
builder.Services.AddValidatorsFromAssemblyContaining<CreateProductRequestValidator>();

// Option A (common): integrate with ASP.NET automatic validation
builder.Services.AddFluentValidationAutoValidation();
// Optional clientside adapters for MVC — not required for pure APIs
```

> Exact extension method names can vary slightly by package version. If `AddFluentValidationAutoValidation` is unavailable, use the version’s documented ASP.NET integration or validate manually with `IValidator<T>`.

### Manual validation in endpoint/service
```csharp
public class ProductsController : ControllerBase
{
    private readonly IValidator<CreateProductRequest> _validator;

    public ProductsController(IValidator<CreateProductRequest> validator)
        => _validator = validator;

    [HttpPost]
    public async Task<ActionResult> Create(CreateProductRequest request, CancellationToken ct)
    {
        var result = await _validator.ValidateAsync(request, ct);
        if (!result.IsValid)
        {
            foreach (var error in result.Errors)
                ModelState.AddModelError(error.PropertyName, error.ErrorMessage);

            return ValidationProblem(ModelState);
        }

        // continue...
        return Ok();
    }
}
```

### Async rule example (careful with DB)
```csharp
RuleFor(x => x.Name)
    .MustAsync(async (name, ct) => !await _products.ExistsByNameAsync(name, ct))
    .WithMessage("Product name already exists");
```

Prefer returning **409 Conflict** for true uniqueness races handled in the service layer when concurrency matters — validation is not a full substitute for unique DB constraints.

---

## 9. DataAnnotations vs FluentValidation

| | DataAnnotations | FluentValidation |
|--|-----------------|------------------|
| Setup cost | Built-in | Package + registration |
| Simple required/range | Excellent | Excellent |
| Complex conditional rules | Awkward | Excellent |
| DTO cleanliness | Attributes on model | Rules external |
| DIY attributes | Possible | Less needed |
| DI in rules | Hard | Natural |
| Beginner ramp | Faster | Slightly more moving parts |

### Practical recommendation
```
Start:   DataAnnotations + [ApiController]
Grow:    IValidatableObject / custom attributes
Complex: FluentValidation for request models
Always:  domain/service checks for business integrity + DB constraints
```

You can mix: annotations for basics, FluentValidation for advanced — but avoid duplicating the same rule in two places.

---

## 10. What Not to Validate Only with Attributes

| Rule type | Better place |
|-----------|--------------|
| “SKU must be unique” | Service + unique index; optional FV MustAsync |
| “User can only edit own order” | Authorization / resource checks |
| “Price cannot drop > 50% without manager” | Domain policy / application service |
| “Card is chargeable” | Payment provider |
| File malware scan | Dedicated pipeline |

Validation attributes protect **shape and basic correctness**.  
Business transactions need deeper layers too.

---

## 11. Knowledge Check

**Q1.** Why is client-side validation not enough?  
**Q2.** What does `[ApiController]` do when DataAnnotations fail?  
**Q3.** What HTTP status is standard for validation failures?  
**Q4.** When do you write a custom `ValidationAttribute`?  
**Q5.** What is `IValidatableObject` good for?  
**Q6.** Name two advantages of FluentValidation over attributes.  
**Q7.** Should uniqueness be enforced only in a validator? Why/why not?

### Mini practice
1. Build `CreateOrderRequest` with Required/Range annotations  
2. POST invalid payloads and inspect validation problem JSON  
3. Add a custom attribute (e.g. `NoHtml`)  
4. Add a cross-field rule with `IValidatableObject`  
5. (Optional) Port rules to FluentValidation and auto-validate  

### Answers (short)
1. Clients can be bypassed  
2. Auto 400 with model state errors  
3. 400  
4. When reusable field rules aren’t built-in  
5. Cross-property validation on the same object  
6. Complex/conditional rules, cleaner DTOs, testability, DI  
7. No — race conditions need DB constraints/transactions too  

---

## ✅ What You Should Feel Confident About

- [ ] Annotate request DTOs with DataAnnotations  
- [ ] Read and return structured validation errors  
- [ ] Write a custom validation attribute  
- [ ] Use `IValidatableObject` for multi-field rules  
- [ ] Explain when to introduce FluentValidation  
- [ ] Keep business invariants out of “format-only” validation  

**Previous:** [01-restful-api-design.md](./01-restful-api-design.md)  
**Next:** [03-error-handling.md](./03-error-handling.md) — global exception handling and Problem Details.
