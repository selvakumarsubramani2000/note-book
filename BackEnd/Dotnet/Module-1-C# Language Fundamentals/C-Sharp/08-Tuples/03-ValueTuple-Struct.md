# 🧱 C# ValueTuple Struct

> **Trainer's Note:** ValueTuple is not just syntax sugar — under the hood it is a **struct** (value type). That explains mutability and many performance advantages over the old Tuple class.

---

## 📑 Table of Contents
1. [ValueTuple is a Struct](#1-valuetuple-is-a-struct)
2. [Mutability and Helpers](#2-mutability-and-helpers)
3. [Tuple Class vs ValueTuple](#3-tuple-class-vs-valuetuple)
4. [When to Use ValueTuple](#4-when-to-use-valuetuple)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. ValueTuple is a Struct

`ValueTuple` is implemented as a **struct** (value type) in `System`.

```csharp
// Modern syntax:
(int a, string b) data = (1, "Hi");

// Same idea under the hood:
ValueTuple<int, string> same = (1, "Hi");
```

### What “struct” means here (simple)
```
class (Tuple)       → like a shared house key object on heap
struct (ValueTuple) → like a small value package you copy
```

### Useful facts
| Point | Meaning |
|-------|---------|
| Type | Value type (`struct`) |
| Mutable fields | Yes — members can be changed |
| Performance | Usually better for small temporary data |
| Naming | Supports named elements (`person.Name`) |
| Equality | Supports value-based comparison helpers |

---

## 2. Mutability and Helpers

### Mutable example
```csharp
(int x, int y) point = (5, 10);
point.x = 50;   // allowed
point.y = 100;
Console.WriteLine(point); // (50, 100)
```

Compare with Tuple class:
```csharp
var oldPoint = Tuple.Create(5, 10);
// oldPoint.Item1 = 50; // ❌ not allowed (read-only properties)
```

### Handy methods
```csharp
var t = (10, "A");
Console.WriteLine(t.ToString()); // (10, A)

var t2 = (10, "A");
Console.WriteLine(t.Equals(t2)); // true
```

### CompareTo (when elements are comparable)
```csharp
var a = (1, "B");
var b = (1, "C");
int result = a.CompareTo(b); // compares field by field
```

---

## 3. Tuple Class vs ValueTuple

| Point | `Tuple` class | `ValueTuple` |
|-------|---------------|--------------|
| Type | Reference type (class) | Value type (struct) |
| Syntax | `Tuple.Create(1, "A")` | `(int id, string name)` |
| Element names | Only `Item1`, `Item2`... | Can use meaningful names |
| Mutable? | No (read-only) | Yes |
| Deconstruction | Less natural | Excellent language support |
| Performance | Heap allocation | Usually lighter for small data |
| Modern recommendation | Old style / legacy code | **Preferred today** |
| Max easy size | Up to 8 (then nested) | Also has limits, but syntax is nicer |

### Side-by-side
```csharp
// OLD — Tuple class
Tuple<int, string> oldStyle = Tuple.Create(1, "Selva");
Console.WriteLine(oldStyle.Item2);

// NEW — ValueTuple
(int Id, string Name) newStyle = (1, "Selva");
Console.WriteLine(newStyle.Name);
```

---

## 4. When to Use ValueTuple

### Perfect for
- Return 2–4 related values from a method
- Temporary grouping inside one method/file
- Quick data packing without a new class model

### Prefer a class/record when
```
If data is a real business concept used in many places
  → create a class/record (Customer, OrderResult)

If data is only a temporary package
  → ValueTuple is fine
```

### Beginner rule of thumb
> For new C# code, use **ValueTuple** with names.  
> Learn **Tuple class** so you can read older code and interview questions.

---

## 5. Knowledge Check

1. Is `ValueTuple` a class or a struct?
2. Can you change `point.x` after creating `(int x, int y) point = (1, 2)`?
3. Give 3 differences between Tuple class and ValueTuple.
4. When should you create a class instead of using a tuple?
5. Why is ValueTuple often preferred for temporary multi-return values?

---

**Previous:** [← ValueTuple](./02-ValueTuple.md)  
**Next:** [Indexers in C# →](../Indexers/00-Indexers-in-CSharp.md)

🎉 **Tuples track complete!** Intro, Tuple class, ValueTuple syntax, and struct behavior are now separate clear guides.
