# 🔀 Logical Operators in Python

> **Trainer's Note:** Logical operators combine boolean expressions. Python spells them out as words (`and`, `or`, `not`) instead of symbols like `&&`, `||`, `!`.

---

## 📑 Table of Contents
1. [List of Logical Operators](#1-list-of-logical-operators)
2. [Truth Tables](#2-truth-tables)
3. [Examples](#3-examples)
4. [Short-Circuit Evaluation](#4-short-circuit-evaluation)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. List of Logical Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `and` | True if **both** are true | `True and False` → `False` |
| `or` | True if **at least one** is true | `True or False` → `True` |
| `not` | Reverses the boolean value | `not True` → `False` |

### Real-world analogy
```
and = both switches must be ON for the light to turn on
or  = at least one switch ON turns the light on
not = flip the switch state
```

---

## 2. Truth Tables

### `and`
| A | B | A and B |
|---|---|---------|
| True | True | True |
| True | False | False |
| False | True | False |
| False | False | False |

### `or`
| A | B | A or B |
|---|---|--------|
| True | True | True |
| True | False | True |
| False | True | True |
| False | False | False |

### `not`
| A | not A |
|---|-------|
| True | False |
| False | True |

---

## 3. Examples

```python
age = 25
has_id = True

if age >= 18 and has_id:
    print("Entry allowed")

is_weekend = False
is_holiday = True

if is_weekend or is_holiday:
    print("No work today")

logged_in = False
if not logged_in:
    print("Please log in")
```

### Combining with comparisons
```python
score = 85

if score >= 90 and score <= 100:
    print("Grade A")
elif score >= 75 and score < 90:
    print("Grade B")
else:
    print("Needs improvement")
```

---

## 4. Short-Circuit Evaluation

Python stops evaluating as soon as the result is determined:

```python
def check():
    print("check() called")
    return True

# 'and' stops early if first is False
result = False and check()   # check() NOT called
print(result)   # False

# 'or' stops early if first is True
result = True or check()     # check() NOT called
print(result)   # True
```

### Practical use: avoid errors
```python
data = None

if data is not None and data["key"] == "value":
    print("Safe access")
# If data were None, checking data["key"] first would crash.
# 'and' short-circuits so the second check is skipped.
```

---

## 5. Knowledge Check

1. What does `True and False` evaluate to?
2. What does `not False` evaluate to?
3. Explain short-circuit evaluation with `or`.
4. Write an `if` condition to check `age` is between 18 and 60 (inclusive).

---

**Previous:** [← Arithmetic Operators](./00-Arithmetic-Operators.md)
**Next:** [Relational Operators →](./02-Relational-Operators.md)
