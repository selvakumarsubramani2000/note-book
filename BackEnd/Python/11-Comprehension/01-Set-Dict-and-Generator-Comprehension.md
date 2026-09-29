# 🧰 Set, Dict, and Generator Comprehensions

> **Trainer's Note:** The comprehension pattern isn't just for lists — Python offers the same shorthand for sets, dictionaries, and memory-efficient generators.

---

## 📑 Table of Contents
1. [Set Comprehension](#1-set-comprehension)
2. [Dictionary Comprehension](#2-dictionary-comprehension)
3. [Generator Expressions](#3-generator-expressions)
4. [Comparing All Comprehension Types](#4-comparing-all-comprehension-types)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Set Comprehension

Same as list comprehension, but with `{}` — produces a **set** (unique, unordered values).

```
{expression for item in iterable}
```

```python
numbers = [1, 2, 2, 3, 3, 3, 4]
unique_squares = {n ** 2 for n in numbers}
print(unique_squares)   # {16, 1, 4, 9} (order not guaranteed, duplicates removed)

words = ["apple", "Banana", "APPLE", "banana"]
unique_lower = {w.lower() for w in words}
print(unique_lower)   # {'apple', 'banana'}
```

### Real-world analogy
```
Set comprehension = sorting mail into a box that automatically
  rejects duplicates — only one copy of each unique item survives
```

---

## 2. Dictionary Comprehension

Builds a **dictionary** using `{key: value for item in iterable}`.

```
{key_expr: value_expr for item in iterable}
```

```python
names = ["asha", "ravi", "meena"]
name_lengths = {name: len(name) for name in names}
print(name_lengths)   # {'asha': 4, 'ravi': 4, 'meena': 5}

numbers = range(1, 6)
squares_dict = {n: n ** 2 for n in numbers}
print(squares_dict)   # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```

### With a condition
```python
scores = {"Asha": 85, "Ravi": 45, "Meena": 92, "Kiran": 60}
passed = {name: score for name, score in scores.items() if score >= 60}
print(passed)   # {'Asha': 85, 'Meena': 92, 'Kiran': 60}
```

### Swapping keys and values
```python
original = {"a": 1, "b": 2, "c": 3}
swapped = {value: key for key, value in original.items()}
print(swapped)   # {1: 'a', 2: 'b', 3: 'c'}
```

---

## 3. Generator Expressions

Same syntax idea, but with `()` — produces a **generator** that computes values **lazily** (one at a time), instead of building the whole collection in memory at once.

```
(expression for item in iterable)
```

```python
squares_gen = (n ** 2 for n in range(1, 6))
print(squares_gen)          # <generator object <genexpr> at 0x...>
print(type(squares_gen))    # <class 'generator'>

for value in squares_gen:
    print(value, end=" ")   # 1 4 9 16 25
```

### Why use a generator instead of a list?
```python
# List comprehension -> builds ALL values in memory immediately
big_list = [n * n for n in range(10_000_000)]   # uses a lot of memory

# Generator expression -> computes values one at a time, on demand
big_gen = (n * n for n in range(10_000_000))    # uses very little memory
```

Generators are perfect for **large or infinite** data streams where you only need to process one value at a time.

---

## 4. Comparing All Comprehension Types

| Type | Syntax | Produces |
|------|--------|----------|
| List | `[x for x in iterable]` | `list` |
| Set | `{x for x in iterable}` | `set` |
| Dict | `{k: v for x in iterable}` | `dict` |
| Generator | `(x for x in iterable)` | `generator` (lazy) |

### Beginner tip
If you find yourself writing `list(x for x in iterable)`, you probably just want a list comprehension `[x for x in iterable]` instead — cleaner and equally fast.

---

## 5. Knowledge Check

1. Write a set comprehension that returns the unique lengths of words in `["cat", "dog", "lion", "ant"]`.
2. Write a dictionary comprehension that maps each number 1–5 to whether it's even (`True`/`False`).
3. What is the main advantage of a generator expression over a list comprehension?
4. When would you choose a set comprehension over a list comprehension?

---

**Previous:** [← List Comprehension](./00-List-Comprehension.md)

🎉 **Comprehension track complete!** You've learned list, set, dictionary comprehensions, and generator expressions.
