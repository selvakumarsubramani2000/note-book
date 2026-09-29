# 🧱 C# StringBuilder

> **Trainer's Note:** StringBuilder is for building text step by step, especially inside loops. It avoids creating many temporary string objects.

---

## 📑 Table of Contents
1. [What is StringBuilder?](#1-what-is-stringbuilder)
2. [Basic Usage](#2-basic-usage)
3. [Why It Helps in Loops](#3-why-it-helps-in-loops)
4. [Useful Members](#4-useful-members)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is StringBuilder?

`StringBuilder` builds text efficiently.

- Namespace: `System.Text`
- Mutable (can change content without creating a new string each time)

### Real-world analogy
```
string        = printing a new full letter every small edit
StringBuilder = writing on a whiteboard and erasing/updating freely
```

---

## 2. Basic Usage

```csharp
using System.Text;

StringBuilder sb = new StringBuilder();
sb.Append("Hello");
sb.Append(" ");
sb.Append("Selva");
sb.AppendLine("!");          // adds text + new line
sb.Insert(0, "Hi, ");        // insert at start
sb.Replace("Hi", "Hello");   // replace text
sb.Remove(0, 6);             // remove some chars

string result = sb.ToString();
Console.WriteLine(result);
```

---

## 3. Why It Helps in Loops

```csharp
// ❌ Slow pattern for many joins
string report = "";
for (int i = 1; i <= 1000; i++)
    report += i + ",";   // many temporary strings created

// ✅ Better pattern
StringBuilder sb = new StringBuilder();
for (int i = 1; i <= 1000; i++)
    sb.Append(i).Append(',');
string report = sb.ToString();
```

---

## 4. Useful Members

| Member | Meaning |
|--------|---------|
| `Append` / `AppendLine` | Add text |
| `Insert` | Insert at index |
| `Remove` | Delete a range |
| `Replace` | Replace text |
| `Clear` | Empty content |
| `Length` | Current character count |
| `Capacity` | Reserved internal space |
| `ToString()` | Final normal string |

```csharp
StringBuilder sb = new StringBuilder(100); // start capacity 100
Console.WriteLine(sb.Capacity);
Console.WriteLine(sb.Length);
```

### Beginner tip
Always call `ToString()` when you need a normal `string` result for APIs that expect string.

---

## 5. Knowledge Check

1. Which namespace contains `StringBuilder`?
2. Why is `report += item` inside a large loop often slower?
3. Name 4 useful StringBuilder methods.
4. How do you convert StringBuilder content to `string`?

---

**Previous:** [← String Class](./02-String-Class.md)  
**Next:** [String vs StringBuilder →](./04-String-vs-StringBuilder.md)
