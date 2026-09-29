# 📞 C# Delegates

> **Trainer's Note:** A delegate is a type-safe function pointer. It lets you pass methods as values and call them later.

---

## 📑 Table of Contents
1. [What is a Delegate?](#1-what-is-a-delegate)
2. [Declare, Assign, Invoke](#2-declare-assign-invoke)
3. [Multicast Delegates](#3-multicast-delegates)
4. [Func, Action, Predicate](#4-func-action-predicate)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is a Delegate?

A **delegate** defines a method signature and can point to methods matching that signature.

```csharp
delegate int MathOp(int x, int y);
```

### Real-world analogy
```
Delegate = TV remote button slot
  slot expects "volume style button"
  you can assign VolumeUp or VolumeDown method
  pressing slot runs whichever method is assigned
```

---

## 2. Declare, Assign, Invoke

```csharp
delegate int MathOp(int x, int y);

int Add(int a, int b) => a + b;
int Mul(int a, int b) => a * b;

MathOp op = Add;
Console.WriteLine(op(10, 5)); // 15

op = Mul;
Console.WriteLine(op(10, 5)); // 50
```

### Pass delegate as parameter
```csharp
int Compute(int a, int b, MathOp operation)
{
    return operation(a, b);
}

Console.WriteLine(Compute(8, 2, Add));
Console.WriteLine(Compute(8, 2, Mul));
```

---

## 3. Multicast Delegates

One delegate can point to multiple methods (`+=`).

```csharp
delegate void Notify(string message);

void Email(string m) => Console.WriteLine($"Email: {m}");
void Sms(string m) => Console.WriteLine($"SMS: {m}");

Notify notify = Email;
notify += Sms;
notify("Order placed");
// both Email and SMS run
```

Remove with `-=`.

For multicast with return values, only last return is kept. Prefer `void` for notifications.

---

## 4. Func, Action, Predicate

Ready-made generic delegates:

| Type | Meaning | Example |
|------|---------|---------|
| `Action` | void method | `Action<string> log` |
| `Func` | returns value | `Func<int,int,int> add` |
| `Predicate` | returns bool | `Predicate<int> isEven` |

```csharp
Action<string> log = msg => Console.WriteLine(msg);
log("Hello");

Func<int, int, int> add = (a, b) => a + b;
Console.WriteLine(add(2, 3));

Predicate<int> isEven = n => n % 2 == 0;
Console.WriteLine(isEven(4));
```

### Beginner rule
```
Custom delegate type needed rarely today
Most everyday code uses Action / Func / Predicate
Events still use delegates under the hood
```

---

## 5. Knowledge Check

1. What is a delegate?
2. What does multicast mean?
3. Difference between Action and Func?
4. Write a Func that returns square of a number.
5. Why are delegates called type-safe?

---

**Previous:** [← Reflection](./01-Reflection-in-CSharp.md)
**Next:** [Events →](./04-Events-in-CSharp.md)
