# 📦 Function Arguments: Packing & Unpacking

> **Trainer's Note:** Python lets a function accept *any number* of arguments using `*args` and `**kwargs` ("packing"), and lets you spread a list/dict into a function call using the same `*`/`**` symbols ("unpacking").

---

## 📑 Table of Contents
1. [Recap: Types of Arguments](#1-recap-types-of-arguments)
2. [Packing with `*args`](#2-packing-with-args)
3. [Packing with `**kwargs`](#3-packing-with-kwargs)
4. [Unpacking Arguments with `*` and `**`](#4-unpacking-arguments-with--and-)
5. [Combining Everything](#5-combining-everything)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. Recap: Types of Arguments

Python functions can accept arguments in a few ways: positional, default, keyword, and variable-length (`*args`, `**kwargs`). This guide focuses on the **variable-length** and **unpacking** side in more depth.

### Real-world analogy
```
*args   = a bag you can drop any number of loose items into
**kwargs = a labeled toolbox where every item has a name tag (key: value)
```

---

## 2. Packing with `*args`

`*args` collects any number of **positional** arguments into a **tuple**.

```python
def add_all(*numbers):
    print(numbers, type(numbers))   # it's a tuple
    return sum(numbers)

print(add_all(1, 2, 3))       # (1, 2, 3) <class 'tuple'>  -> 6
print(add_all(5, 10, 15, 20)) # works with any number of arguments
```

- `args` is just a name (convention) — the `*` is what matters.
- You can mix normal parameters with `*args`, but `*args` must come after them.

```python
def describe(name, *hobbies):
    print(f"{name}'s hobbies: {hobbies}")

describe("Asha", "reading", "chess", "cycling")
```

---

## 3. Packing with `**kwargs`

`**kwargs` collects any number of **keyword** arguments into a **dictionary**.

```python
def print_profile(**details):
    print(details, type(details))   # it's a dict
    for key, value in details.items():
        print(f"{key}: {value}")

print_profile(name="Ravi", age=25, city="Chennai")
```

**Output:**
```
{'name': 'Ravi', 'age': 25, 'city': 'Chennai'} <class 'dict'>
name: Ravi
age: 25
city: Chennai
```

### Order rule when combining
```python
def combo(a, b, *args, **kwargs):
    print(a, b, args, kwargs)

combo(1, 2, 3, 4, x=10, y=20)
# 1 2 (3, 4) {'x': 10, 'y': 20}
```
Parameter order must be: **normal → `*args` → keyword-only → `**kwargs`**

---

## 4. Unpacking Arguments with `*` and `**`

Packing gathers values *into* a function. **Unpacking** does the opposite — it spreads a list/tuple/dict *out* when **calling** a function.

### Unpacking a list/tuple with `*`
```python
def add(a, b, c):
    return a + b + c

numbers = [1, 2, 3]
print(add(*numbers))   # same as add(1, 2, 3) -> 6
```

### Unpacking a dictionary with `**`
```python
def greet(name, greeting):
    print(f"{greeting}, {name}!")

data = {"name": "Meena", "greeting": "Hi"}
greet(**data)   # same as greet(name="Meena", greeting="Hi")
```

### Unpacking inside collections
```python
first = [1, 2, 3]
second = [4, 5]
combined = [*first, *second]   # [1, 2, 3, 4, 5]

defaults = {"theme": "dark"}
overrides = {"font_size": 14}
settings = {**defaults, **overrides}   # {'theme': 'dark', 'font_size': 14}
```

---

## 5. Combining Everything

```python
def order_summary(customer, *items, **extras):
    print(f"Customer: {customer}")
    print(f"Items: {items}")
    print(f"Extras: {extras}")

cart = ["Book", "Pen"]
info = {"discount": "10%", "delivery": "Express"}

order_summary("Kiran", *cart, **info)
# Customer: Kiran
# Items: ('Book', 'Pen')
# Extras: {'discount': '10%', 'delivery': 'Express'}
```

### Beginner tip
- Use `*args`/`**kwargs` when you don't know in advance how many arguments a function should accept (e.g., wrapper functions, logging utilities).
- Use unpacking (`*`, `**`) when you already have data in a list/dict and want to "spread" it into a function call.

---

## 6. Knowledge Check

1. What data type does `*args` collect its values into inside a function?
2. What data type does `**kwargs` collect its values into inside a function?
3. Given `values = [10, 20, 30]`, how would you pass them as three separate arguments to `func(a, b, c)`?
4. What is the correct parameter order when a function uses normal parameters, `*args`, and `**kwargs` together?

---

**Previous:** [← Recursion](./01-Recursion.md)

🎉 **Functions track complete!** You've learned function types, arguments, packing/unpacking, lambdas, and recursion — completing the Python beginner track!
