# 🧮 C# Multidimensional Indexers

> **Trainer's Note:** A multidimensional indexer takes more than one parameter, like a table: row + column. Perfect for grids, seats, and matrices.

---

## 📑 Table of Contents
1. [What is a Multidimensional Indexer?](#1-what-is-a-multidimensional-indexer)
2. [2D Indexer Example](#2-2d-indexer-example)
3. [3D Indexer Idea](#3-3d-indexer-idea)
4. [Tips](#4-tips)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is a Multidimensional Indexer?

A **multidimensional indexer** accepts **two or more parameters**.

```csharp
hall[2, 4] = "Selva";   // row 2, seat 4
```

### Real-world analogy
```
1D indexer   = one locker number
2D indexer   = cinema seat → Row + Seat number
               example: hall[2, 5]
3D indexer   = warehouse floor + row + bin
```

---

## 2. 2D Indexer Example

```csharp
public class CinemaHall
{
    private string[,] seats;

    public CinemaHall(int rows, int cols)
    {
        seats = new string[rows, cols];
    }

    public string this[int row, int col]
    {
        get
        {
            Validate(row, col);
            return seats[row, col] ?? "Empty";
        }
        set
        {
            Validate(row, col);
            seats[row, col] = value;
        }
    }

    private void Validate(int row, int col)
    {
        if (row < 0 || row >= seats.GetLength(0) ||
            col < 0 || col >= seats.GetLength(1))
            throw new ArgumentOutOfRangeException("Invalid seat position");
    }
}
```

### Use it
```csharp
CinemaHall hall = new CinemaHall(5, 10);
hall[2, 4] = "Selva";
hall[0, 0] = "Anu";

Console.WriteLine(hall[2, 4]); // Selva
Console.WriteLine(hall[1, 1]); // Empty
```

---

## 3. 3D Indexer Idea

```csharp
public class StorageCube
{
    private double[,,] storage = new double[3, 3, 3];

    public double this[int x, int y, int z]
    {
        get => storage[x, y, z];
        set => storage[x, y, z] = value;
    }
}

// cube[1, 2, 0] = 9.5;
```

---

## 4. Tips

- Parameter count = dimensions you want
- Always validate indexes
- Great for matrices, grids, game boards, seating charts
- For dictionary-style single key, prefer 1D indexer with string/int key
- Keep get/set logic light and clear

### 1D vs Multidimensional
| Style | Example | Use |
|-------|---------|-----|
| 1D | `obj[i]` | list/order/key |
| 2D | `obj[r, c]` | table/grid |
| 3D | `obj[x, y, z]` | cube/volume/slot map |

---

## 5. Knowledge Check

1. How is a multidimensional indexer different from a normal indexer?
2. Give one real-world example where `obj[row, col]` makes sense.
3. Why should you validate row/col inside get and set?
4. Write a tiny 2D indexer signature for `string this[int r, int c]`.

---

**Previous:** [← C# Indexers](./00-Indexers-in-CSharp.md)  
**Next:** [Overloading of Indexers →](./02-Overloading-of-Indexers.md)
