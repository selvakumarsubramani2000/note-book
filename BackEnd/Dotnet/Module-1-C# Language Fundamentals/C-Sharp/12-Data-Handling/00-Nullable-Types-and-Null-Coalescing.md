# ❓ Nullable Types and Null Coalescing Operator

> **Trainer's Note:** In real apps, some values may be "unknown" or "not set". Nullable types and `??` help you handle missing data safely without crashes.

---

## 📑 Table of Contents
1. [Why Nullable Types?](#1-why-nullable-types)
2. [Nullable Value Types](#2-nullable-value-types)
3. [Null Coalescing Operator `??`](#3-null-coalescing-operator-)
4. [Null-Conditional `?.` and `??=`](#4-null-conditional--and-)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Why Nullable Types?

Normal value types like `int`, `bool`, `DateTime` **cannot be null**.

```csharp
int age = null; // ❌ compile error
```

But sometimes data is missing:
- Age not filled in a form
- Discount not configured
- End date not decided yet

### Real-world analogy
```
Normal int   = a locked scoreboard that must show a number
Nullable int = scoreboard that can show a number OR "Not Available"
```

---

## 2. Nullable Value Types

Use `?` after a value type:

```csharp
int? age = null;          // allowed
bool? isActive = null;
DateTime? endDate = null;

age = 25;
```

`int?` means `Nullable<int>`.

### Important members
```csharp
int? marks = null;

Console.WriteLine(marks.HasValue); // False
// Console.WriteLine(marks.Value); // throws if null

marks = 80;
Console.WriteLine(marks.HasValue); // True
Console.WriteLine(marks.Value);    // 80
```

### Get value or default
```csharp
int? score = null;
int finalScore = score.GetValueOrDefault();     // 0
int finalScore2 = score.GetValueOrDefault(100); // 100
```

### Nullable reference types (modern C#)
```csharp
string name = null;          // older style often allowed
string? city = null;         // explicitly may be null
string country = "India";    // expected non-null
```

Enable nullable context in project for better null warnings.

---

## 3. Null Coalescing Operator `??`

`??` means: **if left side is null, use right side**.

```csharp
int? marks = null;
int result = marks ?? 0;     // result = 0

string? name = null;
string display = name ?? "Guest"; // "Guest"
```

### Real-world analogy
```
?? = backup plan

  Prefer customer nickname
  If nickname is missing → use "Guest"
```

### Chaining
```csharp
string? a = null;
string? b = null;
string? c = "Chennai";

string city = a ?? b ?? c ?? "Unknown";
// city = "Chennai"
```

### Without `??` (longer)
```csharp
int result;
if (marks.HasValue)
    result = marks.Value;
else
    result = 0;
```

---

## 4. Null-Conditional `?.` and `??=`

### Null-conditional `?.`
Call only if object is not null.

```csharp
string? text = null;
int? len = text?.Length;   // null, no crash

string? city = user?.Address?.City;
```

### Null-coalescing assignment `??=`
Assign only if current value is null.

```csharp
string? title = null;
title ??= "Untitled"; // title becomes "Untitled"
title ??= "Other";    // stays "Untitled"
```

### Practical example
```csharp
public class Order
{
    public decimal? Discount { get; set; }
}

Order order = new Order();
decimal payDiscount = order.Discount ?? 0m;
Console.WriteLine($"Discount applied: {payDiscount}");
```

### Beginner safety tips
| Tip | Why |
|-----|-----|
| Use `int?` only when value can truly be missing | Don't make everything nullable |
| Prefer `??` for default values | Cleaner than long if-null checks |
| Use `?.` to avoid `NullReferenceException` | Safe member access |
| Check `HasValue` before `.Value` | Prevent runtime errors |

---

## 5. Knowledge Check

1. Why can't a normal `int` be null?
2. What does `int?` mean?
3. What is the output idea of `int? x = null; int y = x ?? 10;`?
4. When do you use `?.`?
5. What does `name ??= "Guest";` do?

---

**Next:** [Structures →](./01-Structures-Class-vs-Structure.md)
