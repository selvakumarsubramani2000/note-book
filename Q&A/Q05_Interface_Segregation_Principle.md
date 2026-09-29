# Question 5: What is Interface Segregation Principle? Provide a practical example.

## Answer

### What is Interface Segregation Principle (ISP)?

The **Interface Segregation Principle** states:
> **"No client should be forced to depend on methods it does not use."**

In simpler terms: **Create small, specific interfaces rather than one large, general-purpose interface.**

### Why is ISP Important?

1. **Prevents Fat Interfaces**: Avoids bloated interfaces with too many methods
2. **Reduces Dependencies**: Classes only implement what they actually need
3. **Improves Flexibility**: Easier to add new implementations
4. **Better Code Organization**: Clear, focused contracts
5. **Easier Testing**: Smaller interfaces are easier to mock and test

---

## The Problem: Violating ISP

### Bad Example - "Fat Interface"

```csharp
// This interface tries to do TOO MUCH
public interface IMultiFunctionDevice
{
    void Print(Document document);
    void Scan(Document document);
    void Fax(Document document);
    void Email(Document document);
    void Copy(Document document);
}

// Problem 1: Old printer can only print - but must implement ALL methods!
public class OldPrinter : IMultiFunctionDevice
{
    public void Print(Document document)
    {
        Console.WriteLine("Printing document...");
    }
    
    // Forced to implement methods it doesn't support!
    public void Scan(Document document)
    {
        throw new NotSupportedException("This printer cannot scan!");
    }
    
    public void Fax(Document document)
    {
        throw new NotSupportedException("This printer cannot fax!");
    }
    
    public void Email(Document document)
    {
        throw new NotSupportedException("This printer cannot email!");
    }
    
    public void Copy(Document document)
    {
        throw new NotSupportedException("This printer cannot copy!");
    }
}

// Problem 2: Scanner-only device also forced to implement everything!
public class BasicScanner : IMultiFunctionDevice
{
    public void Scan(Document document)
    {
        Console.WriteLine("Scanning document...");
    }
    
    // Forced to implement these even though they're not supported
    public void Print(Document document) { throw new NotSupportedException(); }
    public void Fax(Document document) { throw new NotSupportedException(); }
    public void Email(Document document) { throw new NotSupportedException(); }
    public void Copy(Document document) { throw new NotSupportedException(); }
}
```

**Problems with this approach:**
- Classes implement methods they don't use
- Lots of `NotSupportedException` being thrown
- Confusing for users of the class - which methods actually work?
- Violates the Liskov Substitution Principle too!

---

## The Solution: Following ISP

### Good Example - Segregated Interfaces

```csharp
// Split into small, focused interfaces
public interface IPrinter
{
    void Print(Document document);
}

public interface IScanner
{
    void Scan(Document document);
}

public interface IFax
{
    void Fax(Document document);
}

public interface IEmailer
{
    void Email(Document document);
}

// Now devices only implement what they support!

// Simple printer - only implements IPrinter
public class BasicPrinter : IPrinter
{
    public void Print(Document document)
    {
        Console.WriteLine($"Printing: {document.Name}");
    }
}

// Scanner - only implements IScanner
public class BasicScanner : IScanner
{
    public void Scan(Document document)
    {
        Console.WriteLine($"Scanning: {document.Name}");
    }
}

// Advanced multi-function device - implements multiple interfaces
public class MultiFunctionPrinter : IPrinter, IScanner, IFax, IEmailer
{
    public void Print(Document document)
    {
        Console.WriteLine($"Printing: {document.Name}");
    }
    
    public void Scan(Document document)
    {
        Console.WriteLine($"Scanning: {document.Name}");
    }
    
    public void Fax(Document document)
    {
        Console.WriteLine($"Faxing: {document.Name}");
    }
    
    public void Email(Document document)
    {
        Console.WriteLine($"Emailing: {document.Name}");
    }
}

// Usage - clear what each device can do
public class DocumentManager
{
    public void PrintDocument(IPrinter printer, Document doc)
    {
        printer.Print(doc); // Works with any device that can print
    }
    
    public void ScanDocument(IScanner scanner, Document doc)
    {
        scanner.Scan(doc); // Works with any device that can scan
    }
}
```

---

## Real-World Project Example: User Management System

### Bad Example (Violating ISP):

```csharp
// Fat interface for user operations
public interface IUserService
{
    // Regular user methods
    void Register(User user);
    void Login(string username, string password);
    void UpdateProfile(User user);
    
    // Admin-only methods
    void DeleteUser(int userId);
    void AssignRole(int userId, string role);
    void ViewAllUsers();
    
    // Guest user methods
    void BrowseProducts();
}

// Regular user forced to implement admin methods!
public class RegularUserService : IUserService
{
    public void Register(User user) { /* Implementation */ }
    public void Login(string username, string password) { /* Implementation */ }
    public void UpdateProfile(User user) { /* Implementation */ }
    
    // Doesn't make sense for regular user!
    public void DeleteUser(int userId) { throw new UnauthorizedAccessException(); }
    public void AssignRole(int userId, string role) { throw new UnauthorizedAccessException(); }
    public void ViewAllUsers() { throw new UnauthorizedAccessException(); }
    public void BrowseProducts() { /* Implementation */ }
}
```

### Good Example (Following ISP):

```csharp
// Segregated interfaces
public interface IUserAuthentication
{
    void Register(User user);
    void Login(string username, string password);
    void Logout();
}

public interface IUserProfile
{
    void UpdateProfile(User user);
    User GetProfile(int userId);
}

public interface IUserAdministration
{
    void DeleteUser(int userId);
    void AssignRole(int userId, string role);
    IEnumerable<User> ViewAllUsers();
}

public interface IGuestAccess
{
    void BrowseProducts();
    void SearchProducts(string query);
}

// Regular user service
public class RegularUserService : IUserAuthentication, IUserProfile, IGuestAccess
{
    public void Register(User user) { /* Implementation */ }
    public void Login(string username, string password) { /* Implementation */ }
    public void Logout() { /* Implementation */ }
    public void UpdateProfile(User user) { /* Implementation */ }
    public User GetProfile(int userId) { /* Implementation */ }
    public void BrowseProducts() { /* Implementation */ }
    public void SearchProducts(string query) { /* Implementation */ }
}

// Admin service - has all permissions
public class AdminUserService : IUserAuthentication, IUserProfile, IUserAdministration
{
    public void Register(User user) { /* Implementation */ }
    public void Login(string username, string password) { /* Implementation */ }
    public void Logout() { /* Implementation */ }
    public void UpdateProfile(User user) { /* Implementation */ }
    public User GetProfile(int userId) { /* Implementation */ }
    public void DeleteUser(int userId) { /* Implementation */ }
    public void AssignRole(int userId, string role) { /* Implementation */ }
    public IEnumerable<User> ViewAllUsers() { /* Implementation */ }
}

// Guest service - minimal permissions
public class GuestUserService : IGuestAccess
{
    public void BrowseProducts() { /* Implementation */ }
    public void SearchProducts(string query) { /* Implementation */ }
}
```

---

## Another Practical Example: Repository Pattern

### Bad Example:

```csharp
// This interface has methods not all repositories need
public interface IRepository<T>
{
    T GetById(int id);
    IEnumerable<T> GetAll();
    void Add(T entity);
    void Update(T entity);
    void Delete(int id);
    
    // Not all repositories need these!
    IEnumerable<T> Search(string query);
    void BulkInsert(IEnumerable<T> entities);
    void Archive(int id);
    void Restore(int id);
}
```

### Good Example:

```csharp
// Basic operations that all repositories need
public interface IReadRepository<T>
{
    T GetById(int id);
    IEnumerable<T> GetAll();
}

public interface IWriteRepository<T>
{
    void Add(T entity);
    void Update(T entity);
    void Delete(int id);
}

// Optional capabilities as separate interfaces
public interface ISearchableRepository<T>
{
    IEnumerable<T> Search(string query);
}

public interface IBulkOperationRepository<T>
{
    void BulkInsert(IEnumerable<T> entities);
    void BulkDelete(IEnumerable<int> ids);
}

public interface IArchivableRepository<T>
{
    void Archive(int id);
    void Restore(int id);
}

// Simple read-only repository
public class ReadOnlyProductRepository : IReadRepository<Product>
{
    public Product GetById(int id) { /* Implementation */ }
    public IEnumerable<Product> GetAll() { /* Implementation */ }
}

// Full-featured repository
public class ProductRepository : IReadRepository<Product>, 
                                  IWriteRepository<Product>, 
                                  ISearchableRepository<Product>
{
    public Product GetById(int id) { /* Implementation */ }
    public IEnumerable<Product> GetAll() { /* Implementation */ }
    public void Add(Product entity) { /* Implementation */ }
    public void Update(Product entity) { /* Implementation */ }
    public void Delete(int id) { /* Implementation */ }
    public IEnumerable<Product> Search(string query) { /* Implementation */ }
}
```

---

## Benefits Summary

✅ **Clear Contracts**: Each interface has a clear, focused purpose  
✅ **No Empty Implementations**: Classes only implement what they actually use  
✅ **Easier to Test**: Smaller interfaces are easier to mock  
✅ **Better Flexibility**: Mix and match interfaces as needed  
✅ **Reduced Coupling**: Clients depend only on the methods they use  

---

## Quick Rule of Thumb

**If you find yourself writing `throw new NotSupportedException()` or empty method implementations, you're probably violating ISP!**

Split that fat interface into smaller, focused interfaces instead.
