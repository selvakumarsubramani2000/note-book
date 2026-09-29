# 🧩 Types of Functions in Python

> **Trainer's Note:** A function is a reusable block of code that performs a task. Instead of repeating code, you write it once and "call" it whenever needed.

---

## 📑 Table of Contents
1. [Defining a Function](#1-defining-a-function)
2. [Built-in vs User-defined Functions](#2-built-in-vs-user-defined-functions)
3. [Parameters, Arguments, and Return Values](#3-parameters-arguments-and-return-values)
4. [Default, Keyword, and Variable-length Arguments](#4-default-keyword-and-variable-length-arguments)
5. [Lambda (Anonymous) Functions](#5-lambda-anonymous-functions)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. Defining a Function

```python
def greet():
    print("Hello, welcome!")

greet()   # calling the function
```

### Real-world analogy
```
Function = a coffee machine
  define once (build the machine)
  call it (press the button) whenever you want coffee
```

---

## 2. Built-in vs User-defined Functions

| Type | Description | Example |
|------|-------------|---------|
| Built-in | Provided by Python itself | `len()`, `print()`, `sum()`, `range()` |
| User-defined | Written by you | `greet()`, `calculate_total()` |

```python
print(len("Python"))    # built-in function
print(sum([1, 2, 3]))   # built-in function

def calculate_total(price, qty):   # user-defined function
    return price * qty

print(calculate_total(10, 3))   # 30
```

---

## 3. Parameters, Arguments, and Return Values

```python
def add(a, b):        # a, b are parameters
    return a + b

result = add(5, 3)    # 5, 3 are arguments
print(result)         # 8
```

- **Parameter** — variable name in the function definition
- **Argument** — actual value passed when calling
- **`return`** — sends a value back to the caller (function stops immediately after)

```python
def is_even(n):
    return n % 2 == 0

print(is_even(4))   # True
print(is_even(7))   # False
```

### Functions without `return`
```python
def say_hi():
    print("Hi!")

result = say_hi()   # prints "Hi!"
print(result)       # None — no explicit return means None
```

---

## 4. Default, Keyword, and Variable-length Arguments

```python
# Default argument
def greet(name="Guest"):
    print(f"Hello, {name}!")

greet()          # Hello, Guest!
greet("Selva")   # Hello, Selva!

# Keyword arguments (order doesn't matter)
def describe(name, age):
    print(f"{name} is {age} years old")

describe(age=30, name="Selva")

# Variable-length positional args (*args)
def total(*numbers):
    return sum(numbers)

print(total(1, 2, 3, 4))   # 10

# Variable-length keyword args (**kwargs)
def show_info(**details):
    for key, value in details.items():
        print(f"{key}: {value}")

show_info(name="Selva", city="Chennai")
```

---

## 5. Lambda (Anonymous) Functions

A lambda is a small, one-line, unnamed function — useful for short throwaway logic.

```python
square = lambda x: x * x
print(square(5))   # 25

add = lambda a, b: a + b
print(add(3, 4))   # 7
```

### Common use: with `sorted()`, `map()`, `filter()`
```python
students = [("Selva", 85), ("Kumar", 92), ("Anu", 78)]
sorted_students = sorted(students, key=lambda s: s[1], reverse=True)
print(sorted_students)

numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x * x, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(squares)   # [1, 4, 9, 16, 25]
print(evens)     # [2, 4]
```

---

## 6. Knowledge Check

1. What is the difference between a parameter and an argument?
2. What does a function return if it has no explicit `return` statement?
3. Write a function with a default argument `greeting="Hello"`.
4. What is a lambda function, and when would you use one?

---

**Next:** [Recursion →](./01-Recursion.md)
