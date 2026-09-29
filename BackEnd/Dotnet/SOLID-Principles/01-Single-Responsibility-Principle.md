# 1️⃣ Single Responsibility Principle (SRP)

> **Trainer's Note:** SRP is the easiest SOLID principle to understand but the hardest to apply consistently. Let's fix that today.

---

## 📑 Table of Contents
1. [What is SRP?](#1-what-is-srp)
2. [A Real-World Analogy](#2-a-real-world-analogy)
3. [The Problem — Code Without SRP](#3-the-problem--code-without-srp)
4. [The Solution — Applying SRP](#4-the-solution--applying-srp)
5. [How to Spot SRP Violations](#5-how-to-spot-srp-violations)
6. [Common Beginner Confusions](#6-common-beginner-confusions)
7. [Knowledge Check](#7-knowledge-check)

---

## 1. What is SRP?

> **"A class should have only ONE reason to change."**

This means every class should be responsible for **one job / one part of the functionality** — not many.

**Reason to change** = a specific type of requirement that could force you to edit this class.

- If a class handles both "saving to database" and "sending email", it has **two reasons to change**:
  1. Database schema changes
  2. Email provider changes

That already breaks SRP.

---

## 2. A Real-World Analogy

### 🍽️ Think of a Restaurant

```
❌ WITHOUT SRP — One person does everything:
   The Chef also takes orders, cleans tables, and manages billing.
   If the billing software changes, the chef gets pulled away from cooking.
   If the menu changes, the same person must relearn everything.

✅ WITH SRP — Each role has ONE job:
   👨‍🍳 Chef        → cooks food
   🧑‍💼 Waiter      → takes orders
   💰 Cashier      → handles billing
   🧹 Cleaner      → cleans tables

   A change in billing software only affects the Cashier.
   A change in the menu only affects the Chef.
```

Same idea applies to classes in your code — each class should be like **one employee with one job**.

---

## 3. The Problem — Code Without SRP

```csharp
// ❌ BAD: This class has MULTIPLE responsibilities
public class Employee
{
    public string Name { get; set; }
    public decimal Salary { get; set; }

    // Responsibility 1: Business logic
    public decimal CalculateBonus()
    {
        return Salary * 0.10m;
    }

    // Responsibility 2: Database access
    public void SaveToDatabase()
    {
        var connection = new SqlConnection("connection-string");
        connection.Open();
        // ... save Employee data ...
    }

    // Responsibility 3: Report generation
    public void GeneratePayslipPdf()
    {
        // ... PDF generation logic ...
    }

    // Responsibility 4: Notification
    public void SendEmailNotification()
    {
        var smtp = new SmtpClient("smtp.server.com");
        smtp.Send("hr@company.com", Name, "Payslip Ready", "...");
    }
}
```

**Why this is bad:**
- If the database technology changes (SQL Server → MongoDB) → this class changes
- If the PDF library changes → this class changes
- If the email provider changes → this class changes
- If the bonus calculation rule changes → this class changes

**4 different reasons to change = SRP violation!** This class is doing the job of 4 different "employees."

---

## 4. The Solution — Applying SRP

Split the responsibilities into **separate, focused classes**:

```csharp
// ✅ GOOD: Each class has ONE responsibility

// Responsibility: Hold employee data + business rule
public class Employee
{
    public string Name { get; set; }
    public decimal Salary { get; set; }

    public decimal CalculateBonus() => Salary * 0.10m;
}

// Responsibility: Database access ONLY
public class EmployeeRepository
{
    public void Save(Employee employee)
    {
        var connection = new SqlConnection("connection-string");
        connection.Open();
        // ... save Employee data ...
    }
}

// Responsibility: PDF generation ONLY
public class PayslipGenerator
{
    public void GeneratePdf(Employee employee)
    {
        // ... PDF generation logic ...
    }
}

// Responsibility: Notification ONLY
public class EmailNotifier
{
    public void Send(string toEmail, string subject, string body)
    {
        var smtp = new SmtpClient("smtp.server.com");
        smtp.Send("hr@company.com", toEmail, subject, body);
    }
}
```

**Now:**
- Database logic change → only touch `EmployeeRepository`
- PDF library change → only touch `PayslipGenerator`
- Email provider change → only touch `EmailNotifier`
- Bonus rule change → only touch `Employee`

Each class can be **tested, changed, and understood independently**.

---

## 5. How to Spot SRP Violations

Ask yourself these questions about a class:

| Question | If "Yes" → Possible SRP Violation |
|----------|-------------------------------------|
| Does the class name include "And" or "Manager" (e.g. `OrderAndInvoiceManager`)? | ⚠️ Likely doing too much |
| Can I describe the class in one sentence without using "and"? | If you need "and", it's doing 2+ jobs |
| Does the class talk to a database AND send emails AND do calculations? | ⚠️ Split it up |
| Would 2 different teams (DB team, UI team) need to edit this same class? | ⚠️ Too many responsibilities |

### 💡 Quick Rule of Thumb
> "If you can only describe what a class does using the word **'AND'**, it probably breaks SRP."

Example: *"This class calculates salary **AND** saves to database **AND** sends email"* → 3 responsibilities → split it into 3 classes.

---

## 6. Common Beginner Confusions

| Confusion | Clarification |
|-----------|----------------|
| "SRP means one method per class" | ❌ No. A class can have many methods, as long as they all serve **one** responsibility |
| "SRP means one class per file" | ❌ That's a coding style, not SRP |
| "Splitting classes always improves performance" | ❌ SRP is about **maintainability**, not performance |
| "I need a new class for every tiny thing" | ❌ Don't over-split. Group things that genuinely belong together (like `Name` and `Salary` in `Employee`) |

---

## 7. Knowledge Check

1. What does "a reason to change" mean in the context of SRP?
2. Look at a class in your current project. Can you describe its job in one sentence without using "and"?
3. Why is it risky to mix database logic and business logic inside the same class?
4. Does SRP mean every class should have exactly one method? Why or why not?

---

**Previous:** [← Introduction to SOLID](./00-Introduction-to-SOLID.md)
**Next:** [Interface Segregation Principle →](./02-Interface-Segregation-Principle.md)
