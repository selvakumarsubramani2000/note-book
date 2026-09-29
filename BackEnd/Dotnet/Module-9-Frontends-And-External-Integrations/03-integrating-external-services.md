# 🔗 Integrating External Services — HttpClient, Resilience & Real-World Patterns

> **Trainer's Note:** Your API will call other APIs — email, payments, identity providers, shipping. Use **`IHttpClientFactory`**, not raw long-lived `new HttpClient()` mistakes. Add **timeouts**, think about **retries**, and keep secrets out of code. This file builds production habits around outbound HTTP.

---

## 📑 Table of Contents
1. [Why Backends Call Other Services](#1-why-backends-call-other-services)
2. [HttpClient Basics](#2-httpclient-basics)
3. [The Socket Exhaustion Problem](#3-the-socket-exhaustion-problem)
4. [IHttpClientFactory](#4-ihttpclientfactory)
5. [Typed Clients](#5-typed-clients)
6. [Timeouts and Cancellation](#6-timeouts-and-cancellation)
7. [Retries and Transient Errors (Polly Concepts)](#7-retries-and-transient-errors-polly-concepts)
8. [Email Integration Pattern](#8-email-integration-pattern)
9. [Payment Gateway Pattern (Conceptual)](#9-payment-gateway-pattern-conceptual)
10. [External Authentication Providers (Conceptual)](#10-external-authentication-providers-conceptual)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. Why Backends Call Other Services

```
Your Shop API
   ├── SQL database
   ├── Email provider API (SendGrid/Mailgun/SES…)
   ├── Payment API (Stripe/PayPal/Razorpay…)
   ├── Identity provider (Google/Microsoft/Auth0…)
   └── Shipping / tax / SMS APIs
```

| Benefit of integration | Risk if done poorly |
|------------------------|---------------------|
| Ship features faster | Cascading failures |
| Specialize vendors | Timeouts freeze threads |
| PCI/email deliverability | Leaked API keys |
| SSO convenience | Brittle auth coupling |

Treat every external call as **unreliable**: slow, failing, rate-limited.

---

## 2. HttpClient Basics

```csharp
// conceptual quick call (not the final pattern)
using var client = new HttpClient();
client.BaseAddress = new Uri("https://api.github.com/");
client.DefaultRequestHeaders.UserAgent.ParseAdd("ShopApi");
var json = await client.GetStringAsync("repos/dotnet/runtime");
```

### Common methods
| Method | Use |
|--------|-----|
| `GetAsync` | Read |
| `PostAsync` | Create/submit |
| `PutAsync` / `PatchAsync` | Update |
| `DeleteAsync` | Delete |
| `SendAsync` | Full control |
| `GetFromJsonAsync` / `PostAsJsonAsync` | JSON helpers |

```csharp
var product = await client.GetFromJsonAsync<ExternalProductDto>(
    $"/v1/products/{id}", ct);

var response = await client.PostAsJsonAsync("/v1/messages", payload, ct);
response.EnsureSuccessStatusCode();
```

Always prefer passing **`CancellationToken`** from the incoming ASP.NET request when the outbound call is per-request.

---

## 3. The Socket Exhaustion Problem

### Anti-pattern
```csharp
public async Task BadAsync()
{
    using var client = new HttpClient(); // created per call in a hot path
    await client.GetAsync("https://example.com");
}
```

Or the opposite extreme:
```csharp
public static readonly HttpClient Client = new(); // better, but static defaults are blunt tools
```

| Problem | Cause |
|---------|-------|
| **Socket exhaustion** | Too many `HttpClient` instances dispose TCP connections poorly under load |
| DNS stickiness issues | Single static client may not refresh DNS as expected historically |
| Inconsistent config | Every call site sets timeouts differently |

**Solution for ASP.NET Core:** `IHttpClientFactory` manages handlers and lifetimes correctly.

---

## 4. IHttpClientFactory

### Register named client
```csharp
builder.Services.AddHttpClient("github", client =>
{
    client.BaseAddress = new Uri("https://api.github.com/");
    client.DefaultRequestHeaders.UserAgent.ParseAdd("ShopApi/1.0");
    client.Timeout = TimeSpan.FromSeconds(30);
});
```

### Consume
```csharp
public class GitHubLookupService
{
    private readonly IHttpClientFactory _factory;

    public GitHubLookupService(IHttpClientFactory factory) => _factory = factory;

    public async Task<string> GetRuntimeAsync(CancellationToken ct)
    {
        var client = _factory.CreateClient("github");
        return await client.GetStringAsync("repos/dotnet/runtime", ct);
    }
}
```

```
Your service
   → IHttpClientFactory.CreateClient("name")
        → pooled HttpMessageHandler (managed)
        → outbound HTTP
```

### Basic “default” client
```csharp
builder.Services.AddHttpClient(); // enables factory
var client = _factory.CreateClient(); // unnamed
```

Prefer **named** or **typed** clients for real integrations.

---

## 5. Typed Clients

A typed client = class that receives `HttpClient` via DI.

```csharp
public class WeatherApiClient
{
    private readonly HttpClient _http;

    public WeatherApiClient(HttpClient http) => _http = http;

    public Task<WeatherDto?> GetAsync(string city, CancellationToken ct)
        => _http.GetFromJsonAsync<WeatherDto>($"/v1/weather?city={Uri.EscapeDataString(city)}", ct);
}

// registration
builder.Services.AddHttpClient<WeatherApiClient>(client =>
{
    client.BaseAddress = new Uri(builder.Configuration["Weather:BaseUrl"]!);
    client.DefaultRequestHeaders.Add("X-Api-Key", builder.Configuration["Weather:ApiKey"]);
    client.Timeout = TimeSpan.FromSeconds(15);
});
```

```csharp
public class StoresController : ControllerBase
{
    private readonly WeatherApiClient _weather;
    public StoresController(WeatherApiClient weather) => _weather = weather;

    [HttpGet("{city}/weather")]
    public async Task<ActionResult<WeatherDto>> Get(string city, CancellationToken ct)
    {
        var dto = await _weather.GetAsync(city, ct);
        return dto is null ? NotFound() : Ok(dto);
    }
}
```

### Secrets
API keys via **config/user-secrets/env/vault** — never hard-code.

---

## 6. Timeouts and Cancellation

### Client timeout
```csharp
client.Timeout = TimeSpan.FromSeconds(10);
```
Covers the overall request operation (default is 100 seconds — often too long for user-facing APIs).

### Request-level cancellation
```csharp
public async Task<IActionResult> PlaceOrder(CancellationToken ct)
{
    // if client disconnects, stop outbound work when possible
    await _payments.ChargeAsync(order, ct);
}
```

### Combined guidance
| Setting | Purpose |
|---------|---------|
| Short HttpClient timeout | Fail fast on stuck dependencies |
| Pass `CancellationToken` | Cooperate with request abort |
| Backend deadlines | Don’t wait forever on payment/email |

Slow external dependencies should not hold every ASP.NET thread indefinitely.

---

## 7. Retries and Transient Errors (Polly Concepts)

**Transient errors** = temporary failures worth retrying:
- network blips  
- `408`, `429`, `500`, `502`, `503`, `504` (choose carefully)  
- timeouts (sometimes)  

**Not transient:**
- `400` validation  
- `401`/`403` auth  
- most `404`s  

### Polly / Microsoft resilience (concept)
Libraries like **Polly** (and newer `Microsoft.Extensions.Http.Resilience`) add policies:

```
retry → short backoff → try again
circuit breaker → stop calling failing dependency temporarily
timeout policy → per-attempt limit
```

> Install resilience packages only with approval. Exact APIs differ by package generation; learn the **ideas** first.

### Conceptual registration (illustrative)
```csharp
// Idea: AddStandardResilienceHandler / AddPolicyHandler patterns
builder.Services.AddHttpClient<PaymentApiClient>(/* ... */)
    .AddStandardResilienceHandler(); // if using Microsoft.Extensions.Http.Resilience
```

### Manual simple retry (teaching only — prefer libraries)
```csharp
for (var attempt = 1; attempt <= 3; attempt++)
{
    try
    {
        var response = await client.SendAsync(request, ct);
        if ((int)response.StatusCode is 408 or 429 or >= 500)
        {
            await Task.Delay(TimeSpan.FromMilliseconds(200 * attempt), ct);
            continue;
        }
        response.EnsureSuccessStatusCode();
        return response;
    }
    catch (HttpRequestException) when (attempt < 3)
    {
        await Task.Delay(TimeSpan.FromMilliseconds(200 * attempt), ct);
    }
}
```

### Retry safety
Only retry **idempotent** operations blindly.  
Retrying `POST /charge` without idempotency keys can **double charge**.

```
Payment retries require provider idempotency keys / careful design
Email send may need de-dupe / outbox
GET retries are usually safer
```

---

## 8. Email Integration Pattern

Don’t open SMTP sockets in every controller action ad hoc.

```
Controller/service
   → IEmailSender
        → EmailApiClient (HttpClient to SendGrid/etc.)
        → or background outbox worker
```

### Interface
```csharp
public interface IEmailSender
{
    Task SendAsync(string to, string subject, string htmlBody, CancellationToken ct = default);
}
```

### Typed client sketch
```csharp
public class SendGridEmailSender : IEmailSender
{
    private readonly HttpClient _http;

    public SendGridEmailSender(HttpClient http) => _http = http;

    public async Task SendAsync(string to, string subject, string htmlBody, CancellationToken ct = default)
    {
        var payload = new
        {
            // provider-specific shape
            personalizations = new[] { new { to = new[] { new { email = to } } } },
            from = new { email = "noreply@shop.local" },
            subject,
            content = new[] { new { type = "text/html", value = htmlBody } }
        };

        using var response = await _http.PostAsJsonAsync("/v3/mail/send", payload, ct);
        response.EnsureSuccessStatusCode();
    }
}

builder.Services.AddHttpClient<IEmailSender, SendGridEmailSender>((sp, client) =>
{
    var cfg = sp.GetRequiredService<IConfiguration>();
    client.BaseAddress = new Uri("https://api.sendgrid.com/");
    client.DefaultRequestHeaders.Authorization =
        new AuthenticationHeaderValue("Bearer", cfg["SendGrid:ApiKey"]);
    client.Timeout = TimeSpan.FromSeconds(15);
});
```

### Reliability upgrade
Use an **outbox table** + background worker (Module 7) so HTTP request returns quickly and emails retry safely.

---

## 9. Payment Gateway Pattern (Conceptual)

```
POST /api/orders/{id}/pay
   → validate order ownership
   → create PaymentIntent on provider (HttpClient)
   → store provider payment id + status
   → return client secret / redirect info to frontend
Webhook POST /api/webhooks/payments
   → verify signature
   → update order paid/failed idempotently
```

### Key design rules
| Rule | Why |
|------|-----|
| Never store raw card numbers | PCI compliance |
| Use official provider SDKs when available | Safer than hand-rolled crypto |
| Idempotency keys | Safe retries |
| Webhooks as source of truth for final status | Client may close browser |
| Verify webhook signatures | Prevent fake “paid” events |
| Timeouts + careful retries | Money is not double-click friendly |

```
Frontend          Your API           Payment Provider
   │  pay             │                    │
   │ ───────────────► │ create intent      │
   │                  │ ─────────────────► │
   │ ◄─ client secret │ ◄───────────────── │
   │ complete UI pay  │                    │
   │                  │ ◄── webhook paid ── │
   │                  │ mark order paid    │
```

Keep payment provider keys in secret stores; rotate on leak.

---

## 10. External Authentication Providers (Conceptual)

Instead of only local username/password, users sign in with Google/Microsoft/GitHub via **OIDC/OAuth2**.

```
Browser
  → your API or BFF challenges external IdP
  → user logs in at Google/Microsoft
  → authorization code / tokens returned
  → your app issues its own session/JWT for APIs
```

### Common ASP.NET pieces
- `AddAuthentication().AddGoogle(...)` / Microsoft / OpenIdConnect  
- Or external products: Auth0, Entra ID, IdentityServer/Duende  

### Backend responsibilities
| Task | Note |
|------|------|
| Validate tokens | Issuer, audience, signature, lifetime |
| Map external user → local user | First login provisioning |
| Store minimal claims | Don’t trust UI claims alone |
| Scopes | Request only what you need |
| Secrets | Client secret in vault |

### SPA note
Many modern setups use:
- Authorization Code + PKCE in the SPA or  
- Backend-for-Frontend (BFF) pattern  

Your Web API still receives a bearer token and applies Module 5 authZ.

---

## 11. Knowledge Check

**Q1.** Why is `new HttpClient()` per request risky under load?  
**Q2.** What does `IHttpClientFactory` improve?  
**Q3.** Typed client vs named client?  
**Q4.** Name two transient vs two non-transient HTTP failures.  
**Q5.** Why are naive retries dangerous for payment charges?  
**Q6.** Outline the email outbox idea in one sentence.  
**Q7.** Why verify payment webhooks?

### Mini practice
1. Register a named or typed `HttpClient` for a public test API  
2. Inject it into a service and call from a controller  
3. Set a 10s timeout and pass `CancellationToken`  
4. Wrap the client behind an interface for unit tests (Module 8)  
5. Design (on paper) order pay + webhook flow with idempotency  
6. Move a fake API key from code into user-secrets  

### Answers (short)
1. Socket exhaustion / poor handler lifetime behavior  
2. Manages handlers, DNS-friendly lifetimes, central config  
3. Typed = DI class with HttpClient; named = string key `CreateClient("x")`  
4. Transient: 503/timeouts; non-transient: 400/401  
5. May create duplicate charges without idempotency  
6. Persist “send email” intent first; worker sends/retries later  
7. Ensure events really came from the provider; update order safely  

---

## ✅ What You Should Feel Confident About

- [ ] Use `IHttpClientFactory` / typed clients instead of naive `HttpClient` lifetimes  
- [ ] Set timeouts and pass cancellation tokens  
- [ ] Explain transient errors and cautious retries  
- [ ] Sketch email, payment, and external login integration flows  
- [ ] Keep provider secrets in configuration stores  
- [ ] Isolate outbound calls behind interfaces for testability  

**Previous:** [02-api-documentation-openapi.md](./02-api-documentation-openapi.md)

---

## 🚀 Module 9 Wrap-Up

You can now connect your backend to the outside world:

| Skill | File |
|-------|------|
| SPA consumption, CORS, stable frontend contracts | 01 |
| OpenAPI/Swagger docs, annotations, live try-it-out | 02 |
| HttpClient factory, resilience ideas, email/pay/auth integrations | 03 |

### Integration-ready checklist
- [ ] CORS policies list real SPA origins (no prod wildcards by habit)  
- [ ] DTOs/status codes stay stable or versioned  
- [ ] OpenAPI published for collaborators  
- [ ] Swagger locked down outside dev as needed  
- [ ] Outbound HTTP via `IHttpClientFactory`  
- [ ] Timeouts + sensible retry/idempotency story  
- [ ] Third-party secrets outside git  
- [ ] Webhooks verified when money/identity are involved  

```
SPA  ──CORS+JSON──►  Your API  ──HttpClient──►  Email/Pay/IdP
         │                     │
         └──── OpenAPI docs ───┘
```

**Suggested next:** Containers & deployment, API gateways, advanced resilience (circuit breakers, bulkheads), and contract testing between frontend and OpenAPI specs.
