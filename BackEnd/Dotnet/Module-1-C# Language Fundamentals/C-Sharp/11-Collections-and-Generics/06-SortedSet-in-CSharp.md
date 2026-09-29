# 📶 SortedSet in C#

> **Trainer's Note:** `SortedSet<T>` keeps values unique and always sorted. Use it when uniqueness + order both matter.

---

## 📑 Table of Contents
1. [What is SortedSet?](#1-what-is-sortedset)
2. [Basic Usage](#2-basic-usage)
3. [Min, Max, and Range](#3-min-max-and-range)
4. [HashSet vs SortedSet](#4-hashset-vs-sortedset)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is SortedSet?

`SortedSet<T>` stores **unique items in sorted order**.

- Namespace: `System.Collections.Generic`
- No duplicates
- Always sorted
- Easy Min/Max

### Real-world analogy
```
SortedSet = unique roll numbers always kept ascending
Add 30, 10, 20
Stored as 10, 20, 30
```

---

## 2. Basic Usage

```csharp
using System.Collections.Generic;

SortedSet<int> scores = new SortedSet<int>();
scores.Add(50);
scores.Add(20);
scores.Add(40);
scores.Add(20); // ignored

foreach (int s in scores)
    Console.WriteLine(s);
// 20 40 50
```

### Strings
```csharp
SortedSet<string> names = new SortedSet<string> { "Ravi", "Anu", "Selva" };
// Anu, Ravi, Selva
```

### Set operations still work
```csharp
var a = new SortedSet<int> { 1, 2, 3 };
var b = new SortedSet<int> { 3, 4 };
a.UnionWith(b); // 1,2,3,4 sorted unique
```

---

## 3. Min, Max, and Range

```csharp
SortedSet<int> scores = new SortedSet<int> { 20, 40, 50, 70 };

Console.WriteLine(scores.Min); // 20
Console.WriteLine(scores.Max); // 70

foreach (int s in scores.GetViewBetween(25, 55))
    Console.WriteLine(s); // 40 50

foreach (int s in scores.Reverse())
    Console.WriteLine(s); // descending
```

### Useful members
| Member | Meaning |
|--------|---------|
| `Add` / `Remove` / `Contains` | basic unique ops |
| `Min` / `Max` | ends |
| `GetViewBetween` | values in range |
| `Reverse()` | descending view |
| `UnionWith` / `IntersectWith` / `ExceptWith` | set math |
| `Count` | size |

---

## 4. HashSet vs SortedSet

| Point | HashSet | SortedSet |
|-------|---------|-----------|
| Unique | yes | yes |
| Order | not guaranteed | always sorted |
| Speed focus | very fast membership | keeps sorted structure |
| Min/Max easy | no | yes |
| Index access | no | no |

### Beginner rule
```
Only unique + fast exists check → HashSet
Unique + sorted / min-max needs → SortedSet
Indexed ordered list            → List
```

---

## 5. Knowledge Check

1. Does SortedSet allow duplicates?
2. How do you get the largest item?
3. What does `GetViewBetween` do?
4. Give one difference from HashSet.
5. Write a SortedSet of 3 marks and print sorted order.

---

**Previous:** [← HashSet](./05-HashSet-in-CSharp.md)  
**Next:** [Dictionary →](./07-Dictionary-in-CSharp.md)
