# 📦 C# Tuple

> **Trainer's Note:** A tuple is a simple way to group a few values together without creating a full class. Great for methods that need to return more than one result.

---

## 📑 Table of Contents
1. [What is a Tuple?](#1-what-is-a-tuple)
2. [Why Use Tuples?](#2-why-use-tuples)
3. [Two Main Tuple Styles](#3-two-main-tuple-styles)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. What is a Tuple?

A **tuple** is a lightweight container that holds **multiple values as one unit**.

```csharp
// One method returns both status and message
(bool isSuccess, string message) = ValidateOrder();
```

### Real-world analogy
```
Tuple = a small takeaway bag with fixed slots

  Slot 1 → receipt number
  Slot 2 → customer name
  Slot 3 → total amount

  You carry related items together without building a full suitcase (class).
```

---

## 2. Why Use Tuples?

| Without tuple | With tuple |
|---------------|------------|
| Create a full class only to return 2–3 values | Return values directly |
| Use `out` parameters | Cleaner return style |
| Hard to read temporary grouping | Short and clear grouping |

### Common use cases
- Return success flag + message from a method
- Return coordinates `(x, y)`
- Temporary grouping inside one method
- Quick pairing of related values in LINQ/select

---

## 3. Two Main Tuple Styles

In C#, you will meet two styles:

1. **`Tuple` class** — older, reference type (`System.Tuple`)
2. **`ValueTuple`** — modern, value type (preferred today)

```
Old style:
  Tuple.Create(101, "Selva")
  values as Item1, Item2...

New style:
  (int Id, string Name) person = (101, "Selva");
  values as person.Id, person.Name
```

### Beginner rule of thumb
> For new C# code, use **ValueTuple** with names.  
> Learn **Tuple class** so you can read older code and interview questions.

### What next in this folder
| File | Topic |
|------|--------|
| Tuple Class | old `System.Tuple` details |
| ValueTuple | modern `(...)` syntax, names, deconstruction |
| ValueTuple Struct | value-type behavior, mutability, when to use |

---

## 4. Knowledge Check

1. What problem does a tuple solve in simple words?
2. Name the two main tuple styles in C#.
3. Which style is preferred for new code?
4. Give one method scenario where returning a tuple is useful.

---

**Previous:** [← Strings in C#](../Strings/00-Strings-in-CSharp.md)
**Next:** [Tuple Class →](./01-Tuple-Class.md)
