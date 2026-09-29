# 🧱 OOP Concepts — Object-Oriented Programming

> **Trainer's Note:** OOP is how professional backend code stays organized as projects grow. Instead of one giant script, you model the real world as **classes** and **objects**. Learn the ideas first; syntax second.

---

## 📑 Table of Contents
1. [Why OOP Exists](#1-why-oop-exists)
2. [Class vs Object](#2-class-vs-object)
3. [Properties, Fields, and Methods](#3-properties-fields-and-methods)
4. [Constructors](#4-constructors)
5. [Encapsulation](#5-encapsulation)
6. [Inheritance](#6-inheritance)
7. [Polymorphism](#7-polymorphism)
8. [Abstraction](#8-abstraction)
9. [Interfaces](#9-interfaces)
10. [Access Modifiers](#10-access-modifiers)
11. [Composition over Inheritance](#11-composition-over-inheritance)
12. [OOP in .NET Backend Projects](#12-oop-in-net-backend-projects)
13. [Knowledge Check](#13-knowledge-check)

---

## 1. Why OOP Exists

Without structure, code becomes a messy drawer of loose functions and variables.

**OOP** (Object-Oriented Programming) groups **data + behavior** together.

```
Real world:
  A "Bank Account" has:
    - data: account number, balance
    - behavior: deposit, withdraw, get balance

OOP:
  Class BankAccount models that idea in code
```

### Four pillars (remember these)
| Pillar | One-line meaning |
|--------|------------------|
| **Encapsulation** | Hide internals; expose a safe public face |
| **Inheritance** | Child reuses/extends parent |
| **Polymorphism** | Same action, different behavior by type |
| **Abstraction** | Show essentials; hide messy details |

---

## 2. Class vs Object

| Term | Meaning | Analogy |
|------|---------|---------|
| **Class** | Blueprint / template | House plan |
| **Object** | Real instance created from the class | An actual house built from the plan |

```csharp
// Class = blueprint
public class Dog
{
    public string Name { get; set; } = string.Empty;
    public void Bark() => Console.WriteLine($"{Name} says woof!");
}

// Objects = real dogs
Dog d1 = new Dog { Name = "Bruno" };
Dog d2 = new Dog { Name = "Milo" };

d1.Bark(); // Bruno says woof!
d2.Bark(); // Milo says woof!
```

One class → many objects, each with its own data.

---

## 3. Properties, Fields, and Methods

### Fields — internal storage (usually private)
```csharp
private decimal _balance;
```

### Properties — controlled access to data
```csharp
public string Email { get; set; } = string.Empty;          // auto-property
public decimal Balance { get; private set; }               // outside can read, not set
```

### Methods — behavior
```csharp
public void Deposit(decimal amount)
{
    if (amount <= 0) throw new ArgumentException("Amount must be positive");
    Balance += amount;
}
```

### Full tiny example
```csharp
public class Product
{
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }

    public decimal PriceWithTax(decimal taxRate)
    {
        return Price + (Price * taxRate);
    }
}

var p = new Product { Name = "Keyboard", Price = 1000m };
Console.WriteLine(p.PriceWithTax(0.18m)); // 1180
```

---

## 4. Constructors

A **constructor** runs when you create an object (`new ...`). Use it to set required starting state.

```csharp
public class User
{
    public string Email { get; }
    public string Name { get; set; }

    public User(string email, string name)
    {
        if (string.IsNullOrWhiteSpace(email))
            throw new ArgumentException("Email is required");

        Email = email;
        Name = name;
    }
}

var user = new User("selva@example.com", "Selva");
```

### Why constructors matter in backend
- Force required data (id, email, order items)
- Prevent half-built invalid objects
- Make intent obvious: “to create X, you must provide Y”

---

## 5. Encapsulation

**Encapsulation** = keep object insides protected; allow change only through safe doors.

```
Bad:  anyone can set Balance = -999999
Good: only Deposit/Withdraw can change Balance, with rules
```

```csharp
public class BankAccount
{
    public string AccountNumber { get; }
    public decimal Balance { get; private set; }

    public BankAccount(string accountNumber, decimal openingBalance = 0)
    {
        AccountNumber = accountNumber;
        Balance = openingBalance;
    }

    public void Deposit(decimal amount)
    {
        if (amount <= 0) throw new ArgumentException("Invalid amount");
        Balance += amount;
    }

    public void Withdraw(decimal amount)
    {
        if (amount <= 0) throw new ArgumentException("Invalid amount");
        if (amount > Balance) throw new InvalidOperationException("Insufficient funds");
        Balance -= amount;
    }
}
```

**Benefit:** Business rules live in one place. Controllers/APIs cannot accidentally break money logic.

---

## 6. Inheritance

**Inheritance** lets a new class reuse an existing class.

```
Animal          ← base / parent
  ├── Dog       ← derived / child
  └── Cat
```

```csharp
public class Animal
{
    public string Name { get; set; } = string.Empty;
    public virtual void Speak() => Console.WriteLine("Some sound");
}

public class Dog : Animal
{
    public override void Speak() => Console.WriteLine($"{Name}: Woof");
}

public class Cat : Animal
{
    public override void Speak() => Console.WriteLine($"{Name}: Meow");
}
```

### Useful keywords
| Keyword | Meaning |
|---------|---------|
| `:` | “inherits from” |
| `virtual` | Parent method allowed to be overridden |
| `override` | Child replaces parent method |
| `base` | Call parent version |
| `sealed` | Cannot be inherited further |
| `abstract` | Incomplete class/method; must be completed by child |

### Backend warning
Inheritance is powerful, but deep hierarchies become hard to change. Prefer **shallow** inheritance trees.

---

## 7. Polymorphism

**Polymorphism** = “many forms.” Same call, different behavior depending on the actual object.

```csharp
List<Animal> pets = new()
{
    new Dog { Name = "Bruno" },
    new Cat { Name = "Mimi" }
};

foreach (Animal pet in pets)
{
    pet.Speak(); // each animal speaks its own way
}
```

### Why backend loves this
You can write code against a **general type** (or interface) and plug in different implementations:

```csharp
// later idea (preview):
// IPaymentService can be StripePaymentService or UpiPaymentService
// your order code stays the same
```

---

## 8. Abstraction

**Abstraction** means focusing on **what** something does, not **how** it does it every time.

Two common tools in C#:
1. **Abstract classes** — partial blueprints
2. **Interfaces** — pure contracts (next section)

```csharp
public abstract class NotificationSender
{
    public abstract Task SendAsync(string to, string message);

    public void Log(string text) => Console.WriteLine($"LOG: {text}");
}

public class EmailSender : NotificationSender
{
    public override Task SendAsync(string to, string message)
    {
        Log($"Email to {to}");
        // real email logic here...
        return Task.CompletedTask;
    }
}
```

You cannot do `new NotificationSender()` — it is incomplete on purpose.

---

## 9. Interfaces

An **interface** is a contract: “If you claim to be X, you must provide these methods.”

```csharp
public interface IOrderRepository
{
    Task<Order?> GetByIdAsync(Guid id);
    Task SaveAsync(Order order);
}

public class SqlOrderRepository : IOrderRepository
{
    public Task<Order?> GetByIdAsync(Guid id)
    {
        // read from SQL Server...
        return Task.FromResult<Order?>(null);
    }

    public Task SaveAsync(Order order)
    {
        // write to SQL Server...
        return Task.CompletedTask;
    }
}
```

### Interface vs abstract class (beginner view)
| | Interface | Abstract class |
|--|-----------|----------------|
| Multiple inheritance | A class can implement many interfaces | Only one base class |
| Default purpose | Capability contract | Shared base + some code |
| Fields | No normal instance fields | Can have fields/state |
| Backend use | Services, repositories, swappable parts | Shared hierarchy when truly “is-a” |

> Modern .NET backends use **interfaces heavily** with Dependency Injection.

---

## 10. Access Modifiers

Access modifiers control **who can see what**.

| Modifier | Visible to |
|----------|------------|
| `public` | Everywhere |
| `private` | Only inside the same class |
| `protected` | Same class + child classes |
| `internal` | Same assembly/project |
| `protected internal` | Same assembly OR child classes |
| `private protected` | Same assembly AND child classes |

```csharp
public class Employee
{
    private decimal _salary;                 // hidden
    public string Name { get; set; } = ""; // open
    protected void CalculateBonus() { }      // children can use
}
```

**Rule of thumb:** Start private. Open only what callers truly need.

---

## 11. Composition over Inheritance

**Composition** = “has-a” relationship.  
**Inheritance** = “is-a” relationship.

```
Car is-a Vehicle            → inheritance may fit
Car has-a Engine            → composition fits better
Order has-a List<OrderItem> → composition
```

```csharp
public class Engine
{
    public void Start() => Console.WriteLine("Engine started");
}

public class Car
{
    private readonly Engine _engine = new Engine();

    public void Start() => _engine.Start();
}
```

### Backend preference
Many teams prefer:
- small classes
- interfaces
- composition
- clear services

…instead of tall inheritance trees.

---

## 12. OOP in .NET Backend Projects

In ASP.NET Core APIs you will constantly meet OOP pieces:

```
Controller   → receives HTTP request
Service      → business rules
Repository   → talks to database
Model/Entity → data shape (Order, User, Product)
DTO          → data sent over API (request/response models)
```

### Example sketch
```csharp
public class Order
{
    public Guid Id { get; private set; } = Guid.NewGuid();
    public List<OrderItem> Items { get; private set; } = new();
    public decimal Total => Items.Sum(i => i.LineTotal);

    public void AddItem(string productName, decimal price, int qty)
    {
        Items.Add(new OrderItem(productName, price, qty));
    }
}

public class OrderItem
{
    public string ProductName { get; }
    public decimal UnitPrice { get; }
    public int Quantity { get; }
    public decimal LineTotal => UnitPrice * Quantity;

    public OrderItem(string productName, decimal unitPrice, int quantity)
    {
        ProductName = productName;
        UnitPrice = unitPrice;
        Quantity = quantity;
    }
}
```

### Mental model
```
HTTP JSON comes in
   → Controller maps it to objects
   → Service applies rules using domain objects
   → Repository saves/loads objects
   → HTTP JSON goes out
```

OOP is the language of that middle layer.

---

## 13. Knowledge Check

**Q1.** What is the difference between a class and an object?  
**Q2.** Name the four pillars of OOP.  
**Q3.** Why is encapsulation important for a `BankAccount`?  
**Q4.** What does an interface give you that a concrete class alone does not?  
**Q5.** “Dog is-an Animal” — inheritance or composition?  
**Q6.** “Order has OrderItems” — inheritance or composition?

### Mini practice
Create:
1. An interface `IMessageService` with `Send(string to, string body)`
2. A class `ConsoleMessageService` that implements it by printing to console
3. A `UserNotifier` class that receives `IMessageService` in its constructor and uses it
4. In `Main`, wire them together and send one message

### Answers (short)
1. Class = blueprint; object = instance  
2. Encapsulation, Inheritance, Polymorphism, Abstraction  
3. Protects balance with rules; prevents invalid direct changes  
4. A contract for swappable implementations / loose coupling  
5. Inheritance  
6. Composition  

---

## ✅ What You Should Feel Confident About

- [ ] Explain class vs object with a real-world analogy  
- [ ] Write a class with properties, constructor, and methods  
- [ ] Apply encapsulation with `private set` / validation  
- [ ] Use basic inheritance and `override`  
- [ ] Define and implement a simple interface  
- [ ] Choose composition when “has-a” is the real relationship  

**Previous:** [01-programming-basics.md](./01-programming-basics.md)  
**Next:** [03-web-basics.md](./03-web-basics.md) — how the web and APIs communicate.
