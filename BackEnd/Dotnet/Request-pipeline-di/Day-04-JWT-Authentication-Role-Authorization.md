# Day 4 — JWT Authentication & Role-Based Authorization

> **Goal:** Understand how JSON Web Tokens work, how to issue and validate them in ASP.NET Core, and how to protect endpoints with `[Authorize]`, roles, and policies.

**Prerequisites:** [Day 1](./Day-01-Middleware-Pipeline.md), [Day 2](./Day-02-Dependency-Injection.md), [Day 3](./Day-03-Filters-Global-Exception-Handling.md)

---

## 📑 Table of Contents

1. [Authentication vs Authorization](#1-authentication-vs-authorization)
2. [What is a JWT?](#2-what-is-a-jwt)
3. [The JWT Flow](#3-the-jwt-flow)
4. [Setup — NuGet Packages & Configuration](#4-setup--nuget-packages--configuration)
5. [Issuing a Token on Login](#5-issuing-a-token-on-login)
6. [Validating the Token (Middleware)](#6-validating-the-token-middleware)
7. [`[Authorize]` — Protecting Endpoints](#7-authorize--protecting-endpoints)
8. [Role-Based Authorization](#8-role-based-authorization)
9. [Policy-Based Authorization](#9-policy-based-authorization)
10. [Claims Deep-Dive & Custom Requirements](#10-claims-deep-dive--custom-requirements)
11. [Refresh Tokens Pattern](#11-refresh-tokens-pattern)
12. [Common Pitfalls](#12-common-pitfalls)
13. [Key Takeaways & Exercises](#13-key-takeaways--exercises)

---

## 1. Authentication vs Authorization

They are often confused but they are different steps.

| Concept | Question it answers | Example |
|---------|---------------------|---------|
| **Authentication** | "Who are you?" | User sends credentials → server returns token |
| **Authorization** | "Are you allowed to do this?" | Token says role = Admin → can call `DELETE /vendors/1` |

Authentication comes **first**; authorization comes **after**.

```
Request → [Authentication middleware] → [Authorization middleware] → Endpoint
              ↓ fails = 401                 ↓ fails = 403
```

- **401 Unauthorized** → "I don't know who you are" (missing/invalid token)
- **403 Forbidden** → "I know who you are, but you can't do this" (wrong role/policy)

---

## 2. What is a JWT?

A **JSON Web Token** is a compact, URL-safe string with **three** parts separated by dots:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9  .  eyJzdWIiOiIxIiwibmFtZSI6IkFkbWluIn0  .  4p9sT...signature
     ── HEADER (base64url) ──            ── PAYLOAD (base64url) ──                ── SIGNATURE ──
```

### Header (algorithm info)
```json
{ "alg": "HS256", "typ": "JWT" }
```

### Payload (claims)
```json
{
  "sub":  "42",
  "name": "selva",
  "role": "Admin",
  "exp":  1735689600,
  "iss":  "VendorDirectory",
  "aud":  "VendorDirectoryClients"
}
```
Standard claims: `sub` (subject/user id), `iss` (issuer), `aud` (audience), `exp` (expiry Unix time), `iat` (issued at), `jti` (token id).

### Signature
`HMACSHA256( base64url(header) + "." + base64url(payload), secret )`

If anyone tampers with the payload, the signature stops matching → token is rejected.

> 🔒 **JWTs are signed, not encrypted by default.** Do NOT put passwords or sensitive PII in the payload — anyone can base64-decode it.

---

## 3. The JWT Flow

```
┌─────────┐                    ┌─────────┐                    ┌──────┐
│ Client  │                    │  API    │                    │  DB  │
└────┬────┘                    └────┬────┘                    └──┬───┘
     │  POST /login { u, p }       │                            │
     ├────────────────────────────►│  verify password           │
     │                             ├───────────────────────────►│
     │                             │◄───────────────────────────┤
     │   200 { token: "eyJ..." }   │  sign JWT with secret      │
     │◄────────────────────────────┤                            │
     │                             │                            │
     │  GET /vendors               │                            │
     │  Authorization: Bearer eyJ..│                            │
     ├────────────────────────────►│  validate signature,       │
     │                             │  expiry, issuer, audience  │
     │                             │  → fill HttpContext.User   │
     │   200 [...vendors]          │                            │
     │◄────────────────────────────┤                            │
```

Tokens are **stateless** — the server does not store them. Everything needed to identify the user is inside the token itself.

---

## 4. Setup — NuGet Packages & Configuration

### Install the bearer package
```bash
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
```

### `appsettings.json`
```json
{
  "Jwt": {
    "Issuer":   "VendorDirectory",
    "Audience": "VendorDirectoryClients",
    "Key":      "super-secret-key-at-least-32-characters-long!!",
    "ExpiryMinutes": 60
  }
}
```
> ⚠️ In production, store the key in **user-secrets** or a secrets manager — never commit it.

---

### Strongly-typed options class
```csharp
public class JwtOptions
{
    public string Issuer   { get; set; } = default!;
    public string Audience { get; set; } = default!;
    public string Key      { get; set; } = default!;
    public int    ExpiryMinutes { get; set; } = 60;
}
```

### Register in `Program.cs`
```csharp
var jwt = builder.Configuration.GetSection("Jwt").Get<JwtOptions>()!;
builder.Services.AddSingleton(jwt);

builder.Services
    .AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer           = true,
            ValidateAudience         = true,
            ValidateLifetime         = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer      = jwt.Issuer,
            ValidAudience    = jwt.Audience,
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwt.Key)),
            ClockSkew        = TimeSpan.Zero     // default is 5 minutes
        };
    });

builder.Services.AddAuthorization();
```

### Wire the middleware (order matters!)
```csharp
app.UseRouting();
app.UseAuthentication();    // 👈 must be BEFORE UseAuthorization
app.UseAuthorization();
app.MapControllers();
```

---

## 5. Issuing a Token on Login

A dedicated `ITokenService` keeps things clean and testable.

```csharp
public interface ITokenService
{
    string CreateToken(User user);
}

public class TokenService(JwtOptions jwt) : ITokenService
{
    public string CreateToken(User user)
    {
        var claims = new List<Claim>
        {
            new(JwtRegisteredClaimNames.Sub,  user.Id.ToString()),
            new(JwtRegisteredClaimNames.Email, user.Email),
            new(JwtRegisteredClaimNames.Jti,   Guid.NewGuid().ToString()),
            new(ClaimTypes.Name, user.Username)
        };

        // Add role claims (one per role)
        claims.AddRange(user.Roles.Select(r => new Claim(ClaimTypes.Role, r)));

        var key   = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwt.Key));
        var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

        var token = new JwtSecurityToken(
            issuer:   jwt.Issuer,
            audience: jwt.Audience,
            claims:   claims,
            expires:  DateTime.UtcNow.AddMinutes(jwt.ExpiryMinutes),
            signingCredentials: creds);

        return new JwtSecurityTokenHandler().WriteToken(token);
    }
}
```

Register it:
```csharp
builder.Services.AddScoped<ITokenService, TokenService>();
```

### Auth controller
```csharp
[ApiController]
[Route("api/[controller]")]
public class AuthController(IUserService users, ITokenService tokens) : ControllerBase
{
    [HttpPost("login")]
    public async Task<IActionResult> Login([FromBody] LoginDto dto)
    {
        var user = await users.ValidateAsync(dto.Username, dto.Password);
        if (user is null) return Unauthorized(new { error = "Invalid credentials" });

        return Ok(new
        {
            token   = tokens.CreateToken(user),
            expires = DateTime.UtcNow.AddMinutes(60)
        });
    }
}

public record LoginDto(string Username, string Password);
```

### Example response
```json
{
  "token":   "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MiIsInJvbGUiOiJBZG1pbiIsImV4cCI6MTczNTY4OTYwMH0.xxxxxxxx",
  "expires": "2025-01-01T12:00:00Z"
}
```

### Client usage
```http
GET /api/vendors
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 6. Validating the Token (Middleware)

The `AddJwtBearer` handler automatically:
1. Reads the `Authorization: Bearer <token>` header
2. Parses the JWT
3. Verifies the signature using your `IssuerSigningKey`
4. Checks `iss`, `aud`, `exp`, `nbf`
5. On success → populates `HttpContext.User` with a `ClaimsPrincipal`

You never have to parse the token manually in a controller. Just read claims:
```csharp
var userId = User.FindFirstValue(JwtRegisteredClaimNames.Sub);
var email  = User.FindFirstValue(ClaimTypes.Email);
var isAdmin = User.IsInRole("Admin");
```

---

## 7. `[Authorize]` — Protecting Endpoints

### Basic — "any authenticated user"
```csharp
[Authorize]
[ApiController]
[Route("api/[controller]")]
public class VendorsController : ControllerBase
{
    [HttpGet]
    public IActionResult List() => Ok(/* ... */);
}
```

### Allow anonymous access to specific actions
```csharp
[Authorize]
public class VendorsController : ControllerBase
{
    [AllowAnonymous]
    [HttpGet("public")]
    public IActionResult Public() => Ok("No auth required");

    [HttpGet]
    public IActionResult List() => Ok(/* auth required */);
}
```

### Global auth (every endpoint unless `[AllowAnonymous]`)
```csharp
builder.Services.AddAuthorization(options =>
{
    options.FallbackPolicy = new AuthorizationPolicyBuilder()
        .RequireAuthenticatedUser()
        .Build();
});
```

---

## 8. Role-Based Authorization

Roles are the simplest authorization model. Include them as claims in the JWT (section 5 already does this).

### Single role
```csharp
[Authorize(Roles = "Admin")]
[HttpDelete("{id}")]
public IActionResult Delete(int id) { ... }
```

### Any of multiple roles (OR)
```csharp
[Authorize(Roles = "Admin,Manager")]
[HttpPost]
public IActionResult Create(VendorDto dto) { ... }
```

### All of multiple roles (AND) — stack the attribute
```csharp
[Authorize(Roles = "Admin")]
[Authorize(Roles = "Finance")]
public IActionResult PayoutReport() { ... }
```

### Reading roles in code
```csharp
if (User.IsInRole("Admin"))
    // do admin thing
```

### Token payload example
```json
{
  "sub":  "42",
  "name": "selva",
  "role": ["Admin", "Manager"],
  "exp":  1735689600
}
```

---

## 9. Policy-Based Authorization

Policies are more flexible than roles. A policy is a **named** set of requirements.

### Register policies
```csharp
builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("AdminOnly",        p => p.RequireRole("Admin"));
    options.AddPolicy("ManagerOrAdmin",   p => p.RequireRole("Admin", "Manager"));
    options.AddPolicy("CanDeleteVendor",  p => p.RequireRole("Admin").RequireClaim("Permission", "vendor:delete"));
    options.AddPolicy("Over18",           p => p.RequireAssertion(ctx =>
        int.TryParse(ctx.User.FindFirst("age")?.Value, out var a) && a >= 18));
});
```

### Use them
```csharp
[Authorize(Policy = "AdminOnly")]
public IActionResult AdminStuff() { ... }

[Authorize(Policy = "CanDeleteVendor")]
[HttpDelete("{id}")]
public IActionResult Delete(int id) { ... }
```

### Policies vs Roles — when to use which
| Use | Scenario |
|-----|----------|
| `Roles = "Admin"` | Simple "is this user in role X?" check |
| Policy + `RequireRole` | Centralized role names, reusable |
| Policy + `RequireClaim` | Fine-grained permissions per-action |
| Policy + `RequireAssertion` | Dynamic logic (age, subscription tier, IP range) |

---
## 10. Claims Deep-Dive & Custom Requirements

A **claim** is a key-value pair about the user. The JWT payload becomes a `ClaimsPrincipal` on the server.

### Add custom claims at login
```csharp
var claims = new List<Claim>
{
    new(JwtRegisteredClaimNames.Sub, user.Id.ToString()),
    new(ClaimTypes.Name, user.Username),
    new("tenantId", user.TenantId.ToString()),           // custom
    new("Permission", "vendor:read"),
    new("Permission", "vendor:write"),                   // multiple values OK
    new("subscription", user.Plan.ToString())
};
```

### Read claims in an action
```csharp
public IActionResult Me()
{
    var tenantId     = User.FindFirstValue("tenantId");
    var permissions  = User.FindAll("Permission").Select(c => c.Value);
    var subscription = User.FindFirstValue("subscription");

    return Ok(new { tenantId, permissions, subscription });
}
```

### Custom authorization requirement
When policies aren't expressive enough, write your own requirement + handler.

```csharp
// 1) Requirement (marker class carrying parameters)
public class MinimumRatingRequirement(int min) : IAuthorizationRequirement
{
    public int MinRating { get; } = min;
}

// 2) Handler (actual logic)
public class MinimumRatingHandler
    : AuthorizationHandler<MinimumRatingRequirement>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        MinimumRatingRequirement requirement)
    {
        var rating = context.User.FindFirstValue("rating");
        if (int.TryParse(rating, out var r) && r >= requirement.MinRating)
            context.Succeed(requirement);

        return Task.CompletedTask;
    }
}

// 3) Register
builder.Services.AddSingleton<IAuthorizationHandler, MinimumRatingHandler>();
builder.Services.AddAuthorization(opts =>
{
    opts.AddPolicy("TrustedVendor",
        p => p.Requirements.Add(new MinimumRatingRequirement(4)));
});

// 4) Use
[Authorize(Policy = "TrustedVendor")]
public IActionResult PremiumAction() { ... }
```

---

## 11. Refresh Tokens Pattern

JWTs should be **short-lived** (15–60 min). For better UX, issue a long-lived **refresh token** alongside the JWT.

```
POST /login   →  access (15m) + refresh (7d)
                 │
                 ├─ access expires → call /refresh
                 │
POST /refresh  →  new access (15m) + new refresh (7d)
```

### Minimal setup
```csharp
public record TokenPair(string AccessToken, string RefreshToken, DateTime Expires);

public class RefreshToken
{
    public string Token      { get; set; } = default!;
    public int    UserId     { get; set; }
    public DateTime ExpiresAt{ get; set; }
    public bool   Revoked    { get; set; }
}
```

```csharp
[HttpPost("refresh")]
public async Task<IActionResult> Refresh([FromBody] string refreshToken)
{
    var stored = await _store.FindAsync(refreshToken);
    if (stored is null || stored.Revoked || stored.ExpiresAt < DateTime.UtcNow)
        return Unauthorized();

    var user = await _users.GetAsync(stored.UserId);
    await _store.RevokeAsync(stored);                 // one-time use

    var pair = _tokens.CreatePair(user);              // new access + new refresh
    await _store.SaveAsync(pair.RefreshToken, user.Id);
    return Ok(pair);
}
```

Key rules:
- Refresh tokens are **stored server-side** (DB/Redis) — they are revocable.
- **Rotate** them on each use (invalidate the old one when issuing a new one).
- Store only **hashes** of refresh tokens, not raw values.

---

## 12. Common Pitfalls

### ⚠️ Middleware order wrong
`app.UseAuthorization()` before `app.UseAuthentication()` → `HttpContext.User` is empty. Always auth first.

### ⚠️ `ClockSkew` default is 5 minutes
Tokens appear valid 5 minutes past their `exp`. Set `ClockSkew = TimeSpan.Zero` if you want strict expiry.

### ⚠️ Weak signing key
Use at least **32 characters** for HS256. Use `RSA` (`RS256`) for production across multiple services.

### ⚠️ Sensitive data in payload
JWT payload is base64-encoded, **not encrypted**. Don't put passwords, SSNs, etc. there.

### ⚠️ No token expiry
Always set `exp`. Never issue non-expiring JWTs.

### ⚠️ Accepting tokens over HTTP
Always require HTTPS in production — `app.UseHttpsRedirection()`.

### ⚠️ Forgetting `[AllowAnonymous]` on `/login`
If you use a global `FallbackPolicy`, your login endpoint itself needs `[AllowAnonymous]`.

---

## 13. Key Takeaways & Exercises

### 🎯 Summary Table
| Concept | Remember |
|---------|----------|
| **Authentication** | Who are you? → 401 if missing/invalid token |
| **Authorization** | Are you allowed? → 403 if role/policy fails |
| **JWT parts** | header.payload.signature (base64url) |
| **Signed not encrypted** | Never put secrets in the payload |
| **Middleware order** | `UseAuthentication` before `UseAuthorization` |
| **`[Authorize]`** | Requires any authenticated user |
| **`Roles = "A,B"`** | OR — user needs ANY of the listed roles |
| **Stacked `[Authorize]`** | AND — user needs ALL |
| **Policies** | Named, reusable, can combine claims + custom logic |
| **Custom requirement** | `IAuthorizationRequirement` + `AuthorizationHandler<T>` |
| **Refresh tokens** | Short access (15m) + long refresh (7d), server-stored, rotated |

### Exercises

**Exercise 1 — Implement Login**
Create `ITokenService`, `AuthController.Login`, and issue a JWT for the hard-coded user `selva / pass123` with role `Admin`. Test with Postman — decode the token at [jwt.io](https://jwt.io) and confirm claims.

<details>
<summary>💡 Verification</summary>

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{ "username": "selva", "password": "pass123" }'
```

Copy the `token` from the response, paste into jwt.io, verify `sub`, `role`, `exp`.
</details>

**Exercise 2 — Protect Vendors Endpoints**
- `GET /api/vendors` → any authenticated user
- `POST /api/vendors` → `Admin` OR `Manager`
- `DELETE /api/vendors/{id}` → `Admin` only

Verify each by calling with and without a valid token / correct role — confirm 401, 403, 200 appropriately.

**Exercise 3 — Custom Policy**
Create a `TenantPolicy` that reads a `tenantId` claim and only allows access when the route's `{tenantId}` matches. Use `RequireAssertion` with `context.Resource`.

<details>
<summary>💡 Hint</summary>

```csharp
opts.AddPolicy("SameTenant", p => p.RequireAssertion(ctx =>
{
    if (ctx.Resource is HttpContext http)
    {
        var routeTenant = http.Request.RouteValues["tenantId"]?.ToString();
        var userTenant  = ctx.User.FindFirstValue("tenantId");
        return routeTenant == userTenant;
    }
    return false;
}));
```
</details>

**Exercise 4 — Minimum Rating Requirement**
Implement the `MinimumRatingRequirement` from section 10. Register a `TrustedVendor` policy requiring rating ≥ 4. Create a test endpoint and verify it returns 403 for lower-rated users.

**Exercise 5 — Refresh Token Flow**
Issue access (5 min) + refresh (1 day). Wait 5 minutes → hit an authorized endpoint → observe 401 → call `/refresh` → receive a new pair → retry the original call successfully.

**Exercise 6 — Global Fallback Policy**
Set a global `FallbackPolicy` requiring authentication. Make sure `/api/auth/login` still works by adding `[AllowAnonymous]`.

---

## ➡️ Next: [Day 5 — Logging (Serilog & Structured Logging)](./Day-05-Logging-Serilog.md)

Tomorrow you'll learn:
- `ILogger<T>` basics & log levels
- **Structured logging** with message templates vs string interpolation
- Adding Serilog (console + file + enrichers)
- Log scopes for request correlation
- Writing to seq / ElasticSearch sinks




