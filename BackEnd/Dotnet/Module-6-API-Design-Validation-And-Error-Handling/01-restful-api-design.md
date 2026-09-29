# 🧭 RESTful API Design — Clear Resources, Verbs & Status Codes

> **Trainer's Note:** A great backend is not only working code — it is a **predictable contract**. REST gives clients (SPA, mobile, other APIs) a shared language: nouns for resources, HTTP verbs for actions, and status codes for outcomes. Design URLs and responses like a public product.

---

## 📑 Table of Contents
1. [What “RESTful” Means in Practice](#1-what-restful-means-in-practice)
2. [Resources and URL Design](#2-resources-and-url-design)
3. [Collections vs Items](#3-collections-vs-items)
4. [HTTP Verbs Done Right](#4-http-verbs-done-right)
5. [Safe vs Idempotent Methods](#5-safe-vs-idempotent-methods)
6. [HTTP Status Codes You Must Master](#6-http-status-codes-you-must-master)
7. [Request/Response Body Guidelines](#7-requestresponse-body-guidelines)
8. [Filtering, Sorting, Pagination](#8-filtering-sorting-pagination)
9. [Common REST Anti-Patterns](#9-common-rest-anti-patterns)
10. [End-to-End Resource Example](#10-end-to-end-resource-example)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. What “RESTful” Means in Practice

REST is an **architectural style**, not a library. For Web APIs it usually means:

| Principle | Practical habit |
|-----------|-----------------|
| Resource-oriented | URLs name **things** (`/products`), not actions (`/getProducts`) |
| Uniform interface | Same verbs/status meanings everywhere |
| Stateless | Each request carries what the server needs (e.g. JWT) |
| Representations | JSON is the common representation |
| Correct status codes | Clients branch on `201` vs `400` vs `404`, not only message text |

```
Client thinks in resources:

  Products collection   → /api/products
  One product           → /api/products/42
  Product reviews       → /api/products/42/reviews
```

---

## 2. Resources and URL Design

### Good patterns
```
/api/products
/api/products/{id}
/api/users/{id}
/api/users/{id}/orders
/api/orders/{orderId}/items/{itemId}
```

### Rules of thumb
1. Use **nouns**, plural collections (`products`, `orders`)  
2. Use path params for **identity** (`{id}`)  
3. Keep nesting **shallow** (2 levels is usually enough)  
4. Prefer kebab-case or lowercase consistent segments (`/api/order-items` if needed)  
5. Avoid file extensions (`.json`) in modern APIs  
6. Versioning is separate (see file 04) — e.g. `/api/v1/products`  

### Naming table
| Avoid | Prefer |
|-------|--------|
| `/api/getUser?id=5` | `GET /api/users/5` |
| `/api/createProduct` | `POST /api/products` |
| `/api/product` (mixed) | stick to plural `/api/products` |
| `/api/products/delete/5` | `DELETE /api/products/5` |
| `/api/products/5/updatePrice` (when PATCH works) | `PATCH /api/products/5` |

### Actions that aren’t plain CRUD
Sometimes a real business action doesn’t fit cleanly:

```
POST /api/orders/15/cancel
POST /api/payments/88/refund
```

Use sparingly for genuine **operations**. Don’t turn every verb into a custom path.

---

## 3. Collections vs Items

| Kind | Example | Typical methods |
|------|---------|-----------------|
| **Collection** | `/api/products` | GET list, POST create |
| **Item** | `/api/products/{id}` | GET one, PUT/PATCH update, DELETE |

```
GET    /api/products          → 200 + array/page
POST   /api/products          → 201 + created item
GET    /api/products/10       → 200 + item  | 404
PUT    /api/products/10       → 200/204     | 404
PATCH  /api/products/10       → 200/204     | 404
DELETE /api/products/10       → 204         | 404
```

---

## 4. HTTP Verbs Done Right

| Verb | Intent | Body common? | Example |
|------|--------|--------------|---------|
| **GET** | Read | Usually no | `GET /api/products/5` |
| **POST** | Create / non-idempotent action | Yes | `POST /api/products` |
| **PUT** | Replace **entire** resource | Yes | `PUT /api/products/5` |
| **PATCH** | Partial update | Yes | `PATCH /api/products/5` |
| **DELETE** | Remove | Optional | `DELETE /api/products/5` |

### PUT vs PATCH
```
PUT   → client sends full product representation; missing fields may reset defaults
PATCH → client sends only fields to change: { "price": 999 }
```

### Controller sketch
```csharp
[ApiController]
[Route("api/products")]
public class ProductsController : ControllerBase
{
    [HttpGet]
    public ActionResult<IEnumerable<ProductDto>> GetAll() => Ok(/* ... */);

    [HttpGet("{id:int}")]
    public ActionResult<ProductDto> GetById(int id) => /* Ok or NotFound */;

    [HttpPost]
    public ActionResult<ProductDto> Create(CreateProductRequest request)
        => CreatedAtAction(nameof(GetById), new { id = created.Id }, created);

    [HttpPut("{id:int}")]
    public IActionResult Replace(int id, UpdateProductRequest request) => NoContent();

    [HttpPatch("{id:int}")]
    public IActionResult Patch(int id, PatchProductRequest request) => NoContent();

    [HttpDelete("{id:int}")]
    public IActionResult Delete(int id) => NoContent();
}
```

---

## 5. Safe vs Idempotent Methods

These words show up in reviews and interviews — learn them once.

### Safe
**Safe** = should not change server state.

| Method | Safe? |
|--------|-------|
| GET | Yes |
| POST | No |
| PUT/PATCH/DELETE | No |

Crawlers/proxies may retry GETs. **Never** delete or charge cards via GET.

### Idempotent
**Idempotent** = calling 1 time or N times leaves the **same final state**.

| Method | Idempotent? | Why |
|--------|-------------|-----|
| GET | Yes | Read-only |
| PUT | Yes | Replace with same body → same resource |
| DELETE | Yes | Delete once or five times → resource gone |
| PATCH | Usually designed to be | Depends on patch semantics |
| POST | **No** (usually) | Each call may create another row |

```
POST /api/orders   × 3  → maybe 3 orders   (not idempotent)
DELETE /api/orders/9 × 3 → still deleted   (idempotent)
PUT /api/products/1 with same JSON × 3 → same end state
```

Design important POSTs with **idempotency keys** when payment/order creation can’t tolerate duplicates (advanced pattern).

---

## 6. HTTP Status Codes You Must Master

### Success family
| Code | Name | When |
|------|------|------|
| **200 OK** | Success with body | GET/PUT/PATCH success returning data |
| **201 Created** | Resource created | POST create; include `Location` when possible |
| **204 No Content** | Success, empty body | DELETE or update with no response body |

### Client error family
| Code | Name | When |
|------|------|------|
| **400 Bad Request** | Invalid input | Validation failed, malformed JSON |
| **401 Unauthorized** | Not authenticated | Missing/invalid token |
| **403 Forbidden** | Not allowed | Authenticated but no permission |
| **404 Not Found** | Missing resource | Unknown id / unknown route |
| **409 Conflict** | State conflict | Duplicate email, concurrency conflict |
| **422 Unprocessable** | Semantic validation | Sometimes used instead of 400 (team choice) |

### Server error family
| Code | Name | When |
|------|------|------|
| **500 Internal Server Error** | Unexpected failure | Unhandled exception |
| **503 Service Unavailable** | Temporary outage | Dependency down, maintenance |

### Decision tree
```
Did auth fail?
  missing/bad identity → 401
  identity ok but denied → 403

Is input invalid?
  → 400 (or validation problem details)

Does resource exist?
  no → 404

Business conflict (duplicate, version mismatch)?
  → 409

Created new resource?
  → 201

Success with no body?
  → 204

Success with body?
  → 200

Unexpected boom?
  → 500 (log details server-side; safe message client-side)
```

### Anti-pattern
```
❌ always return 200 with { success: false, error: "..." }
✅ use proper status codes + problem details body
```

---

## 7. Request/Response Body Guidelines

| Verb | Request body | Response body |
|------|--------------|---------------|
| GET collection | No | List/page DTO |
| GET item | No | Item DTO |
| POST | Create DTO | Created resource (+ `Location`) |
| PUT | Full update DTO | Updated resource or empty |
| PATCH | Partial DTO | Updated resource or empty |
| DELETE | Rarely | Empty (`204`) |

### `CreatedAtAction` example
```csharp
return CreatedAtAction(
    nameof(GetById),
    new { id = product.Id },
    productDto);
// Status 201
// Location: /api/products/42
```

### Consistency tips
- Same property casing everywhere (`camelCase` JSON is ASP.NET default)  
- Don’t return EF entities — return DTOs (Module 3)  
- Errors use one envelope (Problem Details — file 03)  

---

## 8. Filtering, Sorting, Pagination

Keep identity in the **path**; use **query string** for modifiers.

```
GET /api/products?search=board&categoryId=3&sort=price&page=2&pageSize=20
```

| Concern | Place |
|---------|-------|
| Resource id | Route `/products/{id}` |
| Filters | Query `categoryId`, `search` |
| Sort | Query `sort`, `dir` |
| Page | Query `page`, `pageSize` |

### Response shape idea
```json
{
  "items": [ ... ],
  "page": 2,
  "pageSize": 20,
  "totalCount": 135
}
```

---

## 9. Common REST Anti-Patterns

| Anti-pattern | Why it hurts | Fix |
|--------------|--------------|-----|
| Verbs in URLs | Breaks uniform interface | HTTP methods |
| One giant `/api/do` endpoint | Undocumentable | Resource routes |
| Ignoring status codes | Clients can’t automate | Map outcomes to codes |
| Returning 200 for errors | Hides failures from monitors | 4xx/5xx |
| Deep nesting | `/a/b/c/d/e/f` unusable | Flatten or limit depth |
| Leaking DB rows | Coupling + security risk | DTOs |
| Breaking URLs casually | Client breakages | Versioning (file 04) |

---

## 10. End-to-End Resource Example

**Resource:** Product  

| Operation | Design |
|-----------|--------|
| List | `GET /api/products` → `200` |
| Get | `GET /api/products/{id}` → `200`/`404` |
| Create | `POST /api/products` → `201` + `Location` |
| Replace | `PUT /api/products/{id}` → `204`/`404` |
| Partial | `PATCH /api/products/{id}` → `204`/`404` |
| Delete | `DELETE /api/products/{id}` → `204`/`404` |
| Admin only delete | same URL + authZ policy/role |

Nested:
```
GET  /api/products/{id}/reviews
POST /api/products/{id}/reviews
```

---

## 11. Knowledge Check

**Q1.** Why prefer `/api/products/5` over `/api/getProduct?id=5`?  
**Q2.** Is `GET` safe? Is `POST` idempotent?  
**Q3.** When do you return `201` instead of `200`?  
**Q4.** `401` vs `403`?  
**Q5.** PUT vs PATCH in one sentence each.  
**Q6.** Why is returning `200` for every failure a bad idea?  
**Q7.** Where should `page` and `search` go — path or query?

### Mini practice
Design the full REST surface for **Orders**:
- list/filter mine  
- get by id  
- create  
- cancel (action)  
- admin refund  

For each: method, path, success code, failure codes.

### Answers (short)
1. Resource nouns + proper verb; cacheable/standard clients  
2. GET safe yes; POST usually not idempotent  
3. When a new resource was created  
4. 401 unauthenticated; 403 authenticated but forbidden  
5. PUT full replace; PATCH partial update  
6. Breaks HTTP semantics, monitoring, client branching  
7. Query string  

---

## ✅ What You Should Feel Confident About

- [ ] Design collection and item URLs  
- [ ] Map CRUD (+ a few actions) to HTTP verbs  
- [ ] Explain safe vs idempotent  
- [ ] Choose correct success and error status codes  
- [ ] Use query params for filter/sort/page  
- [ ] Spot REST anti-patterns in code reviews  

**Next:** [02-validation.md](./02-validation.md) — DataAnnotations, custom validators, Problem Details for validation, FluentValidation.
