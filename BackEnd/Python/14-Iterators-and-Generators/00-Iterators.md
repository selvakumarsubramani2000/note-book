# 🔂 Iterators in Python

> **Trainer's Note:** An iterator is an object that lets you go through a collection **one item at a time**, remembering where it left off — it's the mechanism that powers every `for` loop in Python.

---

## 📑 Table of Contents
1. [Iterable vs Iterator](#1-iterable-vs-iterator)
2. [The `iter()` and `next()` Functions](#2-the-iter-and-next-functions)
3. [How a `for` Loop Really Works](#3-how-a-for-loop-really-works)
4. [Building a Custom Iterator Class](#4-building-a-custom-iterator-class)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Iterable vs Iterator

- **Iterable** — anything you can loop over (`list`, `tuple`, `str`, `dict`, `set`...). It has an `__iter__()` method.
- **Iterator** — the object that actually does the stepping, one item at a time. It has both `__iter__()` and `__next__()` methods.

### Real-world analogy
```
Iterable = a playlist (a collection of songs)
Iterator = the "play next" button that remembers which song is currently playing
```

```python
numbers = [1, 2, 3]        # this is an ITERABLE
iterator = iter(numbers)   # this creates an ITERATOR from it
```

---

## 2. The `iter()` and `next()` Functions

```python
numbers = [10, 20, 30]
it = iter(numbers)   # get an iterator

print(next(it))   # 10
print(next(it))   # 20
print(next(it))   # 30
print(next(it))   # ❌ StopIteration (no more items)
```

`next()` moves the iterator forward one step, and raises `StopIteration` once the items run out.

```python
it = iter([1, 2])
while True:
    try:
        value = next(it)
        print(value)
    except StopIteration:
        print("No more items!")
        break
```

---

## 3. How a `for` Loop Really Works

A `for` loop is just syntactic sugar around `iter()` and `next()`:

```python
numbers = [1, 2, 3]

# This for loop...
for n in numbers:
    print(n)

# ...is roughly equivalent to this:
it = iter(numbers)
while True:
    try:
        n = next(it)
        print(n)
    except StopIteration:
        break
```

---

## 4. Building a Custom Iterator Class

Any class can become an iterator by implementing `__iter__()` (returns `self`) and `__next__()` (returns the next value or raises `StopIteration`).

```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self   # the object itself is the iterator

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

for number in Countdown(3):
    print(number)
# 3
# 2
# 1
```

```python
# Works with next() too
cd = Countdown(2)
print(next(cd))   # 2
print(next(cd))   # 1
print(next(cd))   # ❌ StopIteration
```

### Beginner tip
You rarely need to write custom iterator classes by hand for simple cases — **generators** (covered next) make this much easier. But understanding iterators is key to understanding how `for` loops, generators, and many built-in functions work under the hood.

---

## 5. Knowledge Check

1. What is the difference between an iterable and an iterator?
2. What does `next()` do, and what exception does it raise when there are no more items?
3. What two methods must a class implement to be considered an iterator?
4. Write a custom iterator class `EvenNumbers(limit)` that yields even numbers from 0 up to `limit`.

---

**Next:** [Generators →](./01-Generators.md)
