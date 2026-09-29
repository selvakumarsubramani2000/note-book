# 3️⃣ Open/Closed Principle (OCP)

> **Trainer's Note:** OCP protects your tested, working code from being touched every time a new requirement shows up. Let's see how.

---

## 📑 Table of Contents
1. [What is OCP?](#1-what-is-ocp)
2. [A Real-World Analogy](#2-a-real-world-analogy)
3. [The Problem — Code Without OCP](#3-the-problem--code-without-ocp)
4. [The Solution — Applying OCP](#4-the-solution--applying-ocp)
5. [How to Spot OCP Violations](#5-how-to-spot-ocp-violations)
6. [Common Beginner Confusions](#6-common-beginner-confusions)
7. [Knowledge Check](#7-knowledge-check)

---

## 1. What is OCP?

> **"Software entities (classes, modules, functions) should be OPEN for extension, but CLOSED for modification."**

In simple words:
- **Open for extension** → You should be able to **add new behavior**
- **Closed for modification** → You should **NOT need to edit existing, already-tested code** to add that new behavior

The goal is to add new features by **writing new code**, not by **rewriting old code**.

---

## 2. A Real-World Analogy

### 🔌 Think of an Electrical Wall Socket

```
❌ WITHOUT OCP — Rewiring the wall every time:
   You buy a new appliance (like a hair dryer).
   Instead of just plugging it in, an electrician has to
   REWIRE the entire wall to support this one new appliance!
   Every new gadget = rewire the house. Risky and slow.

✅ WITH OCP — Standard socket, any plug fits:
   The wall socket is a standard interface.
   Any new appliance with a matching plug can be added
   WITHOUT touching the wall's existing wiring.
   New appliance = just plug it in. Old wiring untouched.
```

Your code should behave like the socket: stable and unchanged, while new "appliances" (features) plug in safely.

---

## 3. The Problem — Code Without OCP

```csharp
// ❌ BAD: Every time we add a new discount type, we must EDIT this class
public class DiscountCalculator
{
    public decimal CalculateDiscount(string customerType, decimal amount)
    {
        if (customerType == "Regular")
        {
            return amount * 0.05m;
        }
        else if (customerType == "Premium")
        {
            return amount * 0.10m;
        }
        // 🚩 To add "VIP" discount, we must MODIFY this method again!
        // else if (customerType == "VIP") { return amount * 0.20m; }

        return 0;
    }
}
```

**Why this is bad:**
- Every new customer type means editing this method → risk of breaking existing, working discount logic
- The more `if/else` branches you add, the harder it is to test and maintain
- This class is never truly "done" — it keeps growing forever

---

## 4. The Solution — Applying OCP

Use **abstraction (interface) + polymorphism** so new behavior is added via **new classes**, not by editing old ones:

```csharp
// ✅ GOOD: Define an abstraction
public interface IDiscountStrategy
{
    decimal CalculateDiscount(decimal amount);
}

// Existing, tested implementations — CLOSED for modification
public class RegularCustomerDiscount : IDiscountStrategy
{
    public decimal CalculateDiscount(decimal amount) => amount * 0.05m;
}

public class PremiumCustomerDiscount : IDiscountStrategy
{
    public decimal CalculateDiscount(decimal amount) => amount * 0.10m;
}

// ✅ NEW requirement? Just ADD a new class — no existing code touched!
public class VipCustomerDiscount : IDiscountStrategy
{
    public decimal CalculateDiscount(decimal amount) => amount * 0.20m;
}

// The calculator now depends on the ABSTRACTION, not specific types
public class DiscountCalculator
{
    public decimal CalculateDiscount(IDiscountStrategy strategy, decimal amount)
    {
        return strategy.CalculateDiscount(amount);
    }
}
```

**Usage:**
```csharp
var calculator = new DiscountCalculator();
decimal discount = calculator.CalculateDiscount(new VipCustomerDiscount(), 1000m);
// DiscountCalculator class was NEVER modified to support VIP!
```

**Now:**
- Adding "VIP" (or "Student", "Employee", etc.) discount = create a **new class**
- `DiscountCalculator` and all existing discount classes remain **untouched and safe**
- Old, tested code stays tested — new code is isolated and easy to test independently

---

## 5. How to Spot OCP Violations

| Symptom | What It Means |
|---------|----------------|
| Long `if/else` or `switch` chains based on a "type" field | 🚩 Classic OCP violation |
| Every new requirement means editing the same method again and again | 🚩 Not closed for modification |
| Adding a feature requires touching multiple existing classes | 🚩 High risk of regression bugs |
| No interfaces/abstract classes — everything is a concrete class | 🚩 Hard to extend safely |

### 💡 Quick Rule of Thumb
> "If adding a new 'type' or 'case' means editing an existing method, you are violating OCP. Extract an abstraction instead."

---

## 6. Common Beginner Confusions

| Confusion | Clarification |
|-----------|----------------|
| "OCP means I should never touch old code again" | ❌ Bug fixes still require edits. OCP is about **avoiding edits for new features**, not banning all changes |
| "I need to predict every future case in advance" | ❌ You design for **common extension points**, not everything imaginable |
| "OCP always means using interfaces" | Usually yes, but inheritance, delegates, or the Strategy pattern can also achieve it |
| "More abstraction is always better" | ❌ Over-engineering with unnecessary abstractions makes code harder to read. Apply OCP where change is *likely* |

---

## 7. Knowledge Check

1. What do "open for extension" and "closed for modification" mean in your own words?
2. Find an `if/else` or `switch` chain in your project based on a "type". How would you refactor it using OCP?
3. Why does OCP reduce the risk of breaking existing, tested features?
4. Is it possible to apply OCP without using an interface? How?

---

**Previous:** [← Interface Segregation Principle](./02-Interface-Segregation-Principle.md)
**Next:** [Liskov Substitution Principle →](./04-Liskov-Substitution-Principle.md)
