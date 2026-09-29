# 🧵 Tasks and Parallel Programming in C#

> **Trainer's Note:** Tasks represent units of asynchronous/parallel work. Parallel programming runs CPU work across multiple cores when it helps.

---

## 📑 Table of Contents
1. [Task Basics](#1-task-basics)
2. [Start and Wait for Tasks](#2-start-and-wait-for-tasks)
3. [Parallel Programming Helpers](#3-parallel-programming-helpers)
4. [Practical Tips](#4-practical-tips)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Task Basics

`Task` is a promise of work completion.

Namespace: `System.Threading.Tasks`

```csharp
Task t = Task.Run(() =>
{
    Console.WriteLine("Work in background");
});
```

### Real-world analogy
```
Task = food order token
You place order (start work)
Do other things
Later collect food when ready (await/result)
```

`Task<T>` returns a value:

```csharp
Task<int> compute = Task.Run(() => 10 + 20);
```

---

## 2. Start and Wait for Tasks

```csharp
Task task = Task.Run(() =>
{
    Thread.Sleep(500);
    Console.WriteLine("Done");
});

task.Wait(); // block until finished (avoid in UI/ASP.NET request path when possible)
```

```csharp
Task<int> numberTask = Task.Run(() => 42);
int value = numberTask.Result; // blocks; prefer await in async code
Console.WriteLine(value);
```

### Multiple tasks
```csharp
Task t1 = Task.Run(() => Console.WriteLine("A"));
Task t2 = Task.Run(() => Console.WriteLine("B"));
Task.WaitAll(t1, t2);
```

### Continuation
```csharp
Task.Run(() => 5)
    .ContinueWith(t => Console.WriteLine(t.Result * 2));
```

In modern code, prefer `async/await` over manual `ContinueWith` for clarity.

---

## 3. Parallel Programming Helpers

For CPU-bound loops over independent work:

```csharp
using System.Threading.Tasks;

Parallel.For(0, 5, i =>
{
    Console.WriteLine($"Index {i} on thread {Thread.CurrentThread.ManagedThreadId}");
});

var items = new List<int> { 1, 2, 3, 4, 5 };
Parallel.ForEach(items, n =>
{
    Console.WriteLine(n * n);
});
```

### PLINQ (parallel LINQ)
```csharp
var squares = Enumerable.Range(1, 20)
    .AsParallel()
    .Select(x => x * x)
    .ToList();
```

---

## 4. Practical Tips

| Scenario | Prefer |
|----------|--------|
| I/O wait (HTTP, file, DB) | async/await Task |
| Heavy CPU independent chunks | Parallel / PLINQ carefully |
| Simple sequential business logic | no forced parallelism |

### Watch out
- not all work becomes faster when parallelized
- shared data needs thread-safety
- exceptions in parallel loops need care
- over-parallelism can slow systems

### Beginner rule
```
Waiting for external resources → async Task
CPU crunch on many independent items → consider Parallel
Always measure; don't parallelize blindly
```

---

## 5. Knowledge Check

1. What is a Task?
2. Difference between `Task` and `Task<T>`?
3. What does `Task.Run` do?
4. When is `Parallel.ForEach` useful?
5. Why not always use parallel code?

---

**Previous:** [← Unsafe Codes](./09-Unsafe-Codes.md)  
**Next:** [Multithreading →](./11-Multithreading-in-CSharp.md)
