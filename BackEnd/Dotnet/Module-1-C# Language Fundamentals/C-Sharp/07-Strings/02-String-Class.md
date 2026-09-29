# 🧰 C# String Class

> **Trainer's Note:** `System.String` gives many ready methods for everyday text work — trim, search, split, replace, and compare.

---

## 📑 Table of Contents
1. [Useful Properties / Helpers](#1-useful-properties--helpers)
2. [Common Methods](#2-common-methods)
3. [Examples](#3-examples)
4. [Compare and Null Checks](#4-compare-and-null-checks)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Useful Properties / Helpers

| Member | Meaning |
|--------|---------|
| `Length` | Number of characters |
| `string.Empty` | Empty text `""` |
| `string.IsNullOrEmpty(s)` | null or empty? |
| `string.IsNullOrWhiteSpace(s)` | null, empty, or only spaces? |

---

## 2. Common Methods

| Method | Example result idea |
|--------|---------------------|
| `ToUpper()` / `ToLower()` | Case change |
| `Trim()` / `TrimStart()` / `TrimEnd()` | Remove spaces |
| `Contains("ab")` | true/false search |
| `StartsWith("Mr")` / `EndsWith(".com")` | Prefix/suffix check |
| `IndexOf("a")` | First position (or -1) |
| `Substring(start, len)` | Take part of text |
| `Replace("old", "new")` | Replace text |
| `Split(',')` | Break into parts |
| `string.Join("-", arr)` | Join parts |
| `PadLeft` / `PadRight` | Add spaces/chars |
| `Compare` / `Equals` | Compare text |
| `Format` | Build formatted text |

---

## 3. Examples

```csharp
string email = "  Selva@Example.com  ";

Console.WriteLine(email.Length);
Console.WriteLine(email.Trim());
Console.WriteLine(email.ToLower());
Console.WriteLine(email.Contains("@"));
Console.WriteLine(email.Trim().EndsWith(".com"));

string csv = "pen,book,bag";
string[] parts = csv.Split(',');
string joined = string.Join(" | ", parts); // pen | book | bag

string name = "Selva";
string hello = string.Format("Hello, {0}!", name);
```

---

## 4. Compare and Null Checks

### Comparing strings safely
```csharp
string a = "Hello";
string b = "hello";

bool sameDefault = a == b; // false (case-sensitive)
bool sameIgnoreCase = a.Equals(b, StringComparison.OrdinalIgnoreCase); // true
```

### Null and empty checks (use these often)
```csharp
string input = null;

if (string.IsNullOrWhiteSpace(input))
    Console.WriteLine("Please enter a value");
```

### Beginner tips
- Prefer `IsNullOrWhiteSpace` for user input checks
- Be explicit with case-insensitive compares
- Prefer `$"..."` over heavy `string.Format` in new code when simple

---

## 5. Knowledge Check

1. Name 5 useful methods from the String class.
2. Difference between `IsNullOrEmpty` and `IsNullOrWhiteSpace`?
3. How do you do a case-insensitive equals check?
4. Split `"a,b,c"` into an array and join with `" | "`.

---

**Previous:** [← Verbatim String Literal](./01-Verbatim-String-Literal.md)  
**Next:** [StringBuilder →](./03-StringBuilder.md)
