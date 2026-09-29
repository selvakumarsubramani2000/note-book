# 5️⃣ Dependency Inversion Principle (DIP) — Introduction

> **Trainer's Note:** DIP is the principle that makes Dependency Injection (DI) possible. If you've ever wondered "why do we inject interfaces instead of `new`-ing classes directly?" — this is the answer.

---

## 📑 Table of Contents
1. [What is DIP?](#1-what-is-dip)
2. [A Real-World Analogy](#2-a-real-world-analogy)
3. [The Problem — Code Without DIP](#3-the-problem--code-without-dip)
4. [The Solution — Applying DIP](#4-the-solution--applying-dip)
5. [DIP vs Dependency Injection (DI)](#5-dip-vs-dependency-injection-di)
6. [Common Beginner Confusions](#6-common-beginner-confusions)
7. [Knowledge Check](#7-knowledge-check)

---

## 1. What is DIP?

> **"High-level modules should not depend on low-level modules. Both should depend on abstractions."**
> **"Abstractions should not depend on details. Details should depend on abstractions."**

In simple words:
- **High-level module** = your business logic (e.g., `OrderService`)
- **Low-level module** = specific implementation detail (e.g., `SqlServerRepository`, `SmtpEmailSender`)
- Instead of the business logic directly depending on a **specific technology**, both should depend on an **interface (abstraction)**.

---

## 2. A Real-World Analogy

### 🔌 Think of a Laptop Charger

```
❌ WITHOUT DIP — Charger hardwired into the wall:
   Your laptop charger cable is permanently soldered into
   ONE specific wall socket in ONE specific country.
   Travel to another country with a different socket shape?
   You are stuck — the charger cannot adapt.

✅ WITH DIP — Standard charging port (like USB-C):
   Your laptop has a STANDARD port (abstraction).
   Any charger (from any brand, any country, with a plug adapter)
   that fits the USB-C standard can power your laptop.
   The laptop doesn't care WHICH specific charger brand you use —
   it only cares that it follows the USB-C "contract."
```

Your business logic should be like the laptop: it depends on a **standard port (interface)**, not a specific brand of charger (concrete class).

---

## 3. The Problem — Code Without DIP

```csharp
// ❌ BAD: High-level class directly depends on a LOW-LEVEL, CONCRETE class
public class SqlServerRepository
{
    public void Save(string data)
    {
        Console.WriteLine($"Saving '{data}' to SQL Server...");
    }
}

public class OrderService // high-level business logic
{
    private readonly SqlServerRepository _repository = new SqlServerRepository();

    public void PlaceOrder(string orderData)
    {
        // ... business rules ...
        _repository.Save(orderData);
    }
}
```

**Why this is bad:**
- `OrderService` (business logic) is **tightly coupled** to `SqlServerRepository` (a specific database technology)
- Want to switch to MongoDB or write unit tests with a fake repository? You must **edit `OrderService`**
- You cannot unit test `OrderService` without a **real SQL Server connection**

---

## 4. The Solution — Applying DIP

Introduce an **abstraction (interface)** that both the high-level and low-level modules depend on:

```csharp
// ✅ GOOD: Abstraction that both sides depend on
public interface IRepository
{
    void Save(string data);
}

// Low-level module depends on the abstraction
public class SqlServerRepository : IRepository
{
    public void Save(string data) => Console.WriteLine($"Saving '{data}' to SQL Server...");
}

// Another low-level module — easy to add without touching business logic
public class MongoDbRepository : IRepository
{
    public void Save(string data) => Console.WriteLine($"Saving '{data}' to MongoDB...");
}

// High-level module depends ONLY on the abstraction, not a specific technology
public class OrderService
{
    private readonly IRepository _repository;

    // The specific implementation is "injected" from outside
    public OrderService(IRepository repository)
    {
        _repository = repository;
    }

    public void PlaceOrder(string orderData)
    {
        // ... business rules ...
        _repository.Save(orderData);
    }
}
```

**Usage:**
```csharp
// Production code
var service = new OrderService(new SqlServerRepository());
service.PlaceOrder("Order #1001");

// Unit test — use a Fake/Mock repository instead of a real database!
var testService = new OrderService(new FakeRepository());
testService.PlaceOrder("Test Order");
```

**Now:**
- `OrderService` no longer cares **which** database technology is used
- Switching from SQL Server to MongoDB = **no changes** to `OrderService`
- Unit testing is easy — just inject a fake/mock `IRepository`

---

## 5. DIP vs Dependency Injection (DI)

These two are related but **not the same thing**:

| | Dependency Inversion Principle (DIP) | Dependency Injection (DI) |
|---|---|---|
| **What it is** | A **design principle** — depend on abstractions, not concrete classes | A **technique** — passing dependencies into a class from the outside |
| **Goal** | Reduce coupling between high-level and low-level modules | Provide the actual dependency instances (via constructor, property, etc.) |
| **Example** | Defining `IRepository` and depending on it | Passing `new SqlServerRepository()` into `OrderService`'s constructor |

> **In short:** DIP is the "why" (the principle). DI is the "how" (the mechanism/technique used to fulfill DIP). In .NET, an **IoC/DI Container** (like the built-in `IServiceCollection`) automates wiring these dependencies together.

---

## 6. Common Beginner Confusions

| Confusion | Clarification |
|-----------|----------------|
| "DIP and DI are the same thing" | ❌ DIP is a principle; DI is a technique that helps achieve it |
| "DIP means avoid using 'new' everywhere" | Partially true for **dependencies you want to swap/test**, not for simple value objects like `new List<T>()` |
| "Interfaces automatically mean DIP is applied" | ❌ You must ensure the **high-level module depends on the interface**, not directly on the concrete class |
| "DIP makes code slower" | ❌ The performance impact is negligible; the benefit (testability, flexibility) is worth it |

---

## 7. Knowledge Check

1. What is the difference between a "high-level module" and a "low-level module"?
2. Why does depending directly on `SqlServerRepository` make unit testing harder?
3. Explain the difference between DIP and Dependency Injection in your own words.
4. How does the "USB-C charger" analogy relate to interfaces in C#?

---

**Previous:** [← Liskov Substitution Principle](./04-Liskov-Substitution-Principle.md)

🎉 **Congratulations!** You've completed the SOLID Principles introduction series. Next step: practice refactoring real code in your own projects using these 5 principles together.
