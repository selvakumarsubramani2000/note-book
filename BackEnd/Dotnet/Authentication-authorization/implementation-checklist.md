# Authentication Implementation Checklist

Use this checklist to implement authentication in your .NET + React application step by step.

## Phase 1: Backend Setup (.NET)

### 1.1 Create Project
- [ ] Create new ASP.NET Core Web API project
  ```bash
  dotnet new webapi -n MyApp.API
  cd MyApp.API
  ```

### 1.2 Install NuGet Packages
- [ ] Install JWT Bearer authentication
  ```bash
  dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
  ```
- [ ] Install Entity Framework Core
  ```bash
  dotnet add package Microsoft.EntityFrameworkCore.SqlServer
  dotnet add package Microsoft.EntityFrameworkCore.Tools
  ```
- [ ] Install BCrypt for password hashing
  ```bash
  dotnet add package BCrypt.Net-Next
  ```

### 1.3 Create Database Models
- [ ] Create `Models/User.cs` with properties:
  - `Id` (int)
  - `Email` (string, required, unique)
  - `PasswordHash` (string, required)
  - `Name` (string, required)
  - `Role` (string, default "User")
  - `CreatedAt` (DateTime)

### 1.4 Create Database Context
- [ ] Create `Data/ApplicationDbContext.cs`
- [ ] Add `DbSet<User> Users`
- [ ] Configure unique index on Email

### 1.5 Create DTOs
- [ ] Create `DTOs/AuthDTOs.cs` with:
  - `RegisterRequest` (Email, Password, Name)
  - `LoginRequest` (Email, Password)
  - `AuthResponse` (Token, User)
  - `UserDto` (Id, Email, Name, Role)

### 1.6 Create JWT Service
- [ ] Create `Services/IJwtService.cs` interface
- [ ] Create `Services/JwtService.cs` implementation
- [ ] Implement `GenerateToken(User user)` method
- [ ] Add claims: NameIdentifier, Email, Name, Role
- [ ] Set token expiration (1 hour)

### 1.7 Create Auth Controller
- [ ] Create `Controllers/AuthController.cs`
- [ ] Implement `POST /api/auth/register`:
  - Check if user exists
  - Hash password with BCrypt
  - Save user to database
  - Return success message
- [ ] Implement `POST /api/auth/login`:
  - Find user by email
  - Verify password with BCrypt
  - Generate JWT token
  - Return token and user info

### 1.8 Create Protected Controller
- [ ] Create `Controllers/UserController.cs`
- [ ] Add `[Authorize]` attribute to controller
- [ ] Implement `GET /api/user/profile`:
  - Get user ID from claims
  - Fetch user from database
  - Return user data
- [ ] Implement admin-only endpoint with `[Authorize(Roles = "Admin")]`

### 1.9 Configure JWT Authentication
- [ ] Update `Program.cs`:
  - Add DbContext with connection string
  - Register JwtService
  - Configure Authentication with JwtBearer
  - Set TokenValidationParameters
  - Add Authorization
  - Configure CORS for React app
  - Add middleware in correct order: CORS → Authentication → Authorization

### 1.10 Configure appsettings.json
- [ ] Add connection string
- [ ] Add JWT settings:
  - SecretKey (32+ characters, random)
  - Issuer
  - Audience
- [ ] **⚠️ Add appsettings.json to .gitignore**

### 1.11 Database Migration
- [ ] Create migration:
  ```bash
  dotnet ef migrations add InitialCreate
  ```
- [ ] Update database:
  ```bash
  dotnet ef database update
  ```

### 1.12 Test Backend
- [ ] Run the API:
  ```bash
  dotnet run
  ```
- [ ] Test register endpoint with Postman/curl
- [ ] Test login endpoint
- [ ] Test protected endpoint with token
- [ ] Test protected endpoint without token (should return 401)

---

## Phase 2: Frontend Setup (React)

### 2.1 Create Project
- [ ] Create React app with Vite:
  ```bash
  npm create vite@latest my-app-frontend -- --template react
  cd my-app-frontend
  npm install
  ```

### 2.2 Install Dependencies
- [ ] Install axios:
  ```bash
  npm install axios
  ```
- [ ] Install react-router-dom:
  ```bash
  npm install react-router-dom
  ```

### 2.3 Create Project Structure
- [ ] Create folders:
  - `src/components/`
  - `src/context/`
  - `src/services/`

### 2.4 Create API Service
- [ ] Create `src/services/api.js`
- [ ] Create axios instance with base URL
- [ ] Add request interceptor to attach token
- [ ] Add response interceptor to handle 401 errors
- [ ] Export auth API functions (register, login)
- [ ] Export user API functions (getProfile, updateProfile)

### 2.5 Create Auth Context
- [ ] Create `src/context/AuthContext.jsx`
- [ ] Create AuthContext with createContext
- [ ] Create AuthProvider component with state:
  - `user` (current user)
  - `loading` (initial load)
- [ ] Implement `login(email, password)` function
- [ ] Implement `register(email, password, name)` function
- [ ] Implement `logout()` function
- [ ] Load user from localStorage on mount
- [ ] Export `useAuth()` custom hook

### 2.6 Create Login Component
- [ ] Create `src/components/Login.jsx`
- [ ] Add form with email and password fields
- [ ] Handle form submission
- [ ] Call `login()` from AuthContext
- [ ] Show error messages
- [ ] Redirect to profile on success
- [ ] Add link to register page

### 2.7 Create Register Component
- [ ] Create `src/components/Register.jsx`
- [ ] Add form with name, email, and password fields
- [ ] Handle form submission
- [ ] Call `register()` from AuthContext
- [ ] Show error messages
- [ ] Redirect to login on success
- [ ] Add link to login page

### 2.8 Create Profile Component
- [ ] Create `src/components/Profile.jsx`
- [ ] Display user information (name, email, role)
- [ ] Add logout button
- [ ] Call `logout()` from AuthContext
- [ ] Redirect to login after logout

### 2.9 Create Protected Route Component
- [ ] Create `src/components/ProtectedRoute.jsx`
- [ ] Check if user is authenticated
- [ ] Redirect to login if not authenticated
- [ ] Support `requireAdmin` prop for admin-only routes
- [ ] Render children if authorized

### 2.10 Setup Routing
- [ ] Update `src/App.jsx`:
  - Wrap app with BrowserRouter
  - Wrap app with AuthProvider
  - Create navigation component
  - Add routes:
    - `/` - Home
    - `/login` - Login
    - `/register` - Register
    - `/profile` - Profile (protected)
  - Wrap protected routes with ProtectedRoute

### 2.11 Test Frontend
- [ ] Run the app:
  ```bash
  npm run dev
  ```
- [ ] Test registration flow
- [ ] Test login flow
- [ ] Test accessing protected route without login (should redirect)
- [ ] Test accessing protected route with login (should work)
- [ ] Test logout
- [ ] Test token expiration (wait 1 hour or change expiration to 1 minute)

---

## Phase 3: Security Enhancements

### 3.1 Password Security
- [ ] Add password strength validation (min 8 chars, uppercase, lowercase, number)
- [ ] Add password confirmation field in register form
- [ ] Display password strength indicator

### 3.2 Token Security
- [ ] Consider using HttpOnly cookies instead of localStorage
- [ ] Implement refresh token mechanism
- [ ] Add token blacklist for logout (optional)

### 3.3 Input Validation
- [ ] Add validation attributes to DTOs
- [ ] Add client-side validation in React forms
- [ ] Sanitize user input

### 3.4 Rate Limiting
- [ ] Install AspNetCoreRateLimit package
- [ ] Configure rate limiting for login endpoint (5 attempts per minute)
- [ ] Configure rate limiting for register endpoint

### 3.5 CORS Configuration
- [ ] Update CORS policy to use production domain
- [ ] Remove `AllowAnyOrigin()` if present
- [ ] Test CORS with production URLs

### 3.6 HTTPS
- [ ] Ensure HTTPS is enabled in development
- [ ] Configure SSL certificate for production
- [ ] Add HSTS header

### 3.7 Error Handling
- [ ] Add global error handler in backend
- [ ] Add error boundary in React
- [ ] Don't expose sensitive error details to client

---

## Phase 4: Additional Features (Optional)

### 4.1 Email Verification
- [ ] Add `EmailVerified` field to User model
- [ ] Generate verification token on registration
- [ ] Send verification email
- [ ] Create verification endpoint
- [ ] Prevent login until email is verified

### 4.2 Password Reset
- [ ] Create "Forgot Password" page
- [ ] Generate password reset token
- [ ] Send reset email
- [ ] Create reset password endpoint
- [ ] Create reset password page

### 4.3 Two-Factor Authentication (2FA)
- [ ] Add `TwoFactorEnabled` field to User model
- [ ] Implement TOTP (Time-based One-Time Password)
- [ ] Create 2FA setup page
- [ ] Require 2FA code during login

### 4.4 Social Login
- [ ] Configure OAuth providers (Google, Facebook, GitHub)
- [ ] Add social login buttons
- [ ] Implement OAuth callback handling
- [ ] Link social accounts to existing users

### 4.5 User Management (Admin)
- [ ] Create admin panel
- [ ] List all users
- [ ] Edit user roles
- [ ] Delete users
- [ ] View user activity logs

---

## Phase 5: Testing

### 5.1 Backend Tests
- [ ] Write unit tests for JwtService
- [ ] Write integration tests for AuthController
- [ ] Write integration tests for UserController
- [ ] Test authorization with different roles
- [ ] Test token validation

### 5.2 Frontend Tests
- [ ] Write tests for Login component
- [ ] Write tests for Register component
- [ ] Write tests for AuthContext
- [ ] Write tests for ProtectedRoute
- [ ] Test API service interceptors

---

## Phase 6: Deployment

### 6.1 Backend Deployment
- [ ] Move secrets to environment variables
- [ ] Configure production database
- [ ] Set up CI/CD pipeline
- [ ] Deploy to Azure/AWS/other cloud provider
- [ ] Configure HTTPS certificate
- [ ] Test production API

### 6.2 Frontend Deployment
- [ ] Update API base URL for production
- [ ] Build production bundle:
  ```bash
  npm run build
  ```
- [ ] Deploy to Vercel/Netlify/other hosting
- [ ] Configure environment variables
- [ ] Test production app

### 6.3 Post-Deployment
- [ ] Monitor error logs
- [ ] Set up application insights/monitoring
- [ ] Test all authentication flows in production
- [ ] Perform security audit
- [ ] Set up automated backups

---

## Security Checklist

Before going to production, verify:

- [ ] ✅ HTTPS is enabled
- [ ] ✅ Passwords are hashed with BCrypt
- [ ] ✅ JWT secret key is strong (32+ characters) and stored securely
- [ ] ✅ Token expiration is set (1 hour max)
- [ ] ✅ CORS is configured properly (no `AllowAnyOrigin`)
- [ ] ✅ Input validation is implemented
- [ ] ✅ Rate limiting is enabled
- [ ] ✅ Sensitive data is not in JWT payload
- [ ] ✅ Authorization is enforced on backend (not just frontend)
- [ ] ✅ Error messages don't expose sensitive information
- [ ] ✅ Database connection string is not in source control
- [ ] ✅ API keys and secrets are in environment variables
- [ ] ✅ SQL injection protection (using EF Core parameterized queries)
- [ ] ✅ XSS protection (React escapes by default)
- [ ] ✅ CSRF protection (if using cookies)

---

## Troubleshooting

### Common Issues

**401 Unauthorized on protected endpoints**
- [ ] Check if token is being sent in Authorization header
- [ ] Verify token hasn't expired
- [ ] Check JWT secret key matches between generation and validation
- [ ] Verify issuer and audience match

**CORS errors**
- [ ] Check CORS policy includes React app URL
- [ ] Verify `UseCors()` is before `UseAuthentication()`
- [ ] Check if credentials are allowed if using cookies

**Login fails with correct credentials**
- [ ] Verify password is being hashed correctly
- [ ] Check BCrypt.Verify is comparing correctly
- [ ] Check database has user with that email

**Token not persisting after refresh**
- [ ] Verify token is being saved to localStorage
- [ ] Check AuthContext loads token on mount
- [ ] Verify localStorage is not being cleared

---

## Resources

- [Full Guide](./guide-auth-dotnet-react.md) - Detailed explanations
- [Quick Reference](./quick-reference.md) - Code snippets
- [Microsoft Docs](https://docs.microsoft.com/aspnet/core/security/)
- [JWT.io](https://jwt.io) - Decode and debug JWTs

---

**Estimated Time**: 
- Phase 1 (Backend): 2-3 hours
- Phase 2 (Frontend): 2-3 hours
- Phase 3 (Security): 1-2 hours
- Phase 4 (Optional): 3-5 hours
- Phase 5 (Testing): 2-3 hours
- Phase 6 (Deployment): 1-2 hours

**Total**: 8-12 hours for basic implementation, 15-20 hours with all features.

Good luck! 🚀

