# Question 10: How would you set a property as a required field in your model?

## Answer

There are **multiple ways** to make a property required in .NET Core Web API. Let me show you all the common approaches!

---

## 1. Using `[Required]` Data Annotation (Most Common)

### Basic Usage

```csharp
using System.ComponentModel.DataAnnotations;

public class Product
{
    [Required]
    public string Name { get; set; }
    
    [Required]
    public decimal Price { get; set; }
    
    public string Description { get; set; } // Optional (no [Required])
}
```

### With Custom Error Message

```csharp
public class User
{
    [Required(ErrorMessage = "Username is required")]
    public string Username { get; set; }
    
    [Required(ErrorMessage = "Email address is mandatory")]
    public string Email { get; set; }
    
    [Required(ErrorMessage = "Please provide a password")]
    public string Password { get; set; }
}
```

### In Controller - Validation

```csharp
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    [HttpPost]
    public IActionResult Create([FromBody] Product product)
    {
        // Automatically validated before reaching here
        if (!ModelState.IsValid)
        {
            return BadRequest(ModelState); // Returns validation errors
        }
        
        // If we reach here, all required fields are present
        return Ok("Product created successfully");
    }
}
```

**Request without required field:**
```json
{
  "description": "This is a product"
}
```

**Response (400 Bad Request):**
```json
{
  "errors": {
    "Name": ["The Name field is required."],
    "Price": ["The Price field is required."]
  }
}
```

---

## 2. Using Non-Nullable Reference Types (C# 8.0+)

### Enable Nullable Reference Types

In your `.csproj` file:
```xml
<PropertyGroup>
    <Nullable>enable</Nullable>
</PropertyGroup>
```

### Usage

```csharp
public class Product
{
    // Non-nullable - implicitly required
    public string Name { get; set; } = string.Empty;
    
    // Non-nullable - implicitly required
    public int Price { get; set; }
    
    // Nullable - optional
    public string? Description { get; set; }
    
    // Nullable - optional
    public int? Discount { get; set; }
}
```

**Benefits:**
- Compile-time warnings for potential null values
- Works with ASP.NET Core automatic validation
- More type-safe

---

## 3. Combined Approach (Best Practice)

Use **both** nullable reference types AND data annotations for maximum validation:

```csharp
#nullable enable
using System.ComponentModel.DataAnnotations;

public class CreateUserRequest
{
    [Required(ErrorMessage = "Name is required")]
    [StringLength(100, MinimumLength = 2, ErrorMessage = "Name must be between 2 and 100 characters")]
    public string Name { get; set; } = string.Empty;
    
    [Required(ErrorMessage = "Email is required")]
    [EmailAddress(ErrorMessage = "Invalid email format")]
    public string Email { get; set; } = string.Empty;
    
    [Required(ErrorMessage = "Password is required")]
    [StringLength(50, MinimumLength = 8, ErrorMessage = "Password must be between 8 and 50 characters")]
    [RegularExpression(@"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$", 
        ErrorMessage = "Password must contain at least one uppercase, one lowercase, and one digit")]
    public string Password { get; set; } = string.Empty;
    
    [Required]
    [Range(18, 100, ErrorMessage = "Age must be between 18 and 100")]
    public int Age { get; set; }
    
    // Optional fields
    public string? PhoneNumber { get; set; }
    public string? Address { get; set; }
}
```

---

## 4. Multiple Validation Attributes

### Common Combinations

```csharp
public class ProductModel
{
    // Required + Length constraint
    [Required(ErrorMessage = "Product name is required")]
    [StringLength(100, MinimumLength = 3, ErrorMessage = "Name must be 3-100 characters")]
    public string Name { get; set; }
    
    // Required + Range
    [Required]
    [Range(0.01, 999999.99, ErrorMessage = "Price must be between 0.01 and 999999.99")]
    public decimal Price { get; set; }
    
    // Required + Regex pattern
    [Required]
    [RegularExpression(@"^[A-Z]{2}-\d{4}$", ErrorMessage = "SKU must be in format: XX-0000")]
    public string SKU { get; set; }
    
    // Required + Email validation
    [Required]
    [EmailAddress(ErrorMessage = "Invalid email address")]
    public string ContactEmail { get; set; }
    
    // Required + URL validation
    [Required]
    [Url(ErrorMessage = "Invalid URL format")]
    public string Website { get; set; }
    
    // Required for collections
    [Required]
    [MinLength(1, ErrorMessage = "At least one category is required")]
    public List<string> Categories { get; set; }
}
```

---

## 5. AllowEmptyStrings Option

By default, `[Required]` treats empty strings as invalid. You can change this:

```csharp
public class ExampleModel
{
    // Empty strings NOT allowed (default)
    [Required]
    public string Name { get; set; }
    
    // Empty strings ARE allowed (only null is invalid)
    [Required(AllowEmptyStrings = true)]
    public string Description { get; set; }
}
```

---

## 6. Custom Validation for Required Fields

### Custom Validation Attribute

```csharp
using System.ComponentModel.DataAnnotations;

public class RequiredIfAttribute : ValidationAttribute
{
    private readonly string _otherProperty;
    
    public RequiredIfAttribute(string otherProperty)
    {
        _otherProperty = otherProperty;
    }
    
    protected override ValidationResult IsValid(object value, ValidationContext validationContext)
    {
        var otherPropertyInfo = validationContext.ObjectType.GetProperty(_otherProperty);
        var otherPropertyValue = otherPropertyInfo?.GetValue(validationContext.ObjectInstance);
        
        if (otherPropertyValue != null && value == null)
        {
            return new ValidationResult($"{validationContext.DisplayName} is required");
        }
        
        return ValidationResult.Success;
    }
}

// Usage
public class OrderModel
{
    public bool RequireShipping { get; set; }
    
    // ShippingAddress is required only if RequireShipping is true
    [RequiredIf(nameof(RequireShipping))]
    public string ShippingAddress { get; set; }
}
```

---

## 7. Validating in Controller with Custom Logic

```csharp
[HttpPost]
public IActionResult CreateProduct([FromBody] Product product)
{
    // Automatic model validation
    if (!ModelState.IsValid)
    {
        return BadRequest(ModelState);
    }
    
    // Custom business logic validation
    if (string.IsNullOrWhiteSpace(product.Name))
    {
        ModelState.AddModelError(nameof(product.Name), "Name cannot be only whitespace");
    }
    
    if (product.Price <= 0)
    {
        ModelState.AddModelError(nameof(product.Price), "Price must be greater than zero");
    }
    
    // Check again after custom validation
    if (!ModelState.IsValid)
    {
        return BadRequest(ModelState);
    }
    
    // Process valid product
    return Ok("Product created");
}
```

---

## 8. Using FluentValidation (Alternative Library)

### Install Package
```bash
dotnet add package FluentValidation.AspNetCore
```

### Create Validator

```csharp
using FluentValidation;

public class ProductValidator : AbstractValidator<Product>
{
    public ProductValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Product name is required")
            .Length(3, 100).WithMessage("Name must be between 3 and 100 characters");
        
        RuleFor(x => x.Price)
            .NotEmpty().WithMessage("Price is required")
            .GreaterThan(0).WithMessage("Price must be greater than 0");
        
        RuleFor(x => x.Email)
            .NotEmpty().WithMessage("Email is required")
            .EmailAddress().WithMessage("Invalid email format");
    }
}

// Register in Startup.cs
public void ConfigureServices(IServiceCollection services)
{
    services.AddControllers()
        .AddFluentValidation(fv => fv.RegisterValidatorsFromAssemblyContaining<ProductValidator>());
}
```

---

## 9. Complete Real-World Example

```csharp
using System.ComponentModel.DataAnnotations;

public class CreateUserRequest
{
    [Required(ErrorMessage = "First name is required")]
    [StringLength(50, MinimumLength = 2)]
    public string FirstName { get; set; } = string.Empty;
    
    [Required(ErrorMessage = "Last name is required")]
    [StringLength(50, MinimumLength = 2)]
    public string LastName { get; set; } = string.Empty;
    
    [Required(ErrorMessage = "Email is required")]
    [EmailAddress(ErrorMessage = "Invalid email address")]
    public string Email { get; set; } = string.Empty;
    
    [Required(ErrorMessage = "Password is required")]
    [StringLength(100, MinimumLength = 8, ErrorMessage = "Password must be at least 8 characters")]
    [DataType(DataType.Password)]
    public string Password { get; set; } = string.Empty;
    
    [Required]
    [Compare(nameof(Password), ErrorMessage = "Passwords do not match")]
    [DataType(DataType.Password)]
    public string ConfirmPassword { get; set; } = string.Empty;
    
    [Required]
    [Range(18, 120, ErrorMessage = "Age must be between 18 and 120")]
    public int Age { get; set; }
    
    [Required]
    [Phone(ErrorMessage = "Invalid phone number")]
    public string PhoneNumber { get; set; } = string.Empty;
    
    // Optional fields
    public string? MiddleName { get; set; }
    public string? Address { get; set; }
}

[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    [HttpPost]
    public IActionResult CreateUser([FromBody] CreateUserRequest request)
    {
        if (!ModelState.IsValid)
        {
            var errors = ModelState
                .Where(x => x.Value.Errors.Any())
                .Select(x => new
                {
                    Field = x.Key,
                    Errors = x.Value.Errors.Select(e => e.ErrorMessage)
                });
            
            return BadRequest(new { errors });
        }
        
        // Process valid user
        return Ok("User created successfully");
    }
}
```

---

## 10. API Behavior Options (Global Configuration)

```csharp
// In Startup.cs or Program.cs
public void ConfigureServices(IServiceCollection services)
{
    services.AddControllers()
        .ConfigureApiBehaviorOptions(options =>
        {
            // Automatically return 400 BadRequest for invalid models
            options.InvalidModelStateResponseFactory = context =>
            {
                var errors = context.ModelState
                    .Where(e => e.Value.Errors.Count > 0)
                    .Select(e => new
                    {
                        Name = e.Key,
                        Message = e.Value.Errors.First().ErrorMessage
                    });
                
                return new BadRequestObjectResult(new
                {
                    Message = "Validation failed",
                    Errors = errors
                });
            };
        });
}
```

---

## Summary

**Most Common Approach:**
```csharp
[Required(ErrorMessage = "Custom error message")]
public string PropertyName { get; set; } = string.Empty;
```

**Key Points:**
- ✅ Use `[Required]` data annotation
- ✅ Always check `ModelState.IsValid` in controllers
- ✅ Combine with other validation attributes for robust validation
- ✅ Use nullable reference types for compile-time safety
- ✅ Provide clear, user-friendly error messages

**The validation happens automatically when the model is bound!**
