# 📋 ArrayList in C#

> **Trainer's Note:** ArrayList is the old flexible bag that can grow. Today we usually prefer `List<T>`, but you must know ArrayList because older code and interviews still mention it.

---

## 📑 Table of Contents
1. [What is ArrayList?](#1-what-is-arraylist)
2. [How to Use ArrayList](#2-how-to-use-arraylist)
3. [Casting and Capacity](#3-casting-and-capacity)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. What is ArrayList?

**ArrayList** is a collection that can store **objects of any type** and can **grow or shrink** at runtime.

- Namespace: `System.Collections`
- Stores items as **`object`**
- Size is **dynamic** (not fixed like `int[]`)

### Real-world analogy
```
Array     = fixed row of school lockers (same size forever)
ArrayList = expandable shopping bag

  - You can add more items anytime
  - Bag can hold mixed things (apple, book, key...)
  - But you must check what each item is before using it
```

### Important idea
Because ArrayList stores **`object`**, value types like `int` get **boxed** (wrapped as object) and later **unboxed**. That costs a little performance and can cause type mistakes.

---

## 2. How to Use ArrayList

```csharp
using System.Collections;

ArrayList list = new ArrayList();

// Add items (different types allowed)
list.Add(10);            // int
list.Add("Selva");       // string
list.Add(99.5);          // double
list.Add(true);          // bool

Console.WriteLine(list.Count);   // 4
Console.WriteLine(list[1]);      // Selva

// Insert at index
list.Insert(1, "Chennai");

// Remove
list.Remove("Selva");    // remove by value
list.RemoveAt(0);        // remove by index

// Check and search
bool hasCity = list.Contains("Chennai");
int index = list.IndexOf("Chennai");

// Loop
foreach (object item in list)
    Console.WriteLine(item);

// Clear all
list.Clear();
```

---

## 3. Casting and Capacity

### Casting when reading typed values
```csharp
ArrayList marks = new ArrayList();
marks.Add(80);
marks.Add(90);

int first = (int)marks[0];   // must cast from object → int
```

If the cast is wrong, you get a **runtime error** (`InvalidCastException`).

### Capacity grows automatically
```csharp
ArrayList list = new ArrayList(); // default capacity is small
list.Add(1);
list.Add(2);
// When full, ArrayList creates a bigger internal array and copies items
Console.WriteLine(list.Capacity); // internal space reserved
Console.WriteLine(list.Count);    // actual items present
```

```
Count    = how many items you put in the bag
Capacity = how much space the bag currently reserved
```

### What next in this folder
| File | Topic |
|------|--------|
| ArrayList Class | properties and methods table |
| Array vs ArrayList | comparison + modern `List<T>` advice |

---

## 4. Knowledge Check

1. Which namespace contains `ArrayList`?
2. Why do we often cast values when reading from an ArrayList?
3. What is the difference between `Count` and `Capacity`?
4. Can ArrayList store mixed types? Is that safe?

---

**Previous:** [← Arrays in C#](../Arrays/00-Arrays-in-CSharp.md)
**Next:** [ArrayList Class →](./01-ArrayList-Class.md)
