# 🏷️ Class-level Decorators in Python

> **Trainer's Note:** Decorators aren't just for standalone functions — Python has built-in decorators specifically for use **inside classes** (`@staticmethod`, `@classmethod`, `@property`), and you can even decorate an entire class.

---

## 📑 Table of Contents
1. [`@staticmethod`](#1-staticmethod)
2. [`@classmethod`](#2-classmethod)
3. [`@property` Recap](#3-property-recap)
4. [Comparing Instance / Class / Static Methods](#4-comparing-instance--class--static-methods)
5. [Decorating an Entire Class](#5-decorating-an-entire-class)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. `@staticmethod`

A static method **doesn't need access** to the instance (`self`) or the class (`cls`) — it's just a regular function that happens to live inside a class, for organizational purposes.

```python
class MathUtils:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def is_even(n):
        return n % 2 == 0

print(MathUtils.add(3, 4))       # 7 -> called without creating an object
print(MathUtils.is_even(10))     # True
```

### Real-world analogy
```
@staticmethod = a public tool in a shared toolbox
  Doesn't belong to any specific object; anyone can use it directly
```

---

## 2. `@classmethod`

A class method receives the **class itself** (`cls`) instead of an instance, often used for alternative constructors.

```python
class Employee:
    company = "TechCorp"

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    @classmethod
    def from_string(cls, data_string):
        name, salary = data_string.split("-")
        return cls(name, int(salary))   # creates a new instance using cls

    @classmethod
    def change_company(cls, new_name):
        cls.company = new_name          # modifies the class attribute

e1 = Employee.from_string("Asha-50000")   # alternative constructor
print(e1.name, e1.salary)                 # Asha 50000

Employee.change_company("NewTech")
print(Employee.company)                   # NewTech
```

---

## 3. `@property` Recap

Covered in detail in the Access Specifiers guide — `@property` turns a method into something accessible like an attribute.

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return 3.14159 * self.radius ** 2

c = Circle(5)
print(c.area)   # 78.53975 -> called like an attribute, not area()
```

---

## 4. Comparing Instance / Class / Static Methods

| Type | First parameter | Can access instance data? | Can access class data? | Typical use |
|------|-----------------|----------------------------|--------------------------|-------------|
| Instance method | `self` | ✅ Yes | ✅ Yes (via `type(self)`) | Normal object behavior |
| `@classmethod` | `cls` | ❌ No | ✅ Yes | Alternative constructors, class-wide changes |
| `@staticmethod` | none | ❌ No | ❌ No | Utility functions grouped logically in a class |

```python
class Demo:
    def instance_method(self):
        print("Called on an instance:", self)

    @classmethod
    def class_method(cls):
        print("Called on the class:", cls)

    @staticmethod
    def static_method():
        print("Called with no access to instance or class")
```

---

## 5. Decorating an Entire Class

You can also write a decorator that wraps a **whole class**, not just a method.

```python
def add_greeting(cls):
    cls.greet = lambda self: print(f"Hello from {self.__class__.__name__}!")
    return cls

@add_greeting
class Robot:
    pass

r = Robot()
r.greet()   # Hello from Robot!
```

A common real-world example is Python's built-in `@dataclass`:
```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

p = Point(3, 4)
print(p)         # Point(x=3, y=4) -> __init__, __repr__ auto-generated
```

### Beginner tip
Use `@staticmethod` for helper logic that doesn't touch the object, `@classmethod` when you need the class itself (like alternative constructors), and regular instance methods for everything that works with an object's own data.

---

## 6. Knowledge Check

1. What's the key difference between `@staticmethod` and `@classmethod`?
2. Why would you use `@classmethod` to create an "alternative constructor"?
3. When would a class-level decorator (decorating the whole class) be useful?
4. Write a class `Rectangle` with a `@staticmethod` method `is_square(width, height)`.

---

**Previous:** [← Method Decorators](./00-Method-Decorators.md)

🎉 **Decorators track complete!** You've learned function decorators, `@staticmethod`, `@classmethod`, `@property`, and class-level decorators.
