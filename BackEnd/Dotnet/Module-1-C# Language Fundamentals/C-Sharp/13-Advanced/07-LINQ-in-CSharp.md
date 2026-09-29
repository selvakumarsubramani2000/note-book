# 🔍 LINQ in C#

> **Trainer's Note:** LINQ lets you query collections with clear, readable operations — filter, sort, project, group — without long manual loops.

---

## 📑 Table of Contents
1. [What is LINQ?](#1-what-is-linq)
2. [Method Syntax Essentials](#2-method-syntax-essentials)
3. [Query Syntax](#3-query-syntax)
4. [Deferred Execution](#4-deferred-execution)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is LINQ?

**LINQ = Language Integrated Query**

Works on any `IEnumerable<T>` (and more providers like EF Core).

```csharp
int[] nums = { 5, 3, 8, 1, 9 };
var result = nums.Where(n => n > 5).OrderBy(n => n);
```

### Real-world analogy
```
LINQ = smart assistant for a list of files
  show only PDFs
  sort by name
  pick only file names
```

---

## 2. Method Syntax Essentials

```csharp
using System.Linq;

var students = new[]
{
    new { Name = "Anu", Marks = 90 },
    new { Name = "Ravi", Marks = 65 },
    new { Name = "Selva", Marks = 80 }
};

var top = students
    .Where(s => s.Marks >= 80)
    .OrderByDescending(s => s.Marks)
    .Select(s => s.Name)
    .ToList();
```

### Common operators
| Operator | Use |
|----------|-----|
| `Where` | filter |
| `Select` | project/transform |
| `OrderBy` / `ThenBy` | sort |
| `First` / `FirstOrDefault` | one item |
| `Any` / `All` | conditions |
| `Count` / `Sum` / `Average` | aggregates |
| `GroupBy` | grouping |
| `Distinct` | unique |
| `Take` / `Skip` | paging style |

```csharp
bool hasFail = students.Any(s => s.Marks < 40);
double avg = students.Average(s => s.Marks);
var firstTop = students.FirstOrDefault(s => s.Marks > 85);
```

---

## 3. Query Syntax

```csharp
var query =
    from s in students
    where s.Marks >= 80
    orderby s.Marks descending
    select s.Name;
```

Method syntax is more common in modern C# business code; query syntax is useful for joins/grouping readability.

---

## 4. Deferred Execution

Many LINQ operators do not run immediately.

```csharp
var q = students.Where(s => s.Marks > 70); // not executed yet
foreach (var s in q) // executes now
    Console.WriteLine(s.Name);
```

Force immediate execution:

```csharp
var list = q.ToList();
var arr = q.ToArray();
int count = q.Count(); // executes
```

### Tips
- Prefer `FirstOrDefault` over `First` when item may be missing
- Don't over-chain unreadably long LINQ
- In EF Core, understand what runs in DB vs memory
- Use clear variable names for each meaningful step if chain is complex

---

## 5. Knowledge Check

1. What does LINQ help with?
2. Difference between `Where` and `Select`?
3. What is deferred execution?
4. Write LINQ to get even numbers from an int array.
5. When do you use `ToList()`?

---

**Previous:** [← IEnumerable vs IEnumerator](./06-IEnumerable-vs-IEnumerator.md)  
**Next:** [Anonymous Methods →](./08-Anonymous-Methods.md)
