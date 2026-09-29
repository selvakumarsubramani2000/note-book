# 🔀 Control Statements in C#

> **Trainer's Note:** Control statements decide the path your program takes — like traffic signals and road signs for your code. Once these are clear, you can build real logic.

---

## 📑 Table of Contents
1. [Decision Making](#1-decision-making)
2. [Switch Statement](#2-switch-statement)
3. [Loops in C#](#3-loops-in-c)
4. [Jump Statements](#4-jump-statements)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Decision Making

Decision statements help your program **choose** what to do.

### Real-world analogy
```
Traffic signal:
  if RED    → stop
  else if YELLOW → slow
  else GREEN → go
```

### A) `if` statement
```csharp
int age = 20;
if (age >= 18)
{
    Console.WriteLine("You can vote");
}
```

### B) `if-else`
```csharp
if (age >= 18)
{
    Console.WriteLine("Adult");
}
else
{
    Console.WriteLine("Minor");
}
```

### C) `if-else-if` ladder
```csharp
int marks = 78;

if (marks >= 90)
    Console.WriteLine("Grade A");
else if (marks >= 75)
    Console.WriteLine("Grade B");
else if (marks >= 50)
    Console.WriteLine("Grade C");
else
    Console.WriteLine("Fail");
```

### D) Nested `if`
```csharp
bool hasTicket = true;
bool hasId = true;

if (hasTicket)
{
    if (hasId)
        Console.WriteLine("Entry allowed");
    else
        Console.WriteLine("ID required");
}
else
{
    Console.WriteLine("Buy a ticket first");
}
```

### E) Nested switch (preview — detailed next section)
You can put one `switch` inside another when you need multi-level choices (example: country → state, or category → sub-category).

**Tip:** Prefer simple `if-else-if` or separate methods if nesting becomes hard to read.

---

## 2. Switch Statement

`switch` is clean when one variable has **many fixed options**.

### Real-world analogy
```
ATM menu:
  1 → Withdraw
  2 → Deposit
  3 → Balance
  other → Invalid option
```

### Classic switch
```csharp
int day = 3;
switch (day)
{
    case 1:
        Console.WriteLine("Monday");
        break;
    case 2:
        Console.WriteLine("Tuesday");
        break;
    case 3:
        Console.WriteLine("Wednesday");
        break;
    default:
        Console.WriteLine("Invalid day");
        break;
}
```

### Grouping cases
```csharp
char grade = 'B';
switch (grade)
{
    case 'A':
    case 'B':
        Console.WriteLine("Good job");
        break;
    case 'C':
        Console.WriteLine("Average");
        break;
    default:
        Console.WriteLine("Need improvement");
        break;
}
```

### Modern switch expression (C# 8+)
```csharp
string result = day switch
{
    1 => "Monday",
    2 => "Tuesday",
    3 => "Wednesday",
    _ => "Invalid"
};
```

### Nested switch example
```csharp
string category = "Food";
string item = "Pizza";

switch (category)
{
    case "Food":
        switch (item)
        {
            case "Pizza":
                Console.WriteLine("Price: 299");
                break;
            case "Burger":
                Console.WriteLine("Price: 149");
                break;
            default:
                Console.WriteLine("Food item not found");
                break;
        }
        break;

    case "Drink":
        Console.WriteLine("Drink section");
        break;
}
```

### When to use what?
| Use `if-else` when | Use `switch` when |
|--------------------|-------------------|
| Ranges (`marks > 80`) | Exact values (`day == 1`) |
| Complex conditions | Menu-like options |
| Boolean checks | Many constant cases |

---

## 3. Loops in C#

A **loop** repeats work until a condition ends.

### Real-world analogy
```
Washing 10 plates:
  pick plate → wash → next plate
  repeat until all 10 are done
```

### A) `for` loop — know the count
```csharp
for (int i = 1; i <= 5; i++)
{
    Console.WriteLine($"Count: {i}");
}
```

Parts of `for`:
1. start → `int i = 1`
2. condition → `i <= 5`
3. update → `i++`

### B) `while` loop — repeat while condition is true
```csharp
int stock = 3;
while (stock > 0)
{
    Console.WriteLine("Item sold");
    stock--;
}
```

### C) `do-while` — run at least once
```csharp
int pin;
do
{
    Console.Write("Enter 4-digit PIN: ");
    pin = int.Parse(Console.ReadLine());
}
while (pin != 1234);

Console.WriteLine("Access granted");
```

### D) `foreach` — walk through a collection
```csharp
string[] vendors = { "A1 Traders", "Best Supplies", "Quick Mart" };

foreach (string vendor in vendors)
{
    Console.WriteLine(vendor);
}
```

### Loop choice cheat-sheet
| Loop | Best for |
|------|----------|
| `for` | Fixed number of times |
| `while` | Unknown count, check first |
| `do-while` | Must run once (menu, PIN) |
| `foreach` | Arrays / lists / collections |

---

## 4. Jump Statements

Jump statements **change the flow immediately**.

### A) `break` — exit loop/switch now
```csharp
for (int i = 1; i <= 10; i++)
{
    if (i == 5)
        break;          // stop completely when i is 5
    Console.WriteLine(i);
}
// prints 1 2 3 4
```

### B) `continue` — skip current round, go next
```csharp
for (int i = 1; i <= 5; i++)
{
    if (i == 3)
        continue;       // skip printing 3
    Console.WriteLine(i);
}
// prints 1 2 4 5
```

### C) `goto` — jump to a label (avoid in normal code)
```csharp
int n = 1;
start:
Console.WriteLine(n);
n++;
if (n <= 3)
    goto start;
```
> **Trainer tip:** `goto` makes code hard to follow. Prefer loops/`return` instead. Know it for exams/interviews, rarely use it in real projects.

### D) `return` — exit the method immediately
```csharp
int GetDiscount(int amount)
{
    if (amount <= 0)
        return 0;           // leave method early

    return amount / 10;
}
```

### E) `throw` — raise an error on purpose
```csharp
int Divide(int a, int b)
{
    if (b == 0)
        throw new DivideByZeroException("Cannot divide by zero");

    return a / b;
}
```

### Real-world picture
```
break     = emergency exit from building
continue  = skip this room, check next room
return    = leave the office and go home
throw     = raise a fire alarm (something is wrong)
goto      = teleport (confusing in big buildings)
```

### Mini comparison
| Keyword | Effect |
|---------|--------|
| `break` | Leave loop/switch |
| `continue` | Skip to next iteration |
| `return` | Leave method |
| `throw` | Start exception flow |
| `goto` | Jump to label (use carefully) |

---

## 5. Knowledge Check

1. Write an `if-else-if` that prints ticket price by age: child/adult/senior.
2. When is `switch` better than many `if-else` checks?
3. What is the difference between `while` and `do-while`?
4. What does `continue` do inside a loop?
5. Why should we avoid `goto` in normal project code?
6. Write a `for` loop that prints only even numbers from 1 to 10.
7. What happens when code executes `throw new Exception("error")`?

---

**Previous:** [← C# Fundamentals](./01-CSharp-Fundamentals.md)  
**Next:** [OOP Concepts →](./03-OOP-Concepts.md)
