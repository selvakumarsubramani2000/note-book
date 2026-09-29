# 🏗️ Structural Design Patterns - Introduction (C# / .NET)

> **Trainer's Note:** We just finished Creational patterns ("how to CREATE objects"). Now we move to Structural patterns: **"how to ORGANIZE and CONNECT objects together."**

---

## 📑 Table of Contents
1. [What Are Structural Patterns?](#1-what-are-structural-patterns)
2. [Real-World Analogy](#2-real-world-analogy)
3. [Structural Patterns We Will Learn](#3-structural-patterns-we-will-learn)
4. [Why They Matter](#4-why-they-matter)

---

## 1. What Are Structural Patterns?

**Structural Design Patterns** deal with **how classes and objects are composed (combined)** to form larger, more flexible structures — **without making the whole system rigid or hard to change.**

They answer the question:
> **"How do different pieces of my application fit together cleanly?"**

Unlike Creational patterns (which focus on **object creation**), Structural patterns focus on **object relationships and composition**.

---

## 2. Real-World Analogy

### 🧩 Building with LEGO Blocks

```
LEGO blocks are individually simple, but you can COMBINE them
in many ways to build complex structures (houses, cars, castles)
without changing the blocks themselves.

Structural patterns work the same way:
- Small, simple classes/objects
- Combined in smart ways
- To build bigger, flexible systems
- WITHOUT rewriting the original classes
```

### 🔌 Another Analogy: Universal Travel Adapter

```
Your laptop charger has a US plug, but you're traveling to India
with different sockets. You don't buy a new charger —
you use a TRAVEL ADAPTER that sits between the plug and the socket.

This is literally the "Adapter" pattern we'll cover next!
```

---

## 3. Structural Patterns We Will Learn

| # | Pattern | Real-World Example | One-Line Purpose |
|---|---------|---------------------|-------------------|
| 1 | **Adapter** | Power plug adapter for foreign sockets | Makes two incompatible interfaces work together |
| 2 | **Bridge** | TV remote works with any TV brand | Separates abstraction from implementation so both can change independently |
| 3 | **Composite** | Folder containing files AND other folders | Treats individual objects and groups of objects the same way |
| 4 | **Decorator** | Adding toppings to a pizza | Adds new behavior to an object without changing its original code |
| 5 | **Facade** | One "Power ON" button for TV + sound + lights | Provides a simple interface to a complex subsystem |

```
┌─────────────────────────────────────────────────────────┐
│               STRUCTURAL PATTERNS                        │
├───────────────┬───────────────┬───────────────┬─────────┤
│   ADAPTER     │    BRIDGE     │   COMPOSITE   │ DECORATOR│
│ "Make things  │ "Separate     │ "Treat one    │ "Add     │
│  fit together"│  abstraction  │  or many the  │ features │
│               │  from impl."  │  same way"    │ safely"  │
├───────────────┴───────────────┴───────────────┴─────────┤
│                       FACADE                              │
│           "Hide complexity behind a simple door"          │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Why They Matter

| Without Structural Patterns | With Structural Patterns |
|-------------------------------|-----------------------------|
| Incompatible classes can't work together | Adapter bridges the gap |
| Changing one part breaks unrelated parts | Bridge keeps abstraction and implementation independent |
| Tree-like data (folders, menus) needs special-case code | Composite treats single items and groups uniformly |
| Adding a feature means editing existing class code | Decorator adds features without touching original code |
| Client code needs to know 10 different subsystem classes | Facade gives ONE simple entry point |

### 💡 Simple Rule to Remember:
> If Creational patterns are about **"birth"** of objects, Structural patterns are about **"relationships"** between objects — how they connect, combine, and cooperate.

---

## ✅ Quick Recap

| Concept | Key Takeaway |
|---------|--------------|
| **Structural Patterns** | Focus on how objects/classes are composed into larger structures |
| **Goal** | Flexible, maintainable relationships between objects |
| **5 Patterns Ahead** | Adapter, Bridge, Composite, Decorator, Facade |
| **Real Analogy** | LEGO blocks — simple pieces combined into complex, flexible structures |

---

**Previous → [Prototype Design Pattern](./04-Prototype-Design-Pattern.md)**
**Next → [Adapter Design Pattern](./06-Adapter-Design-Pattern.md)**
