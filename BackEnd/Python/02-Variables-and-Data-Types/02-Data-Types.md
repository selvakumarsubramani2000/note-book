# 🧬 Data Types in Python

> **Trainer's Note:** Python has built-in data types for numbers, text, booleans, and collections. Since typing is dynamic, knowing these types well helps you avoid bugs.

---

## 📑 Table of Contents
1. [Overview of Data Types](#1-overview-of-data-types)
2. [Numeric Types](#2-numeric-types)
3. [Text Type](#3-text-type)
4. [Boolean Type](#4-boolean-type)
5. [Checking and Converting Types](#5-checking-and-converting-types)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. Overview of Data Types

| Category | Types |
|----------|-------|
| Numeric | `int`, `float`, `complex` |
| Text | `str` |
| Boolean | `bool` |
| Sequence | `list`, `tuple`, `range` |
| Mapping | `dict` |
| Set | `set`, `frozenset` |
| None | `NoneType` |

This guide focuses on numeric, text, and boolean. Collections (`list`, `set`, `tuple`, `dict`) are covered in their own topic.

### Real-world analogy
```
int    = whole item count (3 apples)
float  = measured quantity (2.5 kg)
str    = a label/text (product name)
bool   = yes/no switch
```

---

## 2. Numeric Types

```python
age = 25          # int
price = 19.99     # float
result = 3 + 4j   # complex (rarely used by beginners)

print(type(age))     # <class 'int'>
print(type(price))   # <class 'float'>
```

### Common numeric operations
```python
a = 10
b = 3

print(a / b)    # 3.3333333333333335 (true division → float)
print(a // b)   # 3 (floor division → int)
print(a % b)    # 1 (remainder)
print(a ** b)   # 1000 (power)
```

---

## 3. Text Type

```python
name = "Selva"
message = 'Hello there'
multiline = """This is
a multi-line string"""
```

### Common string operations
```python
name = "python"
print(name.upper())      # PYTHON
print(name.capitalize()) # Python
print(len(name))         # 6
print(name[0])           # p (indexing)
print(name + " rocks")   # python rocks
```

(Detailed string methods are covered in the **Data-Structures → String** topic.)

---

## 4. Boolean Type

```python
is_valid = True
is_empty = False

print(type(is_valid))   # <class 'bool'>
```

### Booleans from comparisons
```python
print(5 > 3)     # True
print(5 == 3)    # False
```

### Truthy / Falsy values
```python
bool(0)      # False
bool("")     # False
bool([])     # False
bool(None)   # False

bool(1)      # True
bool("hi")   # True
bool([1,2])  # True
```

---

## 5. Checking and Converting Types

### Check type
```python
x = 10
print(type(x))          # <class 'int'>
print(isinstance(x, int))  # True
```

### Type conversion (casting)
```python
a = "25"
b = int(a)      # string → int
print(b + 5)    # 30

c = 3.9
d = int(c)      # float → int (truncates, not rounds!)
print(d)        # 3

e = 100
f = str(e)      # int → string
print(f + "%")  # "100%"
```

---

## 6. Knowledge Check

1. What is the difference between `int` and `float`?
2. What does `10 // 3` return?
3. Is an empty string `""` truthy or falsy?
4. How do you convert a string `"42"` to an integer?
5. What does `isinstance(x, int)` do?

---

**Previous:** [← Keywords](./01-Keywords.md)
**Next:** [Identifiers →](./03-Identifiers.md)
