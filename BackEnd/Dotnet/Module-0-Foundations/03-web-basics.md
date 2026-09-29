# 🌐 Web Basics — HTTP, REST, JSON & APIs

> **Trainer's Note:** Backend developers live on the web stack. Before ASP.NET Core, understand **how browsers and apps talk to servers**. This file is your map of HTTP, REST, JSON, and the difference between websites and APIs.

---

## 📑 Table of Contents
1. [How the Web Works (Big Picture)](#1-how-the-web-works-big-picture)
2. [HTTP Protocol](#2-http-protocol)
3. [Request and Response](#3-request-and-response)
4. [HTTP Methods](#4-http-methods)
5. [Headers](#5-headers)
6. [Body](#6-body)
7. [Status Codes](#7-status-codes)
8. [REST Principles](#8-rest-principles)
9. [JSON Format](#9-json-format)
10. [APIs vs Web Applications](#10-apis-vs-web-applications)
11. [How They Interact in Real Systems](#11-how-they-interact-in-real-systems)
12. [Tiny End-to-End Example](#12-tiny-end-to-end-example)
13. [Knowledge Check](#13-knowledge-check)

---

## 1. How the Web Works (Big Picture)

```
  Client                         Server
  (Browser / Mobile / App)       (Your .NET backend)

     │  1. HTTP Request             │
     │ ───────────────────────────► │
     │                              │  validate, query DB, apply rules
     │  2. HTTP Response            │
     │ ◄─────────────────────────── │
```

| Role | What it does |
|------|----------------|
| **Client** | Starts the conversation (asks for something) |
| **Server** | Listens, processes, replies |
| **HTTP** | The common language of that conversation |
| **URL** | Address of the resource (`https://api.shop.com/orders/5`) |

### URL parts (simple)
```
https://api.shop.com:443/orders/5?status=open
│       │            │    │        │
│       │            │    │        └─ query string (filters)
│       │            │    └─ path (resource)
│       │            └─ port (443 default for https)
│       └─ host (domain / server name)
└─ scheme (https = HTTP + encryption)
```

---

## 2. HTTP Protocol

**HTTP** = **H**yper**T**ext **T**ransfer **P**rotocol.

It is a **request/response** protocol:
- Client sends a request
- Server sends a response
- (Classic HTTP is **stateless** — each request is independent unless you add tokens/cookies/sessions)

### HTTP vs HTTPS
| | HTTP | HTTPS |
|--|------|-------|
| Encryption | No | Yes (TLS) |
| Safe for passwords/tokens | No | Yes |
| Production default | Avoid | Required |

> As a backend developer, always design as if traffic can be inspected — use HTTPS and never put secrets in URLs.

### Stateless in plain words
The server does **not** automatically remember the previous request.
If the user is “logged in,” your API usually checks a **token** (like JWT) on every request.

---

## 3. Request and Response

### HTTP Request (what client sends)
```
POST /api/orders HTTP/1.1
Host: api.shop.com
Content-Type: application/json
Authorization: Bearer eyJhbGciOi...

{
  "productId": "P-100",
  "quantity": 2
}
```

Main pieces:
| Piece | Meaning |
|-------|---------|
| **Method** | Verb — what kind of action (`GET`, `POST`…) |
| **Path** | Which resource (`/api/orders`) |
| **Headers** | Metadata (content type, auth, language…) |
| **Body** | Optional payload (often JSON) |

### HTTP Response (what server sends)
```
HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/orders/87

{
  "id": 87,
  "productId": "P-100",
  "quantity": 2,
  "status": "Created"
}
```

Main pieces:
| Piece | Meaning |
|-------|---------|
| **Status code** | Quick result signal (`200`, `404`, `500`…) |
| **Headers** | Metadata about the reply |
| **Body** | Optional result data (JSON, HTML, file…) |

---

## 4. HTTP Methods

Methods tell the server **what you want to do**.

| Method | Intent | Body common? | Safe? | Idempotent? |
|--------|--------|--------------|-------|-------------|
| **GET** | Read data | Usually no | Yes | Yes |
| **POST** | Create / submit | Yes | No | No (usually) |
| **PUT** | Replace full resource | Yes | No | Yes |
| **PATCH** | Update partial resource | Yes | No | Usually yes |
| **DELETE** | Remove resource | Sometimes | No | Yes |

### Simple meanings
```
GET    /api/products       → list products
GET    /api/products/10    → get product 10
POST   /api/products       → create a product
PUT    /api/products/10    → replace product 10 completely
PATCH  /api/products/10    → change only some fields of product 10
DELETE /api/products/10    → delete product 10
```

### Safe and idempotent (why seniors care)
- **Safe** = should not change server data (GET is safe)
- **Idempotent** = calling it 1 time or 5 times leaves the same final state  
  - `DELETE /items/1` five times → item still gone (same end state)  
  - `POST /orders` five times → may create five orders (not idempotent)

### Beginner mistakes to avoid
1. Using `GET` to delete or update (wrong and dangerous — caches/crawlers may replay GETs)
2. Using `POST` for everything (works, but unclear and harder to cache/document)
3. Putting sensitive data in the URL query string

---

## 5. Headers

**Headers** are key/value metadata sent with request or response.

### Common request headers
| Header | Example | Purpose |
|--------|---------|---------|
| `Content-Type` | `application/json` | Format of the body you are sending |
| `Accept` | `application/json` | Format you want back |
| `Authorization` | `Bearer <token>` | Who you are / proof of login |
| `User-Agent` | browser/app name | Who is calling |
| `Accept-Language` | `en-US` | Preferred language |

### Common response headers
| Header | Example | Purpose |
|--------|---------|---------|
| `Content-Type` | `application/json` | Format of response body |
| `Location` | `/api/orders/87` | Where a new resource lives (after create) |
| `Cache-Control` | `no-store` | Caching rules |
| `Set-Cookie` | `session=...` | Browser cookie (more common in web apps) |

```
Think of headers like the envelope labels on a parcel:
  - what's inside (Content-Type)
  - who sent it / access pass (Authorization)
  - where to reply format (Accept)
```

In ASP.NET Core you will read/write headers in middleware, authentication, and API controllers.

---

## 6. Body

The **body** carries the main payload.

| Situation | Body? |
|-----------|-------|
| `GET` product list | Usually empty request body; data comes in response body |
| `POST` create user | Request body has user fields |
| File download | Response body is file bytes |
| `DELETE` by id in URL | Request body often empty |

### Content types you will see
| Content-Type | Used for |
|--------------|----------|
| `application/json` | APIs (most common for .NET backends) |
| `application/x-www-form-urlencoded` | Traditional HTML form posts |
| `multipart/form-data` | File uploads + form fields |
| `text/html` | Web pages |
| `text/plain` | Plain text |

> Modern frontend ↔ backend communication is usually **JSON**.

---

## 7. Status Codes

Status codes are a **shared shortcut** so clients know what happened without reading a long essay.

### Families
| Range | Meaning | Examples |
|------|---------|----------|
| **1xx** | Informational | Rarely handled by beginners |
| **2xx** | Success | `200`, `201`, `204` |
| **3xx** | Redirect | `301`, `302` |
| **4xx** | Client mistake | `400`, `401`, `403`, `404` |
| **5xx** | Server mistake | `500`, `502`, `503` |

### Codes every backend dev must know
| Code | Name | When to use |
|------|------|-------------|
| **200 OK** | Success with body | Successful GET/PUT/PATCH |
| **201 Created** | Resource created | Successful POST create |
| **204 No Content** | Success, no body | Successful DELETE often |
| **400 Bad Request** | Invalid input | Validation failed |
| **401 Unauthorized** | Not authenticated | Missing/invalid login token |
| **403 Forbidden** | Authenticated but not allowed | No permission |
| **404 Not Found** | Resource missing | Wrong id / unknown route |
| **409 Conflict** | State conflict | Duplicate email, version clash |
| **500 Internal Server Error** | Unexpected server failure | Unhandled exception |

### Memory tip
```
4xx → "user/client did something wrong (or lacks access)"
5xx → "server failed; fix backend/infrastructure"
```

Never hide everything as `200` with an error message inside. Use proper codes.

---

## 8. REST Principles

**REST** = **Re**presentational **S**tate **T**ransfer.  
It is a **style** for designing web APIs (not a library).

### Core ideas (practical version)
1. **Resources** are nouns (`/orders`, `/users/5`) — not verbs (`/getOrders`)
2. **HTTP methods** express actions (`GET`, `POST`, `PUT`, `DELETE`)
3. **Stateless** requests (auth info travels with each request)
4. **Representations** — JSON is the usual representation of a resource
5. **Uniform interface** — predictable URLs and status codes
6. **Use status codes correctly**

### Good vs weak URL design
```
Good:
  GET    /api/customers
  GET    /api/customers/42
  POST   /api/customers
  GET    /api/customers/42/orders

Weak:
  GET /api/getCustomer?id=42
  POST /api/deleteCustomer
  GET /api/doAction?type=remove&id=42
```

### Resource nesting (keep shallow)
```
/api/orders/15/items        ✅ clear
/api/a/b/c/d/e/f            ❌ too deep, hard to use
```

### REST is not only CRUD
CRUD fits many APIs, but real systems also have workflows:
```
POST /api/orders/15/cancel
POST /api/payments/88/refund
```
Use verbs in path only for **genuine actions** that are not clean create/update/delete.

---

## 9. JSON Format

**JSON** = **J**ava**S**cript **O**bject **N**otation.  
It is plain text that both humans and machines can read. The #1 body format for APIs.

### Rules (simple)
- Data is **key/value pairs**
- Keys are strings in double quotes
- Values can be: string, number, boolean, null, array, object
- Commas separate items
- No comments allowed in strict JSON

### Key/value pairs
```json
{
  "name": "Selva",
  "age": 28,
  "isActive": true
}
```

### Arrays
```json
{
  "skills": ["C#", "SQL", "HTTP"]
}
```

```json
[
  { "id": 1, "title": "Keyboard" },
  { "id": 2, "title": "Mouse" }
]
```

### Nested objects
```json
{
  "orderId": 501,
  "customer": {
    "id": 17,
    "name": "Asha",
    "address": {
      "city": "Chennai",
      "pincode": "600001"
    }
  },
  "items": [
    { "productId": "P-1", "qty": 2, "price": 499.5 },
    { "productId": "P-2", "qty": 1, "price": 999.0 }
  ],
  "paid": false,
  "notes": null
}
```

### JSON types map to C# roughly like this
| JSON | C# common type |
|------|----------------|
| `"text"` | `string` |
| `42` | `int` / `long` |
| `19.99` | `decimal` / `double` |
| `true` / `false` | `bool` |
| `null` | `null` |
| `[...]` | `List<T>` / array |
| `{...}` | `class` / `record` |

### Valid vs invalid (spot the issues)
```json
// ❌ invalid: comments not allowed, single quotes, trailing comma habits from JS
{
  'name': 'Selva',
  'age': 28,
}
```

```json
{
  "name": "Selva",
  "age": 28
}
```
✅ valid

> ASP.NET Core automatically converts JSON ↔ C# objects (model binding + serialization). You still must understand JSON by hand for debugging.

---

## 10. APIs vs Web Applications

People say “web app” and “API” casually. As a backend developer, separate them clearly.

### Web Application (website)
- Users interact through a **browser UI**
- Server often returns **HTML** (and CSS/JS)
- Navigation feels like pages/screens
- Example: company portal rendered by server, or a React site hosted as static files

### API (Application Programming Interface)
- **Other programs** interact with it (mobile app, frontend SPA, another backend)
- Server usually returns **JSON** (or XML, protobuf…)
- No need for HTML buttons — callers send HTTP requests intentionally
- Example: `GET /api/products` used by Android app and website alike

### Side-by-side
| | Web Application | API |
|--|-----------------|-----|
| Primary consumer | Human via browser | Application / frontend code |
| Typical response | HTML / UI | JSON data |
| UI included? | Yes | No (data only) |
| Coupling | Tied to presentation | Reusable by many clients |
| Example URL | `/account/profile` page | `/api/users/me` data |

### Important nuance
A modern product is often **both**:
```
React / Angular website  ──HTTP JSON──►  ASP.NET Core Web API
Mobile app               ──HTTP JSON──►  same API
```
The **UI app** is a client. The **API** is your backend service.

---

## 11. How They Interact in Real Systems

```
┌──────────────┐   HTTPS + JSON    ┌────────────────────┐
│  Web UI App  │ ───────────────►  │                    │
└──────────────┘                   │   .NET Backend API │
┌──────────────┐   HTTPS + JSON    │   (business rules, │
│  Mobile App  │ ───────────────►  │    auth, database) │
└──────────────┘                   │                    │
┌──────────────┐   HTTPS + JSON    │                    │
│ Other API    │ ───────────────►  │                    │
└──────────────┘                   └─────────┬──────────┘
                                             │
                                             ▼
                                        Database
```

### Typical request life (backend view)
1. Client sends `GET /api/orders/5` with `Authorization` header  
2. API authenticates token  
3. API authorizes: can this user see order 5?  
4. API loads order from database  
5. API maps entity → response DTO  
6. API returns `200` + JSON body  

### What stays on which side?
| Concern | Frontend / Web app | Backend API |
|---------|--------------------|-------------|
| Buttons, layout, colors | ✅ | ❌ |
| Input forms UX | ✅ | ❌ (validates data only) |
| Business rules | light only | ✅ source of truth |
| Database access | ❌ | ✅ |
| Security checks | helper only | ✅ must enforce |

> Never trust the client alone. Validate and authorize on the **server**.

---

## 12. Tiny End-to-End Example

**Goal:** Create an order from a frontend.

### 1) Client sends
```http
POST /api/orders HTTP/1.1
Host: localhost:5001
Content-Type: application/json
Authorization: Bearer <token>

{
  "productId": "P-100",
  "quantity": 2
}
```

### 2) Server logic (conceptually)
- Is token valid? else `401`
- Is quantity > 0? else `400`
- Does product exist? else `404`
- Save order
- Return created order

### 3) Server responds
```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/orders/87

{
  "id": 87,
  "productId": "P-100",
  "quantity": 2,
  "status": "Created"
}
```

### 4) Client uses JSON
Web app shows: “Order #87 created.”  
Mobile app refreshes order list with `GET /api/orders`.

This is the daily heartbeat of backend work.

---

## 13. Knowledge Check

**Q1.** What are the four main parts of an HTTP request?  
**Q2.** Which method should fetch a product by id without changing data?  
**Q3.** Is `DELETE /api/items/1` considered idempotent? Why?  
**Q4.** What does status `401` mean vs `403`?  
**Q5.** Rewrite a weak endpoint `GET /api/getUser?id=9` in a more RESTful style.  
**Q6.** In JSON, can a value be another object? What is that called?  
**Q7.** Who is the primary consumer of an API — a human looking at HTML, or another program?  
**Q8.** Why must business rules be enforced on the backend, not only in the UI?

### Mini practice
Design a tiny REST surface for a bookstore:
- List books
- Get one book
- Create book
- Update book price only
- Delete book

For each, write: method + path + success status code + whether request body is needed.

### Answers (short)
1. Method, path/URL, headers, body (optional)  
2. `GET`  
3. Yes — after first delete, resource stays deleted  
4. `401` = not logged in / bad token; `403` = logged in but not allowed  
5. `GET /api/users/9`  
6. Yes — nested object  
7. Another program/client  
8. Clients can be bypassed/modified; server is the trust boundary  

---

## ✅ What You Should Feel Confident About

- [ ] Draw client → HTTP request → server → HTTP response  
- [ ] Choose correct methods: GET/POST/PUT/PATCH/DELETE  
- [ ] Read and explain common headers (`Content-Type`, `Authorization`)  
- [ ] Pick sensible status codes for success and failure  
- [ ] Design simple REST resource URLs  
- [ ] Read nested JSON (objects + arrays)  
- [ ] Explain API vs web application and how a SPA talks to a .NET API  

**Previous:** [02-oop-concepts.md](./02-oop-concepts.md)

---

## 🚀 Module 0 Wrap-Up

You now have the three foundations every .NET backend beginner needs:

1. **Programming basics** — variables, logic, methods, collections  
2. **OOP** — structure code with classes, encapsulation, interfaces  
3. **Web basics** — HTTP, REST, JSON, APIs  

**Next learning path (suggested):** C# language depth → ASP.NET Core Web API → EF Core / database → Authentication → Architecture & patterns.
