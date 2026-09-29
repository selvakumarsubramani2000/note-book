# 🎯 HashSet in C#

> **Trainer's Note:** `HashSet<T>` stores unique values only and is excellent for fast "already exists?" checks.

---

## 📑 Table of Contents
1. [What is HashSet?](#1-what-is-hashset)
2. [Basic Usage](#2-basic-usage)
3. [Set Operations](#3-set-operations)
4. [When to Use HashSet](#4-when-to-use-hashset)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is HashSet?

`HashSet<T>` is a generic collection of **unique items**.

- Namespace: `System.Collections.Generic`
- Duplicates are ignored
- No index like `set[0]`
- Order is not guaranteed

### Real-world analogy
```
HashSet = party guest checklist
Each person enters only once
Door checks very fast: already inside or not?
Order of guests is not important
```

---

## 2. Basic Usage

```csharp
using System.Collections.Generic;

HashSet<string> cities = new HashSet<string>();
cities.Add("Chennai");
cities.Add("Mumbai");
cities.Add("Chennai"); // ignored

Console.WriteLine(cities.Count); // 2
Console.WriteLine(cities.Contains("Mumbai")); // True
cities.Remove("Mumbai");
```

### Initialize
```csharp
HashSet<int> nums = new HashSet<int> { 1, 2, 2, 3, 3 };
// unique: 1,2,3
```

### Remove duplicates from a list
```csharp
List<int> ids = new List<int> { 1, 2, 2, 3, 1 };
HashSet<int> unique = new HashSet<int>(ids);
```

---

## 3. Set Operations

```csharp
HashSet<int> a = new HashSet<int> { 1, 2, 3, 4 };
HashSet<int> b = new HashSet<int> { 3, 4, 5, 6 };

a.UnionWith(b);       // all unique from both

HashSet<int> x = new HashSet<int> { 1, 2, 3, 4 };
HashSet<int> y = new HashSet<int> { 3, 4, 5 };
x.IntersectWith(y);   // common only → 3,4

HashSet<int> p = new HashSet<int> { 1, 2, 3, 4 };
HashSet<int> q = new HashSet<int> { 3, 4 };
p.ExceptWith(q);      // remove matching → 1,2
```

### Useful members
| Member | Meaning |
|--------|---------|
| `Add` | add if new |
| `Remove` | remove item |
| `Contains` | fast exists check |
| `Count` | unique count |
| `UnionWith` | combine unique |
| `IntersectWith` | keep common |
| `ExceptWith` | remove matching |
| `IsSubsetOf` / `IsSupersetOf` | set relation |

---

## 4. When to Use HashSet

Use HashSet when you need:
- Unique IDs / emails / tags
- Fast membership checks
- Duplicate removal
- Set math (union/intersect)

Avoid HashSet when you need:
- Index positions (`[0]`, `[1]`)
- Guaranteed sorted order (use SortedSet)
- Key-value pairs (use Dictionary)

---

## 5. Knowledge Check

1. What happens if you add a duplicate to HashSet?
2. Can you access HashSet by index?
3. Name 3 set operations.
4. Give one real use case for HashSet.
5. How do you make unique values from a List using HashSet?

---

**Previous:** [← SortedList](./04-SortedList-in-CSharp.md)  
**Next:** [SortedSet →](./06-SortedSet-in-CSharp.md)
