# 🗺️ Map, Filter, and Reduce in Python

> **Trainer's Note:** `map()`, `filter()`, and `reduce()` are functional-programming tools that let you transform, select, and combine items in a collection without writing explicit loops.

---

## 📑 Table of Contents
1. [Recap: Lambda Functions](#1-recap-lambda-functions)
2. [`map()` — Transform Every Item](#2-map--transform-every-item)
3. [`filter()` — Keep Only Matching Items](#3-filter--keep-only-matching-items)
4. [`reduce()` — Combine Into a Single Value](#4-reduce--combine-into-a-single-value)
5. [Comparing with List Comprehensions](#5-comparing-with-list-comprehensions)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. Recap: Lambda Functions

A `lambda` is a small, anonymous (unnamed) function written in one line — perfect for short throwaway logic used with `map`/`filter`/`reduce`.

```python
square = lambda x: x ** 2
print(square(5))   # 25

add = lambda a, b: a + b
print(add(2, 3))   # 5
```

### Real-world analogy
```
map    = an assembly line that transforms every item the same way
filter = a sieve that only lets matching items pass through
reduce = a compactor that squashes everything into one final result
```

---

## 2. `map()` — Transform Every Item

`map(function, iterable)` applies `function` to **every item** and returns a map object (convert to `list()` to see results).

```python
numbers = [1, 2, 3, 4, 5]

squared = map(lambda x: x ** 2, numbers)
print(list(squared))   # [1, 4, 9, 16, 25]

names = ["asha", "ravi", "meena"]
capitalized = map(str.upper, names)
print(list(capitalized))   # ['ASHA', 'RAVI', 'MEENA']
```

### `map()` with multiple iterables
```python
a = [1, 2, 3]
b = [10, 20, 30]
sums = map(lambda x, y: x + y, a, b)
print(list(sums))   # [11, 22, 33]
```

---

## 3. `filter()` — Keep Only Matching Items

`filter(function, iterable)` keeps only the items where `function` returns `True`.

```python
numbers = range(1, 11)

evens = filter(lambda x: x % 2 == 0, numbers)
print(list(evens))   # [2, 4, 6, 8, 10]

words = ["python", "is", "fun", "to", "learn"]
long_words = filter(lambda w: len(w) > 2, words)
print(list(long_words))   # ['python', 'fun', 'learn']
```

---

## 4. `reduce()` — Combine Into a Single Value

`reduce()` lives in the `functools` module. It repeatedly applies a function to pairs of items until only **one value** remains.

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]

total = reduce(lambda x, y: x + y, numbers)
print(total)   # 15  -> ((((1+2)+3)+4)+5)

product = reduce(lambda x, y: x * y, numbers)
print(product)   # 120 -> 1*2*3*4*5

# With an initial value
total_with_start = reduce(lambda x, y: x + y, numbers, 100)
print(total_with_start)   # 115 -> starts from 100
```

### How reduce works step by step
```
reduce(f, [1, 2, 3, 4, 5])
  step 1: f(1, 2)   = 3
  step 2: f(3, 3)   = 6
  step 3: f(6, 4)   = 10
  step 4: f(10, 5)  = 15   <- final result
```

---

## 5. Comparing with List Comprehensions

Most `map`/`filter` use cases can also be written as list comprehensions — often considered more "Pythonic" and readable.

```python
numbers = [1, 2, 3, 4, 5]

# map style
squared_map = list(map(lambda x: x ** 2, numbers))

# comprehension style
squared_comp = [x ** 2 for x in numbers]

print(squared_map == squared_comp)   # True

# filter style
evens_filter = list(filter(lambda x: x % 2 == 0, numbers))

# comprehension style
evens_comp = [x for x in numbers if x % 2 == 0]

print(evens_filter == evens_comp)    # True
```

### Beginner tip
`reduce()` has no direct comprehension equivalent — it's genuinely useful for combining values (sums, products, finding max, merging dictionaries, etc.). For simple `map`/`filter` cases, many developers prefer list comprehensions for readability.

---

## 6. Knowledge Check

1. What does `map()` return, and why do you usually wrap it in `list()`?
2. Write a `filter()` call that keeps only strings longer than 4 characters from `["cat", "elephant", "dog", "giraffe"]`.
3. Use `reduce()` to find the maximum number in `[4, 9, 2, 7, 5]` (hint: `lambda x, y: x if x > y else y`).
4. When would you prefer a list comprehension over `map()`/`filter()`?

---

**Next:** Continue to [Iterators and Generators →](../14-Iterators-and-Generators/00-Iterators.md)
