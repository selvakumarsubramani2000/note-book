# Module 6 — API Design, Validation & Error Handling

> Design **REST-compliant** ASP.NET Core Web APIs with clean contracts, solid input validation, consistent Problem Details errors, and intentional versioning.

**Outcome:** Build APIs that clients can trust — correct verbs/status codes, validated inputs, global error handling without secret leakage, and non-breaking evolution via API versions.

---

## 📚 Contents

| # | File | What you learn |
|---|------|----------------|
| 01 | [01-restful-api-design.md](./01-restful-api-design.md) | Resource URLs, HTTP verbs, **safe vs idempotent**, status codes (`200/201/204/400/401/403/404/409/500`) |
| 02 | [02-validation.md](./02-validation.md) | DataAnnotations, custom attributes, validation problems, **FluentValidation** |
| 03 | [03-error-handling.md](./03-error-handling.md) | Global handlers/middleware, **RFC 7807 Problem Details**, safe logging, 404/400/409 |
| 04 | [04-api-versioning.md](./04-api-versioning.md) | Why version, URL vs header strategies, **Asp.Versioning** setup, deprecation |

---

## 🗺️ Learning path

```
01 Design the contract (routes, verbs, codes)
        │
        ▼
02 Validate input at the boundary
        │
        ▼
03 Standardize failures (Problem Details + logs)
        │
        ▼
04 Version when contracts must break
```

### Suggested hands-on build
1. RESTful `ProductsController` with full CRUD status mapping  
2. `CreateProductRequest` with DataAnnotations (+ one custom attribute)  
3. Global exception handler returning `application/problem+json`  
4. `NotFoundException` / `ConflictException` from services  
5. Side-by-side `/api/v1/products` and `/api/v2/products` DTO shapes  

---

## 🔗 Depends on

| Module | Why |
|--------|-----|
| [Module 3 — Web API](../Module-3-AspNetCore-Web-API-Fundamentals/) | Controllers, DTOs, middleware, DI |
| [Module 5 — Auth](../Module-5-Authentication-And-Authorization/) | 401/403 semantics on protected routes |

---

## ✅ Module completion checklist

- [ ] Design collection/item URLs without verbs in paths  
- [ ] Choose GET/POST/PUT/PATCH/DELETE intentionally  
- [ ] Explain safe vs idempotent with examples  
- [ ] Return correct success and error status codes  
- [ ] Validate requests (annotations and/or FluentValidation)  
- [ ] Emit structured validation errors  
- [ ] Handle exceptions globally as Problem Details  
- [ ] Log errors with trace ids — no passwords/tokens in logs  
- [ ] Map not found / conflict scenarios correctly  
- [ ] Configure at least one API versioning strategy  

---

## ⏭️ Next

**Suggested:** Testing & Quality — integration tests for status codes, validation payloads, problem details, and versioned endpoints.
