# Question 20: What is the difference between authentication and authorization?

## Answer

### Simple Explanation

**Authentication** = **"Who are you?"** (Verifying identity)  
**Authorization** = **"What can you do?"** (Verifying permissions)

Think of it like entering a building:
- **Authentication**: Showing your ID card at the entrance (proving who you are)
- **Authorization**: The ID card determines which floors you can access (what you're allowed to do)

---

## Authentication

### What is Authentication?

**Authentication** is the process of verifying the identity of a user. It answers the question: "Are you who you claim to be?"

### How It Works

```
User sends credentials (username + password)
    ↓
System verifies credentials
    ↓
If valid: User is authenticated
    ↓
System issues a token/cookie
    ↓
User sends token with subsequent requests
```

### Common Authentication Methods

1. **Basic Authentication** - Username and password in every request
2. **Token-based Authentication** - JWT (JSON Web Token)
3. **OAuth 2.0** - Third-party authentication (Google, Facebook)
4. **Cookie-based Authentication** - Session cookies
5. **Multi-factor Authentication (MFA)** - Password + SMS/Email code

---

### Authentication Example in .NET Core

#### JWT Token Authentication

```csharp
// 1. Configure in Startup.cs
public void ConfigureServices(IServiceCollection services)
{
    services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
        .AddJwtBearer(options =>
        {
            options.TokenValidationParameters = new TokenValidationParameters
            {
                ValidateIssuer = true,
                ValidateAudience = true,
                ValidateLifetime = true,
                ValidateIssuerSigningKey = true,
                ValidIssuer = Configuration["Jwt:Issuer"],
                ValidAudience = Configuration["Jwt:Audience"],
                IssuerSigningKey = new SymmetricSecurityKey(
                    Encoding.UTF8.GetBytes(Configuration["Jwt:Key"]))
            };
        });
}

public void Configure(IApplicationBuilder app)
{
    app.UseRouting();
    app.UseAuthentication(); // Must come before UseAuthorization
    app.UseAuthorization();
    app.UseEndpoints(endpoints => endpoints.MapControllers());
}

// 2. Login endpoint - Issues JWT token
[ApiController]
[Route("api/[controller]")]
public class AuthController : ControllerBase
{
    [HttpPost("login")]
    public IActionResult Login([FromBody] LoginRequest request)
    {
        // Validate credentials (check database)
        if (request.Username == "john" && request.Password == "password123")
        {
            var token = GenerateJwtToken(request.Username);
            return Ok(new { Token = token });
        }
        
        return Unauthorized("Invalid credentials");
    }
    
    private string GenerateJwtToken(string username)
    {
        var securityKey = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes(_configuration["Jwt:Key"]));
        var credentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha256);
        
        var claims = new[]
        {
            new Claim(JwtRegisteredClaimNames.Sub, username),
            new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString()),
            new Claim(ClaimTypes.Name, username)
        };
        
        var token = new JwtSecurityToken(
            issuer: _configuration["Jwt:Issuer"],
            audience: _configuration["Jwt:Audience"],
            claims: claims,
            expires: DateTime.Now.AddHours(1),
            signingCredentials: credentials);
        
        return new JwtSecurityTokenHandler().WriteToken(token);
    }
}

// 3. Protected endpoint - Requires authentication
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    [Authorize] // Requires authentication
    [HttpGet]
    public IActionResult GetProducts()
    {
        var username = User.Identity.Name; // Get authenticated user's name
        return Ok($"Products for {username}");
    }
}
```

**Request Flow:**
```
1. POST /api/auth/login
   Body: { "username": "john", "password": "password123" }
   Response: { "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." }

2. GET /api/products
   Header: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   Response: 200 OK - "Products for john"

3. GET /api/products (without token)
   Response: 401 Unauthorized
```

---

## Authorization

### What is Authorization?

**Authorization** is the process of determining what an authenticated user is allowed to do. It answers: "What permissions do you have?"

### Key Concepts

1. **Roles** - User belongs to groups (Admin, User, Manager)
2. **Claims** - Key-value pairs about the user (email, age, department)
3. **Policies** - Complex rules combining roles and claims

---

### Authorization Examples

#### 1. Role-Based Authorization

```csharp
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    [HttpGet]
    [Authorize] // Any authenticated user
    public IActionResult GetAll()
    {
        return Ok("All products");
    }
    
    [HttpPost]
    [Authorize(Roles = "Admin,Manager")] // Only Admin or Manager
    public IActionResult Create([FromBody] Product product)
    {
        return Ok("Product created");
    }
    
    [HttpDelete("{id}")]
    [Authorize(Roles = "Admin")] // Only Admin
    public IActionResult Delete(int id)
    {
        return Ok("Product deleted");
    }
}
```

#### 2. Claims-Based Authorization

```csharp
// In Startup.cs - Configure authorization policies
public void ConfigureServices(IServiceCollection services)
{
    services.AddAuthorization(options =>
    {
        options.AddPolicy("MinimumAge18", policy =>
            policy.RequireClaim("Age", "18", "19", "20"...)); // Must be 18+
        
        options.AddPolicy("AdminOnly", policy =>
            policy.RequireRole("Admin"));
        
        options.AddPolicy("EmployeeId", policy =>
            policy.RequireClaim("EmployeeNumber"));
    });
}

// Usage in controller
[Authorize(Policy = "MinimumAge18")]
[HttpPost("purchase")]
public IActionResult PurchaseAlcohol()
{
    return Ok("Purchase allowed");
}
```

#### 3. Custom Policy-Based Authorization

```csharp
// Custom requirement
public class MinimumAgeRequirement : IAuthorizationRequirement
{
    public int MinimumAge { get; }
    
    public MinimumAgeRequirement(int minimumAge)
    {
        MinimumAge = minimumAge;
    }
}

// Custom handler
public class MinimumAgeHandler : AuthorizationHandler<MinimumAgeRequirement>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        MinimumAgeRequirement requirement)
    {
        var ageClaim = context.User.FindFirst(c => c.Type == "Age");
        
        if (ageClaim != null && int.TryParse(ageClaim.Value, out int age))
        {
            if (age >= requirement.MinimumAge)
            {
                context.Succeed(requirement);
            }
        }
        
        return Task.CompletedTask;
    }
}

// Register in Startup.cs
public void ConfigureServices(IServiceCollection services)
{
    services.AddSingleton<IAuthorizationHandler, MinimumAgeHandler>();
    
    services.AddAuthorization(options =>
    {
        options.AddPolicy("AtLeast18", policy =>
            policy.Requirements.Add(new MinimumAgeRequirement(18)));
    });
}

// Usage
[Authorize(Policy = "AtLeast18")]
[HttpGet("adult-content")]
public IActionResult GetAdultContent()
{
    return Ok("Adult content");
}
```

---

## Key Differences Table

| Aspect | Authentication | Authorization |
|--------|---------------|---------------|
| **Question** | "Who are you?" | "What can you do?" |
| **Purpose** | Verify identity | Verify permissions |
| **When** | First (login) | After authentication |
| **Output** | Token/Cookie | Access decision (Allow/Deny) |
| **Failure** | 401 Unauthorized | 403 Forbidden |
| **Example** | Login with username/password | Admin can delete, User cannot |
| **Attribute** | N/A (automatic via token) | `[Authorize(Roles = "Admin")]` |

---

## Real-World Example: E-Commerce System

```csharp
[ApiController]
[Route("api/[controller]")]
public class OrdersController : ControllerBase
{
    // Anyone can view their own orders (must be authenticated)
    [HttpGet("my-orders")]
    [Authorize] // Authentication required
    public IActionResult GetMyOrders()
    {
        var userId = User.FindFirst(ClaimTypes.NameIdentifier).Value;
        return Ok($"Orders for user {userId}");
    }
    
    // Only managers can view all orders
    [HttpGet("all")]
    [Authorize(Roles = "Manager,Admin")] // Authorization: Role check
    public IActionResult GetAllOrders()
    {
        return Ok("All orders");
    }
    
    // Only admins can delete orders
    [HttpDelete("{id}")]
    [Authorize(Roles = "Admin")] // Authorization: Admin only
    public IActionResult DeleteOrder(int id)
    {
        return Ok($"Order {id} deleted");
    }
    
    // Only the order owner or admin can cancel
    [HttpPost("{id}/cancel")]
    [Authorize] // Authentication required
    public IActionResult CancelOrder(int id)
    {
        var userId = User.FindFirst(ClaimTypes.NameIdentifier).Value;
        var isAdmin = User.IsInRole("Admin");
        
        // Custom authorization logic
        if (OrderBelongsToUser(id, userId) || isAdmin)
        {
            return Ok("Order cancelled");
        }
        
        return Forbid(); // 403 Forbidden
    }
    
    private bool OrderBelongsToUser(int orderId, string userId)
    {
        // Check database
        return true;
    }
}
```

**Request Examples:**
```
1. User "john" logs in:
   POST /api/auth/login → Gets token
   
2. John views his orders:
   GET /api/orders/my-orders (with token)
   ✅ Authentication: Pass (valid token)
   ✅ Authorization: Pass (any authenticated user allowed)
   Response: 200 OK

3. John tries to view all orders:
   GET /api/orders/all (with token)
   ✅ Authentication: Pass (valid token)
   ❌ Authorization: Fail (not Manager/Admin)
   Response: 403 Forbidden

4. Admin views all orders:
   GET /api/orders/all (with admin token)
   ✅ Authentication: Pass (valid token)
   ✅ Authorization: Pass (is Admin)
   Response: 200 OK

5. Unauthorized user tries to access:
   GET /api/orders/my-orders (no token)
   ❌ Authentication: Fail (no token)
   Response: 401 Unauthorized
```

---

## HTTP Status Codes

- **401 Unauthorized** - Authentication failed (identity not verified)
  - Missing token
  - Invalid token
  - Expired token

- **403 Forbidden** - Authorization failed (permission denied)
  - Valid identity, but insufficient permissions
  - Wrong role
  - Policy not satisfied

---

## Summary

**Authentication** (Identity):
- ✅ Verifies WHO you are
- ✅ Uses credentials (username/password, token)
- ✅ Happens first
- ❌ Failure → 401 Unauthorized

**Authorization** (Permissions):
- ✅ Verifies WHAT you can do
- ✅ Uses roles, claims, policies
- ✅ Happens after authentication
- ❌ Failure → 403 Forbidden

**Always remember:** You must be **authenticated** before you can be **authorized**!
