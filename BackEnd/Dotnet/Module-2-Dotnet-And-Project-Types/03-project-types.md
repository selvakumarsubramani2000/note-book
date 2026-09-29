# 📦 Project Types — Console, Class Libraries, Web API, `.csproj` & NuGet

> **Trainer's Note:** Backend systems are rarely one giant file. You combine **project types**: a Web API host, class libraries for rules/data, maybe a console tool for jobs. This file shows what each type is for, how `.csproj` works, and how NuGet packages plug in.

---

## 📑 Table of Contents
1. [Why Different Project Types Exist](#1-why-different-project-types-exist)
2. [Console Applications](#2-console-applications)
3. [Class Libraries](#3-class-libraries)
4. [ASP.NET Core Web API](#4-aspnet-core-web-api)
5. [Comparing the Three (Quick Table)](#5-comparing-the-three-quick-table)
6. [Understanding the `.csproj` File](#6-understanding-the-csproj-file)
7. [Project References vs Package References](#7-project-references-vs-package-references)
8. [NuGet Packages — Finding, Adding, Updating](#8-nuget-packages--finding-adding-updating)
9. [A Realistic Beginner Solution Layout](#9-a-realistic-beginner-solution-layout)
10. [Build Outputs and What Gets Published](#10-build-outputs-and-what-gets-published)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. Why Different Project Types Exist

Different project types change:
- **how the app starts**
- **what SDK/web stack is included**
- **whether it produces an executable host or only a reusable DLL**

```
┌──────────────────────────────┐
│  Shop.Api  (Web API project) │  ← entry point: listens for HTTP
│    references ↓              │
│  Shop.Application (classlib) │  ← business use-cases
│    references ↓              │
│  Shop.Domain (classlib)      │  ← entities / core rules
└──────────────────────────────┘

Optional:
  Shop.Worker (console)        ← background job / one-off tool
  Shop.Tests  (test project)   ← automated tests
```

**Rule:** Put HTTP concerns at the edge (API project). Put business logic in libraries.

---

## 2. Console Applications

A **console app** runs from the terminal, writes text in/out, then exits (or loops until stopped).

### Create
```bash
dotnet new console -n HelloWorker -o src/HelloWorker
cd src/HelloWorker
dotnet run
```

### Default shape (modern .NET)
`Program.cs` often uses **top-level statements**:
```csharp
Console.WriteLine("Hello from console!");
```

Or classic style:
```csharp
namespace HelloWorker;

public class Program
{
    public static void Main(string[] args)
    {
        Console.WriteLine("Hello from console!");
    }
}
```

### When console apps help backend developers
| Use | Example |
|-----|---------|
| Learning C# | Practice OOP without HTTP noise |
| One-off tools | Import CSV, re-hash passwords, migrate data |
| Background workers | Long-running loop / queued jobs host |
| Smoke checks | Call an API and print results |

### Mental model
```
OS starts process → Main runs → your code → process ends
```
No HTTP pipeline unless you host one yourself.

---

## 3. Class Libraries

A **class library** compiles to a **DLL** other projects reference. It has **no startup entry point** of its own.

### Create
```bash
dotnet new classlib -n Shop.Domain -o src/Shop.Domain
```

### Typical contents
```csharp
namespace Shop.Domain;

public class Product
{
    public Guid Id { get; private set; } = Guid.NewGuid();
    public string Name { get; private set; }
    public decimal Price { get; private set; }

    public Product(string name, decimal price)
    {
        if (string.IsNullOrWhiteSpace(name))
            throw new ArgumentException("Name is required");
        if (price < 0)
            throw new ArgumentOutOfRangeException(nameof(price));

        Name = name;
        Price = price;
    }
}
```

### Why separate business logic into libraries?
1. **Reuse** — same domain used by API, worker, tests  
2. **Clarity** — domain does not depend on HTTP details  
3. **Testability** — test pure logic without spinning a web server  
4. **Team scale** — boundaries between layers  

### Good vs bad dependency direction
```
Good:
  Web API  →  Application  →  Domain
  (outer layers depend inward)

Bad:
  Domain → Web API     ❌ domain should not know HTTP/controllers
```

### Add a project reference
```bash
dotnet add src/Shop.Api/Shop.Api.csproj reference src/Shop.Domain/Shop.Domain.csproj
```

Now API code can do:
```csharp
using Shop.Domain;
var product = new Product("Keyboard", 1499m);
```

---

## 4. ASP.NET Core Web API

This is the **main project type** for our backend journey.

A **Web API** project:
- hosts an HTTP server (Kestrel)
- maps routes/endpoints
- receives requests and returns responses (usually JSON)
- is the process clients call over the network

### Create
```bash
dotnet new webapi -n Shop.Api -o src/Shop.Api
cd src/Shop.Api
dotnet run
```

Then open the URL printed in the terminal (often includes **Swagger** UI in Development).

### What you get (conceptual)
```
Shop.Api
  ├── Program.cs              ← builds host, middleware, services, endpoints
  ├── appsettings.json        ← configuration
  ├── appsettings.Development.json
  ├── Controllers/ or Minimal endpoint mappings
  └── Shop.Api.csproj
```

### Minimal endpoint sketch
```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/api/health", () => Results.Ok(new { status = "healthy" }));

app.Run();
```

### Controller-style sketch
```csharp
using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    [HttpGet]
    public IActionResult GetAll()
    {
        return Ok(new[] { new { id = 1, name = "Keyboard" } });
    }
}
```

### Why Web API is “the host”
```
Internet / intranet clients
        │
        ▼
   Shop.Api process   ← only this listens on a port
        │ uses
        ▼
   Class libraries    ← no ports; pure code
```

Libraries do not magically become websites. The **Web API project** is what you deploy as the HTTP service (or combined with a generic host for workers).

### Common companion packages (later modules)
| Package area | Examples |
|--------------|----------|
| Data access | EF Core providers |
| Logging | Serilog |
| Auth | JWT bearer packages |
| Validation | FluentValidation (optional) |
| Mapping | AutoMapper / Mapperly (optional) |

---

## 5. Comparing the Three (Quick Table)

| | Console | Class Library | ASP.NET Core Web API |
|--|---------|---------------|----------------------|
| Template | `console` | `classlib` | `webapi` |
| Entry point | `Main` / top-level | None | `Program` host + `Run` |
| Output role | Runnable tool/app | Reusable DLL | Runnable HTTP server |
| Speaks HTTP by default? | No | No | Yes |
| Typical backend use | Jobs / utilities | Domain & application logic | Public/private API surface |
| Deployed alone? | Sometimes | No (consumed by hosts) | Yes (main service) |

---

## 6. Understanding the `.csproj` File

The **`.csproj`** file is the project’s recipe card: target framework, packages, references, and build settings.

### Example — Web API style project
```xml
<Project Sdk="Microsoft.NET.Sdk.Web">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Swashbuckle.AspNetCore" Version="6.6.2" />
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\Shop.Domain\Shop.Domain.csproj" />
  </ItemGroup>

</Project>
```

### Example — Class library
```xml
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

</Project>
```

### Key pieces explained
| Element | Meaning |
|---------|---------|
| `Sdk="Microsoft.NET.Sdk"` | Standard .NET project SDK (libraries, console) |
| `Sdk="Microsoft.NET.Sdk.Web"` | Web SDK — adds ASP.NET Core defaults |
| `TargetFramework` | Which .NET version this project compiles for (`net8.0`) |
| `Nullable` | Enables C# nullable reference type checks |
| `ImplicitUsings` | Auto-global usings for common namespaces |
| `PackageReference` | NuGet dependency |
| `ProjectReference` | Dependency on another project in the solution |

### SDK difference that matters
```
Microsoft.NET.Sdk        → console / classlib baseline
Microsoft.NET.Sdk.Web    → web/API baseline (hosting, MVC/minimal bits)
```
If you accidentally create business logic in a Web SDK project, you can still code — but libraries stay cleaner with `Microsoft.NET.Sdk`.

### Multi-target (awareness)
Some libraries use more than one TFM:
```xml
<TargetFrameworks>net8.0;net9.0</TargetFrameworks>
```
Beginners: stick to one TFM, usually the same LTS as your API.

---

## 7. Project References vs Package References

| Kind | XML tag | Means |
|------|---------|-------|
| **Project reference** | `ProjectReference` | Use **your** other project’s code |
| **Package reference** | `PackageReference` | Use a **NuGet** package from the gallery/feed |

```
Shop.Api
  ├── ProjectReference → Shop.Application
  ├── ProjectReference → Shop.Infrastructure
  └── PackageReference → Serilog.AspNetCore  (NuGet)
```

### CLI equivalents
```bash
# project → project
dotnet add src/Shop.Api reference src/Shop.Domain/Shop.Domain.csproj

# project → NuGet package
dotnet add src/Shop.Api package Serilog.AspNetCore
```

### When to choose which
| Need | Choose |
|------|--------|
| Your team’s domain entities | Project reference |
| Open-source logger, ORM, JSON helper | Package reference |
| Shared code only used in this company | Project reference (or private NuGet later) |

---

## 8. NuGet Packages — Finding, Adding, Updating

**NuGet** is the package manager for .NET (like npm for JavaScript, pip for Python).

### Mental model
```
nuget.org (or private feed)
        │  restore/download
        ▼
 local cache + project obj/bin wiring
        │
        ▼
 your code calls package APIs
```

### Common commands
```bash
dotnet add package Newtonsoft.Json
dotnet add package Microsoft.EntityFrameworkCore.SqlServer --version 8.0.0

dotnet remove package Newtonsoft.Json

dotnet list package
dotnet list package --outdated

dotnet restore
```

### Where package references live
Inside `.csproj`:
```xml
<PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" Version="8.0.0" />
```

Prefer CLI or IDE UI over hand-editing versions when starting out — tooling resolves compatible sets better.

### Version tips for beginners
1. Prefer stable versions (not random `-preview` unless learning previews)  
2. Align major packages with your TFM (EF Core 8 with `net8.0`)  
3. Commit `.csproj` changes; restores are reproducible from them  
4. Avoid adding packages “just in case” — each dependency is maintenance  

### Trust & safety habits
- Prefer well-known packages (Microsoft, established libraries)  
- Check downloads, license, and repo activity on NuGet  
- Companies often use **private feeds** + vulnerability scanning  

---

## 9. A Realistic Beginner Solution Layout

Start simple. Grow structure when pain appears — not before.

### Phase A — one project (first week)
```
Demo.Api/     webapi only
```
Perfect for learning HTTP, routing, and C# in context.

### Phase B — two-three projects (first real app)
```
Shop.sln
  src/
    Shop.Api/            Microsoft.NET.Sdk.Web
    Shop.Domain/         Microsoft.NET.Sdk
    Shop.Application/    Microsoft.NET.Sdk
  tests/
    Shop.Tests/          xUnit/NUnit/MSTest
```

### Create Phase B with CLI
```bash
dotnet new sln -n Shop
dotnet new webapi -n Shop.Api -o src/Shop.Api
dotnet new classlib -n Shop.Domain -o src/Shop.Domain
dotnet new classlib -n Shop.Application -o src/Shop.Application
dotnet new xunit -n Shop.Tests -o tests/Shop.Tests

dotnet sln add src/Shop.Api src/Shop.Domain src/Shop.Application tests/Shop.Tests

dotnet add src/Shop.Application reference src/Shop.Domain
dotnet add src/Shop.Api reference src/Shop.Application
dotnet add src/Shop.Api reference src/Shop.Domain
dotnet add tests/Shop.Tests reference src/Shop.Application
```

### Responsibility cheat-sheet
| Project | Put here | Avoid here |
|---------|----------|------------|
| **Domain** | Entities, core rules | EF Core, HTTP, email vendors |
| **Application** | Use-cases/services interfaces | UI HTML |
| **Api** | Controllers/endpoints, auth wiring, DI setup | Deep business formulas if they belong in domain/app |
| **Tests** | Unit/integration tests | Production-only code |

> Later modules add Infrastructure (EF, email, files). Do not over-split on day one.

---

## 10. Build Outputs and What Gets Published

### After `dotnet build`
```
bin/Debug/net8.0/
  YourProject.dll
  dependencies…
```

| Project kind | Main artifact role |
|--------------|--------------------|
| Class library | `Shop.Domain.dll` referenced by others |
| Console | runnable app + dll |
| Web API | runnable web app + dll |

### After `dotnet publish`
```bash
dotnet publish src/Shop.Api -c Release -o artifacts/api
```
Produces a folder you can deploy (framework-dependent or self-contained depending on flags).

### Beginner deployment picture
```
dotnet publish Api
      │
      ▼
 artifacts/api/   → copy to server or build into Docker image
      │
      ▼
 ASP.NET Core listens on configured ports
```

You almost never deploy a domain class library by itself. You deploy the **host** (API/worker) which includes the libraries it needs.

---

## 11. Knowledge Check

**Q1.** Which project type has no `Main` entry point and cannot run alone?  
**Q2.** Which project type is the primary HTTP entry point for our backend path?  
**Q3.** Why move business rules out of the API project into a class library?  
**Q4.** What does `TargetFramework` net8.0 mean in a `.csproj`?  
**Q5.** Difference between `ProjectReference` and `PackageReference`?  
**Q6.** Which project SDK is typical for Web API: `Microsoft.NET.Sdk` or `Microsoft.NET.Sdk.Web`?  
**Q7.** Name two valid uses of a console app in a backend team.  
**Q8.** What command adds EF Core SQL Server package to a project?

### Mini practice
1. Create solution `Module2.Demo`  
2. Add `Module2.Demo.Api` (webapi), `Module2.Demo.Domain` (classlib), `Module2.Demo.Cli` (console)  
3. Put a `Customer` class in Domain  
4. Reference Domain from Api and Cli  
5. From Cli, create a `Customer` and print it  
6. From Api, return a sample customer as JSON on `GET /api/customers/sample`  
7. Inspect both `.csproj` files and identify SDK + references  

### Answers (short)
1. Class library  
2. ASP.NET Core Web API  
3. Reuse, clearer boundaries, easier testing, less HTTP coupling  
4. Project targets .NET 8  
5. Project = your code; Package = NuGet dependency  
6. `Microsoft.NET.Sdk.Web`  
7. Data migration tool, background worker, learning harness, smoke tester…  
8. `dotnet add package Microsoft.EntityFrameworkCore.SqlServer`

---

## ✅ What You Should Feel Confident About

- [ ] Create console, classlib, and webapi projects from CLI  
- [ ] Explain when to use each type  
- [ ] Read a basic `.csproj` (TFM, SDK, references)  
- [ ] Add project references and NuGet packages  
- [ ] Sketch a small multi-project solution for an API  
- [ ] Know that you deploy the host, not domain DLLs alone  

**Previous:** [02-tools-and-environment.md](./02-tools-and-environment.md)

---

## 🚀 Module 2 Wrap-Up

You can now answer:
1. **What platform am I on?** — modern .NET, CLR, cross-platform  
2. **What tools do I use?** — SDK, IDE/editor, `dotnet` CLI, solutions/templates  
3. **What projects do I create?** — Web API host + class libraries (+ console/tests as needed)

**Suggested next module:** ASP.NET Core Web API fundamentals — `Program.cs`, middleware pipeline, routing, controllers/minimal APIs, configuration, and your first real endpoints.
