# ⚠️ C# Unsafe Codes

> **Trainer's Note:** Unsafe code allows pointers like C/C++. It is powerful and risky. Most business apps never need it. Learn the idea, use only when required.

---

## 📑 Table of Contents
1. [What is Unsafe Code?](#1-what-is-unsafe-code)
2. [Enable and Basic Syntax](#2-enable-and-basic-syntax)
3. [Pointers and fixed](#3-pointers-and-fixed)
4. [When to Use / Avoid](#4-when-to-use--avoid)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is Unsafe Code?

**Unsafe code** bypasses some normal C# safety checks and allows pointer operations.

```csharp
unsafe
{
    int x = 10;
    int* p = &x;
}
```

### Real-world analogy
```
Safe C# = car with airbags and speed limits
Unsafe  = removing safety covers to tune engine directly
Faster access sometimes, higher chance of damage if wrong
```

---

## 2. Enable and Basic Syntax

### Project enable
```xml
<PropertyGroup>
  <AllowUnsafeBlocks>true</AllowUnsafeBlocks>
</PropertyGroup>
```

Or compile with unsafe option.

### unsafe block / method
```csharp
unsafe void ShowAddress()
{
    int number = 42;
    int* ptr = &number;
    Console.WriteLine(*ptr); // 42
}
```

`&` = address of  
`*` = value at pointer (dereference)

---

## 3. Pointers and fixed

Managed objects can move due to GC, so pin them with `fixed` when taking addresses of fields/arrays.

```csharp
unsafe void ReadArray()
{
    int[] nums = { 10, 20, 30 };

    fixed (int* p = nums)
    {
        Console.WriteLine(*p);       // 10
        Console.WriteLine(*(p + 1)); // 20
    }
}
```

### sizeof
```csharp
unsafe
{
    Console.WriteLine(sizeof(int)); // 4 typically
}
```

### stackalloc (advanced memory on stack)
```csharp
unsafe
{
    int* buffer = stackalloc int[3];
    buffer[0] = 1;
    buffer[1] = 2;
    buffer[2] = 3;
}
```

---

## 4. When to Use / Avoid

### Possible uses
- high-performance interop
- low-level memory manipulation
- some image/binary processing
- working with native APIs

### Avoid in normal business apps
- harder to write correctly
- memory corruption risks
- weaker safety guarantees
- most teams ban it unless proven need

### Beginner rule
```
Default path: safe C#
Need native/perf edge carefully reviewed: unsafe
Prefer Span<T> / safe APIs first in modern .NET
```

---

## 5. Knowledge Check

1. What does unsafe code allow that normal C# restricts?
2. How do you enable unsafe code in a project?
3. What does `fixed` help with?
4. Meaning of `&` and `*` with pointers?
5. Why should beginners avoid unsafe code in daily apps?

---

**Previous:** [← Anonymous Methods](./08-Anonymous-Methods.md)  
**Next:** [Tasks and Parallel Programming →](./10-Tasks-and-Parallel-Programming.md)
