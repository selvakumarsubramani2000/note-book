# Module 7 — Advanced Backend Topics

> Make ASP.NET Core Web APIs **production-ready**: observable, faster where it counts, resilient with background work, safe with files, and hardened against common attacks.

**Outcome:** Apply logging/monitoring, caching, background jobs, file handling, and security best practices on top of everything from Modules 3–6.

---

## 📚 Contents

| # | File | What you learn |
|---|------|----------------|
| 01 | [01-logging-and-monitoring.md](./01-logging-and-monitoring.md) | `ILogger` levels, structured logging, Serilog/sinks, PII-safe logs |
| 02 | [02-caching.md](./02-caching.md) | `IMemoryCache`, absolute/sliding expiry, Redis/`IDistributedCache`, invalidation |
| 03 | [03-background-jobs-and-scheduling.md](./03-background-jobs-and-scheduling.md) | `IHostedService`, `BackgroundService`, scopes, Hangfire & Quartz.NET |
| 04 | [04-file-handling.md](./04-file-handling.md) | `IFormFile`, upload validation, disk vs blob storage, streaming downloads |
| 05 | [05-security-best-practices.md](./05-security-best-practices.md) | OWASP-minded API risks, SQLi/XSS/CSRF, safe errors, secrets management |

---

## 🗺️ Learning path

```
01 Observe the system (logs)
        │
        ▼
02 Speed up hot reads (cache)
        │
        ▼
03 Move slow work off the request (jobs)
        │
        ▼
04 Handle files safely
        │
        ▼
05 Harden end-to-end security
```

### Suggested hands-on build
1. Structured request/business logs with `traceId`  
2. Memory-cache product-by-id with invalidate-on-update  
3. `BackgroundService` cleanup or outbox email poller  
4. Authenticated upload + streamed download endpoint  
5. Ownership checks + user-secrets for JWT/DB keys  
6. Personal production publish checklist from file 05  

---

## 🔗 Depends on

| Module | Why |
|--------|-----|
| [Module 3 — Web API](../Module-3-AspNetCore-Web-API-Fundamentals/) | Host, DI, middleware |
| [Module 4 — EF Core](../Module-4-Databases-And-EF-Core/) | Data access in workers/services |
| [Module 5 — Auth](../Module-5-Authentication-And-Authorization/) | JWT/Identity security baseline |
| [Module 6 — Design/Validation/Errors](../Module-6-API-Design-Validation-And-Error-Handling/) | Problem Details, validation, safe errors |

---

## ✅ Module completion checklist

- [ ] Log with levels + templates; avoid secrets/PII  
- [ ] Cache reads with expiry and invalidation  
- [ ] Know when to use distributed cache (multi-node)  
- [ ] Run background work via `BackgroundService` + scopes  
- [ ] Explain Hangfire/Quartz at a high level  
- [ ] Accept and validate uploads; store safely  
- [ ] Stream file downloads with authorization  
- [ ] Prevent IDOR and SQL injection habitually  
- [ ] Manage secrets outside git  
- [ ] Apply a production hardening checklist  

---

## ⏭️ Next

**Suggested:** Testing & CI/CD — automated tests for APIs, containerization, deployment pipelines, and deeper observability (OpenTelemetry/metrics/traces).
