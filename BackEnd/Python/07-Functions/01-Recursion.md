# 🔁 Recursion in Python

> **Trainer's Note:** Recursion is when a function calls itself to solve a smaller version of the same problem, until it reaches a simple base case it can answer directly.

---

## 📑 Table of Contents
1. [What is Recursion?](#1-what-is-recursion)
2. [Base Case and Recursive Case](#2-base-case-and-recursive-case)
3. [Classic Examples](#3-classic-examples)
4. [Recursion vs Iteration](#4-recursion-vs-iteration)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is Recursion?

```python
def countdown(n):
    if n == 0:
        print("Liftoff!")
    else:
        print(n)
        countdown(n - 1)   # function calls itself

countdown(3)
```

**Output:**
```
3
2
1
Liftoff!
```

### Real-world analogy
```
Recursion = Russian nesting dolls (Matryoshka)
  open one doll → find a smaller doll inside → repeat
  until you reach the smallest doll (base case) with nothing inside
```

---

## 2. Base Case and Recursive Case

Every recursive function needs:

1. **Base case** — the simplest scenario where the function stops calling itself
2. **Recursive case** — where the function calls itself with a smaller/simpler input

```python
def factorial(n):
    if n == 0 or n == 1:   # base case
        return 1
    return n * factorial(n - 1)   # recursive case

print(factorial(5))   # 5 * 4 * 3 * 2 * 1 = 120
```

### ⚠️ Without a base case → infinite recursion
```python
def broken(n):
    return broken(n - 1)   # ❌ never stops → RecursionError

# broken(5)   # RecursionError: maximum recursion depth exceeded
```

---

## 3. Classic Examples

### Factorial
```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(4))   # 24
```

### Fibonacci sequence
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

for i in range(7):
    print(fibonacci(i), end=" ")
# Output: 0 1 1 2 3 5 8
```

### Sum of a list
```python
def sum_list(numbers):
    if not numbers:          # base case: empty list
        return 0
    return numbers[0] + sum_list(numbers[1:])

print(sum_list([1, 2, 3, 4]))   # 10
```

### Reversing a string
```python
def reverse_string(s):
    if len(s) <= 1:
        return s
    return reverse_string(s[1:]) + s[0]

print(reverse_string("Python"))   # nohtyP
```

---

## 4. Recursion vs Iteration

| Aspect | Recursion | Iteration (loops) |
|--------|-----------|--------------------|
| Style | Function calls itself | Uses `for`/`while` |
| Readability | Often cleaner for tree/nested problems | Simpler for straightforward repetition |
| Memory | Uses call stack (can hit limits) | Generally more memory-efficient |
| Performance | Can be slower (function call overhead) | Usually faster |

### Same problem, both ways
```python
# Recursive
def factorial_recursive(n):
    return 1 if n <= 1 else n * factorial_recursive(n - 1)

# Iterative
def factorial_iterative(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

print(factorial_recursive(5), factorial_iterative(5))   # 120 120
```

### Beginner tip
Use recursion when a problem naturally breaks into smaller versions of itself (trees, folders, nested data). Otherwise, a simple loop is often easier to read and debug.

---

## 5. Knowledge Check

1. What two parts must every recursive function have?
2. What happens if a recursive function has no base case?
3. Write a recursive function to calculate the sum of numbers from 1 to `n`.
4. When would you prefer recursion over a loop?

---

**Previous:** [← Types of Functions](./00-Types-of-Functions.md)
**Next:** [Arguments & Unpacking →](./02-Arguments-and-Unpacking.md)
