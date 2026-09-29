> **Trainer's Note:** A generator is a simple way to create an iterator using a function with `yield` instead of `return` — Python handles all the `__iter__`/`__next__` bookkeeping for you.

---

## 📑 Table of Contents
1. [The `yield` Keyword](#1-the-yield-keyword)
2. [Generator Functions vs Normal Functions](#2-generator-functions-vs-normal-functions)
3. [Generators are Iterators Too](#3-generators-are-iterators-too)
4. [Generator Expressions Recap](#4-generator-expressions-recap)
5. [Why Use Generators? (Memory Efficiency)](#5-why-use-generators-memory-efficiency)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. The `yield` Keyword

`yield` pauses a function and sends a value back to the caller, **remembering** exactly where it left off for next time.

### Real-world analogy
```
return  = handing over the whole cake at once, then the baker goes home
yield   = the baker hands you one slice at a time, staying in the kitchen
          ready to cut the next slice whenever you ask
```

```python
def countdown(start):
    while start > 0:
        yield start
        start -= 1

for number in countdown(3):
    print(number)
# 3
# 2
# 1
```

---

## 2. Generator Functions vs Normal Functions

```python
def normal_function():
    return [1, 2, 3]         # builds the whole list immediately

def generator_function():
    yield 1
    yield 2
    yield 3                  # produces values one at a time, on demand

print(normal_function())     # [1, 2, 3]
print(generator_function())  # <generator object generator_function at 0x...>
```

Calling a generator function does **not** run its code right away — it just creates a generator object. The code runs only as values are requested.

```python
gen = generator_function()
print(next(gen))   # 1  -> runs up to first yield
print(next(gen))   # 2  -> resumes, runs to second yield
print(next(gen))   # 3
print(next(gen))   # ❌ StopIteration -> function finished
```

---

## 3. Generators are Iterators Too

Every generator automatically supports `iter()` and `next()`, so it works seamlessly with `for` loops.

```python
def squares_up_to(n):
    for i in range(1, n + 1):
        yield i ** 2

for sq in squares_up_to(5):
    print(sq, end=" ")   # 1 4 9 16 25

# Manually
gen = squares_up_to(3)
print(next(gen))   # 1
print(next(gen))   # 4
print(next(gen))   # 9
```

### Infinite generators
Because values are produced lazily, a generator can even represent an **infinite** sequence safely (as long as you don't try to convert it to a list!).

```python
def infinite_counter(start=0):
    while True:
        yield start
        start += 1

counter = infinite_counter()
print(next(counter))   # 0
print(next(counter))   # 1
print(next(counter))   # 2
# ... goes on forever, only stops when you stop asking
```

---

## 4. Generator Expressions Recap

A shorthand, one-line way to create a generator (covered earlier in Comprehensions):

```python
squares = (n ** 2 for n in range(1, 6))
print(next(squares))   # 1
print(list(squares))   # [4, 9, 16, 25] -> remaining values
```

---

## 5. Why Use Generators? (Memory Efficiency)

```python
# List: computes and stores ALL 10 million values in memory right now
big_list = [n * n for n in range(10_000_000)]

# Generator: computes ONE value at a time, uses almost no memory
big_gen = (n * n for n in range(10_000_000))
```

Generators are ideal for:
- Reading huge files line by line
- Streaming data (e.g., API pagination)
- Infinite sequences
- Pipelines where each step processes one item before moving to the next

### Beginner tip
If a function's job is to **produce a sequence of values over time** rather than build a full collection upfront, reach for `yield` — it's simpler than writing a custom iterator class and far more memory-friendly than returning a full list.

---

## 6. Knowledge Check

1. What keyword turns a normal function into a generator function?
2. What happens when you call a generator function — does its code run immediately?
3. Why can a generator safely represent an infinite sequence, while a list cannot?
4. Write a generator function `even_numbers(limit)` that yields even numbers from 0 up to `limit`.

---

**Previous:** [← Iterators](./00-Iterators.md)

🎉 **Iterators and Generators track complete!** You've learned iterables, iterators, `iter()`/`next()`, custom iterator classes, generator functions with `yield`, and generator expressions.
