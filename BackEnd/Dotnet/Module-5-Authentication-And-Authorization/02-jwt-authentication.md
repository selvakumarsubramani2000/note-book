# 🎫 JWT Authentication — Issue and Validate Bearer Tokens

> **Trainer's Note:** JWT is the workhorse of modern Web API authentication. You will configure bearer auth once, issue tokens on login, and validate them automatically on protected endpoints. Read the token anatomy carefully — debugging “401 loops” becomes much easier.

---

## 📑 Table of Contents
1. [What Is a JWT?](#1-what-is-a-jwt)
2. [JWT Anatomy: Header, Payload, Signature](#2-jwt-anatomy-header-payload-signature)
3. [Claims You Will Use](#3-claims-you-will-use)
4. [Packages and Configuration](#4-packages-and-configuration)
5. [Register JWT Bearer Authentication](#5-register-jwt-bearer-authentication)
6. [Middleware Order Reminder](#6-middleware-order-reminder)
7. [Implementing a Login Endpoint](#7-implementing-a-login-endpoint)
8. [Issuing a Signed Token in C#](#8-issuing-a-signed-token-in-c)
9. [Client Usage: Authorization Bearer Header](#9-client-usage-authorization-bearer-header)
10. [Testing and Common Failures](#10-testing-and-common-failures)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. What Is a JWT?

**JWT** = **J**SON **W**eb **T**oken.

A compact, URL-safe string that carries **claims** about a user, **signed** so your API can trust it wasn’t forged.

```
Login success
   → API builds claims (sub, email, role…)
   → signs them with a secret/private key
   → returns token string to client
Later requests
   → client sends token
   → API validates signature + lifetime (+ issuer/audience)
   → HttpContext.User becomes authenticated
```

### Why APIs use JWT
| Benefit | Meaning |
|---------|---------|
| Stateless validation | No session lookup required for basic trust |
| Portable | SPA, mobile, other services can send same header |
| Self-contained claims | Roles/user id travel with the request |
| Standard ecosystem | Libraries + middleware everywhere |

JWT is not magic security. It is a **signed message format**. You still need HTTPS, short lifetimes, and solid authorization.

---

## 2. JWT Anatomy: Header, Payload, Signature

A JWT has **three Base64Url parts** separated by dots:

```
xxxxx.yyyyy.zzzzz
│     │     │
│     │     └─ Signature
│     └─ Payload (claims)
└─ Header
```

### Header (algorithm + type)
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

| Field | Meaning |
|-------|---------|
| `alg` | Signing algorithm (`HS256`, `RS256`, …) |
| `typ` | Usually `JWT` |

### Payload (claims)
```json
{
  "sub": "42",
  "email": "selva@shop.com",
  "role": "Admin",
  "iss": "shop-api",
  "aud": "shop-clients",
  "exp": 1735689600,
  "iat": 1735686000
}
```

Anyone can decode payload. **Do not store passwords or secrets here.**

### Signature
```
HMACSHA256(
  base64Url(header) + "." + base64Url(payload),
  secret-key
)
```
For asymmetric algorithms, private key signs; public key verifies.

### What validation proves
1. Signature matches → not tampered, signed by holder of key  
2. `exp` not passed → not expired  
3. Optional: issuer/audience match your config  

---

## 3. Claims You Will Use

| Claim | Meaning | Example |
|-------|---------|---------|
| `sub` | Subject (user id) | `"42"` |
| `email` | Email | `selva@shop.com` |
| `role` / roles | Authorization roles | `Admin` |
| `iss` | Issuer | `shop-api` |
| `aud` | Audience | `shop-clients` |
| `exp` | Expiration (unix time) | required practically |
| `iat` | Issued at | optional but useful |
| `jti` | Unique token id | revocation strategies |

In .NET you often use `ClaimTypes.NameIdentifier`, `ClaimTypes.Role`, etc., which map to standard claim URIs.

---

## 4. Packages and Configuration

```bash
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
```

(On modern .NET web SDKs, some shared framework pieces exist; the JwtBearer package is still the explicit auth handler package you configure.)

### `appsettings.json` section
```json
{
  "Jwt": {
    "Issuer": "shop-api",
    "Audience": "shop-clients",
    "Key": "DEV_ONLY_CHANGE_ME_TO_A_LONG_RANDOM_SECRET_32+CHARS",
    "ExpireMinutes": 60
  }
}
```

### Options class
```csharp
public class JwtOptions
{
    public const string SectionName = "Jwt";
    public string Issuer { get; set; } = string.Empty;
    public string Audience { get; set; } = string.Empty;
    public string Key { get; set; } = string.Empty;
    public int ExpireMinutes { get; set; } = 60;
}
```

**Production:** put `Jwt:Key` in env vars / vault — never commit real secrets.

```bash
dotnet user-secrets set "Jwt:Key" "a-very-long-random-dev-secret-value"
```

---

## 5. Register JWT Bearer Authentication

```csharp
using System.Text;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;

var builder = WebApplication.CreateBuilder(args);

builder.Services.Configure<JwtOptions>(
    builder.Configuration.GetSection(JwtOptions.SectionName));

var jwt = builder.Configuration.GetSection(JwtOptions.SectionName).Get<JwtOptions>()
          ?? throw new InvalidOperationException("Jwt config missing");

builder.Services
    .AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidIssuer = jwt.Issuer,

            ValidateAudience = true,
            ValidAudience = jwt.Audience,

            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(jwt.Key)),

            ValidateLifetime = true,
            ClockSkew = TimeSpan.FromMinutes(1) // small tolerance
        };
    });

builder.Services.AddAuthorization();
builder.Services.AddControllers();

var app = builder.Build();

app.UseAuthentication(); // who are you?
app.UseAuthorization();  // are you allowed?
app.MapControllers();
app.Run();
```

### What this enables
- Reads `Authorization: Bearer ...`  
- Validates signature/exp/iss/aud  
- Populates `HttpContext.User` (`ClaimsPrincipal`)  

---

## 6. Middleware Order Reminder

```csharp
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();
```

```
❌ UseAuthorization before UseAuthentication
✅ Authenticate first, authorize second
```

Without `UseAuthentication()`, tokens won’t turn into a user identity.

---

## 7. Implementing a Login Endpoint

### Request/response DTOs
```csharp
public record LoginRequest(string Email, string Password);
public record LoginResponse(string AccessToken, DateTime ExpiresAtUtc);
```

### Controller sketch (demo credential check)
```csharp
[ApiController]
[Route("api/auth")]
public class AuthController : ControllerBase
{
    private readonly ITokenService _tokens;
    private readonly IUserService _users; // validates credentials

    public AuthController(ITokenService tokens, IUserService users)
    {
        _tokens = tokens;
        _users = users;
    }

    [HttpPost("login")]
    [AllowAnonymous]
    public async Task<ActionResult<LoginResponse>> Login(
        LoginRequest request,
        CancellationToken ct)
    {
        var user = await _users.ValidateCredentialsAsync(
            request.Email, request.Password, ct);

        if (user is null)
            return Unauthorized(new { message = "Invalid email or password" });

        var token = _tokens.CreateToken(user);
        return Ok(token);
    }
}
```

### Credential validation rules
1. Look up user by email  
2. Verify password against **hash** (Identity or your hasher)  
3. Reject with same message for unknown user/wrong password (reduce user-enumeration)  
4. Issue JWT only after success  

> Later file uses ASP.NET Core Identity for registration/login hashing. Here, focus on the token issuance path.

---

## 8. Issuing a Signed Token in C#

```csharp
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.Extensions.Options;
using Microsoft.IdentityModel.Tokens;

public interface ITokenService
{
    LoginResponse CreateToken(AppUser user);
}

public class TokenService : ITokenService
{
    private readonly JwtOptions _opt;

    public TokenService(IOptions<JwtOptions> opt) => _opt = opt.Value;

    public LoginResponse CreateToken(AppUser user)
    {
        var claims = new List<Claim>
        {
            new(JwtRegisteredClaimNames.Sub, user.Id.ToString()),
            new(JwtRegisteredClaimNames.Email, user.Email),
            new(ClaimTypes.NameIdentifier, user.Id.ToString()),
            new(ClaimTypes.Name, user.Email)
        };

        foreach (var role in user.Roles)
            claims.Add(new Claim(ClaimTypes.Role, role));

        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_opt.Key));
        var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);
        var expires = DateTime.UtcNow.AddMinutes(_opt.ExpireMinutes);

        var token = new JwtSecurityToken(
            issuer: _opt.Issuer,
            audience: _opt.Audience,
            claims: claims,
            notBefore: DateTime.UtcNow,
            expires: expires,
            signingCredentials: creds);

        var jwt = new JwtSecurityTokenHandler().WriteToken(token);
        return new LoginResponse(jwt, expires);
    }
}
```

Register:
```csharp
builder.Services.AddScoped<ITokenService, TokenService>();
```

### Symmetric vs asymmetric (awareness)
| Mode | Algo example | Key idea |
|------|--------------|----------|
| Symmetric | HS256 | Same secret signs & verifies (simple single API) |
| Asymmetric | RS256 | Private signs, public verifies (gateway/multi-service) |

Start with HS256 + long random secret for learning.

---

## 9. Client Usage: Authorization Bearer Header

After login, client stores access token (memory / secure storage — careful with `localStorage` XSS risks on SPAs).

### Every protected request
```http
GET /api/products HTTP/1.1
Host: localhost:5001
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Accept: application/json
```

### JavaScript fetch sketch
```javascript
const res = await fetch('/api/products', {
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Accept': 'application/json'
  }
});
```

### curl
```bash
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" https://localhost:7xxx/api/products
```

### Swagger UI
Configure bearer scheme so you can Authorize once and test:
```csharp
// conceptual: AddSwaggerGen with Bearer security definition
```
Many templates/docs show adding a security definition named `Bearer` with scheme `bearer` and format `JWT`.

---

## 10. Testing and Common Failures

### Happy path
1. `POST /api/auth/login` with valid credentials → token  
2. Call protected endpoint with header → `200`  
3. Call without header → `401`  

### Common 401 causes
| Cause | Fix |
|-------|-----|
| Missing header | Send `Authorization: Bearer ...` |
| Typo `Bearer` | Exact scheme + space |
| Expired token | Login again / refresh flow |
| Wrong signing key | Same key issue & validate |
| Issuer/audience mismatch | Align token + validation options |
| Auth middleware missing/order wrong | `UseAuthentication` before authz |
| Clock skew extremes | Check server time; adjust `ClockSkew` carefully |

### Debugging tips
- Decode payload at [jwt.io](https://jwt.io) **with dummy data only** — don’t paste production tokens casually  
- Log authentication failures in Development  
- Ensure HTTPS in real environments  

### Minimal protect check
```csharp
[Authorize]
[HttpGet("me")]
public IActionResult Me()
{
    var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);
    var email = User.FindFirstValue(ClaimTypes.Email)
                ?? User.FindFirstValue(ClaimTypes.Name);
    return Ok(new { userId, email, claims = User.Claims.Select(c => new { c.Type, c.Value }) });
}
```

---

## 11. Knowledge Check

**Q1.** What are the three parts of a JWT?  
**Q2.** Is the JWT payload secret by default?  
**Q3.** Which middleware must run before authorization when using bearer tokens?  
**Q4.** What header does the client send after login?  
**Q5.** Name three `TokenValidationParameters` you should usually enable.  
**Q6.** Why reject invalid login with a generic error message?  
**Q7.** Where should the JWT signing key live in production?

### Mini practice
1. Add JwtBearer package and config section  
2. Register authentication + authorization  
3. Implement `ITokenService` and `POST /api/auth/login`  
4. Create `[Authorize] GET /api/auth/me`  
5. Prove 401 without token and 200 with token in Swagger/curl  

### Answers (short)
1. Header, payload, signature  
2. No — Base64-readable; only signed  
3. `UseAuthentication`  
4. `Authorization: Bearer <token>`  
5. Issuer, audience, signing key, lifetime  
6. Reduce account enumeration / info leaks  
7. Secret store / env / vault — not git  

---

## ✅ What You Should Feel Confident About

- [ ] Explain JWT purpose and structure  
- [ ] Configure `AddAuthentication().AddJwtBearer(...)`  
- [ ] Issue a signed token with claims and expiry  
- [ ] Build a login endpoint that validates credentials then issues JWT  
- [ ] Call APIs with `Authorization: Bearer`  
- [ ] Diagnose basic 401 validation failures  

**Previous:** [01-security-basics.md](./01-security-basics.md)  
**Next:** [03-authorization-in-aspnet-core.md](./03-authorization-in-aspnet-core.md) — `[Authorize]`, roles, and policies.
