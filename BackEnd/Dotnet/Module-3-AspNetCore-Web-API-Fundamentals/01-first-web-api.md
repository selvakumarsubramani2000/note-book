# 🚀 Your First Web API — From Template to Running Endpoints

> **Trainer's Note:** This is where backend work becomes real. You create an ASP.NET Core Web API, read `Program.cs`, understand startup, and write your first controllers. Keep a terminal open and run every example.

---

## 📑 Table of Contents
1. [Create a Web API with `dotnet new webapi`](#1-create-a-web-api-with-dotnet-new-webapi)
2. [What the Template Gives You](#2-what-the-template-gives-you)
3. [Program.cs and the Minimal Hosting Model](#3-programcs-and-the-minimal-hosting-model)
4. [Application Startup Process](#4-application-startup-process)
5. [Controller Basics](#5-controller-basics)
6. [ControllerBase and Useful Base Members](#6-controllerbase-and-useful-base-members)
7. [Route and HTTP Verb Attributes](#7-route-and-http-verb-attributes)
8. [Run, Swagger, and Your First Manual Test](#8-run-swagger-and-your-first-manual-test)
9. [Minimal APIs vs Controllers (Awareness)](#9-minimal-apis-vs-controllers-awareness)
10. [Knowledge Check](#10-knowledge-check)

---

## 1. Create a Web API with `dotnet new webapi`

```bash
dotnet new webapi -n Shop.Api -o Shop.Api
cd Shop.Api
dotnet run
```

### Useful template options
| Option | Purpose |
|--------|---------|
| `-n Shop.Api` | Project name |
| `-o Shop.Api` | Output folder |
| `-f net8.0` | Target framework |
| `--use-controllers` | Scaffold controller-based API (SDK-dependent) |

> Template defaults change slightly across SDK versions. Some default to **Minimal APIs**. Controllers are still industry-standard for many teams — this module teaches both startup and **controllers** deeply.

### Trust HTTPS dev certificate (first time)
```bash
dotnet dev-certs https --trust
```

---

## 2. What the Template Gives You

```
Shop.Api/
  ├── Program.cs                 ← host setup + middleware + endpoints
  ├── appsettings.json           ← configuration
  ├── appsettings.Development.json
  ├── Properties/
  │     └── launchSettings.json  ← local URLs & profiles
  ├── Controllers/               ← if controllers template
  │     └── WeatherForecastController.cs   (sample)
  └── Shop.Api.csproj
```

| File | Job |
|------|-----|
| `Program.cs` | Build web host, register services, configure pipeline |
| `appsettings*.json` | Settings (connection strings, feature flags later) |
| `launchSettings.json` | Dev ports, environment (`Development`) |
| Controllers | HTTP endpoint classes |

Delete the weather sample once you understand it — replace with your own resources (`Products`, `Orders`).

---

## 3. Program.cs and the Minimal Hosting Model

Modern ASP.NET Core uses the **minimal hosting model**: one `Program.cs` instead of old `Startup.cs` + `Program.cs` split.

### Anatomy (controller-friendly)
```csharp
var builder = WebApplication.CreateBuilder(args);

// 1) Register services (DI container)
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// 2) Configure HTTP pipeline (middleware)
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();   // discover controller routes

app.Run();              // start listening
```

### Two phases you must never mix up
```
Phase A — Service registration          Phase B — Middleware pipeline
builder.Services.AddX()                 app.UseY() / app.MapZ()
(before Build)                          (after Build)
```

```
CreateBuilder
    → register services
Build
    → configure middleware & routes
Run
    → listen for HTTP
```

| API | When | Purpose |
|-----|------|---------|
| `WebApplication.CreateBuilder(args)` | Start | Load config, logging, DI, default host |
| `builder.Services...` | Before `Build` | Register dependencies |
| `builder.Build()` | Middle | Freeze service provider; create `app` |
| `app.Use...` / `app.Map...` | After `Build` | Pipeline + endpoints |
| `app.Run()` | End | Block and serve requests |

---

## 4. Application Startup Process

### Step-by-step startup story
```
1. Process starts (dotnet run / deployed host)
2. CreateBuilder reads:
     - appsettings.json
     - appsettings.{Environment}.json
     - environment variables
     - command-line args
     - launchSettings (dev)
3. You register services into DI
4. Build() creates the app + service provider
5. You order middleware
6. Map controllers / minimal endpoints
7. Kestrel listens on configured URLs
8. Each HTTP request flows through the pipeline
```

### Where do URLs come from?
| Source | Example |
|--------|---------|
| `launchSettings.json` | `https://localhost:7xxx` |
| CLI | `dotnet run --urls http://localhost:5080` |
| Environment | `ASPNETCORE_URLS` |

### Development vs Production behavior
```csharp
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}
```
Swagger is great in dev. Many teams turn it off (or lock it) in production.

### Host vs your code
```
Kestrel (web server)
   └── ASP.NET Core host
         └── Your middleware + controllers
```
You rarely configure raw sockets. The host does listening; you write endpoints and rules.

---

## 5. Controller Basics

A **controller** is a class that groups related HTTP endpoints for a resource.

### Rules of thumb
1. Inherit from `ControllerBase` (API) — not MVC `Controller` (HTML views)
2. Mark class with `[ApiController]`
3. Set a base route with `[Route]`
4. Mark actions with `[HttpGet]`, `[HttpPost]`, etc.

### First real controller
```csharp
using Microsoft.AspNetCore.Mvc;

namespace Shop.Api.Controllers;

[ApiController]
[Route("api/[controller]")]   // → api/products
public class ProductsController : ControllerBase
{
    private static readonly List<ProductDto> Products = new()
    {
        new(1, "Keyboard", 1499m),
        new(2, "Mouse", 699m)
    };

    [HttpGet]
    public ActionResult<IEnumerable<ProductDto>> GetAll()
    {
        return Ok(Products);
    }

    [HttpGet("{id:int}")]
    public ActionResult<ProductDto> GetById(int id)
    {
        var product = Products.FirstOrDefault(p => p.Id == id);
        if (product is null) return NotFound();
        return Ok(product);
    }

    [HttpPost]
    public ActionResult<ProductDto> Create(ProductDto input)
    {
        var created = input with { Id = Products.Max(p => p.Id) + 1 };
        Products.Add(created);
        return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
    }
}

public record ProductDto(int Id, string Name, decimal Price);
```

### `[ApiController]` gives you free superpowers
| Behavior | Meaning |
|----------|---------|
| Attribute routing required | Cleaner REST style |
| Automatic 400 on invalid model state | Bad input → problem details |
| Inference for binding sources | Less repetitive `[FromBody]` in many cases |
| Better error response conventions | Consistent API client experience |

---

## 6. ControllerBase and Useful Base Members

`ControllerBase` is the API-focused base class.

| Member / helper | Use |
|-----------------|-----|
| `Ok(object)` | `200` + body |
| `NotFound()` | `404` |
| `BadRequest(error)` | `400` |
| `CreatedAtAction(...)` | `201` + `Location` header |
| `NoContent()` | `204` |
| `Unauthorized()` | `401` |
| `StatusCode(int, object?)` | Custom code |
| `Request` / `HttpContext` | Low-level request access |
| `User` | Authenticated principal (later module) |

```csharp
return Ok(product);           // 200
return NotFound();            // 404
return BadRequest("Invalid"); // 400
return NoContent();           // 204
```

Prefer these helpers over manually crafting every response — readable and consistent.

---

## 7. Route and HTTP Verb Attributes

### Class-level route
```csharp
[Route("api/[controller]")]  // [controller] token → class name without "Controller"
public class ProductsController : ControllerBase
```
`ProductsController` → `api/products`

### Fixed route
```csharp
[Route("api/catalog/products")]
```

### Verb attributes
| Attribute | HTTP method | Typical use |
|-----------|-------------|-------------|
| `[HttpGet]` | GET | Read |
| `[HttpGet("{id}")]` | GET | Read one |
| `[HttpPost]` | POST | Create |
| `[HttpPut("{id}")]` | PUT | Full replace |
| `[HttpPatch("{id}")]` | PATCH | Partial update |
| `[HttpDelete("{id}")]` | DELETE | Remove |

### Combining routes
```csharp
[ApiController]
[Route("api/products")]
public class ProductsController : ControllerBase
{
    [HttpGet]                     // GET  api/products
    public IActionResult GetAll() => Ok();

    [HttpGet("{id:int}")]         // GET  api/products/5
    public IActionResult Get(int id) => Ok();

    [HttpPost]                    // POST api/products
    public IActionResult Create() => Ok();

    [HttpGet("{id:int}/reviews")] // GET  api/products/5/reviews
    public IActionResult Reviews(int id) => Ok();
}
```

### Route constraints (preview)
```csharp
[HttpGet("{id:int}")]
[HttpGet("{sku:alpha}")]
```
Constraints reject obviously wrong URLs early (`/api/products/abc` won’t bind to `int id`).

---

## 8. Run, Swagger, and Your First Manual Test

```bash
dotnet run
```

Terminal prints listening URLs. In Development, open Swagger UI (often `/swagger`).

### Test without Swagger
```http
GET https://localhost:7xxx/api/products
Accept: application/json
```

Or with curl:
```bash
curl -k https://localhost:7xxx/api/products
```

### Checklist when nothing responds
1. Did `MapControllers()` get called?  
2. Is the controller `public`?  
3. Is `[ApiController]` + route present?  
4. Correct port from `launchSettings`?  
5. Build errors ignored? (`dotnet build`)

---

## 9. Minimal APIs vs Controllers (Awareness)

| Style | Look | Strength |
|-------|------|----------|
| **Minimal APIs** | `app.MapGet(...)` in `Program.cs` or extension files | Small services, fast to start |
| **Controllers** | Classes with attributes | Large APIs, clear grouping, filters ecosystem |

```csharp
// Minimal API style
app.MapGet("/api/health", () => Results.Ok(new { status = "ok" }));
```

This notebook focuses on **controllers** for structure, while you keep Minimal API literacy for reading templates and microservices.

---

## 10. Knowledge Check

**Q1.** Which method starts listening for HTTP traffic — `Build()` or `Run()`?  
**Q2.** What are the two phases around `builder.Build()`?  
**Q3.** Why inherit `ControllerBase` instead of `Controller` for JSON APIs?  
**Q4.** What URL does `[Route("api/[controller]")]` produce for `OrdersController`?  
**Q5.** What does `[ApiController]` automatically do with invalid incoming models?  
**Q6.** Which helper returns `201 Created` with a `Location` header path?

### Mini practice
1. Create `Shop.Api` with `dotnet new webapi`  
2. Add `ProductsController` with in-memory list  
3. Implement `GET /api/products` and `GET /api/products/{id}`  
4. Implement `POST /api/products` returning `CreatedAtAction`  
5. Verify in Swagger  

### Answers (short)
1. `Run()`  
2. Register services → configure pipeline  
3. `ControllerBase` is for APIs without view support baggage  
4. `api/orders`  
5. Returns `400 Bad Request` (model state errors)  
6. `CreatedAtAction(...)`

---

## ✅ What You Should Feel Confident About

- [ ] Scaffold and run a Web API project  
- [ ] Read and explain `Program.cs` hosting flow  
- [ ] Register controllers and map them  
- [ ] Write a controller with `[Route]` + HTTP verb attributes  
- [ ] Return `Ok` / `NotFound` / `CreatedAtAction`  
- [ ] Test endpoints via Swagger or HTTP calls  

**Next:** [02-routing-and-endpoints.md](./02-routing-and-endpoints.md) — routing styles, parameters, and result types in depth.
