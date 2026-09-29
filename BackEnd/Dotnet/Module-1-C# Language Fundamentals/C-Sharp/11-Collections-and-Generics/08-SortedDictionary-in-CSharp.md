# 🌲 SortedDictionary Implementation in C#

> **Trainer's Note:** `SortedDictionary` is a key-value map that always keeps keys sorted. Use it when sorted traversal matters and you update often.

---

## 📑 Table of Contents
1. [What is SortedDictionary?](#1-what-is-sorteddictionary)
2. [Implementation / Basic Usage](#2-implementation--basic-usage)
3. [Common Operations](#3-common-operations)
4. [SortedDictionary vs SortedList vs Dictionary](#4-sorteddictionary-vs-sortedlist-vs-dictionary)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is SortedDictionary?

`SortedDictionary<TKey, TValue>` stores key-value pairs sorted by key.

- Namespace: `System.Collections.Generic`
- Unique keys
- Sorted key order
- Tree-based implementation idea (good for many inserts/removes)

### Real-world analogy
```
SortedDictionary = contacts always shown A-Z by name
Add people anytime
List stays alphabetically sorted
```

---

## 2. Implementation / Basic Usage

```csharp
using System.Collections.Generic;

SortedDictionary<string, int> marks = new SortedDictionary<string, int>();
marks.Add("Ravi", 80);
marks.Add("Anu", 90);
marks.Add("Selva", 85);

foreach (var kv in marks)
    Console.WriteLine($"{kv.Key}: {kv.Value}");
// Anu, Ravi, Selva
```

### Create with data
```csharp
var data = new SortedDictionary<int, string>
{
    [3] = "C",
    [1] = "A",
    [2] = "B"
};
// keys iterate 1,2,3
```

---

## 3. Common Operations

```csharp
marks["Anu"] = 95; // update
marks.Remove("Ravi");

bool has = marks.ContainsKey("Selva");

if (marks.TryGetValue("Selva", out int score))
    Console.WriteLine(score);

foreach (string key in marks.Keys)
    Console.WriteLine(key);
```

### Useful members
| Member | Meaning |
|--------|---------|
| `Add` | add pair |
| `dict[key] = value` | add/update |
| `Remove` | delete key |
| `ContainsKey` | key exists |
| `TryGetValue` | safe read |
| `Keys` / `Values` | sequences |
| `Count` | size |
| `Clear` | empty all |

---

## 4. SortedDictionary vs SortedList vs Dictionary

| Point | Dictionary | SortedDictionary | SortedList |
|-------|------------|------------------|------------|
| Sorted keys | no | yes | yes |
| Main strength | fastest general lookup | sorted + flexible updates | sorted + index access |
| Index by position | no | no | yes |
| Internal feel | hash map | tree map | array-like pairs |
| Choose when | no sort needed | sorted keys, frequent edits | sorted keys + index needs |

### Beginner rule
```
No sorting needed                 → Dictionary
Need sorted keys, many updates    → SortedDictionary
Need sorted keys + index lookup   → SortedList
```

---

## 5. Knowledge Check

1. Does SortedDictionary keep keys sorted?
2. Are keys unique?
3. Name 3 common operations.
4. When do you pick SortedDictionary over Dictionary?
5. One difference between SortedDictionary and SortedList?

---

**Previous:** [← Dictionary](./07-Dictionary-in-CSharp.md)  
**Next:** [Hashtable →](./09-Hashtable-in-CSharp.md)
