# 📋 List Data Type in Python

> **Trainer's Note:** A list is an ordered, changeable (mutable) collection that can hold mixed data types. It's Python's most commonly used collection.

---

## 📑 Table of Contents
1. [Creating Lists](#1-creating-lists)
2. [Accessing and Modifying](#2-accessing-and-modifying)
3. [Common List Methods](#3-common-list-methods)
4. [Looping Through a List](#4-looping-through-a-list)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Creating Lists

```python
fruits = ["apple", "banana", "cherry"]
mixed = [1, "two", 3.0, True]
empty = []

print(type(fruits))   # <class 'list'>
```

### Real-world analogy
```
List = a shopping list on paper
  items in order
  you can add, remove, or reorder items anytime
```

---

## 2. Accessing and Modifying

```python
fruits = ["apple", "banana", "cherry"]

print(fruits[0])     # apple
print(fruits[-1])    # cherry (last item)

fruits[1] = "mango"  # lists are mutable
print(fruits)        # ['apple', 'mango', 'cherry']

fruits.append("kiwi")
print(fruits)        # ['apple', 'mango', 'cherry', 'kiwi']
```

---

## 3. Common List Methods

```python
numbers = [5, 3, 8, 1]

numbers.append(10)      # add to end        → [5, 3, 8, 1, 10]
numbers.insert(0, 100)  # insert at index    → [100, 5, 3, 8, 1, 10]
numbers.remove(3)       # remove value 3     → [100, 5, 8, 1, 10]
numbers.pop()           # remove & return last item
numbers.sort()          # sort ascending
numbers.reverse()       # reverse order
print(len(numbers))     # count of items
print(numbers.count(5)) # how many times 5 appears
print(numbers.index(8)) # position of value 8
```

### Combining lists
```python
a = [1, 2]
b = [3, 4]
combined = a + b        # [1, 2, 3, 4]
a.extend(b)              # a becomes [1, 2, 3, 4]
```

### List comprehension (compact way to build lists)
```python
squares = [x * x for x in range(1, 6)]
print(squares)   # [1, 4, 9, 16, 25]

evens = [x for x in range(10) if x % 2 == 0]
print(evens)     # [0, 2, 4, 6, 8]
```

---

## 4. Looping Through a List

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)

for index, fruit in enumerate(fruits):
    print(index, fruit)
```

**Output:**
```
apple
banana
cherry
0 apple
1 banana
2 cherry
```

---

## 5. Knowledge Check

1. Is a Python list mutable or immutable?
2. What does `fruits.append("kiwi")` do?
3. Write a list comprehension to get squares of numbers 1 to 5.
4. What's the difference between `remove()` and `pop()`?

---

**Previous:** [← String Data Type](./00-String-Data-Type.md)
**Next:** [Set Data Types →](./02-Set-Data-Types.md)
