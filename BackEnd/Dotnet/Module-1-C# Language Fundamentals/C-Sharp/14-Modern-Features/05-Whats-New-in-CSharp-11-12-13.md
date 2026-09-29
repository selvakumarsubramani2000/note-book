# 🆕 What's New in C# 11 / 12 / 13

> **Trainer's Note:** You don't need every new feature on day one. Learn the useful ones that make real code cleaner — then explore deeper when needed.

---

## 📑 Table of Contents
1. [How to Read "What's New"](#1-how-to-read-whats-new)
2. [C# 11 Highlights](#2-c-11-highlights)
3. [C# 12 Highlights](#3-c-12-highlights)
4. [C# 13 Highlights](#4-c-13-highlights)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. How to Read "What's New"

Each C# version adds language features. Runtime/SDK versions matter too (for example modern .NET releases).

### Real-world analogy
```
Language updates = toolkit upgrades
  new screwdriver heads
  you still use old tools, but new jobs become easier
```

Focus on features that reduce boilerplate and improve safety/readability.

---

## 2. C# 11 Highlights

### Raw string literals
```csharp
string json = """
{
  "name": "Selva"
}
""";
```

### List patterns
```csharp
int[] nums = { 1, 2, 3 };
if (nums is [1, 2, 3]) { }
```

### Required members
```csharp
public class User
{
    public required string Name { get; init; }
}
```

### Other useful ideas in this era
- UTF-8 string literals
- generic math direction (deeper topic)
- more pattern power

---

## 3. C# 12 Highlights

### Primary constructors for classes/structs
```csharp
public class Student(string name, int age)
{
    public string Name { get; } = name;
    public int Age { get; } = age;
}
```

### Collection expressions
```csharp
int[] a = [1, 2, 3];
List<string> names = ["Anu", "Ravi"];
```

### Optional parameters in lambdas and other refinements
```csharp
var add = (int x, int y = 1) => x + y;
```

### Alias any type improvements / cleaner everyday syntax
C# 12 focuses a lot on reducing ceremony for common app code.

---

## 4. C# 13 Highlights

C# 13 continues quality-of-life and advanced capability improvements (exact set depends on your SDK). Common themes:

- more flexible `params` usage improvements
- refinements around locks/threading helpers in modern .NET
- continued pattern/collection experience polish
- better productivity for everyday coding

### Practical approach for learners
```
1) Stay updated with your .NET SDK version
2) Learn 2–3 high-impact features first:
   - collection expressions
   - primary constructors
   - raw strings / required members
3) Use new features only when they improve clarity
```

### Version check tip
```bash
dotnet --version
```

Then match language version in project if needed:
```xml
<LangVersion>latest</LangVersion>
```

---

## 5. Knowledge Check

1. Name two C# 11 features that help with text/data matching.
2. What is a collection expression example?
3. What is a primary constructor benefit?
4. Why should beginners not force every new feature into every file?

---

**Previous:** [← Nullable Reference Types](./04-Nullable-Reference-Types.md)  
**Next:** [Global Usings →](./06-Global-Usings.md)
