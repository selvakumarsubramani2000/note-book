# 🌉 Bridge Design Pattern (C# / .NET)

> **Trainer's Note:** Bridge sounds tricky but the idea is simple: **"Separate WHAT something does from HOW it does it, so both can change independently."**

---

## 📑 Table of Contents
1. [What is the Bridge Pattern?](#1-what-is-the-bridge-pattern)
2. [Real-World Analogy](#2-real-world-analogy)
3. [C# Implementation](#3-c-implementation)
4. [Where Used in Real .NET Projects](#4-where-used-in-real-net-projects)
5. [Common Mistakes](#5-common-mistakes)

---

## 1. What is the Bridge Pattern?

**Bridge** decouples an **abstraction** (the "what") from its **implementation** (the "how"), so you can change or extend either one **without affecting the other**.

### 🎯 The Problem It Solves

Imagine you have `Shape` types (Circle, Square) and `Color` types (Red, Blue). Without Bridge, you might create a class for **every combination**:

```
❌ RedCircle, BlueCircle, RedSquare, BlueSquare ...
   Adding a new color = new classes for EVERY shape!
   Adding a new shape = new classes for EVERY color!

This explodes combinatorially: 2 shapes × 2 colors = 4 classes
                                3 shapes × 5 colors = 15 classes 😱
```

**Bridge Pattern** solves this by splitting "Shape" and "Color" into **two separate hierarchies** connected by a bridge, instead of one giant combined hierarchy.

---

## 2. Real-World Analogy

### 📺 TV and Remote Control

```
Different TV BRANDS (Sony, Samsung, LG)  →  the "Implementation"
Different REMOTE TYPES (Basic, Smart)     →  the "Abstraction"

A Basic Remote and a Smart Remote should BOTH be able to work with
ANY TV brand, WITHOUT needing a separate remote class for every
brand + remote-type combination.

[Smart Remote] ──uses bridge──► [Any TV Brand: Sony / Samsung / LG]
[Basic Remote] ──uses bridge──► [Any TV Brand: Sony / Samsung / LG]

The remote (abstraction) and the TV (implementation) can each
evolve independently.
```

---

## 3. C# Implementation

### Step 1: The Implementation Hierarchy ("How" - TV brands)

```csharp
// Implementation interface
public interface ITelevision
{
    void On();
    void Off();
    void SetChannel(int channel);
}

public class SonyTV : ITelevision
{
    public void On() => Console.WriteLine("Sony TV: ON");
    public void Off() => Console.WriteLine("Sony TV: OFF");
    public void SetChannel(int channel) => Console.WriteLine($"Sony TV: Channel {channel}");
}

public class SamsungTV : ITelevision
{
    public void On() => Console.WriteLine("Samsung TV: ON");
    public void Off() => Console.WriteLine("Samsung TV: OFF");
    public void SetChannel(int channel) => Console.WriteLine($"Samsung TV: Channel {channel}");
}
```

### Step 2: The Abstraction Hierarchy ("What" - Remote types)

```csharp
// Abstraction - holds a REFERENCE to the implementation (the "bridge")
public abstract class RemoteControl
{
    protected ITelevision _tv;   // 👈 This reference IS the bridge

    protected RemoteControl(ITelevision tv)
    {
        _tv = tv;
    }

    public virtual void TurnOn() => _tv.On();
    public virtual void TurnOff() => _tv.Off();
}

// Refined abstraction - adds extra behavior
public class SmartRemoteControl : RemoteControl
{
    public SmartRemoteControl(ITelevision tv) : base(tv) { }

    public void VoiceCommand(string command)
    {
        Console.WriteLine($"Voice command recognized: '{command}'");
        if (command == "turn on") TurnOn();
    }

    public void GoToFavoriteChannel() => _tv.SetChannel(100);
}
```

### Using It:

```csharp
// Mix and match ANY remote with ANY TV brand freely!
RemoteControl basicRemoteForSony = new RemoteControl(new SonyTV()) { };
SmartRemoteControl smartRemoteForSamsung = new SmartRemoteControl(new SamsungTV());

smartRemoteForSamsung.VoiceCommand("turn on");       // Samsung TV: ON
smartRemoteForSamsung.GoToFavoriteChannel();          // Samsung TV: Channel 100

// Swap the TV brand without touching the SmartRemoteControl class at all:
SmartRemoteControl smartRemoteForSony = new SmartRemoteControl(new SonyTV());
smartRemoteForSony.GoToFavoriteChannel();             // Sony TV: Channel 100
```

### 💡 Key Idea
> The `RemoteControl` (abstraction) holds a **reference** to `ITelevision` (implementation) instead of inheriting from a specific TV class. This reference is the **"bridge"** — you can change the remote type or the TV brand **independently**, and any combination just works.

---

## 4. Where Used in Real .NET Projects

| Real .NET Example | Why Bridge? |
|--------------------|---------------|
| `System.Data.Common.DbConnection` (ADO.NET) | Abstraction (`DbConnection`) is decoupled from implementation (`SqlConnection`, `MySqlConnection`, etc.) |
| `ILogger` + multiple logging providers | The logging abstraction works with Console, File, Application Insights providers interchangeably |
| Repository pattern with multiple ORMs | `IRepository` abstraction can bridge to EF Core, Dapper, or MongoDB implementations |

---

## 5. Common Mistakes

| Mistake | Why It's Wrong |
|---------|-----------------|
| ❌ Confusing Bridge with Adapter | Adapter fixes **incompatible** interfaces after the fact; Bridge is **designed upfront** to keep abstraction/implementation separate |
| ❌ Using Bridge for simple, single-dimension variation | If you only vary ONE thing (just shapes, no colors), you don't need Bridge — plain inheritance is enough |
| ❌ Tightly coupling abstraction to one specific implementation | Defeats the purpose — always program against the implementation **interface**, not a concrete class |

---

## ✅ Quick Recap

| Concept | Key Takeaway |
|---------|--------------|
| **Bridge Pattern** | Separates "what" (abstraction) from "how" (implementation) so both evolve independently |
| **Real Analogy** | TV remote (abstraction) working with any TV brand (implementation) |
| **Key Benefit** | Avoids combinatorial explosion of classes when you have two independent variations |
| **Real Use Case** | ADO.NET `DbConnection`, `ILogger` with multiple providers |

---

**Previous → [Adapter Design Pattern](./06-Adapter-Design-Pattern.md)**
**Next → [Composite Design Pattern](./08-Composite-Design-Pattern.md)**
