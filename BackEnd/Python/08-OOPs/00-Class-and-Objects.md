# 🏛️ Classes and Objects in Python

> **Trainer's Note:** A **class** is a blueprint. An **object** is a real thing built from that blueprint. One blueprint (class) can create many houses (objects).

---

## 📑 Table of Contents
1. [What is a Class?](#1-what-is-a-class)
2. [Creating Objects](#2-creating-objects)
3. [The `__init__` Constructor](#3-the-__init__-constructor)
4. [Instance vs Class Attributes](#4-instance-vs-class-attributes)
5. [Methods](#5-methods)
6. [The `self` Keyword](#6-the-self-keyword)
7. [Knowledge Check](#7-knowledge-check)

---

## 1. What is a Class?

```python
class Car:
    pass   # empty class for now
```

### Real-world analogy
```
Class  = blueprint of a car (design on paper)
Object = the actual car built from that blueprint
  You can build many cars (objects) from one blueprint (class)
```

---

## 2. Creating Objects

```python
class Car:
    pass

car1 = Car()   # object 1
car2 = Car()   # object 2

print(type(car1))   # <class '__main__.Car'>
print(car1 is car2) # False -> two separate objects
```

---

## 3. The `__init__` Constructor

`__init__` runs automatically when an object is created — it's used to set up initial data.

```python
class Car:
    def __init__(self, brand, color):
        self.brand = brand
        self.color = color

car1 = Car("Toyota", "Red")
car2 = Car("Honda", "Blue")

print(car1.brand, car1.color)   # Toyota Red
print(car2.brand, car2.color)   # Honda Blue
```

---

## 4. Instance vs Class Attributes

```python
class Car:
    wheels = 4   # class attribute -> shared by all objects

    def __init__(self, brand):
        self.brand = brand   # instance attribute -> unique per object

car1 = Car("Toyota")
car2 = Car("Honda")

print(car1.wheels, car2.wheels)   # 4 4  (shared)
print(car1.brand, car2.brand)     # Toyota Honda (unique)

Car.wheels = 6         # change at class level
print(car1.wheels)     # 6 (affects all objects, unless overridden)
```

---

## 5. Methods

Methods are functions defined inside a class that describe what an object **can do**.

```python
class Car:
    def __init__(self, brand):
        self.brand = brand

    def drive(self):
        print(f"{self.brand} is driving!")

    def honk(self):
        print("Beep beep!")

car1 = Car("Toyota")
car1.drive()   # Toyota is driving!
car1.honk()    # Beep beep!
```

---

## 6. The `self` Keyword

- `self` refers to the **current object** calling the method.
- It's always the **first parameter** of instance methods, but you don't pass it manually — Python does it automatically.

```python
class Person:
    def __init__(self, name):
        self.name = name   # self.name belongs to THIS object

    def greet(self):
        print(f"Hi, I'm {self.name}")

p1 = Person("Asha")
p2 = Person("Ravi")

p1.greet()   # Hi, I'm Asha
p2.greet()   # Hi, I'm Ravi
```

### Beginner tip
Think of `self` as saying "this particular object's" — `self.name` means "this object's name."

---

## 7. Knowledge Check

1. What is the difference between a class and an object?
2. What does the `__init__` method do?
3. What is the difference between an instance attribute and a class attribute?
4. Why do instance methods need `self` as their first parameter?

---

**Next:** [Inheritance →](./01-Inheritance.md)
