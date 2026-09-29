# 🚧 Try, Except, and Finally in Python

> **Trainer's Note:** Exception handling lets your program deal with errors gracefully instead of crashing.

---

## 📑 Table of Contents
1. [What is an Exception?](#1-what-is-an-exception)
2. [Basic `try`/`except`](#2-basic-tryexcept)
3. [Catching Specific Exceptions](#3-catching-specific-exceptions)
4. [The `else` Clause](#4-the-else-clause)
5. [The `finally` Clause](#5-the-finally-clause)
6. [Common Built-in Exceptions](#6-common-built-in-exceptions)
7. [Knowledge Check](#7-knowledge-check)

---

## 1. What is an Exception?

An exception is an error that occurs **during execution** and stops the program unless handled.

```python
print(10 / 0)   # ZeroDivisionError: division by zero
```

### Real-world analogy
```
try     = "attempt this task"
except  = "if something goes wrong, here's the backup plan"
finally = "do this no matter what happens" (like turning off the stove)
```

---

## 2. Basic `try`/`except`

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("You can't divide by zero!")

print("Program continues...")
```

**Output:**
```
You can't divide by zero!
Program continues...
```

---

## 3. Catching Specific Exceptions

```python
try:
    numbers = [1, 2, 3]
    print(numbers[5])
except IndexError:
    print("Index out of range!")
except ZeroDivisionError:
    print("Can't divide by zero!")
except Exception as e:   # generic catch-all (use last)
    print(f"Something went wrong: {e}")
```

### Catching multiple exceptions in one block
```python
try:
    value = int("abc")
except (ValueError, TypeError) as e:
    print(f"Invalid input: {e}")
```

---

## 4. The `else` Clause

Runs **only if no exception occurred** in the `try` block.

```python
try:
    number = int("42")
except ValueError:
    print("Not a valid number")
else:
    print(f"Conversion succeeded: {number}")   # runs since no error happened
```

---

## 5. The `finally` Clause

Runs **always** — whether an exception happened or not. Great for cleanup (closing files, releasing resources).

```python
try:
    file = open("data.txt", "r")
    content = file.read()
except FileNotFoundError:
    print("File not found!")
finally:
    print("This always runs (e.g., closing resources)")
```

### Full flow example
```python
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Error: division by zero")
        return None
    else:
        print("Division successful")
        return result
    finally:
        print("Divide operation finished")

divide(10, 2)
# Division successful
# Divide operation finished

divide(10, 0)
# Error: division by zero
# Divide operation finished
```

---

## 6. Common Built-in Exceptions

| Exception | When it happens |
|-----------|------------------|
| `ValueError` | Invalid value (e.g., `int("abc")`) |
| `TypeError` | Wrong type used (e.g., `"2" + 2`) |
| `IndexError` | List index out of range |
| `KeyError` | Dictionary key doesn't exist |
| `ZeroDivisionError` | Dividing by zero |
| `FileNotFoundError` | File doesn't exist |
| `AttributeError` | Object doesn't have that attribute/method |

### Beginner tip
Always catch **specific** exceptions first, and use a generic `except Exception` only as a last resort — catching everything blindly can hide real bugs.

---

## 7. Knowledge Check

1. What is the difference between the `else` and `finally` clauses in exception handling?
2. Write a `try`/`except` block that handles both `ValueError` and `ZeroDivisionError`.
3. Why is `finally` useful for closing files or releasing resources?
4. What's wrong with using a bare `except:` (no exception type) in most cases?

---

**Next:** [Custom Exceptions & Raising →](./01-Custom-Exceptions-and-Raising.md)
