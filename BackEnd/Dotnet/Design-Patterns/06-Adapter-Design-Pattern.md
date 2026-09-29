# 🔌 Adapter Design Pattern (C# / .NET)

> **Trainer's Note:** Adapter is one of the most practical patterns you'll use — especially when working with third-party libraries or legacy code you can't modify.

---

## 📑 Table of Contents
1. [What is the Adapter Pattern?](#1-what-is-the-adapter-pattern)
2. [Real-World Analogy](#2-real-world-analogy)
3. [C# Implementation](#3-c-implementation)
4. [Where Used in Real .NET Projects](#4-where-used-in-real-net-projects)
5. [Common Mistakes](#5-common-mistakes)

---

## 1. What is the Adapter Pattern?

**Adapter** allows two **incompatible interfaces** to work together by wrapping one of them in a new class that "translates" calls between them.

### 🎯 The Problem It Solves

You have an existing class (maybe from a third-party library) whose interface **doesn't match** what your application expects — and you **can't change** that library's code.

```
Your App expects:      INotificationService.Send(string message)
Third-Party Library:   LegacySmsGateway.DispatchSms(string text, string number)

These don't match! You need something in between to "translate".
```

---

## 2. Real-World Analogy

### 🔌 Travel Power Plug Adapter

```
Your laptop charger (US plug) doesn't fit an Indian wall socket.

You don't rebuild your charger or rewire the wall socket.
You use a TRAVEL ADAPTER in between:

[US Plug] ──► [Travel Adapter] ──► [Indian Socket]

The adapter TRANSLATES one shape into another, without
changing either the charger or the socket.
```

**Adapter Pattern = A "translator" class that sits between your code and an incompatible class, so they can work together.**

---

## 3. C# Implementation

### The Problem Setup

```csharp
// Your application's expected interface
public interface INotificationService
{
    void Send(string message);
}

// A third-party SMS library you CANNOT modify
public class LegacySmsGateway
{
    public void DispatchSms(string text, string phoneNumber)
    {
        Console.WriteLine($"SMS to {phoneNumber}: {text}");
    }
}
```

Your app only knows how to call `Send(string message)`, but `LegacySmsGateway` needs `DispatchSms(text, phoneNumber)`. They don't match!

### ✅ The Adapter Solution

```csharp
// The Adapter - implements YOUR interface, wraps the incompatible class
public class SmsNotificationAdapter : INotificationService
{
    private readonly LegacySmsGateway _legacyGateway;
    private readonly string _defaultPhoneNumber;

    public SmsNotificationAdapter(LegacySmsGateway legacyGateway, string defaultPhoneNumber)
    {
        _legacyGateway = legacyGateway;
        _defaultPhoneNumber = defaultPhoneNumber;
    }

    // Translates the call from your interface to the legacy method
    public void Send(string message)
    {
        _legacyGateway.DispatchSms(message, _defaultPhoneNumber);
    }
}
```

### Using It:

```csharp
LegacySmsGateway legacyGateway = new LegacySmsGateway();
INotificationService notifier = new SmsNotificationAdapter(legacyGateway, "9999999999");

// Your app just calls Send() - doesn't know or care about LegacySmsGateway!
notifier.Send("Your order has been shipped!");
// Output: SMS to 9999999999: Your order has been shipped!
```

### 💡 Why This Works
- ✅ Your app code only depends on `INotificationService` (clean, testable)
- ✅ You never touched or modified `LegacySmsGateway`
- ✅ You can swap in `EmailNotificationAdapter`, `PushNotificationAdapter`, etc. later without changing app code

---

## 4. Where Used in Real .NET Projects

| Real .NET Example | Why Adapter? |
|--------------------|---------------|
| `ILogger` wrapping third-party logging libraries (Serilog, NLog) | Adapts different logging libraries to a common `ILogger` interface |
| `IMemoryCache` vs `IDistributedCache` wrappers | Adapts different caching backends behind a common interface |
| Payment gateway integrations (Stripe, PayPal, Razorpay) | Adapts each provider's SDK into your app's common `IPaymentService` |
| `DataAdapter` (ADO.NET, e.g. `SqlDataAdapter`) | Adapts database results into `DataSet` objects your app understands |

---

## 5. Common Mistakes

| Mistake | Why It's Wrong |
|---------|-----------------|
| ❌ Modifying the third-party/legacy class directly | You may not have access to it, or it may break future library updates |
| ❌ Putting business logic inside the Adapter | Adapter should only **translate calls**, not add business rules |
| ❌ Creating an Adapter when interfaces already match | Unnecessary — only use Adapter when there's an actual mismatch |
| ❌ Confusing Adapter with Facade | Adapter makes ONE interface match another; Facade simplifies access to MANY subsystems (see later) |

---

## ✅ Quick Recap

| Concept | Key Takeaway |
|---------|--------------|
| **Adapter Pattern** | Wraps an incompatible class so it matches the interface your app expects |
| **Real Analogy** | A travel power plug adapter |
| **Key Benefit** | Lets old/third-party code work with new code, without modifying either |
| **Real Use Case** | Logging wrappers, payment gateway integrations, `SqlDataAdapter` |

---

**Previous → [Structural Patterns Introduction](./05-Structural-Patterns-Introduction.md)**
**Next → [Bridge Design Pattern](./07-Bridge-Design-Pattern.md)**
