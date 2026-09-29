# 📚 C# Stack with Examples

> **Trainer's Note:** Stack is LIFO — Last In, First Out. The newest item is the first one removed.

---

## 📑 Table of Contents
1. [What is Stack?](#1-what-is-stack)
2. [Basic Operations with Examples](#2-basic-operations-with-examples)
3. [Useful Members](#3-useful-members)
4. [Real Use Cases](#4-real-use-cases)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is Stack?

`Stack<T>` stores items in **LIFO** order.

- Namespace: `System.Collections.Generic`
- `Push` to add
- `Pop` to remove top
- `Peek` to look at top

### Real-world analogy
```
Stack = plates in a canteen
Last plate placed on top is taken first
Bottom plate waits
```

---

## 2. Basic Operations with Examples

```csharp
using System.Collections.Generic;

Stack<string> pages = new Stack<string>();
pages.Push("Home");
pages.Push("Products");
pages.Push("Cart");

Console.WriteLine(pages.Peek()); // Cart (not removed)
Console.WriteLine(pages.Pop());  // Cart removed
Console.WriteLine(pages.Pop());  // Products removed
Console.WriteLine(pages.Count);  // 1
```

### Loop (top to bottom)
```csharp
foreach (string page in pages)
    Console.WriteLine(page);
```

### Safe pop/peek
```csharp
if (pages.TryPop(out string top))
    Console.WriteLine(top);

if (pages.TryPeek(out string current))
    Console.WriteLine(current);
```

### Order demo
```csharp
Stack<int> s = new();
s.Push(1);
s.Push(2);
s.Push(3);
// Pop order: 3, then 2, then 1
```

---

## 3. Useful Members

| Member | Meaning |
|--------|---------|
| `Push(item)` | add on top |
| `Pop()` | remove + return top |
| `Peek()` | read top |
| `Contains(item)` | exists? |
| `Clear()` | empty |
| `Count` | size |
| `TryPop` / `TryPeek` | no throw if empty |

---

## 4. Real Use Cases

- Browser back-button history
- Undo feature in editors
- Balancing parentheses problems
- Nested operation tracking
- Depth-first style workflows

### Mini undo example
```csharp
Stack<string> undo = new Stack<string>();
undo.Push("Typed A");
undo.Push("Typed B");
string last = undo.Pop(); // undo Typed B
```

### Beginner tip
```
Need latest-first behavior → Stack
Need oldest-first behavior → Queue
Need index list            → List
```

---

## 5. Knowledge Check

1. What does LIFO mean?
2. Difference between Pop and Peek?
3. What does Push do?
4. Write a stack example with 3 page names.
5. Give one real project use case for Stack.

---

**Previous:** [← Hashtable](./09-Hashtable-in-CSharp.md)  
**Next:** [Queue →](./11-Queue-in-CSharp.md)
