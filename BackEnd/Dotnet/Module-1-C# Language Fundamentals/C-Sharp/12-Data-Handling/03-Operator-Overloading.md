# ➕ Operator Overloading in C#

> **Trainer's Note:** Operator overloading lets your custom types use symbols like `+`, `-`, `==` in a natural way. Use it only when it makes code clearer.

---

## 📑 Table of Contents
1. [What is Operator Overloading?](#1-what-is-operator-overloading)
2. [Basic Example](#2-basic-example)
3. [Equality Operators and True/False Care](#3-equality-operators-and-truefalse-care)
4. [Rules and Best Practices](#4-rules-and-best-practices)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is Operator Overloading?

It means giving new meaning to operators for your own class/struct.

```csharp
Money total = m1 + m2; // + works for Money objects
```

### Real-world analogy
```
Without overload:
  total = m1.Add(m2)

With overload:
  total = m1 + m2
  reads like normal math language
```

---

## 2. Basic Example

```csharp
public class Money
{
    public decimal Amount { get; }

    public Money(decimal amount)
    {
        Amount = amount;
    }

    public static Money operator +(Money a, Money b)
    {
        return new Money(a.Amount + b.Amount);
    }

    public static Money operator -(Money a, Money b)
    {
        return new Money(a.Amount - b.Amount);
    }

    public override string ToString() => $"{Amount:C}";
}

Money m1 = new Money(100);
Money m2 = new Money(40);
Money sum = m1 + m2;      // 140
Money diff = m1 - m2;     // 60
```

### Unary operator example
```csharp
public static Money operator -(Money m)
{
    return new Money(-m.Amount);
}

Money discount = -m2; // -40
```

---

## 3. Equality Operators and True/False Care

If you overload `==`, also overload `!=`.

```csharp
public class Point
{
    public int X { get; }
    public int Y { get; }

    public Point(int x, int y)
    {
        X = x; Y = y;
    }

    public static bool operator ==(Point a, Point b)
    {
        if (ReferenceEquals(a, b)) return true;
        if (a is null || b is null) return false;
        return a.X == b.X && a.Y == b.Y;
    }

    public static bool operator !=(Point a, Point b) => !(a == b);

    public override bool Equals(object? obj)
        => obj is Point p && this == p;

    public override int GetHashCode() => HashCode.Combine(X, Y);
}
```

### Comparison pair rule
If you overload `<`, also overload `>` (and usually `<=`, `>=`).

---

## 4. Rules and Best Practices

| Rule | Meaning |
|------|---------|
| Must be `public static` | Operator methods have fixed signature style |
| At least one operand is your type | Cannot redefine `int + int` |
| Some operators come in pairs | `==` with `!=`, `<` with `>` |
| Keep meaning natural | `+` should feel like addition/combine |
| Don't overuse | Confusing overloads hurt readability |

### Operators you can overload (common)
`+ - * / % ++ -- == != < > <= >= & | ^ ! ~ true false`

### Operators you cannot overload
`= . ?. ?? new is as typeof ->` and a few language operators

### When it is a good idea
```
Math-like types: Money, Vector, Matrix, Fraction → good
Business services: OrderService + UserService → bad idea
```

### Beginner rule of thumb
> Overload operators only when the symbol already has clear meaning for your type.

---

## 5. Knowledge Check

1. What does operator overloading mean in one line?
2. Why are operator methods declared `public static`?
3. If you overload `==`, what else should you overload?
4. Give one good and one bad example for operator overloading.
5. Write a `+` overload idea for a `Vector` with `X` and `Y`.

---

**Previous:** [← Enums](./02-Enums-in-CSharp.md)  
**Next:** [Namespaces →](./04-Namespaces-in-CSharp.md)
