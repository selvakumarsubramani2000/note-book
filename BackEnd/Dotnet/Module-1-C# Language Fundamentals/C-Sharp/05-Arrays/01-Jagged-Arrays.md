# 🧩 Jagged Arrays in C#

> **Trainer's Note:** A jagged array is an array of arrays. Each inner array can have a different length — useful for uneven groups.

---

## 📑 Table of Contents
1. [What is a Jagged Array?](#1-what-is-a-jagged-array)
2. [Example](#2-example)
3. [Jagged vs Rectangular 2D](#3-jagged-vs-rectangular-2d)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. What is a Jagged Array?

A **jagged array** is an **array of arrays**. Each inner array can have a **different length**.

### Real-world analogy
```
Rectangular 2D array = classroom desks in perfect rows (same seats each row)
Jagged array        = train coaches with different seat counts

  Coach 0 → 4 seats
  Coach 1 → 2 seats
  Coach 2 → 5 seats
```

---

## 2. Example

```csharp
// 3 rows, each row can have different length
int[][] teams = new int[3][];

teams[0] = new int[] { 10, 20, 30 };     // 3 players
teams[1] = new int[] { 40, 50 };         // 2 players
teams[2] = new int[] { 60, 70, 80, 90 }; // 4 players

Console.WriteLine(teams[0][1]); // 20
Console.WriteLine(teams[2].Length); // 4

for (int i = 0; i < teams.Length; i++)
{
    Console.Write($"Team {i}: ");
    for (int j = 0; j < teams[i].Length; j++)
        Console.Write(teams[i][j] + " ");
    Console.WriteLine();
}
```

### Access style
```
teams[row][col]
outer index = which inner array
inner index = item inside that array
```

---

## 3. Jagged vs Rectangular 2D

| | Rectangular `[,]` | Jagged `[][]` |
|---|-------------------|---------------|
| Shape | Every row same length | Rows can differ |
| Memory | One block | Separate arrays |
| Use when | Fixed table | Uneven groups (students per class) |
| Access | `arr[r, c]` | `arr[r][c]` |

### When jagged is a good fit
- Students per classroom (different counts)
- Orders per customer (different counts)
- Any list-of-lists where sizes are uneven

---

## 4. Knowledge Check

1. What is a jagged array in one line?
2. Write a jagged array for 2 classrooms: class A has 3 marks, class B has 5 marks.
3. How is jagged different from `int[,]`?
4. How do you print the length of the second inner array?

---

**Previous:** [← Arrays in C#](./00-Arrays-in-CSharp.md)  
**Next:** [Array Class →](./02-Array-Class.md)
