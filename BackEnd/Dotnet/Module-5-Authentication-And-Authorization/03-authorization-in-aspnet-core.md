# 🛡️ Authorization in ASP.NET Core — Roles, Policies & Protected Endpoints

> **Trainer's Note:** Authentication only opens the door. **Authorization** decides which rooms you may enter. In ASP.NET Core you start with `[Authorize]`, then layer **roles** and **policies** for real permission models. Keep controllers declarative; put complex rules in handlers/services.

---

## 📑 Table of Contents
1. [Authorization After Authentication](#1-authorization-after-authentication)
2. [`[Authorize]` and `[AllowAnonymous]`](#2-authorize-and-allowanonymous)
3. [Controller vs Action Level Rules](#3-controller-vs-action-level-rules)
4. [Reading the Current User](#4-reading-the-current-user)
5. [Role-Based Access Control (RBAC)](#5-role-based-access-control-rbac)
6. [Embedding Roles in JWTs](#6-embedding-roles-in-jwts)
7. [Policy-Based Authorization](#7-policy-based-authorization)
8. [Custom Requirements and Handlers](#8-custom-requirements-and-handlers)
9. [Resource-Based Authorization (Awareness)](#9-resource-based-authorization-awareness)
10. [Practical Endpoint Patterns](#10-practical-endpoint-patterns)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. Authorization After Authentication

```
Token valid?
   no  → 401
   yes → identity established (User is authenticated)
            │
            ▼
         Allowed by role/policy/resource rules?
            no  → 403
            yes → action runs
```

| Result | Meaning |
|--------|---------|
| 401 | No valid authentication |
| 403 | Authenticated but forbidden |
| 200… | Passed authZ |

Ensure:
```csharp
builder.Services.AddAuthorization();
app.UseAuthentication();
app.UseAuthorization();
```

---

## 2. `[Authorize]` and `[AllowAnonymous]`

### Protect an action
```csharp
[HttpGet("{id:int}")]
[Authorize]
public async Task<ActionResult<OrderDto>> GetById(int id, CancellationToken ct)
{
    // only authenticated users
}
```

### Protect a whole controller
```csharp
[ApiController]
[Route("api/orders")]
[Authorize]
public class OrdersController : ControllerBase
{
    [HttpGet]
    public IActionResult List() => Ok();

    [HttpGet("public-stats")]
    [AllowAnonymous] // exception for one action
    public IActionResult PublicStats() => Ok(new { openOrders = 10 });
}
```

| Attribute | Effect |
|-----------|--------|
| `[Authorize]` | Requires authenticated user (by default) |
| `[AllowAnonymous]` | Allows call without auth even if controller is protected |

### Fallback policy (optional hard default)
```csharp
builder.Services.AddAuthorization(options =>
{
    options.FallbackPolicy = new AuthorizationPolicyBuilder()
        .RequireAuthenticatedUser()
        .Build();
});
```
Then every endpoint needs auth unless `[AllowAnonymous]`. Great for secure-by-default APIs.

---

## 3. Controller vs Action Level Rules

```csharp
[Authorize] // all actions need login
public class ProductsController : ControllerBase
{
    [HttpGet]
    public IActionResult GetAll() => Ok(); // any authenticated user

    [Authorize(Roles = "Admin")]
    [HttpDelete("{id:int}")]
    public IActionResult Delete(int id) => NoContent(); // tighter
}
```

Most specific applicable rules combine: user must satisfy requirements. Prefer least privilege on sensitive verbs (`DELETE`, `PUT`).

---

## 4. Reading the Current User

```csharp
var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);
var email = User.FindFirstValue(ClaimTypes.Email);
var isAdmin = User.IsInRole("Admin");
var roles = User.FindAll(ClaimTypes.Role).Select(c => c.Value);
```

```csharp
[HttpGet("me")]
[Authorize]
public IActionResult Me()
{
    return Ok(new
    {
        IsAuthenticated = User.Identity?.IsAuthenticated ?? false,
        Name = User.Identity?.Name,
        Claims = User.Claims.Select(c => new { c.Type, c.Value })
    });
}
```

Use `userId` from claims to filter data (“only my orders”) — don’t trust a client-sent user id blindly.

---

## 5. Role-Based Access Control (RBAC)

**RBAC** assigns users to **roles**; roles grant access.

```
Users          Roles           Permissions (conceptual)
─────          ─────           ────────────────────────
Selva    →     Admin      →    manage products, users
Asha     →     Manager    →    manage orders
Ravi     →     Customer   →    place/read own orders
```

### Attribute usage
```csharp
[Authorize(Roles = "Admin")]
[HttpPost]
public IActionResult CreateProduct() => Ok();

[Authorize(Roles = "Admin,Manager")] // OR semantics for multiple roles in one attribute
[HttpGet("reports")]
public IActionResult Reports() => Ok();
```

### Multiple `[Authorize]` attributes
```csharp
[Authorize(Roles = "Admin")]
[Authorize(Roles = "Finance")] // AND — must satisfy both attributes
```
Know the difference: comma inside one attribute vs multiple attributes.

### When RBAC shines
- Coarse permissions  
- Simple org structures  
- Fast to implement  

### When RBAC gets awkward
- “Managers can refund only orders under $100”  
- “Users edit their own profile only”  
→ need **policies** and/or **resource checks**

---

## 6. Embedding Roles in JWTs

Roles must appear as role claims for `Roles = "..."` to work.

### When issuing token
```csharp
foreach (var role in user.Roles)
    claims.Add(new Claim(ClaimTypes.Role, role));
```

### Role claim type gotcha
JWT may emit `"role"` while ASP.NET expects `ClaimTypes.Role` URI.

If roles don’t bind, map the inbound claim:

```csharp
.AddJwtBearer(options =>
{
    options.TokenValidationParameters = new TokenValidationParameters
    {
        // ... standard validation ...
        RoleClaimType = ClaimTypes.Role,
        NameClaimType = ClaimTypes.Name
    };

    // Sometimes needed depending on token shape:
    // options.MapInboundClaims = false; // advanced; understand before flipping
});
```

Also check `JwtSecurityTokenHandler.DefaultInboundClaimTypeMap` behavior when debugging missing roles.

### Practical test
Login as Admin → inspect `/api/auth/me` claims → confirm role claim present → hit `[Authorize(Roles="Admin")]` endpoint.

---

## 7. Policy-Based Authorization

**Policies** name a bundle of requirements.

```csharp
builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("StaffOnly", policy =>
        policy.RequireRole("Admin", "Manager"));

    options.AddPolicy("HasEmail", policy =>
        policy.RequireClaim(ClaimTypes.Email));

    options.AddPolicy("Over21", policy =>
        policy.Requirements.Add(new MinimumAgeRequirement(21)));
});
```

### Use policy name
```csharp
[Authorize(Policy = "StaffOnly")]
[HttpGet("dashboard")]
public IActionResult Dashboard() => Ok();
```

| Style | Example | Best for |
|-------|---------|----------|
| Roles | `[Authorize(Roles="Admin")]` | simple RBAC |
| Policy | `[Authorize(Policy="StaffOnly")]` | named reusable rules |
| Custom requirement | age, department, feature flags | granular logic |

Policies scale better: rename/centralize rules without hunting magic strings on every action (still be consistent).

---

## 8. Custom Requirements and Handlers

### 1) Requirement
```csharp
public class MinimumAgeRequirement : IAuthorizationRequirement
{
    public MinimumAgeRequirement(int minimumAge) => MinimumAge = minimumAge;
    public int MinimumAge { get; }
}
```

### 2) Handler
```csharp
public class MinimumAgeHandler : AuthorizationHandler<MinimumAgeRequirement>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        MinimumAgeRequirement requirement)
    {
        var dobValue = context.User.FindFirstValue("dob"); // date of birth claim
        if (dobValue is null) return Task.CompletedTask;

        if (!DateTime.TryParse(dobValue, out var dob)) return Task.CompletedTask;

        var age = DateTime.UtcNow.Year - dob.Year;
        if (dob.Date > DateTime.UtcNow.AddYears(-age)) age--;

        if (age >= requirement.MinimumAge)
            context.Succeed(requirement);

        return Task.CompletedTask;
    }
}
```

### 3) Register handler
```csharp
builder.Services.AddSingleton<IAuthorizationHandler, MinimumAgeHandler>();
```

### Another useful example: department claim
```csharp
public class DepartmentRequirement : IAuthorizationRequirement
{
    public DepartmentRequirement(string department) => Department = department;
    public string Department { get; }
}

public class DepartmentHandler : AuthorizationHandler<DepartmentRequirement>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        DepartmentRequirement requirement)
    {
        if (context.User.HasClaim("department", requirement.Department))
            context.Succeed(requirement);
        return Task.CompletedTask;
    }
}
```

```csharp
options.AddPolicy("FinanceDepartment", p =>
    p.Requirements.Add(new DepartmentRequirement("Finance")));
```

Handlers keep complex if/else out of controllers.

---

## 9. Resource-Based Authorization (Awareness)

Sometimes permission depends on the **resource instance**:
- “Edit order **only if I own it**”  
- “Managers approve orders in **their region**”  

```csharp
// conceptual flow
var order = await _orders.GetAsync(id);
var auth = await _authorizationService.AuthorizeAsync(User, order, "EditOrder");
if (!auth.Succeeded) return Forbid();
```

Custom handlers receive the resource object and evaluate ownership/region rules.

This is more advanced than attribute-only authZ but essential for multi-tenant/user-owned data. You can enforce simpler ownership in services too:

```csharp
if (order.CustomerId.ToString() != userId) return Forbid();
```
Prefer centralized handlers as the app grows.

---

## 10. Practical Endpoint Patterns

### Public catalog
```csharp
[AllowAnonymous]
[HttpGet]
public IActionResult ListProducts() => Ok();
```

### Authenticated create order
```csharp
[Authorize]
[HttpPost]
public async Task<IActionResult> PlaceOrder(PlaceOrderRequest request) { /* ... */ }
```

### Admin delete
```csharp
[Authorize(Roles = "Admin")]
[HttpDelete("{id:int}")]
public async Task<IActionResult> Delete(int id) { /* ... */ }
```

### Policy-protected report
```csharp
[Authorize(Policy = "StaffOnly")]
[HttpGet("sales-summary")]
public IActionResult SalesSummary() => Ok();
```

### Combine identities carefully
```
Customer token hitting Admin endpoint → 403
Expired Admin token → 401
Missing token on protected endpoint → 401
```

### Fail closed
Default to deny when unsure. Explicitly allow public endpoints with `[AllowAnonymous]`.

---

## 11. Knowledge Check

**Q1.** Difference between `[Authorize]` and `[AllowAnonymous]`?  
**Q2.** 401 vs 403 after a protected call — how do you interpret them?  
**Q3.** How do you restrict an action to Admin using RBAC?  
**Q4.** Why might `[Authorize(Roles="Admin")]` fail even after login?  
**Q5.** What is a policy in ASP.NET Core authorization?  
**Q6.** What two types do you implement for custom policy logic?  
**Q7.** Why is “only the owner can edit” often more than a simple role check?

### Mini practice
1. Protect all `OrdersController` actions with `[Authorize]`  
2. Allow anonymous on `GET /api/products`  
3. Restrict `DELETE /api/products/{id}` to role `Admin`  
4. Add policy `StaffOnly` for Admin|Manager and apply it  
5. Implement a custom claim-based policy (e.g., `department=Finance`)  
6. Verify 401/403 behavior with different tokens  

### Answers (short)
1. Require auth vs explicitly allow unauthenticated access  
2. 401 unauthenticated/invalid token; 403 authenticated but not permitted  
3. `[Authorize(Roles = "Admin")]`  
4. Role claim missing/mismapped in JWT  
5. Named set of authorization requirements  
6. `IAuthorizationRequirement` + `AuthorizationHandler<T>`  
7. Depends on resource ownership/data, not only global role  

---

## ✅ What You Should Feel Confident About

- [ ] Protect endpoints with `[Authorize]` and carve-outs with `[AllowAnonymous]`  
- [ ] Apply role-based checks  
- [ ] Put roles into JWTs and verify claim mapping  
- [ ] Define and apply named policies  
- [ ] Write a simple custom requirement + handler  
- [ ] Distinguish coarse RBAC from resource-based rules  

**Previous:** [02-jwt-authentication.md](./02-jwt-authentication.md)  
**Next:** [04-aspnet-core-identity.md](./04-aspnet-core-identity.md) — Identity users, roles, registration, and password hashing.
