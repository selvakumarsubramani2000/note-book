# 🔄 Method Overriding in Python

> **Trainer's Note:** Method overriding means a child class provides its **own version** of a method that already exists in the parent class.

---

## 📑 Table of Contents
1. [What is Method Overriding?](#1-what-is-method-overriding)
2. [Calling the Parent's Version with `super()`](#2-calling-the-parents-version-with-super)
3. [Method Overloading (Python's Way)](#3-method-overloading-pythons-way)
4. [Polymorphism in Action](#4-polymorphism-in-action)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is Method Overriding?

### Real-world analogy
```
Parent class Animal has a generic makeSound() -> "Some sound"
Child class Dog overrides makeSound() -> "Woof!"
Child class Cat overrides makeSound() -> "Meow!"
  Same method name, different behavior per class
```

```python
class Animal:
    def make_sound(self):
        print("Some generic animal sound")

class Dog(Animal):
    def make_sound(self):   # overrides parent's version
        print("Woof!")

class Cat(Animal):
    def make_sound(self):   # overrides parent's version
        print("Meow!")

Animal().make_sound()   # Some generic animal sound
Dog().make_sound()      # Woof!
Cat().make_sound()      # Meow!
```

---

## 2. Calling the Parent's Version with `super()`

Sometimes you want to **extend** the parent's behavior, not fully replace it.

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def details(self):
        print(f"Name: {self.name}, Salary: {self.salary}")

class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)   # reuse parent's __init__
        self.team_size = team_size

    def details(self):
        super().details()   # call parent's version first
        print(f"Team Size: {self.team_size}")

m = Manager("Priya", 90000, 5)
m.details()
# Name: Priya, Salary: 90000
# Team Size: 5
```

---

## 3. Method Overloading (Python's Way)

Python doesn't support traditional method overloading (same method name, different parameter lists) like Java/C#. Instead, use **default arguments** or `*args`.

```python
class Calculator:
    def add(self, a, b=0, c=0):
        return a + b + c

calc = Calculator()
print(calc.add(2))         # 2
print(calc.add(2, 3))      # 5
print(calc.add(2, 3, 4))   # 9
```

---

## 4. Polymorphism in Action

"Poly" (many) + "morph" (forms) — the same method call behaves differently depending on the object.

```python
animals = [Dog(), Cat(), Animal()]

for animal in animals:
    animal.make_sound()
# Woof!
# Meow!
# Some generic animal sound
```

This is powerful because the calling code (`animal.make_sound()`) doesn't need to know the exact type — it just works for every object that has a `make_sound()` method.

### Beginner tip
Overriding lets each subclass customize shared behavior, while `super()` lets you build on top of the parent instead of rewriting everything from scratch.

---

## 5. Knowledge Check

1. What is method overriding, and how is it different from method overloading?
2. Why would you call `super().method_name()` inside an overridden method?
3. Does Python support traditional method overloading? What's the common workaround?
4. What is polymorphism, and how does the `animals` loop example demonstrate it?

---

**Previous:** [← Inheritance](./01-Inheritance.md)
**Next:** [Access Specifiers →](./03-Access-Specifiers.md)
