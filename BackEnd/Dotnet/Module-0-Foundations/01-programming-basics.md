# 💻 Programming Basics — Your First Steps

> **Trainer's Note:** Before you become a .NET backend developer, you need solid programming foundations. Think of this as learning the alphabet before writing stories. No jargon walls — plain words, clear pictures, and small code you can try yourself.

---

## 📑 Table of Contents
1. [What is Programming?](#1-what-is-programming)
2. [How a Computer Thinks](#2-how-a-computer-thinks)
3. [Variables and Data Types](#3-variables-and-data-types)
4. [Operators](#4-operators)
5. [Input and Output](#5-input-and-output)
6. [Control Flow — Decisions](#6-control-flow--decisions)
7. [Loops — Repeating Work](#7-loops--repeating-work)
8. [Functions / Methods](#8-functions--methods)
9. [Collections — Holding Many Values](#9-collections--holding-many-values)
10. [Errors and Debugging Mindset](#10-errors-and-debugging-mindset)
11. [How This Connects to .NET Backend](#11-how-this-connects-to-net-backend)
12. [Knowledge Check](#12-knowledge-check)

---

## 1. What is Programming?

**Programming** means giving a computer **clear, step-by-step instructions** so it can solve a problem or do a job.

```
Real life:
  Recipe to cook rice  →  steps a human follows

Programming:
  Recipe in code       →  steps a computer follows
```

| Term | Simple meaning |
|------|----------------|
| **Program / Application** | A finished set of instructions (the app) |
| **Code** | The text you write in a language computers understand (with help) |
| **Programming language** | Rules + vocabulary to write those instructions (C#, Python, Java…) |
| **Algorithm** | The plan / logic before (or behind) the code |
| **Bug** | A mistake that makes the program behave wrong |

### Why C# and .NET?
- C# is a modern, readable language from Microsoft
- .NET is the platform that **runs** C# and gives you ready-made tools (web, database, security)
- Together they are a top choice for **backend APIs**, enterprise systems, and cloud apps

---

## 2. How a Computer Thinks

A computer is **extremely fast** and **extremely literal**. It only does what you tell it — nothing more, nothing less.

```
┌─────────────────────────────────────────┐
│  1. Input   → data coming in            │
│  2. Process → logic / calculations      │
│  3. Output  → result going out          │
└─────────────────────────────────────────┘
```

**Backend mindset (early):**
- A user (or another system) sends a **request**
- Your code **processes** it (validate, save, calculate)
- You send a **response** back

You will see this pattern again in HTTP and APIs.

---

## 3. Variables and Data Types

A **variable** is a named box that holds a value.

```csharp
string name = "Selva";   // text
int age = 28;            // whole number
decimal price = 99.50m;  // money-friendly decimal
bool isActive = true;    // true or false
```

### Common data types (C#)

| Type | Holds | Example |
|------|-------|---------|
| `string` | Text | `"Hello"` |
| `int` | Whole numbers | `42` |
| `long` | Bigger whole numbers | `9_000_000_000` |
| `double` | Decimal numbers | `3.14` |
| `decimal` | Precise decimals (money) | `19.99m` |
| `bool` | True / False | `true` |
| `DateTime` | Date and time | `DateTime.Now` |
| `char` | Single character | `'A'` |

### Rules beginners must remember
1. **Name clearly** — `userEmail` is better than `x`
2. **Type matters** — you cannot put text into an `int` without converting
3. **Value can change** (unless you make it `const` or `readonly`)

```csharp
const double TaxRate = 0.18;  // cannot change later
int quantity = 2;
quantity = 3;                 // allowed
```

### Null — “no value”
Sometimes a variable has **nothing** inside. That is `null` (for reference types).

```csharp
string? nickname = null;  // no nickname yet
```

As a backend developer you will check for null often (missing data, optional fields).

---

## 4. Operators

Operators let you **calculate** and **compare**.

### Arithmetic
```csharp
int a = 10;
int b = 3;

int sum = a + b;      // 13
int diff = a - b;     // 7
int product = a * b;  // 30
int quotient = a / b; // 3  (integer division)
int remainder = a % b;// 1
```

### Comparison (result is `bool`)
```csharp
a == b  // equal?
a != b  // not equal?
a > b   // greater?
a >= b  // greater or equal?
a < b
a <= b
```

### Logical
```csharp
bool isAdult = age >= 18;
bool hasId = true;

bool canEnter = isAdult && hasId;  // AND — both must be true
bool canTry = isAdult || hasId;    // OR  — at least one true
bool blocked = !canEnter;          // NOT — reverse true/false
```

### Assignment shortcuts
```csharp
int score = 10;
score += 5;  // score = score + 5 → 15
score++;     // score = score + 1 → 16
```

---

## 5. Input and Output

### Output (show something)
```csharp
Console.WriteLine("Welcome to backend learning!");
Console.WriteLine($"Hello, {name}. You are {age} years old.");
```

`$"..."` is **string interpolation** — easy way to mix text and variables.

### Input (read something)
```csharp
Console.Write("Enter your name: ");
string? input = Console.ReadLine();
```

> Backend note: In real APIs, “input” is usually **HTTP request data** (URL, headers, JSON body), not the console. Console is perfect for learning and small tools.

---

## 6. Control Flow — Decisions

Programs make decisions with `if`, `else if`, `else`, and `switch`.

### if / else
```csharp
int temperature = 36;

if (temperature >= 38)
{
    Console.WriteLine("Fever — see a doctor");
}
else if (temperature >= 37)
{
    Console.WriteLine("Slightly high — rest and monitor");
}
else
{
    Console.WriteLine("Normal range");
}
```

### switch (many clear cases)
```csharp
string role = "Admin";

switch (role)
{
    case "Admin":
        Console.WriteLine("Full access");
        break;
    case "Editor":
        Console.WriteLine("Can edit content");
        break;
    case "Viewer":
        Console.WriteLine("Read-only");
        break;
    default:
        Console.WriteLine("Unknown role");
        break;
}
```

### Modern switch expression
```csharp
string message = role switch
{
    "Admin"  => "Full access",
    "Editor" => "Can edit content",
    "Viewer" => "Read-only",
    _        => "Unknown role"
};
```

**Backend habit:** Validate early.
```csharp
if (string.IsNullOrWhiteSpace(email))
{
    // reject request — bad input
}
```

---

## 7. Loops — Repeating Work

Use loops when you need to do something **many times**.

### for — you know how many times
```csharp
for (int i = 1; i <= 5; i++)
{
    Console.WriteLine($"Step {i}");
}
```

### while — repeat while condition is true
```csharp
int retries = 3;
while (retries > 0)
{
    Console.WriteLine("Trying...");
    retries--;
}
```

### foreach — go through each item in a collection
```csharp
string[] cities = { "Chennai", "Bengaluru", "Hyderabad" };

foreach (string city in cities)
{
    Console.WriteLine(city);
}
```

| Loop | Best when |
|------|-----------|
| `for` | Counting / index matters |
| `while` | Stop condition is dynamic |
| `foreach` | Visiting every item in a list/array |

**Watch out:** Infinite loops never stop (condition never becomes false). Always ensure progress toward the end.

---

## 8. Functions / Methods

A **method** is a reusable block of code with a name.

```
Why methods?
  - Avoid copy-paste
  - Name your intent (CalculateTotal, ValidateEmail)
  - Test smaller pieces
```

### Anatomy
```csharp
// returnType Name(parameters)
int Add(int x, int y)
{
    return x + y;
}

int total = Add(10, 5);  // 15
```

### void — no return value
```csharp
void Greet(string name)
{
    Console.WriteLine($"Hello, {name}");
}
```

### Parameters vs arguments
- **Parameter** = placeholder in the definition (`name`)
- **Argument** = actual value you pass (`"Selva"`)

### Why this matters in backend
Your API will be full of methods like:
- `CreateOrder(...)`
- `GetUserById(...)`
- `CalculateShipping(...)`

Small, clear methods = readable backend code.

---

## 9. Collections — Holding Many Values

One variable holds one value. Collections hold **many**.

### Array — fixed size
```csharp
int[] marks = { 80, 90, 75 };
Console.WriteLine(marks[0]);  // 80 (index starts at 0)
```

### List — grows as needed (very common)
```csharp
List<string> skills = new List<string>();
skills.Add("C#");
skills.Add("SQL");
skills.Add("HTTP");

Console.WriteLine(skills.Count);  // 3
```

### Dictionary — key → value map
```csharp
Dictionary<string, int> ages = new Dictionary<string, int>
{
    ["Selva"] = 28,
    ["Asha"] = 31
};

Console.WriteLine(ages["Selva"]);  // 28
```

| Collection | Use when |
|------------|----------|
| Array | Fixed number of items |
| `List<T>` | Growing list of items |
| `Dictionary<TKey,TValue>` | Lookup by key (id → object, code → name) |

---

## 10. Errors and Debugging Mindset

Errors are normal. Professionals expect them and handle them calmly.

### Compile-time vs runtime
| Kind | When it appears | Example |
|------|-----------------|---------|
| **Compile-time** | Before the app runs | Typo, wrong type |
| **Runtime** | While app is running | Divide by zero, null reference, file missing |

### try / catch (basic safety net)
```csharp
try
{
    int number = int.Parse("abc");  // will fail
}
catch (FormatException ex)
{
    Console.WriteLine($"Invalid number: {ex.Message}");
}
```

### Beginner debugging checklist
1. Read the error message slowly
2. Find the **line number**
3. Check assumptions (is this null? is this empty? is this 0?)
4. Print / log intermediate values
5. Fix one thing, then retest

> Backend truth: Good logs and clear error messages save hours in production.

---

## 11. How This Connects to .NET Backend

Everything in this file shows up again in real backend work:

| Basics | Backend form |
|--------|--------------|
| Variables & types | Request models, database fields |
| if / validation | Reject bad input early |
| loops | Process lists of orders, users, messages |
| methods | Controllers, services, repositories |
| collections | JSON arrays, query results |
| errors | HTTP 400/500 responses, exception handling |

```
Browser / Mobile App
        │  HTTP request (JSON)
        ▼
   Your .NET API  ← you write logic here
        │
        ▼
   Database / other services
```

Next foundation topics:
- **OOP** → how to structure bigger code
- **Web basics** → how HTTP and APIs talk

---

## 12. Knowledge Check

**Q1.** What is a variable in one sentence?  
**Q2.** Which type is best for money values in C# — `double` or `decimal`?  
**Q3.** What does `&&` mean?  
**Q4.** When do you prefer `foreach` over `for`?  
**Q5.** Why do we write methods instead of one long script?  
**Q6.** What is the difference between a compile-time error and a runtime error?

### Mini practice
Write a tiny console program that:
1. Stores a product name (`string`) and price (`decimal`)
2. Asks for quantity
3. Calculates total (`price * quantity`)
4. If total > 1000, prints `"Eligible for discount"`
5. Else prints `"No discount"`

### Answers (short)
1. A named container that stores a value  
2. `decimal` (better precision for money)  
3. Logical AND — both sides must be true  
4. When you need every item and do not care much about index  
5. Reuse, clarity, easier testing and maintenance  
6. Compile-time = before run (syntax/types); runtime = while running

---

## ✅ What You Should Feel Confident About

- [ ] Explain programming in plain words  
- [ ] Declare variables with correct types  
- [ ] Use if/else and loops  
- [ ] Write a simple method with parameters and return value  
- [ ] Use `List<T>` for a growing collection  
- [ ] Stay calm when reading error messages  

**Next:** [02-oop-concepts.md](./02-oop-concepts.md) — structure your code like real-world objects.
