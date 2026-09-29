# 🔃 How to Sort an Array in C# using Array.Sort()

> **Trainer's Note:** `Array.Sort()` sorts elements in place. Learn ascending, descending, partial sort, and when BinarySearch becomes useful.

---

## 📑 Table of Contents
1. [Array.Sort Basics](#1-arraysort-basics)
2. [Sort Strings and Descending Order](#2-sort-strings-and-descending-order)
3. [Partial Sort and BinarySearch](#3-partial-sort-and-binarysearch)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. Array.Sort Basics

`Array.Sort()` sorts elements **in place** (changes the original array).

### Real-world analogy
```
Array.Sort = sorting exam mark sheets from lowest to highest
Array.Reverse after Sort = highest to lowest ranking list
```

### Sort numbers (ascending)
```csharp
int[] scores = { 75, 40, 90, 55, 20 };
Array.Sort(scores);

// Result: 20, 40, 55, 75, 90
foreach (int s in scores)
    Console.Write(s + " ");
```

---

## 2. Sort Strings and Descending Order

### Sort strings
```csharp
string[] names = { "Ravi", "Anu", "Zara", "Bala" };
Array.Sort(names);

// Result: Anu, Bala, Ravi, Zara (alphabetical)
```

### Descending order (easy way)
```csharp
int[] scores = { 75, 40, 90, 55, 20 };
Array.Sort(scores);      // ascending first
Array.Reverse(scores);   // then reverse → descending

// Result: 90, 75, 55, 40, 20
```

---

## 3. Partial Sort and BinarySearch

### Sort only a part of the array
```csharp
int[] data = { 9, 3, 7, 1, 5, 8 };
// Sort 3 elements starting from index 1 → positions 1,2,3
Array.Sort(data, 1, 3);

// data becomes roughly: 9, 1, 3, 7, 5, 8
```

### Tips
- Works for common types: `int`, `string`, `double`, etc.
- For custom objects, you need comparison rules (later topic: `IComparable`)
- After `Sort()`, `BinarySearch` becomes useful for fast lookup

```csharp
int[] scores = { 20, 40, 55, 75, 90 }; // already sorted
int index = Array.BinarySearch(scores, 55);
Console.WriteLine(index); // 2
```

---

## 4. Knowledge Check

1. Sort `{ 12, 5, 9, 1 }` ascending using `Array.Sort`.
2. How do you get descending order using Sort + Reverse?
3. Does `Array.Sort` create a new array or change the same array?
4. Why should BinarySearch usually run on a sorted array?

---

**Previous:** [← Array Class](./02-Array-Class.md)  
**Next:** [Array Rank →](./04-Array-Rank.md)
