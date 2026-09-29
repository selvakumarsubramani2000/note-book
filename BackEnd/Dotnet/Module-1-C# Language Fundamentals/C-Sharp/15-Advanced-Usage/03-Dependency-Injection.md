# 🔌 Dependency Injection in C#

> **Trainer's Note:** DI means a class does not create all its dependencies itself. Dependencies are provided from outside. This makes code testable and flexible.

---

## 📑 Table of Contents
1. [What is DI?](#1-what-is-di)
2. [Without DI vs With DI](#2-without-di-vs-with-di)
3. [DI in ASP.NET Core (Simple)](#3-di-in-aspnet-core-simple)
4. [Service Lifetimes](#4-service-lifetimes)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is DI?

**Dependency Injection** is a technique where required objects (services) are injected into a class, usually through constructor parameters.

### Real-world analogy
```
Without DI:
  Chef grows vegetables, builds stove, then cooks

With DI:
  Kitchen manager provides stove + ingredients
  Chef focuses on cooking
```

Related principle: Dependency Inversion (depend on abstractions).

---

## 2. Without DI vs With DI

### Tight coupling (hard to test)
```csharp
public class OrderService
{
    private readonly EmailSender _email = new EmailSender(); // fixed concrete type

    public void Place(string orderId) => _email.Send(orderId);
}
```

### Constructor injection (better)
```csharp
public interface IEmailSender
{
    void Send(string message);
}

public class EmailSender : IEmailSender
{
    public void Send(string message) => Console.WriteLine(message);
}

public class OrderService
{
    private readonly IEmailSender _email;

    public OrderService(IEmailSender email)
    {
        _email = email;
    }

    public void Place(string orderId) => _email.Send($"Order {orderId}");
}
```

Now you can inject a fake sender in unit tests.

---

## 3. DI in ASP.NET Core (Simple)

Register services in `Program.cs`:

```csharp
builder.Services.AddScoped<IEmailSender, EmailSender>();
builder.Services.AddScoped<OrderService>();
```

Framework injects them automatically into controllers/services:

```csharp
public class OrdersController : ControllerBase
{
    private readonly OrderService _orders;

    public OrdersController(OrderService orders)
    {
        _orders = orders;
    }
}
```

---

## 4. Service Lifetimes

| Lifetime | Meaning | Typical use |
|----------|---------|-------------|
| **Transient** | new instance every request for it | lightweight stateless helpers |
| **Scoped** | one instance per request scope | EF DbContext, business services in web request |
| **Singleton** | one instance for app lifetime | shared cache/config-style services (careful with state) |

```csharp
builder.Services.AddTransient<ITransient, Transient>();
builder.Services.AddScoped<IScoped, Scoped>();
builder.Services.AddSingleton<ISingleton, Singleton>();
```

### Beginner tips
- Prefer interfaces for replaceable infrastructure (email, payment, storage)
- Don't new up everything inside business classes
- Start with Scoped for many web app services
- Avoid heavy mutable state in Singleton unless designed for thread-safety

---

## 5. Knowledge Check

1. What problem does DI solve?
2. What is constructor injection?
3. Name the 3 common service lifetimes.
4. Why inject `IEmailSender` instead of `new EmailSender()` inside a service?

---

**Previous:** [← HttpClient](./02-REST-API-Calls-with-HttpClient.md)  
**Next:** [Unit Testing →](./04-Unit-Testing-NUnit-xUnit-MSTest.md)
