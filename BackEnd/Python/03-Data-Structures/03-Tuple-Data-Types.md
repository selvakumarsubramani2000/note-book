# 🔗 Tuple Data Type in Python

> **Trainer's Note:** A tuple is like a list, but immutable — once created, its items can't change. Use tuples for fixed collections of data.

---

## 📑 Table of Contents
1. [Creating Tuples](#1-creating-tuples)
2. [Tuple Immutability](#2-tuple-immutability)
3. [Accessing Tuple Items](#3-accessing-tuple-items)
4. [Tuple Unpacking](#4-tuple-unpacking)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Creating Tuples

```python
point = (3, 4)
colors = ("red", "green", "blue")
single = (5,)         # NOTE: comma required for single-item tuple!
not_a_tuple = (5)     # this is just an int in parentheses

print(type(point))    # <class 'tuple'>
print(type(single))   # <class 'tuple'>
print(type(not_a_tuple))  # <class 'int'>
```

### Real-world analogy
```
Tuple = a sealed envelope with fixed contents
  (latitude, longitude) — coordinates that shouldn't change
```

---

## 2. Tuple Immutability

```python
point = (3, 4)
# point[0] = 10   # ❌ TypeError: 'tuple' object does not support item assignment
```

Once created, you cannot change, add, or remove items directly.

### Why use tuples then?
- Faster than lists (slightly)
- Signal "this data shouldn't change" (safer code intent)
- Can be used as dictionary keys (lists cannot)

```python
locations = {(10.0, 20.0): "Office", (30.0, 40.0): "Warehouse"}
```

---

## 3. Accessing Tuple Items

```python
colors = ("red", "green", "blue")

print(colors[0])     # red
print(colors[-1])    # blue
print(len(colors))   # 3

for color in colors:
    print(color)
```

### Tuples can be nested
```python
nested = (1, (2, 3), [4, 5])
print(nested[1][0])   # 2
```

---

## 4. Tuple Unpacking

```python
point = (3, 4)
x, y = point
print(x, y)   # 3 4

person = ("Selva", 30, "Chennai")
name, age, city = person
print(name, age, city)
```

### Function returning multiple values (common real use case)
```python
def get_min_max(numbers):
    return min(numbers), max(numbers)   # returns a tuple

low, high = get_min_max([4, 2, 9, 1])
print(low, high)   # 1 9
```

### Star unpacking
```python
first, *rest = (1, 2, 3, 4)
print(first)   # 1
print(rest)    # [2, 3, 4]
```

---

## 5. Knowledge Check

1. Is a tuple mutable or immutable?
2. How do you create a tuple with a single item?
3. Why might you choose a tuple over a list?
4. Write code to unpack `(10, 20)` into two variables `a` and `b`.

---

**Previous:** [← Set Data Types](./02-Set-Data-Types.md)
**Next:** [Dictionary Data Types →](./04-Dictionary-Data-Types.md)
