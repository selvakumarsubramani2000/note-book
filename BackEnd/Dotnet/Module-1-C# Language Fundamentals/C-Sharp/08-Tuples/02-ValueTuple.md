# 📦 C# ValueTuple

> **Trainer's Note:** ValueTuple is the modern tuple syntax (C# 7+). Use named elements and deconstruction for clean, readable code.

---

## 📑 Table of Contents
1. [What is ValueTuple?](#1-what-is-valuetuple)
2. [Create ValueTuple](#2-create-valuetuple)
3. [Return Multiple Values](#3-return-multiple-values)
4. [Deconstruction](#4-deconstruction)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is ValueTuple?

**ValueTuple** is the modern tuple style used from **C# 7** onward.

```csharp
(int id, string name) person = (101, "Selva");
Console.WriteLine(person.id);
Console.WriteLine(person.name);
```

### Real-world analogy
```
ValueTuple = labeled lunch box sections

  Instead of "box slot 1 / slot 2"
  You can label: Rice | Curry | Salad
```

---

## 2. Create ValueTuple

```csharp
// Named elements (best style)
(string city, int pincode) address = ("Chennai", 600001);

// Unnamed elements
var point = (10, 20);
Console.WriteLine(point.Item1); // 10
Console.WriteLine(point.Item2); // 20

// Infer types with var + names
var product = (Id: 5, Name: "Pen", Price: 10.5);
Console.WriteLine(product.Name);
```

### Use in loops / simple grouping
```csharp
var scores = new[]
{
    (Name: "Anu", Marks: 90),
    (Name: "Ravi", Marks: 76)
};

foreach (var s in scores)
    Console.WriteLine($"{s.Name}: {s.Marks}");
```

---

## 3. Return Multiple Values

```csharp
(bool ok, string msg, int code) Validate(int age)
{
    if (age < 18)
        return (false, "Too young", 1001);

    return (true, "Allowed", 0);
}

var result = Validate(20);
Console.WriteLine(result.ok);  // true
Console.WriteLine(result.msg); // Allowed
```

This is cleaner than many `out` parameters for simple multi-result methods.

---

## 4. Deconstruction

Deconstruction unpacks tuple parts into separate variables.

```csharp
(string city, int pin) = ("Mumbai", 400001);
Console.WriteLine(city); // Mumbai

// Discard a value with _
(bool ok, _, int code) = Validate(15);
```

### Beginner tips
- Prefer named elements for readability
- Use deconstruction at call sites when useful
- Keep tuples small (2–4 values is ideal)
- If the shape is a real business model used everywhere, create a class/record instead

---

## 5. Knowledge Check

1. Write a ValueTuple named `(string City, int Pin)` for Chennai / 600001.
2. What is deconstruction in tuples?
3. Return three values from a method using ValueTuple syntax.
4. Why are named elements better than Item1/Item2?
5. When should you still create a class instead of ValueTuple?

---

**Previous:** [← Tuple Class](./01-Tuple-Class.md)  
**Next:** [ValueTuple Struct →](./03-ValueTuple-Struct.md)
