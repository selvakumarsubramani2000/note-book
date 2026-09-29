# 🔐 Security Basics — AuthN, AuthZ, Tokens & Password Safety

> **Trainer's Note:** Before JWT attributes and Identity packages, lock the mental model. **Authentication** proves identity. **Authorization** decides permissions. Most API security bugs come from mixing these up or storing secrets badly. This file is your foundation.

---

## 📑 Table of Contents
1. [Authentication vs Authorization](#1-authentication-vs-authorization)
2. [Where Security Sits in an API Request](#2-where-security-sits-in-an-api-request)
3. [Stateful vs Stateless Authentication](#3-stateful-vs-stateless-authentication)
4. [Token-Based Architecture](#4-token-based-architecture)
5. [Sessions, Cookies, and APIs (Awareness)](#5-sessions-cookies-and-apis-awareness)
6. [Hashing vs Encryption](#6-hashing-vs-encryption)
7. [Password Salting and Secure Storage](#7-password-salting-and-secure-storage)
8. [Other Backend Crypto Concepts You’ll Hear](#8-other-backend-crypto-concepts-youll-hear)
9. [Security Rules of Thumb for APIs](#9-security-rules-of-thumb-for-apis)
10. [Knowledge Check](#10-knowledge-check)

---

## 1. Authentication vs Authorization

| Term | Question it answers | Example |
|------|---------------------|---------|
| **Authentication (AuthN)** | **Who are you?** | Login with email/password → prove you are `selva@shop.com` |
| **Authorization (AuthZ)** | **What are you allowed to do?** | User is authenticated, but only **Admin** can delete products |

```
Authentication first, authorization second.

  1) Prove identity   →  "I am user 42"
  2) Check permission →  "User 42 may POST /api/products"
```

### Real-world analogy
```
Authentication  = showing your employee badge at the building door
Authorization   = badge lets you into Floor 3, not the server room
```

### HTTP status codes (common mapping)
| Code | Typical meaning in auth flows |
|------|-------------------------------|
| **401 Unauthorized** | Not authenticated (missing/invalid token) — naming is historical |
| **403 Forbidden** | Authenticated, but not allowed |
| **400 Bad Request** | Malformed login input |
| **200/201** | Success |

> Beginners: “Unauthorized” in HTTP often means “unauthenticated.” Yes, the wording is confusing. Focus on **401 = no valid identity**, **403 = identity lacks permission**.

---

## 2. Where Security Sits in an API Request

```
Client
  │  Authorization: Bearer <token>
  ▼
ASP.NET Core pipeline
  ├── Authentication middleware   → builds HttpContext.User
  ├── Authorization middleware    → enforces [Authorize] / policies
  └── Controller / endpoint       → business logic (still re-check sensitive rules)
```

| Layer | Responsibility |
|-------|----------------|
| HTTPS | Encrypt data in transit |
| Authentication | Validate token/cookie → identity |
| Authorization | Roles/policies/resources |
| Application rules | “Can this user edit *this* order?” |
| Database | Least-privilege connection users |

**Never trust the client alone.** UI can hide buttons; API must still enforce access.

---

## 3. Stateful vs Stateless Authentication

### Stateful (server remembers login)
```
Login success → server stores session in memory/DB/Redis
Client sends session id (often cookie)
Each request: server looks up session
```

| Pros | Cons |
|------|------|
| Easy to revoke instantly | Server must store session state |
| Familiar for classic websites | Harder to scale horizontally without shared store |
| | Sticky sessions / session DB complexity |

### Stateless (server does not keep session per user by default)
```
Login success → server issues a signed token
Client sends token every request
Server validates signature + claims (no session lookup required)
```

| Pros | Cons |
|------|------|
| Scales well for APIs | Revocation is harder (need short expiry / blocklist) |
| Fits mobile + SPA + multi-service | Token theft is dangerous until expiry |
| Less server memory for sessions | Must design claims carefully |

**Modern public APIs** often use **stateless JWT bearer tokens** (next file), sometimes with refresh-token strategies.

---

## 4. Token-Based Architecture

```
┌──────────┐   1) POST /api/auth/login (credentials)
│  Client  │ ──────────────────────────────────────► ┌─────────────┐
│ SPA/App  │ ◄────────────────────────────────────── │  Your API   │
└──────────┘   2) access token (JWT)                  └─────────────┘
     │
     │  3) GET /api/orders
     │     Header: Authorization: Bearer eyJhbGciOi...
     ▼
┌─────────────┐
│  Your API   │  4) validate token → set User → authorize → return data
└─────────────┘
```

### Main pieces
| Piece | Role |
|-------|------|
| **Credentials** | Prove identity at login (password, OTP, external IdP) |
| **Access token** | Short-lived proof for API calls |
| **Refresh token** (optional) | Longer-lived credential to get new access tokens |
| **Claims** | Statements inside token: user id, roles, email |
| **Signing key** | Server secret/private key to prevent forgery |

### Why APIs love tokens
- Same token works for browser SPA, mobile app, another backend  
- No server-side session *required* for basic validation  
- Natural fit with `Authorization` header  

---

## 5. Sessions, Cookies, and APIs (Awareness)

| Style | Common in | Client sends |
|-------|-----------|--------------|
| Cookie session | Server-rendered websites | Cookie automatically |
| JWT in header | SPAs, mobile, pure Web APIs | `Authorization: Bearer ...` |
| JWT in cookie | Some web apps (careful with CSRF) | Cookie |

For **this notebook’s Web API path**, prefer:

```
Authorization: Bearer <access-token>
```

Cookie auth is a valid advanced topic (SameSite, CSRF). Master bearer tokens first.

---

## 6. Hashing vs Encryption

These are **not** the same.

| | **Hashing** | **Encryption** |
|--|-------------|----------------|
| Purpose | One-way fingerprint | Hide data so it can be revealed later |
| Reversible? | **No** (by design) | **Yes** (with key) |
| Typical use | Passwords, integrity checks | Secrets at rest, sensitive fields |
| Key? | Not for simple hash; password hashing uses salt/pepper strategies | Requires key management |
| Example algorithms | SHA-256 (general), bcrypt/argon2/PBKDF2 (passwords) | AES |

```
Password "Nexus@123"
    │
    ▼  password hash function + salt
Stored: "v2.argon2id$....randomsalt....hash..."

You cannot get the original password back from the hash.
You only verify: hash(input + salt) == stored_hash
```

### Wrong mental model
```
❌ encrypt password with AES and store ciphertext
   (if AES key leaks, all passwords decrypt)

✅ store slow, salted password hashes
```

### Hashing ≠ “encoding”
Base64 is **encoding**, not security. Anyone can decode it.

---

## 7. Password Salting and Secure Storage

### Why plain hashing without salt fails
Attackers use **rainbow tables** (precomputed hash → password maps).

If two users share `Password1` and you store unsalted SHA-256, both hashes match → easier bulk compromise.

### Salt
A **salt** is random data unique per password:

```
hash(password + salt) → store (salt, hash, algorithm parameters)
```

| Benefit | Explanation |
|---------|-------------|
| Unique hashes | Same password → different stored values |
| Breaks rainbow tables | Precomputed lists become useless per salt |
| Per-user randomness | One cracked password doesn’t unlock identical hashes |

### Pepper (awareness)
A **pepper** is an app-level secret added to hashing, stored separately from DB. Optional hardening; Identity handles modern defaults for beginners.

### What “secure storage” means in practice
1. **Never store plaintext passwords**  
2. Use a **password hashing algorithm** designed to be slow (bcrypt, PBKDF2, Argon2, scrypt)  
3. Store algorithm version + salt + hash  
4. Use constant-time compare for verification (framework does this)  
5. Enforce password policies (length, breach lists later)  
6. Protect the database and backups like they contain gold  

### ASP.NET Core Identity note
Identity’s `PasswordHasher` already does modern salted password hashing for you. Prefer it over inventing crypto.

```
You:   userManager.CreateAsync(user, password)
Identity: hashes password safely → stores hash on user record
```

### Timing and brute force
- Slow hash algorithms slow down password guessing  
- Add rate limiting / lockouts on login endpoints  
- HTTPS always  

---

## 8. Other Backend Crypto Concepts You’ll Hear

| Concept | Simple meaning | API relevance |
|---------|----------------|---------------|
| **HTTPS / TLS** | Encrypts traffic on the wire | Mandatory for login/tokens |
| **Symmetric key** | Same key signs/encrypts and verifies | JWT HMAC (`HS256`) signing key |
| **Asymmetric keys** | Private signs, public verifies | JWT RSA/ECDSA; multi-service validation |
| **Digital signature** | Proves token wasn’t tampered | JWT signature section |
| **Random tokens** | Unpredictable values | Refresh tokens, reset links |
| **Secret management** | Keys not in git | User secrets, env, vault |

### Signing vs encryption of JWTs
Most access tokens are **signed** (integrity + authenticity), not encrypted. Payload is Base64-readable — **do not put passwords or secrets in JWT claims**.

```
JWT payload is readable to anyone who has the token.
Sign it so nobody can modify it.
Encrypt only if you have a special need (uncommon for basic APIs).
```

---

## 9. Security Rules of Thumb for APIs

1. Authenticate identity; authorize every sensitive action  
2. Use HTTPS everywhere  
3. Short-lived access tokens; rotate signing keys thoughtfully  
4. Least privilege roles/policies  
5. Never log passwords, tokens, or connection strings  
6. Validate input even for authenticated users  
7. Enforce authZ in API + critical domain rules (not UI only)  
8. Store password hashes, not passwords  
9. Keep secrets in vault/env/user-secrets — never source control  
10. Assume tokens can leak → expiry + HTTPS + careful XSS protection on clients  

```
Defense in depth:

  Transport security (HTTPS)
    + strong authn (credentials/token validation)
    + authz (roles/policies/resources)
    + validated input
    + least-privilege DB
    + logging/monitoring/alerts
```

---

## 10. Knowledge Check

**Q1.** In one sentence each, define authentication and authorization.  
**Q2.** A valid login token is sent, but the user cannot delete a product. Is that usually AuthN or AuthZ failure? Which status code is typical?  
**Q3.** What makes token-based API auth “stateless” in the common case?  
**Q4.** Hashing vs encryption — which is reversible with a key?  
**Q5.** Why salt passwords?  
**Q6.** Why must you not put secrets in a JWT payload?  
**Q7.** Why is Base64 not a password storage strategy?

### Mini practice
Write a one-page design note for a shop API:
1. Public endpoints (catalog list)  
2. Authenticated endpoints (place order)  
3. Admin-only endpoints (delete product)  
4. How passwords are stored  
5. How the client sends proof after login  

### Answers (short)
1. AuthN = who you are; AuthZ = what you can do  
2. Authorization; often 403  
3. Server validates signed token claims without session store lookup  
4. Encryption  
5. Unique per-user randomness defeats rainbow tables and identical-hash leaks  
6. JWT payload is readable; only signature prevents tampering  
7. Encoding is reversible and not a hash  

---

## ✅ What You Should Feel Confident About

- [ ] Clearly separate AuthN vs AuthZ  
- [ ] Explain 401 vs 403 at a practical level  
- [ ] Describe stateful vs stateless auth trade-offs  
- [ ] Sketch token-based API flow  
- [ ] Distinguish hashing, encryption, and encoding  
- [ ] Explain salt + secure password storage habits  

**Next:** [02-jwt-authentication.md](./02-jwt-authentication.md) — JWT structure, ASP.NET Core bearer setup, login & issuing tokens.
