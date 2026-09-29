# 🗺️ Dictionary in C#

> **Trainer's Note:** Dictionary is your default key → value map. Think roll number → student name, product code → price.

---

## 📑 Table of Contents
1. [What is Dictionary?](#1-what-is-dictionary)
2. [Basic Usage](#2-basic-usage)
3. [Safe Lookup and Loop](#3-safe-lookup-and-loop)
4. [Useful Members and Tips](#4-useful-members-and-tips)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is Dictionary?

`Dictionary<TKey, TValue>` stores pairs of **unique keys** and values.

- Namespace: `System.Collections.Generic`
- Very fast lookup by key
- Keys unique
- Order not guaranteed

### Real-world analogy
```
Dictionary = phone contacts
Key   = contact name
Value = phone number
Search by name is fast
```

---

## 2. Basic Usage

```csharp
using System.Collections.Generic;

Dictionary<int, string> students = new Dictionary<int, string>();
students.Add(101, "Anu");
students.Add(102, "Ravi");
students[103] = "Selva";   // add
students[102] = "Ravi K";  // update existing key

Console.WriteLine(students[101]); // Anu
Console.WriteLine(students.Count);
```

### Quick init
```csharp
var prices = new Dictionary<string, decimal>
{
    ["Pen"] = 10,
    ["Book"] = 50
};
```

### Duplicate key rule
```csharp
students.Add(101, "New"); // throws if key exists
students[101] = "New";    // updates safely
```

---

## 3. Safe Lookup and Loop

```csharp
// direct access throws if key missing
// Console.WriteLine(students[999]);

if (students.TryGetValue(102, out string name))
    Console.WriteLine(name);
else
    Console.WriteLine("Not found");

if (students.ContainsKey(101))
    Console.WriteLine("101 exists");
```

### Loop
```csharp
foreach (KeyValuePair<int, string> kv in students)
    Console.WriteLine($"{kv.Key} => {kv.Value}");

foreach (var key in students.Keys)
    Console.WriteLine(key);

foreach (var value in students.Values)
    Console.WriteLine(value);
```

---

## 4. Useful Members and Tips

| Member | Meaning |
|--------|---------|
| `Add` | add new key |
| `dict[key] = value` | add or update |
| `Remove(key)` | delete |
| `ContainsKey` / `ContainsValue` | search |
| `TryGetValue` | safe get |
| `Keys` / `Values` | all keys/values |
| `Clear` | remove all |
| `Count` | size |

### Good use cases
- ID → object/name
- cache-like in-memory maps
- counting frequencies
- config style key lookups

```csharp
var freq = new Dictionary<char, int>();
foreach (char c in "banana")
{
    if (!freq.ContainsKey(c)) freq[c] = 0;
    freq[c]++;
}
```

### Beginner tips
- Always think about missing keys → use `TryGetValue`
- Don't depend on dictionary order
- Choose meaningful key types (`int`, `string`, `Guid`)
- For sorted keys, use SortedDictionary/SortedList

---

## 5. Knowledge Check

1. Must dictionary keys be unique?
2. Difference between `Add` and `dict[key] = value`?
3. Why is `TryGetValue` safer?
4. Write a dictionary of city → pincode with 2 entries.
5. Is dictionary order guaranteed?

---

**Previous:** [← SortedSet](./06-SortedSet-in-CSharp.md)  
**Next:** [SortedDictionary →](./08-SortedDictionary-in-CSharp.md)
