# 📂 Namespaces in C#

> **Trainer's Note:** Namespaces are folders for your code names. They prevent class name clashes and keep large projects organized.

---

## 📑 Table of Contents
1. [What is a Namespace?](#1-what-is-a-namespace)
2. [Declare and Use Namespaces](#2-declare-and-use-namespaces)
3. [using Directive and Aliases](#3-using-directive-and-aliases)
4. [Nested Namespaces and Good Structure](#4-nested-namespaces-and-good-structure)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is a Namespace?

A **namespace** groups related types under a unique path-like name.

```csharp
namespace MyApp.Billing
{
    public class Invoice { }
}
```

Full name becomes: `MyApp.Billing.Invoice`.

### Real-world analogy
```
Without namespaces:
  many people named "Ravi" in one room → confusion

With namespaces:
  School.Students.Ravi
  Company.Employees.Ravi
  clear identity by context
```

---

## 2. Declare and Use Namespaces

```csharp
namespace Shop.Catalog
{
    public class Product
    {
        public string Name { get; set; }
    }
}

namespace Shop.Orders
{
    public class Order
    {
        public int Id { get; set; }
    }
}
```

### Access with full name
```csharp
Shop.Catalog.Product p = new Shop.Catalog.Product();
```

### File-scoped namespace (modern short style)
```csharp
namespace Shop.Catalog;

public class Product
{
    public string Name { get; set; }
}
```

---

## 3. using Directive and Aliases

### Import namespace
```csharp
using Shop.Catalog;
using Shop.Orders;

Product p = new Product();
Order o = new Order();
```

### Resolve same class names with alias
```csharp
using TextProduct = Shop.Catalog.Product;
using ReportProduct = Shop.Reports.Product;

TextProduct a = new TextProduct();
ReportProduct b = new ReportProduct();
```

### static using
```csharp
using static System.Math;

double result = Sqrt(25); // no Math. prefix
```

### global using (project-level modern feature)
```csharp
global using System.Collections.Generic;
// available across many files
```

---

## 4. Nested Namespaces and Good Structure

```csharp
namespace Company
{
    namespace Sales
    {
        public class Customer { }
    }
}

// same as:
namespace Company.Sales
{
    public class Customer { }
}
```

### Practical project style
```
MyApp
  MyApp.Domain
  MyApp.Application
  MyApp.Infrastructure
  MyApp.Api
```

### Why namespaces matter
| Benefit | Meaning |
|---------|---------|
| Organization | Related classes stay together |
| Avoid conflicts | Same short names in different areas |
| Clear architecture | Namespace shows layer/module |
| Easier navigation | Large solutions stay readable |

### Beginner tips
- Keep namespace matching folder structure
- Don't put all classes in global namespace
- Avoid very deep namespaces without need
- Use `using` at top; avoid repeated long full names

---

## 5. Knowledge Check

1. What problem do namespaces solve?
2. What is the full name of class `Invoice` inside `MyApp.Billing`?
3. Why do we write `using System.Collections.Generic;`?
4. When do you need a namespace alias?
5. What is a file-scoped namespace?

---

**Previous:** [← Operator Overloading](./03-Operator-Overloading.md)  
**Next:** [Preprocessor Directives →](./05-Preprocessor-Directives.md)
