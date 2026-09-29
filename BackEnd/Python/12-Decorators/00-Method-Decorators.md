# 🎁 Method (Function) Decorators in Python

> **Trainer's Note:** A decorator is a function that **wraps another function** to add extra behavior — without changing the original function's code.

---

## 📑 Table of Contents
1. [Functions are Objects](#1-functions-are-objects)
2. [Building a Simple Decorator](#2-building-a-simple-decorator)
3. [The `@` Syntax](#3-the--syntax)
4. [Decorators with Arguments (`*args`, `**kwargs`)](#4-decorators-with-arguments-args-kwargs)
5. [Decorators That Take Their Own Arguments](#5-decorators-that-take-their-own-arguments)
6. [Preserving Metadata with `functools.wraps`](#6-preserving-metadata-with-functoolswraps)
7. [Knowledge Check](#7-knowledge-check)

---

## 1. Functions are Objects

In Python, functions can be passed around like any other value — stored in variables, passed as arguments, or returned from other functions.

```python
def greet():
    print("Hello!")

say_hello = greet   # assign function to another name
say_hello()          # Hello!
```

### Real-world analogy
```
Decorator = gift wrapping
  The gift (original function) stays the same inside
  The wrapping (decorator) adds something extra around it
  (a ribbon, a card) without changing the gift itself
```

---

## 2. Building a Simple Decorator

```python
def my_decorator(func):
    def wrapper():
        print("Before the function runs")
        func()
        print("After the function runs")
    return wrapper

def say_hello():
    print("Hello!")

decorated = my_decorator(say_hello)
decorated()
# Before the function runs
# Hello!
# After the function runs
```

---

## 3. The `@` Syntax

The `@decorator_name` syntax is just shorthand for `func = decorator(func)`.

```python
def my_decorator(func):
    def wrapper():
        print("Before the function runs")
        func()
        print("After the function runs")
    return wrapper

@my_decorator          # same as: say_hello = my_decorator(say_hello)
def say_hello():
    print("Hello!")

say_hello()
# Before the function runs
# Hello!
# After the function runs
```

---

## 4. Decorators with Arguments (`*args`, `**kwargs`)

Real functions usually take arguments, so the wrapper needs to accept and forward them.

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timer
def add(a, b):
    return a + b

print(add(5, 3))   # add took 0.0000 seconds \n 8
```

---

## 5. Decorators That Take Their Own Arguments

A decorator factory is a function that returns a decorator — used when the decorator itself needs configuration.

```python
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    print(f"Hello, {name}!")

greet("Asha")
# Hello, Asha!
# Hello, Asha!
# Hello, Asha!
```

---

## 6. Preserving Metadata with `functools.wraps`

Without `functools.wraps`, decorated functions lose their original name/docstring.

```python
import functools

def logger(func):
    @functools.wraps(func)   # preserves func.__name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@logger
def add(a, b):
    """Adds two numbers."""
    return a + b

print(add(2, 3))          # Calling add \n 5
print(add.__name__)       # add (without @wraps, this would print 'wrapper')
print(add.__doc__)        # Adds two numbers.
```

### Beginner tip
Always use `@functools.wraps(func)` inside your custom decorators — it keeps debugging, documentation, and introspection tools working correctly.

---

## 7. Knowledge Check

1. What does a decorator actually do to the function it decorates?
2. What is the `@decorator_name` syntax shorthand for?
3. Why does a wrapper function typically use `*args, **kwargs`?
4. What problem does `functools.wraps` solve?

---

**Next:** [Class-level Decorators →](./01-Class-level-Decorators.md)
