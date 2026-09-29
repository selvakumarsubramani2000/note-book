# 🧩 Collection Class in C#

> **Trainer's Note:** "Collection class" means the ready-made classes .NET gives you to store groups of items. You don't build add/remove/search logic from zero every time.

---

## 📑 Table of Contents
1. [What is a Collection Class?](#1-what-is-a-collection-class)
2. [Important Interfaces Behind Collections](#2-important-interfaces-behind-collections)
3. [Non-Generic Collection Classes](#3-non-generic-collection-classes)
4. [Generic Collection Classes](#4-generic-collection-classes)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is a Collection Class?

A **collection class** is a built-in type designed to hold multiple objects and manage them.

Examples:
- `ArrayList`, `Hashtable` (old style)
- `List<T>`, `Dictionary<TKey,TValue>` (modern style)

### Real-world analogy
```
Collection class = branded storage box with buttons
  Add item
  Remove item
  Count items
  Search item

You buy the box; you don't invent hinges every time.
```

### What collection classes usually give you
```csharp
Add / Insert
Remove / Clear
Count
Contains
foreach support
Sometimes Sort / Index access / Key access
```

---

## 2. Important Interfaces Behind Collections

Many collection classes implement common interfaces.

| Interface | Simple meaning |
|-----------|----------------|
| `IEnumerable` / `IEnumerable<T>` | Can loop with `foreach` |
| `ICollection` / `ICollection<T>` | Count, Add/Remove style members |
| `IList` / `IList<T>` | Index access (`list[i]`) |
| `IDictionary` / `IDictionary<TKey,TValue>` | Key-value map |

You don't need to memorize every method now. Just know:
> Collection classes share common contracts, so learning one makes the next easier.

```csharp
IEnumerable<string> items = new List<string> { "A", "B" };
foreach (var item in items)
    Console.WriteLine(item);
```

---

## 3. Non-Generic Collection Classes

Namespace: `System.Collections`

| Class | Stores | Notes |
|-------|--------|-------|
| `ArrayList` | objects | dynamic list, casting needed |
| `Hashtable` | key/value objects | old dictionary style |
| `Queue` | objects | FIFO |
| `Stack` | objects | LIFO |
| `SortedList` | key/value objects | sorted keys (non-generic) |

```csharp
using System.Collections;

ArrayList list = new ArrayList();
list.Add(10);
list.Add("Selva");
int n = (int)list[0]; // cast required
```

Use these mainly when reading older code.

---

## 4. Generic Collection Classes

Namespace: `System.Collections.Generic`

| Class | Best for |
|-------|----------|
| `List<T>` | ordered growable list |
| `Dictionary<TKey,TValue>` | fast key lookup |
| `HashSet<T>` | unique values |
| `SortedSet<T>` | unique + sorted |
| `SortedList<TKey,TValue>` | sorted key-value + index style |
| `SortedDictionary<TKey,TValue>` | sorted key-value tree style |
| `Stack<T>` | LIFO |
| `Queue<T>` | FIFO |
| `LinkedList<T>` | node-based inserts |

```csharp
using System.Collections.Generic;

List<int> marks = new List<int> { 70, 80, 90 };
Dictionary<string, int> ages = new() { ["Anu"] = 20 };
```

### Why generic collection classes are better for new projects
- Type safety at compile time
- Less casting
- Better performance for value types
- Clearer intent (`List<Order>` vs `ArrayList`)

---

## 5. Knowledge Check

1. What is a collection class in one sentence?
2. Which namespace is used for modern generic collections?
3. Name 3 generic collection classes.
4. Why does `ArrayList` often need casting?
5. Which interface enables `foreach`?

---

**Previous:** [← Collections in C#](./00-Collections-in-CSharp.md)  
**Next:** [Generics and Generic Classes →](./02-Generics-and-Generic-Classes.md)
