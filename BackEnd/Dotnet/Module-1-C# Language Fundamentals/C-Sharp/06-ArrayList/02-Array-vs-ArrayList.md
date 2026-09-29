# ⚖️ C# | Array vs ArrayList

> **Trainer's Note:** Array and ArrayList look similar, but they behave differently. Knowing the difference is a classic beginner and interview question.

---

## 📑 Table of Contents
1. [Comparison Table](#1-comparison-table)
2. [Side-by-Side Code](#2-side-by-side-code)
3. [Modern Advice](#3-modern-advice)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. Comparison Table

| Point | Array (`int[]`) | ArrayList |
|-------|------------------|-----------|
| **Size** | Fixed after creation | Grows / shrinks dynamically |
| **Type safety** | Strong (only one type) | Weak (stores `object`) |
| **Performance** | Faster for same-type data | Slower (boxing/unboxing) |
| **Syntax** | `int[] a = new int[3];` | `ArrayList list = new ArrayList();` |
| **Add more items** | Cannot grow (need new array) | `Add()` anytime |
| **Casting needed** | No for matching type | Yes when reading typed values |
| **Namespace** | Built-in language feature | `System.Collections` |
| **Dimensions** | 1D, 2D, 3D, jagged supported | Mainly one list of items |
| **Modern choice** | Still useful for fixed data | Prefer `List<T>` instead |

### Real-world picture
```
Array:
  Train with FIXED number of seats
  Only passengers of one type of ticket

ArrayList:
  Bus that can add extra seats
  Can take mixed luggage — but harder to manage safely
```

---

## 2. Side-by-Side Code

```csharp
// ARRAY — fixed, type-safe
int[] scores = new int[3];
scores[0] = 80;
scores[1] = 90;
// scores[3] = 100; // ❌ runtime error (out of range)
// scores.Add(100); // ❌ no Add method

// ARRAYLIST — flexible, not type-safe
ArrayList list = new ArrayList();
list.Add(80);
list.Add(90);
list.Add(100);      // ✅ grows
list.Add("oops");   // ✅ allowed, but dangerous

int x = (int)list[0];     // cast needed
// int y = (int)list[3];  // ❌ crash if index 3 is a string
```

---

## 3. Modern Advice

| Need | Prefer |
|------|--------|
| Fixed size, same type, high speed | **Array** (`int[]`, `string[]`) |
| Growing list, same type, type-safe | **`List<T>`** (modern best choice) |
| Reading old .NET Framework code / interview basics | Know **ArrayList** |
| New production code | Avoid ArrayList; use `List<T>` |

### Modern equivalent of ArrayList
```csharp
// Old style
ArrayList oldList = new ArrayList();
oldList.Add(10);

// Modern style (recommended)
List<int> newList = new List<int>();
newList.Add(10);   // type-safe, no cast needed
```

```
ArrayList  → bag of unknown objects
List<int>  → bag that ONLY accepts integers (safer + faster)
```

### Beginner rule of thumb
> Can an array grow after creation? **No.**  
> Can an ArrayList? **Yes.**  
> For new C# apps needing a growable typed list, use **`List<T>`**.

---

## 4. Knowledge Check

1. Can an array grow after creation? Can an ArrayList?
2. Give 3 differences between Array and ArrayList.
3. Why is `List<T>` preferred over ArrayList in modern C#?
4. Which one needs casting more often when reading values?
5. Which one supports multi-dimensional forms more naturally?

---

**Previous:** [← ArrayList Class](./01-ArrayList-Class.md)  
**Next:** [Strings in C# →](../Strings/00-Strings-in-CSharp.md)

🎉 **ArrayList track complete!** Usage, class members, and Array vs ArrayList comparison are now separate clear guides.
