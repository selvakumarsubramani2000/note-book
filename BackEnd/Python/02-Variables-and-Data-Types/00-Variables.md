# 📦 Variables in Python

> **Trainer's Note:** A variable is simply a labeled box that stores a value. In Python, you don't declare a type — Python figures it out automatically.

---

## 📑 Table of Contents
1. [What is a Variable?](#1-what-is-a-variable)
2. [Declaring Variables](#2-declaring-variables)
3. [Dynamic Typing](#3-dynamic-typing)
4. [Multiple Assignment](#4-multiple-assignment)
5. [Naming Rules](#5-naming-rules)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. What is a Variable?

A **variable** is a name that refers to a value stored in memory.

### Real-world analogy
```
Variable = a labeled storage box
  box "age"  contains  25
  box "name" contains  "Selva"
```

---

## 2. Declaring Variables

Unlike C#/Java, Python has **no type keyword** — just assign a value:

```python
age = 25
name = "Selva"
price = 99.99
is_active = True
```

No `int`, `string`, `bool` keyword needed. Python infers the type from the value.

---

## 3. Dynamic Typing

Python is **dynamically typed** — a variable's type can change as the program runs.

```python
x = 10        # x is an int
print(type(x))   # <class 'int'>

x = "hello"   # now x is a string
print(type(x))   # <class 'str'>
```

### Compare with C# (statically typed)
```csharp
int x = 10;
x = "hello"; // ❌ compile error in C#
```

```python
x = 10
x = "hello"  # ✅ perfectly valid in Python
```

### Beginner caution
Just because you *can* change types doesn't mean you *should* — keep variable purpose consistent for readable code.

---

## 4. Multiple Assignment

### Assign same value to many variables
```python
a = b = c = 0
print(a, b, c)   # 0 0 0
```

### Assign multiple values in one line
```python
x, y, z = 1, 2, 3
print(x, y, z)   # 1 2 3
```

### Swap values (Python trick — no temp variable needed)
```python
x, y = 5, 10
x, y = y, x
print(x, y)   # 10 5
```

---

## 5. Naming Rules

| Rule | Example |
|------|---------|
| Must start with letter or underscore | `_score`, `total` |
| Cannot start with a digit | ❌ `1value` |
| Only letters, digits, underscores | `user_name1` |
| Case-sensitive | `Age` and `age` are different |
| Cannot use Python keywords | ❌ `class = 5` |

### Naming convention (PEP 8)
```python
student_name = "Anu"     # snake_case preferred for variables
MAX_LIMIT = 100           # UPPER_CASE for constants (by convention)
```

---

## 6. Knowledge Check

1. Does Python require you to declare a variable's type?
2. What will `type(x)` return after `x = "hello"`?
3. Write code to swap two variables without a temp variable.
4. Is `2value` a valid Python variable name? Why or why not?

---

**Next:** [Keywords →](./01-Keywords.md)
