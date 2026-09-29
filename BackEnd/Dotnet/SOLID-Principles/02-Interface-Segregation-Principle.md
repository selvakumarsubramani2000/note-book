# 2️⃣ Interface Segregation Principle (ISP)

> **Trainer's Note:** ISP is about not forcing classes to carry "baggage" they don't need. Let's see why fat interfaces cause pain.

---

## 📑 Table of Contents
1. [What is ISP?](#1-what-is-isp)
2. [A Real-World Analogy](#2-a-real-world-analogy)
3. [The Problem — Code Without ISP](#3-the-problem--code-without-isp)
4. [The Solution — Applying ISP](#4-the-solution--applying-isp)
5. [How to Spot ISP Violations](#5-how-to-spot-isp-violations)
6. [Common Beginner Confusions](#6-common-beginner-confusions)
7. [Knowledge Check](#7-knowledge-check)

---

## 1. What is ISP?

> **"Clients should not be forced to depend on interfaces (methods) they do not use."**

In simple words: **Don't create one giant interface with many methods.** Instead, create **small, focused interfaces**, so each class only implements what it actually needs.

"Client" here means **any class that implements or uses an interface**.

---

## 2. A Real-World Analogy

### 🖨️ Think of an Office Machine

```
❌ WITHOUT ISP — One giant "IMachine" interface:
   interface IMachine
   {
       void Print();
       void Scan();
       void Fax();
       void StapleDocuments();
   }

   A simple ink-jet printer is FORCED to implement Scan(), Fax(),
   and StapleDocuments() — even though it physically CANNOT do those things!
   It ends up throwing "NotImplementedException" everywhere. Ugly.

✅ WITH ISP — Small, focused interfaces:
   interface IPrinter    { void Print(); }
   interface IScanner    { void Scan(); }
   interface IFax        { void Fax(); }
   interface IStapler    { void StapleDocuments(); }

   A simple printer implements ONLY IPrinter.
   A high-end "all-in-one" machine implements ALL of them.
   Nobody is forced to implement something they can't do.
```

---

## 3. The Problem — Code Without ISP

```csharp
// ❌ BAD: One fat interface forces unrelated behavior on every implementer
public interface IWorker
{
    void Work();
    void Eat();
    void Sleep();
}

// A human worker can do all three — fine.
public class HumanWorker : IWorker
{
    public void Work()  => Console.WriteLine("Working...");
    public void Eat()   => Console.WriteLine("Eating lunch...");
    public void Sleep() => Console.WriteLine("Taking a nap...");
}

// A robot worker CANNOT eat or sleep — but is FORCED to implement them!
public class RobotWorker : IWorker
{
    public void Work()  => Console.WriteLine("Working 24/7...");
    public void Eat()   => throw new NotImplementedException(); // ❌ forced, meaningless
    public void Sleep() => throw new NotImplementedException(); // ❌ forced, meaningless
}
```

**Why this is bad:**
- `RobotWorker` is forced to implement `Eat()` and `Sleep()` even though it makes no sense
- Anyone calling `robotWorker.Eat()` will get a crash at runtime — a design mistake surfacing too late
- The interface is not truly describing "what a robot can do"

---

## 4. The Solution — Applying ISP

Break the fat interface into **smaller, role-specific interfaces**:

```csharp
// ✅ GOOD: Small, focused interfaces
public interface IWorkable { void Work(); }
public interface IEatable  { void Eat(); }
public interface ISleepable { void Sleep(); }

// Human implements all relevant interfaces
public class HumanWorker : IWorkable, IEatable, ISleepable
{
    public void Work()  => Console.WriteLine("Working...");
    public void Eat()   => Console.WriteLine("Eating lunch...");
    public void Sleep() => Console.WriteLine("Taking a nap...");
}

// Robot implements ONLY what makes sense
public class RobotWorker : IWorkable
{
    public void Work() => Console.WriteLine("Working 24/7...");
    // No Eat() or Sleep() — because it doesn't need them!
}
```

**Now:**
- `RobotWorker` only implements what it can actually do
- No `NotImplementedException` traps
- Code that only needs "workable" behavior can depend on `IWorkable` alone — it doesn't even need to know about `Eat()` or `Sleep()`

```csharp
// A method that only cares about work doesn't need to know about eating/sleeping
public void AssignTask(IWorkable worker)
{
    worker.Work();
}

AssignTask(new HumanWorker()); // ✅ works
AssignTask(new RobotWorker()); // ✅ works
```

---

## 5. How to Spot ISP Violations

| Symptom | What It Means |
|---------|----------------|
| A class implements an interface method with `throw new NotImplementedException();` | 🚩 Clear ISP violation |
| An interface has 10+ unrelated methods | 🚩 Probably should be split |
| You see empty method bodies `{ }` just to "satisfy" an interface | 🚩 The interface is forcing unwanted behavior |
| Adding one new feature to an interface breaks 5 unrelated classes | 🚩 Interface is too broad |

### 💡 Quick Rule of Thumb
> "If implementing an interface makes you write code you don't actually need, the interface is too fat. Split it."

---

## 6. Common Beginner Confusions

| Confusion | Clarification |
|-----------|----------------|
| "ISP means every interface should have only 1 method" | ❌ Not a strict rule — group methods that are always used together |
| "ISP is the same as SRP" | ❌ SRP is about **classes** having one job; ISP is about **interfaces** being focused, so implementers aren't forced into unrelated behavior |
| "Splitting interfaces always adds unnecessary complexity" | ❌ A few small, well-named interfaces are usually easier to understand than one giant one |
| "ISP only applies to interfaces, not abstract classes" | Mostly true — but the same idea (don't force unused behavior) applies to abstract classes too |

---

## 7. Knowledge Check

1. What problem does ISP solve, in your own words?
2. Look at any interface in your project with 5+ methods. Could it be split into smaller ones?
3. Why is `throw new NotImplementedException()` often a sign of an ISP violation?
4. How is ISP different from SRP?

---

**Previous:** [← Single Responsibility Principle](./01-Single-Responsibility-Principle.md)
**Next:** [Open/Closed Principle →](./03-Open-Closed-Principle.md)
