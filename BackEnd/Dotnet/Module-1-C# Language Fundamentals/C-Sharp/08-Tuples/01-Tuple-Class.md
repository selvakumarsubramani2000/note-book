# 🏛️ C# Tuple Class

> **Trainer's Note:** The Tuple class is the older style. You still need it for legacy code and interviews, but ValueTuple is better for new work.

---

## 📑 Table of Contents
1. [What is the Tuple Class?](#1-what-is-the-tuple-class)
2. [Create and Access](#2-create-and-access)
3. [Method Return and Nested Tuples](#3-method-return-and-nested-tuples)
4. [Limitations](#4-limitations)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is the Tuple Class?

The **Tuple class** lives in `System` and is a **reference type** (class).

```csharp
Tuple<int, string> person = Tuple.Create(1, "Anu");
```

### Real-world analogy
```
Tuple class = fixed unlabeled box slots
  Slot1, Slot2, Slot3...
  Useful, but names are not friendly
```

---

## 2. Create and Access

### Create
```csharp
// Factory method (common)
Tuple<int, string, double> student =
    Tuple.Create(101, "Selva", 89.5);

// Constructor
var emp = new Tuple<int, string>(1, "Anu");
```

### Access values — Item1, Item2, Item3...
```csharp
Console.WriteLine(student.Item1); // 101
Console.WriteLine(student.Item2); // Selva
Console.WriteLine(student.Item3); // 89.5
```

There are no meaningful names like `Id` / `Name` on classic Tuple class members.

---

## 3. Method Return and Nested Tuples

### Method returning Tuple class
```csharp
Tuple<bool, string> Login(string user, string pass)
{
    if (user == "admin" && pass == "123")
        return Tuple.Create(true, "Welcome");

    return Tuple.Create(false, "Invalid login");
}

var result = Login("admin", "123");
Console.WriteLine(result.Item1); // true
Console.WriteLine(result.Item2); // Welcome
```

### Nested tuples (when more than 8 values)
A single `Tuple` can hold up to **8 elements**. The 8th can itself be another tuple (nesting).

```csharp
var t = Tuple.Create(1, 2, 3, 4, 5, 6, 7, Tuple.Create(8, 9));
Console.WriteLine(t.Item7);        // 7
Console.WriteLine(t.Rest.Item1);   // 8
Console.WriteLine(t.Rest.Item2);   // 9
```

---

## 4. Limitations

| Limitation | Meaning |
|------------|---------|
| Only `Item1`, `Item2`... | Harder to read |
| Reference type | Heap allocation |
| Read-only members | Cannot change Item values after create |
| Feels heavy for tiny groups | Overkill for temporary pairs |

```csharp
var oldPoint = Tuple.Create(5, 10);
// oldPoint.Item1 = 50; // ❌ not allowed
```

> In modern C#, prefer **ValueTuple** unless you maintain old code.

---

## 5. Knowledge Check

1. Is the Tuple class a reference type or value type?
2. How do you read the second value from `Tuple.Create(10, "Hi")`?
3. How many elements can one Tuple hold before nesting?
4. Why are Item names a disadvantage?
5. Write a Tuple method return for success + message.

---

**Previous:** [← C# Tuple](./00-CSharp-Tuple.md)  
**Next:** [ValueTuple →](./02-ValueTuple.md)
