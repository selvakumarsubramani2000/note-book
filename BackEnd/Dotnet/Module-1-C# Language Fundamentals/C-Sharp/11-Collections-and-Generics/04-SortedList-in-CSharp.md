# 📑 C# SortedList

> **Trainer's Note:** `SortedList` stores key-value pairs and keeps keys sorted automatically. Good when you need map + sorted keys + index access.

---

## 📑 Table of Contents
1. [What is SortedList?](#1-what-is-sortedlist)
2. [Generic SortedList Usage](#2-generic-sortedlist-usage)
3. [Useful Members](#3-useful-members)
4. [SortedList vs Dictionary vs SortedDictionary](#4-sortedlist-vs-dictionary-vs-sorteddictionary)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is SortedList?

`SortedList<TKey, TValue>` is a generic collection of **key → value** pairs sorted by key.

- Namespace: `System.Collections.Generic`
- Keys must be unique
- Always maintains key order
- Can access by key and by index

### Real-world analogy
```
SortedList = dictionary always arranged A to Z
Insert words in any order
Pages remain sorted by word
```

---

## 2. Generic SortedList Usage

```csharp
using System.Collections.Generic;

SortedList<int, string> students = new SortedList<int, string>();
students.Add(103, "Ravi");
students.Add(101, "Anu");
students.Add(102, "Selva");

foreach (var kv in students)
    Console.WriteLine($"{kv.Key} => {kv.Value}");
// Keys appear as 101, 102, 103
```

### Access
```csharp
Console.WriteLine(students[101]);            // by key
Console.WriteLine(students.Keys[0]);         // 101
Console.WriteLine(students.Values[0]);       // Anu
Console.WriteLine(students.IndexOfKey(102)); // 1
```

### Update / remove / check
```csharp
students[102] = "Selva K";
students.Remove(103);
bool hasKey = students.ContainsKey(101);
bool hasVal = students.ContainsValue("Anu");
```

### Safe get
```csharp
if (students.TryGetValue(101, out string name))
    Console.WriteLine(name);
```

### Older non-generic SortedList
```csharp
using System.Collections;

SortedList old = new SortedList();
old.Add("b", 2);
old.Add("a", 1); // sorted by key, values are object
```

Prefer generic version in new code.

---

## 3. Useful Members

| Member | Meaning |
|--------|---------|
| `Add(key, value)` | add pair |
| `Remove(key)` | remove by key |
| `ContainsKey` / `ContainsValue` | search |
| `Keys` / `Values` | key/value lists |
| `IndexOfKey` / `IndexOfValue` | index lookup |
| `TryGetValue` | safe read |
| `Count` | number of pairs |

---

## 4. SortedList vs Dictionary vs SortedDictionary

| Point | Dictionary | SortedList | SortedDictionary |
|-------|------------|------------|------------------|
| Order | not guaranteed | sorted by key | sorted by key |
| Index access | no | yes (key/value by index) | no |
| Fast plain lookup | excellent | good | good |
| Many insert/remove | great | can be heavier | often better than SortedList |
| Best for | general map | sorted map + index needs | sorted map + frequent updates |

### Beginner rule
```
Need fastest key lookup, order not needed → Dictionary
Need sorted keys + index style access     → SortedList
Need sorted keys + many inserts/removes   → SortedDictionary
```

---

## 5. Knowledge Check

1. Are SortedList keys unique?
2. What order does SortedList keep?
3. How do you read value by key?
4. How is SortedList different from Dictionary?
5. Write a SortedList of rollNo → name with 2 students.

---

**Previous:** [← List](./03-List-Implementation.md)  
**Next:** [HashSet →](./05-HashSet-in-CSharp.md)
