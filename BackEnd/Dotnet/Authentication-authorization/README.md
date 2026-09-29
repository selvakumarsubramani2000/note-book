# Authentication & Authorization

Complete guide to implementing secure authentication and authorization in modern web applications.

## 📂 Structure

```
authentication-authorization/
├── 01-fundamentals/           # Core concepts and theory
├── 02-dotnet-react/           # .NET + React implementation
├── 03-security-best-practices/ # Security considerations
└── 04-advanced-topics/        # OAuth, SSO, MFA, etc.
```

## 🎯 Learning Path

### For Beginners
1. Start with `01-fundamentals/` to understand authentication vs authorization
2. Learn the .NET + React implementation in `02-dotnet-react/`
3. Study security best practices in `03-security-best-practices/`
4. Explore advanced topics when ready

## 📚 What You'll Learn

### Fundamentals
- **Authentication vs Authorization**: What's the difference?
- **Session-based vs Token-based**: Pros and cons
- **JWT (JSON Web Tokens)**: How they work
- **OAuth 2.0 & OpenID Connect**: Industry standards
- **Common Auth Flows**: Login, logout, token refresh

### .NET + React Implementation
- **Backend (.NET)**: ASP.NET Core Identity, JWT Bearer authentication
- **Frontend (React)**: Auth context, protected routes, token management
- **Complete Example**: Working login/register system
- **Role-based Authorization**: Implementing RBAC
- **API Security**: Protecting endpoints

### Security Best Practices
- **Token Storage**: HttpOnly cookies vs localStorage
- **HTTPS**: Why it's mandatory
- **Password Security**: Hashing, salting, validation
- **CORS**: Cross-Origin Resource Sharing
- **Common Vulnerabilities**: XSS, CSRF, token theft

### Advanced Topics
- **OAuth 2.0 Providers**: Google, Facebook, GitHub login
- **Single Sign-On (SSO)**: Enterprise authentication
- **Multi-Factor Authentication (MFA)**: Adding extra security
- **Refresh Tokens**: Long-lived sessions
- **Claims-based Authorization**: Fine-grained permissions

## 🚀 Quick Start

**Want to implement auth right away?**
1. Read the [Quick Reference](./02-dotnet-react/quick-reference.md) (10 min)
2. Follow the [Step-by-Step Implementation Guide](./02-dotnet-react/implementation-step-by-step.md) (60 min)
3. Review [Security Checklist](./03-security-best-practices/security-checklist.md) (15 min)

**Want to understand the theory first?**
1. Read the [Comprehensive Guide](./02-dotnet-react/guide-auth-dotnet-react.md) (45 min)
2. Then follow the implementation guide

## 🔑 Key Concepts

### Authentication
**"Who are you?"** - Verifying user identity
- Login with username/password
- Social login (Google, Facebook)
- Biometric authentication

### Authorization
**"What can you do?"** - Determining user permissions
- Role-based (Admin, User, Guest)
- Claims-based (specific permissions)
- Resource-based (owner can edit)

### JWT (JSON Web Token)
**Stateless authentication** - Server doesn't store session
- Encoded token containing user info
- Signed to prevent tampering
- Sent with each request

## 🛠️ Tech Stack Covered

**Backend**:
- ASP.NET Core 8.0+
- Entity Framework Core
- JWT Bearer Authentication
- ASP.NET Core Identity (optional)

**Frontend**:
- React 18+
- React Router v6
- Axios for HTTP requests
- Context API for state management

**Security**:
- HTTPS/TLS
- bcrypt for password hashing
- CORS configuration
- Secure token storage

## 📖 Prerequisites

Before diving in, you should know:
- [ ] C# and .NET basics
- [ ] React fundamentals (components, hooks, state)
- [ ] HTTP basics (requests, responses, headers)
- [ ] Basic understanding of REST APIs

## 🔄 Last Updated

January 2026

