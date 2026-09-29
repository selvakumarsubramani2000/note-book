# 🔒 Access Specifiers in Python

> **Trainer's Note:** Python doesn't enforce strict `public`/`private` like Java or C#. Instead it uses **naming conventions** to signal how a member should be used.

---

## 📑 Table of Contents
1. [Public Members](#1-public-members)
2. [Protected Members (`_single_underscore`)](#2-protected-members-_single_underscore)
3. [Private Members (`__double_underscore`)](#3-private-members-__double_underscore)
4. [Name Mangling](#4-name-mangling)
5. [Getters/Setters with Properties](#5-getterssetters-with-properties)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. Public Members

By default, everything in Python is **public** — accessible from anywhere.

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name       # public
        self.salary = salary   # public

e = Employee("Ravi", 50000)
print(e.name, e.salary)   # accessible directly -> Ravi 50000
```

### Real-world analogy
```
Public   = the reception area of an office — anyone can walk in
Protected = staff-only areas — meant for the team, but not physically locked
Private   = the manager's safe — strongly discouraged to access from outside
```

---

## 2. Protected Members (`_single_underscore`)

A single leading underscore is a **convention** meaning "internal use — please don't touch from outside," but Python doesn't block access.

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self._salary = salary   # protected (by convention)

e = Employee("Ravi", 50000)
print(e._salary)   # still works, but considered bad practice: 50000
```

Subclasses are expected to use protected members freely:
```python
class Manager(Employee):
    def show_salary(self):
        print(f"Manager salary: {self._salary}")   # OK, accessed inside subclass
```

---

## 3. Private Members (`__double_underscore`)

A double leading underscore triggers **name mangling**, making it much harder (not impossible) to access from outside the class.

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.__salary = salary   # private

    def get_salary(self):
        return self.__salary   # accessible inside the class

e = Employee("Ravi", 50000)
print(e.get_salary())   # 50000 (through a method)

# print(e.__salary)   # ❌ AttributeError: 'Employee' object has no attribute '__salary'
```

---

## 4. Name Mangling

Python renames `__salary` to `_ClassName__salary` internally, which is why direct access fails.

```python
print(e._Employee__salary)   # 50000 -> still technically accessible (not truly private)
```

### Beginner tip
Python's philosophy: **"We are all consenting adults here."** Access control is about signaling intent, not enforcing security. Use underscores to communicate what should and shouldn't be touched.

---

## 5. Getters/Setters with Properties

The Pythonic way to control access to a private attribute is the `@property` decorator.

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.__salary = salary

    @property
    def salary(self):          # getter
        return self.__salary

    @salary.setter
    def salary(self, value):   # setter with validation
        if value < 0:
            raise ValueError("Salary cannot be negative")
        self.__salary = value

e = Employee("Ravi", 50000)
print(e.salary)     # 50000 (calls getter, looks like an attribute)
e.salary = 60000     # calls setter
print(e.salary)      # 60000
# e.salary = -100    # ❌ ValueError: Salary cannot be negative
```

---

## 6. Knowledge Check

1. What's the difference between `_protected` and `__private` naming in Python?
2. What is "name mangling," and why does it happen?
3. Why does Python not enforce true private access like Java or C#?
4. Write a class `BankAccount` with a private `__balance` attribute and a `@property` getter for it.

---

**Previous:** [← Method Overriding](./02-Method-Overriding.md)

🎉 **OOPs track complete!** You've learned classes, objects, inheritance, method overriding, polymorphism, and access specifiers.
