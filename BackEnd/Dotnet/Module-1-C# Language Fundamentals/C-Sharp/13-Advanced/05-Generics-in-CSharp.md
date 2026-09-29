# 🧬 C# Generics (Advanced View)

> **Trainer's Note:** You already use generics with `List<T>`. Here we go deeper: generic methods, classes, interfaces, and constraints for reusable type-safe design.

---

## 📑 Table of Contents
1. [Generics Recap](#1-generics-recap)
2. [Generic Methods and Classes](#2-generic-methods-and-classes)
3. [Generic Interfaces](#3-generic-interfaces)
4. [Constraints and Practical Patterns](#4-constraints-and-practical-patterns)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Generics Recap

Generics let one definition work with many types safely.

```csharp
List<int> marks = new();
List<string> names = new();
Dictionary<string, decimal> prices = new();
```

### Benefits
- compile-time type safety
- less casting
- better performance vs object collections
- reusable algorithms/components

---

## 2. Generic Methods and Classes

```csharp
public static T Max<T>(T a, T b) where T : IComparable<T>
{
    return a.CompareTo(b) >= 0 ? a : b;
}

Console.WriteLine(Max(10, 20));
Console.WriteLine(Max("A", "C"));
```

```csharp
public class Result<T>
{
    public bool Success { get; init; }
    public T? Data { get; init; }
    public string? Error { get; init; }

    public static Result<T> Ok(T data) => new() { Success = true, Data = data };
    public static Result<T> Fail(string error) => new() { Success = false, Error = error };
}

var ok = Result<int>.Ok(100);
var fail = Result<string>.Fail("Not found");
```

---

## 3. Generic Interfaces

```csharp
public interface IRepository<T>
{
    T? GetById(int id);
    void Add(T item);
}

public class Product { public int Id { get; set; } }

public class ProductRepository : IRepository<Product>
{
    private readonly List<Product> _items = new();
    public Product? GetById(int id) => _items.FirstOrDefault(x => x.Id == id);
    public void Add(Product item) => _items.Add(item);
}
```

This pattern is common in real .NET apps.

---

## 4. Constraints and Practical Patterns

```csharp
public class Factory<T> where T : new()
{
    public T Create() => new T();
}

public class EntityService<T> where T : class
{
    public void PrintType() => Console.WriteLine(typeof(T).Name);
}

public class NumberHelper<T> where T : struct, IComparable<T>
{
    public T Clamp(T value, T min, T max)
    {
        if (value.CompareTo(min) < 0) return min;
        if (value.CompareTo(max) > 0) return max;
        return value;
    }
}
```

### Common constraints
`class`, `struct`, `new()`, base class, interface, `notnull`

### Practical advice
```
API response wrappers      → Result<T>
Repositories               → IRepository<T>
Collections/algorithms     → List<T>, methods with T
Don't force generics everywhere — use when reuse + safety is real
```

---

## 5. Knowledge Check

1. Why are generics safer than `object`?
2. Write a generic method signature for Swap.
3. What does `where T : new()` mean?
4. Give one generic interface example from business apps.
5. Name 3 common constraints.

---

**Previous:** [← Events](./04-Events-in-CSharp.md)  
**Next:** [IEnumerable vs IEnumerator →](./06-IEnumerable-vs-IEnumerator.md)
