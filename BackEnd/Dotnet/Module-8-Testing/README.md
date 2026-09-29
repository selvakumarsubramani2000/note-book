# Module 8 — Testing

> Validate backend behavior automatically: **unit tests**, **mocks/fakes**, and **ASP.NET Core integration/functional tests**.

**Outcome:** Isolate business logic without real databases, mock repositories and HTTP dependencies with Moq, exercise endpoints through `WebApplicationFactory`, and refactor with a green safety net.

---

## 📚 Contents

| # | File | What you learn |
|---|------|----------------|
| 01 | [01-unit-testing.md](./01-unit-testing.md) | Why automate; xUnit vs NUnit vs MSTest; AAA; Facts/Theories; service/domain tests without SQL |
| 02 | [02-mocking-and-isolation.md](./02-mocking-and-isolation.md) | Test doubles; Moq setup/verify; mock repos & HTTP ports; fakes; pitfalls |
| 03 | [03-integration-and-functional-testing.md](./03-integration-and-functional-testing.md) | `WebApplicationFactory`; EF InMemory & SQLite; validation; authN/authZ test flows |

---

## 🗺️ Learning path

```
01 Unit-test pure logic (xUnit + AAA)
        │
        ▼
02 Isolate dependencies (Moq / fakes)
        │
        ▼
03 Functional-test the API pipeline + data + security
```

### Suggested hands-on build
1. `BankAccount` / `PricingService` unit tests  
2. `ProductService` tests with Moq (happy path + duplicate name)  
3. `Shop.Api.Tests` with `WebApplicationFactory`  
4. Assert 400 validation, 401 anonymous, Admin authorized path  
5. Create-then-get against EF InMemory  

---

## 🔗 Depends on

| Module | Why |
|--------|-----|
| Module 3 — Web API | Controllers, DI, middleware |
| Module 4 — EF Core | Persistence seams for integration tests |
| Module 5 — Auth | 401/403 and roles in functional tests |
| Module 6 — Validation/Errors | Status codes & problem details asserts |

---

## ✅ Completion checklist

- [ ] Choose xUnit for this notebook’s style and run `dotnet test`  
- [ ] Write AAA unit tests for domain/services without a real DB  
- [ ] Mock repositories and external HTTP interfaces with Moq  
- [ ] Verify important interactions (`Times.Once` / `Never`)  
- [ ] Functional-test endpoints with `WebApplicationFactory`  
- [ ] Use InMemory or SQLite for test persistence  
- [ ] Cover authentication and authorization outcomes over HTTP  

---

## ⏭️ Next

Wire `dotnet test` into CI, then consider Testcontainers for real SQL engines and a few smoke E2E journeys for production deploys.
