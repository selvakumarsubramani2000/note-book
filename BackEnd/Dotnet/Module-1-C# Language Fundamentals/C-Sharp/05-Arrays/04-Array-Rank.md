# 📏 How to Find the Rank of an Array in C#

> **Trainer's Note:** Rank means how many dimensions an array has. It tells you whether you need `arr[i]`, `arr[i,j]`, or more indexes.

---

## 📑 Table of Contents
1. [What is Rank?](#1-what-is-rank)
2. [Using .Rank](#2-using-rank)
3. [GetLength and Why Rank Matters](#3-getlength-and-why-rank-matters)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. What is Rank?

**Rank** = number of **dimensions** of an array.

| Array type | Example | Rank |
|------------|---------|------|
| 1D array | `int[] a = new int[5];` | 1 |
| 2D array | `int[,] m = new int[2, 3];` | 2 |
| 3D array | `int[,,] c = new int[2, 2, 2];` | 3 |
| Jagged | `int[][] j = new int[3][];` | 1 (outer array only) |

### Real-world analogy
```
Rank = how many "directions" you need to address one locker

  1D: locker number only            → Rank 1
  2D: row + column                  → Rank 2
  3D: floor + row + column          → Rank 3
```

---

## 2. Using `.Rank`

```csharp
int[] oneD = new int[5];
int[,] twoD = new int[3, 4];
int[,,] threeD = new int[2, 2, 2];
int[][] jagged = new int[3][];

Console.WriteLine(oneD.Rank);    // 1
Console.WriteLine(twoD.Rank);    // 2
Console.WriteLine(threeD.Rank);  // 3
Console.WriteLine(jagged.Rank);  // 1  (jagged is array-of-arrays)
```

### Why jagged rank is 1
A jagged array is one outer array whose elements are other arrays.  
The outer array itself is still 1-dimensional.

---

## 3. GetLength and Why Rank Matters

```csharp
int[,] table = new int[3, 4];

Console.WriteLine(table.Rank);           // 2 dimensions
Console.WriteLine(table.Length);         // 12 (total elements = 3*4)
Console.WriteLine(table.GetLength(0));   // 3  (rows)
Console.WriteLine(table.GetLength(1));   // 4  (columns)
```

### Why rank matters
- Helps when writing generic array utility methods
- Tells you how many indexes you need: `arr[i]` vs `arr[i, j]` vs `arr[i, j, k]`
- Avoids mistakes when copying or looping multi-dimensional data

---

## 4. Knowledge Check

1. What is the rank of `int[,] grid = new int[4, 5];`?
2. Why is the rank of a jagged array usually 1?
3. Difference between `Length` and `GetLength(0)` on a 2D array?
4. What rank does `int[,,] cube = new int[2,2,2];` have?

---

**Previous:** [← Array.Sort](./03-Array-Sort.md)  
**Next:** [ArrayList in C# →](../ArrayList/00-ArrayList-in-CSharp.md)

🎉 **Arrays track complete!** Basics, jagged arrays, Array class helpers, sorting, and rank are now separate clear guides.
