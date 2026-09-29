# 🔒 Singleton Design Pattern (C# / .NET)

> **Trainer's Note:** Singleton is the **most commonly asked** design pattern in interviews. Take your time here — once you understand this deeply, other patterns become much easier.

---

## 📑 Table of Contents
1. [What is the Singleton Pattern?](#1-what-is-the-singleton-pattern)
2. [Real-World Analogy](#2-real-world-analogy)
3. [Basic Singleton Implementation](#3-basic-singleton-implementation)
4. [Why is the Singleton Class Sealed?](#4-why-is-the-singleton-class-sealed)
5. [Thread Safety in Singleton](#5-thread-safety-in-singleton)
6. [Lazy vs Eager Loading in Singleton](#6-lazy-vs-eager-loading-in-singleton)
7. [Static Class vs Singleton](#7-static-class-vs-singleton)
8. [Real Example: Exception Logging using Singleton](#8-real-example-exception-logging-using-singleton)
9. [Where Singleton is Used in Real .NET Projects](#9-where-singleton-is-used-in-real-net-projects)
10. [Common Mistakes](#10-common-mistakes)

---

## 1. What is the Singleton Pattern?

**Singleton** ensures a class has **only ONE instance** throughout the entire application, and provides a **single global point of access** to it.

### 🎯 The Problem It Solves:

Imagine multiple parts of your app create their own **database connection** or **logger** objects:
```
Controller A → creates new Logger() → wastes memory
Controller B → creates new Logger() → wastes memory
Controller C → creates new Logger() → wastes memory

Result: 3 different Logger objects doing the same job! 😩
```

**Singleton fixes this** by saying: *"There will be only ONE Logger object, and everyone will share it."*

```
Controller A ─┐
Controller B ─┼──► ONE shared Logger instance ✅
Controller C ─┘
```

---

## 2. Real-World Analogy

### 🇮🇳 The President of a Country

```
A country can have only ONE President at a time.
- You cannot create a "new President" whenever you want.
- Everyone refers to the SAME President.
- There is a single, official way to know "who is the President".

This is exactly how Singleton works in code:
- Only ONE instance of the class exists.
- Everyone accesses the SAME instance.
```

### 🖨️ Another Example: Office Printer

```
An office has ONE shared printer (not one printer per employee).
Every employee sends print jobs to the SAME printer instance.
This saves cost and avoids conflicts — same idea as Singleton!
```

---

## 3. Basic Singleton Implementation

```csharp
public sealed class Logger
{
    // Step 1: Private static field to hold the ONE instance
    private static Logger _instance;

    // Step 2: Private constructor - NO ONE outside can create it with "new"
    private Logger()
    {
        Console.WriteLine("Logger instance created!");
    }

    // Step 3: Public static property to access the single instance
    public static Logger Instance
    {
        get
        {
            if (_instance == null)
            {
                _instance = new Logger();
            }
            return _instance;
        }
    }

    public void Log(string message)
    {
        Console.WriteLine($"[LOG]: {message}");
    }
}
```

### How to Use It:

```csharp
Logger.Instance.Log("Application started");
Logger.Instance.Log("User logged in");

// Both calls use the SAME Logger object - no "new Logger()" anywhere!
```

### 🔑 3 Key Ingredients of a Singleton:

| Ingredient | Purpose |
|------------|---------|
| **Private constructor** | Stops other classes from doing `new Logger()` |
| **Private static field** | Holds the one-and-only instance |
| **Public static property/method** | The only "door" to access the instance |

---

## 4. Why is the Singleton Class Sealed?

You'll often see Singleton classes marked as `sealed`:

```csharp
public sealed class Logger { ... }
```

### 🤔 The Problem Without `sealed`:

```csharp
public class Logger  // NOT sealed
{
    private Logger() { }
    public static Logger Instance { get; } = new Logger();
}

// A sneaky developer could do this:
public class HackedLogger : Logger  // ❌ Inheriting breaks Singleton!
{
    public HackedLogger() : base() { }  // Creates ANOTHER instance!
}
```

Wait — actually since the base constructor is `private`, direct inheritance won't even compile *unless* the constructor is `protected`. But here's the real danger:

### 🎯 The Real Reason: **Protect the Guarantee**

Singleton's entire promise is **"only ONE instance will ever exist."**

If someone **inherits** from your Singleton class, they could:
- Create their own constructor logic
- Override methods and change core behavior
- Potentially create multiple "flavors" of what should be ONE unique object

**`sealed` = "This class is FINAL. No one can inherit from it."**

```
Think of it like a Presidential Seal 🏛️
Once a document has the official seal, NO ONE can modify or extend it.
Similarly, `sealed` locks the class so its Singleton behavior
can NEVER be broken by inheritance.
```

### 💡 Simple Rule:
> **Always mark Singleton classes as `sealed`** to guarantee that the "only one instance" rule can never be violated by a subclass.

---

## 5. Thread Safety in Singleton

### ⚠️ The Problem: Multiple Threads at the Same Time

Our basic Singleton from Section 3 has a **hidden bug** in multi-threaded apps (like web APIs handling many requests at once):

```csharp
public static Logger Instance
{
    get
    {
        if (_instance == null)      // Thread A checks: null? YES
        {                            // Thread B checks: null? YES (at same time!)
            _instance = new Logger(); // Thread A creates instance #1
        }                            // Thread B ALSO creates instance #2! ❌
        return _instance;
    }
}
```

**Result:** TWO instances get created — Singleton is broken! 💥

### ✅ Solution 1: Lock Keyword (Thread-Safe)

```csharp
public sealed class Logger
{
    private static Logger _instance;
    private static readonly object _lock = new object();

    private Logger() { }

    public static Logger Instance
    {
        get
        {
            lock (_lock)  // Only ONE thread can enter this block at a time
            {
                if (_instance == null)
                {
                    _instance = new Logger();
                }
                return _instance;
            }
        }
    }
}
```

**How `lock` helps:**
```
Thread A enters lock → creates instance → exits lock
Thread B WAITS outside lock → enters after A finishes → sees instance already exists → reuses it ✅
```

### ✅ Solution 2: `Lazy<T>` (Best & Simplest - Recommended)

```csharp
public sealed class Logger
{
    private static readonly Lazy<Logger> _instance =
        new Lazy<Logger>(() => new Logger());

    private Logger() { }

    public static Logger Instance => _instance.Value;
}
```

`Lazy<T>` **automatically handles thread-safety internally** — no need to write your own `lock` code!

---

## 6. Lazy vs Eager Loading in Singleton

### 🐢 Eager Loading (Instance Created Immediately)

```csharp
public sealed class Logger
{
    // Instance created the MOMENT the app starts / class is first touched
    private static readonly Logger _instance = new Logger();

    private Logger() { }

    public static Logger Instance => _instance;
}
```

### 🐇 Lazy Loading (Instance Created Only When Needed)

```csharp
public sealed class Logger
{
    private static Logger _instance;

    private Logger() { }

    public static Logger Instance
    {
        get
        {
            if (_instance == null)
                _instance = new Logger();
            return _instance;
        }
    }
}
```

### 📊 Comparison Table

| Aspect | Eager Loading | Lazy Loading |
|--------|---------------|---------------|
| **When created** | As soon as app/class loads | Only when first accessed |
| **Memory usage** | Uses memory even if never used | Saves memory until needed |
| **Thread safety** | ✅ Automatically thread-safe (CLR guarantees it) | ⚠️ Needs `lock` or `Lazy<T>` |
| **Best for** | Lightweight objects always needed | Heavy objects (DB connections, big caches) |
| **Simple analogy** | Turning on the office printer at 9 AM whether used or not | Turning on the printer only when someone needs to print |

### 💡 Recommendation:
> Use **`Lazy<T>`** in modern C# — it gives you **lazy loading + thread safety** in one clean line of code.

---

## 7. Static Class vs Singleton

This is a **very common interview question**! Let's clear the confusion.

### 📊 Side-by-Side Comparison

| Feature | Static Class | Singleton |
|---------|---------------|-----------|
| **Instance** | No instance at all (just a class with static members) | Exactly ONE real object instance |
| **Can implement interfaces?** | ❌ No | ✅ Yes |
| **Can be passed as parameter?** | ❌ No | ✅ Yes (it's a normal object) |
| **Supports Dependency Injection?** | ❌ No | ✅ Yes (very DI-friendly) |
| **Can have constructor logic (state setup)?** | ⚠️ Limited (static constructor only) | ✅ Yes (full constructor) |
| **Lazy loading possible?** | ⚠️ Partially (CLR-controlled) | ✅ Fully controllable |
| **Inheritance** | ❌ Cannot inherit from a static class | ✅ Can implement interfaces, be sealed etc. |
| **Testing (Unit Tests)** | ❌ Hard to mock | ✅ Easy to mock via interface |

### 🎯 Example: Why DI-Friendliness Matters

```csharp
// ❌ Static Class - Cannot be injected or mocked easily
public static class MathHelper
{
    public static int Add(int a, int b) => a + b;
}

// Usage - tightly coupled, hard to unit test
var result = MathHelper.Add(2, 3);


// ✅ Singleton - Can implement an interface, easy to mock in tests
public interface ICalculator
{
    int Add(int a, int b);
}

public sealed class Calculator : ICalculator
{
    private static readonly Lazy<Calculator> _instance = new(() => new Calculator());
    public static Calculator Instance => _instance.Value;
    private Calculator() { }

    public int Add(int a, int b) => a + b;
}

// In ASP.NET Core, you can even register it in DI:
// builder.Services.AddSingleton<ICalculator, Calculator>();
```

### 💡 Simple Rule of Thumb:
> Use a **static class** for simple, stateless helper/utility methods (like `Math.Round()`).
> Use a **Singleton** when the object has **state**, needs to implement an **interface**, or should be **testable/injectable**.

---

## 8. Real Example: Exception Logging using Singleton

A very practical, real-world use case — a centralized **Exception Logger** that every part of your app can use.

```csharp
public sealed class ExceptionLogger
{
    private static readonly Lazy<ExceptionLogger> _instance =
        new Lazy<ExceptionLogger>(() => new ExceptionLogger());

    private readonly string _logFilePath = "exceptions.log";
    private readonly object _fileLock = new object();

    // Private constructor - prevents external creation
    private ExceptionLogger() { }

    public static ExceptionLogger Instance => _instance.Value;

    public void LogException(Exception ex)
    {
        string logEntry = $"{DateTime.Now:yyyy-MM-dd HH:mm:ss} | " +
                           $"{ex.GetType().Name} | {ex.Message}\n";

        // Lock ensures only ONE thread writes to file at a time
        lock (_fileLock)
        {
            File.AppendAllText(_logFilePath, logEntry);
        }
    }
}
```

### Using It Across Your Application:

```csharp
public class OrderService
{
    public void PlaceOrder(int orderId)
    {
        try
        {
            // Order processing logic...
            if (orderId <= 0)
                throw new ArgumentException("Invalid Order ID");
        }
        catch (Exception ex)
        {
            // Every service in the app uses the SAME logger instance
            ExceptionLogger.Instance.LogException(ex);
        }
    }
}

public class PaymentService
{
    public void ProcessPayment(decimal amount)
    {
        try
        {
            if (amount <= 0)
                throw new InvalidOperationException("Amount must be positive");
        }
        catch (Exception ex)
        {
            ExceptionLogger.Instance.LogException(ex);  // Same shared instance!
        }
    }
}
```

### 🎯 Why Singleton is Perfect Here:
- ✅ Only ONE log file connection is managed (no file conflicts)
- ✅ Every service across the app shares the **same logging mechanism**
- ✅ `lock` inside ensures **thread-safe file writing**
- ✅ Centralized — if you want to change logging (e.g., to database), you update **ONE class**

---

## 9. Where Singleton is Used in Real .NET Projects

| Real .NET Example | Why Singleton? |
|--------------------|-----------------|
| `IServiceCollection.AddSingleton<T>()` | ASP.NET Core built-in DI supports Singleton lifetime |
| `HttpClientFactory` internals | Reuses expensive HTTP connections |
| `IMemoryCache` | One shared cache across the whole app |
| `IConfiguration` | One shared configuration object |
| `ILoggerFactory` | One shared logging factory |

---

## 10. Common Mistakes

| Mistake | Why It's Wrong |
|---------|-----------------|
| ❌ Forgetting `private` constructor | Anyone can create multiple instances with `new` |
| ❌ Not handling thread safety | Multiple threads may create multiple instances |
| ❌ Making Singleton hold too much state | Becomes a "God Object" - hard to maintain |
| ❌ Using Singleton for everything | Overuse causes tightly-coupled, hard-to-test code |
| ❌ Forgetting `sealed` | Someone could break the "only one instance" guarantee via inheritance |

---

## ✅ Quick Recap

| Concept | Key Takeaway |
|---------|--------------|
| **Singleton** | Ensures only ONE instance of a class exists |
| **Sealed** | Prevents inheritance from breaking the Singleton guarantee |
| **Thread Safety** | Use `lock` or (better) `Lazy<T>` to prevent race conditions |
| **Lazy vs Eager** | Lazy = created on first use; Eager = created immediately |
| **Static vs Singleton** | Static = no instance, no DI; Singleton = real object, DI-friendly, testable |
| **Real Use Case** | Centralized logging, caching, configuration |

---

**Previous → [Introduction to Design Patterns](./00-Introduction-to-Design-Patterns.md)**
**Next → [Factory Design Pattern](./02-Factory-Design-Pattern.md)**
