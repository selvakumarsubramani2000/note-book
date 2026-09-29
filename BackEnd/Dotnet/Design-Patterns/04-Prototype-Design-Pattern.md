# 🧬 Prototype Design Pattern (C# / .NET)

> **Trainer's Note:** Prototype is the simplest Creational pattern to understand: **"Copy an existing object instead of building a new one from scratch."**

---

## 📑 Table of Contents
1. [Prototype Design Pattern - Introduction](#1-prototype-design-pattern---introduction)
2. [Prototype Design Pattern Implementation](#2-prototype-design-pattern-implementation)
3. [Shallow Copy vs Deep Copy](#3-shallow-copy-vs-deep-copy)
4. [Where Used in Real .NET Projects](#4-where-used-in-real-net-projects)
5. [Common Mistakes](#5-common-mistakes)

---

## 1. Prototype Design Pattern - Introduction

### 🎯 The Problem It Solves

Sometimes creating a new object from scratch is **expensive or complex**:
- It requires reading from a database or file
- It requires heavy calculations
- It has many properties already set up in a specific way, and you just need a **slightly modified copy**

```csharp
// ❌ Expensive: re-fetch and re-build everything from scratch
Employee emp2 = LoadEmployeeFromDatabase(empId); // slow DB call again!
emp2.Name = "New Name";
```

### 📄 Real-World Analogy: Photocopying a Document

```
You have a signed contract template with 20 filled-in fields.
Instead of typing all 20 fields again for a new client,
you PHOTOCOPY the existing document and just change the name and date.

Photocopy (fast) > Re-typing everything (slow)

This is exactly what the Prototype pattern does with OBJECTS.
```

**Prototype Pattern = Create new objects by COPYING an existing object (the "prototype"), instead of building one from scratch.**

### ✅ Benefits
- Avoids costly re-creation (DB calls, complex setup)
- Quick way to get an object that's "mostly the same" with small changes
- Reduces number of subclasses needed just to represent variations

---

## 2. Prototype Design Pattern Implementation

C# makes this easy using the built-in `ICloneable` interface (or a custom `Clone()` method).

### 💻 C# Implementation

```csharp
public class Employee : ICloneable
{
    public string Name { get; set; }
    public string Department { get; set; }
    public decimal Salary { get; set; }
    public List<string> Skills { get; set; } = new List<string>();

    // Prototype method - creates a copy of THIS object
    public object Clone()
    {
        return this.MemberwiseClone();  // shallow copy - explained in Section 3
    }

    public override string ToString() =>
        $"{Name} | {Department} | ${Salary} | Skills: {string.Join(", ", Skills)}";
}
```

### Using It:

```csharp
// Original object - imagine this took a long DB call to build
Employee original = new Employee
{
    Name = "John",
    Department = "Engineering",
    Salary = 75000,
    Skills = new List<string> { "C#", "SQL" }
};

// Instead of rebuilding from scratch, CLONE it!
Employee copy = (Employee)original.Clone();
copy.Name = "Jane";   // only change what's different
copy.Salary = 80000;

Console.WriteLine(original); // John | Engineering | $75000 | Skills: C#, SQL
Console.WriteLine(copy);     // Jane | Engineering | $80000 | Skills: C#, SQL
```

**Notice:** We didn't touch the database again or manually re-set `Department` — we just copied and tweaked!

---

## 3. Shallow Copy vs Deep Copy

This is the **most important gotcha** in the Prototype pattern.

### 🥤 Shallow Copy (`MemberwiseClone()`)

Copies all **value type** fields directly, but for **reference type** fields (like `List<string>`), it only copies the **reference** (pointer) — not the actual list!

```csharp
Employee copy = (Employee)original.Clone();
copy.Skills.Add("Azure");  // ⚠️ This modifies BOTH original AND copy's list!

Console.WriteLine(original.Skills.Count); // 3 - Oops! original changed too!
```

```
Shallow Copy:

original.Skills ───┐
                    ├──► SAME List object in memory ["C#", "SQL", "Azure"]
copy.Skills     ───┘

Changing one affects BOTH! ❌
```

### 🍰 Deep Copy (Manually Clone Nested Objects)

A **Deep Copy** creates brand-new copies of every reference-type field too, so the two objects are **completely independent**.

```csharp
public object Clone()
{
    Employee clone = (Employee)this.MemberwiseClone();
    clone.Skills = new List<string>(this.Skills); // create a NEW list
    return clone;
}
```

```
Deep Copy:

original.Skills ──► List object #1 ["C#", "SQL"]
copy.Skills     ──► List object #2 ["C#", "SQL"]  (separate copy)

Changing one does NOT affect the other! ✅
```

### 📊 Comparison Table

| Aspect | Shallow Copy | Deep Copy |
|--------|--------------|-----------|
| **Value type fields** (int, decimal, bool) | Copied normally | Copied normally |
| **Reference type fields** (List, class objects) | Shared reference (same object) | New independent copy |
| **Speed** | Faster | Slower (more memory allocation) |
| **Risk** | Changes can accidentally affect original | Safe - fully independent |
| **C# Method** | `MemberwiseClone()` | Manually clone each reference field |

### 💡 Simple Rule:
> If your class has **only simple properties** (string, int, bool, decimal), Shallow Copy is fine. If it has **lists, arrays, or nested objects**, use Deep Copy to avoid shared-reference bugs.

---

## 4. Where Used in Real .NET Projects

| Real .NET Example | Why Prototype? |
|--------------------|------------------|
| `Object.MemberwiseClone()` | Built-in shallow clone support in every .NET object |
| `ICloneable` interface | Standard .NET contract for "cloneable" types |
| AutoMapper's `.Clone()`-like mapping | Copying DTOs into new instances with slight modifications |
| Prototype-based configuration templates | E.g., cloning a "default settings" object and tweaking a few values per environment |

---

## 5. Common Mistakes

| Mistake | Why It's Wrong |
|---------|-----------------|
| ❌ Assuming `MemberwiseClone()` copies everything | It only does a SHALLOW copy — reference fields are shared |
| ❌ Not overriding Clone for complex objects | Nested lists/objects will silently share state, causing hard-to-find bugs |
| ❌ Using Prototype for simple, cheap-to-create objects | Unnecessary — just use `new` directly |
| ❌ Forgetting `ICloneable` returns `object` | You must cast the result back to your actual type |

---

## ✅ Quick Recap

| Concept | Key Takeaway |
|---------|--------------|
| **Prototype Pattern** | Create new objects by copying an existing one instead of building from scratch |
| **Real Analogy** | Photocopying a document instead of retyping it |
| **Shallow Copy** | Copies simple fields; reference fields are SHARED |
| **Deep Copy** | Copies everything, including nested objects — fully independent |
| **Real Use Case** | `MemberwiseClone()`, `ICloneable`, cloning template/config objects |

---

**Previous → [Builder Design Pattern](./03-Builder-Design-Pattern.md)**
**Next → [Structural Design Patterns Introduction](./05-Structural-Patterns-Introduction.md)**
