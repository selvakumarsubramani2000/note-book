# 🧾 Records in C#

> **Trainer's Note:** A record is perfect for immutable data models — like DTOs — with value-based equality and less boilerplate.

---

## 📑 Table of Contents
1. [What is a Record?](#1-what-is-a-record)
2. [Record Class Basics](#2-record-class-basics)
3. [with Expression and Equality](#3-with-expression-and-equality)
4. [record class vs record struct](#4-record-class-vs-record-struct)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is a Record?

A **record** is a C# type focused on **data**.

```csharp
public record Person(string Name, int Age);
```

### Real-world analogy
```
class   = employee with behavior and changing state
record  = filled form/data card
          compare by content, copy with small edits easily
```

Introduced strongly from **C# 9** (record class), with more options in later versions.

---

## 2. Record Class Basics

```csharp
public record Product(string Name, decimal Price);

var p1 = new Product("Pen", 10);
var p2 = new Product("Pen", 10);

Console.WriteLine(p1);                 // Product { Name = Pen, Price = 10 }
Console.WriteLine(p1 == p2);           // True (value-based equality)
Console.WriteLine(p1.Name);
```

### Positional record
Primary constructor parameters become public properties automatically (init-only style for record class positional syntax).

### Manual style also works
```csharp
public record Customer
{
    public string Name { get; init; } = "";
    public string City { get; init; } = "";
}
```

---

## 3. with Expression and Equality

### Non-destructive copy
```csharp
var original = new Product("Book", 100);
var updated = original with { Price = 120 };

Console.WriteLine(original.Price); // 100
Console.WriteLine(updated.Price);  // 120
```

### Equality is by values
Two records with same property values are equal (for record reference types, equality compares contents, not only references).

```csharp
var a = new Person("Anu", 20);
var b = new Person("Anu", 20);
Console.WriteLine(a.Equals(b)); // True
```

---

## 4. record class vs record struct

| Point | `record` / `record class` | `record struct` |
|-------|----------------------------|-----------------|
| Type | Reference type | Value type |
| Default use | Most DTOs | Small immutable values |
| Nullability | Can be null (unless NRT rules say no) | Non-nullable by default as value type |
| Copy semantics | Reference + with-copy | Value copy behavior |

```csharp
public record struct Point(int X, int Y);
```

### When to use records
- API request/response models
- Immutable configuration snippets
- Event payloads / read models

### When a normal class is better
- Heavy mutable behavior
- Complex lifecycle / identity entities that change often

---

## 5. Knowledge Check

1. What problem do records solve compared to normal classes?
2. What does `with` do?
3. Are two records with same values equal by default?
4. When would you choose `record struct`?

---

**Previous:** [← Tuples](./00-Tuples-in-CSharp.md)  
**Next:** [Pattern Matching Enhancements →](./02-Pattern-Matching-Enhancements.md)
