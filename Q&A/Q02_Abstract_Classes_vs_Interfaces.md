# Question 2: What is the difference between abstract classes and interfaces? When would you use each?

## Answer

### The Big Picture

Think of **Abstract Classes** as a **template with some pre-built parts**, while **Interfaces** are like a **contract or blueprint** that says "you must implement these methods."

---

## Abstract Classes

### What is an Abstract Class?

An abstract class is a **partially implemented class** that cannot be instantiated directly. It's meant to be a base class that other classes inherit from.

### Key Characteristics:

1. **Can have both abstract and concrete methods**
2. **Can have fields and properties**
3. **Can have constructors**
4. **Supports access modifiers** (public, private, protected)
5. **A class can inherit only ONE abstract class** (single inheritance)
6. **Can have implementation code**

### Example:

```csharp
public abstract class Vehicle
{
    // Fields
    protected string brand;
    protected int year;
    
    // Constructor
    public Vehicle(string brand, int year)
    {
        this.brand = brand;
        this.year = year;
    }
    
    // Concrete method (fully implemented)
    public void DisplayInfo()
    {
        Console.WriteLine($"Brand: {brand}, Year: {year}");
    }
    
    // Abstract method (must be implemented by derived classes)
    public abstract void StartEngine();
    
    // Abstract method
    public abstract double CalculateFuelEfficiency();
}

// Derived class
public class Car : Vehicle
{
    public Car(string brand, int year) : base(brand, year)
    {
    }
    
    // Must implement abstract methods
    public override void StartEngine()
    {
        Console.WriteLine("Car engine started with key ignition");
    }
    
    public override double CalculateFuelEfficiency()
    {
        return 25.5; // km per liter
    }
}
```

---

## Interfaces

### What is an Interface?

An interface is a **pure contract** that defines what methods a class must implement, but doesn't provide any implementation (until C# 8.0 which allows default implementations).

### Key Characteristics:

1. **Only method signatures** (traditionally - no implementation)
2. **Cannot have fields** (can have properties)
3. **Cannot have constructors**
4. **All members are public by default**
5. **A class can implement MULTIPLE interfaces** (multiple inheritance)
6. **No access modifiers needed**

### Example:

```csharp
public interface IPayable
{
    void ProcessPayment(decimal amount);
    bool ValidatePayment();
    string GetPaymentStatus();
}

public interface IRefundable
{
    void ProcessRefund(decimal amount);
    bool CanRefund();
}

// A class can implement multiple interfaces
public class CreditCardPayment : IPayable, IRefundable
{
    public void ProcessPayment(decimal amount)
    {
        Console.WriteLine($"Processing credit card payment of ${amount}");
    }
    
    public bool ValidatePayment()
    {
        // Validation logic
        return true;
    }
    
    public string GetPaymentStatus()
    {
        return "Completed";
    }
    
    public void ProcessRefund(decimal amount)
    {
        Console.WriteLine($"Processing refund of ${amount}");
    }
    
    public bool CanRefund()
    {
        return true;
    }
}
```

---

## Key Differences Table

| Feature | Abstract Class | Interface |
|---------|---------------|-----------|
| **Implementation** | Can have both abstract and concrete methods | Only method signatures (C# 8.0+ allows default) |
| **Fields** | Can have fields | Cannot have fields |
| **Constructor** | Can have constructors | Cannot have constructors |
| **Access Modifiers** | Can use any access modifier | Members are public by default |
| **Inheritance** | Single inheritance only | Multiple inheritance supported |
| **When to Use** | When classes share common code | When classes share common behavior but different implementations |

---

## When to Use Each?

### Use Abstract Class When:

1. **You have common code to share** among related classes
2. **You want to provide default behavior** that can be overridden
3. **You need constructors or fields**
4. **Classes have an "IS-A" relationship** (Car IS-A Vehicle)

**Example:**
```csharp
// All employees have common fields and some common behavior
public abstract class Employee
{
    public string Name { get; set; }
    public decimal BaseSalary { get; set; }
    
    // Common method
    public void DisplayEmployeeInfo()
    {
        Console.WriteLine($"{Name}: ${BaseSalary}");
    }
    
    // Each employee type calculates bonus differently
    public abstract decimal CalculateBonus();
}
```

### Use Interface When:

1. **You want to define a capability** that multiple unrelated classes can have
2. **You need multiple inheritance**
3. **You want to define a contract** without implementation
4. **Classes have a "CAN-DO" relationship** (Car CAN-BE Drivable, Washable)

**Example:**
```csharp
// Unrelated classes can all be "loggable"
public interface ILoggable
{
    void LogActivity(string message);
}

// Both User and Product can implement ILoggable
public class User : ILoggable { }
public class Product : ILoggable { }
```

---

## Real-World Project Example

```csharp
// Abstract class for shared repository logic
public abstract class BaseRepository<T>
{
    protected readonly DbContext _context;
    
    public BaseRepository(DbContext context)
    {
        _context = context;
    }
    
    // Common implementation
    public virtual async Task<T> GetByIdAsync(int id)
    {
        return await _context.Set<T>().FindAsync(id);
    }
    
    // Must be implemented by derived classes
    public abstract Task<IEnumerable<T>> GetAllActiveAsync();
}

// Interface for auditable entities
public interface IAuditable
{
    DateTime CreatedDate { get; set; }
    string CreatedBy { get; set; }
    DateTime? ModifiedDate { get; set; }
    string ModifiedBy { get; set; }
}

// A class can inherit abstract class AND implement interface
public class ProductRepository : BaseRepository<Product>, IAuditable
{
    public DateTime CreatedDate { get; set; }
    public string CreatedBy { get; set; }
    public DateTime? ModifiedDate { get; set; }
    public string ModifiedBy { get; set; }
    
    public override async Task<IEnumerable<Product>> GetAllActiveAsync()
    {
        // Custom implementation
        return await _context.Products.Where(p => p.IsActive).ToListAsync();
    }
}
```

---

## Summary

- **Abstract Class**: Use when you want to share CODE and have an IS-A relationship
- **Interface**: Use when you want to define a CONTRACT and have a CAN-DO relationship
- You can use BOTH together for maximum flexibility!
