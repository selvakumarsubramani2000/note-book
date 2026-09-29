# ⚖️ Relational (Comparison) Operators in Python

> **Trainer's Note:** Relational operators compare two values and always produce a boolean (`True`/`False`) result. They're the backbone of `if` conditions and loops.

---

## 📑 Table of Contents
1. [List of Relational Operators](#1-list-of-relational-operators)
2. [Examples](#2-examples)
3. [Chained Comparisons](#3-chained-comparisons)
4. [Comparing Different Types](#4-comparing-different-types)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. List of Relational Operators

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `==` | Equal to | `5 == 5` | `True` |
| `!=` | Not equal to | `5 != 3` | `True` |
| `>` | Greater than | `5 > 3` | `True` |
| `<` | Less than | `5 < 3` | `False` |
| `>=` | Greater than or equal | `5 >= 5` | `True` |
| `<=` | Less than or equal | `5 <= 4` | `False` |

### Real-world analogy
```
Relational operators = a weighing scale
  == balanced exactly
  >  left side heavier
  <  right side heavier
```

---

## 2. Examples

```python
a = 10
b = 20

print(a == b)   # False
print(a != b)   # True
print(a > b)    # False
print(a < b)    # True
print(a >= 10)  # True
print(b <= 20)  # True
```

### Common `if` usage
```python
age = 20

if age >= 18:
    print("Adult")
else:
    print("Minor")
```

### Comparing strings (alphabetical / lexicographic)
```python
print("apple" == "apple")   # True
print("apple" < "banana")   # True (a comes before b)
print("Apple" == "apple")   # False (case-sensitive)
```

---

## 3. Chained Comparisons

Python allows a neat shorthand for range checks:

```python
age = 25

# Instead of: age >= 18 and age <= 60
if 18 <= age <= 60:
    print("Working age")
```

```python
x = 5
print(1 < x < 10)   # True — equivalent to (1 < x) and (x < 10)
```

---

## 4. Comparing Different Types

```python
print(5 == 5.0)     # True — numeric types compare by value
print(5 == "5")      # False — different types (int vs str) never equal
# print(5 < "5")      # ❌ TypeError in Python 3 — can't compare int and str
```

### Beginner tip
Always ensure you're comparing compatible types. Convert first if needed:
```python
user_input = "18"
if int(user_input) >= 18:
    print("Adult")
```

---

## 5. Knowledge Check

1. What does `5 != 3` return?
2. Write a chained comparison to check if `x` is between 1 and 100.
3. Does `5 == "5"` evaluate to True or False in Python?
4. What symbol checks "greater than or equal to"?

---

**Previous:** [← Logical Operators](./01-Logical-Operators.md)
**Next:** [Bitwise Operators →](./03-Bitwise-Operators.md)
