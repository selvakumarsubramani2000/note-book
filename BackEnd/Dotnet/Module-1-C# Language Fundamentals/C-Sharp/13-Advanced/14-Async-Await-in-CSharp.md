# ⏳ Async / Await in C#

> **Trainer's Note:** async/await helps you write non-blocking I/O code that still looks sequential. Perfect for APIs, file/network calls, and scalable services.

---

## 📑 Table of Contents
1. [Why Async/Await?](#1-why-asyncawait)
2. [Basic Syntax](#2-basic-syntax)
3. [Task, Return Types, Exception Flow](#3-task-return-types-exception-flow)
4. [Good Practices](#4-good-practices)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Why Async/Await?

Sync I/O waits and holds a thread:

```csharp
var text = File.ReadAllText("a.txt"); // blocks until done
```

Async frees the thread while waiting:

```csharp
var text = await File.ReadAllTextAsync("a.txt");
```

### Real-world analogy
```
Sync  = stand at door waiting for delivery, doing nothing
Async = give gate pass to security, continue other work
        come back when parcel arrives
```

Goal: better responsiveness and scalability, especially under many concurrent waits.

---

## 2. Basic Syntax

```csharp
public async Task<string> GetMessageAsync()
{
    await Task.Delay(500); // simulate async wait
    return "Hello";
}

string msg = await GetMessageAsync();
Console.WriteLine(msg);
```

### Important keywords
- `async` marks method as asynchronous method
- `await` waits for Task without blocking thread the same way as `.Result`
- awaited method usually returns `Task` / `Task<T>` / `ValueTask`

```csharp
public async Task SaveAsync()
{
    await File.WriteAllTextAsync("log.txt", "ok");
}
```

---

## 3. Task, Return Types, Exception Flow

| Return type | Use |
|-------------|-----|
| `Task` | async method, no return value |
| `Task<T>` | async method returns `T` |
| `void` | event handlers only (avoid elsewhere) |
| `ValueTask` / `ValueTask<T>` | advanced optimization cases |

```csharp
public async Task<int> GetAgeAsync()
{
    await Task.Delay(100);
    return 25;
}
```

### Exceptions
```csharp
try
{
    await GetAgeAsync();
}
catch (Exception ex)
{
    Console.WriteLine(ex.Message);
}
```

Exceptions thrown inside async method are captured into the Task and rethrown at await.

### Run multiple independent calls
```csharp
Task<string> t1 = ReadAAsync();
Task<string> t2 = ReadBAsync();
await Task.WhenAll(t1, t2);
```

---

## 4. Good Practices

| Do | Don't |
|----|-------|
| await I/O calls | block with `.Result` / `.Wait()` in ASP.NET |
| name methods `SomethingAsync` | make everything async with no I/O |
| use try/catch around await | forget cancellation for long calls |
| pass `CancellationToken` in libraries/APIs | mix blocking and async carelessly |

```csharp
public async Task<string> DownloadAsync(CancellationToken ct)
{
    // pass ct to HTTP/file APIs when available
    await Task.Delay(300, ct);
    return "data";
}
```

### Sync over async danger
```csharp
// can deadlock/block request threads in some contexts
var bad = GetMessageAsync().Result;
```

Prefer full async chain from controller/UI down to I/O.

### Beginner rule
```
CPU-only quick method            → normal sync is fine
Waiting on network/file/DB/http  → async/await
UI/API scalability concerns      → async all the way
```

---

## 5. Knowledge Check

1. What problem does async/await solve?
2. Difference between `Task` and `Task<T>`?
3. Why prefer `await` over `.Result`?
4. Write a simple async method that delays and returns a string.
5. When is async not necessary?

---

**Previous:** [← Lambda Expressions](./13-Lambda-Expressions.md)

🎉 **Advanced track complete!** You covered attributes, reflection, properties, delegates, events, generics, enumerable patterns, LINQ, anonymous methods, unsafe code, tasks/parallelism, multithreading, extensions, lambdas, and async/await.
