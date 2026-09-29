# 🧵 C# Multithreading

> **Trainer's Note:** Multithreading means doing multiple threads of work in one process. It can improve responsiveness and throughput, but shared data needs protection.

---

## 📑 Table of Contents
1. [What is Multithreading?](#1-what-is-multithreading)
2. [Create and Start Threads](#2-create-and-start-threads)
3. [Thread Safety Basics](#3-thread-safety-basics)
4. [Thread vs Task](#4-thread-vs-task)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is Multithreading?

A **thread** is a path of execution. Multithreading runs more than one path.

```csharp
// main thread + worker thread
```

### Real-world analogy
```
One cook cooking all dishes = single thread
Multiple cooks in one kitchen = multithreading
Need coordination so they don't fight over same pan
```

Namespace: `System.Threading`

---

## 2. Create and Start Threads

```csharp
using System.Threading;

void Work(object? name)
{
    for (int i = 1; i <= 3; i++)
    {
        Console.WriteLine($"{name}: step {i}");
        Thread.Sleep(200);
    }
}

Thread t1 = new Thread(Work);
Thread t2 = new Thread(Work);

t1.Start("Worker-A");
t2.Start("Worker-B");

t1.Join(); // wait for finish
t2.Join();
```

### Thread pool (better for many short works)
```csharp
ThreadPool.QueueUserWorkItem(_ =>
{
    Console.WriteLine("Pool work");
});
```

In modern apps, prefer `Task.Run` / async over manual thread management when possible.

---

## 3. Thread Safety Basics

Problem: two threads update same data.

```csharp
int counter = 0;

void Inc()
{
    for (int i = 0; i < 1000; i++)
        counter++; // not safe with multi threads
}
```

### lock
```csharp
object gate = new object();
int counter = 0;

void SafeInc()
{
    for (int i = 0; i < 1000; i++)
    {
        lock (gate)
        {
            counter++;
        }
    }
}
```

### Other tools (know names)
- `Interlocked.Increment`
- `Monitor`
- `Mutex` / `Semaphore` (advanced scenarios)
- concurrent collections (`ConcurrentDictionary`)

---

## 4. Thread vs Task

| Point | Thread | Task |
|-------|--------|------|
| Level | low-level execution path | higher-level work unit |
| Management | manual-ish | runtime schedules efficiently |
| Best modern default | special cases | yes for async/parallel work |
| Extra features | basic | continuations, async ecosystem |

### Beginner rule
```
Learn Thread concepts (race, lock, join)
Build apps mostly with Task + async/await
Use locks/concurrent tools only for shared mutable state
```

### Practical tips
- UI apps: keep UI thread free
- ASP.NET: prefer async I/O, don't block threads
- Never assume print order without synchronization
- Keep critical sections small

---

## 5. Knowledge Check

1. What is a thread?
2. What does `Join` do?
3. Why can `counter++` be unsafe with multiple threads?
4. What does `lock` protect?
5. When prefer Task over manual Thread?

---

**Previous:** [← Tasks and Parallel Programming](./10-Tasks-and-Parallel-Programming.md)  
**Next:** [Extension Methods →](./12-Extension-Methods.md)
