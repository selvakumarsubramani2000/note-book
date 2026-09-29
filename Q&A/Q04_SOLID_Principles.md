# Question 4: Explain the SOLID principles with code examples from your project.

## Answer

SOLID is an acronym for five design principles that make software more understandable, flexible, and maintainable.

---

## S - Single Responsibility Principle (SRP)

### Definition
**A class should have only ONE reason to change** - meaning it should have only ONE job or responsibility.

### Bad Example (Violates SRP):
```csharp
// This class does TOO MUCH - handles user data, email, and logging
public class UserService
{
    public void RegisterUser(User user)
    {
        // 1. Save user to database
        SaveToDatabase(user);
        
        // 2. Send welcome email
        var emailBody = $"Welcome {user.Name}!";
        var smtpClient = new SmtpClient("smtp.gmail.com");
        smtpClient.Send(user.Email, "Welcome", emailBody);
        
        // 3. Log the action
        File.AppendAllText("log.txt", $"User {user.Name} registered at {DateTime.Now}");
    }
}
```

### Good Example (Follows SRP):
```csharp
// Each class has ONE responsibility
public class UserService
{
    private readonly IUserRepository _userRepository;
    private readonly IEmailService _emailService;
    private readonly ILogger _logger;
    
    public UserService(IUserRepository userRepository, IEmailService emailService, ILogger logger)
    {
        _userRepository = userRepository;
        _emailService = emailService;
        _logger = logger;
    }
    
    public void RegisterUser(User user)
    {
        _userRepository.Save(user);
        _emailService.SendWelcomeEmail(user);
        _logger.LogInfo($"User {user.Name} registered");
    }
}

public class UserRepository : IUserRepository
{
    public void Save(User user) { /* Only handles database operations */ }
}

public class EmailService : IEmailService
{
    public void SendWelcomeEmail(User user) { /* Only handles email sending */ }
}

public class FileLogger : ILogger
{
    public void LogInfo(string message) { /* Only handles logging */ }
}
```

---

## O - Open/Closed Principle (OCP)

### Definition
**Software entities should be OPEN for extension but CLOSED for modification** - you should be able to add new functionality without changing existing code.

### Bad Example (Violates OCP):
```csharp
public class PaymentProcessor
{
    public void ProcessPayment(string paymentType, decimal amount)
    {
        if (paymentType == "CreditCard")
        {
            // Credit card logic
        }
        else if (paymentType == "PayPal")
        {
            // PayPal logic
        }
        else if (paymentType == "Stripe") // Adding new payment = modifying this class!
        {
            // Stripe logic
        }
    }
}
```

### Good Example (Follows OCP):
```csharp
// Abstract base class - CLOSED for modification
public abstract class PaymentProcessor
{
    public abstract void ProcessPayment(decimal amount);
}

// OPEN for extension - just add new classes
public class CreditCardPaymentProcessor : PaymentProcessor
{
    public override void ProcessPayment(decimal amount)
    {
        Console.WriteLine($"Processing ${amount} via Credit Card");
    }
}

public class PayPalPaymentProcessor : PaymentProcessor
{
    public override void ProcessPayment(decimal amount)
    {
        Console.WriteLine($"Processing ${amount} via PayPal");
    }
}

// Adding Stripe? Just create a new class - no modification needed!
public class StripePaymentProcessor : PaymentProcessor
{
    public override void ProcessPayment(decimal amount)
    {
        Console.WriteLine($"Processing ${amount} via Stripe");
    }
}
```

---

## L - Liskov Substitution Principle (LSP)

### Definition
**Objects of a derived class should be able to replace objects of the base class without breaking the application.**

### Bad Example (Violates LSP):
```csharp
public class Bird
{
    public virtual void Fly()
    {
        Console.WriteLine("Flying...");
    }
}

public class Penguin : Bird
{
    public override void Fly()
    {
        throw new NotSupportedException("Penguins can't fly!"); // Breaks LSP!
    }
}

// This code will crash with Penguin
void MakeBirdFly(Bird bird)
{
    bird.Fly(); // Works with Bird, crashes with Penguin!
}
```

### Good Example (Follows LSP):
```csharp
public abstract class Bird
{
    public abstract void Move();
}

public class FlyingBird : Bird
{
    public override void Move()
    {
        Console.WriteLine("Flying in the sky");
    }
}

public class Penguin : Bird
{
    public override void Move()
    {
        Console.WriteLine("Swimming in water");
    }
}

// Works correctly with all birds
void MakeBirdMove(Bird bird)
{
    bird.Move(); // Works with FlyingBird AND Penguin!
}
```

---

## I - Interface Segregation Principle (ISP)

### Definition
**Clients should not be forced to depend on interfaces they don't use** - better to have multiple small, specific interfaces than one large, general-purpose interface.

### Bad Example (Violates ISP):
```csharp
// Too many methods - not all implementations need all of them
public interface IWorker
{
    void Work();
    void Eat();
    void Sleep();
    void GetSalary();
}

// Robot doesn't eat or sleep but is forced to implement these methods!
public class Robot : IWorker
{
    public void Work() { Console.WriteLine("Working..."); }
    public void Eat() { throw new NotImplementedException(); } // Forced to implement!
    public void Sleep() { throw new NotImplementedException(); } // Forced to implement!
    public void GetSalary() { Console.WriteLine("No salary for robots"); }
}
```

### Good Example (Follows ISP):
```csharp
// Segregated interfaces
public interface IWorkable
{
    void Work();
}

public interface IEatable
{
    void Eat();
}

public interface ISleepable
{
    void Sleep();
}

public interface IPayable
{
    void GetSalary();
}

// Human implements all interfaces
public class Human : IWorkable, IEatable, ISleepable, IPayable
{
    public void Work() { Console.WriteLine("Human working"); }
    public void Eat() { Console.WriteLine("Human eating"); }
    public void Sleep() { Console.WriteLine("Human sleeping"); }
    public void GetSalary() { Console.WriteLine("Receiving salary"); }
}

// Robot only implements what it needs
public class Robot : IWorkable
{
    public void Work() { Console.WriteLine("Robot working"); }
}
```

---

## D - Dependency Inversion Principle (DIP)

### Definition
**High-level modules should not depend on low-level modules. Both should depend on abstractions.**

### Bad Example (Violates DIP):
```csharp
// High-level class depends directly on low-level class
public class OrderService
{
    private SqlServerDatabase _database = new SqlServerDatabase(); // Tight coupling!
    
    public void CreateOrder(Order order)
    {
        _database.Save(order);
    }
}

public class SqlServerDatabase
{
    public void Save(Order order) { /* SQL Server specific code */ }
}
```

### Good Example (Follows DIP):
```csharp
// Abstraction
public interface IDatabase
{
    void Save(Order order);
}

// Low-level implementations
public class SqlServerDatabase : IDatabase
{
    public void Save(Order order) { /* SQL Server code */ }
}

public class MongoDatabase : IDatabase
{
    public void Save(Order order) { /* MongoDB code */ }
}

// High-level module depends on abstraction
public class OrderService
{
    private readonly IDatabase _database;
    
    // Dependency is injected
    public OrderService(IDatabase database)
    {
        _database = database;
    }
    
    public void CreateOrder(Order order)
    {
        _database.Save(order); // Works with ANY database implementation!
    }
}

// In Startup.cs
services.AddScoped<IDatabase, SqlServerDatabase>();
// Easy to switch: services.AddScoped<IDatabase, MongoDatabase>();
```

---

## Real-World Project Example (All Together)

```csharp
// D - Depend on abstractions
public interface IRepository<T>
{
    Task<T> GetByIdAsync(int id);
}

public interface INotificationService
{
    Task SendAsync(string message);
}

// I - Small, focused interfaces
public interface IOrderProcessor
{
    Task ProcessOrderAsync(Order order);
}

// S - Single responsibility
public class OrderService : IOrderProcessor
{
    private readonly IRepository<Order> _orderRepository;
    private readonly INotificationService _notificationService;
    
    public OrderService(IRepository<Order> orderRepository, INotificationService notificationService)
    {
        _orderRepository = orderRepository;
        _notificationService = notificationService;
    }
    
    public async Task ProcessOrderAsync(Order order)
    {
        await _orderRepository.SaveAsync(order);
        await _notificationService.SendAsync($"Order {order.Id} processed");
    }
}
```

---

## Summary

| Principle | Remember As |
|-----------|------------|
| **S**RP | One class, one job |
| **O**CP | Add new code, don't modify old code |
| **L**SP | Substitution should work seamlessly |
| **I**SP | Small, focused interfaces |
| **D**IP | Depend on interfaces, not implementations |
