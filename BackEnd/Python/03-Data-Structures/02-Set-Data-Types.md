# 🎯 Set Data Type in Python

> **Trainer's Note:** A set stores unique, unordered items. Perfect when you need to remove duplicates or perform math-style set operations (union, intersection).

---

## 📑 Table of Contents
1. [Creating Sets](#1-creating-sets)
2. [Set Characteristics](#2-set-characteristics)
3. [Common Set Operations](#3-common-set-operations)
4. [Set Methods](#4-set-methods)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Creating Sets

```python
colors = {"red", "green", "blue"}
numbers = set([1, 2, 2, 3, 3, 3])   # duplicates auto-removed
empty_set = set()   # NOTE: {} creates an empty dict, not a set!

print(numbers)   # {1, 2, 3}
```

### Real-world analogy
```
Set = a bag of unique stamps
  no duplicate stamps allowed
  order doesn't matter, just which stamps you own
```

---

## 2. Set Characteristics

| Property | Description |
|----------|-------------|
| Unordered | No guaranteed order, no indexing (`numbers[0]` ❌) |
| Unique items | Duplicates are automatically removed |
| Mutable | Can add/remove items |
| Unhashable items not allowed | Lists can't be set elements |

```python
nums = {1, 2, 3}
# print(nums[0])  # ❌ TypeError: 'set' object is not subscriptable
```

---

## 3. Common Set Operations

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(a | b)   # Union            → {1, 2, 3, 4, 5, 6}
print(a & b)   # Intersection     → {3, 4}
print(a - b)   # Difference       → {1, 2}
print(a ^ b)   # Symmetric diff   → {1, 2, 5, 6}
```

### Real-world analogy
```
a | b  = combine two guest lists (all unique names)
a & b  = names common to both lists
a - b  = names only in list a
a ^ b  = names not shared by both
```

---

## 4. Set Methods

```python
colors = {"red", "green"}

colors.add("blue")          # add single item
colors.update(["yellow", "pink"])  # add multiple
colors.remove("red")        # removes; error if not found
colors.discard("purple")    # removes if present; no error if missing
colors.clear()               # empties the set

fruits = {"apple", "banana"}
print("apple" in fruits)     # True — fast membership check
print(len(fruits))           # 2
```

### Converting between list and set (removing duplicates)
```python
nums = [1, 2, 2, 3, 3, 3]
unique_nums = list(set(nums))
print(unique_nums)   # [1, 2, 3] (order not guaranteed)
```

---

## 5. Knowledge Check

1. Can a set contain duplicate values?
2. How do you find the union of two sets?
3. What is the difference between `remove()` and `discard()` on a set?
4. Why does `{}` NOT create an empty set?

---

**Previous:** [← List Data Types](./01-List-Data-Types.md)
**Next:** [Tuple Data Types →](./03-Tuple-Data-Types.md)
