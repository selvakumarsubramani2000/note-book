# Module 5 — Authentication & Authorization

> Secure ASP.NET Core Web APIs with **stateless JWT bearer tokens**, **roles**, **policies**, and **ASP.NET Core Identity**.

**Outcome:** Design, configure, and protect API endpoints end-to-end — from password hashing and login issuance to `[Authorize]`, RBAC, custom policies, and Identity-backed user management.

---

## 📚 Contents

| # | File | What you learn |
|---|------|----------------|
| 01 | [01-security-basics.md](./01-security-basics.md) | AuthN vs AuthZ, **401 vs 403**, stateful vs **stateless** tokens, hashing vs encryption vs encoding, salting & secure storage |
| 02 | [02-jwt-authentication.md](./02-jwt-authentication.md) | JWT anatomy (header/payload/signature), `JwtBearer` setup in `Program.cs`, login + signed token issuance, `Authorization: Bearer`, debugging **401** |
| 03 | [03-authorization-in-aspnet-core.md](./03-authorization-in-aspnet-core.md) | `[Authorize]` / `[AllowAnonymous]`, **RBAC** with roles in JWT, **policy-based** auth, custom requirements & handlers |
| 04 | [04-aspnet-core-identity.md](./04-aspnet-core-identity.md) | Identity + EF Core, `UserManager` / `SignInManager`, register/login, password hashing & lockout, users, roles, claims + JWT |

---

## 🗺️ Learning path

```
01 Security concepts
        │
        ▼
02 Issue & validate JWTs
        │
        ▼
03 Gate endpoints (roles + policies)
        │
        ▼
04 Identity membership store + login/register
        │
        ▼
   Secured Web API (Bearer + Identity)
```

### Suggested hands-on build
1. Public `GET /api/products`  
2. `POST /api/auth/register` + `POST /api/auth/login` → JWT  
3. Authenticated `POST /api/orders` with `[Authorize]`  
4. Admin `DELETE /api/products/{id}` with `[Authorize(Roles = "Admin")]`  
5. Policy-protected report endpoint (e.g. `StaffOnly` or department claim)  

---

## 🔗 Depends on

| Module | Why |
|--------|-----|
| [Module 3 — Web API Fundamentals](../Module-3-AspNetCore-Web-API-Fundamentals/) | Controllers, middleware order, DI, configuration |
| [Module 4 — EF Core](../Module-4-Databases-And-EF-Core/) | DbContext, migrations (Identity tables) |

---

## ✅ Module completion checklist

- [ ] Explain AuthN vs AuthZ and choose 401 vs 403 correctly  
- [ ] Configure `AddAuthentication().AddJwtBearer(...)` and middleware order  
- [ ] Implement login that issues a signed JWT with user id + roles  
- [ ] Call protected APIs with `Authorization: Bearer <token>`  
- [ ] Use `[Authorize]`, `[AllowAnonymous]`, and role restrictions  
- [ ] Define at least one named authorization policy  
- [ ] Integrate Identity (`IdentityDbContext`, register, password hash)  
- [ ] Login with `UserManager` and/or `SignInManager` (lockout-aware)  
- [ ] Keep JWT signing keys and passwords out of source control  

---

## ⏭️ Next

**Module 6 (suggested):** Testing & Quality — unit/integration tests for APIs, authenticated test clients, and verifying authorization rules automatically.
