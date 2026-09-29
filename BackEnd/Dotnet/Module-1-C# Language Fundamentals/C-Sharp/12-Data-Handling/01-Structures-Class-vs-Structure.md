# 🧱 Structures — Class versus Structure

> **Trainer's Note:** Both `class` and `struct` can hold data + methods. The big difference is **reference type vs value type**. Choose carefully.

---

## 📑 Table of Contents
1. [What is a Structure?](#1-what-is-a-structure)
2. [Structure Example](#2-structure-example)
3. [Class vs Structure](#3-class-vs-structure)
4. [When to Use Which](#4-when-to-use-which)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is a Structure?

A **structure (`struct`)** is a **value type** custom data shape.

```csharp
struct Point
{
    public int X;
    public int Y;
}
```

### Real-world analogy
```
class  = house address (reference)
         copy address → both people point to same house

struct = photocopy of a form (value)
         copy form → each person has separate paper
```

---

## 2. Structure Example

```csharp
public struct Point
{
    public int X { get; set; }
    public int Y { get; set; }

    public Point(int x, int y)
    {
        X = x;
        Y = y;
    }

    public double DistanceFromOrigin()
    {
        return Math.Sqrt(X * X + Y * Y);
    }
}

Point p1 = new Point(3, 4);
Point p2 = p1;   // copy values
p2.X = 100;

Console.WriteLine(p1.X); // 3  (unchanged)
Console.WriteLine(p2.X); // 100
```

### Struct rules beginners should know
- Cannot inherit from another struct/class (except interfaces)
- Can implement interfaces
- Has default value (all fields zero/null/false style defaults)
- Best when data is small and immutable-like

```csharp
public struct Money
{
    public decimal Amount { get; }
    public string Currency { get; }

    public Money(decimal amount, string currency)
    {
        Amount = amount;
        Currency = currency;
    }
}
```

---

## 3. Class vs Structure

| Point | Class | Structure |
|-------|-------|-----------|
| Type | Reference type | Value type |
| Storage | Heap (object reference) | Usually stack/inline value semantics |
| Assignment | Copy reference | Copy data |
| Inheritance | Yes | No (can implement interfaces) |
| Default constructor | Can customize freely | Parameterless always available conceptually as default values |
| null | Can be null | Non-nullable by default (`Point?` needed for null) |
| Best for | Complex objects, identity, large models | Small data holders (coordinates, range, simple values) |

### Side-by-side behavior
```csharp
// CLASS
public class Person
{
    public string Name { get; set; }
}

Person a = new Person { Name = "Anu" };
Person b = a;
b.Name = "Ravi";
Console.WriteLine(a.Name); // Ravi (same object)

// STRUCT
public struct Pixel
{
    public int Color { get; set; }
}

Pixel x = new Pixel { Color = 1 };
Pixel y = x;
y.Color = 9;
Console.WriteLine(x.Color); // 1 (separate copy)
```

---

## 4. When to Use Which

### Use `struct` when:
- Data is small
- Represents a single value concept (`Point`, `RGB`, `Range`)
- You want value copy behavior
- Immutability is preferred

### Use `class` when:
- Object has identity and lifecycle
- Data is larger / complex
- You need inheritance
- Many parts share same instance

### Beginner rule of thumb
```
Customer, Order, Service, Repository → class
Point(x,y), Temperature, Money amount pair → struct (maybe)
If unsure for business models → start with class
```

---

## 5. Knowledge Check

1. Is `struct` a value type or reference type?
2. What happens when you assign one struct variable to another?
3. Can a struct inherit from a class?
4. Give 3 differences between class and structure.
5. Give one good example for struct and one for class.

---

**Previous:** [← Nullable Types](./00-Nullable-Types-and-Null-Coalescing.md)  
**Next:** [Enums →](./02-Enums-in-CSharp.md)
