# 🚦 Decisional (Conditional) Statements in Python

> **Trainer's Note:** Decisional statements let your program choose different paths based on conditions — the "if this, then that" logic every program needs.

---

## 📑 Table of Contents
1. [The `if` Statement](#1-the-if-statement)
2. [`if...else`](#2-ifelse)
3. [`if...elif...else`](#3-ifelifelse)
4. [Nested and Ternary Conditions](#4-nested-and-ternary-conditions)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. The `if` Statement

```python
age = 20

if age >= 18:
    print("You are an adult")
```

### Real-world analogy
```
if = a decision gate
  condition true  → walk through the gate (run the block)
  condition false → gate stays closed (skip the block)
```

### Important: Indentation matters!
Python uses **indentation** (4 spaces is standard) instead of `{ }` to define blocks.

```python
if age >= 18:
    print("Adult")   # must be indented — part of the if block
print("Done")          # not indented — runs regardless
```

---

## 2. `if...else`

```python
age = 15

if age >= 18:
    print("Adult")
else:
    print("Minor")
```

**Output:**
```
Minor
```

---

## 3. `if...elif...else`

```python
marks = 72

if marks >= 90:
    print("Grade A")
elif marks >= 75:
    print("Grade B")
elif marks >= 60:
    print("Grade C")
else:
    print("Fail")
```

**Output:**
```
Grade C
```

`elif` is Python's version of "else if" — you can chain as many as needed.

---

## 4. Nested and Ternary Conditions

### Nested if
```python
age = 20
has_ticket = True

if age >= 18:
    if has_ticket:
        print("Entry allowed")
    else:
        print("Buy a ticket first")
else:
    print("Not old enough")
```

### Ternary (conditional expression) — one-line if/else
```python
age = 20
status = "Adult" if age >= 18 else "Minor"
print(status)   # Adult
```

### Real use case
```python
score = 45
result = "Pass" if score >= 40 else "Fail"
print(result)
```

---

## 5. Knowledge Check

1. What symbol does Python use instead of `{ }` to define an if-block?
2. Rewrite this using `elif`: check grade A (>=90), B (>=75), else Fail.
3. Write a ternary expression to assign "Even" or "Odd" based on a number.
4. What happens if the `if` block isn't indented correctly?

---

**Next:** [Looping Statements →](./01-Looping-Statements.md)
