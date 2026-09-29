# 🏷️ Identifiers in Python

> **Trainer's Note:** An identifier is the name you give to a variable, function, class, or module. Good identifier names make code self-explanatory.

---

## 📑 Table of Contents
1. [What is an Identifier?](#1-what-is-an-identifier)
2. [Rules for Identifiers](#2-rules-for-identifiers)
3. [Naming Conventions (PEP 8)](#3-naming-conventions-pep-8)
4. [Valid vs Invalid Examples](#4-valid-vs-invalid-examples)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is an Identifier?

An **identifier** is the name used to identify a variable, function, class, module, or other object.

```python
student_name = "Anu"     # student_name is an identifier
def calculate_total():   # calculate_total is an identifier
    pass
class Student:           # Student is an identifier
    pass
```

### Real-world analogy
```
Identifier = a nameplate on a door
  "Manager's Office" tells you what's inside
  "student_name" tells you what the variable holds
```

---

## 2. Rules for Identifiers

| Rule | Example |
|------|---------|
| Can contain letters, digits, underscore | `total_1`, `_value` |
| Must start with a letter or underscore | ✅ `_temp`, `age` |
| Cannot start with a digit | ❌ `1age` |
| Cannot contain spaces or special symbols | ❌ `my var`, `price$` |
| Cannot be a Python keyword | ❌ `def = 5` |
| Case-sensitive | `Age` ≠ `age` |
| No length limit (but keep it reasonable) | `student_first_name` |

---

## 3. Naming Conventions (PEP 8)

| Element | Convention | Example |
|---------|-----------|---------|
| Variables | snake_case | `total_price` |
| Functions | snake_case | `calculate_total()` |
| Classes | PascalCase | `class BankAccount:` |
| Constants | UPPER_CASE | `MAX_LIMIT = 100` |
| Private (convention) | leading underscore | `_internal_value` |
| "Really private" (name mangling) | double leading underscore | `__secret` |

### Examples
```python
MAX_RETRIES = 3          # constant

class OrderService:      # class name
    def process_order(self):  # method name
        order_total = 0        # variable name
        return order_total
```

---

## 4. Valid vs Invalid Examples

```python
# ✅ Valid
name = "Selva"
_age = 25
total_1 = 100
MAX_VALUE = 999

# ❌ Invalid
1name = "Selva"     # starts with digit
user-name = "Anu"   # hyphen not allowed
class = "A"         # keyword used as identifier
my var = 10         # space not allowed
```

### Beginner tip
Choose descriptive names over short cryptic ones:
```python
# Poor
x = 25

# Better
student_age = 25
```

---

## 5. Knowledge Check

1. Can an identifier start with a digit?
2. What naming convention is recommended for Python class names?
3. Is `total-price` a valid identifier? Why or why not?
4. What is the naming convention typically used for constants?

---

**Previous:** [← Data Types](./02-Data-Types.md)

🎉 **Variables and Data Types track complete!** You now understand variables, keywords, data types, and identifiers in Python.
