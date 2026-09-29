# 📘 API Documentation & OpenAPI — Swagger as the Shared Contract

> **Trainer's Note:** Frontends shouldn’t guess your endpoints. **OpenAPI** (often shown via **Swagger UI**) documents routes, schemas, and status codes — and lets you try APIs live. In ASP.NET Core you’ll meet **Swashbuckle** and newer **Microsoft.AspNetCore.OpenApi** options. Learn the concepts once; package names evolve.

---

## 📑 Table of Contents
1. [What OpenAPI and Swagger Are](#1-what-openapi-and-swagger-are)
2. [Why Backend Teams Use Them](#2-why-backend-teams-use-them)
3. [Add Swagger / OpenAPI to a Project](#3-add-swagger--openapi-to-a-project)
4. [Minimal Program.cs Setup (Swashbuckle Style)](#4-minimal-programcs-setup-swashbuckle-style)
5. [Swagger UI and the JSON Spec](#5-swagger-ui-and-the-json-spec)
6. [Annotating Endpoints](#6-annotating-endpoints)
7. [Documenting Status Codes and Auth](#7-documenting-status-codes-and-auth)
8. [Improving Schemas and Examples](#8-improving-schemas-and-examples)
9. [Securing and Environment Strategy](#9-securing-and-environment-strategy)
10. [Using Swagger UI for Live Testing](#10-using-swagger-ui-for-live-testing)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. What OpenAPI and Swagger Are

| Term | Meaning |
|------|---------|
| **OpenAPI** | Language-agnostic **specification** for describing HTTP APIs (formerly Swagger spec) |
| **Swagger** | Popular tooling ecosystem around OpenAPI (UI, codegen, editor) |
| **OpenAPI document** | Usually `swagger.json` / `openapi.json` describing paths & schemas |
| **Swagger UI** | Interactive HTML that reads the OpenAPI document |

```
Your ASP.NET Core API
        │ generates
        ▼
 openapi.json  (machine-readable contract)
        │ rendered by
        ▼
 Swagger UI    (human-interactive try-it-out)
```

---

## 2. Why Backend Teams Use Them

| Benefit | Detail |
|---------|--------|
| Onboarding | New devs explore APIs without tribal knowledge |
| Frontend collaboration | Clear DTOs and status codes |
| Live testing | Call endpoints with tokens from the browser |
| Code generation | Generate client SDKs (optional) |
| Contract reviews | Diff specs across versions |

OpenAPI is documentation **and** a collaboration surface — not just a pretty page.

---

## 3. Add Swagger / OpenAPI to a Project

Many `dotnet new webapi` templates already include OpenAPI/Swagger pieces.

### Swashbuckle package (classic, still widely taught)
```bash
dotnet add package Swashbuckle.AspNetCore
```

### Microsoft OpenAPI (newer template direction)
Modern .NET webapi templates may use `Microsoft.AspNetCore.OpenApi` plus scalar/swagger UI packages depending on version.

> Confirm packages against your target framework. Conceptually you always need:
> 1) a way to **generate** an OpenAPI document  
> 2) a way to **display** it (Swagger UI / Scalar)

This file shows the **Swashbuckle** style most beginners still find online; map names if your template differs.

---

## 4. Minimal Program.cs Setup (Swashbuckle Style)

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "Shop API",
        Version = "v1",
        Description = "Catalog, orders, and auth endpoints for the Shop backend."
    });
});

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();      // serves OpenAPI JSON
    app.UseSwaggerUI();    // serves interactive UI
}

app.UseHttpsRedirection();
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();
app.Run();
```

### What each call does
| Call | Role |
|------|------|
| `AddEndpointsApiExplorer` | Metadata for minimal endpoints + exploration |
| `AddSwaggerGen` | Builds OpenAPI document generation |
| `UseSwagger` | HTTP endpoint for the JSON spec |
| `UseSwaggerUI` | Browser UI |

---

## 5. Swagger UI and the JSON Spec

### Typical URLs (dev)
| URL | Content |
|-----|---------|
| `/swagger` | Swagger UI |
| `/swagger/v1/swagger.json` | OpenAPI document |

### What’s inside the JSON (conceptually)
```json
{
  "openapi": "3.0.1",
  "info": { "title": "Shop API", "version": "v1" },
  "paths": {
    "/api/products": {
      "get": { "responses": { "200": { "...": "..." } } },
      "post": { "...": "..." }
    }
  },
  "components": {
    "schemas": {
      "ProductDto": {
        "type": "object",
        "properties": {
          "id": { "type": "integer" },
          "name": { "type": "string" }
        }
      }
    }
  }
}
```

Frontends and tools can consume this file directly.

### Customize UI path/title
```csharp
app.UseSwaggerUI(c =>
{
    c.SwaggerEndpoint("/swagger/v1/swagger.json", "Shop API v1");
    c.DocumentTitle = "Shop API Docs";
});
```

---

## 6. Annotating Endpoints

### XML comments (optional but powerful)
Enable in `.csproj`:
```xml
<PropertyGroup>
  <GenerateDocumentationFile>true</GenerateDocumentationFile>
  <NoWarn>$(NoWarn);1591</NoWarn>
</PropertyGroup>
```

```csharp
builder.Services.AddSwaggerGen(options =>
{
    var xml = Path.Combine(AppContext.BaseDirectory, "Shop.Api.xml");
    if (File.Exists(xml))
        options.IncludeXmlComments(xml);
});
```

```csharp
/// <summary>Gets a product by id.</summary>
/// <param name="id">Product identifier.</param>
/// <returns>The product DTO.</returns>
/// <response code="200">Product found.</response>
/// <response code="404">Product not found.</response>
[HttpGet("{id:int}")]
[ProducesResponseType(typeof(ProductDto), StatusCodes.Status200OK)]
[ProducesResponseType(StatusCodes.Status404NotFound)]
public async Task<ActionResult<ProductDto>> GetById(int id) { /* ... */ }
```

### DataAnnotations / attributes help schemas
```csharp
public class CreateProductRequest
{
    /// <summary>Display name of the product.</summary>
    [Required, StringLength(200)]
    public string Name { get; set; } = string.Empty;

    [Range(0.01, 1_000_000)]
    public decimal Price { get; set; }
}
```

### `[Produces]` / `[Consumes]`
```csharp
[Produces("application/json")]
[Consumes("application/json")]
public class ProductsController : ControllerBase { }
```

---

## 7. Documenting Status Codes and Auth

### Explicit response types
```csharp
[HttpPost]
[ProducesResponseType(typeof(ProductDto), StatusCodes.Status201Created)]
[ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
[ProducesResponseType(StatusCodes.Status401Unauthorized)]
public async Task<ActionResult<ProductDto>> Create(CreateProductRequest request) { /* ... */ }
```

Without these, Swagger may only show generic 200s — annotations keep docs honest.

### JWT bearer in Swagger UI
```csharp
using Microsoft.OpenApi.Models;

builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo { Title = "Shop API", Version = "v1" });

    options.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Name = "Authorization",
        Type = SecuritySchemeType.Http,
        Scheme = "bearer",
        BearerFormat = "JWT",
        In = ParameterLocation.Header,
        Description = "Paste JWT only — UI may add the 'Bearer ' prefix depending on config."
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
```

Then use **Authorize** in Swagger UI to attach a token for locked endpoints.

---

## 8. Improving Schemas and Examples

### Good controller return types help schema inference
```csharp
public ActionResult<ProductDto> Get(...) 
// better than IActionResult alone when possible
```

### Example via attributes (Swashbuckle/support varies)
```csharp
[SwaggerOperation(Summary = "Create product", Description = "Creates a catalog item.")]
```
(Requires Swashbuckle annotations package if used.)

### Keep DTOs document-friendly
| Habit | Effect |
|-------|--------|
| Clear property names | Readable schemas |
| Record/class parity with real JSON | No mystery fields |
| Separate request/response DTOs | Accurate docs |
| Enum for statuses | Documented allowed values |

### Versioned docs
With API versioning (Module 6), generate one Swagger doc per version (`v1`, `v2`) so UI can switch.

---

## 9. Securing and Environment Strategy

| Environment | Recommendation |
|-------------|----------------|
| Development | Swagger UI on, detailed docs |
| Staging | Often on, maybe auth-gated |
| Production | Off by default, or locked to internal network / admin auth |

```csharp
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}
```

### Risks of public prod Swagger
- Reveals surface area to attackers  
- Invites accidental write tests against live data  
- May expose internal DTOs  

If you must expose docs in prod, require auth and use non-production datasets.

---

## 10. Using Swagger UI for Live Testing

### Happy path drill
1. Open `/swagger`  
2. Expand `POST /api/auth/login`  
3. **Try it out** → execute → copy token  
4. Click **Authorize** → paste token  
5. Call `GET /api/products` or protected routes  
6. Observe status codes and schemas  

### Validate documentation quality
| Check | Question |
|-------|----------|
| Paths | Are all public endpoints listed? |
| Schemas | Do fields match actual JSON? |
| Responses | Are 400/401/404 documented? |
| Auth | Can you exercise protected routes? |
| Examples | Can a frontend dev succeed without Slack? |

### Export the contract
Download/save `swagger.json` and share with frontend or commit a published spec artifact in CI for contract diffs.

---

## 11. Knowledge Check

**Q1.** OpenAPI vs Swagger UI in one sentence each?  
**Q2.** What does `AddSwaggerGen` + `UseSwagger` give you?  
**Q3.** Why annotate `ProducesResponseType` for 404/400?  
**Q4.** How do you let Swagger UI send JWTs?  
**Q5.** Why disable or lock Swagger in production?  
**Q6.** Where is the machine-readable contract usually served?  
**Q7.** How do XML comments improve docs?

### Mini practice
1. Enable Swagger UI in Development  
2. Set API title/description  
3. Annotate `GetById` with 200/404 response types  
4. Add Bearer security definition  
5. Login → Authorize → call a protected endpoint  
6. Open `swagger.json` and find your DTO schema  

### Answers (short)
1. OpenAPI = spec format; Swagger UI = interactive renderer  
2. Generated OpenAPI JSON + (with UI) interactive page  
3. So docs show real failure contracts, not only 200  
4. Security definition + requirement for Bearer scheme  
5. Information disclosure / accidental live writes  
6. `/swagger/v1/swagger.json` (typical Swashbuckle path)  
7. Summaries/param notes appear in the UI from doc file  

---

## ✅ What You Should Feel Confident About

- [ ] Explain OpenAPI as a contract, Swagger UI as a tool  
- [ ] Wire basic Swagger generation and UI in `Program.cs`  
- [ ] Find and read the OpenAPI JSON  
- [ ] Annotate endpoints with summaries and status codes  
- [ ] Configure Bearer auth in Swagger UI  
- [ ] Limit docs exposure by environment  

**Previous:** [01-frontend-consumption-and-cors.md](./01-frontend-consumption-and-cors.md)  
**Next:** [03-integrating-external-services.md](./03-integrating-external-services.md) — HttpClient, factories, retries, and third-party integrations.
