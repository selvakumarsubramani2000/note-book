# 🚀 Top-level Statements in C#

> **Trainer's Note:** Top-level statements let you write a program without a visible `Main` method. Great for small apps, demos, and learning samples.

---

## 📑 Table of Contents
1. [What are Top-level Statements?](#1-what-are-top-level-statements)
2. [Before vs After](#2-before-vs-after)
3. [Args, Await, and Local Functions](#3-args-await-and-local-functions)
4. [When to Use](#4-when-to-use)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What are Top-level Statements?

From **C# 9**, you can put executable code directly in a file.

```csharp
Console.WriteLine("Hello C#");
```

The compiler generates a `Main` entry point for you.

### Real-world analogy
```
Old style = formal letter with header and signature block every time
Top-level = quick sticky note that still gets delivered
```

---

## 2. Before vs After

### Old style
```csharp
namespace Demo;

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Hello");
    }
}
```

### Top-level style
```csharp
Console.WriteLine("Hello");
```

Much less ceremony for console samples and scripts.

---

## 3. Args, Await, and Local Functions

### Command-line args
```csharp
if (args.Length > 0)
    Console.WriteLine($"Hi {args[0]}");
```

### await at top level
```csharp
using var client = new HttpClient();
string html = await client.GetStringAsync("https://example.com");
Console.WriteLine(html.Length);
```

### Local functions still work
```csharp
int Square(int x) => x * x;
Console.WriteLine(Square(5));
```

---

## 4. When to Use

| Good for | Not ideal as only style for |
|----------|-----------------------------|
| Learning demos | Large multi-module systems without structure |
| Small tools | Big business domains needing clear class design |
| Quick prototypes | Shared libraries (libraries don't use app entry points like this) |

### Beginner tips
- One top-level statements file acts as entry point in a project
- You can still create classes/records in other files
- Keep top-level files short and clear

---

## 5. Knowledge Check

1. Do you still need a `Main` method with top-level statements?
2. How do you read command-line args in top-level code?
3. Can you use `await` in top-level statements?
4. Give one good and one weak use case for top-level statements.

---

**Previous:** [← Pattern Matching](./02-Pattern-Matching-Enhancements.md)  
**Next:** [Nullable Reference Types →](./04-Nullable-Reference-Types.md)
