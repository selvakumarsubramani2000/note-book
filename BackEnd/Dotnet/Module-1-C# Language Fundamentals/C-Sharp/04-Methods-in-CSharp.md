# 🔧 Methods in C#

> **Trainer's Note:** Methods are reusable actions. Instead of copying the same steps again and again, put them in a method and call it whenever needed — like a saved recipe.

---

## 📑 Table of Contents
1. [Methods in C#](#1-methods-in-c)
2. [Method Overloading](#2-method-overloading)
3. [Method Overriding](#3-method-overriding)
4. [Function Parameters](#4-function-parameters)
5. [Anonymous Methods](#5-anonymous-methods)
6. [Overloading vs Overriding](#6-overloading-vs-overriding)
7. [Knowledge Check](#7-knowledge-check)

---

## 1. Methods in C#

A **method** is a block of code that does one job and can be called many times.

### Real-world analogy
```
Method = washing-machine program button
  Press "Quick Wash" → same steps run every time
  You don't rewrite wash instructions each day
```

### Basic method structure
```csharp
returnType MethodName(parameterList)
{
    // body
    return value; // if returnType is not void
}
```

### Example
```csharp
public class Calculator
{
    public int Add(int a, int b)
    {
        return a + b;
    }

    public void PrintSum(int a, int b)
    {
        Console.WriteLine(a + b); // void = no return value
    }
}

var calc = new Calculator();
int result = calc.Add(10, 5);   // 15
calc.PrintSum(10, 5);           // prints 15
```

### Why methods matter
- Avoid copy-paste code
- Easier testing
- Clear names explain intent (`CalculateTax`, `SendEmail`)
- One place to fix bugs

---

## 2. Method Overloading

**Overloading** = same method name, **different parameter list**, in the **same class**.

### Real-world analogy
```
"Print" button:
  Print(document)
  Print(document, color)
  Print(document, color, copies)

Same action name, different options.
```

```csharp
public class Printer
{
    public void Print(string text)
    {
        Console.WriteLine(text);
    }

    public void Print(string text, int copies)
    {
        for (int i = 0; i < copies; i++)
            Console.WriteLine(text);
    }

    public void Print(string text, bool isUpperCase)
    {
        Console.WriteLine(isUpperCase ? text.ToUpper() : text);
    }
}
```

### What can differ in overloading?
| Allowed difference | Example |
|--------------------|---------|
| Number of parameters | `Add(int a)` vs `Add(int a, int b)` |
| Type of parameters | `Add(int a, int b)` vs `Add(double a, double b)` |
| Order of types | `Show(string s, int n)` vs `Show(int n, string s)` |

### What is NOT enough?
- Only changing return type → ❌ not overloading
```csharp
// int Add(int a, int b)
// double Add(int a, int b)  ❌ conflict
```

**Compile-time decision:** compiler picks the correct overload based on arguments.

---

## 3. Method Overriding

**Overriding** = child class provides a **new version** of a parent method.

### Real-world analogy
```
Parent rule: MakePayment()
  CreditCard child: pay by card machine
  Upi child: pay by QR scan

Same method name, different actual behavior.
```

```csharp
public class Payment
{
    public virtual void Pay(decimal amount)
    {
        Console.WriteLine($"Paying {amount} (generic)");
    }
}

public class UpiPayment : Payment
{
    public override void Pay(decimal amount)
    {
        Console.WriteLine($"Paying {amount} via UPI");
    }
}

public class CardPayment : Payment
{
    public override void Pay(decimal amount)
    {
        Console.WriteLine($"Paying {amount} via Card");
    }
}

Payment p1 = new UpiPayment();
Payment p2 = new CardPayment();
p1.Pay(100); // UPI version
p2.Pay(100); // Card version
```

### Keywords required
| Keyword | Where | Meaning |
|---------|-------|---------|
| `virtual` | parent method | allows child to override |
| `override` | child method | replaces parent version |
| `base.Pay(...)` | child (optional) | call parent version too |

```csharp
public override void Pay(decimal amount)
{
    base.Pay(amount); // optional parent call
    Console.WriteLine("UPI success SMS sent");
}
```

**Runtime decision:** which method runs depends on the actual object type (polymorphism).

---

## 4. Function Parameters

Parameters are inputs you pass into a method.

### A) Normal (value) parameter
```csharp
void Increase(int number)
{
    number = number + 1; // changes local copy only
}

int x = 10;
Increase(x);
Console.WriteLine(x); // still 10
```

### B) `ref` parameter — pass variable itself (must be initialized)
```csharp
void Increase(ref int number)
{
    number = number + 1;
}

int x = 10;
Increase(ref x);
Console.WriteLine(x); // 11
```

### C) `out` parameter — method will assign value
```csharp
bool TryDivide(int a, int b, out int result)
{
    if (b == 0)
    {
        result = 0;
        return false;
    }
    result = a / b;
    return true;
}

if (TryDivide(10, 2, out int answer))
    Console.WriteLine(answer); // 5
```

### D) `in` parameter — pass by reference but read-only
```csharp
int Square(in int number)
{
    // number = 5; ❌ cannot change
    return number * number;
}
```

### E) `params` — variable number of arguments
```csharp
int Sum(params int[] numbers)
{
    int total = 0;
    foreach (int n in numbers)
        total += n;
    return total;
}

Console.WriteLine(Sum(1, 2, 3));       // 6
Console.WriteLine(Sum(5, 10, 15, 20)); // 50
```

### F) Optional parameters & named arguments
```csharp
void Greet(string name, string city = "Chennai")
{
    Console.WriteLine($"Hello {name} from {city}");
}

Greet("Selva");                 // city uses default
Greet("Selva", "Madurai");
Greet(city: "Delhi", name: "Raj"); // named arguments
```

### Parameter cheat-sheet
| Keyword | Must initialize before call? | Method can assign? | Use case |
|---------|------------------------------|--------------------|----------|
| (normal) | Yes (if using value) | Local copy only | Simple input |
| `ref` | Yes | Yes | Update existing variable |
| `out` | No | Must assign | Return extra results |
| `in` | Yes | No (read-only) | Big structs efficiently |
| `params` | — | — | Flexible argument count |

---

## 5. Anonymous Methods

An **anonymous method** is a method **without a name**, written inline using `delegate`.

### Real-world analogy
```
Sometimes you need a one-time helper.
You don't give that helper a permanent job title.
You just say: "Do this small task now."
```

### Old style: anonymous method
```csharp
Func<int, int, int> add = delegate (int a, int b)
{
    return a + b;
};

Console.WriteLine(add(3, 4)); // 7
```

### Modern style: lambda expression (preferred today)
```csharp
Func<int, int, int> add = (a, b) => a + b;
Console.WriteLine(add(3, 4)); // 7
```

### Useful with callbacks / lists
```csharp
List<int> numbers = new List<int> { 1, 2, 3, 4, 5 };

// anonymous method style
var evenOld = numbers.FindAll(delegate (int n) { return n % 2 == 0; });

// lambda style (same idea, shorter)
var evenNew = numbers.FindAll(n => n % 2 == 0);

foreach (var n in evenNew)
    Console.WriteLine(n); // 2 4
```

### When to use
- Short one-off logic
- Event handlers
- LINQ filters/selectors
- Callbacks

> In modern C#, **lambda expressions** mostly replace anonymous methods. Learn both: anonymous method for understanding, lambda for daily coding.

---

## 6. Overloading vs Overriding

You listed both topics — keep this table clear:

| Point | Overloading | Overriding |
|-------|-------------|------------|
| Where | Same class | Parent + child class |
| Method name | Same | Same |
| Parameters | Must differ | Usually same |
| Keywords | None special | `virtual` + `override` |
| When decided | Compile time | Runtime |
| Purpose | Same action, different inputs | Same action, different behavior in child |

```csharp
// Overloading (same class)
void Save(string path) { }
void Save(string path, bool overwrite) { }

// Overriding (parent/child)
class Logger { public virtual void Write(string msg) { } }
class FileLogger : Logger { public override void Write(string msg) { } }
```

---

## 7. Knowledge Check

1. What are the 4 main parts of a method definition?
2. Create 2 overloaded `Area` methods: one for square, one for rectangle.
3. Why do we mark a parent method as `virtual` before overriding?
4. What is the difference between `ref` and `out`?
5. Write a method using `params` that returns the largest number.
6. Rewrite this anonymous method as a lambda: `delegate(int x) { return x * x; }`
7. In one line each: define overloading and overriding.

---

**Previous:** [← OOP Concepts](./03-OOP-Concepts.md)
**Next:** [Arrays in C# →](./Arrays/00-Arrays-in-CSharp.md)

🎉 **Great work!** You now have the C# beginner core: .NET basics → fundamentals → control flow → OOP → methods. Practice each example in a console app.
