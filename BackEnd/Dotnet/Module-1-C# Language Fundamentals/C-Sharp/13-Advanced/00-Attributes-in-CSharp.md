# 🏷️ C# Attributes

> **Trainer's Note:** Attributes are sticky notes on your code. They add extra information that tools, frameworks, and reflection can read later.

---

## 📑 Table of Contents
1. [What are Attributes?](#1-what-are-attributes)
2. [Built-in Attributes](#2-built-in-attributes)
3. [Custom Attributes](#3-custom-attributes)
4. [When to Use Attributes](#4-when-to-use-attributes)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What are Attributes?

An **attribute** attaches metadata (extra info) to code elements: classes, methods, properties, parameters, etc.

```csharp
[Obsolete("Use NewPay() instead")]
public void OldPay() { }
```

### Real-world analogy
```
Attribute = sticker on a product box
  "Fragile"
  "Expires 2027"
  "Handle with care"

The sticker is not the product.
It gives extra information for systems/people handling it.
```

Syntax uses square brackets: `[AttributeName]`

---

## 2. Built-in Attributes

| Attribute | Meaning |
|-----------|---------|
| `[Obsolete]` | mark old API, warn/error on use |
| `[Serializable]` | mark type as serializable (legacy scenarios) |
| `[DllImport]` | call native library methods |
| `[Conditional]` | include method calls only if symbol defined |
| `[Flags]` | enum can combine values |
| `[HttpGet]` / `[HttpPost]` | ASP.NET route/method metadata |
| `[Required]` / `[Range]` | validation metadata |

```csharp
[Obsolete("Use CalculateV2", true)] // true = compile error
public int CalculateV1() => 1;

[Flags]
public enum Permission
{
    None = 0,
    Read = 1,
    Write = 2
}
```

### Attribute targets (common)
```csharp
[assembly: AssemblyVersion("1.0.0.0")] // assembly-level
```

---

## 3. Custom Attributes

Create your own by inheriting `System.Attribute`.

```csharp
[AttributeUsage(AttributeTargets.Class | AttributeTargets.Method)]
public class AuthorAttribute : Attribute
{
    public string Name { get; }
    public string Version { get; set; } = "1.0";

    public AuthorAttribute(string name)
    {
        Name = name;
    }
}

[Author("Selva", Version = "2.1")]
public class OrderService
{
    [Author("Anu")]
    public void Create() { }
}
```

### Read attribute with reflection
```csharp
var attr = typeof(OrderService)
    .GetCustomAttributes(typeof(AuthorAttribute), false)
    .Cast<AuthorAttribute>()
    .FirstOrDefault();

Console.WriteLine(attr?.Name);
```

---

## 4. When to Use Attributes

### Good uses
- Framework integration (ASP.NET, EF, xUnit)
- Validation markers
- Documentation / tooling metadata
- Feature switches read by scanners

### Avoid
- Putting heavy business logic inside attributes
- Overusing custom attributes when a normal config/method is clearer

### Beginner rule
```
Need to mark code for a framework/tool → Attribute
Need to run business behavior now      → normal method/class
```

---

## 5. Knowledge Check

1. What is an attribute in simple words?
2. What does `[Obsolete]` do?
3. How do you create a custom attribute class?
4. Which class do custom attributes inherit from?
5. Give one real ASP.NET example of attributes.

---

**Next:** [Reflection →](./01-Reflection-in-CSharp.md)
