# 🛡️ Exception Handling in C#

> **Trainer's Note:** Exceptions are unexpected runtime errors. Good handling keeps apps stable and shows clear messages instead of sudden crashes.

---

## 📑 Table of Contents
1. [What is an Exception?](#1-what-is-an-exception)
2. [try / catch / finally](#2-try--catch--finally)
3. [Common Exception Types](#3-common-exception-types)
4. [Best Practices](#4-best-practices)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is an Exception?

An **exception** is an error event that disrupts normal flow.

```csharp
int x = 10;
int y = 0;
int z = x / y; // DivideByZeroException
```

### Real-world analogy
```
Normal code = driving on road
Exception   = sudden roadblock
try/catch   = emergency diversion plan
finally     = always lock the car before leaving
```

Base type: `System.Exception`

---

## 2. try / catch / finally

```csharp
try
{
    Console.WriteLine("Open file / do work");
    int result = 10 / int.Parse("0");
}
catch (DivideByZeroException ex)
{
    Console.WriteLine($"Math error: {ex.Message}");
}
catch (FormatException ex)
{
    Console.WriteLine($"Invalid number: {ex.Message}");
}
catch (Exception ex)
{
    Console.WriteLine($"Something failed: {ex.Message}");
}
finally
{
    Console.WriteLine("Cleanup always runs");
}
```

### What each block does
| Block | Meaning |
|-------|---------|
| `try` | Risky code |
| `catch` | Handle specific/general errors |
| `finally` | Always runs (cleanup) |
| `throw` | Raise/rethrow exception |

### throw and rethrow
```csharp
catch (Exception ex)
{
    // log here
    throw;          // preserve stack trace
    // throw ex;    // resets stack trace (usually avoid)
}
```

### when filter (advanced beginner)
```csharp
catch (Exception ex) when (ex.Message.Contains("timeout"))
{
    Console.WriteLine("Retry later");
}
```

---

## 3. Common Exception Types

| Exception | Typical cause |
|-----------|---------------|
| `NullReferenceException` | Used null object |
| `ArgumentNullException` | Required arg is null |
| `ArgumentException` | Invalid argument |
| `FormatException` | Bad parse format |
| `IndexOutOfRangeException` | Bad array index |
| `InvalidOperationException` | Operation not valid in current state |
| `FileNotFoundException` | File missing |
| `IOException` | Input/output failure |
| `DivideByZeroException` | Divide by zero |

```csharp
string? name = null;
// Console.WriteLine(name.Length); // NullReferenceException
```

---

## 4. Best Practices

1. Catch **specific** exceptions first, general last  
2. Don't catch and ignore silently  
3. Use `finally` or `using` for cleanup  
4. Throw meaningful exceptions with clear messages  
5. Validate inputs early  
6. Log details for developers, show friendly text to users  

```csharp
public int ParseAge(string input)
{
    if (string.IsNullOrWhiteSpace(input))
        throw new ArgumentException("Age is required");

    if (!int.TryParse(input, out int age))
        throw new FormatException("Age must be a number");

    if (age < 0 || age > 120)
        throw new ArgumentOutOfRangeException(nameof(input), "Age out of range");

    return age;
}
```

### Beginner rule of thumb
```
Expected normal branch (valid/invalid user input) → if checks / TryParse
Unexpected failure (file missing mid-process)     → exceptions
```

---

## 5. Knowledge Check

1. What is an exception in simple words?
2. Difference between `catch` and `finally`?
3. Why catch specific exceptions before `Exception`?
4. Why is `throw;` preferred over `throw ex;` when rethrowing?
5. Name 4 common exception types.

---

**Previous:** [← Regular Expressions](./06-Regular-Expressions.md)  
**Next:** [Custom Exceptions →](./08-Custom-Exceptions.md)
