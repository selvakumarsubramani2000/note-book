# 🎁 Decorator Design Pattern (C# / .NET)

> **Trainer's Note:** Decorator lets you **add new behavior to an object at runtime**, without touching its original code and without creating a huge chain of subclasses.

---

## 📑 Table of Contents
1. [What is the Decorator Pattern?](#1-what-is-the-decorator-pattern)
2. [Real-World Analogy](#2-real-world-analogy)
3. [C# Implementation](#3-c-implementation)
4. [Where Used in Real .NET Projects](#4-where-used-in-real-net-projects)
5. [Common Mistakes](#5-common-mistakes)

---

## 1. What is the Decorator Pattern?

**Decorator** attaches **additional responsibilities/behavior** to an object dynamically, by **wrapping** it in another object that implements the same interface.

### 🎯 The Problem It Solves

```
You have a basic Coffee. Now you want:
  Coffee + Milk
  Coffee + Milk + Sugar
  Coffee + Sugar + Caramel
  Coffee + Milk + Sugar + Caramel + WhippedCream ...

❌ Without Decorator: you'd need a subclass for EVERY combination
   (CoffeeWithMilk, CoffeeWithMilkAndSugar, CoffeeWithMilkSugarCaramel...)
   → Class explosion, just like the Bridge pattern problem!

✅ With Decorator: wrap the base Coffee with small "add-on" decorators,
   one at a time, in any combination you like.
```

---

## 2. Real-World Analogy

### ☕ Building a Custom Coffee Order

```
Start with:        Plain Coffee                 ($2.00)
Wrap with Milk:     Plain Coffee + Milk           ($2.50)
Wrap with Sugar:    (Plain Coffee + Milk) + Sugar ($2.70)
Wrap with Caramel:  (...) + Caramel               ($3.20)

Each "topping" WRAPS the previous drink and adds its own
cost/description, without changing the original Coffee class.

[Coffee] → wrapped by → [Milk] → wrapped by → [Sugar] → wrapped by → [Caramel]
```

**Decorator Pattern = Wrap an object with one or more "decorator" objects that add new behavior, while keeping the same interface.**

---

## 3. C# Implementation

```csharp
// Step 1: Common interface for the base object AND all decorators
public interface ICoffee
{
    string GetDescription();
    decimal GetCost();
}

// Step 2: The base/concrete object (plain coffee)
public class PlainCoffee : ICoffee
{
    public string GetDescription() => "Plain Coffee";
    public decimal GetCost() => 2.00m;
}

// Step 3: Abstract Decorator - implements the SAME interface, wraps an ICoffee
public abstract class CoffeeDecorator : ICoffee
{
    protected readonly ICoffee _coffee;   // the object being wrapped

    protected CoffeeDecorator(ICoffee coffee)
    {
        _coffee = coffee;
    }

    public virtual string GetDescription() => _coffee.GetDescription();
    public virtual decimal GetCost() => _coffee.GetCost();
}

// Step 4: Concrete Decorators - each adds its own behavior
public class MilkDecorator : CoffeeDecorator
{
    public MilkDecorator(ICoffee coffee) : base(coffee) { }

    public override string GetDescription() => _coffee.GetDescription() + " + Milk";
    public override decimal GetCost() => _coffee.GetCost() + 0.50m;
}

public class SugarDecorator : CoffeeDecorator
{
    public SugarDecorator(ICoffee coffee) : base(coffee) { }

    public override string GetDescription() => _coffee.GetDescription() + " + Sugar";
    public override decimal GetCost() => _coffee.GetCost() + 0.20m;
}

public class CaramelDecorator : CoffeeDecorator
{
    public CaramelDecorator(ICoffee coffee) : base(coffee) { }

    public override string GetDescription() => _coffee.GetDescription() + " + Caramel";
    public override decimal GetCost() => _coffee.GetCost() + 0.50m;
}
```

### Using It:

```csharp
ICoffee order = new PlainCoffee();
order = new MilkDecorator(order);
order = new SugarDecorator(order);
order = new CaramelDecorator(order);

Console.WriteLine($"{order.GetDescription()} = ${order.GetCost()}");
// Plain Coffee + Milk + Sugar + Caramel = $3.20

// Want a DIFFERENT combination? Just wrap differently - no new classes needed!
ICoffee simpleOrder = new SugarDecorator(new PlainCoffee());
Console.WriteLine($"{simpleOrder.GetDescription()} = ${simpleOrder.GetCost()}");
// Plain Coffee + Sugar = $2.20
```

### 💡 Key Idea
> Each decorator **wraps** the previous object and implements the **same interface** (`ICoffee`), so you can **stack decorators in any order/combination** — all while the original `PlainCoffee` class remains untouched.

---

## 4. Where Used in Real .NET Projects

| Real .NET Example | Why Decorator? |
|--------------------|------------------|
| `Stream` classes (`GZipStream`, `CryptoStream`, `BufferedStream`) | Each wraps a base `Stream` to add compression, encryption, or buffering |
| ASP.NET Core Middleware pipeline | Each middleware "wraps" the next one, adding behavior (logging, auth, etc.) before/after calling the next |
| `DelegatingHandler` in `HttpClient` | Wraps HTTP requests to add retry logic, logging, auth headers, etc. |

```csharp
// Real .NET example - Stream decoration!
using var fileStream = new FileStream("data.txt", FileMode.Open);
using var bufferedStream = new BufferedStream(fileStream);      // adds buffering
using var gZipStream = new GZipStream(bufferedStream, CompressionMode.Decompress); // adds decompression
// Each layer WRAPS the previous one, just like our Coffee example!
```

---

## 5. Common Mistakes

| Mistake | Why It's Wrong |
|---------|-----------------|
| ❌ Confusing Decorator with Inheritance | Inheritance is fixed at compile-time; Decorator lets you combine behaviors dynamically at runtime |
| ❌ Not implementing the same interface as the wrapped object | Breaks the ability to stack decorators transparently |
| ❌ Over-decorating (10+ layers) | Can hurt readability/performance — use judiciously |
| ❌ Putting unrelated logic inside a decorator | Each decorator should add ONE focused responsibility (Single Responsibility Principle) |

---

## ✅ Quick Recap

| Concept | Key Takeaway |
|---------|--------------|
| **Decorator Pattern** | Adds new behavior to an object by wrapping it, without modifying its original class |
| **Real Analogy** | Adding toppings (milk, sugar, caramel) to a base coffee |
| **Key Benefit** | Avoids class explosion from needing a subclass for every combination |
| **Real Use Case** | `Stream` wrapping (`GZipStream`, `CryptoStream`), ASP.NET Core middleware pipeline |

---

**Previous → [Composite Design Pattern](./08-Composite-Design-Pattern.md)**
**Next → [Facade Design Pattern](./10-Facade-Design-Pattern.md)**
