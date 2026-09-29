# 🕵️ C# Anonymous Methods

> **Trainer's Note:** An anonymous method is an inline method without a formal name. Today lambdas are more common, but you should still understand anonymous methods.

---

## 📑 Table of Contents
1. [What is an Anonymous Method?](#1-what-is-an-anonymous-method)
2. [Syntax and Examples](#2-syntax-and-examples)
3. [Anonymous Method vs Lambda](#3-anonymous-method-vs-lambda)
4. [When to Use](#4-when-to-use)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is an Anonymous Method?

A method defined using `delegate` keyword without naming a separate method.

```csharp
Action<string> log = delegate(string msg)
{
    Console.WriteLine(msg);
};
```

### Real-world analogy
```
Named method = saved recipe card with title
Anonymous method = quick handwritten instruction used once
```

---

## 2. Syntax and Examples

```csharp
Func<int, int, int> add = delegate(int a, int b)
{
    return a + b;
};

Console.WriteLine(add(2, 3)); // 5
```

### With no parameters
```csharp
Action hello = delegate
{
    Console.WriteLine("Hello");
};
hello();
```

### Used with events
```csharp
button.Click += delegate(object? sender, EventArgs e)
{
    Console.WriteLine("Clicked");
};
```

### Can ignore unused parameters (older style flexibility)
```csharp
Action<int> print = delegate
{
    Console.WriteLine("Got call");
};
```

---

## 3. Anonymous Method vs Lambda

```csharp
// Anonymous method
Func<int, int> square1 = delegate(int x) { return x * x; };

// Lambda (modern preferred)
Func<int, int> square2 = x => x * x;
```

| Point | Anonymous method | Lambda |
|-------|------------------|--------|
| Keyword | `delegate` | `=>` |
| Style | older/longer | shorter modern |
| Expression form | mostly block | expression or block |
| Everyday use now | less | **preferred** |

Both can be assigned to delegates like `Action`/`Func`.

---

## 4. When to Use

- Reading older C# codebases
- Interview questions about evolution of C#
- Inline short callbacks (though lambda is usually better)

Prefer lambda in new code:

```csharp
list.Where(x => x > 10);
list.ForEach(x => Console.WriteLine(x));
```

---

## 5. Knowledge Check

1. What is an anonymous method?
2. Write one using `delegate`.
3. Convert it to a lambda.
4. Why are lambdas preferred today?
5. Where might you still see anonymous methods?

---

**Previous:** [← LINQ](./07-LINQ-in-CSharp.md)  
**Next:** [Unsafe Codes →](./09-Unsafe-Codes.md)
