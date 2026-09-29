# 🌐 Frontend Consumption & CORS — How Browsers Talk to Your API

> **Trainer's Note:** Your ASP.NET Core API rarely lives alone. React, Angular, Vue, or plain JavaScript call it from another origin. Browsers enforce **CORS**. Backend developers must design **stable contracts** and configure CORS deliberately — not with `AllowAnyOrigin` forever.

---

## 📑 Table of Contents
1. [How Frontends Consume APIs](#1-how-frontends-consume-apis)
2. [Typical SPA ↔ API Flow](#2-typical-spa--api-flow)
3. [Fetch and Axios Examples](#3-fetch-and-axios-examples)
4. [Auth Headers from the Browser](#4-auth-headers-from-the-browser)
5. [What CORS Is (Browser Security)](#5-what-cors-is-browser-security)
6. [Simple vs Preflight Requests](#6-simple-vs-preflight-requests)
7. [Configure CORS in ASP.NET Core](#7-configure-cors-in-aspnet-core)
8. [Cookies, Credentials, and Common CORS Traps](#8-cookies-credentials-and-common-cors-traps)
9. [Stable API Contracts for Frontends](#9-stable-api-contracts-for-frontends)
10. [Breaking Changes and Versioning Habits](#10-breaking-changes-and-versioning-habits)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. How Frontends Consume APIs

A browser app is just another **HTTP client**.

```
React/Angular/Vue (localhost:3000)
        │  HTTPS + JSON
        ▼
ASP.NET Core API (localhost:5001)
        │
        ▼
  DB / external services
```

| Frontend responsibility | Backend responsibility |
|-------------------------|------------------------|
| UI state, forms, routing | Validation, authZ, business rules |
| Call endpoints | Stable URLs + status codes |
| Attach tokens | Issue/validate tokens |
| Render errors | Problem Details / consistent errors |

Frontends can be bypassed — **never** trust UI-only checks.

---

## 2. Typical SPA ↔ API Flow

```
1. User opens SPA (static host or dev server)
2. SPA calls POST /api/auth/login
3. API returns JWT (or sets cookie — different model)
4. SPA stores access token (memory / careful storage)
5. SPA calls GET /api/products with Authorization header
6. API returns JSON DTOs
7. SPA renders lists/forms
```

### Same origin vs cross origin
| Scenario | Example | CORS? |
|----------|---------|-------|
| Same origin | UI and API both `https://shop.com` | No extra CORS friction |
| Cross origin | UI `https://app.shop.com`, API `https://api.shop.com` | **Yes** |
| Local dev | UI `http://localhost:3000`, API `https://localhost:5001` | **Yes** |

Most SPA development is cross-origin — CORS configuration is required.

---

## 3. Fetch and Axios Examples

### Browser `fetch`
```javascript
// GET
const res = await fetch('https://localhost:5001/api/products', {
  headers: {
    'Accept': 'application/json'
  }
});
if (!res.ok) throw new Error(`HTTP ${res.status}`);
const products = await res.json();

// POST JSON
const createRes = await fetch('https://localhost:5001/api/products', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${accessToken}`
  },
  body: JSON.stringify({ name: 'Keyboard', price: 1499, categoryId: 1 })
});
```

### Angular `HttpClient` (sketch)
```typescript
this.http.get<Product[]>('/api/products').subscribe(data => this.products = data);
this.http.post<Product>('/api/products', body, {
  headers: { Authorization: `Bearer ${token}` }
}).subscribe();
```

### React with axios (sketch)
```javascript
import axios from 'axios';
const api = axios.create({ baseURL: 'https://localhost:5001' });
api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
const { data } = await api.get('/api/products');
```

Frontends care about: **URL**, **method**, **headers**, **status**, **JSON shape**.

---

## 4. Auth Headers from the Browser

For JWT bearer APIs (Module 5):

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

| Approach | Notes |
|----------|-------|
| Token in memory | Safer vs XSS than `localStorage`; lost on refresh |
| `localStorage` | Common but XSS-sensitive |
| HttpOnly cookie | Needs CSRF strategy; different CORS credential rules |

Backend still validates every request. Frontend only **sends** the credential.

---

## 5. What CORS Is (Browser Security)

**CORS** = **Cross-Origin Resource Sharing**.

Browsers block frontend JavaScript on **origin A** from reading responses from **origin B** unless B explicitly allows it via CORS headers.

### Origin parts
```
https://app.shop.com:443
│       │            │
scheme  host         port
```
Any difference in scheme/host/port → different origin.

### Who enforces CORS?
| Actor | Role |
|-------|------|
| **Browser** | Enforces CORS |
| **API server** | Sends `Access-Control-*` headers |
| **curl / mobile / Postman** | Not browser CORS (still need real auth!) |

```
❌ "CORS error" is not proof your API is broken for all clients
✅ It means the browser refused to expose the response to JS
```

---

## 6. Simple vs Preflight Requests

### “Simple” request (simplified)
Some GET/POST forms may go directly. Browser still checks response ACAO headers for JS access.

### Preflight
For many JSON APIs, browser sends **OPTIONS** first:

```http
OPTIONS /api/products HTTP/1.1
Origin: http://localhost:3000
Access-Control-Request-Method: POST
Access-Control-Request-Headers: content-type,authorization
```

API must respond with permission headers:

```http
HTTP/1.1 204 No Content
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Methods: GET,POST,PUT,DELETE
Access-Control-Allow-Headers: content-type,authorization
```

Then the real POST runs.

```
SPA JS  →  OPTIONS preflight  →  API
SPA JS  →  actual POST        →  API
SPA JS  ←  JSON (if allowed)  ←  API
```

---

## 7. Configure CORS in ASP.NET Core

### Program.cs — named policy
```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddCors(options =>
{
    options.AddPolicy("SpaDev", policy =>
    {
        policy.WithOrigins(
                "http://localhost:3000",
                "http://localhost:4200") // React / Angular defaults
              .AllowAnyHeader()
              .AllowAnyMethod();
        // .AllowCredentials(); // only with specific origins, not *
    });

    options.AddPolicy("ProductionSpa", policy =>
    {
        policy.WithOrigins("https://app.shop.com")
              .WithHeaders("Content-Type", "Authorization")
              .WithMethods("GET", "POST", "PUT", "PATCH", "DELETE");
    });
});

builder.Services.AddControllers();

var app = builder.Build();

app.UseHttpsRedirection();

// order: usually before auth endpoints are hit by browser preflight
app.UseCors("SpaDev"); // pick policy by environment in real apps

app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();
app.Run();
```

### Environment-based selection
```csharp
var corsPolicy = app.Environment.IsDevelopment() ? "SpaDev" : "ProductionSpa";
app.UseCors(corsPolicy);
```

### Middleware order reminder
```
UseRouting (if explicit)
UseCors
UseAuthentication
UseAuthorization
MapControllers
```
Wrong order → confusing preflight failures.

### Avoid this in production
```csharp
policy.AllowAnyOrigin().AllowAnyHeader().AllowAnyMethod();
// convenient for 5 minutes of demos — dangerous as a permanent habit
```

`AllowAnyOrigin()` **cannot** combine with `AllowCredentials()`.

---

## 8. Cookies, Credentials, and Common CORS Traps

### Credentials mode
If frontend sends cookies:

```javascript
fetch(url, { credentials: 'include' })
```

API must:
```csharp
policy.WithOrigins("https://app.shop.com")
      .AllowCredentials();
```
and **not** use `*`.

### Common errors
| Symptom | Likely cause |
|---------|--------------|
| Browser CORS error, Postman works | Missing/incorrect CORS policy |
| Preflight fails | OPTIONS blocked; policy missing headers/methods |
| Works without Authorization, fails with it | `Authorization` not allowed in CORS headers |
| `AllowAnyOrigin` + cookies | Invalid combination |
| Multiple `UseCors` confusion | Wrong policy name / order |

### Debug checklist
1. Exact UI origin (scheme/host/port) listed in `WithOrigins`  
2. `UseCors` before auth where needed  
3. Allow required request headers  
4. HTTPS certificate trust in local SPA→API calls  
5. No accidental double conflicting CORS middleware  

---

## 9. Stable API Contracts for Frontends

A **contract** is what the SPA relies on:

| Contract piece | Example |
|----------------|---------|
| Path + method | `GET /api/products/{id}` |
| Status codes | `200`, `404`, `400` |
| JSON shape | `{ id, name, price }` |
| Headers | `Authorization`, pagination headers |
| Error shape | Problem Details fields |

### DTO stability tips
```csharp
// ✅ additive optional field later
public record ProductDto(int Id, string Name, decimal Price, string? Sku = null);

// ❌ sudden type change breaks UI
// price: number  →  price: { amount, currency }
```

### Naming & shape habits
1. Use consistent `camelCase` JSON (ASP.NET default)  
2. Don’t return EF entities — return DTOs  
3. Document required vs optional fields  
4. Prefer additive changes  
5. Keep error format stable (`application/problem+json`)  
6. Page responses consistently (`items`, `totalCount`, …)  

### Frontend-friendly GET list
```json
{
  "items": [ { "id": 1, "name": "Keyboard", "price": 1499 } ],
  "page": 1,
  "pageSize": 20,
  "totalCount": 135
}
```

---

## 10. Breaking Changes and Versioning Habits

### Often breaking
- Rename/remove JSON fields  
- Change field types  
- Make optional fields required  
- Change auth requirements overnight  
- Change URL paths without notice  

### Often non-breaking
- Add optional response field  
- Add new endpoint  
- Add optional query param with defaults  

```
Ship breaking change:
  v1 keeps old DTO
  v2 introduces new DTO
  SPA migrates
  deprecate v1
```

Coordinate with frontend via OpenAPI (next file), changelog, and Module 6 versioning strategies.

### Contract collaboration
| Practice | Why |
|----------|-----|
| Shared OpenAPI spec | Single source of truth |
| Consumer-driven examples | Fewer surprises |
| Feature flags | Gradual UI rollout |
| Integration tests for public DTOs | Catch accidental breaks |

---

## 11. Knowledge Check

**Q1.** Why does a React app on port 3000 calling API port 5001 need CORS?  
**Q2.** Who enforces CORS — browser or server?  
**Q3.** What is a preflight request?  
**Q4.** Why is `AllowAnyOrigin` + `AllowCredentials` invalid?  
**Q5.** How does an SPA typically send a JWT?  
**Q6.** Name two breaking API changes for frontends.  
**Q7.** Name two additive (safer) changes.

### Mini practice
1. Run API on https://localhost:5xxx and a SPA on localhost:3000  
2. Observe browser CORS error without policy  
3. Add `WithOrigins("http://localhost:3000")` policy + `UseCors`  
4. Call GET then authorized POST with `Authorization` header  
5. Add an optional DTO field; confirm SPA still works  
6. Document one breaking change you’d put in v2 only  

### Answers (short)
1. Different origins (port) → browser cross-origin rules  
2. Browser enforces; server advertises allowance  
3. OPTIONS check before actual cross-origin request  
4. Credentials require explicit origin, not wildcard  
5. `Authorization: Bearer <token>` header  
6. Remove field, change type, rename path…  
7. Add optional field, add endpoint  

---

## ✅ What You Should Feel Confident About

- [ ] Explain how SPAs consume JSON APIs  
- [ ] Describe CORS and preflight in plain words  
- [ ] Configure a named CORS policy in `Program.cs`  
- [ ] Avoid dangerous CORS defaults in production  
- [ ] Design stable DTOs/status contracts for UI consumers  
- [ ] Spot breaking vs additive changes  

**Next:** [02-api-documentation-openapi.md](./02-api-documentation-openapi.md) — Swagger/OpenAPI as the shared contract.
