# 🔌 Integration & Functional Testing — Real Pipeline, Test Data, Auth Flows

> **Trainer's Note:** Unit tests prove pieces. **Integration / functional tests** prove the ASP.NET Core host works together: routing, binding, validation, filters, auth, DI, and often EF persistence. Use `WebApplicationFactory` for an in-process test server — no manual “start the API” step.

---

## 📑 Table of Contents
1. [Unit vs Integration vs Functional (API View)](#1-unit-vs-integration-vs-functional-api-view)
2. [WebApplicationFactory and the Test Server](#2-webapplicationfactory-and-the-test-server)
3. [Create an API Test Project](#3-create-an-api-test-project)
4. [First Endpoint Tests](#4-first-endpoint-tests)
5. [Customize the Host for Tests](#5-customize-the-host-for-tests)
6. [EF Core InMemory Provider](#6-ef-core-inmemory-provider)
7. [SQLite In-Memory Alternative](#7-sqlite-in-memory-alternative)
8. [Testing Validation and Problem Details](#8-testing-validation-and-problem-details)
9. [Testing Authentication & Authorization](#9-testing-authentication--authorization)
10. [Stability Practices](#10-stability-practices)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. Unit vs Integration vs Functional (API View)

| Kind | Scope | Example |
|------|-------|---------|
| **Unit** | One class, mocked deps | `ProductService` + mock repo |
| **Integration** | Several real parts | EF mapping + repository against InMemory DB |
| **Functional** (API) | Full HTTP pipeline in-process | `HttpClient` → controllers → services → DB |

```
Functional/API test:

  HttpClient
      → TestServer (your Program pipeline)
          → auth middleware
          → controller
          → service
          → EF / fakes you registered
```

People use “integration test” for API tests too — that’s fine. The important part is **real pipeline**, not browser E2E.

---

## 2. WebApplicationFactory and the Test Server

Package: `Microsoft.AspNetCore.Mvc.Testing`

```csharp
public class ShopApiFactory : WebApplicationFactory<Program>
{
}
```

Top-level statements hide `Program`. Expose it:

```csharp
// at the bottom of the API Program.cs
public partial class Program { }
```

### Share factory across tests in a class
```csharp
public class ProductsEndpointTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public ProductsEndpointTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.CreateClient();
    }
}
```

`CreateClient()` talks to an in-memory test server hosting your app.

---

## 3. Create an API Test Project

```bash
dotnet new xunit -n Shop.Api.Tests -o tests/Shop.Api.Tests
dotnet add tests/Shop.Api.Tests reference src/Shop.Api/Shop.Api.csproj
dotnet add tests/Shop.Api.Tests package Microsoft.AspNetCore.Mvc.Testing
dotnet test tests/Shop.Api.Tests
```

Optional helpers:
```bash
dotnet add tests/Shop.Api.Tests package FluentAssertions
dotnet add tests/Shop.Api.Tests package Microsoft.EntityFrameworkCore.InMemory
# and/or SQLite:
dotnet add tests/Shop.Api.Tests package Microsoft.EntityFrameworkCore.Sqlite
```

Install only with your approval/policy.

---

## 4. First Endpoint Tests

```csharp
public class CatalogTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public CatalogTests(WebApplicationFactory<Program> factory)
        => _client = factory.CreateClient();

    [Fact]
    public async Task GetProducts_ReturnsOk()
    {
        var response = await _client.GetAsync("/api/products");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var json = await response.Content.ReadAsStringAsync();
        Assert.False(string.IsNullOrWhiteSpace(json));
    }
}
```

### Create with JSON body
```csharp
[Fact]
public async Task CreateProduct_ValidBody_ReturnsCreated()
{
    var content = JsonContent.Create(new
    {
        name = "Keyboard",
        price = 1499m,
        categoryId = 1
    });

    var response = await _client.PostAsync("/api/products", content);

    Assert.Equal(HttpStatusCode.Created, response.StatusCode);
    Assert.NotNull(response.Headers.Location);
}
```

You are testing the API **contract**: status codes, headers, payload shape.

---

## 5. Customize the Host for Tests

Override environment, config, and services:

```csharp
public class ShopApiFactory : WebApplicationFactory<Program>
{
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.UseEnvironment("Development");

        builder.ConfigureAppConfiguration((_, config) =>
        {
            config.AddInMemoryCollection(new Dictionary<string, string?>
            {
                ["Jwt:Key"] = "TEST_ONLY_KEY_MUST_BE_LONG_ENOUGH_123456",
                ["Jwt:Issuer"] = "shop-tests",
                ["Jwt:Audience"] = "shop-tests",
                ["Jwt:ExpireMinutes"] = "60"
            });
        });

        builder.ConfigureServices(services =>
        {
            // swap infrastructure here (DB, email, clock, ...)
        });
    }
}
```

Use `IClassFixture<ShopApiFactory>` instead of the raw factory when you need these overrides.

---

## 6. EF Core InMemory Provider

**InMemory** is a lightweight EF provider — great for quick API tests, **not** a full SQL Server emulator.

### Replace DbContext registration
```csharp
protected override void ConfigureWebHost(IWebHostBuilder builder)
{
    builder.ConfigureServices(services =>
    {
        RemoveDbContext<AppDbContext>(services);

        services.AddDbContext<AppDbContext>(opt =>
            opt.UseInMemoryDatabase($"ShopTests-{Guid.NewGuid()}"));

        var sp = services.BuildServiceProvider();
        using var scope = sp.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        db.Database.EnsureCreated();
        // optional seed...
    });
}

private static void RemoveDbContext<TContext>(IServiceCollection services)
    where TContext : DbContext
{
    var descriptors = services
        .Where(d =>
            d.ServiceType == typeof(DbContextOptions<TContext>) ||
            d.ServiceType == typeof(TContext))
        .ToList();

    foreach (var d in descriptors)
        services.Remove(d);
}
```

### Round-trip test idea
```csharp
[Fact]
public async Task CreateThenGet_ReturnsPersistedProduct()
{
    var create = await _client.PostAsync("/api/products",
        JsonContent.Create(new { name = "Mouse", price = 499m, categoryId = 1 }));
    create.EnsureSuccessStatusCode();

    var list = await _client.GetAsync("/api/products");
    var body = await list.Content.ReadAsStringAsync();
    Assert.Contains("Mouse", body);
}
```

### InMemory limitations (know these)
| Real SQL often has | InMemory may not fully mimic |
|--------------------|------------------------------|
| Unique indexes / constraints | Partial or different behavior |
| Transactions / raw SQL | Limited |
| Provider-specific types | Differences |

For critical persistence rules, prefer SQLite in-memory, Testcontainers, or a real test database.

---

## 7. SQLite In-Memory Alternative

Closer to relational behavior than EF InMemory for many cases.

```csharp
var connection = new SqliteConnection("DataSource=:memory:");
connection.Open(); // keep open for lifetime of DB

services.AddDbContext<AppDbContext>(opt =>
    opt.UseSqlite(connection));

// EnsureCreated / Migrate on the open connection
```

Hold the connection for the factory lifetime (field on custom factory) so the in-memory DB is not disposed early.

```
API tests
  └── SQLite :memory: connection (kept open)
        └── EF Core model + migrations/ensure created
```

Still not 100% identical to SQL Server/PostgreSQL — but excellent for many integration suites without Docker.

---

## 8. Testing Validation and Problem Details

```csharp
[Fact]
public async Task CreateProduct_InvalidBody_Returns400()
{
    var content = new StringContent(
        """{"name":"","price":-5}""",
        Encoding.UTF8,
        "application/json");

    var response = await _client.PostAsync("/api/products", content);

    Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);

    var payload = await response.Content.ReadAsStringAsync();
    Assert.Contains("errors", payload, StringComparison.OrdinalIgnoreCase);
}
```

Also assert **404**, **409**, **401**, **403** as part of the functional contract (ties to Modules 5–6).

---

## 9. Testing Authentication & Authorization

### A) Anonymous vs authenticated outcomes
```csharp
[Fact]
public async Task DeleteProduct_Anonymous_Returns401()
{
    var response = await _client.DeleteAsync("/api/products/1");
    Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
}
```

### B) Test authentication handler (fast & common)
```csharp
public class TestAuthHandler : AuthenticationHandler<AuthenticationSchemeOptions>
{
    public const string SchemeName = "Test";

    public TestAuthHandler(
        IOptionsMonitor<AuthenticationSchemeOptions> options,
        ILoggerFactory logger,
        UrlEncoder encoder)
        : base(options, logger, encoder) { }

    protected override Task<AuthenticateResult> HandleAuthenticateAsync()
    {
        if (!Request.Headers.ContainsKey("X-Test-User"))
            return Task.FromResult(AuthenticateResult.NoResult());

        var role = Request.Headers["X-Test-Role"].FirstOrDefault() ?? "Customer";
        var claims = new List<Claim>
        {
            new(ClaimTypes.NameIdentifier, "user-1"),
            new(ClaimTypes.Name, "tester"),
            new(ClaimTypes.Role, role)
        };
        var identity = new ClaimsIdentity(claims, SchemeName);
        var ticket = new AuthenticationTicket(new ClaimsPrincipal(identity), SchemeName);
        return Task.FromResult(AuthenticateResult.Success(ticket));
    }
}
```

Register in factory (alongside or replacing JWT defaults carefully):

```csharp
services.AddAuthentication(options =>
{
    options.DefaultAuthenticateScheme = TestAuthHandler.SchemeName;
    options.DefaultChallengeScheme = TestAuthHandler.SchemeName;
})
.AddScheme<AuthenticationSchemeOptions, TestAuthHandler>(
    TestAuthHandler.SchemeName, _ => { });

services.AddAuthorization();
```

### Authenticated client calls
```csharp
_client.DefaultRequestHeaders.Add("X-Test-User", "yes");
_client.DefaultRequestHeaders.Add("X-Test-Role", "Admin");

var response = await _client.DeleteAsync("/api/products/1");
Assert.True(response.StatusCode is HttpStatusCode.NoContent or HttpStatusCode.NotFound);
```

### C) Real JWT in tests
Configure the same test signing key as the factory config; issue a token in the test arrange phase; send `Authorization: Bearer ...`. Closest to production AuthN.

### Authorization matrix to cover
| Call | Expected |
|------|----------|
| No credentials on `[Authorize]` | 401 |
| User role on Admin-only | 403 |
| Admin role on Admin-only | 2xx |
| Owner can read own order; other user cannot | 200 vs 404/403 |

```
Test matrix:

  [AllowAnonymous] GET /api/products          → 200
  [Authorize] POST /api/orders (no token)     → 401
  [Authorize(Roles="Admin")] DELETE (user)    → 403
  [Authorize(Roles="Admin")] DELETE (admin)   → 204/404
```

---

## 10. Stability Practices

| Practice | Why |
|----------|-----|
| Unique InMemory database names | Avoid cross-test contamination |
| Seed explicitly | Deterministic data |
| Independent tests | Parallel-safe |
| Don’t `Thread.Sleep` for sync | Flaky |
| Replace email/payment with fakes | No external network |
| Disable / raise rate limits in test env | Avoid random 429 |
| Assert status codes + small payload checks | Stable contracts |
| `IClassFixture` for expensive host | Speed |

### Parallelization note
xUnit parallelizes across classes. If tests share one DB name, use a collection fixture with `DisableParallelization = true`, or give each factory a unique DB.

### What a solid API suite includes
1. Public happy path GET  
2. Validation 400  
3. Create + read persistence path  
4. 401 anonymous  
5. 403 forbidden role  
6. Allowed role success  
7. Not found path  

---

## 11. Knowledge Check

**Q1.** What does `WebApplicationFactory<Program>` provide?  
**Q2.** Why add `public partial class Program { }`?  
**Q3.** Name one strength and one limitation of EF InMemory.  
**Q4.** Why keep a SQLite in-memory connection open?  
**Q5.** How can you simulate an Admin user without full JWT infrastructure?  
**Q6.** What status do you expect for invalid POST bodies with `[ApiController]`?  
**Q7.** Unit test vs functional API test for “missing bearer token returns 401”?

### Mini practice
1. Create `Shop.Api.Tests` with `Microsoft.AspNetCore.Mvc.Testing`  
2. Write GET returns 200 test  
3. Write invalid POST returns 400 test  
4. Custom factory + EF InMemory with unique DB name  
5. Create-then-get product integration path  
6. Add `TestAuthHandler` and cover 401 / 403 / Admin success  

### Answers (short)
1. In-process test host + `HttpClient` against your app pipeline  
2. Expose entry point type for the factory generic parameter  
3. Strength: fast/easy; limitation: not full relational/SQL fidelity  
4. Closing it destroys the in-memory database  
5. Custom test authentication handler + headers/claims  
6. 400  
7. Functional/integration via HTTP pipeline — not a pure service unit test  

---

## ✅ What You Should Feel Confident About

- [ ] Spin up API tests with `WebApplicationFactory`  
- [ ] Assert endpoint status codes and basic payloads  
- [ ] Swap EF to InMemory or SQLite for test persistence  
- [ ] Seed/isolate test data safely  
- [ ] Test anonymous, authenticated, and role-based flows  
- [ ] Know when a test belongs in unit vs API functional layers  

**Previous:** [02-mocking-and-isolation.md](./02-mocking-and-isolation.md)

---

## 🚀 Module 8 (Testing) Wrap-Up

You can now validate backend behavior automatically:

| Skill | File |
|-------|------|
| Why tests matter; xUnit/NUnit/MSTest; AAA unit tests without SQL | 01 |
| Moq isolation for repositories, DB ports, HTTP exteriors | 02 |
| `WebApplicationFactory`, InMemory/SQLite, authz functional tests | 03 |

### Confidence checklist
- [ ] Unit-test business rules offline  
- [ ] Mock/fake dependencies instead of real SQL/network  
- [ ] Functional-test endpoints through the real ASP.NET pipeline  
- [ ] Cover validation and security status codes  
- [ ] Refactor with a growing green suite  

```
Change code
  → unit tests (fast logic)
  → API tests (pipeline + data + auth)
  → refactor with confidence
```

**Suggested next:** CI pipelines that run `dotnet test` on every PR, Testcontainers for real SQL engines, and end-to-end smoke tests for critical journeys.
