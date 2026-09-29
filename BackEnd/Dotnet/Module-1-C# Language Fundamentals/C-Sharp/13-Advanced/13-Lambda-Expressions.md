# ➡️ Lambda Expressions in C#

> **Trainer's Note:** A lambda is a short way to write an anonymous function. You will see lambdas everywhere in LINQ, events, and modern C#.

---

## 📑 Table of Contents
1. [What is a Lambda?](#1-what-is-a-lambda)
2. [Syntax Forms](#2-syntax-forms)
3. [Lambdas with Func/Action and LINQ](#3-lambdas-with-funcaction-and-linq)
4. [Captures and Tips](#4-captures-and-tips)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is a Lambda?

A **lambda expression** creates a function inline using `=>`.

```csharp
Func<int, int> square = x => x * x;
Console.WriteLine(square(5)); // 25
```

### Real-world analogy
```
Named method = full form to fill
Lambda = quick one-line instruction
  "if number even, keep it"
```

---

## 2. Syntax Forms

### Expression lambda
```csharp
x => x * 2
(x, y) => x + y
() => Console.WriteLine("Hi")
```

### Statement lambda
```csharp
Func<int, int> abs = x =>
{
    if (x < 0) return -x;
    return x;
};
```

### Parameter types optional in many cases
```csharp
Func<int, bool> isEven = n => n % 2 == 0;
Func<int, bool> isEven2 = (int n) => n % 2 == 0;
```

---

## 3. Lambdas with Func/Action and LINQ

```csharp
Action<string> log = msg => Console.WriteLine(msg);
log("Hello");

Func<int, int, int> add = (a, b) => a + b;
```

### LINQ
```csharp
int[] nums = { 1, 2, 3, 4, 5, 6 };

var evens = nums.Where(n => n % 2 == 0).ToList();
var squares = nums.Select(n => n * n).ToList();
int firstBig = nums.First(n => n > 4);
```

### Events
```csharp
service.OrderPlaced += id => Console.WriteLine($"Order {id}");
```

### Compared with anonymous method
```csharp
// older
Func<int, int> f1 = delegate(int x) { return x * x; };
// modern
Func<int, int> f2 = x => x * x;
```

---

## 4. Captures and Tips

Lambdas can use outer variables (closure):

```csharp
int factor = 10;
Func<int, int> mul = n => n * factor;
Console.WriteLine(mul(3)); // 30
```

### Tips
- keep lambdas short and readable
- extract named method if logic becomes big
- be careful capturing loop variables in older patterns
- perfect for filters/projections/callbacks

### Beginner rule
```
Short callback/filter → lambda
Large multi-step process → normal method
```

---

## 5. Knowledge Check

1. What symbol defines a lambda?
2. Write a lambda that returns true for adult age >= 18.
3. Difference between expression and statement lambda?
4. Write LINQ Where using lambda for names starting with A.
5. Why are lambdas common in modern C#?

---

**Previous:** [← Extension Methods](./12-Extension-Methods.md)  
**Next:** [Async Await →](./14-Async-Await-in-CSharp.md)
