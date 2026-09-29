# 🏭 Factory Design Pattern (C# / .NET)

> **Trainer's Note:** Factory patterns are all about **"who creates the object"**. Instead of your code saying `new SomeClass()` everywhere, you delegate that job to a Factory.

---

## 📑 Table of Contents
1. [Factory Design Pattern - Introduction](#1-factory-design-pattern---introduction)
2. [Factory Method Design Pattern](#2-factory-method-design-pattern)
3. [Abstract Factory Design Pattern](#3-abstract-factory-design-pattern)
4. [Factory Method vs Abstract Factory](#4-factory-method-vs-abstract-factory)
5. [Where Used in Real .NET Projects](#5-where-used-in-real-net-projects)
6. [Common Mistakes](#6-common-mistakes)

---

## 1. Factory Design Pattern - Introduction

### 🎯 The Problem It Solves

Imagine you write `new` everywhere to create objects:

```csharp
Pizza pizza1 = new MargheritaPizza();
Pizza pizza2 = new PepperoniPizza();
Pizza pizza3 = new VeggiePizza();
```

If tomorrow a new pizza type is added, or the creation logic changes (e.g., add default toppings), you must **update every single place** in your code where `new` was used. That's risky and messy.

### 🍕 Real-World Analogy: Pizza Shop

```
You don't go into the kitchen and make your own pizza.
You just tell the counter: "I want a Pepperoni Pizza."
The KITCHEN (Factory) decides HOW to prepare it and hands it to you.

Customer → orders "Pepperoni" → Factory → creates PepperoniPizza → gives to customer
```

**Factory Pattern = A dedicated method/class whose JOB is to create objects, so the rest of your code doesn't need to know the creation details.**

### ✅ Benefits
- Creation logic is in **ONE place** (easy to maintain)
- Client code depends on an **interface/abstract type**, not concrete classes
- Easy to add new types without breaking existing code (Open/Closed Principle)

---

## 2. Factory Method Design Pattern

**Factory Method** defines a method for creating an object, but lets **subclasses decide** which class to instantiate.

### 🧩 Structure

```
IPizza (interface)
   ├── MargheritaPizza
   └── PepperoniPizza

PizzaFactory (abstract creator)
   └── CreatePizza(string type) → returns IPizza
```

### 💻 C# Implementation

```csharp
// Step 1: Common interface for all products
public interface IPizza
{
    void Prepare();
}

// Step 2: Concrete products
public class MargheritaPizza : IPizza
{
    public void Prepare() => Console.WriteLine("Preparing Margherita Pizza 🍕");
}

public class PepperoniPizza : IPizza
{
    public void Prepare() => Console.WriteLine("Preparing Pepperoni Pizza 🍕");
}

// Step 3: The Factory - single place that knows "how to create"
public class PizzaFactory
{
    public IPizza CreatePizza(string type)
    {
        return type.ToLower() switch
        {
            "margherita" => new MargheritaPizza(),
            "pepperoni" => new PepperoniPizza(),
            _ => throw new ArgumentException("Unknown pizza type")
        };
    }
}
```

### Using It:

```csharp
var factory = new PizzaFactory();

IPizza pizza = factory.CreatePizza("pepperoni");
pizza.Prepare();   // Client doesn't know or care about PepperoniPizza class directly
```

### 💡 Key Idea
> The **client code** only talks to `IPizza` and `PizzaFactory`. It never writes `new PepperoniPizza()` directly. If a new pizza type is added, you only touch the `PizzaFactory` class.

---

## 3. Abstract Factory Design Pattern

**Abstract Factory** creates **families of related objects** without specifying their exact concrete classes.

### 🪑 Real-World Analogy: Furniture Factory

```
A furniture company makes matching SETS:
  Modern Set   → Modern Sofa + Modern Chair + Modern Table
  Victorian Set → Victorian Sofa + Victorian Chair + Victorian Table

You don't mix a Modern Sofa with a Victorian Chair - they come as a MATCHING FAMILY.
```

Factory Method creates **ONE product**. Abstract Factory creates a **FAMILY of related products** that must work together.

### 💻 C# Implementation

```csharp
// Product interfaces
public interface IChair { void SitOn(); }
public interface ISofa { void LieOn(); }

// Modern family
public class ModernChair : IChair { public void SitOn() => Console.WriteLine("Sitting on Modern Chair"); }
public class ModernSofa : ISofa { public void LieOn() => Console.WriteLine("Lying on Modern Sofa"); }

// Victorian family
public class VictorianChair : IChair { public void SitOn() => Console.WriteLine("Sitting on Victorian Chair"); }
public class VictorianSofa : ISofa { public void LieOn() => Console.WriteLine("Lying on Victorian Sofa"); }

// Abstract Factory contract
public interface IFurnitureFactory
{
    IChair CreateChair();
    ISofa CreateSofa();
}

// Concrete factories - one per family
public class ModernFurnitureFactory : IFurnitureFactory
{
    public IChair CreateChair() => new ModernChair();
    public ISofa CreateSofa() => new ModernSofa();
}

public class VictorianFurnitureFactory : IFurnitureFactory
{
    public IChair CreateChair() => new VictorianChair();
    public ISofa CreateSofa() => new VictorianSofa();
}
```

### Using It:

```csharp
IFurnitureFactory factory = new ModernFurnitureFactory();

IChair chair = factory.CreateChair();
ISofa sofa = factory.CreateSofa();

chair.SitOn();  // Sitting on Modern Chair
sofa.LieOn();   // Lying on Modern Sofa

// Switch the ENTIRE family just by changing the factory:
factory = new VictorianFurnitureFactory();
chair = factory.CreateChair();  // Now creates Victorian Chair automatically
```

### 💡 Key Idea
> Change **one line** (`new ModernFurnitureFactory()` → `new VictorianFurnitureFactory()`) and your **entire family of objects** switches consistently. No mismatched combinations possible.

---

## 4. Factory Method vs Abstract Factory

| Aspect | Factory Method | Abstract Factory |
|--------|-----------------|-------------------|
| **Creates** | ONE product | A FAMILY of related products |
| **Structure** | Single method (`CreatePizza`) | Interface with multiple creation methods |
| **Real Example** | Pizza shop making ONE pizza type | Furniture shop making a MATCHING SET |
| **Complexity** | Simple | More complex (multiple factories/products) |
| **When to Use** | You need to create one type of object flexibly | You need to create groups of related objects that must stay consistent |

---

## 5. Where Used in Real .NET Projects

| Real .NET Example | Why Factory? |
|--------------------|---------------|
| `HttpClientFactory.CreateClient()` | Creates configured `HttpClient` instances centrally |
| `DbProviderFactory` (ADO.NET) | Creates DB connections/commands for SQL Server, MySQL, etc. |
| `ILoggerFactory.CreateLogger()` | Creates logger instances without exposing concrete logger classes |
| `Activator.CreateInstance()` | Low-level factory-style object creation used internally by .NET |

---

## 6. Common Mistakes

| Mistake | Why It's Wrong |
|---------|-----------------|
| ❌ Using Factory for a single, never-changing object | Unnecessary complexity - just use `new` directly |
| ❌ Putting business logic inside the Factory | Factory should only handle **creation**, not business rules |
| ❌ Mixing Factory Method and Abstract Factory concepts | Keep clear boundaries: one product vs a family of products |
| ❌ Forgetting to code against interfaces | Client code should depend on `IPizza`, not `PepperoniPizza` |

---

## ✅ Quick Recap

| Concept | Key Takeaway |
|---------|--------------|
| **Factory Pattern** | Centralizes object creation logic in one place |
| **Factory Method** | Creates ONE type of product based on input |
| **Abstract Factory** | Creates a FAMILY of related products consistently |
| **Real Use Case** | `HttpClientFactory`, `DbProviderFactory`, `ILoggerFactory` |

---

**Previous → [Singleton Design Pattern](./01-Singleton-Design-Pattern.md)**
**Next → [Builder Design Pattern](./03-Builder-Design-Pattern.md)**
