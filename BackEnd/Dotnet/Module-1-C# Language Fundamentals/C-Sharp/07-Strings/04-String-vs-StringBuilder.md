# ⚖️ C# String vs StringBuilder

> **Trainer's Note:** Both handle text, but they solve different problems. Choose based on how often text grows.

---

## 📑 Table of Contents
1. [Side-by-Side Comparison](#1-side-by-side-comparison)
2. [When to Use Which](#2-when-to-use-which)
3. [Code Comparison](#3-code-comparison)
4. [Beginner Rule](#4-beginner-rule)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Side-by-Side Comparison

| Point | `string` | `StringBuilder` |
|-------|----------|-----------------|
| Mutable? | No (immutable) | Yes (mutable) |
| Best for | Short text, one-time text work | Many appends / loops |
| Memory in loops | Creates many temporary objects | Updates buffer, fewer temps |
| Namespace | `System` | `System.Text` |
| Easy methods | Very rich string APIs | Focused on building/editing buffer |
| Final output | Already a string | Call `ToString()` |
| Thread-safety | Immutable helps safety | Not thread-safe by default |

---

## 2. When to Use Which

```
Use string when:
  - Reading, comparing, formatting once
  - Email, name, status messages
  - Few concatenations only

Use StringBuilder when:
  - Building a big report in a loop
  - Appending thousands of pieces
  - Generating long CSV / log text dynamically
```

---

## 3. Code Comparison

```csharp
// string — simple and clear
string fullName = firstName + " " + lastName;

// StringBuilder — efficient for repeated growth
StringBuilder sb = new StringBuilder();
foreach (var line in lines)
    sb.AppendLine(line);
string fileContent = sb.ToString();
```

---

## 4. Beginner Rule

> If you concatenate inside a loop many times, use **StringBuilder**.  
> For normal everyday text, use **string**.

### Practical checklist
| Question | Prefer |
|----------|--------|
| Is text mostly fixed/small? | `string` |
| Do I keep adding in a loop? | `StringBuilder` |
| Need Trim/Split/Contains style APIs heavily? | `string` (then maybe build with SB earlier) |
| Final API needs `string`? | SB then `ToString()` |

---

## 5. Knowledge Check

1. Give 3 differences between `string` and `StringBuilder`.
2. Which one is immutable?
3. Which one is better for building a 10,000-line log in a loop?
4. How do you get a final `string` from StringBuilder?
5. For `fullName = first + " " + last`, do you need StringBuilder?

---

**Previous:** [← StringBuilder](./03-StringBuilder.md)  
**Next:** [Tuples in C# →](../Tuples/00-CSharp-Tuple.md)

🎉 **Strings track complete!** Basics, verbatim, String class, StringBuilder, and comparison are now separate clear guides.
