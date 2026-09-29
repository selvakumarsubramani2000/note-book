# Authentication & Authorization Quick Reference

> **TL;DR**: Authentication = "Who are you?" (login), Authorization = "What can you do?" (permissions). Use JWT tokens for .NET + React apps.

## Core Concepts

### Authentication vs Authorization

| Concept | Question | Example |
|---------|----------|---------|
| **Authentication** | "Who are you?" | Login with email/password |
| **Authorization** | "What can you do?" | Admin can delete users, regular users cannot |

### Session vs Token Authentication

| Feature | Session-Based | Token-Based (JWT) |
|---------|---------------|-------------------|
| **Storage** | Server-side (DB/Redis) | Client-side (localStorage/cookie) |
| **Scalability** | Harder (shared sessions) | Easier (stateless) |
| **Mobile/API** | Not ideal | Perfect |
| **Logout** | Instant (delete session) | Wait for expiration |
| **Best for** | Traditional web apps | SPAs, APIs, mobile |

**Recommendation for .NET + React**: Use **JWT (token-based)**

## JWT Structure

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

[Header].[Payload].[Signature]
```

- **Header**: Algorithm and token type
- **Payload**: User data (claims) - **base64-encoded, NOT encrypted!**
- **Signature**: Ensures token hasn't been tampered with

**⚠️ Never put sensitive data in JWT!** (passwords, credit cards, etc.)

## Authentication Flow

```
1. User registers → Backend hashes password → Saves to DB
2. User logs in → Backend verifies credentials → Generates JWT
3. Frontend stores token (localStorage or cookie)
4. Frontend sends token with every request (Authorization header)
5. Backend validates token → Grants/denies access
6. User logs out → Frontend removes token
```

## .NET Backend Cheat Sheet

### Setup (NuGet Packages)

```bash
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
dotnet add package BCrypt.Net-Next
```

### User Model

```csharp
public class User
{
    public int Id { get; set; }
    public string Email { get; set; }
    public string PasswordHash { get; set; } // Never store plain password!
    public string Name { get; set; }
    public string Role { get; set; } = "User";
}
```

### Generate JWT

```csharp
public string GenerateToken(User user)
{
    var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_secretKey));
    var credentials = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);
    
    var claims = new[]
    {
        new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
        new Claim(ClaimTypes.Email, user.Email),
        new Claim(ClaimTypes.Role, user.Role)
    };
    
    var token = new JwtSecurityToken(
        issuer: "MyApp",
        audience: "MyAppUsers",
        claims: claims,
        expires: DateTime.UtcNow.AddHours(1),
        signingCredentials: credentials
    );
    
    return new JwtSecurityTokenHandler().WriteToken(token);
}
```

### Register Endpoint

```csharp
[HttpPost("register")]
public async Task<IActionResult> Register([FromBody] RegisterRequest request)
{
    // Check if user exists
    if (await _context.Users.AnyAsync(u => u.Email == request.Email))
        return BadRequest("User already exists");
    
    // Hash password
    var passwordHash = BCrypt.Net.BCrypt.HashPassword(request.Password);
    
    // Create user
    var user = new User
    {
        Email = request.Email,
        PasswordHash = passwordHash,
        Name = request.Name
    };
    
    _context.Users.Add(user);
    await _context.SaveChangesAsync();
    
    return Ok(new { message = "User registered" });
}
```

### Login Endpoint

```csharp
[HttpPost("login")]
public async Task<IActionResult> Login([FromBody] LoginRequest request)
{
    // Find user
    var user = await _context.Users.FirstOrDefaultAsync(u => u.Email == request.Email);
    
    // Verify password
    if (user == null || !BCrypt.Net.BCrypt.Verify(request.Password, user.PasswordHash))
        return Unauthorized("Invalid credentials");
    
    // Generate token
    var token = _jwtService.GenerateToken(user);
    
    return Ok(new { token, user = new { user.Id, user.Email, user.Name, user.Role } });
}
```

### Protected Endpoint

```csharp
[Authorize] // Requires authentication
[HttpGet("profile")]
public IActionResult GetProfile()
{
    var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
    // ... fetch and return user data
}

[Authorize(Roles = "Admin")] // Requires Admin role
[HttpDelete("users/{id}")]
public IActionResult DeleteUser(int id)
{
    // Only admins can access
}
```

### Configure JWT in Program.cs

```csharp
// Add authentication
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = "MyApp",
            ValidAudience = "MyAppUsers",
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(secretKey))
        };
    });

// Add CORS
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowReactApp", policy =>
        policy.WithOrigins("http://localhost:3000")
              .AllowAnyHeader()
              .AllowAnyMethod());
});

// In middleware pipeline (ORDER MATTERS!)
app.UseCors("AllowReactApp");
app.UseAuthentication(); // Before Authorization!
app.UseAuthorization();
```

## React Frontend Cheat Sheet

### Setup (npm packages)

```bash
npm install axios react-router-dom
```

### API Service with Axios Interceptor

```javascript
import axios from 'axios';

const api = axios.create({
    baseURL: 'https://localhost:7001/api'
});

// Add token to all requests
api.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Handle 401 errors (token expired)
api.interceptors.response.use(
    response => response,
    error => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default api;
```

### Auth Context

```javascript
import { createContext, useState, useContext } from 'react';

const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);

    const login = async (email, password) => {
        const response = await api.post('/auth/login', { email, password });
        const { token, user } = response.data;
        
        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify(user));
        setUser(user);
    };

    const logout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user }}>
            {children}
        </AuthContext.Provider>
    );
}

export const useAuth = () => useContext(AuthContext);
```

### Login Component

```javascript
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await login(email, password);
            navigate('/profile');
        } catch (error) {
            alert('Login failed');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} />
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
            <button type="submit">Login</button>
        </form>
    );
}
```

### Protected Route

```javascript
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function ProtectedRoute({ children }) {
    const { isAuthenticated } = useAuth();
    
    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }
    
    return children;
}

// Usage in App.jsx
<Route path="/profile" element={
    <ProtectedRoute>
        <Profile />
    </ProtectedRoute>
} />
```

## Authorization Strategies

### 1. Role-Based (RBAC)

```csharp
// Backend
[Authorize(Roles = "Admin")]
[HttpDelete("users/{id}")]
public IActionResult DeleteUser(int id) { ... }
```

```javascript
// Frontend
const { user } = useAuth();
{user?.role === 'Admin' && <button>Delete</button>}
```

### 2. Claims-Based

```csharp
// Backend
builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("CanEditPosts", policy =>
        policy.RequireClaim("CanEditPosts", "true"));
});

[Authorize(Policy = "CanEditPosts")]
[HttpPut("posts/{id}")]
public IActionResult EditPost(int id) { ... }
```

### 3. Resource-Based

```csharp
// Backend
[Authorize]
[HttpPut("posts/{id}")]
public IActionResult EditPost(int id)
{
    var post = _context.Posts.Find(id);
    var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
    
    if (post.AuthorId.ToString() != userId)
        return Forbid(); // 403 Forbidden
    
    // Allow edit
}
```

## Security Checklist

### ✅ DO

- ✅ Use HTTPS (always!)
- ✅ Hash passwords with BCrypt
- ✅ Set token expiration (1 hour max)
- ✅ Use strong secret keys (32+ characters)
- ✅ Validate tokens on backend
- ✅ Implement refresh tokens
- ✅ Use HttpOnly cookies (better than localStorage)
- ✅ Configure CORS properly
- ✅ Validate all user input
- ✅ Implement rate limiting
- ✅ Enforce authorization on backend (never trust frontend!)

### ❌ DON'T

- ❌ Store passwords in plain text
- ❌ Put sensitive data in JWT
- ❌ Use weak secret keys
- ❌ Store tokens in localStorage (XSS risk - use HttpOnly cookies)
- ❌ Make tokens too long-lived
- ❌ Trust client-side authorization
- ❌ Use `.AllowAnyOrigin()` in CORS
- ❌ Skip input validation
- ❌ Ignore token expiration

## Token Storage Comparison

| Storage | Security | Pros | Cons |
|---------|----------|------|------|
| **localStorage** | ❌ XSS vulnerable | Easy to use | Can be stolen by scripts |
| **HttpOnly Cookie** | ✅ Secure | Not accessible to JS | Requires CORS config |
| **Memory only** | ✅ Most secure | Can't be stolen | Lost on refresh |

**Recommendation**: Use **HttpOnly cookies** for production.

## Common Pitfalls

1. **Storing sensitive data in JWT** - JWT is base64-encoded, not encrypted!
2. **Not validating token expiration** - Always set `ValidateLifetime = true`
3. **Weak secret keys** - Use at least 32 random characters
4. **Trusting client-side auth** - Always enforce on backend
5. **Not handling token expiration** - Use axios interceptors

## Quick Start Commands

### Backend (.NET)

```bash
# Create project
dotnet new webapi -n MyApp.API

# Install packages
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
dotnet add package BCrypt.Net-Next

# Create migration
dotnet ef migrations add InitialCreate
dotnet ef database update

# Run
dotnet run
```

### Frontend (React)

```bash
# Create project
npm create vite@latest my-app -- --template react

# Install packages
npm install axios react-router-dom

# Run
npm run dev
```

## Testing

### Test Login (curl)

```bash
# Register
curl -X POST https://localhost:7001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","name":"Test User"}'

# Login
curl -X POST https://localhost:7001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Access protected endpoint
curl -X GET https://localhost:7001/api/user/profile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Resources

- [Microsoft Docs: ASP.NET Core Security](https://docs.microsoft.com/aspnet/core/security/)
- [JWT.io](https://jwt.io) - Decode JWTs
- [OWASP Auth Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [React Router Docs](https://reactrouter.com)

---

**For detailed explanations, see**: [guide-auth-dotnet-react.md](./guide-auth-dotnet-react.md)

