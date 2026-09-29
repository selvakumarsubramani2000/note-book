# 🧩 Extension Methods in C#

> **Trainer's Note:** Extension methods let you add new methods to existing types without modifying the original class. LINQ is built on this idea.

---

## 📑 Table of Contents
1. [What is an Extension Method?](#1-what-is-an-extension-method)
2. [How to Write One](#2-how-to-write-one)
3. [Real Examples](#3-real-examples)
4. [Rules and Best Practices](#4-rules-and-best-practices)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is an Extension Method?

An **extension method** looks like an instance method but is defined as a static method with `this` on first parameter.

```csharp
string name = "  selva  ";
string clean = name.TrimAndTitle(); // extension style call
```

### Real-world analogy
```
You cannot redesign a factory phone easily
But you can add a useful silicone case accessory
Extension method = add-on tool for existing type
```

---

## 2. How to Write One

Rules:
1. static class
2. static method
3. first parameter marked with `this`

```csharp
public static class StringExtensions
{
    public static string TrimAndTitle(this string value)
    {
        if (string.IsNullOrWhiteSpace(value))
            return string.Empty;

        value = value.Trim();
        return char.ToUpper(value[0]) + value.Substring(1).ToLower();
    }
}

// usage
Console.WriteLine("  hELLo ".TrimAndTitle()); // Hello
```

Import the namespace of the extension class with `using`.

---

## 3. Real Examples

### Null/empty helpers
```csharp
public static class StringExt
{
    public static bool IsBlank(this string? s)
        => string.IsNullOrWhiteSpace(s);
}

if (input.IsBlank())
    Console.WriteLine("Required");
```

### Collection helper
```csharp
public static class ListExt
{
    public static void AddMany<T>(this List<T> list, params T[] items)
        => list.AddRange(items);
}

var nums = new List<int>();
nums.AddMany(1, 2, 3);
```

### LINQ-style feel
```csharp
public static class EnumExt
{
    public static IEnumerable<int> Evens(this IEnumerable<int> source)
        => source.Where(x => x % 2 == 0);
}
```

---

## 4. Rules and Best Practices

| Do | Don't |
|----|-------|
| Keep helpers small and clear | Hide complex business workflows |
| Extend types you don't own carefully | Overuse on every class |
| Name class `SomethingExtensions` | Surprise side effects |
| Put in clear namespace | Make ambiguous conflicting extensions |

### Important facts
- Cannot override existing instance methods
- If instance method same signature exists, instance method wins
- Works with interfaces too (`this IEnumerable<T>`)
- Extension methods are syntactic sugar over static calls

```csharp
// these are same idea
name.TrimAndTitle();
StringExtensions.TrimAndTitle(name);
```

---

## 5. Knowledge Check

1. What is an extension method?
2. What special keyword is used on first parameter?
3. Can extension methods modify the original class source? 
4. Write an extension `IsEven` for `int`.
5. Why is LINQ related to extension methods?

---

**Previous:** [← Multithreading](./11-Multithreading-in-CSharp.md)  
**Next:** [Lambda Expressions →](./13-Lambda-Expressions.md)
