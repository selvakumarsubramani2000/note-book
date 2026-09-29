# 📝 C# Verbatim String Literal — `@`

> **Trainer's Note:** Verbatim strings start with `@` and treat text almost exactly as written. Perfect for Windows paths and multi-line text.

---

## 📑 Table of Contents
1. [What is a Verbatim String?](#1-what-is-a-verbatim-string)
2. [Paths and Escaping](#2-paths-and-escaping)
3. [Multi-line and Quotes](#3-multi-line-and-quotes)
4. [Raw Strings and Interpolation](#4-raw-strings-and-interpolation)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is a Verbatim String?

A **verbatim string** starts with `@`.

### Real-world analogy
```
Normal string  = you must escape special symbols by hand
Verbatim (@)   = "write it as it looks on the page"
```

---

## 2. Paths and Escaping

### Without `@` (normal string)
```csharp
string path = "C:\\Users\\Selva\\Documents\\notes.txt";
// You must escape every backslash with \\
```

### With `@` (verbatim)
```csharp
string path = @"C:\Users\Selva\Documents\notes.txt";
// Backslashes are kept as-is. Much easier to read.
```

---

## 3. Multi-line and Quotes

### Multi-line text with `@`
```csharp
string letter = @"Dear Team,
Please review the order.
Thank you.";
```

### Quote inside verbatim string
To put a double-quote inside a verbatim string, write it twice:

```csharp
string quote = @"He said, ""Welcome"".";
// He said, "Welcome".
```

---

## 4. Raw Strings and Interpolation

### Raw string literals (modern C# 11+)
```csharp
string json = """
{
  "name": "Selva",
  "city": "Chennai"
}
""";
```

Use this for multi-line JSON/SQL when your project targets newer C#.

### Quick comparison
| Need | Prefer |
|------|--------|
| File path with `\` | `@"C:\folder\file.txt"` |
| Multi-line plain text | Verbatim `@""` or raw `""" """` |
| Insert variables | `$"..."` or `$@"..."` |

```csharp
string folder = "Reports";
string path = $@"C:\Data\{folder}\summary.txt";
```

---

## 5. Knowledge Check

1. Rewrite this path using a verbatim string: `"C:\\Data\\Files\\a.txt"`.
2. How do you put a double-quote inside a verbatim string?
3. When would you use `$@"..."`?
4. What is one benefit of raw string literals `""" ... """`?

---

**Previous:** [← Strings in C#](./00-Strings-in-CSharp.md)  
**Next:** [String Class →](./02-String-Class.md)
