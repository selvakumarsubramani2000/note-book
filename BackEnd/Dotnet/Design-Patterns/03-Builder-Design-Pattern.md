# 🧱 Builder Design Pattern (C# / .NET)

> **Trainer's Note:** Builder pattern solves ONE simple problem: **"How do I create a complex object step-by-step, without a messy constructor?"**

---

## 📑 Table of Contents
1. [Builder Design Pattern - Introduction](#1-builder-design-pattern---introduction)
2. [Builder Design Pattern Implementation](#2-builder-design-pattern-implementation)
3. [Fluent Builder Design Pattern](#3-fluent-builder-design-pattern)
4. [Where Used in Real .NET Projects](#4-where-used-in-real-net-projects)
5. [Common Mistakes](#5-common-mistakes)

---

## 1. Builder Design Pattern - Introduction

### 🎯 The Problem It Solves

Imagine a `House` class with many optional parts:

```csharp
// ❌ "Telescoping Constructor" problem
public House(string walls, string roof, bool hasGarage, bool hasGarden,
             bool hasPool, bool hasSolarPanels, int floors, string paintColor)
{
    // ... 8 parameters! Hard to read, easy to mix up order
}

var house = new House("Brick", "Tile", true, false, true, false, 2, "White");
// What does "true, false, true, false" even mean here?? 😵
```

This is called a **"Telescoping Constructor"** — as more optional fields are added, the constructor keeps growing, and calling code becomes unreadable.

### 🍔 Real-World Analogy: Custom Burger Order

```
At a burger shop, you build your burger step-by-step:
  1. Choose bun     → Sesame bun
  2. Choose patty    → Chicken patty
  3. Add cheese?      → Yes, cheddar
  4. Add sauce?       → Mayo
  5. Add veggies?     → Skip

You don't shout ALL options at once in one confusing sentence.
You build it ONE STEP AT A TIME → Builder Pattern works the same way!
```

**Builder Pattern = Construct a complex object step-by-step, and only set the parts you actually need.**

---

## 2. Builder Design Pattern Implementation

### 💻 C# Implementation (Classic Builder)

```csharp
// The complex object we want to build
public class House
{
    public string Walls { get; set; }
    public string Roof { get; set; }
    public bool HasGarage { get; set; }
    public bool HasGarden { get; set; }
    public bool HasPool { get; set; }

    public override string ToString() =>
        $"House [Walls={Walls}, Roof={Roof}, Garage={HasGarage}, Garden={HasGarden}, Pool={HasPool}]";
}

// The Builder - responsible for constructing House step-by-step
public class HouseBuilder
{
    private readonly House _house = new House();

    public HouseBuilder SetWalls(string walls)
    {
        _house.Walls = walls;
        return this;
    }

    public HouseBuilder SetRoof(string roof)
    {
        _house.Roof = roof;
        return this;
    }

    public HouseBuilder AddGarage()
    {
        _house.HasGarage = true;
        return this;
    }

    public HouseBuilder AddGarden()
    {
        _house.HasGarden = true;
        return this;
    }

    public HouseBuilder AddPool()
    {
        _house.HasPool = true;
        return this;
    }

    // Final step - hand over the completed object
    public House Build() => _house;
}
```

### Using It:

```csharp
HouseBuilder builder = new HouseBuilder();

House house = builder
    .SetWalls("Brick")
    .SetRoof("Tile")
    .AddGarage()
    .AddPool()
    .Build();

Console.WriteLine(house);
// House [Walls=Brick, Roof=Tile, Garage=True, Garden=False, Pool=True]
```

### 💡 Why This is Better
- ✅ No confusing `true, false, true` parameter order
- ✅ Only set the parts you need — rest use sensible defaults
- ✅ Reads like plain English: `SetWalls().SetRoof().AddGarage()`

---

## 3. Fluent Builder Design Pattern

Notice in the example above, each method **returns `this`** (the builder itself). This chaining style is called a **Fluent Builder** — it's the most common way Builder is implemented in modern C#.

### 🔗 What Makes It "Fluent"?

```csharp
public HouseBuilder SetWalls(string walls)
{
    _house.Walls = walls;
    return this;   // 👈 THIS is what enables chaining
}
```

Because each method returns `this`, you can **chain calls together** like a sentence:

```csharp
var house = new HouseBuilder()
    .SetWalls("Concrete")
    .SetRoof("Metal")
    .AddGarden()
    .Build();
```

### 🍕 Real-World Analogy: Ordering Coffee (Starbucks Style)

```
"I'd like a Latte, with oat milk, extra shot, no sugar, medium size"

Fluent code mirrors this natural sentence flow:

var coffee = new CoffeeBuilder()
    .OfType("Latte")
    .WithMilk("Oat")
    .WithExtraShot()
    .WithoutSugar()
    .OfSize("Medium")
    .Build();
```

### 💻 Another Practical Example: Building an Email

```csharp
public class Email
{
    public string From { get; set; }
    public string To { get; set; }
    public string Subject { get; set; }
    public string Body { get; set; }
    public bool IsHtml { get; set; }
}

public class EmailBuilder
{
    private readonly Email _email = new Email();

    public EmailBuilder From(string from) { _email.From = from; return this; }
    public EmailBuilder To(string to) { _email.To = to; return this; }
    public EmailBuilder WithSubject(string subject) { _email.Subject = subject; return this; }
    public EmailBuilder WithBody(string body) { _email.Body = body; return this; }
    public EmailBuilder AsHtml() { _email.IsHtml = true; return this; }

    public Email Build() => _email;
}

// Usage - reads like plain English!
var email = new EmailBuilder()
    .From("admin@shop.com")
    .To("customer@gmail.com")
    .WithSubject("Order Confirmation")
    .WithBody("<h1>Thank you for your order!</h1>")
    .AsHtml()
    .Build();
```

### 💡 Key Idea
> **Fluent Builder** is just a Builder where every method returns `this`, allowing you to **chain method calls** for a clean, readable, sentence-like way of constructing objects.

---

## 4. Where Used in Real .NET Projects

| Real .NET Example | Why Builder? |
|--------------------|---------------|
| `StringBuilder` | Builds a string step-by-step (`.Append().Append()`) |
| `WebApplication.CreateBuilder(args)` (ASP.NET Core) | Fluently configures and builds the app (`builder.Services.Add...`) |
| `DbContextOptionsBuilder` (Entity Framework Core) | Configures DB options step-by-step (`.UseSqlServer().EnableSensitiveDataLogging()`) |
| `HostBuilder` | Builds and configures the generic .NET host |

```csharp
// Real ASP.NET Core example - this IS the Builder pattern!
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddControllers();
builder.Services.AddSwaggerGen();
var app = builder.Build();  // 👈 Final "Build()" step, just like our HouseBuilder!
```

---

## 5. Common Mistakes

| Mistake | Why It's Wrong |
|---------|-----------------|
| ❌ Using Builder for simple objects (2-3 properties) | Overkill — a normal constructor or object initializer is enough |
| ❌ Forgetting to return `this` in each method | Breaks the fluent chaining |
| ❌ Not calling `Build()` at the end | Client may get an incomplete object |
| ❌ Making the Builder mutate a shared object across multiple builds | Can cause one build to unexpectedly affect another. Create a **new** internal object per builder instance. |

---

## ✅ Quick Recap

| Concept | Key Takeaway |
|---------|--------------|
| **Builder Pattern** | Constructs complex objects step-by-step instead of one huge constructor |
| **Problem Solved** | Avoids "telescoping constructor" with too many parameters |
| **Fluent Builder** | Each method returns `this`, enabling readable method chaining |
| **Real Use Case** | `StringBuilder`, `WebApplication.CreateBuilder`, `DbContextOptionsBuilder` |

---

**Previous → [Factory Design Pattern](./02-Factory-Design-Pattern.md)**
**Next → [Prototype Design Pattern](./04-Prototype-Design-Pattern.md)**
