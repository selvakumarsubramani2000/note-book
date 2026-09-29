# 🧰 Array Class in C#

> **Trainer's Note:** Every array is based on `System.Array`. That class gives ready helper methods so you don't rebuild common operations by hand.

---

## 📑 Table of Contents
1. [What is the Array Class?](#1-what-is-the-array-class)
2. [Common Members](#2-common-members)
3. [Examples](#3-examples)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. What is the Array Class?

In C#, every array is based on the **`System.Array`** class.

### Real-world analogy
```
Array class = toolbox for locker rows
  Sort, Reverse, Find, Copy, Clear are ready tools
  You don't rebuild these tools by hand every time
```

---

## 2. Common Members

| Member | What it does |
|--------|----------------|
| `Length` | Total number of elements |
| `Rank` | Number of dimensions |
| `Array.Sort(arr)` | Sorts elements |
| `Array.Reverse(arr)` | Reverses order |
| `Array.IndexOf(arr, value)` | Finds first index of a value |
| `Array.BinarySearch(arr, value)` | Fast search (array must be sorted) |
| `Array.Clear(arr, start, count)` | Sets range to default values |
| `Array.Copy(source, dest, length)` | Copies elements |
| `Array.Resize(ref arr, newSize)` | Creates new size (copies old data) |

---

## 3. Examples

```csharp
int[] nums = { 5, 2, 8, 1 };

Console.WriteLine(nums.Length);              // 4
Console.WriteLine(Array.IndexOf(nums, 8));   // 2

Array.Reverse(nums); // { 1, 8, 2, 5 }

int[] copy = new int[4];
Array.Copy(nums, copy, 4);

Array.Clear(copy, 0, 2); // first 2 items become 0
```

### Tips
- `Length` is one of the most used members
- Prefer `Array.*` helpers for clear, standard operations
- `Resize` does not truly grow the same array object; it creates a new underlying storage

---

## 4. Knowledge Check

1. Name 4 useful methods from the `Array` class.
2. What does `Array.IndexOf` return if value is missing? (conceptually -1)
3. What does `Array.Clear` do?
4. Why might `Resize` be needed if arrays are fixed size?

---

**Previous:** [← Jagged Arrays](./01-Jagged-Arrays.md)  
**Next:** [Array.Sort →](./03-Array-Sort.md)
