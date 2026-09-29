# ✂️ Slicing in Python

> **Trainer's Note:** Slicing lets you extract a portion (a "slice") of a sequence — string, list, or tuple — using a simple `start:stop:step` syntax.

---

## 📑 Table of Contents
1. [Slicing Syntax](#1-slicing-syntax)
2. [Slicing Strings](#2-slicing-strings)
3. [Slicing Lists](#3-slicing-lists)
4. [Step and Negative Indices](#4-step-and-negative-indices)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Slicing Syntax

```
sequence[start:stop:step]
```

- **start** — index to begin (inclusive), default `0`
- **stop** — index to end (exclusive!), default = length
- **step** — how many indices to skip, default `1`

### Real-world analogy
```
Slicing = cutting a piece of ribbon
  start = where you begin cutting
  stop  = where you stop (but don't include that mark)
  step  = skip pattern (every 2nd mark, etc.)
```

---

## 2. Slicing Strings

```python
text = "Hello, Python!"

print(text[0:5])     # "Hello"
print(text[:5])      # "Hello"      (start defaults to 0)
print(text[7:]) # "Python!"   (stop defaults to end)
print(text[:])       # full copy of the string
print(text[-7:])     # "Python!"    (negative index from end)
```

### Reversing a string (popular trick)
```python
text = "Python"
print(text[::-1])   # "nohtyP"
```

---

## 3. Slicing Lists

```python
numbers = [10, 20, 30, 40, 50, 60]

print(numbers[1:4])    # [20, 30, 40]
print(numbers[:3])     # [10, 20, 30]
print(numbers[3:])     # [40, 50, 60]
print(numbers[-3:])    # [40, 50, 60] (last 3 items)
print(numbers[:-2])    # [10, 20, 30, 40] (all except last 2)
```

### Modifying a list with slicing
```python
numbers = [10, 20, 30, 40, 50]
numbers[1:3] = [99, 100]     # replace a slice
print(numbers)   # [10, 99, 100, 40, 50]
```

---

## 4. Step and Negative Indices

```python
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(numbers[0:10:2])   # [0, 2, 4, 6, 8]   (every 2nd item)
print(numbers[::3])      # [0, 3, 6, 9]      (every 3rd item)
print(numbers[::-1])     # reversed list
print(numbers[8:2:-2])   # [8, 6, 4]         (backwards with step)
```

### Index reference chart
```
Index:      0    1    2    3    4
Value:    'P'  'y'  't'  'h'  'n'
Neg idx:   -5   -4   -3   -2   -1
```

---

## 5. Knowledge Check

1. What does `text[2:5]` return for `text = "Python"`?
2. Write a slice expression to reverse a list.
3. What is the default value of `step` in slicing?
4. What does `numbers[:-1]` give you?

---

**Previous:** [← Dictionary Data Types](./04-Dictionary-Data-Types.md)

🎉 **Data Structures track complete!** You now know Strings, Lists, Sets, Tuples, Dictionaries, and Slicing in Python.
