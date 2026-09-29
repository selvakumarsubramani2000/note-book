# 🏷️ Enums (Enumerations) in C#

> **Trainer's Note:** Enums give meaningful names to fixed choices. Instead of magic numbers like 1,2,3, you write `Status.Approved`.

---

## 📑 Table of Contents
1. [What is an Enum?](#1-what-is-an-enum)
2. [Enum Basics and Values](#2-enum-basics-and-values)
3. [Useful Enum Operations](#3-useful-enum-operations)
4. [Flags Enum (Simple Idea)](#4-flags-enum-simple-idea)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is an Enum?

An **enum** is a named set of constant choices.

```csharp
enum OrderStatus
{
    Pending,
    Approved,
    Shipped,
    Delivered,
    Cancelled
}
```

### Real-world analogy
```
Without enum:
  status = 1  (what is 1? pending? paid?)

With enum:
  status = OrderStatus.Pending
  readable like form dropdown options
```

---

## 2. Enum Basics and Values

```csharp
OrderStatus status = OrderStatus.Approved;
Console.WriteLine(status);           // Approved
Console.WriteLine((int)status);      // 1 (default starts at 0)
```

### Custom numbers
```csharp
enum HttpSuccess
{
    Ok = 200,
    Created = 201,
    Accepted = 202
}
```

### Use in conditions
```csharp
if (status == OrderStatus.Shipped)
    Console.WriteLine("On the way");

switch (status)
{
    case OrderStatus.Pending:
        Console.WriteLine("Wait");
        break;
    case OrderStatus.Delivered:
        Console.WriteLine("Done");
        break;
}
```

### Default underlying type is `int`
```csharp
enum Priority : byte
{
    Low = 1,
    Medium = 2,
    High = 3
}
```

---

## 3. Useful Enum Operations

```csharp
// string → enum
OrderStatus s1 = Enum.Parse<OrderStatus>("Shipped");

// safe parse
if (Enum.TryParse("Approved", out OrderStatus s2))
    Console.WriteLine(s2);

// check defined
bool ok = Enum.IsDefined(typeof(OrderStatus), 2);

// list all names
foreach (string name in Enum.GetNames(typeof(OrderStatus)))
    Console.WriteLine(name);

// list all values
foreach (OrderStatus value in Enum.GetValues<OrderStatus>())
    Console.WriteLine($"{value} = {(int)value}");
```

### Why enums are better than strings/numbers
| Approach | Problem |
|----------|---------|
| `int status = 2` | Meaning unclear; invalid numbers easy |
| `string status = "aproved"` | Typos at runtime |
| `OrderStatus.Approved` | Clear + compile-time checks |

---

## 4. Flags Enum (Simple Idea)

Use `[Flags]` when multiple options can be combined.

```csharp
[Flags]
enum FilePermission
{
    None = 0,
    Read = 1,      // 0001
    Write = 2,     // 0010
    Execute = 4,   // 0100
    ReadWrite = Read | Write
}

FilePermission p = FilePermission.Read | FilePermission.Write;
Console.WriteLine(p.HasFlag(FilePermission.Read)); // True
```

### Real-world analogy
```
Flags enum = pizza toppings checklist
  you can select multiple toppings together
```

### Beginner tips
- Use enums for fixed business states
- Keep names clear and stable
- Don't overuse flags unless combinations are real
- Prefer enum over raw numbers in public APIs

---

## 5. Knowledge Check

1. What problem do enums solve?
2. What is the default first value number of an enum?
3. How do you convert enum to int and int/string to enum?
4. When do you use `[Flags]`?
5. Write a simple enum for payment modes: Cash, Card, Upi.

---

**Previous:** [← Structures](./01-Structures-Class-vs-Structure.md)  
**Next:** [Operator Overloading →](./03-Operator-Overloading.md)
