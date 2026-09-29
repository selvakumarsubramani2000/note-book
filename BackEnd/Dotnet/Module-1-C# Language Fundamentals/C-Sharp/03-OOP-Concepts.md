# 🏛️ OOP Concepts in C#

> **Trainer's Note:** OOP means organizing code like real-world things. Instead of one long script, we create small "objects" with data + behavior. This is the heart of C# design.

---

## 📑 Table of Contents
1. [Class and Objects](#1-class-and-objects)
2. [Constructors](#2-constructors)
3. [Inheritance](#3-inheritance)
4. [Encapsulation](#4-encapsulation)
5. [Abstraction](#5-abstraction)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. Class and Objects

### Real-world analogy
```
Class  = Blueprint of a house
Object = Actual house built from that blueprint

One blueprint → many houses
One class     → many objects
```

### Class
A **class** is a template. It defines:
- **Data** (fields/properties) → what it has
- **Behavior** (methods) → what it can do

```csharp
public class Vendor
{
    // data
    public string Name { get; set; }
    public string City { get; set; }

    // behavior
    public void PrintInfo()
    {
        Console.WriteLine($"{Name} from {City}");
    }
}
```

### Object
An **object** is a real instance created from a class.

```csharp
Vendor v1 = new Vendor();
v1.Name = "A1 Traders";
v1.City = "Chennai";
v1.PrintInfo();

Vendor v2 = new Vendor();
v2.Name = "Best Supplies";
v2.City = "Madurai";
v2.PrintInfo();
```

```
Class: Vendor
   ├── Object v1 (A1 Traders, Chennai)
   └── Object v2 (Best Supplies, Madurai)
```

**Remember:** Class = design, Object = living thing created from design.

---

## 2. Constructors

A **constructor** is a special method that runs **automatically when an object is created**.

### Real-world analogy
```
When a new SIM card is activated, the shop sets:
  - phone number
  - plan
  - activation date
Constructor does this "first setup" for your object.
```

### Default constructor
```csharp
public class Product
{
    public string Name;
    public decimal Price;

    // default constructor (no parameters)
    public Product()
    {
        Name = "Unknown";
        Price = 0;
    }
}

Product p = new Product(); // constructor runs here
```

### Parameterized constructor
```csharp
public class Product
{
    public string Name;
    public decimal Price;

    public Product(string name, decimal price)
    {
        Name = name;
        Price = price;
    }
}

Product p = new Product("Mouse", 499);
```

### Constructor overloading
Multiple constructors with different parameters:

```csharp
public class Employee
{
    public string Name;
    public string Role;

    public Employee(string name)
    {
        Name = name;
        Role = "Staff";
    }

    public Employee(string name, string role)
    {
        Name = name;
        Role = role;
    }
}
```

### Important rules
- Constructor name = class name
- No return type (not even `void`)
- Called with `new`
- Used to set initial values safely

---

## 3. Inheritance

**Inheritance** lets a child class reuse and extend a parent class.

### Real-world analogy
```
Parent: Vehicle
  has: speed, brand
  can: Start()

Child: Car is-a Vehicle
  extra: numberOfDoors
  can: OpenTrunk()

Child gets parent features + its own features.
```

```csharp
public class Vehicle
{
    public string Brand { get; set; }

    public void Start()
    {
        Console.WriteLine($"{Brand} started");
    }
}

public class Car : Vehicle   // Car inherits Vehicle
{
    public int Doors { get; set; }

    public void OpenTrunk()
    {
        Console.WriteLine("Trunk opened");
    }
}

Car car = new Car();
car.Brand = "Honda";
car.Doors = 4;
car.Start();      // from parent
car.OpenTrunk();  // from child
```

### Benefits
- Reuse code
- Less duplication
- Clear "is-a" relationships (`Car` is a `Vehicle`)

### Types you will hear
| Type | Meaning in C# |
|------|----------------|
| Single | One parent (common) |
| Multi-level | Grandparent → Parent → Child |
| Hierarchical | One parent, many children |
| Multiple class inheritance | ❌ Not supported for classes |
| Multiple interfaces | ✅ Supported |

```csharp
// Multi-level
class Animal { }
class Dog : Animal { }
class Puppy : Dog { }
```

---

## 4. Encapsulation

**Encapsulation** means **hide internal details** and allow access only in a controlled way.

### Real-world analogy
```
Medicine capsule:
  outer cover protects inner medicine
  you don't touch raw chemicals directly
  you take it the safe way

In code:
  private fields are protected inside
  public properties/methods are the safe door
```

### Without encapsulation (risky)
```csharp
public class BankAccount
{
    public decimal Balance; // anyone can set Balance = -1000 😬
}
```

### With encapsulation (safe)
```csharp
public class BankAccount
{
    private decimal _balance; // hidden

    public decimal Balance
    {
        get { return _balance; }
        private set { _balance = value; }
    }

    public void Deposit(decimal amount)
    {
        if (amount > 0)
            _balance += amount;
    }

    public void Withdraw(decimal amount)
    {
        if (amount > 0 && amount <= _balance)
            _balance -= amount;
        else
            Console.WriteLine("Invalid withdraw");
    }
}
```

```csharp
BankAccount acc = new BankAccount();
acc.Deposit(1000);
acc.Withdraw(200);
Console.WriteLine(acc.Balance); // 800
// acc.Balance = -50; ❌ not allowed if set is private
```

### Why encapsulation matters
- Protects data
- Prevents invalid values
- Lets you change internal logic later without breaking outside code
- Supports clean APIs (`Deposit`, `Withdraw`)

---

## 5. Abstraction

**Abstraction** means **show only what is needed**, hide complex internal steps.

### Real-world analogy
```
ATM:
  You press "Withdraw 500"
  You do NOT see:
    bank server checks, ledger updates, cash counter motors...

  ATM shows simple buttons.
  Complex process is hidden.
  That is abstraction.
```

### Way 1: Abstract class
```csharp
public abstract class Payment
{
    public abstract void Pay(decimal amount); // must be implemented by child

    public void PrintReceipt(decimal amount)
    {
        Console.WriteLine($"Paid: {amount}");
    }
}

public class UpiPayment : Payment
{
    public override void Pay(decimal amount)
    {
        Console.WriteLine($"UPI payment of {amount} done");
    }
}

Payment payment = new UpiPayment();
payment.Pay(250);
payment.PrintReceipt(250);
```

### Way 2: Interface (pure contract)
```csharp
public interface INotifier
{
    void Send(string message);
}

public class EmailNotifier : INotifier
{
    public void Send(string message)
    {
        Console.WriteLine($"Email: {message}");
    }
}

public class SmsNotifier : INotifier
{
    public void Send(string message)
    {
        Console.WriteLine($"SMS: {message}");
    }
}
```

### Abstraction vs Encapsulation (beginner-friendly)
| | Abstraction | Encapsulation |
|---|-------------|---------------|
| Focus | Hide complexity, show essentials | Hide data, control access |
| Question | "What can this thing do?" | "How is data protected?" |
| Tools | abstract class / interface | private fields + properties/methods |
| ATM example | Buttons you see | Internal bank validation logic protected |

---

## 6. Knowledge Check

1. What is the difference between a class and an object?
2. Why do we use constructors?
3. Write a small parent-child inheritance example (`Employee` → `Manager`).
4. How does encapsulation protect a bank balance?
5. What problem does abstraction solve for the user of a class?
6. Can a C# class inherit from two classes? What can it implement multiple of?
7. Is encapsulation the same as abstraction? Explain simply.

---

**Previous:** [← Control Statements](./02-Control-Statements.md)  
**Next:** [Methods in C# →](./04-Methods-in-CSharp.md)
