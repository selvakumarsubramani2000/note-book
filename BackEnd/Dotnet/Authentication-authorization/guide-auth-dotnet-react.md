# Authentication & Authorization: Complete Guide for .NET + React

> **Last Updated**: January 12, 2026  
> **Difficulty Level**: Beginner to Intermediate  
> **Estimated Time**: 60 minutes  
> **Tech Stack**: ASP.NET Core 8.0 + React 18

## Overview

This comprehensive guide teaches you everything you need to know about implementing secure authentication and authorization in a modern web application with .NET backend and React frontend. Whether you're building a simple login system or a complex enterprise application, this guide covers the fundamentals and best practices.

## Prerequisites

Before starting, you should be familiar with:
- [ ] C# and ASP.NET Core basics
- [ ] React fundamentals (components, hooks, useState, useEffect)
- [ ] HTTP requests and REST APIs
- [ ] Basic understanding of JSON

**No prior authentication experience required!** This guide assumes you're new to auth.

## Learning Objectives

By the end of this guide, you will be able to:
1. Explain the difference between authentication and authorization
2. Understand how JWT (JSON Web Tokens) work
3. Implement user registration and login in .NET
4. Secure your .NET API endpoints
5. Build login/register forms in React
6. Manage authentication state in React
7. Implement protected routes in React
8. Handle token storage and refresh
9. Implement role-based authorization
10. Follow security best practices

---

## Table of Contents

1. [Fundamentals](#fundamentals)
2. [Authentication vs Authorization](#authentication-vs-authorization)
3. [Session-based vs Token-based Authentication](#session-based-vs-token-based-authentication)
4. [Understanding JWT](#understanding-jwt)
5. [The Authentication Flow](#the-authentication-flow)
6. [.NET Backend Implementation](#net-backend-implementation)
7. [React Frontend Implementation](#react-frontend-implementation)
8. [Authorization Strategies](#authorization-strategies)
9. [Security Best Practices](#security-best-practices)
10. [Common Pitfalls](#common-pitfalls)
11. [Testing Authentication](#testing-authentication)
12. [Summary](#summary)
13. [Next Steps](#next-steps)

---

## Fundamentals

### What is Authentication?

**Authentication** answers the question: **"Who are you?"**

It's the process of verifying that a user is who they claim to be.

**Real-world analogy**: Showing your ID at airport security. You prove your identity with a passport or driver's license.

**In web apps**:
- User provides credentials (username/password)
- System verifies credentials against stored data
- System confirms identity

**Examples**:
- Logging in with email and password
- Logging in with Google/Facebook (OAuth)
- Biometric authentication (fingerprint, face ID)
- Two-factor authentication (2FA)

### What is Authorization?

**Authorization** answers the question: **"What can you do?"**

It's the process of determining what an authenticated user is allowed to access or do.

**Real-world analogy**: Your employee badge gets you into the building (authentication), but only certain rooms based on your role (authorization).

**In web apps**:
- User is already authenticated
- System checks user's permissions/roles
- System grants or denies access to resources

**Examples**:
- Admin can delete users, regular users cannot
- Users can only edit their own posts
- Premium subscribers can access exclusive content

### Key Difference

```
Authentication: "You are John Doe" ✅
Authorization: "John Doe can access Admin Panel" ✅ or ❌
```

**Important**: You must authenticate before you can authorize. You can't determine what someone can do until you know who they are.

---

## Authentication vs Authorization

Let's see this in action with a practical example:

### Example Scenario: Blog Application

**Authentication**:
```
User visits /login
User enters: email="john@example.com", password="secret123"
System checks database: Does this user exist? Is password correct?
✅ Yes → User is authenticated as "John Doe"
❌ No → Show error "Invalid credentials"
```

**Authorization**:
```
Authenticated user "John Doe" tries to access /admin/users
System checks: Does John have "Admin" role?
✅ Yes → Show admin panel
❌ No → Show error "403 Forbidden"

Authenticated user "John Doe" tries to edit post #42
System checks: Is John the author of post #42?
✅ Yes → Allow editing
❌ No → Show error "You can only edit your own posts"
```

### In Code

**Authentication** (Backend):
```csharp
// Login endpoint
[HttpPost("login")]
public IActionResult Login([FromBody] LoginRequest request)
{
    // 1. Find user by email
    var user = _context.Users.FirstOrDefault(u => u.Email == request.Email);
    
    // 2. Verify password
    if (user == null || !VerifyPassword(request.Password, user.PasswordHash))
    {
        return Unauthorized("Invalid credentials");
    }
    
    // 3. User is authenticated! Generate token
    var token = GenerateJwtToken(user);
    return Ok(new { token, user.Email, user.Name });
}
```

**Authorization** (Backend):
```csharp
// Protected endpoint - requires authentication
[Authorize] // Must be logged in
[HttpGet("profile")]
public IActionResult GetProfile()
{
    var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
    var user = _context.Users.Find(userId);
    return Ok(user);
}

// Admin-only endpoint - requires specific role
[Authorize(Roles = "Admin")] // Must be logged in AND have Admin role
[HttpDelete("users/{id}")]
public IActionResult DeleteUser(int id)
{
    // Only admins can delete users
    var user = _context.Users.Find(id);
    _context.Users.Remove(user);
    _context.SaveChanges();
    return Ok();
}
```

---

## Session-based vs Token-based Authentication

There are two main approaches to authentication in web applications. Understanding the difference is crucial for choosing the right approach.

### Session-based Authentication (Traditional)

**How it works**:
1. User logs in with credentials
2. Server creates a session and stores it (in memory, database, or Redis)
3. Server sends session ID to client as a cookie
4. Client sends cookie with every request
5. Server looks up session to verify user

**Diagram**:
```
Client                          Server
  |                               |
  |-- Login (email, password) --> |
  |                               | Create session in database
  |                               | Session ID: "abc123"
  | <-- Set-Cookie: session=abc123|
  |                               |
  |-- GET /profile -------------> |
  |    Cookie: session=abc123     | Look up session "abc123"
  |                               | Find user from session
  | <-- User data ---------------|
```

**Pros**:
- ✅ Server has full control (can invalidate sessions instantly)
- ✅ More secure (session data stored server-side)
- ✅ Easy to implement logout (just delete session)

**Cons**:
- ❌ Requires server-side storage (memory/database)
- ❌ Harder to scale (session must be shared across servers)
- ❌ Not ideal for mobile apps or APIs
- ❌ CSRF vulnerability (need CSRF tokens)

### Token-based Authentication (Modern)

**How it works**:
1. User logs in with credentials
2. Server generates a JWT (JSON Web Token)
3. Server sends JWT to client
4. Client stores JWT (localStorage, sessionStorage, or cookie)
5. Client sends JWT with every request (in Authorization header)
6. Server verifies JWT signature (no database lookup needed)

**Diagram**:
```
Client                          Server
  |                               |
  |-- Login (email, password) --> |
  |                               | Verify credentials
  |                               | Generate JWT token
  | <-- { token: "eyJhbG..." } ---|
  |                               |
  | Store token in localStorage   |
  |                               |
  |-- GET /profile -------------> |
  |    Authorization: Bearer eyJ..| Verify JWT signature
  |                               | Extract user info from token
  | <-- User data ---------------|
```

**Pros**:
- ✅ Stateless (no server-side storage needed)
- ✅ Scalable (works across multiple servers)
- ✅ Perfect for APIs and mobile apps
- ✅ Works across different domains (CORS-friendly)

**Cons**:
- ❌ Can't invalidate tokens easily (must wait for expiration)
- ❌ Token size larger than session ID
- ❌ If token is stolen, attacker has access until expiration
- ❌ Need refresh token strategy for long sessions

### Which Should You Use?

**For .NET + React apps in 2026**: **Token-based (JWT)** is the standard choice because:
- Modern SPAs (Single Page Applications) work better with tokens
- Easier to scale and deploy
- Works well with microservices
- Industry standard for APIs

**Use session-based if**:
- You need instant logout/session invalidation
- You're building a traditional server-rendered app
- You have strict security requirements

**For this guide, we'll use JWT (token-based) authentication.**

---

## Understanding JWT

### What is JWT?

**JWT (JSON Web Token)** is a compact, URL-safe token format used for securely transmitting information between parties.

**Structure**: A JWT consists of three parts separated by dots (`.`):

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

[Header].[Payload].[Signature]
```

### JWT Parts Explained

#### 1. Header
Contains metadata about the token:
```json
{
  "alg": "HS256",  // Algorithm used for signing
  "typ": "JWT"     // Token type
}
```

#### 2. Payload
Contains the claims (user data):
```json
{
  "sub": "1234567890",           // Subject (user ID)
  "name": "John Doe",            // User name
  "email": "john@example.com",   // User email
  "role": "Admin",               // User role
  "iat": 1516239022,             // Issued at (timestamp)
  "exp": 1516242622              // Expiration (timestamp)
}
```

**Important**: The payload is **base64-encoded, not encrypted**. Anyone can decode and read it. Don't put sensitive data (passwords, credit cards) in JWT!

#### 3. Signature
Ensures the token hasn't been tampered with:
```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

The signature is created using:
- The encoded header
- The encoded payload
- A secret key (only known to the server)

**Why it's secure**: Without the secret key, attackers can't create valid signatures. If they modify the payload, the signature won't match, and the server will reject the token.

### How JWT Works in Practice

**1. User Logs In**:
```csharp
// Server generates JWT
var token = new JwtSecurityToken(
    issuer: "your-app",
    audience: "your-app-users",
    claims: new[]
    {
        new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
        new Claim(ClaimTypes.Email, user.Email),
        new Claim(ClaimTypes.Role, user.Role)
    },
    expires: DateTime.UtcNow.AddHours(1),
    signingCredentials: new SigningCredentials(secretKey, SecurityAlgorithms.HmacSha256)
);

var tokenString = new JwtSecurityTokenHandler().WriteToken(token);
// Returns: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**2. Client Stores Token**:
```javascript
// React frontend
localStorage.setItem('token', tokenString);
```

**3. Client Sends Token with Requests**:
```javascript
// React frontend
axios.get('/api/profile', {
    headers: {
        'Authorization': `Bearer ${token}`
    }
});
```

**4. Server Validates Token**:
```csharp
// ASP.NET Core automatically validates:
// - Signature (using secret key)
// - Expiration (exp claim)
// - Issuer and audience (if configured)

[Authorize] // This attribute triggers JWT validation
[HttpGet("profile")]
public IActionResult GetProfile()
{
    // If we reach here, token is valid
    var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
    // ...
}
```

### JWT Claims

**Claims** are key-value pairs in the JWT payload that describe the user.

**Standard claims**:
- `sub` (subject): User ID
- `iat` (issued at): When token was created
- `exp` (expiration): When token expires
- `iss` (issuer): Who created the token
- `aud` (audience): Who the token is for

**Custom claims**:
```csharp
new Claim(ClaimTypes.Email, "john@example.com"),
new Claim(ClaimTypes.Role, "Admin"),
new Claim("department", "Engineering"),
new Claim("subscription", "Premium")
```

You can add any data you need for authorization decisions.

### JWT Security Considerations

**✅ DO**:
- Use HTTPS (always!)
- Set short expiration times (15 minutes to 1 hour)
- Use refresh tokens for long sessions
- Store secret key securely (environment variables, Azure Key Vault)
- Validate signature, expiration, issuer, audience

**❌ DON'T**:
- Put sensitive data in JWT (it's readable!)
- Use weak secret keys
- Store JWT in localStorage if XSS is a concern (use HttpOnly cookies instead)
- Make tokens too long-lived
- Share secret key across environments

---

## The Authentication Flow

Let's walk through the complete authentication flow from login to accessing protected resources.

### Complete Flow Diagram

```
┌─────────────┐                                    ┌─────────────┐
│   React     │                                    │  .NET API   │
│  Frontend   │                                    │   Backend   │
└─────────────┘                                    └─────────────┘
       │                                                   │
       │  1. POST /api/auth/register                      │
       │     { email, password, name }                    │
       │──────────────────────────────────────────────────>│
       │                                                   │ Hash password
       │                                                   │ Save user to DB
       │  2. { message: "User created" }                  │
       │<──────────────────────────────────────────────────│
       │                                                   │
       │  3. POST /api/auth/login                         │
       │     { email, password }                          │
       │──────────────────────────────────────────────────>│
       │                                                   │ Verify credentials
       │                                                   │ Generate JWT
       │  4. { token: "eyJhbG...", user: {...} }          │
       │<──────────────────────────────────────────────────│
       │                                                   │
       │  Store token in localStorage                     │
       │  Update auth state (user logged in)              │
       │                                                   │
       │  5. GET /api/profile                             │
       │     Authorization: Bearer eyJhbG...              │
       │──────────────────────────────────────────────────>│
       │                                                   │ Validate JWT
       │                                                   │ Extract user ID
       │                                                   │ Fetch user data
       │  6. { id, email, name, role }                    │
       │<──────────────────────────────────────────────────│
       │                                                   │
       │  7. POST /api/admin/users (Admin only)           │
       │     Authorization: Bearer eyJhbG...              │
       │──────────────────────────────────────────────────>│
       │                                                   │ Validate JWT
       │                                                   │ Check role claim
       │                                                   │ ❌ Not admin
       │  8. 403 Forbidden                                │
       │<──────────────────────────────────────────────────│
       │                                                   │
       │  9. POST /api/auth/logout                        │
       │──────────────────────────────────────────────────>│
       │                                                   │ (Optional: blacklist token)
       │  10. { message: "Logged out" }                   │
       │<──────────────────────────────────────────────────│
       │                                                   │
       │  Remove token from localStorage                  │
       │  Update auth state (user logged out)             │
       │                                                   │
```

### Step-by-Step Explanation

**Step 1-2: Registration**
- User fills out registration form
- Frontend sends email, password, name to backend
- Backend hashes password and saves user to database
- Returns success message

**Step 3-4: Login**
- User enters credentials
- Backend verifies email and password
- Backend generates JWT containing user info
- Frontend receives token and user data

**Step 5: Store Token**
- Frontend stores token in localStorage (or sessionStorage, or HttpOnly cookie)
- Frontend updates application state (user is now logged in)
- Frontend can now make authenticated requests

**Step 6-7: Access Protected Resources**
- Frontend sends token in `Authorization` header with every request
- Backend validates token automatically (via `[Authorize]` attribute)
- If valid, backend processes request
- If invalid or expired, backend returns 401 Unauthorized

**Step 8-9: Authorization Check**
- Some endpoints require specific roles
- Backend checks role claim in JWT
- If user doesn't have required role, returns 403 Forbidden

**Step 10-11: Logout**
- Frontend removes token from storage
- Frontend updates state (user logged out)
- Optionally, backend can blacklist the token (requires database)

---

## .NET Backend Implementation

Now let's build the backend! We'll create a complete authentication system step by step.

### Project Setup

**1. Create new ASP.NET Core Web API project**:
```bash
dotnet new webapi -n MyApp.API
cd MyApp.API
```

**2. Install required NuGet packages**:
```bash
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
dotnet add package Microsoft.EntityFrameworkCore.Tools
dotnet add package BCrypt.Net-Next
```

**Packages explained**:
- `JwtBearer`: JWT authentication middleware
- `EntityFrameworkCore`: Database access
- `BCrypt.Net-Next`: Password hashing

### Database Models

**Create `Models/User.cs`**:
```csharp
using System.ComponentModel.DataAnnotations;

namespace MyApp.API.Models
{
    public class User
    {
        public int Id { get; set; }

        [Required]
        [EmailAddress]
        public string Email { get; set; } = string.Empty;

        [Required]
        public string PasswordHash { get; set; } = string.Empty;

        [Required]
        public string Name { get; set; } = string.Empty;

        public string Role { get; set; } = "User"; // Default role

        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    }
}
```

**Create `Data/ApplicationDbContext.cs`**:
```csharp
using Microsoft.EntityFrameworkCore;
using MyApp.API.Models;

namespace MyApp.API.Data
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
        }

        public DbSet<User> Users { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Ensure email is unique
            modelBuilder.Entity<User>()
                .HasIndex(u => u.Email)
                .IsUnique();
        }
    }
}
```

### DTOs (Data Transfer Objects)

**Create `DTOs/AuthDTOs.cs`**:
```csharp
using System.ComponentModel.DataAnnotations;

namespace MyApp.API.DTOs
{
    public class RegisterRequest
    {
        [Required]
        [EmailAddress]
        public string Email { get; set; } = string.Empty;

        [Required]
        [MinLength(6, ErrorMessage = "Password must be at least 6 characters")]
        public string Password { get; set; } = string.Empty;

        [Required]
        public string Name { get; set; } = string.Empty;
    }

    public class LoginRequest
    {
        [Required]
        [EmailAddress]
        public string Email { get; set; } = string.Empty;

        [Required]
        public string Password { get; set; } = string.Empty;
    }

    public class AuthResponse
    {
        public string Token { get; set; } = string.Empty;
        public UserDto User { get; set; } = null!;
    }

    public class UserDto
    {
        public int Id { get; set; }
        public string Email { get; set; } = string.Empty;
        public string Name { get; set; } = string.Empty;
        public string Role { get; set; } = string.Empty;
    }
}
```

**Why DTOs?**
- Separate internal models from API contracts
- Don't expose sensitive data (like PasswordHash)
- Validate input data
- Control what data is sent/received

### JWT Service

**Create `Services/IJwtService.cs`**:
```csharp
using MyApp.API.Models;

namespace MyApp.API.Services
{
    public interface IJwtService
    {
        string GenerateToken(User user);
    }
}
```

**Create `Services/JwtService.cs`**:
```csharp
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.IdentityModel.Tokens;
using MyApp.API.Models;

namespace MyApp.API.Services
{
    public class JwtService : IJwtService
    {
        private readonly IConfiguration _configuration;

        public JwtService(IConfiguration configuration)
        {
            _configuration = configuration;
        }

        public string GenerateToken(User user)
        {
            // Get secret key from configuration
            var secretKey = _configuration["Jwt:SecretKey"]
                ?? throw new InvalidOperationException("JWT secret key not configured");

            var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(secretKey));
            var credentials = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

            // Create claims
            var claims = new[]
            {
                new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
                new Claim(ClaimTypes.Email, user.Email),
                new Claim(ClaimTypes.Name, user.Name),
                new Claim(ClaimTypes.Role, user.Role)
            };

            // Create token
            var token = new JwtSecurityToken(
                issuer: _configuration["Jwt:Issuer"],
                audience: _configuration["Jwt:Audience"],
                claims: claims,
                expires: DateTime.UtcNow.AddHours(1), // Token valid for 1 hour
                signingCredentials: credentials
            );

            return new JwtSecurityTokenHandler().WriteToken(token);
        }
    }
}
```

### Authentication Controller

**Create `Controllers/AuthController.cs`**:
```csharp
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using MyApp.API.Data;
using MyApp.API.DTOs;
using MyApp.API.Models;
using MyApp.API.Services;
using BCrypt.Net;

namespace MyApp.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class AuthController : ControllerBase
    {
        private readonly ApplicationDbContext _context;
        private readonly IJwtService _jwtService;

        public AuthController(ApplicationDbContext context, IJwtService jwtService)
        {
            _context = context;
            _jwtService = jwtService;
        }

        // POST: api/auth/register
        [HttpPost("register")]
        public async Task<IActionResult> Register([FromBody] RegisterRequest request)
        {
            // Check if user already exists
            if (await _context.Users.AnyAsync(u => u.Email == request.Email))
            {
                return BadRequest(new { message = "User with this email already exists" });
            }

            // Hash password
            var passwordHash = BCrypt.Net.BCrypt.HashPassword(request.Password);

            // Create user
            var user = new User
            {
                Email = request.Email,
                PasswordHash = passwordHash,
                Name = request.Name,
                Role = "User" // Default role
            };

            _context.Users.Add(user);
            await _context.SaveChangesAsync();

            return Ok(new { message = "User registered successfully" });
        }

        // POST: api/auth/login
        [HttpPost("login")]
        public async Task<IActionResult> Login([FromBody] LoginRequest request)
        {
            // Find user by email
            var user = await _context.Users
                .FirstOrDefaultAsync(u => u.Email == request.Email);

            // Verify user exists and password is correct
            if (user == null || !BCrypt.Net.BCrypt.Verify(request.Password, user.PasswordHash))
            {
                return Unauthorized(new { message = "Invalid email or password" });
            }

            // Generate JWT token
            var token = _jwtService.GenerateToken(user);

            // Return token and user info
            var response = new AuthResponse
            {
                Token = token,
                User = new UserDto
                {
                    Id = user.Id,
                    Email = user.Email,
                    Name = user.Name,
                    Role = user.Role
                }
            };

            return Ok(response);
        }
    }
}
```

**Key points**:
- `Register`: Checks if email exists, hashes password with BCrypt, saves user
- `Login`: Verifies credentials, generates JWT, returns token and user info
- **Never store plain-text passwords!** Always hash with BCrypt or similar
- Return appropriate HTTP status codes (200 OK, 400 Bad Request, 401 Unauthorized)

### Protected Controller Example

**Create `Controllers/UserController.cs`**:
```csharp
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using MyApp.API.Data;
using MyApp.API.DTOs;
using System.Security.Claims;

namespace MyApp.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize] // All endpoints require authentication
    public class UserController : ControllerBase
    {
        private readonly ApplicationDbContext _context;

        public UserController(ApplicationDbContext context)
        {
            _context = context;
        }

        // GET: api/user/profile
        [HttpGet("profile")]
        public async Task<IActionResult> GetProfile()
        {
            // Get user ID from JWT claims
            var userIdClaim = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;

            if (userIdClaim == null)
            {
                return Unauthorized();
            }

            var userId = int.Parse(userIdClaim);
            var user = await _context.Users.FindAsync(userId);

            if (user == null)
            {
                return NotFound();
            }

            return Ok(new UserDto
            {
                Id = user.Id,
                Email = user.Email,
                Name = user.Name,
                Role = user.Role
            });
        }

        // PUT: api/user/profile
        [HttpPut("profile")]
        public async Task<IActionResult> UpdateProfile([FromBody] UpdateProfileRequest request)
        {
            var userIdClaim = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
            if (userIdClaim == null) return Unauthorized();

            var userId = int.Parse(userIdClaim);
            var user = await _context.Users.FindAsync(userId);

            if (user == null) return NotFound();

            // Update user
            user.Name = request.Name;
            await _context.SaveChangesAsync();

            return Ok(new { message = "Profile updated successfully" });
        }

        // GET: api/user/all (Admin only)
        [HttpGet("all")]
        [Authorize(Roles = "Admin")] // Only admins can access
        public async Task<IActionResult> GetAllUsers()
        {
            var users = await _context.Users
                .Select(u => new UserDto
                {
                    Id = u.Id,
                    Email = u.Email,
                    Name = u.Name,
                    Role = u.Role
                })
                .ToListAsync();

            return Ok(users);
        }
    }
}

// Add this DTO to DTOs/AuthDTOs.cs
public class UpdateProfileRequest
{
    [Required]
    public string Name { get; set; } = string.Empty;
}
```

### Configuration (Program.cs)

**Update `Program.cs`**:
```csharp
using System.Text;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using MyApp.API.Data;
using MyApp.API.Services;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Database
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// JWT Service
builder.Services.AddScoped<IJwtService, JwtService>();

// Authentication
var jwtSettings = builder.Configuration.GetSection("Jwt");
var secretKey = jwtSettings["SecretKey"] ?? throw new InvalidOperationException("JWT secret key not configured");

builder.Services.AddAuthentication(options =>
{
    options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
})
.AddJwtBearer(options =>
{
    options.TokenValidationParameters = new TokenValidationParameters
    {
        ValidateIssuer = true,
        ValidateAudience = true,
        ValidateLifetime = true,
        ValidateIssuerSigningKey = true,
        ValidIssuer = jwtSettings["Issuer"],
        ValidAudience = jwtSettings["Audience"],
        IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(secretKey)),
        ClockSkew = TimeSpan.Zero // Remove default 5 minute tolerance
    };
});

builder.Services.AddAuthorization();

// CORS (allow React frontend)
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowReactApp", policy =>
    {
        policy.WithOrigins("http://localhost:3000", "http://localhost:5173") // React dev servers
              .AllowAnyHeader()
              .AllowAnyMethod()
              .AllowCredentials();
    });
});

var app = builder.Build();

// Configure the HTTP request pipeline
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseCors("AllowReactApp"); // Must be before Authentication/Authorization

app.UseAuthentication(); // Must be before Authorization
app.UseAuthorization();

app.MapControllers();

app.Run();
```

**Important order**:
1. `UseCors` - Handle CORS first
2. `UseAuthentication` - Validate JWT
3. `UseAuthorization` - Check permissions
4. `MapControllers` - Route to controllers

### Configuration File (appsettings.json)

**Update `appsettings.json`**:
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\mssqllocaldb;Database=MyAppDb;Trusted_Connection=true;MultipleActiveResultSets=true"
  },
  "Jwt": {
    "SecretKey": "YourSuperSecretKeyThatIsAtLeast32CharactersLong!",
    "Issuer": "MyApp.API",
    "Audience": "MyApp.Users"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*"
}
```

**⚠️ Security Warning**:
- **Never commit secret keys to source control!**
- Use environment variables or Azure Key Vault in production
- Generate a strong random key (at least 32 characters)

### Database Migration

**Create and apply migration**:
```bash
dotnet ef migrations add InitialCreate
dotnet ef database update
```

### Testing the Backend

**1. Run the API**:
```bash
dotnet run
```

**2. Test with curl or Postman**:

**Register**:
```bash
curl -X POST https://localhost:7001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123",
    "name": "John Doe"
  }'
```

**Login**:
```bash
curl -X POST https://localhost:7001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

**Response**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "john@example.com",
    "name": "John Doe",
    "role": "User"
  }
}
```

**Access Protected Endpoint**:
```bash
curl -X GET https://localhost:7001/api/user/profile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## React Frontend Implementation

Now let's build the React frontend to consume our authentication API.

### Project Setup

**1. Create React app with Vite**:
```bash
npm create vite@latest my-app-frontend -- --template react
cd my-app-frontend
npm install
```

**2. Install dependencies**:
```bash
npm install axios react-router-dom
```

**Packages**:
- `axios`: HTTP client for API calls
- `react-router-dom`: Routing and protected routes

### Project Structure

```
src/
├── components/
│   ├── Login.jsx
│   ├── Register.jsx
│   ├── Profile.jsx
│   └── ProtectedRoute.jsx
├── context/
│   └── AuthContext.jsx
├── services/
│   └── api.js
├── App.jsx
└── main.jsx
```

### API Service

**Create `src/services/api.js`**:
```javascript
import axios from 'axios';

const API_URL = 'https://localhost:7001/api';

// Create axios instance
const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json'
    }
});

// Add token to requests automatically
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Handle 401 errors (token expired)
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Token expired or invalid
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// Auth API calls
export const authAPI = {
    register: (email, password, name) =>
        api.post('/auth/register', { email, password, name }),

    login: (email, password) =>
        api.post('/auth/login', { email, password }),
};

// User API calls
export const userAPI = {
    getProfile: () => api.get('/user/profile'),

    updateProfile: (name) => api.put('/user/profile', { name }),

    getAllUsers: () => api.get('/user/all'), // Admin only
};

export default api;
```

**Key features**:
- **Request interceptor**: Automatically adds JWT token to all requests
- **Response interceptor**: Handles 401 errors (expired tokens) by redirecting to login
- **Centralized API calls**: All API logic in one place

### Auth Context

**Create `src/context/AuthContext.jsx`**:
```javascript
import { createContext, useState, useContext, useEffect } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // Load user from localStorage on mount
    useEffect(() => {
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            setUser(JSON.parse(storedUser));
        }
        setLoading(false);
    }, []);

    const login = async (email, password) => {
        try {
            const response = await authAPI.login(email, password);
            const { token, user } = response.data;

            // Store token and user
            localStorage.setItem('token', token);
            localStorage.setItem('user', JSON.stringify(user));
            setUser(user);

            return { success: true };
        } catch (error) {
            return {
                success: false,
                error: error.response?.data?.message || 'Login failed'
            };
        }
    };

    const register = async (email, password, name) => {
        try {
            await authAPI.register(email, password, name);
            return { success: true };
        } catch (error) {
            return {
                success: false,
                error: error.response?.data?.message || 'Registration failed'
            };
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        setUser(null);
    };

    const value = {
        user,
        login,
        register,
        logout,
        isAuthenticated: !!user,
        isAdmin: user?.role === 'Admin'
    };

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};

// Custom hook to use auth context
export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider');
    }
    return context;
};
```

**What this does**:
- Manages authentication state globally
- Provides `login`, `register`, `logout` functions
- Persists user data in localStorage
- Provides `isAuthenticated` and `isAdmin` helpers

### Login Component

**Create `src/components/Login.jsx`**:
```javascript
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        const result = await login(email, password);

        if (result.success) {
            navigate('/profile');
        } else {
            setError(result.error);
        }

        setLoading(false);
    };

    return (
        <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px' }}>
            <h2>Login</h2>

            {error && (
                <div style={{ color: 'red', marginBottom: '10px' }}>
                    {error}
                </div>
            )}

            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: '15px' }}>
                    <label>Email:</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        style={{ width: '100%', padding: '8px' }}
                    />
                </div>

                <div style={{ marginBottom: '15px' }}>
                    <label>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        style={{ width: '100%', padding: '8px' }}
                    />
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    style={{ width: '100%', padding: '10px' }}
                >
                    {loading ? 'Logging in...' : 'Login'}
                </button>
            </form>

            <p style={{ marginTop: '15px' }}>
                Don't have an account? <Link to="/register">Register</Link>
            </p>
        </div>
    );
}
```

### Register Component

**Create `src/components/Register.jsx`**:
```javascript
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Register() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [name, setName] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const { register } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        const result = await register(email, password, name);

        if (result.success) {
            alert('Registration successful! Please login.');
            navigate('/login');
        } else {
            setError(result.error);
        }

        setLoading(false);
    };

    return (
        <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px' }}>
            <h2>Register</h2>

            {error && (
                <div style={{ color: 'red', marginBottom: '10px' }}>
                    {error}
                </div>
            )}

            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: '15px' }}>
                    <label>Name:</label>
                    <input
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        required
                        style={{ width: '100%', padding: '8px' }}
                    />
                </div>

                <div style={{ marginBottom: '15px' }}>
                    <label>Email:</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        style={{ width: '100%', padding: '8px' }}
                    />
                </div>

                <div style={{ marginBottom: '15px' }}>
                    <label>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        minLength="6"
                        style={{ width: '100%', padding: '8px' }}
                    />
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    style={{ width: '100%', padding: '10px' }}
                >
                    {loading ? 'Registering...' : 'Register'}
                </button>
            </form>

            <p style={{ marginTop: '15px' }}>
                Already have an account? <Link to="/login">Login</Link>
            </p>
        </div>
    );
}
```

### Profile Component

**Create `src/components/Profile.jsx`**:
```javascript
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export default function Profile() {
    const { user, logout, isAdmin } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <div style={{ maxWidth: '600px', margin: '50px auto', padding: '20px' }}>
            <h2>Profile</h2>

            <div style={{ marginBottom: '20px' }}>
                <p><strong>Name:</strong> {user?.name}</p>
                <p><strong>Email:</strong> {user?.email}</p>
                <p><strong>Role:</strong> {user?.role}</p>
                {isAdmin && (
                    <p style={{ color: 'green' }}>✅ You have admin privileges</p>
                )}
            </div>

            <button
                onClick={handleLogout}
                style={{ padding: '10px 20px' }}
            >
                Logout
            </button>
        </div>
    );
}
```

### Protected Route Component

**Create `src/components/ProtectedRoute.jsx`**:
```javascript
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function ProtectedRoute({ children, requireAdmin = false }) {
    const { isAuthenticated, isAdmin } = useAuth();

    if (!isAuthenticated) {
        // Not logged in, redirect to login
        return <Navigate to="/login" replace />;
    }

    if (requireAdmin && !isAdmin) {
        // Logged in but not admin, redirect to profile
        return <Navigate to="/profile" replace />;
    }

    // Authorized, render the component
    return children;
}
```

**Usage**:
```javascript
// Protect any route
<Route path="/profile" element={
    <ProtectedRoute>
        <Profile />
    </ProtectedRoute>
} />

// Admin-only route
<Route path="/admin" element={
    <ProtectedRoute requireAdmin={true}>
        <AdminPanel />
    </ProtectedRoute>
} />
```

### App Component

**Update `src/App.jsx`**:
```javascript
import { BrowserRouter, Routes, Route, Navigate, Link } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './components/Login';
import Register from './components/Register';
import Profile from './components/Profile';
import ProtectedRoute from './components/ProtectedRoute';

function Navigation() {
    const { isAuthenticated, user } = useAuth();

    return (
        <nav style={{ padding: '10px', background: '#f0f0f0', marginBottom: '20px' }}>
            <Link to="/" style={{ marginRight: '15px' }}>Home</Link>
            {!isAuthenticated ? (
                <>
                    <Link to="/login" style={{ marginRight: '15px' }}>Login</Link>
                    <Link to="/register">Register</Link>
                </>
            ) : (
                <>
                    <Link to="/profile" style={{ marginRight: '15px' }}>Profile</Link>
                    <span>Welcome, {user?.name}!</span>
                </>
            )}
        </nav>
    );
}

function Home() {
    const { isAuthenticated } = useAuth();

    return (
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
            <h1>Welcome to My App</h1>
            {!isAuthenticated ? (
                <p>Please <Link to="/login">login</Link> or <Link to="/register">register</Link></p>
            ) : (
                <p>You are logged in! Go to your <Link to="/profile">profile</Link></p>
            )}
        </div>
    );
}

function App() {
    return (
        <BrowserRouter>
            <AuthProvider>
                <Navigation />
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route
                        path="/profile"
                        element={
                            <ProtectedRoute>
                                <Profile />
                            </ProtectedRoute>
                        }
                    />
                    <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
            </AuthProvider>
        </BrowserRouter>
    );
}

export default App;
```

### Running the React App

```bash
npm run dev
```

Visit `http://localhost:5173` and test:
1. Register a new user
2. Login with credentials
3. View profile (protected route)
4. Logout
5. Try accessing `/profile` without logging in (should redirect to login)

---

## Authorization Strategies

Now that we have authentication working, let's explore different authorization approaches.

### 1. Role-Based Authorization (RBAC)

**What it is**: Users are assigned roles (Admin, User, Guest), and access is granted based on roles.

**Backend (.NET)**:
```csharp
// Assign role during registration
user.Role = "User"; // or "Admin", "Moderator", etc.

// Protect endpoint with role
[Authorize(Roles = "Admin")]
[HttpDelete("users/{id}")]
public IActionResult DeleteUser(int id) { ... }

// Multiple roles
[Authorize(Roles = "Admin,Moderator")]
[HttpPost("posts/{id}/approve")]
public IActionResult ApprovePost(int id) { ... }
```

**Frontend (React)**:
```javascript
const { isAdmin } = useAuth();

{isAdmin && (
    <button onClick={deleteUser}>Delete User</button>
)}
```

**Pros**: Simple, easy to understand
**Cons**: Not flexible for complex permissions

### 2. Claims-Based Authorization

**What it is**: Users have specific claims (permissions), and access is granted based on claims.

**Backend (.NET)**:
```csharp
// Add claims during token generation
var claims = new[]
{
    new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
    new Claim(ClaimTypes.Email, user.Email),
    new Claim("CanEditPosts", "true"),
    new Claim("CanDeleteComments", "true"),
    new Claim("Department", "Engineering")
};

// Protect endpoint with policy
builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("CanEditPosts", policy =>
        policy.RequireClaim("CanEditPosts", "true"));
});

[Authorize(Policy = "CanEditPosts")]
[HttpPut("posts/{id}")]
public IActionResult EditPost(int id) { ... }
```

**Pros**: Very flexible, fine-grained control
**Cons**: More complex to manage

### 3. Resource-Based Authorization

**What it is**: Access depends on the specific resource (e.g., users can only edit their own posts).

**Backend (.NET)**:
```csharp
[Authorize]
[HttpPut("posts/{id}")]
public async Task<IActionResult> EditPost(int id, [FromBody] UpdatePostRequest request)
{
    var post = await _context.Posts.FindAsync(id);
    if (post == null) return NotFound();

    // Check if user owns the post
    var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
    if (post.AuthorId.ToString() != userId)
    {
        return Forbid(); // 403 Forbidden
    }

    // User owns the post, allow edit
    post.Title = request.Title;
    post.Content = request.Content;
    await _context.SaveChangesAsync();

    return Ok(post);
}
```

**Pros**: Precise control, secure
**Cons**: Requires custom logic for each resource

---

## Security Best Practices

### 1. Always Use HTTPS

**Why**: JWT tokens are sent in headers. Without HTTPS, they can be intercepted.

**How**:
- Development: ASP.NET Core uses HTTPS by default
- Production: Use SSL/TLS certificates (Let's Encrypt, Azure, AWS)

### 2. Secure Token Storage

**Options**:

| Storage | Security | Pros | Cons |
|---------|----------|------|------|
| **localStorage** | ❌ Vulnerable to XSS | Easy to use | Can be stolen by malicious scripts |
| **sessionStorage** | ❌ Vulnerable to XSS | Cleared on tab close | Can be stolen by malicious scripts |
| **HttpOnly Cookie** | ✅ Secure | Not accessible to JavaScript | Requires CORS configuration |
| **Memory only** | ✅ Most secure | Can't be stolen | Lost on page refresh |

**Recommendation**: Use **HttpOnly cookies** for production.

**Implementation**:
```csharp
// Backend: Set token as HttpOnly cookie
[HttpPost("login")]
public IActionResult Login([FromBody] LoginRequest request)
{
    // ... verify credentials ...

    var token = _jwtService.GenerateToken(user);

    // Set as HttpOnly cookie
    Response.Cookies.Append("token", token, new CookieOptions
    {
        HttpOnly = true,  // Not accessible to JavaScript
        Secure = true,    // Only sent over HTTPS
        SameSite = SameSiteMode.Strict, // CSRF protection
        Expires = DateTimeOffset.UtcNow.AddHours(1)
    });

    return Ok(new { user });
}
```

```javascript
// Frontend: No need to manually handle token
// Browser automatically sends cookie with requests
axios.get('/api/user/profile', {
    withCredentials: true // Important!
});
```

### 3. Token Expiration and Refresh

**Problem**: Short-lived tokens expire quickly, annoying users. Long-lived tokens are security risks.

**Solution**: Use refresh tokens.

**How it works**:
1. Issue short-lived access token (15 min) + long-lived refresh token (7 days)
2. When access token expires, use refresh token to get new access token
3. If refresh token is stolen, it can be revoked

**Implementation** (simplified):
```csharp
// Generate both tokens
var accessToken = GenerateAccessToken(user); // 15 min
var refreshToken = GenerateRefreshToken(); // 7 days

// Store refresh token in database
_context.RefreshTokens.Add(new RefreshToken
{
    Token = refreshToken,
    UserId = user.Id,
    ExpiresAt = DateTime.UtcNow.AddDays(7)
});

// Refresh endpoint
[HttpPost("refresh")]
public IActionResult Refresh([FromBody] string refreshToken)
{
    var storedToken = _context.RefreshTokens
        .FirstOrDefault(t => t.Token == refreshToken && t.ExpiresAt > DateTime.UtcNow);

    if (storedToken == null) return Unauthorized();

    var user = _context.Users.Find(storedToken.UserId);
    var newAccessToken = GenerateAccessToken(user);

    return Ok(new { token = newAccessToken });
}
```

### 4. Password Security

**✅ DO**:
- Hash passwords with BCrypt, Argon2, or PBKDF2
- Use salt (BCrypt does this automatically)
- Enforce minimum password length (8+ characters)
- Validate password strength

**❌ DON'T**:
- Store plain-text passwords
- Use weak hashing (MD5, SHA1)
- Use same salt for all passwords

**Example**:
```csharp
// Hash password
var passwordHash = BCrypt.Net.BCrypt.HashPassword(password);

// Verify password
var isValid = BCrypt.Net.BCrypt.Verify(password, passwordHash);
```

### 5. CORS Configuration

**Why**: Prevent unauthorized domains from accessing your API.

**How**:
```csharp
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowReactApp", policy =>
    {
        policy.WithOrigins("https://myapp.com") // Production domain
              .AllowAnyHeader()
              .AllowAnyMethod()
              .AllowCredentials();
    });
});
```

**⚠️ Never use** `.AllowAnyOrigin()` in production!

### 6. Input Validation

**Always validate user input**:
```csharp
public class RegisterRequest
{
    [Required]
    [EmailAddress]
    public string Email { get; set; }

    [Required]
    [MinLength(6)]
    [RegularExpression(@"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$",
        ErrorMessage = "Password must contain uppercase, lowercase, and number")]
    public string Password { get; set; }
}
```

### 7. Rate Limiting

**Prevent brute-force attacks**:
```csharp
// Install: AspNetCoreRateLimit
builder.Services.AddMemoryCache();
builder.Services.Configure<IpRateLimitOptions>(options =>
{
    options.GeneralRules = new List<RateLimitRule>
    {
        new RateLimitRule
        {
            Endpoint = "POST:/api/auth/login",
            Limit = 5,
            Period = "1m" // 5 attempts per minute
        }
    };
});
```

---

## Common Pitfalls

### 1. Storing Sensitive Data in JWT

**❌ Wrong**:
```csharp
new Claim("password", user.Password) // NEVER!
new Claim("creditCard", user.CreditCard) // NEVER!
```

**✅ Correct**:
```csharp
new Claim(ClaimTypes.NameIdentifier, user.Id.ToString())
new Claim(ClaimTypes.Email, user.Email)
new Claim(ClaimTypes.Role, user.Role)
```

**Remember**: JWT payload is base64-encoded, not encrypted. Anyone can decode and read it.

### 2. Not Validating Token Expiration

**❌ Wrong**:
```csharp
options.TokenValidationParameters = new TokenValidationParameters
{
    ValidateLifetime = false // DON'T DO THIS!
};
```

**✅ Correct**:
```csharp
options.TokenValidationParameters = new TokenValidationParameters
{
    ValidateLifetime = true,
    ClockSkew = TimeSpan.Zero // Remove 5-minute tolerance
};
```

### 3. Weak Secret Keys

**❌ Wrong**:
```json
"Jwt": {
    "SecretKey": "secret" // Too short!
}
```

**✅ Correct**:
```json
"Jwt": {
    "SecretKey": "YourSuperSecretKeyThatIsAtLeast32CharactersLongAndRandomlyGenerated!"
}
```

**Generate strong key**:
```bash
openssl rand -base64 32
```

### 4. Not Handling Token Expiration in Frontend

**❌ Wrong**:
```javascript
// Token expires, user gets 401 errors everywhere
```

**✅ Correct**:
```javascript
// Axios interceptor handles 401
api.interceptors.response.use(
    response => response,
    error => {
        if (error.response?.status === 401) {
            // Try refresh token, or logout
            logout();
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);
```

### 5. Trusting Client-Side Authorization

**❌ Wrong**:
```javascript
// Only hiding UI elements
{user.role === 'Admin' && <button>Delete</button>}
// Attacker can still call API directly!
```

**✅ Correct**:
```javascript
// Hide UI elements
{user.role === 'Admin' && <button>Delete</button>}

// AND protect backend endpoint
[Authorize(Roles = "Admin")]
[HttpDelete("users/{id}")]
public IActionResult DeleteUser(int id) { ... }
```

**Always enforce authorization on the backend!**

---

## Testing Authentication

### Backend Tests

**Test login endpoint**:
```csharp
[Fact]
public async Task Login_WithValidCredentials_ReturnsToken()
{
    // Arrange
    var request = new LoginRequest
    {
        Email = "test@example.com",
        Password = "password123"
    };

    // Act
    var response = await _client.PostAsJsonAsync("/api/auth/login", request);

    // Assert
    response.EnsureSuccessStatusCode();
    var result = await response.Content.ReadFromJsonAsync<AuthResponse>();
    Assert.NotNull(result.Token);
}

[Fact]
public async Task ProtectedEndpoint_WithoutToken_Returns401()
{
    // Act
    var response = await _client.GetAsync("/api/user/profile");

    // Assert
    Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
}
```

### Frontend Tests

**Test login component**:
```javascript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from '../context/AuthContext';
import Login from '../components/Login';

test('login with valid credentials', async () => {
    render(
        <BrowserRouter>
            <AuthProvider>
                <Login />
            </AuthProvider>
        </BrowserRouter>
    );

    fireEvent.change(screen.getByLabelText(/email/i), {
        target: { value: 'test@example.com' }
    });

    fireEvent.change(screen.getByLabelText(/password/i), {
        target: { value: 'password123' }
    });

    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => {
        expect(localStorage.getItem('token')).toBeTruthy();
    });
});
```

---

## Summary

### Key Takeaways

1. **Authentication** verifies identity ("Who are you?"), **Authorization** determines permissions ("What can you do?")

2. **JWT (token-based)** is the modern standard for SPAs and APIs - stateless, scalable, CORS-friendly

3. **Backend (.NET)** handles:
   - Password hashing (BCrypt)
   - JWT generation and validation
   - Protected endpoints with `[Authorize]`
   - Role/claims-based authorization

4. **Frontend (React)** handles:
   - Login/register forms
   - Token storage (localStorage or HttpOnly cookies)
   - Auth context for global state
   - Protected routes
   - Axios interceptors for automatic token handling

5. **Security is critical**:
   - Always use HTTPS
   - Hash passwords
   - Validate tokens
   - Use strong secret keys
   - Implement token expiration
   - Never trust client-side authorization

6. **Common patterns**:
   - Role-based (Admin, User)
   - Claims-based (specific permissions)
   - Resource-based (owner can edit)

### Complete Flow Recap

```
1. User registers → Backend hashes password → Saves to DB
2. User logs in → Backend verifies → Generates JWT → Returns token
3. Frontend stores token → Adds to all requests
4. Backend validates token → Grants/denies access
5. User logs out → Frontend removes token
```

---

## Next Steps

### Immediate Actions

1. **Build the example app**:
   - [ ] Create .NET API with auth endpoints
   - [ ] Create React app with login/register
   - [ ] Test the complete flow

2. **Enhance security**:
   - [ ] Implement refresh tokens
   - [ ] Use HttpOnly cookies instead of localStorage
   - [ ] Add rate limiting
   - [ ] Implement password strength validation

3. **Add features**:
   - [ ] Email verification
   - [ ] Password reset
   - [ ] Two-factor authentication (2FA)
   - [ ] Social login (Google, Facebook)

### Further Learning

**Advanced Topics**:
- OAuth 2.0 and OpenID Connect
- Single Sign-On (SSO)
- Identity providers (Auth0, Azure AD, Keycloak)
- Multi-factor authentication
- Passwordless authentication

**Resources**:
- [Microsoft Docs: ASP.NET Core Security](https://docs.microsoft.com/aspnet/core/security/)
- [JWT.io](https://jwt.io) - Decode and learn about JWTs
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [React Router Documentation](https://reactrouter.com)

### Related Guides

- **Implementation Step-by-Step**: Detailed code walkthrough
- **Security Best Practices**: Deep dive into security
- **OAuth 2.0 Guide**: Third-party authentication
- **Testing Authentication**: Comprehensive testing strategies

---

**Congratulations!** You now understand authentication and authorization fundamentals and can implement a secure auth system in .NET + React. Remember: security is not optional - always follow best practices and keep learning! 🔐
```


