# 🎟️ C# Queue with Examples

> **Trainer's Note:** Queue is FIFO — First In, First Out. The first item added is the first item removed.

---

## 📑 Table of Contents
1. [What is Queue?](#1-what-is-queue)
2. [Basic Operations with Examples](#2-basic-operations-with-examples)
3. [Useful Members](#3-useful-members)
4. [Real Use Cases](#4-real-use-cases)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is Queue?

`Queue<T>` stores items in **FIFO** order.

- Namespace: `System.Collections.Generic`
- `Enqueue` adds at end
- `Dequeue` removes from front
- `Peek` looks at front

### Real-world analogy
```
Queue = ticket counter line
First person in line is served first
New people join at the end
```

---

## 2. Basic Operations with Examples

```csharp
using System.Collections.Generic;

Queue<string> printJobs = new Queue<string>();
printJobs.Enqueue("Doc1");
printJobs.Enqueue("Doc2");
printJobs.Enqueue("Doc3");

Console.WriteLine(printJobs.Peek());    // Doc1
Console.WriteLine(printJobs.Dequeue()); // Doc1 removed
Console.WriteLine(printJobs.Dequeue()); // Doc2 removed
Console.WriteLine(printJobs.Count);     // 1
```

### Loop
```csharp
foreach (string job in printJobs)
    Console.WriteLine(job);
```

### Safe methods
```csharp
if (printJobs.TryDequeue(out string job))
    Console.WriteLine($"Printing {job}");

if (printJobs.TryPeek(out string next))
    Console.WriteLine($"Next is {next}");
```

### Order demo
```csharp
Queue<int> q = new();
q.Enqueue(1);
q.Enqueue(2);
q.Enqueue(3);
// Dequeue order: 1, then 2, then 3
```

---

## 3. Useful Members

| Member | Meaning |
|--------|---------|
| `Enqueue(item)` | add at end |
| `Dequeue()` | remove + return front |
| `Peek()` | read front |
| `Contains(item)` | exists? |
| `Clear()` | empty |
| `Count` | size |
| `TryDequeue` / `TryPeek` | safe versions |

---

## 4. Real Use Cases

- Print / job processing queues
- Customer support ticket lines
- Message processing order
- Breadth-first style processing
- Request throttling pipelines (simple models)

### Mini service-line example
```csharp
Queue<string> counter = new Queue<string>();
counter.Enqueue("Customer-A");
counter.Enqueue("Customer-B");

while (counter.Count > 0)
{
    string current = counter.Dequeue();
    Console.WriteLine($"Serving {current}");
}
```

### Stack vs Queue reminder
```
Stack Push A,B,C → Pop C,B,A
Queue Enqueue A,B,C → Dequeue A,B,C
```

---

## 5. Knowledge Check

1. What does FIFO mean?
2. Difference between Dequeue and Peek?
3. What does Enqueue do?
4. Write a queue with 3 print jobs and process one.
5. Give one real use case for Queue.

---

**Previous:** [← Stack](./10-Stack-in-CSharp.md)  
**Next:** [LinkedList →](./12-LinkedList-in-CSharp.md)
