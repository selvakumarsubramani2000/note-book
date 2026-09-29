# 🧬 Generics and Generic Classes in C#

> **Trainer's Note:** Generics let you write one reusable design and plug in the real type later (`int`, `string`, `Order`). This is why `List<T>` is safe and powerful.

---

## 📑 Table of Contents
1. [What are Generics?](#1-what-are-generics)
2. [Generic Methods](#2-generic-methods)
3. [Generic Classes](#3-generic-classes)
4. [Constraints (Simple)](#4-constraints-simple)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What are Generics?

**Generics** use a type placeholder (often `T`) and replace it with a real type when used.

```csharp
List<int> a = new List<int>();         // T = int
List<string> b = new List<string>();   // T = string
```

### Real-world analogy
```
Generic = reusable box template Box<T>
  Box<Eggs>
  Box<Pens>
Same design, different allowed content.
No accidental "pen inside egg box".
```

### Benefits
| Without generics | With generics |
|------------------|---------------|
| `ArrayList` stores `object` | `List<int>` stores only int |
| Casting needed | Usually no cast |
| Runtime type bugs | Compile-time checks |
| Boxing costs | Better for value types |

---

## 2. Generic Methods

```csharp
public static void Swap<T>(ref T left, ref T right)
{
    T temp = left;
    left = right;
    right = temp;
}

int x = 10, y = 20;
Swap(ref x, ref y);

string a = "A", b = "B";
Swap(ref a, ref b); // same method, different type
```

Compiler infers `T` from arguments in many cases.

---

## 3. Generic Classes

```csharp
public class Box<T>
{
    private T _item;

    public void Put(T value) => _item = value;
    public T Take() => _item;
}

Box<int> numberBox = new Box<int>();
numberBox.Put(100);
Console.WriteLine(numberBox.Take());

Box<string> textBox = new Box<string>();
textBox.Put("Hello");
```

### Two type parameters
```csharp
public class Pair<TKey, TValue>
{
    public TKey Key { get; set; }
    public TValue Value { get; set; }
}

var pair = new Pair<int, string> { Key = 1, Value = "Pen" };
```

This is the same idea used by `Dictionary<TKey, TValue>`.

---

## 4. Constraints (Simple)

Constraints limit what `T` is allowed to be.

```csharp
// T must be a reference type
public class Repo<T> where T : class { }

// T must have parameterless constructor
public class Factory<T> where T : new()
{
    public T Create() => new T();
}

// T must implement an interface
public class Sorter<T> where T : IComparable<T>
{
    public int Compare(T a, T b) => a.CompareTo(b);
}
```

### Common constraints
| Constraint | Meaning |
|------------|---------|
| `where T : class` | reference type |
| `where T : struct` | value type |
| `where T : new()` | has empty constructor |
| `where T : BaseType` | inherits/implements type |
| `where T : IComparable<T>` | can compare |

### Beginner rule of thumb
```
Need one algorithm/class for many types → Generics
Need storage for many typed items       → Generic collections
Need old object-based collections only  → legacy scenarios
```

---

## 5. Knowledge Check

1. What does `T` mean in `List<T>`?
2. Write a tiny generic class `Box<T>` with Put/Take.
3. Why is `List<int>` safer than `ArrayList` for numbers?
4. What does `where T : class` mean?
5. Give one real example of two type parameters.

---

**Previous:** [← Collection Class](./01-Collection-Class-in-CSharp.md)  
**Next:** [List Implementation →](./03-List-Implementation.md)
