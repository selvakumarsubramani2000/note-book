# 🔐 C# Properties (Get and Set)

> **Trainer's Note:** Properties are the safe public face of private data. Outside code uses `obj.Name`, while you control reading/writing rules in `get` and `set`.

---

## 📑 Table of Contents
1. [Get and Set Basics](#1-get-and-set-basics)
2. [Auto, Full, and Init Properties](#2-auto-full-and-init-properties)
3. [Access Levels on Get/Set](#3-access-levels-on-getset)
4. [Property Patterns and Tips](#4-property-patterns-and-tips)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Get and Set Basics

```csharp
public class Student
{
    private string name;

    public string Name
    {
        get { return name; }      // read
        set { name = value; }     // write ("value" is incoming data)
    }
}

Student s = new Student();
s.Name = "Selva";          // calls set
Console.WriteLine(s.Name); // calls get
```

### Real-world analogy
```
get = view through a window
set = put item in through a controlled door
```

---

## 2. Auto, Full, and Init Properties

### Auto-property
```csharp
public string City { get; set; }
public int Age { get; set; } = 18;
```

### Full property with validation
```csharp
private int age;
public int Age
{
    get => age;
    set
    {
        if (value < 0 || value > 120)
            throw new ArgumentException("Invalid age");
        age = value;
    }
}
```

### Read-only / init-only
```csharp
public string Id { get; }              // set in constructor
public string Code { get; init; }      // set during object init only

var e = new Employee { Code = "E1" };
```

### Computed get-only
```csharp
public class Circle
{
    public double Radius { get; set; }
    public double Area => Math.PI * Radius * Radius;
}
```

---

## 3. Access Levels on Get/Set

```csharp
public string Email { get; private set; } // public read, private write

public class User
{
    public string Email { get; private set; }

    public void UpdateEmail(string email)
    {
        Email = email; // allowed inside class
    }
}
```

### Common styles
| Style | Meaning |
|-------|---------|
| `{ get; set; }` | read/write |
| `{ get; }` | read-only outside constructor/init context |
| `{ get; private set; }` | controlled writes |
| `{ get; init; }` | set at creation time |
| `{ set; }` only | write-only (rare) |

---

## 4. Property Patterns and Tips

```csharp
public class BankAccount
{
    private decimal balance;

    public string AccountNo { get; }
    public decimal Balance => balance; // expose read-only view

    public BankAccount(string accountNo) => AccountNo = accountNo;

    public void Deposit(decimal amount)
    {
        if (amount <= 0) throw new ArgumentOutOfRangeException(nameof(amount));
        balance += amount;
    }
}
```

### Tips
- Prefer properties over public fields
- Validate in `set` when needed
- Keep get logic light (avoid heavy side effects)
- Use methods for actions (`Deposit`), properties for state (`Balance`)

---

## 5. Knowledge Check

1. What is `value` inside `set`?
2. Difference between auto-property and full property?
3. How do you allow public get but private set?
4. When do you use `init`?
5. Why are properties better than public fields?

---

**Previous:** [← Restrictions on Properties](./01-Restrictions-on-Properties.md)

🎉 **Properties track complete!** You covered basics, restrictions, and get/set patterns in one place.
