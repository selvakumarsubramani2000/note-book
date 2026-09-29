# 📘 OOP - Object-Oriented Programming Complete Guide (C#)

## Why This Guide?
OOP is the **foundation** of C# and .NET development. Every ASP.NET Core API,
Entity Framework model, and service class you write uses OOP concepts.
Understanding OOP will make you a **better developer** — not just in C#,
but in any modern language.

---

## Table of Contents
1. [What is OOP?](#1-what-is-oop)
2. [Why Do We Need OOP?](#2-why-do-we-need-oop---the-problem-it-solves)
3. [Class & Object - The Foundation](#3-class--object---the-foundation)
4. [The 4 Pillars of OOP](#4-the-4-pillars-of-oop)
5. [Pillar 1: Encapsulation](#5-encapsulation---hiding-the-internals)
6. [Pillar 2: Inheritance](#6-inheritance---reusing-code)
7. [Pillar 3: Polymorphism](#7-polymorphism---many-forms)
8. [Pillar 4: Abstraction](#8-abstraction---hiding-complexity)
9. [Interfaces vs Abstract Classes](#9-interfaces-vs-abstract-classes)
10. [Static Members & Static Classes](#10-static-members--static-classes)
11. [SOLID Principles (OOP Best Practices)](#11-solid-principles)
12. [OOP in Your Daily Work](#12-oop-in-your-daily-work---real-examples)
13. [Common OOP Terms](#13-common-oop-terms)

---

## 1. What is OOP?

**OOP (Object-Oriented Programming)** is a way of organizing your code around
**objects** — things that have **data** (properties) and **behavior** (methods).

### Think of it Like the Real World:

```
Real World Object: Car 🚗
  Data (Properties):          Behavior (Methods):
  ├── Color = "Red"           ├── Start()
  ├── Brand = "Toyota"        ├── Accelerate()
  ├── Speed = 0               ├── Brake()
  ├── FuelLevel = 100%        └── TurnOff()
  └── IsRunning = false

C# Object: Vendor
  Data (Properties):          Behavior (Methods):
  ├── VendorName = "Acme"     ├── Activate()
  ├── Email = "a@b.com"       ├── Deactivate()
  ├── Status = "Active"       ├── UpdateEmail()
  └── CreatedAt = DateTime    └── GetContactInfo()
```

### Two Key Concepts:
```
CLASS  = Blueprint / Template / Recipe
         (Defines WHAT an object looks like)

OBJECT = Instance / Actual thing created from the class
         (The REAL thing built from the blueprint)

Example:
  Class  = "Car" blueprint       → defines what a car IS
  Object = Your specific red Toyota → an actual car you drive

  Class  = "Vendor" model        → defines what a vendor IS
  Object = "Acme Corporation"    → an actual vendor in your database
```

---

## 2. Why Do We Need OOP? - The Problem It Solves

### Without OOP (Procedural Code) — The Old Way:
```csharp
// ❌ Everything is loose functions and variables — gets messy fast!

string vendorName = "Acme Corp";
string vendorEmail = "acme@email.com";
string vendorStatus = "Active";

string vendor2Name = "Global Tech";
string vendor2Email = "global@email.com";
string vendor2Status = "Active";

// What if you have 100 vendors? 300 variables!
// What if you need to add a phone number? Change EVERYWHERE!

void ActivateVendor(ref string status) {
    status = "Active";
}

void DeactivateVendor(ref string status) {
    status = "Inactive";
}

// Who validates? Who ensures email format? Nobody!
// Any code anywhere can set vendorEmail = "not-an-email" 💥
```

### With OOP — The Modern Way:
```csharp
// ✅ Data and behavior are bundled together — clean and safe!

public class Vendor
{
    // Data is PROTECTED (encapsulation)
    public string VendorName { get; private set; }
    public string Email { get; private set; }
    public string Status { get; private set; }

    // Constructor ensures valid creation
    public Vendor(string name, string email)
    {
        if (string.IsNullOrEmpty(name))
            throw new ArgumentException("Name is required!");

        VendorName = name;
        Email = email;
        Status = "Active";
    }

    // Behavior is tied to the data
    public void Deactivate() => Status = "Inactive";
    public void Activate() => Status = "Active";

    public void UpdateEmail(string newEmail)
    {
        if (!newEmail.Contains("@"))
            throw new ArgumentException("Invalid email!");
        Email = newEmail;
    }
}

// Now creating vendors is clean:
var vendor1 = new Vendor("Acme Corp", "acme@email.com");
var vendor2 = new Vendor("Global Tech", "global@email.com");

vendor1.Deactivate();          // ✅ Safe — validation built in
vendor1.UpdateEmail("bad");    // ❌ Throws exception — protected!
```

### Why OOP Matters — Summary:
```
┌────────────────────────┬────────────────────────────────────────────┐

---

## 3. Class & Object - The Foundation

### Defining a Class:
```csharp
// A class is a BLUEPRINT — it describes what a Vendor looks like
public class Vendor
{
    // ── Properties (Data) ─────────────────────────
    public int Id { get; set; }
    public string VendorName { get; set; }
    public string Email { get; set; }
    public string Category { get; set; }
    public string Status { get; set; }
    public DateTime CreatedAt { get; set; }

    // ── Constructor (How to create one) ───────────
    public Vendor()   // Default constructor
    {
        Status = "Active";
        CreatedAt = DateTime.UtcNow;
    }

    public Vendor(string name, string email)  // Parameterized constructor
    {
        VendorName = name;
        Email = email;
        Status = "Active";
        CreatedAt = DateTime.UtcNow;
    }

    // ── Methods (Behavior) ────────────────────────
    public void Activate()
    {
        Status = "Active";
    }

    public void Deactivate()
    {
        Status = "Inactive";
    }

    public string GetSummary()
    {
        return $"{VendorName} ({Category}) - {Status}";
    }

    // ── Override ToString (built-in method) ───────
    public override string ToString()
    {
        return $"[{Id}] {VendorName} - {Status}";
    }
}
```

### Creating Objects (Instances):
```csharp
// Creating objects from the Vendor class blueprint

// Using default constructor
var vendor1 = new Vendor();
vendor1.VendorName = "Acme Corporation";
vendor1.Email = "contact@acme.com";
vendor1.Category = "Supplier";

// Using parameterized constructor
var vendor2 = new Vendor("Global Tech", "info@globaltech.com");
vendor2.Category = "Manufacturer";

// Using object initializer (most common in C#)
var vendor3 = new Vendor
{
    VendorName = "Pacific Trading",
    Email = "hello@pacific.com",
    Category = "Distributor",
    Status = "Active"
};

// Using the objects
Console.WriteLine(vendor1.GetSummary());  // Acme Corporation (Supplier) - Active
vendor2.Deactivate();
Console.WriteLine(vendor2.Status);        // Inactive
Console.WriteLine(vendor3);              // [0] Pacific Trading - Active
```

### Class vs Object - Visual:
```
    CLASS (Blueprint)                    OBJECTS (Instances)
┌──────────────────────┐          ┌──────────────────────────┐
│  Vendor              │          │ vendor1:                 │
│  ├── VendorName      │ ──new──▶ │  VendorName = "Acme"     │
│  ├── Email           │          │  Email = "a@acme.com"    │
│  ├── Status          │          │  Status = "Active"       │
│  ├── Activate()      │          └──────────────────────────┘
│  ├── Deactivate()    │
│  └── GetSummary()    │ ──new──▶ ┌──────────────────────────┐
│                      │          │ vendor2:                 │
│  (ONE blueprint)     │          │  VendorName = "Global"   │
│                      │          │  Email = "g@global.com"  │
│                      │          │  Status = "Inactive"     │
└──────────────────────┘          └──────────────────────────┘
                                  (MANY instances from same class)
```

### Access Modifiers:
```csharp
public class Vendor
{
    public string VendorName;     // ✅ Anyone can access
    private string _internalCode; // 🔒 Only this class can access
    protected int _score;         // 🔐 This class + child classes
    internal string _teamNote;    // 📦 Only within same project/assembly
}
```
```
┌─────────────┬──────────┬──────────┬───────────┬──────────┐
│ Modifier    │ Same     │ Child    │ Same      │ Other    │
│             │ Class    │ Class    │ Assembly  │ Assembly │
├─────────────┼──────────┼──────────┼───────────┼──────────┤
│ public      │ ✅       │ ✅       │ ✅        │ ✅       │
│ private     │ ✅       │ ❌       │ ❌        │ ❌       │
│ protected   │ ✅       │ ✅       │ ❌        │ ❌       │
│ internal    │ ✅       │ ✅       │ ✅        │ ❌       │
│ prot.intern.│ ✅       │ ✅       │ ✅        │ ❌       │
└─────────────┴──────────┴──────────┴───────────┴──────────┘
```


---

## 4. The 4 Pillars of OOP

```
                    ┌─────────────────────────────────┐
                    │    Object-Oriented Programming   │
                    └───────────────┬─────────────────┘
          ┌─────────────┬──────────┼──────────┬─────────────┐
          ▼             ▼          ▼          ▼
   ┌─────────────┐ ┌──────────┐ ┌──────────────┐ ┌─────────────┐
   │Encapsulation│ │Inheritance│ │Polymorphism  │ │ Abstraction │
   │             │ │           │ │              │ │             │
   │ Hide data   │ │ Reuse    │ │ Many forms   │ │ Hide        │
   │ behind      │ │ code from│ │ same action  │ │ complexity  │
   │ methods     │ │ parent   │ │ different    │ │ show only   │
   │             │ │ class    │ │ behavior     │ │ essentials  │
   └─────────────┘ └──────────┘ └──────────────┘ └─────────────┘

   🔒 Protect       ♻️ Reuse      🔀 Flexibility   🎭 Simplify
```

---

## 5. Encapsulation - Hiding the Internals

**Encapsulation** = Bundling data + methods together AND controlling access.
Like a **capsule** that protects what's inside.

### Real-World Analogy:
```
ATM Machine:
  You CAN:     Insert card, enter PIN, withdraw money
  You CAN'T:   Open the machine, access the safe, change software

  The ATM ENCAPSULATES the complexity — you only see simple buttons.
  The internal mechanism is HIDDEN and PROTECTED.
```

### ❌ Without Encapsulation:
```csharp
// Anyone can mess with the data directly!
public class BankAccount
{
    public decimal Balance;    // 💥 Anyone can set this to anything!
    public string AccountNumber;
}

var account = new BankAccount();
account.Balance = -99999;      // 💥 Negative balance? No validation!
account.Balance = 999999999;   // 💥 Free money? No rules!
account.AccountNumber = "";    // 💥 Empty account number? Chaos!
```

### ✅ With Encapsulation:
```csharp
public class BankAccount
{
    // Private fields — HIDDEN from outside
    private decimal _balance;
    private string _accountNumber;
    private List<string> _transactionHistory = new();

    // Public properties — CONTROLLED access
    public decimal Balance => _balance;  // Read-only (no set!)
    public string AccountNumber => _accountNumber;
    public IReadOnlyList<string> Transactions => _transactionHistory;

    // Constructor — controlled creation
    public BankAccount(string accountNumber, decimal initialDeposit)
    {
        if (string.IsNullOrEmpty(accountNumber))
            throw new ArgumentException("Account number required!");
        if (initialDeposit < 0)
            throw new ArgumentException("Initial deposit can't be negative!");

        _accountNumber = accountNumber;
        _balance = initialDeposit;
        _transactionHistory.Add($"Account opened with ₹{initialDeposit}");
    }

    // Public methods — controlled behavior
    public void Deposit(decimal amount)
    {
        if (amount <= 0)
            throw new ArgumentException("Deposit must be positive!");

        _balance += amount;
        _transactionHistory.Add($"Deposited ₹{amount}. Balance: ₹{_balance}");
    }

    public void Withdraw(decimal amount)
    {
        if (amount <= 0)
            throw new ArgumentException("Withdrawal must be positive!");
        if (amount > _balance)
            throw new InvalidOperationException("Insufficient funds!");

        _balance -= amount;
        _transactionHistory.Add($"Withdrew ₹{amount}. Balance: ₹{_balance}");
    }
}

// Usage:
var account = new BankAccount("ACC-001", 1000);
account.Deposit(500);            // ✅ Balance = 1500
account.Withdraw(200);           // ✅ Balance = 1300
// account._balance = 999999;    // ❌ Compile error! Can't access private
// account.Withdraw(-100);       // ❌ Exception! Must be positive
// account.Withdraw(99999);      // ❌ Exception! Insufficient funds
```

### C# Properties — The Encapsulation Tool:
```csharp
public class Vendor
{
    // Auto-property (most common)
    public string VendorName { get; set; }

    // Read-only from outside, writable inside
    public string Status { get; private set; }

    // Computed property (no stored value)
    public bool IsActive => Status == "Active";

    // Property with validation
    private string _email;
    public string Email
    {
        get => _email;
        set
        {
            if (!value.Contains("@"))
                throw new ArgumentException("Invalid email format!");
            _email = value;
        }
    }

    // Init-only property (C# 9+) — set only during object creation
    public DateTime CreatedAt { get; init; }
}

// Usage:
var vendor = new Vendor
{
    VendorName = "Acme",
    Email = "valid@email.com",   // ✅ Contains @
    CreatedAt = DateTime.UtcNow  // ✅ Set during init
};

vendor.VendorName = "New Name";  // ✅ Can change (public set)
vendor.Status = "Inactive";      // ❌ Compile error (private set)
vendor.CreatedAt = DateTime.Now; // ❌ Compile error (init only)
```

---

## 6. Inheritance - Reusing Code

**Inheritance** = Creating a new class FROM an existing class.
The child class **inherits** all properties and methods from the parent.

### Real-World Analogy:
```
Parent: Vehicle
  ├── Has wheels, engine, color
  ├── Can start(), stop(), accelerate()

Child: Car (inherits from Vehicle)
  ├── Gets ALL of Vehicle's features automatically!
  ├── Adds: numberOfDoors, hasTrunk
  └── Adds: openTrunk()

Child: Motorcycle (inherits from Vehicle)
  ├── Gets ALL of Vehicle's features automatically!
  ├── Adds: hasSidecar
  └── Adds: doWheelie()
```

### C# Inheritance Example:
```csharp
// ── BASE CLASS (Parent) ────────────────────────────
public class BaseEntity
{
    public int Id { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? UpdatedAt { get; set; }
    public bool IsDeleted { get; set; } = false;

    public void SoftDelete()
    {
        IsDeleted = true;
        UpdatedAt = DateTime.UtcNow;
    }

    public void MarkUpdated()
    {
        UpdatedAt = DateTime.UtcNow;
    }
}

// ── CHILD CLASS (inherits from BaseEntity) ─────────
public class Vendor : BaseEntity   // Vendor IS A BaseEntity
{
    // Vendor gets Id, CreatedAt, UpdatedAt, IsDeleted, SoftDelete()
    // FOR FREE! No need to rewrite them!

    // Vendor-specific properties
    public string VendorName { get; set; }
    public string Email { get; set; }
    public string Category { get; set; }
    public string Status { get; set; } = "Active";

    // Vendor-specific methods
    public void Deactivate()
    {
        Status = "Inactive";
        MarkUpdated();   // Calling parent's method!
    }
}

// ── ANOTHER CHILD CLASS ────────────────────────────
public class User : BaseEntity    // User IS A BaseEntity
{
    public string Name { get; set; }
    public string Email { get; set; }
    public string Role { get; set; } = "User";

    public void PromoteToAdmin()
    {
        Role = "Admin";
        MarkUpdated();   // Calling parent's method!
    }
}

// ── USAGE ──────────────────────────────────────────
var vendor = new Vendor { VendorName = "Acme", Email = "a@b.com" };
Console.WriteLine(vendor.Id);         // 0 (from BaseEntity)
Console.WriteLine(vendor.CreatedAt);  // 2026-04-16... (from BaseEntity)
Console.WriteLine(vendor.VendorName); // Acme (from Vendor)

vendor.SoftDelete();                  // Method from BaseEntity!
Console.WriteLine(vendor.IsDeleted);  // True
```

### Inheritance Hierarchy:
```
       BaseEntity         (Parent/Base)
       ├── Id
       ├── CreatedAt
       ├── UpdatedAt
       ├── IsDeleted
       ├── SoftDelete()
       └── MarkUpdated()
           │
     ┌─────┴──────┐
     ▼            ▼
   Vendor        User            (Children/Derived)
   ├── VendorName├── Name
   ├── Email     ├── Email
   ├── Category  ├── Role
   ├── Status    └── PromoteToAdmin()
   └── Deactivate()
```

### Key Inheritance Rules in C#:
```csharp
// ✅ Single inheritance only — C# allows ONE parent class
public class Vendor : BaseEntity { }           // ✅ OK

// ❌ Multiple class inheritance NOT allowed
// public class Vendor : BaseEntity, AuditLog { }  // ❌ Compile error!

// ✅ But you CAN implement multiple interfaces (covered in Section 9)
public class Vendor : BaseEntity, IActivatable, IExportable { }  // ✅ OK

// ✅ Chain of inheritance
public class BaseEntity { }
public class Vendor : BaseEntity { }
public class PremiumVendor : Vendor { }   // PremiumVendor → Vendor → BaseEntity

// sealed = prevent further inheritance
public sealed class FinalVendor : Vendor { }
// public class SuperVendor : FinalVendor { }   // ❌ Can't inherit from sealed!
```

### "is" and "as" Keywords:
```csharp
Vendor vendor = new Vendor { VendorName = "Acme" };

// "is" — checks if object IS of a type
if (vendor is BaseEntity)        // ✅ True — Vendor inherits from BaseEntity
    Console.WriteLine("It's a BaseEntity!");

if (vendor is Vendor)            // ✅ True
    Console.WriteLine("It's a Vendor!");

// "as" — tries to cast, returns null if fails
BaseEntity entity = vendor as BaseEntity;   // ✅ Works
User user = vendor as User;                 // null — Vendor is not a User
```

---

## 7. Polymorphism - Many Forms

**Polymorphism** = "Many Forms". Same method name, **different behavior**
depending on the object type. The most POWERFUL pillar of OOP.

### Real-World Analogy:
```
"MakeSound()" method:
  Dog.MakeSound()    → "Bark!"
  Cat.MakeSound()    → "Meow!"
  Duck.MakeSound()   → "Quack!"

Same action name, DIFFERENT behavior based on the object!
```

### Type 1: Method Overriding (Runtime Polymorphism)

The child class **replaces** the parent's method with its own version.

```csharp
// Base class with virtual method (CAN be overridden)
public class NotificationService
{
    public virtual void Send(string message, string recipient)
    {
        Console.WriteLine($"[BASE] Sending '{message}' to {recipient}");
    }
}

// Child: Email notification
public class EmailNotification : NotificationService
{
    public override void Send(string message, string recipient)
    {
        Console.WriteLine($"📧 EMAIL to {recipient}: {message}");
        // Actually send email via SMTP...
    }
}

// Child: SMS notification
public class SmsNotification : NotificationService
{
    public override void Send(string message, string recipient)
    {
        Console.WriteLine($"📱 SMS to {recipient}: {message}");
        // Actually send SMS via Twilio...
    }
}

// Child: Push notification
public class PushNotification : NotificationService
{
    public override void Send(string message, string recipient)
    {
        Console.WriteLine($"🔔 PUSH to {recipient}: {message}");
        // Actually send push via Firebase...
    }
}

// ── THE MAGIC OF POLYMORPHISM ──────────────────────
// One variable type, different behaviors!
NotificationService notifier;

notifier = new EmailNotification();
notifier.Send("Order shipped", "selva@email.com");  // 📧 EMAIL

notifier = new SmsNotification();
notifier.Send("Order shipped", "+91-9876543210");    // 📱 SMS

notifier = new PushNotification();
notifier.Send("Order shipped", "device-token-123");  // 🔔 PUSH

// Even better — process a list of different notifications:
List<NotificationService> notifications = new()
{
    new EmailNotification(),
    new SmsNotification(),
    new PushNotification()
};

foreach (var n in notifications)
{
    n.Send("Welcome!", "user@example.com");
    // Each one behaves DIFFERENTLY — that's polymorphism!
}
```

### Type 2: Method Overloading (Compile-Time Polymorphism)

Same method name, **different parameters**.

```csharp
public class VendorService
{
    // Same name "Search", different parameters
    public List<Vendor> Search(string name)
    {
        return _db.Vendors.Where(v => v.VendorName.Contains(name)).ToList();
    }

    public List<Vendor> Search(string name, string state)
    {
        return _db.Vendors
            .Where(v => v.VendorName.Contains(name) && v.State == state)
            .ToList();
    }

    public List<Vendor> Search(string name, string state, string category)
    {
        return _db.Vendors
            .Where(v => v.VendorName.Contains(name)
                     && v.State == state
                     && v.Category == category)
            .ToList();
    }
}

// Usage — compiler picks the right method based on arguments:
var service = new VendorService();
service.Search("Acme");                          // Calls 1-parameter version
service.Search("Acme", "NY");                    // Calls 2-parameter version
service.Search("Acme", "NY", "Supplier");        // Calls 3-parameter version
```

### virtual → override → base:
```csharp
public class BaseEntity
{
    public virtual string GetDisplayName()   // virtual = CAN be overridden
    {
        return $"Entity #{Id}";
    }
}

public class Vendor : BaseEntity
{
    public override string GetDisplayName()  // override = replaces parent
    {
        return $"{VendorName} ({Category})";
    }
}

public class PremiumVendor : Vendor
{
    public override string GetDisplayName()
    {
        return "⭐ " + base.GetDisplayName();  // base = call parent version
        // Result: "⭐ Acme Corp (Supplier)"
    }
}
```

---

## 8. Abstraction - Hiding Complexity

**Abstraction** = Show only **what** something does, hide **how** it does it.
Define a contract that says "you MUST implement these methods" without
specifying the implementation.

### Real-World Analogy:
```
TV Remote:
  You press "Volume Up" → Volume increases
  You DON'T need to know: circuits, signal processing, speaker drivers

  The remote ABSTRACTS the complexity — you only see simple buttons.

Driving a Car:
  You turn the steering wheel → Car turns
  You DON'T need to know: rack and pinion gear, hydraulic fluid pressure

  The steering wheel ABSTRACTS the mechanical complexity.
```

### Abstract Classes:
```csharp
// abstract class = CANNOT be instantiated directly
// It's a TEMPLATE that child classes MUST complete

public abstract class PaymentProcessor
{
    // Regular property — shared by all children
    public string TransactionId { get; protected set; }

    // Regular method — shared by all children
    public void GenerateTransactionId()
    {
        TransactionId = Guid.NewGuid().ToString("N")[..8].ToUpper();
    }

    // ABSTRACT method — NO body! Children MUST implement this!
    public abstract bool ProcessPayment(decimal amount, string currency);

    // ABSTRACT method — children MUST implement
    public abstract bool Refund(string transactionId);

    // Virtual method — children CAN override (optional)
    public virtual string GetReceipt()
    {
        return $"Transaction: {TransactionId}";
    }
}

// Child MUST implement all abstract methods
public class CreditCardProcessor : PaymentProcessor
{
    public override bool ProcessPayment(decimal amount, string currency)
    {
        GenerateTransactionId();  // Use parent's method
        Console.WriteLine($"💳 Charging credit card ₹{amount} {currency}");
        // Connect to card network, validate, charge...
        return true;
    }

    public override bool Refund(string transactionId)
    {
        Console.WriteLine($"💳 Refunding transaction {transactionId}");
        return true;
    }
}

public class UpiProcessor : PaymentProcessor
{
    public override bool ProcessPayment(decimal amount, string currency)
    {
        GenerateTransactionId();
        Console.WriteLine($"📱 UPI payment ₹{amount} {currency}");
        // Send UPI request, wait for PIN...
        return true;
    }

    public override bool Refund(string transactionId)
    {
        Console.WriteLine($"📱 UPI refund for {transactionId}");
        return true;
    }

    public override string GetReceipt()  // Override virtual method
    {
        return $"UPI Receipt | {base.GetReceipt()}";
    }
}

// ── USAGE ──────────────────────────────────────────
// var p = new PaymentProcessor();  // ❌ Can't instantiate abstract class!

PaymentProcessor processor = new CreditCardProcessor();
processor.ProcessPayment(999.99m, "INR");  // 💳 Charging credit card

processor = new UpiProcessor();
processor.ProcessPayment(500m, "INR");     // 📱 UPI payment
```

### Interfaces — Pure Abstraction:
```csharp
// Interface = 100% abstract — ONLY defines WHAT, never HOW
// Like a CONTRACT: "Any class that implements me MUST have these methods"

public interface IExportable
{
    string ExportToCsv();
    byte[] ExportToPdf();
    string ExportToJson();
}

public interface IActivatable
{
    bool IsActive { get; }
    void Activate();
    void Deactivate();
}

// A class can implement MULTIPLE interfaces
public class Vendor : BaseEntity, IExportable, IActivatable
{
    public string VendorName { get; set; }
    public string Status { get; set; }

    // IActivatable implementation
    public bool IsActive => Status == "Active";
    public void Activate() => Status = "Active";
    public void Deactivate() => Status = "Inactive";

    // IExportable implementation
    public string ExportToCsv() => $"{Id},{VendorName},{Status}";
    public byte[] ExportToPdf() => Encoding.UTF8.GetBytes($"PDF: {VendorName}");
    public string ExportToJson() => JsonSerializer.Serialize(this);
}
```

---

## 9. Interfaces vs Abstract Classes

This is one of the **most common questions** and an important design decision.

```
┌────────────────────────┬──────────────────────┬──────────────────────┐
│ Feature                │ Abstract Class       │ Interface            │
├────────────────────────┼──────────────────────┼──────────────────────┤
│ Keyword                │ abstract class       │ interface            │
│ Can instantiate?       │ ❌ No                │ ❌ No                │
│ Can have constructor?  │ ✅ Yes               │ ❌ No                │
│ Can have fields?       │ ✅ Yes               │ ❌ No                │
│ Can have method body?  │ ✅ Yes (non-abstract)│ ✅ Yes (default, C#8)│
│ Multiple inheritance?  │ ❌ One class only    │ ✅ Many interfaces   │
│ Access modifiers?      │ ✅ Any               │ public only (default)│
│ When to use?           │ "IS A" relationship  │ "CAN DO" capability  │
│                        │ Share code + state   │ Define a contract    │
└────────────────────────┴──────────────────────┴──────────────────────┘
```

### When to Use Which?
```csharp
// Use ABSTRACT CLASS when:
// → Classes share common code/state (fields, constructors)
// → "IS A" relationship: "Vendor IS A BaseEntity"

public abstract class BaseEntity        // Shared state + code
{
    public int Id { get; set; }          // Shared field
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public void SoftDelete() { /* shared logic */ }  // Shared method
}
public class Vendor : BaseEntity { }    // Vendor IS A BaseEntity

// Use INTERFACE when:
// → Define a CAPABILITY that multiple unrelated classes can have
// → "CAN DO" relationship: "Vendor CAN be exported"

public interface IExportable { string ExportToCsv(); }
public class Vendor : IExportable { }      // Vendor CAN export
public class Report : IExportable { }      // Report CAN export
public class Invoice : IExportable { }     // Invoice CAN export
// (Vendor, Report, Invoice are unrelated — but all CAN export)
```

### Real-World Pattern — Dependency Injection with Interfaces:
```csharp
// ── INTERFACE (Contract) ───────────────────────────
public interface IVendorRepository
{
    Task<Vendor> GetByIdAsync(int id);
    Task<List<Vendor>> GetAllAsync();
    Task CreateAsync(Vendor vendor);
    Task UpdateAsync(Vendor vendor);
    Task DeleteAsync(int id);
}

// ── IMPLEMENTATION 1: SQL Server ───────────────────
public class SqlVendorRepository : IVendorRepository
{
    private readonly AppDbContext _db;

    public async Task<Vendor> GetByIdAsync(int id)
        => await _db.Vendors.FindAsync(id);

    public async Task<List<Vendor>> GetAllAsync()
        => await _db.Vendors.ToListAsync();
    // ... other methods
}

// ── IMPLEMENTATION 2: In-Memory (for testing) ─────
public class InMemoryVendorRepository : IVendorRepository
{
    private readonly List<Vendor> _vendors = new();

    public Task<Vendor> GetByIdAsync(int id)
        => Task.FromResult(_vendors.FirstOrDefault(v => v.Id == id));

    public Task<List<Vendor>> GetAllAsync()
        => Task.FromResult(_vendors.ToList());
    // ... other methods
}

// ── CONTROLLER doesn't care WHICH implementation ───
public class VendorController : ControllerBase
{
    private readonly IVendorRepository _repo;  // Uses INTERFACE, not class!

    public VendorController(IVendorRepository repo) => _repo = repo;

    [HttpGet("{id}")]
    public async Task<IActionResult> Get(int id)
    {
        var vendor = await _repo.GetByIdAsync(id);
        return vendor == null ? NotFound() : Ok(vendor);
    }
}

// ── REGISTRATION in Program.cs ─────────────────────
// Production: Use SQL Server
builder.Services.AddScoped<IVendorRepository, SqlVendorRepository>();

// Testing: Swap to In-Memory (no code changes in controller!)
builder.Services.AddScoped<IVendorRepository, InMemoryVendorRepository>();
```

---

## 10. Static Members & Static Classes

> **The big idea:** Normally, members belong to an **object** (instance). A `static` member belongs to the **class itself** — shared by everyone, existing before any object is created.

### Real-World Analogy

Think of a **company** (the class) vs **employees** (instances):

| Thing | Belongs to | Example |
|-------|-----------|---------|
| Employee's salary | The **employee** (instance) | Each person has their own salary |
| Company logo | The **company** (class) | One logo shared by everyone |
| Number of employees | The **company** (class) | One counter, shared |

The logo and employee count are **static** — they exist at the company level, not per employee.

---

### 10.1 Static Members on a Regular Class

A normal class can have both **instance** members (per object) and **static** members (per class).

```csharp
public class Vendor
{
    // ── Instance members ─ each Vendor object has its own copy ──
    public int Id { get; set; }
    public string Name { get; set; } = "";

    // ── Static members ─ ONE copy shared by ALL Vendors ──
    public static int TotalVendorsCreated { get; private set; }
    public static readonly string CompanyDomain = "vendors.example.com";

    public Vendor(string name)
    {
        Name = name;
        TotalVendorsCreated++;       // shared counter bumps up
    }

    // Static method — called on the class, not an object
    public static string BuildEmail(string user) => $"{user}@{CompanyDomain}";
}
```

**Using them:**
```csharp
var v1 = new Vendor("Acme");
var v2 = new Vendor("Globex");

Console.WriteLine(Vendor.TotalVendorsCreated);   // 2   (NOT v1.Total... — that's illegal)
Console.WriteLine(Vendor.BuildEmail("sales"));   // sales@vendors.example.com
```

> **Key rule:** You access static members via the **class name**, not via an instance. `v1.TotalVendorsCreated` is a compile error.

---

### 10.2 Static Classes

A **`static class`** is a class that:
- Cannot be instantiated (`new StaticClass()` is a compile error)
- Cannot have instance members — **every member must be `static`**
- Is implicitly `sealed` — you cannot inherit from it

Use it for **pure utility / helper code** that has no state worth instantiating.

```csharp
public static class VendorValidator
{
    private const int MinNameLength = 2;

    public static bool IsValidName(string? name) =>
        !string.IsNullOrWhiteSpace(name) && name.Length >= MinNameLength;

    public static bool IsValidGstin(string gstin) =>
        gstin?.Length == 15;
}

// Usage
if (!VendorValidator.IsValidName(vendor.Name))
    throw new ArgumentException("Bad name");
```

**Built-in examples you already use every day:**
- `Math` → `Math.Min`, `Math.Sqrt`, `Math.PI`
- `Console` → `Console.WriteLine`
- `File`, `Directory`, `Path` (in `System.IO`)
- `Enumerable` → all the LINQ methods (`Where`, `Select`, ...)

---

### 10.3 Static Constructor

A **static constructor** runs **once** — the first time the class is touched (accessing any static member or creating an instance). You can't call it, you can't give it parameters, and it has no access modifier.

```csharp
public class AppConfig
{
    public static string Environment { get; }
    public static DateTime StartedAt { get; }

    static AppConfig()                          // ← runs ONCE, automatically
    {
        Environment = System.Environment.GetEnvironmentVariable("ASPNETCORE_ENVIRONMENT") ?? "Production";
        StartedAt   = DateTime.UtcNow;
        Console.WriteLine($"AppConfig initialized for {Environment}");
    }
}
```

Good for: initializing expensive static state, reading config once, building lookup tables.

---

### 10.4 `static readonly` vs `const`

Both hold "values that don't change", but they behave differently:

| Feature | `const` | `static readonly` |
|---------|---------|-------------------|
| Evaluated at | **Compile time** | **Runtime** |
| Allowed types | Primitives + `string` only | **Any** type |
| Can use `new`, method calls | ❌ No | ✅ Yes |
| Baked into callers | ✅ Yes (changing requires recompiling callers!) | ❌ No |
| Implicitly static | ✅ Yes | You write `static` explicitly |

```csharp
public class Limits
{
    public const int MaxVendors = 1000;                          // compile-time literal
    public static readonly TimeSpan Timeout = TimeSpan.FromSeconds(30);  // runtime value
    public static readonly string[] AllowedTiers = { "Gold", "Silver" }; // object
}
```

> **Rule of thumb:** Prefer `static readonly` for anything non-primitive, or any value that might evolve across versions. Use `const` only for true compile-time constants (enum-like numbers, fixed strings).

---

### 10.5 Static Classes Host Extension Methods

**Extension methods must live in a static class**, and the method itself must be static with `this` on the first parameter. This is the most common reason you'll write a static class in real code.

```csharp
public static class StringExtensions
{
    public static bool IsValidEmail(this string? s) =>
        !string.IsNullOrWhiteSpace(s) && s.Contains('@');

    public static string Truncate(this string s, int max) =>
        s.Length <= max ? s : s[..max] + "...";
}

// Usage — feels like an instance method, but it's really StringExtensions.Truncate(name, 20)
var shortName = vendor.Name.Truncate(20);
```

---

### 10.6 `using static` — Importing Static Members

C# 6+ lets you import a type's static members so you can drop the class-name prefix:

```csharp
using static System.Math;
using static System.Console;

WriteLine(Sqrt(16));     // instead of Console.WriteLine(Math.Sqrt(16));
WriteLine(PI);
```

Useful in math-heavy code, but use sparingly — overuse hurts readability.

---

### 10.7 Thread-Safety Warning

Static state is **shared across all threads** in your process. In a web API, this means **every request reads and writes the same instance.**

```csharp
public static class Counter
{
    private static int _hits;
    public static void Increment() => _hits++;    // ❌ NOT thread-safe!
    public static int Value => _hits;
}
```

Under load, `_hits++` is three operations (read, add, write) that can interleave → lost updates. Fix with `Interlocked`:

```csharp
public static class Counter
{
    private static int _hits;
    public static void Increment() => Interlocked.Increment(ref _hits);  // ✅ atomic
    public static int Value => _hits;
}
```

For richer state use `lock`, `ConcurrentDictionary<TKey,TValue>`, or avoid static state altogether.

> ⚠️ **Rule:** In ASP.NET Core, prefer DI with `Singleton` lifetime over `static` state. Singletons are easier to test, swap, and reason about.

---

### 10.8 Modern C# Extras

**Static local functions (C# 8+)** — a nested function that can't capture enclosing variables; slightly faster and clearer intent:

```csharp
public int Calculate(IEnumerable<Vendor> vs)
{
    return vs.Sum(Score);

    static int Score(Vendor v) => v.IsActive ? 10 : 0;   // no capture = safer
}
```

**`static abstract` interface members (C# 11 / .NET 7+)** — interfaces can now declare static members that implementations must provide. Enables generic math and factory patterns:

```csharp
public interface IParseable<T>
{
    static abstract T Parse(string input);
}

public class VendorId : IParseable<VendorId>
{
    public int Value { get; init; }
    public static VendorId Parse(string s) => new() { Value = int.Parse(s) };
}

// Generic method can now call T.Parse — impossible before C# 11
public static T Read<T>(string s) where T : IParseable<T> => T.Parse(s);
```

---

### 10.9 Static vs Singleton — Which to Use?

They feel similar, but they serve different goals:

| Aspect | `static class` | Singleton (DI `AddSingleton`) |
|--------|---------------|-------------------------------|
| Instantiation | Never | Exactly once per app |
| Can implement interface | ❌ No | ✅ Yes |
| Can be injected | ❌ No — you call `ClassName.Method()` | ✅ Yes — via constructor |
| Easy to mock in tests | ❌ Hard | ✅ Swap implementation |
| Holds dependencies | ❌ Awkward | ✅ Natural |
| Best for | Stateless pure utilities (`Math`, validators, formatters) | Services with dependencies, config, caches |

**Rule:** In a modern ASP.NET Core app, **default to singletons via DI**. Reach for `static class` only for genuinely stateless helpers.

---

### 10.10 When to Use vs Avoid

**✅ Good uses of `static`:**
- Pure helper functions with no state (`Math`, parsers, formatters)
- Extension methods
- Constants and lookup tables (`static readonly`)
- Factory-style helpers that don't need dependencies

**❌ Avoid `static` for:**
- Anything holding mutable state in a web app (testability + thread-safety nightmares)
- Business logic that depends on services (use DI instead)
- Anything you want to mock or swap in tests

---

### 🎯 Quick Summary

| Concept | One-liner |
|---------|-----------|
| Static member | Belongs to the **class**, shared by all instances |
| Static class | Can't be instantiated or inherited; all members must be static |
| Static constructor | Runs once, auto, before first use |
| `const` | Compile-time literal (primitives + `string`) |
| `static readonly` | Runtime value, any type |
| `using static` | Import static members without class prefix |
| `static abstract` | Interface requires static impl (C# 11+) |
| Static local fn | Nested fn that can't capture outer vars |

### Exercises

**Exercise 1 — Counter**
Give the `Vendor` class a `static int TotalVendorsCreated` that increments in the constructor. Create 5 vendors and print the count.

**Exercise 2 — Utility Class**
Build a `static class PriceHelper` with `CalculateGst(decimal amount, decimal rate)` and `FormatInr(decimal amount)`. Use it without creating an instance.

**Exercise 3 — Static Constructor**
Add a static constructor to a `VendorRegistry` class that loads a `Dictionary<int, string>` of seed vendors once. Verify (with a `Console.WriteLine`) that it runs only on first access.

**Exercise 4 — `const` vs `static readonly`**
Declare `const int MaxNameLength = 50` and `static readonly TimeSpan Timeout = TimeSpan.FromSeconds(10)`. Try making `Timeout` a `const` and explain the compile error.

**Exercise 5 — Thread-Safety**
Create a `static int` counter incremented from 1000 parallel tasks. Run it, see the wrong result, then fix with `Interlocked.Increment`.

**Exercise 6 — Static vs Singleton**
Convert a `static class VendorCache` into a `Singleton` service (`IVendorCache` + `VendorCache : IVendorCache` registered with `AddSingleton`). Inject it into a controller and compare the two styles.

---

## 11. SOLID Principles

SOLID = 5 OOP best practices that make your code **clean, flexible, and maintainable**.

### S - Single Responsibility Principle (SRP)
```
A class should have ONLY ONE reason to change.

❌ BAD: VendorService handles CRUD + email + PDF export + logging
✅ GOOD: Separate classes for each responsibility
```
```csharp
// ❌ BAD — This class does TOO MUCH
public class VendorService
{
    public void CreateVendor(Vendor v) { /* save to DB */ }
    public void SendWelcomeEmail(Vendor v) { /* send email */ }
    public byte[] GenerateReport(List<Vendor> v) { /* create PDF */ }
    public void LogAction(string msg) { /* write to log */ }
}

// ✅ GOOD — Each class has ONE job
public class VendorService { public void Create(Vendor v) { } }
public class EmailService { public void SendWelcome(Vendor v) { } }
public class ReportService { public byte[] Generate(List<Vendor> v) { } }
public class LogService { public void Log(string msg) { } }
```

### O - Open/Closed Principle (OCP)
```
Open for EXTENSION, Closed for MODIFICATION.
Add new features by adding new code, NOT changing existing code.
```
```csharp
// ❌ BAD — Must modify this method every time you add a new export type
public string Export(string format, Vendor vendor)
{
    if (format == "csv") return vendor.ToCsv();
    if (format == "json") return vendor.ToJson();
    if (format == "xml") return vendor.ToXml();    // Added later — modified!
    // Every new format = change this code 💥
}

// ✅ GOOD — Add new formats WITHOUT changing existing code
public interface IExporter { string Export(Vendor vendor); }
public class CsvExporter : IExporter { public string Export(Vendor v) => /*csv*/; }
public class JsonExporter : IExporter { public string Export(Vendor v) => /*json*/; }
public class XmlExporter : IExporter { public string Export(Vendor v) => /*xml*/; }
// New format? Just add a NEW class! No existing code changes!
```

### L - Liskov Substitution Principle (LSP)
```
Child classes should be usable WHEREVER parent class is expected
without breaking anything.
```
```csharp
// If code works with BaseEntity, it MUST work with Vendor too
void ProcessEntity(BaseEntity entity)
{
    entity.SoftDelete();  // Must work for ANY BaseEntity child
}

ProcessEntity(new Vendor());   // ✅ Works
ProcessEntity(new User());     // ✅ Works
```

### I - Interface Segregation Principle (ISP)
```
Don't force classes to implement methods they don't use.
Split large interfaces into smaller, specific ones.
```
```csharp
// ❌ BAD — One big interface forces all implementations to have everything
public interface IVendorService
{
    void Create(Vendor v);
    void Update(Vendor v);
    void Delete(int id);
    byte[] ExportToPdf();        // Not every service needs this!
    void SendNotification();     // Not every service needs this!
}

// ✅ GOOD — Small, focused interfaces
public interface ICrudService<T> { void Create(T item); void Update(T item); }
public interface IExportable { byte[] ExportToPdf(); }
public interface INotifiable { void SendNotification(); }

// Classes implement ONLY what they need
public class VendorService : ICrudService<Vendor>, IExportable { }
public class SimpleVendorService : ICrudService<Vendor> { }  // No export needed!
```

### D - Dependency Inversion Principle (DIP)
```
Depend on ABSTRACTIONS (interfaces), not CONCRETE classes.
```
```csharp
// ❌ BAD — Controller depends on a SPECIFIC class
public class VendorController
{
    private readonly SqlVendorRepository _repo = new();  // Tightly coupled!
    // Can't switch to a different database without changing this code!
}

// ✅ GOOD — Controller depends on INTERFACE
public class VendorController
{
    private readonly IVendorRepository _repo;  // Depends on abstraction!
    public VendorController(IVendorRepository repo) => _repo = repo;
    // Can swap SQL → MongoDB → InMemory without changing controller!
}
```

---

## 12. OOP in Your Daily Work - Real Examples

### Where You Already USE OOP (Even Without Knowing!):

```csharp
// ── 1. ENTITY FRAMEWORK MODELS = Classes ───────────
public class Vendor          // ← This is a CLASS (OOP!)
{
    public int Id { get; set; }             // ← Properties (Encapsulation!)
    public string VendorName { get; set; }
    public List<Order> Orders { get; set; } // ← Relationship (Composition!)
}

// ── 2. CONTROLLERS = Inheritance + DI ──────────────
public class VendorController : ControllerBase  // ← Inheritance!
{
    private readonly IVendorService _service;   // ← Interface (Abstraction!)
    public VendorController(IVendorService s) => _service = s; // ← DI (DIP!)
}

// ── 3. DbContext = Inheritance ─────────────────────
public class AppDbContext : DbContext           // ← Inherits from DbContext!
{
    public DbSet<Vendor> Vendors { get; set; } // ← Property
}

// ── 4. MIDDLEWARE = Interfaces ─────────────────────
public class LoggingMiddleware : IMiddleware    // ← Implements interface!
{
    public async Task InvokeAsync(HttpContext ctx, RequestDelegate next)
    {
        Console.WriteLine($"Request: {ctx.Request.Path}");
        await next(ctx);
    }
}

// ── 5. EXCEPTIONS = Inheritance ────────────────────
public class VendorNotFoundException : Exception  // ← Inherits Exception!
{
    public int VendorId { get; }
    public VendorNotFoundException(int id)
        : base($"Vendor with Id {id} was not found")
    {
        VendorId = id;
    }
}
```

### OOP in ASP.NET Core Architecture:
```
┌──────────────────────────────────────────────────────┐
│                 ASP.NET Core Web API                  │
│                                                      │
│  Controller (Inheritance: ControllerBase)             │
│    └── Uses IVendorService (Interface: Abstraction)  │
│          └── VendorService (Class: Encapsulation)    │
│                └── Uses IVendorRepo (Interface: DIP) │
│                      └── SqlVendorRepo (Polymorphism)│
│                            └── AppDbContext (Inherit)│
│                                  └── Vendor (Class)  │
│                                                      │
│  Every layer uses OOP concepts!                      │
└──────────────────────────────────────────────────────┘
```

---

## 13. Common OOP Terms

```
┌────────────────────┬──────────────────────────────────────────────────┐
│ Term               │ Meaning                                          │
├────────────────────┼──────────────────────────────────────────────────┤
│ Class              │ Blueprint/template for creating objects           │
│ Object             │ Instance created from a class                    │
│ Property           │ Data stored in an object (Name, Email, etc.)     │
│ Method             │ Action an object can perform (Save, Delete)      │
│ Constructor        │ Special method that runs when creating an object │
│ Encapsulation      │ Hide data, control access via properties/methods │
│ Inheritance        │ Child class gets parent's properties & methods   │
│ Polymorphism       │ Same method, different behavior per class        │
│ Abstraction        │ Show WHAT, hide HOW (interfaces, abstract)      │
│ Interface          │ Contract: "you MUST implement these methods"     │
│ Abstract Class     │ Partial blueprint: some implemented, some not   │
│ Virtual            │ Method that CAN be overridden by child          │
│ Override           │ Child replaces parent's virtual method           │
│ Sealed             │ Class that CANNOT be inherited                   │
│ Static             │ Belongs to the CLASS, not to any instance        │
│ Composition        │ Object CONTAINS other objects ("HAS A")         │
│ Overloading        │ Same method name, different parameters           │
│ Overriding         │ Child replaces parent method (virtual/override)  │
│ DI (Dependency     │ Inject dependencies via constructor instead      │
│   Injection)       │   of creating them inside the class              │
│ SOLID              │ 5 OOP best practices for clean code              │
│ Coupling           │ How dependent classes are on each other (low=✅) │
│ Cohesion           │ How focused a class is on one task (high=✅)     │
└────────────────────┴──────────────────────────────────────────────────┘
```

---

## 📝 Quick Revision Sheet

```
┌────────────────┬─────────────────────────────────────────────────────┐
│ Concept        │ One-Line Summary                                    │
├────────────────┼─────────────────────────────────────────────────────┤
│ Class          │ Blueprint: public class Vendor { }                  │
│ Object         │ Instance: var v = new Vendor();                     │
│ Encapsulation  │ Private data + Public methods = Protection          │
│ Inheritance    │ class Vendor : BaseEntity — gets parent's stuff     │
│ Polymorphism   │ virtual + override — same call, different behavior  │
│ Abstraction    │ abstract class / interface — define contract        │
│ Interface      │ CAN DO: IExportable, IActivatable                  │
│ Abstract Class │ IS A + share code: abstract class BaseEntity        │
│ SOLID          │ S=One job, O=Extend don't modify, L=Substitutable  │
│                │ I=Small interfaces, D=Depend on abstractions        │
└────────────────┴─────────────────────────────────────────────────────┘
```

### The 4 Pillars — Memory Trick (EIPA):
```
E - Encapsulation   🔒 "Hide and Protect"
I - Inheritance      ♻️ "Reuse from Parent"
P - Polymorphism     🔀 "Same Call, Different Action"
A - Abstraction      🎭 "Show What, Hide How"
```

---

**Related Guides:**
**[SQL Learning →](../sql-learning/01-SQL-Basics.md)**
**[gRPC Guide →](../grpc-learning/01-gRPC-Complete-Guide.md)**