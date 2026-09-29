# 🔒 Security Best Practices — Harden Your ASP.NET Core APIs

> **Trainer's Note:** Security is not one middleware — it’s a set of habits across auth, input, data access, errors, and configuration. This file maps **OWASP-minded risks** to practical .NET defenses you already have (EF Core, Identity, Problem Details, User Secrets) and closes gaps beginners often miss.

---

## 📑 Table of Contents
1. [Security Mindset for APIs](#1-security-mindset-for-apis)
2. [OWASP Top 10 (API-Relevant Overview)](#2-owasp-top-10-api-relevant-overview)
3. [Broken Auth and Access Control](#3-broken-auth-and-access-control)
4. [SQL Injection and EF Core Parameterization](#4-sql-injection-and-ef-core-parameterization)
5. [XSS and APIs](#5-xss-and-apis)
6. [CSRF and Cookie-Based Clients](#6-csrf-and-cookie-based-clients)
7. [Injection Beyond SQL](#7-injection-beyond-sql)
8. [Secure Error Handling](#8-secure-error-handling)
9. [Secrets and Configuration Management](#9-secrets-and-configuration-management)
10. [Transport, Headers, and Hardening Checklist](#10-transport-headers-and-hardening-checklist)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. Security Mindset for APIs

```
Assume:
  - clients are hostile or buggy
  - tokens leak eventually
  - users will hit every endpoint directly
  - logs and errors are attacker-visible if careless
```

| Principle | Practice |
|-----------|----------|
| Least privilege | Roles/policies; DB user permissions |
| Defense in depth | Auth + validation + EF + logging + network |
| Fail safe | Deny by default |
| Secure defaults | HTTPS, short JWT lifetime, validated input |
| Don’t trust client | Re-check authZ server-side |

---

## 2. OWASP Top 10 (API-Relevant Overview)

OWASP lists change over years. Learn the **themes**, not only letter codes.

| Risk theme | API example | Mitigations you know |
|------------|-------------|----------------------|
| Broken access control | IDOR: read `/orders/SomeoneElsesId` | AuthZ + ownership checks |
| Cryptographic failures | Plaintext passwords, HTTP login | Identity hashing, HTTPS, secret stores |
| Injection | SQL/command/LDAP injection | Parameterized EF/SQL, validate input |
| Insecure design | No rate limits, weak flows | Threat model, idempotency, review |
| Security misconfiguration | Swagger public in prod, default secrets | Env-specific config, harden |
| Vulnerable components | Outdated NuGet packages | `dotnet list package --vulnerable` |
| Auth failures | Weak JWT key, no expiry | Module 5 practices |
| Integrity failures | Unsigned software/updates | Supply chain hygiene |
| Logging/monitoring failures | No alerts on auth spikes | Structured logs + monitoring |
| SSRF | API fetches user-provided URLs blindly | Allow-lists, block internal ranges |

> Treat this as a map. Full OWASP docs go deeper — revisit as you grow.

---

## 3. Broken Auth and Access Control

### Classic IDOR (Insecure Direct Object Reference)
```csharp
// ❌ trusts client id alone
[Authorize]
[HttpGet("{id:guid}")]
public async Task<IActionResult> GetOrder(Guid id)
{
    var order = await _db.Orders.FindAsync(id);
    return order is null ? NotFound() : Ok(order);
}
```

```csharp
// ✅ ownership check
[Authorize]
[HttpGet("{id:guid}")]
public async Task<IActionResult> GetOrder(Guid id)
{
    var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);
    var order = await _db.Orders.AsNoTracking()
        .FirstOrDefaultAsync(o => o.Id == id && o.CustomerId == userId);
    return order is null ? NotFound() : Ok(OrderDto.From(order));
}
```

### Habits
- Authenticate globally (fallback policy) where appropriate  
- Authorize sensitive actions with roles/policies  
- Enforce **resource-level** rules in services  
- Prefer `404` over `403` for private resources sometimes (reduce probing) — team decision  
- Short-lived JWTs; rotate signing keys carefully  
- Lockout / rate limit login endpoints  

---

## 4. SQL Injection and EF Core Parameterization

**SQL injection** happens when user input is concatenated into SQL.

```csharp
// ❌ vulnerable pattern
var sql = $"SELECT * FROM Products WHERE Name = '{name}'";
// name = "x'; DROP TABLE Products;--"
```

### EF Core LINQ (parameterized)
```csharp
// ✅ parameters under the hood
var items = await _db.Products
    .Where(p => p.Name == name)
    .ToListAsync();
```

### Raw SQL done safely
```csharp
// ✅ interpolated FormattableString becomes parameters
var items = await _db.Products
    .FromSqlInterpolated($"SELECT * FROM Products WHERE Name = {name}")
    .ToListAsync();

// ❌ FromSqlRaw with string concat
var bad = $"SELECT * FROM Products WHERE Name = '{name}'";
await _db.Products.FromSqlRaw(bad).ToListAsync();
```

| Safe | Unsafe |
|------|--------|
| LINQ to Entities | String-concat SQL |
| `FromSqlInterpolated` | `FromSqlRaw` + user input concat |
| Parameterized ADO.NET commands | Hand-built SQL strings |

EF is not magic if **you** build unsafe SQL strings. Unique constraints and least-privilege DB accounts still matter.

---

## 5. XSS and APIs

**XSS (Cross-Site Scripting)** mostly hurts **browsers** rendering untrusted HTML/JS.

Pure JSON APIs don’t execute HTML, but they can **store** attack payloads that a frontend later renders unsafely.

```
Attacker saves name: <script>steal(document.cookie)</script>
API stores it
Web UI renders with innerHTML → XSS
```

### API responsibilities
| Practice | Why |
|----------|-----|
| Validate/sanitize where appropriate | Reject crazy control characters / HTML if not allowed |
| Don’t return executable HTML content types by default | Keep `application/json` |
| Encode on the client when rendering | Primary XSS fix in UI |
| CSP headers on web apps | Defense in depth |

For APIs serving HTML (Razor), use encoding helpers and avoid raw HTML concatenation.

---

## 6. CSRF and Cookie-Based Clients

**CSRF (Cross-Site Request Forgery)** tricks a browser into sending **cookie credentials** to your site from another site.

```
User logged into bank.com (session cookie)
User visits evil.com
evil.com posts form → bank.com/transfer
Browser attaches bank cookie automatically
```

### JWT Bearer in Authorization header
```
Authorization: Bearer ...
```
Not auto-attached by cross-site forms the same way cookies are → **classic CSRF is less relevant** for pure bearer-token SPAs/mobile.

### Cookie-based auth (MVC/SPA with cookies)
You **must** consider CSRF:
- antiforgery tokens  
- `SameSite` cookie attributes  
- careful CORS  

```csharp
// conceptual cookie auth hardening
options.Cookie.HttpOnly = true;
options.Cookie.SecurePolicy = CookieSecurePolicy.Always;
options.Cookie.SameSite = SameSiteMode.Strict; // or Lax per scenario
```

### CORS
CORS is not CSRF protection by itself, but misconfigured CORS + cookies is dangerous.

```csharp
// be explicit — avoid AllowAnyOrigin with credentials
builder.Services.AddCors(o => o.AddPolicy("Spa", p =>
    p.WithOrigins("https://app.shop.local")
     .AllowAnyHeader()
     .AllowAnyMethod()
     .AllowCredentials()));
```

---

## 7. Injection Beyond SQL

| Type | Example | Defense |
|------|---------|---------|
| OS command injection | `Process.Start("cmd", userInput)` | Never pass raw input to shells |
| Path traversal | `../../etc/passwd` in file names | `Path.GetFileName`, root jail, generated names |
| Header injection | CRLF in logs/headers | sanitize |
| LDAP/NoSQL injection | string-built queries | parameterized APIs / builders |
| SSRF | server fetches attacker URL | allow-list hosts; block link-local/metadata IPs |

File upload rules from the previous file are path-traversal defenses.

---

## 8. Secure Error Handling

From Module 6 — reinforce:

| Do | Don't |
|----|-------|
| Problem Details with safe messages | Return stack traces in production |
| Log exception + traceId server-side | Log tokens/passwords |
| Generic 500 detail for unknowns | Reveal SQL/table names to clients |
| Consistent 401/403/404 | Detailed “user exists” on login if avoiding enumeration |

```csharp
// production client body
{
  "title": "Server error",
  "status": 500,
  "detail": "An unexpected error occurred.",
  "traceId": "00-..."
}
```

Disable detailed Developer Exception Pages for public production traffic.

---

## 9. Secrets and Configuration Management

### Never commit
- JWT signing keys  
- DB passwords  
- API keys (email, payment, storage)  
- Client secrets  
- Private certificates  

### Development: User Secrets
```bash
dotnet user-secrets init
dotnet user-secrets set "ConnectionStrings:ShopDb" "Server=...;Password=...;"
dotnet user-secrets set "Jwt:Key" "super-long-random-dev-key"
```

### Production: environment variables / vault
```bash
ConnectionStrings__ShopDb=...
Jwt__Key=...
```

Or Azure Key Vault / AWS Secrets Manager / HashiCorp Vault via configuration providers.

### appsettings.json
```json
{
  "Jwt": {
    "Issuer": "shop-api",
    "Audience": "shop-clients",
    "ExpireMinutes": 60
  }
}
```
Keep non-secret structure in git; inject secret values at runtime.

### Extra config hygiene
| Habit | Why |
|-------|-----|
| Different secrets per environment | Blast radius |
| Rotate keys/passwords | Assume eventual leak |
| Restrict secret store IAM | Least privilege |
| Scan repos for secrets | Catch accidents early |
| No secrets in Docker images layers carelessly | Images get copied |

---

## 10. Transport, Headers, and Hardening Checklist

### HTTPS everywhere
```csharp
app.UseHttpsRedirection();
// HSTS in production for browsers
if (!app.Environment.IsDevelopment())
    app.UseHsts();
```

### Useful production headers (web-facing)
- `Strict-Transport-Security`  
- `X-Content-Type-Options: nosniff`  
- `Content-Security-Policy` (esp. if serving web content)  
- Remove unnecessary server fingerprint headers when possible  

### Rate limiting (modern .NET)
Protect login and public APIs from brute force/abuse with `Microsoft.AspNetCore.RateLimiting`.

### Dependency hygiene
```bash
dotnet list package --outdated
dotnet list package --vulnerable
```

### Production API checklist
- [ ] HTTPS only; certificates valid  
- [ ] JWT validation complete (iss/aud/lifetime/key)  
- [ ] Passwords hashed via Identity (or equivalent)  
- [ ] `[Authorize]` defaults / fallback policy considered  
- [ ] Resource ownership checks on sensitive GETs/PUTs  
- [ ] EF LINQ/parameterized SQL only  
- [ ] Input validation on all write endpoints  
- [ ] Upload allow-lists + size caps  
- [ ] CORS explicit origins  
- [ ] CSRF strategy if using cookies  
- [ ] Problem Details without stacks  
- [ ] Secrets in vault/env/user-secrets  
- [ ] Swagger locked down or disabled publicly  
- [ ] Logging without PII/secrets + alerting on errors  
- [ ] Packages patched  

```
Secure request path:

  TLS
   → authn (JWT)
   → authz (role/policy/resource)
   → validation
   → parameterized data access
   → safe result or safe problem details
   → structured audit/error logs
```

---

## 11. Knowledge Check

**Q1.** What is IDOR, and how do you prevent it on `GET /orders/{id}`?  
**Q2.** Why is EF LINQ safer than concatenating SQL strings?  
**Q3.** How can a JSON API still be involved in XSS?  
**Q4.** When is CSRF a major concern — bearer header APIs or cookie session web apps?  
**Q5.** Name three secrets that must not live in git.  
**Q6.** What should a production 500 response include and exclude?  
**Q7.** Give two misconfiguration examples that hurt API security.

### Mini practice
1. Add ownership checks to a get-by-id endpoint  
2. Search your code for `FromSqlRaw` / string-built SQL and fix  
3. Move a hard-coded secret to user-secrets  
4. Verify production exception handler does not return stacks  
5. Write a personal “API secure publish” checklist for your project  
6. Run `dotnet list package --vulnerable` if packages exist  

### Answers (short)
1. Accessing another user’s object by id; filter by caller identity/authZ  
2. Values sent as parameters, not executable SQL text  
3. It may store malicious scripts that a web client renders unsafely  
4. Cookie session web apps (auto credentials)  
5. JWT keys, DB passwords, third-party API keys…  
6. Include safe title/status/traceId; exclude stack/secrets  
7. Public Swagger with prod data, default CORS `*`, debug pages online…  

---

## ✅ What You Should Feel Confident About

- [ ] Map OWASP-style risks to API scenarios  
- [ ] Prevent IDOR with ownership/policy checks  
- [ ] Avoid SQL injection with EF parameterization habits  
- [ ] Explain XSS/CSRF relevance for APIs vs cookie web apps  
- [ ] Keep errors and logs safe  
- [ ] Manage secrets with user-secrets/env/vault  
- [ ] Apply a practical production hardening checklist  

**Previous:** [04-file-handling.md](./04-file-handling.md)

---

## 🚀 Module 7 Wrap-Up

You can now push an ASP.NET Core Web API closer to **production-ready**:

| Skill | File |
|-------|------|
| Logging levels, structured logs, Serilog/sinks, PII-safe logging | 01 |
| `IMemoryCache`, Redis distributed cache, invalidation, stale data | 02 |
| `IHostedService` / `BackgroundService`, scopes, Hangfire/Quartz | 03 |
| `IFormFile` uploads, validation, disk/blob storage, streaming | 04 |
| OWASP-minded API hardening, injection, CSRF/XSS, secrets | 05 |

### Production-ready habits checklist
- [ ] Structured logs with levels + correlation ids  
- [ ] No secrets/PII in logs or git  
- [ ] Cache with TTL + invalidate-on-write  
- [ ] Long work in background workers/queues  
- [ ] Uploads validated and stored safely  
- [ ] Downloads streamed with authz  
- [ ] HTTPS, authn/authz, parameterized data access  
- [ ] Safe Problem Details errors  
- [ ] Rate limiting & package hygiene considered  

```
Client
  → secure transport + auth
  → validated API
  → fast reads (cache) + solid writes (DB)
  → async side-effects (jobs)
  → observable via logs/metrics
```

**Suggested next steps:** Testing & quality (integration tests), CI/CD deployment, containers, and observability with OpenTelemetry — the natural next modules after this backend core.
