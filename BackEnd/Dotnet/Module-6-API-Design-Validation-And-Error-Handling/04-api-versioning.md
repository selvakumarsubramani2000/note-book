# 📌 API Versioning — Change Without Breaking Clients

> **Trainer's Note:** Your first API will change. Field renames, auth shifts, pagination formats — clients break if you only edit v1 in place. **Versioning** lets old apps keep working while new apps adopt improved contracts. Design for change early, implement when it starts to hurt — but understand strategies now.

---

## 📑 Table of Contents
1. [Why APIs Need Versions](#1-why-apis-need-versions)
2. [What Counts as a Breaking Change?](#2-what-counts-as-a-breaking-change)
3. [Versioning Strategies Overview](#3-versioning-strategies-overview)
4. [URL-Based Versioning](#4-url-based-versioning)
5. [Header-Based Versioning](#5-header-based-versioning)
6. [Query String Versioning (Awareness)](#6-query-string-versioning-awareness)
7. [ASP.NET Core API Versioning Libraries](#7-aspnet-core-api-versioning-libraries)
8. [Configure Versioning in Program.cs](#8-configure-versioning-in-programcs)
9. [Versioning Controllers](#9-versioning-controllers)
10. [Deprecation, Sunset, and Team Practices](#10-deprecation-sunset-and-team-practices)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. Why APIs Need Versions

```
Mobile app v3.2 still in the wild
   uses GET /api/products → expects price as number

You change price to { amount, currency } object
   without versioning
      → mobile crashes
```

| Reality | Impact |
|---------|--------|
| Multiple clients | Not everyone deploys the same day |
| Long-lived mobile apps | Store review delays |
| Partner integrations | External teams move slowly |
| Continuous delivery | Backend ships weekly |

Versioning = **compatibility insurance**.

---

## 2. What Counts as a Breaking Change?

### Usually breaking
- Remove/rename a field  
- Change field type (`string` → `object`)  
- Make optional field required  
- Change auth requirements unexpectedly  
- Change URL paths clients call  
- Change status code meanings clients depend on  
- Tighten validation that rejects previously valid payloads  

### Often non-breaking (additive)
- Add a new optional response field  
- Add a new endpoint  
- Add optional query parameter with default  
- Loosen validation carefully  

```
Safe evolution idea:
  v1 keeps old shape
  v2 introduces new shape
  sunset v1 after clients migrate
```

Not every tweak needs a new version — additive changes can stay in the same version if you guarantee backward compatibility.

---

## 3. Versioning Strategies Overview

| Strategy | Example | Pros | Cons |
|----------|---------|------|------|
| **URL path** | `/api/v1/products` | Very visible, easy to try in browser | URL changes per version |
| **Header** | `X-Api-Version: 1` or media type | Clean URLs | Harder to discover/debug casually |
| **Query string** | `/api/products?api-version=1.0` | Simple | Easy to omit; caches/proxies quirks |
| **Media type** | `Accept: application/vnd.shop.v2+json` | HTTP-pure | Verbose; less beginner-friendly |

For most beginner/intermediate APIs, **URL path versioning** is the clearest teaching and onboarding choice. Many enterprises use headers.

---

## 4. URL-Based Versioning

```
/api/v1/products
/api/v2/products
```

### Controllers sketch
```csharp
[ApiController]
[ApiVersion("1.0")]
[Route("api/v{version:apiVersion}/products")]
public class ProductsV1Controller : ControllerBase
{
    [HttpGet]
    public ActionResult<IEnumerable<ProductV1Dto>> Get() => Ok(/* v1 shape */);
}

[ApiController]
[ApiVersion("2.0")]
[Route("api/v{version:apiVersion}/products")]
public class ProductsV2Controller : ControllerBase
{
    [HttpGet]
    public ActionResult<IEnumerable<ProductV2Dto>> Get() => Ok(/* v2 shape */);
}
```

### Pros in daily work
- Visible in logs and support tickets  
- Easy Swagger separation  
- Easy gateway routing rules  

### Cons
- Duplicate controllers/code unless carefully shared  
- “REST purists” argue resource identity shouldn’t include version (practicality usually wins)

---

## 5. Header-Based Versioning

```http
GET /api/products HTTP/1.1
Host: api.shop.local
X-Api-Version: 2.0
```

or:

```http
Accept: application/json; version=2.0
```

### Pros
- Stable public URLs  
- Same path maps to multiple implementations  

### Cons
- Easy for clients to forget header  
- Browser address-bar testing weaker  
- Caching must vary by header  

Use when public URL cleanliness is a product requirement or when an API gateway already standardizes version headers.

---

## 6. Query String Versioning (Awareness)

```
GET /api/products?api-version=1.0
```

| Good for | Caution |
|----------|---------|
| Quick internal tools | Default version required |
| Prototypes | Unattractive public contracts |
| Library defaults often support it | Easy to leave off and hit wrong version |

---

## 7. ASP.NET Core API Versioning Libraries

Microsoft’s API versioning stack evolved over time. Common modern packages (names can vary by generation):

```bash
# Example set — confirm current package IDs for your .NET version
dotnet add package Asp.Versioning.Http
dotnet add package Asp.Versioning.Mvc
dotnet add package Asp.Versioning.Mvc.ApiExplorer
```

Older tutorials mention `Microsoft.AspNetCore.Mvc.Versioning`. Prefer the **current Asp.Versioning.*** packages for new work on modern .NET.

| Package area | Role |
|--------------|------|
| Http/Mvc versioning | Read version from URL/header/query; select controllers |
| ApiExplorer | Swagger/OpenAPI versioned docs |

> **Note:** Exact APIs differ slightly by package major version. Treat the following as the **standard pattern**; adjust namespaces (`Asp.Versioning`) to match the package you install.

---

## 8. Configure Versioning in Program.cs

```csharp
using Asp.Versioning;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();

builder.Services
    .AddApiVersioning(options =>
    {
        options.DefaultApiVersion = new ApiVersion(1, 0);
        options.AssumeDefaultVersionWhenUnspecified = true;
        options.ReportApiVersions = true; // adds api-supported-versions headers

        // URL segment + header readers (pick what you support)
        options.ApiVersionReader = ApiVersionReader.Combine(
            new UrlSegmentApiVersionReader(),
            new HeaderApiVersionReader("X-Api-Version"),
            new QueryStringApiVersionReader("api-version"));
    })
    .AddMvc() // controller model binding support
    .AddApiExplorer(options =>
    {
        options.GroupNameFormat = "'v'VVV"; // v1, v2
        options.SubstituteApiVersionInUrl = true;
    });

var app = builder.Build();
app.MapControllers();
app.Run();
```

### Key options
| Option | Meaning |
|--------|---------|
| `DefaultApiVersion` | Fallback version |
| `AssumeDefaultVersionWhenUnspecified` | If client omits version, use default |
| `ReportApiVersions` | Advertise supported/deprecated versions in response headers |
| `ApiVersionReader` | Where to read version from |

### Swagger tip
Generate one OpenAPI doc **per version** (v1, v2) using ApiExplorer group names so clients see the correct routes and schemas.

---

## 9. Versioning Controllers

### Attributes
```csharp
[ApiVersion("1.0")]
[ApiVersion("2.0")] // same controller serving dual versions (optional)
[Route("api/v{version:apiVersion}/orders")]
public class OrdersController : ControllerBase
{
    [HttpGet]
    [MapToApiVersion("1.0")]
    public IActionResult GetV1() => Ok("v1");

    [HttpGet]
    [MapToApiVersion("2.0")]
    public IActionResult GetV2() => Ok("v2");
}
```

### Separate controllers per version (often clearer)
```
Controllers/
  v1/ProductsController.cs
  v2/ProductsController.cs
```

Share application services underneath; only map different DTOs at the edge.

```
v1 controller → old DTO shape
v2 controller → new DTO shape
        \\     //
        services / domain
              │
           database
```

### Neutral routes without version
Health checks often stay unversioned:
```
GET /health
GET /swagger
```

---

## 10. Deprecation, Sunset, and Team Practices

### Mark deprecated version
```csharp
[ApiVersion("1.0", Deprecated = true)]
```

With `ReportApiVersions = true`, responses may include headers like:
```
api-supported-versions: 2.0
api-deprecated-versions: 1.0
```

### Sunset policy (product practice)
| Step | Action |
|------|--------|
| 1 | Ship v2 alongside v1 |
| 2 | Announce deprecation date |
| 3 | Monitor v1 traffic |
| 4 | Return `Deprecation`/`Sunset` headers if you adopt them |
| 5 | Remove v1 code after migration |

### Team rules of thumb
1. Prefer additive change inside a version when possible  
2. New breaking contract → new version  
3. Don’t maintain infinite versions (cost explodes)  
4. Contract tests per version  
5. Document migration guides (`price` number → `money` object)  
6. Keep shared business logic version-agnostic  

### When *not* to version yet
Internal prototype with one client you control — still design DTOs carefully so the first public release can freeze as v1.

---

## 11. Knowledge Check

**Q1.** Why is “just change the live API” dangerous with mobile clients?  
**Q2.** Name two breaking changes and two non-breaking changes.  
**Q3.** URL vs header versioning — one pro each.  
**Q4.** What does `AssumeDefaultVersionWhenUnspecified` do?  
**Q5.** Where should version differences live — domain core or API edge DTOs/controllers?  
**Q6.** What is API deprecation trying to achieve?  
**Q7.** Why share services across v1/v2 controllers?

### Mini practice
1. Add versioning packages appropriate for your .NET version  
2. Configure default v1.0 + URL reader  
3. Create `GET /api/v1/products` and `GET /api/v2/products` with different DTO shapes  
4. Call both URLs and compare JSON  
5. Mark v1 deprecated and observe version headers  
6. Write a short migration note for clients  

### Answers (short)
1. Old binaries keep calling; breaks in the wild  
2. Breaking: remove field, change type; non-breaking: add optional field, add endpoint  
3. URL visible/debuggable; header keeps clean paths  
4. Uses default version when client omits one  
5. API edge (controllers/DTOs); keep domain stable  
6. Give clients time to migrate before removal  
7. Avoid duplicating business rules — only contracts differ  

---

## ✅ What You Should Feel Confident About

- [ ] Explain why versioning exists  
- [ ] Spot breaking vs additive changes  
- [ ] Compare URL vs header strategies  
- [ ] Configure ASP.NET Core API versioning basics  
- [ ] Map controllers/actions to versions  
- [ ] Plan deprecation instead of hard cuts  

**Previous:** [03-error-handling.md](./03-error-handling.md)

---

## 🚀 Module 6 Wrap-Up

You can now design **robust, REST-compliant** ASP.NET Core APIs with:

| Skill | File |
|-------|------|
| Resource URLs, verbs, safety/idempotency, status codes | 01 |
| DataAnnotations, custom validation, FluentValidation, validation problems | 02 |
| Global exception handling, Problem Details, safe logging, 404/400/409 | 03 |
| API versioning strategies + Asp.Versioning configuration | 04 |

### Production-minded API checklist
- [ ] Noun-based routes; correct HTTP verbs  
- [ ] Status codes match outcomes (no fake all-200s)  
- [ ] Input validated at the boundary  
- [ ] Errors return consistent `application/problem+json`  
- [ ] Stacks/secrets only in logs, not client payloads  
- [ ] Breaking contract changes ship under a new version  
- [ ] Deprecated versions monitored and sunset intentionally  

```
Client request
   → version selected
   → authn/authz
   → validation
   → controller/service
   → success DTO  OR  problem details error
```

**Suggested next module:** Testing & Quality — unit/integration tests for controllers, validation, problem details payloads, and multi-version contracts.
