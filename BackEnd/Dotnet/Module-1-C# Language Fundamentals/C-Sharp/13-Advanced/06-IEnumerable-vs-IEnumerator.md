# 🔁 IEnumerable vs IEnumerator in C#

> **Trainer's Note:** These two interfaces power `foreach`. One says "I can be looped". The other is the actual cursor moving item by item.

---

## 📑 Table of Contents
1. [Big Picture](#1-big-picture)
2. [IEnumerable](#2-ienumerable)
3. [IEnumerator](#3-ienumerator)
4. [Side-by-Side and foreach](#4-side-by-side-and-foreach)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Big Picture

```csharp
foreach (var item in list)
{
    Console.WriteLine(item);
}
```

Behind the scenes:
1. get enumerator from collection
2. call `MoveNext()`
3. read `Current`
4. repeat until finished

### Real-world analogy
```
IEnumerable = a book
IEnumerator = a bookmark/reader finger
  MoveNext → go next page
  Current  → read current page
```

---

## 2. IEnumerable

`IEnumerable` / `IEnumerable<T>` means the object can be enumerated.

```csharp
IEnumerable<int> numbers = new List<int> { 1, 2, 3 };
foreach (int n in numbers)
    Console.WriteLine(n);
```

Key member:

```csharp
IEnumerator<T> GetEnumerator();
```

Most collections implement this: `List<T>`, arrays, etc.

### LINQ works on IEnumerable
```csharp
var even = numbers.Where(n => n % 2 == 0);
```

---

## 3. IEnumerator

`IEnumerator` / `IEnumerator<T>` is the iterator object.

Members:
- `bool MoveNext()`
- `T Current { get; }`
- `void Reset()` (less used)

```csharp
IEnumerable<string> cities = new[] { "Chennai", "Mumbai", "Delhi" };
using IEnumerator<string> e = cities.GetEnumerator();

while (e.MoveNext())
{
    Console.WriteLine(e.Current);
}
```

---

## 4. Side-by-Side and foreach

| Point | IEnumerable | IEnumerator |
|-------|-------------|-------------|
| Role | collection can be looped | cursor during looping |
| Main API | `GetEnumerator()` | `MoveNext`, `Current` |
| You use daily | yes (`foreach`, LINQ) | rarely directly |
| Multiple loops | get new enumerator each foreach | one pass state |

### Manual equivalent of foreach
```csharp
var list = new List<int> { 10, 20, 30 };
var enumerator = list.GetEnumerator();
try
{
    while (enumerator.MoveNext())
    {
        int current = enumerator.Current;
        Console.WriteLine(current);
    }
}
finally
{
    enumerator.Dispose();
}
```

### Beginner rule
```
Need to expose loopable data → return IEnumerable<T>
Need custom iteration logic  → implement enumerator (advanced)
Daily coding                 → foreach + LINQ is enough
```

---

## 5. Knowledge Check

1. What does IEnumerable mean?
2. What does IEnumerator mean?
3. Which members does IEnumerator provide?
4. Why does foreach need both concepts?
5. Why do we usually code against IEnumerable, not IEnumerator?

---

**Previous:** [← Generics](./05-Generics-in-CSharp.md)  
**Next:** [LINQ →](./07-LINQ-in-CSharp.md)
