# 🧬 Inheritance in Python

> **Trainer's Note:** Inheritance lets one class (child) reuse the properties and behavior of another class (parent), so you don't repeat code.

---

## 📑 Table of Contents
1. [What is Inheritance?](#1-what-is-inheritance)
2. [Single Inheritance](#2-single-inheritance)
3. [Using `super()`](#3-using-super)
4. [Multiple Inheritance](#4-multiple-inheritance)
5. [Multilevel Inheritance](#5-multilevel-inheritance)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. What is Inheritance?

### Real-world analogy
```
Parent class = "Vehicle" (general features: wheels, engine)
Child class  = "Car" inherits from Vehicle, adds its own features (trunk, AC)
  A Car IS-A Vehicle, plus extra stuff
```

---

## 2. Single Inheritance

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name} is eating")

class Dog(Animal):   # Dog inherits from Animal
    def bark(self):
        print(f"{self.name} says Woof!")

d = Dog("Rex")
d.eat()    # inherited from Animal -> Rex is eating
d.bark()   # defined in Dog -> Rex says Woof!
```

---

## 3. Using `super()`

`super()` lets a child class call the parent class's methods, especially `__init__`.

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name} is eating")

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)   # call parent's __init__
        self.breed = breed

    def bark(self):
        print(f"{self.name} ({self.breed}) says Woof!")

d = Dog("Rex", "Labrador")
d.bark()   # Rex (Labrador) says Woof!
d.eat()    # Rex is eating
```

---

## 4. Multiple Inheritance

A class can inherit from **more than one** parent class.

```python
class Flyable:
    def fly(self):
        print("I can fly!")

class Swimmable:
    def swim(self):
        print("I can swim!")

class Duck(Flyable, Swimmable):
    pass

d = Duck()
d.fly()    # I can fly!
d.swim()   # I can swim!
```

---

## 5. Multilevel Inheritance

A chain: grandparent → parent → child.

```python
class Animal:
    def eat(self):
        print("Eating...")

class Mammal(Animal):
    def walk(self):
        print("Walking...")

class Dog(Mammal):
    def bark(self):
        print("Barking...")

d = Dog()
d.eat()    # from Animal
d.walk()   # from Mammal
d.bark()   # from Dog
```

### `isinstance()` and `issubclass()`
```python
print(isinstance(d, Animal))     # True
print(issubclass(Dog, Mammal))   # True
```

### Beginner tip
Use inheritance when there's a clear **"IS-A"** relationship (a Dog IS-A Animal). If it's more of a "HAS-A" relationship (a Car HAS-A engine), prefer composition instead.

---

## 6. Knowledge Check

1. What does the `super()` function do?
2. What's the difference between single, multiple, and multilevel inheritance?
3. Write a `Cat` class that inherits from `Animal` and adds a `meow()` method.
4. When should you prefer inheritance over composition?

---

**Previous:** [← Class and Objects](./00-Class-and-Objects.md)
**Next:** [Method Overriding →](./02-Method-Overriding.md)
