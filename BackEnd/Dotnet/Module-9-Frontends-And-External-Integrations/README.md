# Module 9 — Frontends & External Integrations

> Connect your ASP.NET Core API to **SPAs**, document it with **OpenAPI/Swagger**, and call **third-party services** safely with `IHttpClientFactory`.

**Outcome:** Configure CORS for browser clients, publish a clear API contract, and integrate email/payments/external auth patterns without socket exhaustion or secret leaks.

---

## 📚 Contents

| # | File | What you learn |
|---|------|----------------|
| 01 | [01-frontend-consumption-and-cors.md](./01-frontend-consumption-and-cors.md) | How React/Angular consume APIs; CORS & preflight; stable contracts |
| 02 | [02-api-documentation-openapi.md](./02-api-documentation-openapi.md) | OpenAPI/Swagger; UI + JSON spec; annotations; bearer try-it-out |
| 03 | [03-integrating-external-services.md](./03-integrating-external-services.md) | `HttpClient` / `IHttpClientFactory`; timeouts; Polly-style retries; email/pay/IdP patterns |

---

## 🗺️ Learning path

```
01 Let the SPA talk to you (CORS + contracts)
        │
        ▼
02 Document and try the API (OpenAPI)
        │
        ▼
03 Call other APIs the right way (HttpClient factory + resilience)
```

### Suggested hands-on build
1. Allow `http://localhost:3000` via named CORS policy  
2. SPA fetch list + authorized POST  
3. Swagger UI with title, 200/400/404 annotations, Bearer auth  
4. Typed client for an external API with timeout  
5. Sketch payment intent + webhook flow on paper  
6. Move third-party API key to user-secrets  

---

## 🔗 Depends on

| Module | Why |
|--------|-----|
| Module 3 — Web API | Controllers, middleware order |
| Module 5 — Auth | JWT for SPA and Swagger Authorize |
| Module 6 — Design/Errors/Versioning | Contracts, problem details, versions |
| Module 7 — Advanced | Outbox/background sends for email |
| Module 8 — Testing | Mock external HTTP ports |

---

## ✅ Completion checklist

- [ ] Explain SPA ↔ API JSON flow  
- [ ] Configure CORS with explicit origins  
- [ ] Avoid credential + `AllowAnyOrigin` mistakes  
- [ ] Serve OpenAPI JSON and Swagger UI in Development  
- [ ] Annotate responses and enable Bearer testing  
- [ ] Use `IHttpClientFactory` / typed clients  
- [ ] Apply timeouts and cautious retries  
- [ ] Sketch email, payment, and external login integrations  

---

## ⏭️ Next

Deployment/containers, API gateways, deeper resilience policies, and consumer-driven contract tests against OpenAPI.
