# 👤 ASP.NET Core Identity — Users, Roles, Registration & Secure Passwords

> **Trainer's Note:** Identity is Microsoft’s full membership system for .NET apps: users, roles, claims, password hashing, lockout, and EF Core stores. You combine Identity for **user management** with JWT bearer for **API authentication**. Don’t reinvent password storage.

---

## 📑 Table of Contents
1. [What Identity Gives You](#1-what-identity-gives-you)
2. [Packages and Project Setup](#2-packages-and-project-setup)
3. [Custom User Type and DbContext](#3-custom-user-type-and-dbcontext)
4. [Register Identity Services](#4-register-identity-services)
5. [Password Options and Validation](#5-password-options-and-validation)
6. [User Registration Endpoint](#6-user-registration-endpoint)
7. [Login Workflow with Identity + JWT](#7-login-workflow-with-identity--jwt)
8. [Using SignInManager for Validation & Lockout](#8-using-signinmanager-for-validation--lockout)
9. [Working with Roles](#9-working-with-roles)
10. [Claims on Users](#10-claims-on-users)
11. [Common Operations Cheat Sheet](#11-common-operations-cheat-sheet)
12. [Knowledge Check](#12-knowledge-check)

---

## 1. What Identity Gives You

| Feature | Why it matters |
|---------|----------------|
| User store | Create/find/update users |
| Password hasher | Secure salted hashing by default |
| Password validators | Length, complexity rules |
| Roles | Map users ↔ roles |
| Claims | Extra user attributes |
| Lockout | Brute-force protection options |
| Token providers | Email confirmation / reset flows (extend later) |
| EF Core integration | Tables via migrations |

```
Identity (membership & password security)
        +
JWT bearer (stateless API access tokens)
        =
Common modern Web API auth stack
```

Identity can also do cookie auth for MVC/Blazor. For pure APIs, use Identity APIs + issue JWTs yourself (as in file 02).

---

## 2. Packages and Project Setup

```bash
dotnet add package Microsoft.AspNetCore.Identity.EntityFrameworkCore
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
# or Npgsql package for PostgreSQL
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
```

Design package + `dotnet-ef` still needed for migrations (Module 4).

### Mental model of tables (simplified)
```
AspNetUsers
AspNetRoles
AspNetUserRoles
AspNetUserClaims
AspNetRoleClaims
AspNetUserLogins
AspNetUserTokens
```
You can rename/customize with fluent config; beginners can keep defaults.

---

## 3. Custom User Type and DbContext

### User class
```csharp
using Microsoft.AspNetCore.Identity;

public class AppUser : IdentityUser
{
    // IdentityUser already has: Id, Email, UserName, PasswordHash, ...
    public string? DisplayName { get; set; }
}
```

`IdentityUser` default key is `string` (GUID strings). You can use `IdentityUser<Guid>` if you prefer GUID keys.

### DbContext
```csharp
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

public class AppDbContext : IdentityDbContext<AppUser>
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
    {
    }

    public DbSet<Product> Products => Set<Product>();

    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder); // required for Identity model
        // your entity configs...
    }
}
```

### Migration
```bash
dotnet ef migrations add AddIdentity
dotnet ef database update
```

---

## 4. Register Identity Services

```csharp
builder.Services.AddDbContext<AppDbContext>(opt =>
    opt.UseSqlServer(builder.Configuration.GetConnectionString("ShopDb")));

builder.Services
    .AddIdentity<AppUser, IdentityRole>(options =>
    {
        // password options shown in next section
        options.User.RequireUniqueEmail = true;
        options.SignIn.RequireConfirmedAccount = false; // enable later with email flow
    })
    .AddEntityFrameworkStores<AppDbContext>()
    .AddDefaultTokenProviders();

// JWT auth (from Module file 02)
builder.Services
    .AddAuthentication(options =>
    {
        options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
        options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
    })
    .AddJwtBearer(/* TokenValidationParameters */);

builder.Services.AddAuthorization();
builder.Services.AddScoped<ITokenService, TokenService>();
```

### Why set DefaultAuthenticateScheme to JWT?
API clients send bearer tokens, not Identity cookies. You still use `UserManager` / `RoleManager` for store operations.

### Managers you inject
| Type | Purpose |
|------|---------|
| `UserManager<AppUser>` | Create users, check passwords, roles/claims on users |
| `RoleManager<IdentityRole>` | Create/manage roles |
| `SignInManager<AppUser>` | High-level sign-in helpers: password check + lockout + cookie flows |

**For pure JWT Web APIs:**
- Use `UserManager` for registration, roles, claims, password hashes
- Use `SignInManager.CheckPasswordSignInAsync` when you want **lockout and sign-in result flags** without issuing cookies
- You usually **do not** call `PasswordSignInAsync` (that is cookie-oriented) unless you also run browser cookie auth

Both approaches are valid. Beginners often start with `CheckPasswordAsync`, then graduate to `SignInManager` for lockout.

---

## 5. Password Options and Validation

```csharp
builder.Services.AddIdentity<AppUser, IdentityRole>(options =>
{
    options.Password.RequiredLength = 8;
    options.Password.RequireDigit = true;
    options.Password.RequireLowercase = true;
    options.Password.RequireUppercase = true;
    options.Password.RequireNonAlphanumeric = true;
    options.Password.RequiredUniqueChars = 1;

    options.Lockout.MaxFailedAccessAttempts = 5;
    options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(15);
    options.Lockout.AllowedForNewUsers = true;

    options.User.RequireUniqueEmail = true;
});
```

### What happens under the hood on create
```
plain password
   → Identity PasswordHasher (salted, modern algorithm)
   → PasswordHash column stored
```
You never write hash code yourself for standard cases.

### Tuning tip
Balance security and UX. Prefer longer passphrases; consider relaxing symbol rules if length is high (org policy dependent).

---

## 6. User Registration Endpoint

### DTO
```csharp
public class RegisterRequest
{
    [Required, EmailAddress]
    public string Email { get; set; } = string.Empty;

    [Required, MinLength(8)]
    public string Password { get; set; } = string.Empty;

    public string? DisplayName { get; set; }
}
```

### Endpoint
```csharp
[ApiController]
[Route("api/auth")]
public class AuthController : ControllerBase
{
    private readonly UserManager<AppUser> _users;

    public AuthController(UserManager<AppUser> users) => _users = users;

    [HttpPost("register")]
    [AllowAnonymous]
    public async Task<IActionResult> Register(RegisterRequest request)
    {
        var existing = await _users.FindByEmailAsync(request.Email);
        if (existing is not null)
            return Conflict(new { message = "Email already registered" });

        var user = new AppUser
        {
            UserName = request.Email,
            Email = request.Email,
            DisplayName = request.DisplayName
        };

        var result = await _users.CreateAsync(user, request.Password);
        if (!result.Succeeded)
        {
            return BadRequest(new
            {
                errors = result.Errors.Select(e => e.Description)
            });
        }

        // optional: await _users.AddToRoleAsync(user, "Customer");

        return CreatedAtAction(nameof(Register), new { id = user.Id }, new
        {
            user.Id,
            user.Email,
            user.DisplayName
        });
    }
}
```

`CreateAsync(user, password)` validates password options + stores hash.

---

## 7. Login Workflow with Identity + JWT

### Approach A — `UserManager.CheckPasswordAsync` (simple)
```csharp
[HttpPost("login")]
[AllowAnonymous]
public async Task<ActionResult<LoginResponse>> Login(
    LoginRequest request,
    [FromServices] ITokenService tokens)
{
    var user = await _users.FindByEmailAsync(request.Email);
    if (user is null)
        return Unauthorized(new { message = "Invalid email or password" });

    var valid = await _users.CheckPasswordAsync(user, request.Password);
    if (!valid)
        return Unauthorized(new { message = "Invalid email or password" });

    var roles = await _users.GetRolesAsync(user);
    var response = tokens.CreateToken(user, roles);
    return Ok(response);
}
```

### Token service accepts roles
```csharp
public LoginResponse CreateToken(AppUser user, IList<string> roles)
{
    var claims = new List<Claim>
    {
        new(ClaimTypes.NameIdentifier, user.Id),
        new(ClaimTypes.Name, user.UserName ?? user.Email ?? user.Id),
        new(ClaimTypes.Email, user.Email ?? string.Empty),
        new(JwtRegisteredClaimNames.Sub, user.Id)
    };
    foreach (var role in roles)
        claims.Add(new Claim(ClaimTypes.Role, role));

    // sign JWT as in 02-jwt-authentication.md
}
```

### End-to-end flow
```
POST /api/auth/register
POST /api/auth/login  → JWT
GET  /api/orders      + Authorization: Bearer …
```

---

## 8. Using SignInManager for Validation & Lockout

`SignInManager<TUser>` sits on top of `UserManager` and adds **sign-in orchestration**:
password check, lockout counters, two-factor flags, and (for web apps) cookie issuance.

### Inject both managers
```csharp
[ApiController]
[Route("api/auth")]
public class AuthController : ControllerBase
{
    private readonly UserManager<AppUser> _users;
    private readonly SignInManager<AppUser> _signIn;
    private readonly ITokenService _tokens;

    public AuthController(
        UserManager<AppUser> users,
        SignInManager<AppUser> signIn,
        ITokenService tokens)
    {
        _users = users;
        _signIn = signIn;
        _tokens = tokens;
    }
}
```

### Approach B — recommended API login with lockout awareness
```csharp
[HttpPost("login")]
[AllowAnonymous]
public async Task<ActionResult<LoginResponse>> Login(LoginRequest request)
{
    var user = await _users.FindByEmailAsync(request.Email);
    if (user is null)
        return Unauthorized(new { message = "Invalid email or password" });

    // lockoutOnFailure: true → counts failures toward lockout
    var result = await _signIn.CheckPasswordSignInAsync(
        user,
        request.Password,
        lockoutOnFailure: true);

    if (result.IsLockedOut)
        return StatusCode(StatusCodes.Status423Locked,
            new { message = "Account locked. Try again later." });

    if (result.IsNotAllowed)
        return Unauthorized(new { message = "Sign-in not allowed for this account." });

    if (!result.Succeeded)
        return Unauthorized(new { message = "Invalid email or password" });

    // Optional: clear failure count on success is handled by Identity flows
    var roles = await _users.GetRolesAsync(user);
    var dbClaims = await _users.GetClaimsAsync(user);
    return Ok(_tokens.CreateToken(user, roles, dbClaims));
}
```

### `CheckPasswordSignInAsync` vs `PasswordSignInAsync`
| Method | Cookie issued? | Typical use |
|--------|----------------|-------------|
| `CheckPasswordSignInAsync` | **No** | **JWT APIs** — validate + lockout, then issue your own token |
| `PasswordSignInAsync` | **Yes** (Identity application cookie) | MVC/Razor/Blazor server apps with cookie auth |
| `UserManager.CheckPasswordAsync` | No | Simple password verify; **you** handle lockout manually if needed |

```
JWT API sweet spot:

  SignInManager.CheckPasswordSignInAsync  (validate + lockout)
            │
            ▼ success
  ITokenService.CreateToken(...)          (stateless access token)
            │
            ▼
  Client sends Authorization: Bearer ...
```

### Manual lockout helpers (if not using SignInManager)
```csharp
await _users.AccessFailedAsync(user);          // increment fail count
await _users.ResetAccessFailedCountAsync(user);
var locked = await _users.IsLockedOutAsync(user);
```

### Enable lockout in options (reminder)
```csharp
options.Lockout.MaxFailedAccessAttempts = 5;
options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(15);
options.Lockout.AllowedForNewUsers = true;
```

> **Important:** Lockout only helps if your login path actually records failures (`lockoutOnFailure: true` or `AccessFailedAsync`). A bare `CheckPasswordAsync` without those calls will not lock accounts.

---

## 9. Working with Roles

### Ensure roles exist (startup seed)
```csharp
public static async Task SeedRolesAsync(RoleManager<IdentityRole> roles)
{
    string[] required = ["Admin", "Manager", "Customer"];
    foreach (var name in required)
    {
        if (!await roles.RoleExistsAsync(name))
            await roles.CreateAsync(new IdentityRole(name));
    }
}
```

Call inside a startup scope after migrate (Development/first deploy strategies vary).

### Assign role to user
```csharp
await _users.AddToRoleAsync(user, "Admin");
await _users.RemoveFromRoleAsync(user, "Customer");
var userRoles = await _users.GetRolesAsync(user);
var isAdmin = await _users.IsInRoleAsync(user, "Admin");
```

### Admin-only endpoint remains the same
```csharp
[Authorize(Roles = "Admin")]
[HttpPost("assign-role")]
public async Task<IActionResult> AssignRole(string userId, string role)
{
    var user = await _users.FindByIdAsync(userId);
    if (user is null) return NotFound();

    var result = await _users.AddToRoleAsync(user, role);
    return result.Succeeded ? NoContent() : BadRequest(result.Errors);
}
```

Remember: roles assigned in DB must be **re-issued into new JWTs** on next login (existing tokens keep old claims until expiry).

---

## 10. Claims on Users

Claims = key/value attributes stored for a user (beyond roles).

```csharp
await _users.AddClaimAsync(user, new Claim("department", "Finance"));
await _users.AddClaimAsync(user, new Claim("employee_number", "E-204"));

var claims = await _users.GetClaimsAsync(user);
```

### Include custom claims in JWT at login
```csharp
var dbClaims = await _users.GetClaimsAsync(user);
claims.AddRange(dbClaims);
```

Then policy handlers can require `department=Finance` as in file 03.

### Role claims vs user claims
| | Role | User claim |
|--|------|------------|
| Scope | Many users share | Specific to one user |
| Example | `Admin` | `department=Finance` |
| Management | `RoleManager` / user-role links | `UserManager` claims APIs |

---

## 11. Common Operations Cheat Sheet

| Goal | API |
|------|-----|
| Create user + password | `UserManager.CreateAsync(user, password)` |
| Find by email | `FindByEmailAsync` |
| Find by id | `FindByIdAsync` |
| Verify password | `CheckPasswordAsync` |
| Validate password + lockout (API) | `SignInManager.CheckPasswordSignInAsync` |
| Cookie sign-in (MVC-style) | `SignInManager.PasswordSignInAsync` |
| Record failed attempt | `AccessFailedAsync` |
| Change password | `ChangePasswordAsync` |
| Add to role | `AddToRoleAsync` |
| Get roles | `GetRolesAsync` |
| Add claim | `AddClaimAsync` |
| Get claims | `GetClaimsAsync` |
| Create role | `RoleManager.CreateAsync` |
| Role exists? | `RoleExistsAsync` |

### IdentityResult handling
```csharp
if (!result.Succeeded)
{
    foreach (var error in result.Errors)
        ModelState.AddModelError(error.Code, error.Description);
    return ValidationProblem(ModelState);
}
```

### Security extras to explore later
- Email confirmation  
- Password reset tokens  
- Two-factor authentication  
- External logins (Google, Microsoft)  
- Refresh tokens + rotation  

Master register/login/roles/JWT first.

---

## 12. Knowledge Check

**Q1.** What does Identity handle for you that you should not reinvent first?
**Q2.** Why inherit `IdentityDbContext<AppUser>` instead of plain `DbContext`?
**Q3.** Which method creates a user and hashes the password?
**Q4.** Name two ways to verify credentials at login with Identity.
**Q5.** For a JWT API, why prefer `CheckPasswordSignInAsync` over `PasswordSignInAsync`?
**Q6.** After `AddToRoleAsync`, does an already-issued JWT suddenly gain that role?
**Q7.** Difference between roles and user claims?
**Q8.** For a pure Web API, which auth scheme usually validates requests — Identity cookie or JWT bearer?

### Mini practice
1. Add Identity EF packages and `AppUser`
2. Convert DbContext to `IdentityDbContext<AppUser>` and migrate
3. Configure password options + lockout + JWT defaults
4. Implement `POST /api/auth/register` with `UserManager.CreateAsync`
5. Implement `POST /api/auth/login` with `SignInManager.CheckPasswordSignInAsync` + JWT issue
6. Seed roles and assign `Admin` to one user
7. Protect an endpoint with `[Authorize(Roles="Admin")]` and test with tokens
8. Intentionally fail login until lockout triggers and observe the response

### Answers (short)
1. Password hashing/validation, user/role/claim storage, lockout primitives…
2. It includes Identity user/role/claim model configuration and sets
3. `UserManager.CreateAsync(user, password)`
4. `UserManager.CheckPasswordAsync` and `SignInManager.CheckPasswordSignInAsync`
5. It validates + supports lockout **without** issuing an Identity cookie
6. No — old token claims until expiry; user must get a new token
7. Roles group users; claims are arbitrary attributes (often per user)
8. JWT bearer for API clients

---

## ✅ What You Should Feel Confident About

- [ ] Add Identity EF Core to a Web API solution
- [ ] Create `AppUser` + `IdentityDbContext` and migrate
- [ ] Register users with safe password hashing and validation options
- [ ] Login with `UserManager` and/or `SignInManager` then issue JWT
- [ ] Enable and test lockout-on-failure behavior
- [ ] Manage roles and user claims
- [ ] Combine Identity membership with bearer authorization attributes

**Previous:** [03-authorization-in-aspnet-core.md](./03-authorization-in-aspnet-core.md)

---

## 🚀 Module 5 Wrap-Up

You can now secure ASP.NET Core Web APIs end-to-end:

| Skill | File |
|-------|------|
| AuthN vs AuthZ, tokens, hashing/salting | 01 |
| JWT anatomy, bearer setup, login issuance, client header | 02 |
| `[Authorize]`, roles, policies, handlers | 03 |
| Identity + `UserManager`/`SignInManager`, roles/claims, register/login + JWT | 04 |

### Secure API checklist
- [ ] HTTPS only in real environments
- [ ] Passwords stored as Identity hashes (never plaintext)
- [ ] Login path records failures / lockout when required
- [ ] JWT signing key outside git
- [ ] Short access-token lifetime
- [ ] `UseAuthentication` before `UseAuthorization`
- [ ] Sensitive actions require roles/policies
- [ ] Ownership rules enforced for user data
- [ ] 401/403 used intentionally
- [ ] No secrets in JWT payloads
- [ ] Role changes reflected on subsequent token issue

### Typical production stack you now understand
```
Client
  → POST /auth/register (UserManager.CreateAsync hashes password)
  → POST /auth/login (SignInManager validates + lockout → JWT)
  → receives JWT (roles/claims)
  → calls API with Bearer token
  → ASP.NET validates JWT
  → [Authorize]/roles/policies gate endpoints
  → services enforce resource rules + EF data access
```

**Suggested next module:** Testing & Quality — unit/integration tests for APIs, test auth handlers, and verifying authorization rules automatically.
