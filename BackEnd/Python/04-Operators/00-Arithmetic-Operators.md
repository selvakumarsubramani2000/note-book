# ➕ Arithmetic Operators in Python

> **Trainer's Note:** Arithmetic operators perform basic math. Python adds two useful ones beyond most languages: `//` (floor division) and `**` (power).

---

## 📑 Table of Contents
1. [List of Arithmetic Operators](#1-list-of-arithmetic-operators)
2. [Examples](#2-examples)
3. [Operator Precedence](#3-operator-precedence)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. List of Arithmetic Operators

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `+` | Addition | `5 + 3` | `8` |
| `-` | Subtraction | `5 - 3` | `2` |
| `*` | Multiplication | `5 * 3` | `15` |
| `/` | True Division | `5 / 2` | `2.5` |
| `//` | Floor Division | `5 // 2` | `2` |
| `%` | Modulus (remainder) | `5 % 2` | `1` |
| `**` | Exponentiation (power) | `5 ** 2` | `25` |

### Real-world analogy
```
/  = sharing 5 candies among 2 people evenly (with fraction leftover)
// = sharing 5 candies among 2 people, keep only whole candies each
%  = the candy left over after even sharing
```

---

## 2. Examples

```python
a = 10
b = 3

print(a + b)   # 13
print(a - b)   # 7
print(a * b)   # 30
print(a / b)   # 3.3333333333333335
print(a // b)  # 3
print(a % b)   # 1
print(a ** b)  # 1000
```

### Real use case: check even/odd
```python
number = 7
if number % 2 == 0:
    print("Even")
else:
    print("Odd")
```

### Real use case: average with floor division
```python
total_items = 17
per_box = 5
full_boxes = total_items // per_box   # 3 full boxes
leftover = total_items % per_box      # 2 leftover items
print(full_boxes, leftover)
```

---

## 3. Operator Precedence

Python follows standard math precedence (like PEMDAS):

```
1. ** (highest)
2. * / // %
3. + - (lowest)
```

```python
result = 2 + 3 * 4        # 14 (multiplication first)
result2 = (2 + 3) * 4     # 20 (parentheses override precedence)
result3 = 2 ** 3 ** 2     # 512 (right to left: 2 ** (3 ** 2))
```

### Beginner tip
When unsure, use parentheses `()` to make the intended order explicit — clearer for readers too.

---

## 4. Knowledge Check

1. What does `17 // 5` return?
2. What does `17 % 5` return?
3. What is the result of `2 ** 3`?
4. Which operator has higher precedence: `*` or `+`?

---

**Next:** [Logical Operators →](./01-Logical-Operators.md)
