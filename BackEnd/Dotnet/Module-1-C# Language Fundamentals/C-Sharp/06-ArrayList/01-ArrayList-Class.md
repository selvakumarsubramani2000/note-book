# 🧩 ArrayList Class

> **Trainer's Note:** The ArrayList class gives properties and methods to manage a dynamic object list. Learn the important members you will use and see in interviews.

---

## 📑 Table of Contents
1. [Useful Properties](#1-useful-properties)
2. [Useful Methods](#2-useful-methods)
3. [Sort, Reverse, and Warnings](#3-sort-reverse-and-warnings)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. Useful Properties

| Property | Meaning |
|----------|---------|
| `Count` | Number of items currently stored |
| `Capacity` | Internal storage size reserved |
| `IsFixedSize` | Whether size is fixed |
| `IsReadOnly` | Whether list can be changed |
| `Item[index]` / `[index]` | Get or set value at index |

```csharp
using System.Collections;

ArrayList list = new ArrayList();
list.Add("A");
list.Add("B");

Console.WriteLine(list.Count);     // 2
Console.WriteLine(list.Capacity);  // reserved slots
Console.WriteLine(list[0]);        // A
```

---

## 2. Useful Methods

| Method | What it does |
|--------|----------------|
| `Add(object)` | Adds item at the end |
| `Insert(index, object)` | Inserts item at position |
| `Remove(object)` | Removes first matching value |
| `RemoveAt(index)` | Removes item at index |
| `RemoveRange(index, count)` | Removes a range |
| `Clear()` | Removes all items |
| `Contains(object)` | Checks if value exists |
| `IndexOf(object)` | Finds first index of value |
| `LastIndexOf(object)` | Finds last index of value |
| `Sort()` | Sorts items (same type works best) |
| `Reverse()` | Reverses order |
| `ToArray()` | Converts to object array |
| `Clone()` | Creates a shallow copy |
| `BinarySearch(object)` | Fast search (list should be sorted) |

### Quick demo
```csharp
ArrayList cities = new ArrayList();
cities.Add("Chennai");
cities.Insert(0, "Mumbai");
bool has = cities.Contains("Chennai");
int i = cities.IndexOf("Mumbai");
cities.RemoveAt(0);
object[] arr = cities.ToArray();
```

---

## 3. Sort, Reverse, and Warnings

### Sort and Reverse example
```csharp
ArrayList nums = new ArrayList() { 40, 10, 30, 20 };
nums.Sort();     // 10, 20, 30, 40
nums.Reverse();  // 40, 30, 20, 10
```

### Mixing types warning
```csharp
ArrayList mixed = new ArrayList() { 10, "A", 20 };
// mixed.Sort();  // can throw error — items are not comparable together
```

Sort works best when items are the **same comparable type**.

### Beginner tips
- Prefer same-type content even in ArrayList
- Check `Contains` before assumptions
- Remember casts when reading value types/strings from `object`
- For new code, prefer `List<T>` over ArrayList

---

## 4. Knowledge Check

1. Difference between `Count` and `Capacity`?
2. Difference between `Remove` and `RemoveAt`?
3. What can go wrong if ArrayList stores mixed types and you call `Sort()`?
4. Name 5 useful ArrayList methods.
5. What does `ToArray()` return?

---

**Previous:** [← ArrayList in C#](./00-ArrayList-in-CSharp.md)  
**Next:** [Array vs ArrayList →](./02-Array-vs-ArrayList.md)
