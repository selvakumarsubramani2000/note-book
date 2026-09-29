# 🧮 List Comprehension in Python

> **Trainer's Note:** List comprehension is a short, readable way to build a new list from an existing iterable, in a single line — instead of writing a full `for` loop.

---

## 📑 Table of Contents
1. [The Problem It Solves](#1-the-problem-it-solves)
2. [Basic Syntax](#2-basic-syntax)
3. [Adding a Condition (`if`)](#3-adding-a-condition-if)
4. [`if`/`else` Inside Comprehension](#4-ifelse-inside-comprehension)
5. [Nested Loops in Comprehension](#5-nested-loops-in-comprehension)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. The Problem It Solves

```python
# Traditional loop
squares = []
for n in range(1, 6):
    squares.append(n ** 2)
print(squares)   # [1, 4, 9, 16, 25]

# Same result with list comprehension
squares = [n ** 2 for n in range(1, 6)]
print(squares)   # [1, 4, 9, 16, 25]
```

### Real-world analogy
```
List comprehension = an assembly line instruction:
  "for each item coming in, transform it this way, and put it on the output belt"
```

---

## 2. Basic Syntax

```
[expression for item in iterable]
```

```python
names = ["asha", "ravi", "meena"]
upper_names = [name.upper() for name in names]
print(upper_names)   # ['ASHA', 'RAVI', 'MEENA']

numbers = [1, 2, 3, 4]
doubled = [n * 2 for n in numbers]
print(doubled)   # [2, 4, 6, 8]
```

---

## 3. Adding a Condition (`if`)

```
[expression for item in iterable if condition]
```

```python
numbers = range(1, 11)
evens = [n for n in numbers if n % 2 == 0]
print(evens)   # [2, 4, 6, 8, 10]

words = ["python", "is", "fun", "to", "learn"]
long_words = [w for w in words if len(w) > 2]
print(long_words)   # ['python', 'fun', 'learn']
```

---

## 4. `if`/`else` Inside Comprehension

When you want to transform **every** item differently based on a condition (not filter them out), put `if/else` before the `for`.

```
[expression_if_true if condition else expression_if_false for item in iterable]
```

```python
numbers = [1, 2, 3, 4, 5, 6]
labels = ["even" if n % 2 == 0 else "odd" for n in numbers]
print(labels)   # ['odd', 'even', 'odd', 'even', 'odd', 'even']
```

### Combining filter + transform
```python
numbers = range(1, 11)
result = [n * 10 if n % 2 == 0 else n for n in numbers if n != 5]
print(result)   # [1, 2, 20, 4, 60, 7, 80, 9, 100]
```

---

## 5. Nested Loops in Comprehension

```python
# Traditional nested loop
pairs = []
for x in [1, 2]:
    for y in ["a", "b"]:
        pairs.append((x, y))
print(pairs)   # [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]

# Same with comprehension
pairs = [(x, y) for x in [1, 2] for y in ["a", "b"]]
print(pairs)   # [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]
```

### Flattening a nested list
```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
print(flat)   # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### Beginner tip
List comprehensions are great for **short, simple** transformations. If the logic needs multiple steps or gets hard to read on one line, use a regular `for` loop instead — readability wins.

---

## 6. Knowledge Check

1. Rewrite this loop as a list comprehension: `result = []; for x in range(5): result.append(x * x)`
2. Write a list comprehension that returns only the odd numbers from `range(1, 20)`.
3. Write a list comprehension that labels numbers 1–5 as `"positive"` if greater than 0, else `"non-positive"`.
4. When should you avoid using a list comprehension in favor of a regular loop?

---

**Next:** [Set, Dict & Generator Comprehensions →](./01-Set-Dict-and-Generator-Comprehension.md)
