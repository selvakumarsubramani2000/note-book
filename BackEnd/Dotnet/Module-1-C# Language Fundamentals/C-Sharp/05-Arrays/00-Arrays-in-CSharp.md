# 📦 Arrays in C#

> **Trainer's Note:** An array is a fixed-size box of same-type items. Once you understand arrays, lists and collections become much easier.

---

## 📑 Table of Contents
1. [What is an Array?](#1-what-is-an-array)
2. [Declare, Read, Loop](#2-declare-read-loop)
3. [Important Rules](#3-important-rules)
4. [Multi-dimensional Array (Simple Idea)](#4-multi-dimensional-array-simple-idea)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is an Array?

An **array** stores **multiple values of the same type** in one variable, in a fixed order.

### Real-world analogy
```
Array = a row of lockers in a school corridor

  Locker 0 → "Pen"
  Locker 1 → "Book"
  Locker 2 → "Bag"

  - Same type of lockers (same data type)
  - Each locker has a number (index starts at 0)
  - Total lockers is fixed when built (fixed size)
```

---

## 2. Declare, Read, Loop

### Declare and create
```csharp
// Way 1: declare size, fill later
int[] marks = new int[5];
marks[0] = 80;
marks[1] = 90;

// Way 2: declare + fill together
string[] cities = { "Chennai", "Mumbai", "Delhi" };

// Way 3: new + values
int[] numbers = new int[] { 10, 20, 30, 40 };
```

### Read and loop
```csharp
Console.WriteLine(cities[0]);        // Chennai
Console.WriteLine(cities.Length);    // 3

for (int i = 0; i < cities.Length; i++)
    Console.WriteLine(cities[i]);

foreach (string city in cities)
    Console.WriteLine(city);
```

---

## 3. Important Rules

| Rule | Meaning |
|------|---------|
| Index starts at **0** | First item is `arr[0]` |
| Size is **fixed** | Cannot grow later like a List |
| Same data type | `int[]` cannot store strings |
| Out of range throws error | `arr[100]` on size 3 → crash |

---

## 4. Multi-dimensional Array (Simple Idea)

```csharp
// 2D array = like a table (rows x columns)
int[,] matrix = new int[2, 3]
{
    { 1, 2, 3 },
    { 4, 5, 6 }
};

Console.WriteLine(matrix[1, 2]); // 6 (row 1, column 2)
```

### What next in this folder
| File | Topic |
|------|--------|
| Jagged Arrays | array of arrays with different lengths |
| Array Class | helper methods from `System.Array` |
| Array.Sort | sorting arrays |
| Rank | number of dimensions |

---

## 5. Knowledge Check

1. What is the index of the first element in a C# array?
2. Can an `int[]` array grow after creation? What do you use if you need growth?
3. Write three ways to create an int array with values 1,2,3.
4. What happens if you access an index outside the array length?

---

**Previous:** [← Methods in C#](../04-Methods-in-CSharp.md)  
**Next:** [Jagged Arrays →](./01-Jagged-Arrays.md)
