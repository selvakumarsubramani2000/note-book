# 4️⃣ Liskov Substitution Principle (LSP)

> **Trainer's Note:** LSP makes sure your inheritance hierarchies actually make sense. A famous "square inherits from rectangle" bug lives here — let's understand why.

---

## 📑 Table of Contents
1. [What is LSP?](#1-what-is-lsp)
2. [A Real-World Analogy](#2-a-real-world-analogy)
3. [The Problem — Code Without LSP](#3-the-problem--code-without-lsp)
4. [The Solution — Applying LSP](#4-the-solution--applying-lsp)
5. [How to Spot LSP Violations](#5-how-to-spot-lsp-violations)
6. [Common Beginner Confusions](#6-common-beginner-confusions)
7. [Knowledge Check](#7-knowledge-check)

---

## 1. What is LSP?

> **"Objects of a subclass should be replaceable with objects of the parent class, without breaking the correctness of the program."**

In simple words: if `B` is a subclass of `A`, then anywhere your code uses `A`, you should be able to plug in a `B` instead — **and everything should still work correctly**.

If substituting the subclass **breaks** something or produces **wrong/unexpected behavior**, that's an LSP violation.

---

## 2. A Real-World Analogy

### 🪑 Think of Office Chairs

```
❌ WITHOUT LSP:
   Base class: "OfficeChair" — promises "You can sit on me safely."
   Subclass: "BrokenChair" — inherits from OfficeChair but COLLAPSES
             when someone sits on it!

   Anyone who picks ANY "OfficeChair" from the storage room expects
   to sit safely. A BrokenChair breaks that promise — it should
   NOT be labeled as an "OfficeChair" at all.

✅ WITH LSP:
   Every class labeled "OfficeChair" (Ergonomic, Wooden, Plastic)
   can be sat on safely, exactly as promised.
   You can swap any of them without surprises.
```

The key idea: **a subclass must honor the promises (behavior/contract) of its parent class.**

---

## 3. The Problem — Code Without LSP

The most famous example: **Rectangle / Square**.

```csharp
// ❌ BAD: Square "IS-A" Rectangle mathematically, but breaks behavior
public class Rectangle
{
    public virtual int Width { get; set; }
    public virtual int Height { get; set; }

    public int GetArea() => Width * Height;
}

// A Square inherits from Rectangle (seems logical, mathematically)
public class Square : Rectangle
{
    public override int Width
    {
        get => base.Width;
        set { base.Width = value; base.Height = value; } // forces both sides equal
    }

    public override int Height
    {
        get => base.Height;
        set { base.Width = value; base.Height = value; } // forces both sides equal
    }
}
```

```csharp
// Code that expects normal Rectangle behavior
public void TestRectangle(Rectangle rect)
{
    rect.Width = 5;
    rect.Height = 10;

    // For any real Rectangle: Area should be 5 * 10 = 50
    Console.WriteLine(rect.GetArea());
}

TestRectangle(new Rectangle());  // ✅ Output: 50 — correct!
TestRectangle(new Square());     // ❌ Output: 100 — WRONG! Because setting Height also changed Width!
```

**Why this is bad:**
- `Square` silently changes the behavior expected from `Rectangle`
- Code written for `Rectangle` produces **wrong results** when a `Square` is substituted
- This breaks LSP — the subclass does **not** honor the parent's contract

---

## 4. The Solution — Applying LSP

Don't force an inheritance relationship just because it "sounds correct" mathematically. Instead, model behavior correctly:

```csharp
// ✅ GOOD: Common abstraction, no false "IS-A" relationship
public interface IShape
{
    int GetArea();
}

public class Rectangle : IShape
{
    public int Width { get; set; }
    public int Height { get; set; }

    public int GetArea() => Width * Height;
}

public class Square : IShape
{
    public int Side { get; set; }

    public int GetArea() => Side * Side;
}
```

```csharp
public void PrintArea(IShape shape)
{
    Console.WriteLine(shape.GetArea());
}

PrintArea(new Rectangle { Width = 5, Height = 10 }); // ✅ 50
PrintArea(new Square { Side = 5 });                  // ✅ 25 — correct, and no surprises!
```

**Now:**
- `Square` and `Rectangle` both implement `IShape` but are **independent** — no false inheritance
- Substituting any `IShape` implementation works predictably
- No hidden side effects when swapping one shape for another

---

## 5. How to Spot LSP Violations

| Symptom | What It Means |
|---------|----------------|
| A subclass overrides a method to do **nothing** (`{ }`) or throw an exception | 🚩 It cannot honor the parent's contract |
| A subclass changes the **meaning** of a property (like `Square` forcing Width = Height) | 🚩 Breaks expected behavior |
| Code has `if (obj is SpecificSubclass) { ... special handling ... }` | 🚩 A sign that substitution isn't working transparently |
| Unit tests written for the base class **fail** when run against a subclass | 🚩 Clear LSP violation |

### 💡 Quick Rule of Thumb
> "If replacing a parent object with a child object changes the correctness of your program, you have an LSP violation."

---

## 6. Common Beginner Confusions

| Confusion | Clarification |
|-----------|----------------|
| "LSP means every subclass must implement every parent method the same way" | ❌ It means behavior must remain **logically consistent** with what the parent promises |
| "If it inherits, it's automatically fine" | ❌ Inheritance is a coding mechanism; LSP is about **behavioral correctness** |
| "Square not inheriting Rectangle is weird" | Mathematically a square IS a rectangle, but in **code behavior**, they don't share the same mutable contract — that's the key lesson |
| "LSP only applies to classes" | It applies to any parent/child relationship — including interfaces and their implementations |

---

## 7. Knowledge Check

1. In your own words, what does it mean for a subclass to "honor the parent's contract"?
2. Why does the classic `Square extends Rectangle` example violate LSP?
3. What is a warning sign in code (`if (obj is X)`) that hints at an LSP violation?
4. How would you redesign a class hierarchy if a subclass cannot logically support a method from its parent?

---

**Previous:** [← Open/Closed Principle](./03-Open-Closed-Principle.md)
**Next:** [Dependency Inversion Principle →](./05-Dependency-Inversion-Principle.md)
