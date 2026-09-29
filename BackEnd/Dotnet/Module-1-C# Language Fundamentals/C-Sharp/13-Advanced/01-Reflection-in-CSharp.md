# 🪞 C# Reflection

> **Trainer's Note:** Reflection lets your program inspect itself at runtime — types, methods, properties, attributes — and even call them dynamically.

---

## 📑 Table of Contents
1. [What is Reflection?](#1-what-is-reflection)
2. [Inspect Types and Members](#2-inspect-types-and-members)
3. [Create Objects and Invoke Methods](#3-create-objects-and-invoke-methods)
4. [When to Use / Avoid](#4-when-to-use--avoid)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is Reflection?

**Reflection** reads metadata of assemblies/types at runtime.

Namespace: `System.Reflection`

```csharp
Type t = typeof(string);
Console.WriteLine(t.FullName);
```

### Real-world analogy
```
Reflection = X-ray of a machine while it is running
  Which parts exist?
  What screws/buttons are available?
  Can I press a button by name?
```

---

## 2. Inspect Types and Members

```csharp
using System.Reflection;

public class Product
{
    public int Id { get; set; }
    public string Name { get; set; }
    public void Print() => Console.WriteLine(Name);
}

Type type = typeof(Product);

Console.WriteLine(type.Name); // Product

foreach (PropertyInfo p in type.GetProperties())
    Console.WriteLine($"Property: {p.Name} ({p.PropertyType.Name})");

foreach (MethodInfo m in type.GetMethods(BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly))
    Console.WriteLine($"Method: {m.Name}");
```

### Get type from object
```csharp
object obj = new Product();
Type t2 = obj.GetType();
```

### Read attributes
```csharp
var attrs = type.GetCustomAttributes(false);
```

---

## 3. Create Objects and Invoke Methods

```csharp
Type type = typeof(Product);

// create instance
object? instance = Activator.CreateInstance(type);

// set property
PropertyInfo? nameProp = type.GetProperty("Name");
nameProp?.SetValue(instance, "Pen");

// call method
MethodInfo? print = type.GetMethod("Print");
print?.Invoke(instance, null);
```

### Practical example: simple mapper idea
```csharp
void ShowAllProperties(object source)
{
    foreach (var prop in source.GetType().GetProperties())
        Console.WriteLine($"{prop.Name} = {prop.GetValue(source)}");
}
```

---

## 4. When to Use / Avoid

### Useful for
- Frameworks/plugins
- Serialization tools
- Dependency injection containers
- Analyzing attributes
- Admin/debug utilities

### Avoid for everyday business code
- Slower than direct calls
- Less compile-time safety
- Harder to read and refactor

### Beginner rule
```
Normal app flow                 → direct code
Dynamic/plugin/framework needs  → reflection carefully
```

---

## 5. Knowledge Check

1. What does reflection do?
2. Difference between `typeof(Product)` and `obj.GetType()`?
3. How do you list properties of a type?
4. How can you call a method by name at runtime?
5. Give one reason reflection can be risky.

---

**Previous:** [← Attributes](./00-Attributes-in-CSharp.md)
**Next:** [Delegates →](./03-Delegates-in-CSharp.md)

> Properties get/set moved to: [Properties track →](../Properties/00-Properties-in-CSharp.md)
