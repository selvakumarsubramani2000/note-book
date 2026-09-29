# 🚫 C# Restrictions on Properties

> **Trainer's Note:** Properties are powerful, but C# puts clear limits. Learn these restrictions once — they prevent many beginner and interview mistakes.

---

## 📑 Table of Contents
1. [Why Restrictions Matter](#1-why-restrictions-matter)
2. [Main Restrictions](#2-main-restrictions)
3. [Practical Summary Table](#3-practical-summary-table)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. Why Restrictions Matter

Properties look like fields, but they are accessors. Because of that, C# does **not** allow every field-style trick on properties.

### Real-world analogy
```
Property = labeled door on a room
  Door name is fixed (Name, Age, Price)
  You can lock write side (private set)
  Door itself does not take "row, column" args
  For seat-style access, build an indexer room map
```

---

## 2. Main Restrictions

### 1) Property cannot take parameters
```csharp
// ❌ Invalid property style
// public string thisName[int i] { get; set; }

// ✅ For indexed access use an INDEXER:
public string this[int i]
{
    get => items[i];
    set => items[i] = value;
}
```

### 2) Cannot overload properties by parameter list
Properties are identified by **name**, not parameters.  
For multiple ways of access, use methods or indexers.

### 3) `ref` and `out` are not used like method parameters on normal properties
```csharp
// ❌ Invalid beginner idea
// public ref int Mark { get; set; }

// Prefer normal get/set, or carefully designed methods for advanced ref scenarios
```

### 4) A property must have at least get or set
```csharp
public int X { get; set; }     // ✅ read/write
public int Y { get; }          // ✅ get only
public int Z { set { ... } }   // ✅ set only (rare)

// ❌ property with no get and no set is not useful/valid design
```

### 5) Accessors cannot be more accessible than the property
```csharp
// ❌ Invalid idea:
// private string Name { public get; public set; }

// ✅ Valid:
public string Name { get; private set; }
// property is public; set is more restricted (private)
```

### 6) Auto-property restrictions
```csharp
// Auto-property cannot have custom logic in get/set body.
// If you need validation, switch to full property with backing field.

public int Age { get; set; } // auto - no validation possible inside

private int age;
public int AgeSafe
{
    get => age;
    set
    {
        if (value < 0) throw new ArgumentException();
        age = value;
    }
}
```

### 7) Abstract / override / virtual rules (inheritance)
```csharp
public abstract class Shape
{
    public abstract double Area { get; } // no body in abstract property
}

public class Square : Shape
{
    public double Side { get; set; }
    public override double Area => Side * Side; // must override
}
```

Notes:
- `abstract` property has no implementation in base
- derived class must provide implementation with `override`
- `virtual` property can have default implementation and may be overridden

### 8) Keep property names clear
Avoid confusing naming that collides with type names or hurts readability.

### 9) Properties are not variables
Treat properties as accessors, not raw storage slots in every low-level scenario.

### 10) Common beginner restriction hits
| Restriction | Simple meaning |
|-------------|----------------|
| No parameters | Use indexer if you need `obj[i]` |
| No normal `ref`/`out` style usage | Use methods for those cases |
| Auto-property = no custom logic | Use full property for validation |
| Accessor visibility limited | `set` can be stricter, not looser than property |
| Name uniqueness | One property name per class (no param overload) |

---

## 3. Practical Summary Table

| Want this | Use this |
|-----------|----------|
| Safe read/write class data | Property |
| Validation on write | Full property (`get`/`set` + backing field) |
| Read-only after create | `{ get; }` or `{ get; init; }` |
| `obj[i]` access | Indexer, not property parameters |
| Action with arguments | Method |

### Good style reminder
```csharp
public class BankAccount
{
    private decimal balance;

    public string AccountNumber { get; }
    public decimal Balance => balance;

    public void Deposit(decimal amount)
    {
        if (amount <= 0) throw new ArgumentException();
        balance += amount;
    }
}
```

---

## 4. Knowledge Check

1. Why can't a normal property take parameters?
2. If you need validation, auto-property or full property?
3. Is `public string Name { get; private set; }` valid? Why?
4. What should you use instead of a property with an index parameter?
5. Name 3 important restrictions on properties in C#.

---

**Previous:** [← Properties in C#](./00-Properties-in-CSharp.md)  
**Next:** [Properties Get and Set (Advanced style) →](./02-Properties-Get-and-Set.md)

🎉 **Nice work!** You now know both how properties work and where C# draws the line.
