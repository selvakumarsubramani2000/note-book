# 📁 File-Scoped Namespaces in C#

> **Trainer's Note:** File-scoped namespaces remove one nesting level of braces. Your class code starts left-aligned and stays easier to read.

---

## 📑 Table of Contents
1. [What is a File-Scoped Namespace?](#1-what-is-a-file-scoped-namespace)
2. [Old Style vs New Style](#2-old-style-vs-new-style)
3. [Rules and Tips](#3-rules-and-tips)
4. [Combine with Modern Project Style](#4-combine-with-modern-project-style)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is a File-Scoped Namespace?

From **C# 10**, you can declare a namespace for the whole file without wrapping everything in `{ }`.

```csharp
namespace MyApp.Services;

public class OrderService
{
}
```

Everything after the namespace line belongs to that namespace (until end of file).

### Real-world analogy
```
Block namespace = put furniture inside a labeled cabinet with doors
File-scoped    = label the whole room once, then arrange furniture freely
```

---

## 2. Old Style vs New Style

### Classic block-scoped
```csharp
namespace MyApp.Services
{
    public class OrderService
    {
        public void Create() { }
    }
}
```

### File-scoped
```csharp
namespace MyApp.Services;

public class OrderService
{
    public void Create() { }
}
```

Less indentation, same meaning for typical one-namespace files.

---

## 3. Rules and Tips

- Usually one namespace per file with this style
- Great for standard class/record files
- Keep file focused (one main type or tightly related types)
- Namespace still organizes types the same way

### When classic braces may still appear
- Multiple namespaces in rare special files
- Older templates / generated code

---

## 4. Combine with Modern Project Style

A modern C# file often looks like:

```csharp
namespace MyApp.Domain;

public record Customer(string Name, string City);
```

With global usings + file-scoped namespaces + records, code becomes short and clear.

### Beginner rule
```
New class files in modern projects → file-scoped namespace by default
Reading old code → still understand block namespace braces
```

---

## 5. Knowledge Check

1. What advantage does file-scoped namespace give?
2. Convert a block namespace example into file-scoped style.
3. From which C# version is this feature available?
4. Does file-scoped namespace change runtime behavior or mainly syntax/readability?

---

**Previous:** [← Global Usings](./06-Global-Usings.md)

🎉 **Modern Features track complete!** Tuples entry, records, pattern matching, top-level statements, nullable references, recent C# highlights, global usings, and file-scoped namespaces are ready as separate guides.
