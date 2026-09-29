# 🎯 Pattern Matching Enhancements in C#

> **Trainer's Note:** Pattern matching helps you check shape/type/value in a clear way. Modern C# made switch expressions and richer patterns everyday tools.

---

## 📑 Table of Contents
1. [What is Pattern Matching?](#1-what-is-pattern-matching)
2. [is Patterns and Type Patterns](#2-is-patterns-and-type-patterns)
3. [Switch Expressions](#3-switch-expressions)
4. [Useful Modern Patterns](#4-useful-modern-patterns)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is Pattern Matching?

**Pattern matching** tests a value against a shape/condition and often extracts data at the same time.

### Real-world analogy
```
Package arrives
  If it is a letter → open letter flow
  If it is a box    → open box flow
  If fragile sticker → careful path
```

---

## 2. is Patterns and Type Patterns

```csharp
object data = "Hello";

if (data is string text)
{
    Console.WriteLine(text.Length); // text is already string
}

if (data is int number and > 0)
{
    Console.WriteLine(number);
}
```

### Property pattern
```csharp
public record Order(string Status, decimal Amount);

Order order = new("Paid", 500);

if (order is { Status: "Paid", Amount: > 100 })
{
    Console.WriteLine("Process paid large order");
}
```

---

## 3. Switch Expressions

```csharp
string Describe(object shape) => shape switch
{
    int n when n < 0 => "negative int",
    int n => $"int {n}",
    string s => $"text length {s.Length}",
    null => "null",
    _ => "something else"
};
```

Cleaner than long if-else chains for classification.

---

## 4. Useful Modern Patterns

### Relational + logical patterns
```csharp
string Grade(int mark) => mark switch
{
    < 0 or > 100 => "Invalid",
    >= 90 => "A",
    >= 75 => "B",
    >= 50 => "C",
    _ => "F"
};
```

### List pattern (C# 11+)
```csharp
int[] nums = { 1, 2, 3 };

if (nums is [1, 2, 3])
    Console.WriteLine("Exact match");

if (nums is [1, .., 3])
    Console.WriteLine("Starts with 1 and ends with 3");
```

### Beginner tips
- Prefer switch expression for mapping values
- Keep patterns readable; split complex conditions
- Combine with records for clean property matching

---

## 5. Knowledge Check

1. What does `if (obj is string s)` give you?
2. Write a switch expression that maps day numbers 1–7 to weekday/weekend.
3. What does `_` mean in a switch expression?
4. Give one example of a property pattern.

---

**Previous:** [← Records](./01-Records-in-CSharp.md)  
**Next:** [Top-level Statements →](./03-Top-level-Statements.md)
