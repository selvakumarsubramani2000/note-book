# 📄 C# List Implementation

> **Trainer's Note:** `List<T>` is the collection you will use most in real projects. It is a dynamic, type-safe, index-based list.

---

## 📑 Table of Contents
1. [What is List&lt;T&gt;?](#1-what-is-listt)
2. [Create and Basic Operations](#2-create-and-basic-operations)
3. [Useful Methods](#3-useful-methods)
4. [Count vs Capacity (Internal Idea)](#4-count-vs-capacity-internal-idea)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is List&lt;T&gt;?

`List<T>` is a **generic dynamic array-like collection**.

- Namespace: `System.Collections.Generic`
- Grows automatically
- Keeps order by index
- Type-safe

### Real-world analogy
```
List = expandable notebook
  page 0, page 1, page 2...
  add more pages anytime
  open any page by number
```

```csharp
List<string> fruits = new List<string>();
```

---

## 2. Create and Basic Operations

```csharp
using System.Collections.Generic;

List<string> fruits = new List<string>();
fruits.Add("Apple");
fruits.Add("Mango");
fruits.Insert(1, "Banana");
fruits.Remove("Mango");
fruits.RemoveAt(0);

Console.WriteLine(fruits.Count);
Console.WriteLine(fruits[0]); // indexer
Console.WriteLine(fruits.Contains("Banana"));
```

### Quick initialization
```csharp
List<int> marks = new List<int> { 80, 70, 95, 60 };
```

### Loop
```csharp
foreach (int m in marks)
    Console.WriteLine(m);

for (int i = 0; i < marks.Count; i++)
    Console.WriteLine($"{i}: {marks[i]}");
```

---

## 3. Useful Methods

| Member | Meaning |
|--------|---------|
| `Add(item)` | add at end |
| `Insert(index, item)` | insert at position |
| `Remove(item)` | remove first match |
| `RemoveAt(index)` | remove by index |
| `Contains(item)` | exists check |
| `IndexOf(item)` | find index |
| `Sort()` | sort ascending |
| `Reverse()` | reverse order |
| `Clear()` | remove all |
| `ToArray()` | convert to array |
| `Find` / `FindAll` | search with condition |

```csharp
List<int> nums = new List<int> { 40, 10, 30, 20 };
nums.Sort();     // 10,20,30,40
nums.Reverse();  // 40,30,20,10

string? name = new List<string> { "Anu", "Selva" }
    .Find(n => n.StartsWith("S"));
```

---

## 4. Count vs Capacity (Internal Idea)

```csharp
List<int> list = new List<int>();
Console.WriteLine(list.Count);     // actual items
Console.WriteLine(list.Capacity);  // reserved internal slots

list.Add(1);
list.Add(2);
// when full, list grows (often doubles) and copies to bigger array
```

```
Count    = bottles currently stored
Capacity = shelf spaces currently reserved
```

You usually care about `Count`. Capacity is an internal performance detail.

### When to use List
- Shopping cart lines
- Student marks
- API result lists
- Any ordered growable same-type data

### When not to force List
- Need unique-only values → HashSet
- Need key-value lookup → Dictionary
- Need LIFO/FIFO → Stack/Queue

---

## 5. Knowledge Check

1. Which namespace contains `List<T>`?
2. Difference between `Add` and `Insert`?
3. What is the difference between Count and Capacity?
4. Write a list of 3 cities and print with foreach.
5. Why is `List<int>` better than `ArrayList` for integers?

---

**Previous:** [← Generics](./02-Generics-and-Generic-Classes.md)  
**Next:** [SortedList →](./04-SortedList-in-CSharp.md)
