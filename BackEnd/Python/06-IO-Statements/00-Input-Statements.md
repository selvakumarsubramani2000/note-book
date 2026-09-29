# ⌨️ Input Statements in Python

> **Trainer's Note:** The `input()` function lets your program pause and ask the user to type something — it's how programs become interactive instead of just running fixed code.

---

## 📑 Table of Contents
1. [The `input()` Function](#1-the-input-function)
2. [Input Always Returns a String](#2-input-always-returns-a-string)
3. [Type Conversion with Input](#3-type-conversion-with-input)
4. [Taking Multiple Inputs](#4-taking-multiple-inputs)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. The `input()` Function

```python
name = input("Enter your name: ")
print("Hello,", name)
```

**How it works:**
```
1. Program pauses and shows the prompt "Enter your name: "
2. User types something and presses Enter
3. Whatever was typed is stored in the 'name' variable
```

### Real-world analogy
```
input() = a form asking you a question and waiting for your answer
  before moving to the next step
```

---

## 2. Input Always Returns a String

This is the #1 beginner trap in Python — `input()` **always** gives back a string, even if the user types a number.

```python
age = input("Enter your age: ")
print(type(age))   # <class 'str'>  — even if user typed "25"

# age + 5   # ❌ TypeError: can only concatenate str (not "int") to str
```

---

## 3. Type Conversion with Input

Convert the string to the type you actually need:

```python
age = int(input("Enter your age: "))
print(age + 5)   # works now — age is an int

price = float(input("Enter price: "))
print(price * 1.18)   # add 18% tax
```

### Handling invalid input safely
```python
try:
    age = int(input("Enter your age: "))
    print(f"Next year you'll be {age + 1}")
except ValueError:
    print("Please enter a valid number!")
```

---

## 4. Taking Multiple Inputs

### Using `split()` for multiple values on one line
```python
data = input("Enter name and age separated by space: ")
name, age = data.split()
print(name, age)
```

```python
# Example run:
# Input: "Selva 30"
# name = "Selva", age = "30" (still strings!)
```

### Converting multiple numeric inputs
```python
x, y = input("Enter two numbers separated by space: ").split()
x = int(x)
y = int(y)
print(x + y)

# Shorter, common idiom:
x, y = map(int, input("Enter two numbers: ").split())
print(x + y)
```

### Taking a list of numbers
```python
numbers = list(map(int, input("Enter numbers separated by space: ").split()))
print(numbers)          # e.g. [1, 2, 3, 4]
print(sum(numbers))     # sum of all entered numbers
```

---

## 5. Knowledge Check

1. What data type does `input()` always return?
2. Write code to read an integer age from the user safely.
3. How do you read two numbers on the same line and convert both to `int`?
4. What error occurs if you try to add a string and an integer directly?

---

**Next:** [Print Statements →](./01-Print-Statements.md)
