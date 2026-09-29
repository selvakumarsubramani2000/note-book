# 🧱 C# Fundamentals

> **Trainer's Note:** These are the building blocks. If variables and data types are clear, everything else in C# becomes easier. We will go slow and use everyday examples.

---

## 📑 Table of Contents
1. [C# Identifiers](#1-c-identifiers)
2. [Data Types in C#](#2-data-types-in-c)
3. [Variables in C#](#3-variables-in-c)
4. [Constants & Literals](#4-constants--literals)
5. [Operators in C#](#5-operators-in-c)
6. [C# Keywords (All Important Groups)](#6-c-keywords-all-important-groups)
7. [Knowledge Check](#7-knowledge-check)

---

## 1. C# Identifiers

An **identifier** is the **name** you give to a variable, method, class, or anything in code.

```csharp
int age = 25;           // "age" is an identifier
string customerName;    // "customerName" is an identifier
void PrintBill() { }    // "PrintBill" is an identifier
```

### Naming rules
| Rule | Example |
|------|---------|
| Can use letters, digits, underscore | `total_Amount`, `item2` |
| Must **not** start with a digit | ❌ `2value`  ✅ `value2` |
| Cannot be a reserved keyword alone | ❌ `int`  ✅ `intValue` |
| Case-sensitive | `Name` and `name` are different |
| No spaces | ❌ `customer name`  ✅ `customerName` |

### Real-world analogy
```
Identifier = the label on a storage box
  Box labeled "Sugar"  → you know what is inside
  Box with no label    → confusion
```

### Good naming style (recommended)
```csharp
// Camel case for variables/methods
string firstName;
void calculateTotal() { }

// Pascal case for classes
class CustomerOrder { }
```

---

## 2. Data Types in C#

A **data type** tells C# **what kind of value** a box can hold.

### Two big families

```
DATA TYPES
├── Value Types   → store the actual value (int, bool, struct…)
└── Reference Types → store a reference/address (class, string, array…)
```

### Common value types
| Type | Example | Holds |
|------|---------|-------|
| `int` | `25` | Whole numbers |
| `long` | `9999999999` | Big whole numbers |
| `float` | `12.5f` | Decimal (less precise) |
| `double` | `12.55` | Decimal (more precise) |
| `decimal` | `99.99m` | Money-safe decimal |
| `char` | `'A'` | Single character |
| `bool` | `true` / `false` | Yes/No values |
| `byte` | `255` | 0 to 255 |

### Common reference types
| Type | Example | Holds |
|------|---------|-------|
| `string` | `"Hello"` | Text |
| `object` | any value boxed | Base of all types |
| `array` | `int[] nums` | List of same type |
| `class` instance | `new Customer()` | Custom object |

### Real-world picture
```
Value type     = cash in your pocket (the money itself)
Reference type = bank locker key (key points to the real money in bank)
```

```csharp
int price = 100;                 // value type
string product = "Laptop";       // reference type
bool isAvailable = true;         // value type
```

---

## 3. Variables in C#

A **variable** is a named box in memory that holds a value.

```csharp
// declaration
int quantity;

// assignment
quantity = 10;

// declaration + assignment together
int quantity = 10;
string vendorName = "ABC Traders";
```

### Rules to remember
1. Declare type before use (C# is strongly typed)
2. Give a meaningful name
3. Initialize before reading (safer)
4. One variable → one purpose

### `var` keyword (type is guessed by compiler)
```csharp
var count = 5;          // compiler knows this is int
var title = "Invoice";  // compiler knows this is string
// var x;  ❌ not allowed — must assign at declaration
```

### Real-world analogy
```
Variable = labeled jar in kitchen
  jar "salt" contains salt
  jar "sugar" contains sugar
  wrong label = bugs in cooking (and in code!)
```

---

## 4. Constants & Literals

### Constants
A **constant** is a value that **cannot change** after it is set.

```csharp
const double Pi = 3.14159;
const int MaxLoginAttempts = 3;

// Pi = 3.14;  ❌ compile error — constant cannot change
```

**When to use:** tax percentage, max size, app name, fixed config values.

### Literals
A **literal** is the **raw value written in code**.

```csharp
42          // integer literal
3.14        // double literal
3.14f       // float literal
99.99m      // decimal literal
'A'         // char literal
"Hello"     // string literal
true        // bool literal
null        // null literal
```

### Real-world analogy
```
Constant = permanent marker writing on a board (fixed)
Variable = pencil writing (can erase and rewrite)
Literal  = the actual number/text you write
```

---

## 5. Operators in C#

**Operators** are symbols that perform operations.

### 1) Arithmetic
```csharp
int a = 10, b = 3;
Console.WriteLine(a + b);  // 13
Console.WriteLine(a - b);  // 7
Console.WriteLine(a * b);  // 30
Console.WriteLine(a / b);  // 3  (integer division)
Console.WriteLine(a % b);  // 1  (remainder)
```

### 2) Relational (comparison) → result is bool
```csharp
a == b   // equal?
a != b   // not equal?
a > b    // greater?
a < b
a >= b
a <= b
```

### 3) Logical
```csharp
true && false   // AND → false
true || false   // OR  → true
!true           // NOT → false
```

### 4) Assignment
```csharp
int x = 5;
x += 2;   // x = x + 2 → 7
x -= 1;   // 6
x *= 3;   // 18
x /= 2;   // 9
```

### 5) Unary / Increment
```csharp
int n = 5;
n++;      // n becomes 6
n--;      // n becomes 5
```

### 6) Ternary (short if-else)
```csharp
string result = (age >= 18) ? "Adult" : "Minor";
```

### Real-world analogy
```
Operators = kitchen actions
  +  mix
  -  remove
  *  multiply portions
  /  split
  == check if same
```

---

## 6. C# Keywords (All Important Groups)

**Keywords** are reserved words. C# already owns their meaning. You cannot use them as normal identifiers.

### A) Value Type Keywords
`int`, `long`, `float`, `double`, `decimal`, `char`, `bool`, `byte`, `short`, `uint`, `ulong`, `sbyte`, `ushort`, `struct`, `enum`

```csharp
int age = 30;
bool isActive = true;
```

### B) Reference Type Keywords
`class`, `interface`, `delegate`, `object`, `string`, `dynamic`

```csharp
class Product { }
string name = "Tea";
```

### C) Modifier Keywords
Control access / behavior of classes and members.

| Keyword | Simple meaning |
|---------|----------------|
| `public` | Anyone can use |
| `private` | Only inside same class |
| `protected` | Class + child classes |
| `internal` | Same project/assembly |
| `static` | Belongs to type, not object |
| `readonly` | Set once (in declaration/constructor) |
| `abstract` | Incomplete, must be completed by child |
| `sealed` | Cannot be inherited |
| `virtual` | Can be overridden |
| `override` | Replaces parent virtual method |
| `const` | Compile-time constant |
| `async` | Asynchronous method |
| `partial` | Class split across files |

### D) Statement Keywords
`if`, `else`, `switch`, `case`, `default`, `for`, `foreach`, `while`, `do`, `break`, `continue`, `goto`, `return`, `throw`, `try`, `catch`, `finally`, `using`, `lock`, `checked`, `unchecked`

### E) Method Parameter Keywords
| Keyword | Meaning |
|---------|---------|
| `params` | Variable number of arguments |
| `ref` | Pass by reference (must be initialized) |
| `out` | Pass by reference (method will assign) |
| `in` | Pass by reference but read-only |

```csharp
void Add(in int a, in int b, out int sum)
{
    sum = a + b;
}
```

### F) Namespace Keywords
`namespace`, `using`, `extern`

```csharp
using System;
namespace MyShop.Billing { }
```

### G) Operator Keywords
`as`, `is`, `new`, `sizeof`, `typeof`, `stackalloc`, `nameof`

```csharp
if (obj is string s) { }
var t = typeof(int);
```

### H) Conversion Keywords
`explicit`, `implicit`, `operator`

```csharp
// used when creating custom conversion operators in advanced code
```

### I) Access Keywords
`base`, `this`

```csharp
public Student(string name) { this.name = name; } // this = current object
base.Print(); // call parent version
```

### J) Literal Keywords
`true`, `false`, `null`, `default`

```csharp
bool ok = true;
string? text = null;
int n = default; // 0
```

### Quick memory picture
```
Keywords are like reserved seats in a theater.
  Seat "if" always means decision-making.
  You cannot rename that seat for your variable.
```

---

## 7. Knowledge Check

1. What is an identifier? Give 2 valid and 1 invalid example.
2. What is the difference between value type and reference type?
3. Why do we use `const`?
4. What does the `%` operator return?
5. Name 3 modifier keywords and what they do.
6. What is the difference between `ref` and `out`?
7. Can you use `class` as a variable name? Why?

---

**Previous:** [← .NET Basics](./00-DotNet-Basics.md)  
**Next:** [Control Statements →](./02-Control-Statements.md)
