# 🏷️ Properties in C#

> **Trainer's Note:** Properties are the safe doors to your class data. Outside code can read/write values, but you control the rules. This is cleaner than public fields.

---

## 📑 Table of Contents
1. [What is a Property?](#1-what-is-a-property)
2. [Properties in C#](#2-properties-in-c)
3. [Property vs Field vs Method](#3-property-vs-field-vs-method)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. What is a Property?

A **property** is a class member that looks like a variable from outside, but works like methods inside (`get` / `set`).

```csharp
student.Name = "Selva";   // looks like a field
string n = student.Name;  // easy to use
```

Behind the scenes, the property can validate, format, or protect data.

### Real-world analogy
```
Field (public) = open box on the table
                 anyone can put anything inside

Property       = locker with a small window
                 people can put/take items
                 but YOU control the rules
                 (no empty name, age cannot be negative)
```

### Why properties matter
| Without properties | With properties |
|--------------------|-----------------|
| Public fields can be set to bad values | You can validate in `set` |
| Hard to change access rules later | Easy to add logic without breaking callers |
| No control on read format | You can format values in `get` |

---

## 2. Properties in C#

### Basic full property (with backing field)
```csharp
public class Student
{
    private string name; // backing field (private storage)

    public string Name
    {
        get { return name; }
        set { name = value; } // "value" is the incoming data
    }
}

Student s = new Student();
s.Name = "Anu";
Console.WriteLine(s.Name);
```

### Auto-implemented property (most common)
```csharp
public class Product
{
    public int Id { get; set; }
    public string Title { get; set; }
    public decimal Price { get; set; }
}
```

Compiler creates a hidden backing field for you.

### Read-only property
```csharp
public class Order
{
    public string OrderId { get; }  // set only inside constructor/init

    public Order(string id)
    {
        OrderId = id;
    }
}
```

### Write-only property (rare)
```csharp
public class Account
{
    private string password;

    public string Password
    {
        set { password = value; } // no get
    }
}
```

### Property with validation
```csharp
public class Person
{
    private int age;

    public int Age
    {
        get => age;
        set
        {
            if (value < 0 || value > 120)
                throw new ArgumentException("Age must be 0 to 120");
            age = value;
        }
    }
}
```

### Init-only property (modern C#)
```csharp
public class Employee
{
    public string EmpCode { get; init; } // set only during object creation
}

var e = new Employee { EmpCode = "E101" };
// e.EmpCode = "E999"; // ❌ not allowed later
```

### Expression-bodied properties
```csharp
public class Circle
{
    public double Radius { get; set; }
    public double Area => 3.14 * Radius * Radius; // get-only calculated
}
```

### Access modifier on get/set
```csharp
public class User
{
    public string Email { get; private set; } // outside can read, only class can set

    public void UpdateEmail(string email)
    {
        Email = email;
    }
}
```

### Static property
```csharp
public class AppConfig
{
    public static string AppName { get; set; } = "Notes App";
}

Console.WriteLine(AppConfig.AppName);
```

---

## 3. Property vs Field vs Method

| Point | Field | Property | Method |
|-------|-------|----------|--------|
| Syntax | `obj.age` | `obj.Age` | `obj.GetAge()` |
| Can validate? | No (if public) | Yes (`set`) | Yes |
| Typical use | Internal storage | Safe public data access | Actions / calculations with inputs |
| Can take params? | No | No | Yes |
| Encapsulation | Weak if public | Strong | Strong |

### Beginner rule of thumb
```
Store data inside class privately     → private field
Expose data safely to outside world   → property
Do an action / need parameters        → method
Need obj[i] access                    → indexer
```

### Good style example
```csharp
public class BankAccount
{
    private decimal balance;                 // field (hidden)

    public string AccountNumber { get; }     // property (read-only)
    public decimal Balance => balance;       // property (read-only view)

    public void Deposit(decimal amount)      // method (action)
    {
        if (amount <= 0) throw new ArgumentException();
        balance += amount;
    }
}
```

---

## 4. Knowledge Check

1. What is the difference between a field and a property in simple words?
2. What does `value` mean inside a `set` accessor?
3. Write an auto-property for `string City`.
4. How do you make a property readable by all, but writable only inside the class?
5. If you need validation, should you use auto-property or full property? Why?

---

**Previous:** [← Indexers in C#](../Indexers/00-Indexers-in-CSharp.md)
**Next:** [Restrictions on Properties →](./01-Restrictions-on-Properties.md)

🎉 **Good start!** Next, learn the important restrictions so you avoid common property mistakes.
