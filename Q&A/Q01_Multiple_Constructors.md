# Question 1: Can a class have multiple constructors? Explain with an example.

## Answer

### Understanding Constructor Overloading

Yes, absolutely! A class can have multiple constructors - this is called **Constructor Overloading**. Think of it like having different ways to create the same object, depending on what information you have available.

### Why Do We Need Multiple Constructors?

Imagine you're creating a `Student` class. Sometimes you might:
- Have all the student's information (name, age, grade)
- Have only the student's name
- Want to create a student with default values

Multiple constructors give you flexibility in how you create objects.

### Detailed Example

```csharp
public class Student
{
    public string Name { get; set; }
    public int Age { get; set; }
    public string Grade { get; set; }
    
    // Constructor 1: Default constructor (no parameters)
    public Student()
    {
        Name = "Unknown";
        Age = 0;
        Grade = "Not Assigned";
        Console.WriteLine("Default constructor called");
    }
    
    // Constructor 2: Constructor with only name
    public Student(string name)
    {
        Name = name;
        Age = 0;
        Grade = "Not Assigned";
        Console.WriteLine($"Constructor with name called for {name}");
    }
    
    // Constructor 3: Constructor with name and age
    public Student(string name, int age)
    {
        Name = name;
        Age = age;
        Grade = "Not Assigned";
        Console.WriteLine($"Constructor with name and age called for {name}");
    }
    
    // Constructor 4: Constructor with all parameters
    public Student(string name, int age, string grade)
    {
        Name = name;
        Age = age;
        Grade = grade;
        Console.WriteLine($"Full constructor called for {name}");
    }
    
    public void DisplayInfo()
    {
        Console.WriteLine($"Name: {Name}, Age: {Age}, Grade: {Grade}");
    }
}

// Usage:
class Program
{
    static void Main()
    {
        // Using different constructors
        Student student1 = new Student();                          // Default constructor
        Student student2 = new Student("Alice");                   // Name only
        Student student3 = new Student("Bob", 15);                 // Name and age
        Student student4 = new Student("Charlie", 16, "A");        // All parameters
        
        student1.DisplayInfo();
        student2.DisplayInfo();
        student3.DisplayInfo();
        student4.DisplayInfo();
    }
}
```

### Constructor Chaining (Advanced Concept)

You can also make constructors call each other using the `this` keyword to avoid code duplication:

```csharp
public class Student
{
    public string Name { get; set; }
    public int Age { get; set; }
    public string Grade { get; set; }
    
    // Main constructor with all logic
    public Student(string name, int age, string grade)
    {
        Name = name;
        Age = age;
        Grade = grade;
    }
    
    // This constructor calls the main constructor
    public Student(string name, int age) : this(name, age, "Not Assigned")
    {
    }
    
    // This constructor also calls the main constructor
    public Student(string name) : this(name, 0, "Not Assigned")
    {
    }
    
    // Default constructor
    public Student() : this("Unknown", 0, "Not Assigned")
    {
    }
}
```

### Key Rules to Remember

1. **Different Signatures**: Each constructor must have a different parameter list (different number or types of parameters)
2. **Same Name**: All constructors have the same name as the class
3. **No Return Type**: Constructors don't have a return type (not even `void`)
4. **Automatic Selection**: C# automatically chooses the right constructor based on the arguments you provide

### Real-World Example: API DTO Class

```csharp
public class ApiResponse
{
    public bool Success { get; set; }
    public string Message { get; set; }
    public object Data { get; set; }
    
    // Success response with data
    public ApiResponse(object data)
    {
        Success = true;
        Message = "Operation successful";
        Data = data;
    }
    
    // Error response
    public ApiResponse(string errorMessage)
    {
        Success = false;
        Message = errorMessage;
        Data = null;
    }
    
    // Custom response
    public ApiResponse(bool success, string message, object data)
    {
        Success = success;
        Message = message;
        Data = data;
    }
}
```

This flexibility makes your code more user-friendly and easier to maintain!
