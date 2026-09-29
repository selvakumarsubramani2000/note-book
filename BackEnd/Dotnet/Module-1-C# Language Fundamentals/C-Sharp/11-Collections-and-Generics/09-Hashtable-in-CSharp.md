# 🗄️ C# Hashtable

> **Trainer's Note:** Hashtable is the older non-generic key-value collection. Still useful to understand for legacy code and interviews. Prefer Dictionary for new work.

---

## 📑 Table of Contents
1. [What is Hashtable?](#1-what-is-hashtable)
2. [Basic Usage](#2-basic-usage)
3. [Loop and Common Members](#3-loop-and-common-members)
4. [Hashtable vs Dictionary](#4-hashtable-vs-dictionary)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is Hashtable?

`Hashtable` stores key-value pairs as **object**.

- Namespace: `System.Collections`
- Non-generic
- Keys should be unique
- Requires casting when reading typed values

### Real-world analogy
```
Hashtable = old mixed filing cabinet
Can store many labeled folders
Labels/values are loosely typed
You must check what you pull out
```

---

## 2. Basic Usage

```csharp
using System.Collections;

Hashtable table = new Hashtable();
table.Add(101, "Anu");
table.Add(102, "Ravi");
table[103] = "Selva";
table[102] = "Ravi K"; // update

Console.WriteLine(table[101]);          // Anu (object)
string name = (string)table[101];       // cast needed
```

### Contains / remove
```csharp
bool has = table.ContainsKey(101);
table.Remove(103);
Console.WriteLine(table.Count);
```

### Mixed types possible (not recommended style)
```csharp
table.Add("city", "Chennai");
table.Add(1.5, 100);
```

This flexibility often causes runtime cast mistakes.

---

## 3. Loop and Common Members

```csharp
foreach (DictionaryEntry entry in table)
    Console.WriteLine($"{entry.Key} => {entry.Value}");

foreach (var key in table.Keys)
    Console.WriteLine(key);
```

| Member | Meaning |
|--------|---------|
| `Add` | add key/value |
| `Remove` | remove by key |
| `Contains` / `ContainsKey` / `ContainsValue` | search |
| `Keys` / `Values` | sequences |
| `Count` | size |
| `Clear` | remove all |
| `SyncRoot` | old sync helper |

---

## 4. Hashtable vs Dictionary

| Point | Hashtable | Dictionary&lt;TKey,TValue&gt; |
|-------|-----------|-------------------------------|
| Generic | no | yes |
| Type safety | weak | strong |
| Casting | often yes | rarely |
| Performance with value types | boxing cost | better |
| Modern recommendation | legacy | **default choice** |
| Namespace | `System.Collections` | `System.Collections.Generic` |

### Side-by-side
```csharp
// old
Hashtable ht = new Hashtable();
ht.Add(1, "A");
string a = (string)ht[1];

// modern
Dictionary<int, string> dict = new();
dict.Add(1, "A");
string b = dict[1];
```

### Beginner rule
> Learn Hashtable. Use Dictionary in new code.

---

## 5. Knowledge Check

1. Which namespace contains Hashtable?
2. Why is casting common with Hashtable?
3. How do you loop Hashtable entries?
4. Give 3 reasons Dictionary is preferred.
5. Write Hashtable with one int key and string value.

---

**Previous:** [← SortedDictionary](./08-SortedDictionary-in-CSharp.md)  
**Next:** [Stack →](./10-Stack-in-CSharp.md)
