# 🆔 Identity Operators in Python

> **Trainer's Note:** Identity operators (`is`, `is not`) check whether two variables point to the **same object in memory** — not just equal values. This is different from `==`.

---

## 📑 Table of Contents
1. [List of Identity Operators](#1-list-of-identity-operators)
2. [`is` vs `==`](#2-is-vs-)
3. [Examples](#3-examples)
4. [The Special Case of `None`](#4-the-special-case-of-none)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. List of Identity Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `is` | True if both refer to the same object | `a is b` |
| `is not` | True if they refer to different objects | `a is not b` |

### Real-world analogy
```
==  = "Do these two people have the same name?"
is  = "Are these two people literally the same person?"
```

---

## 2. `is` vs `==`

| Operator | Checks | Use for |
|----------|--------|---------|
| `==` | Value equality | Comparing content ("do they look the same?") |
| `is` | Identity (same memory location) | Checking if two references point to the same object |

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)   # True  — same values
print(a is b)   # False — different objects in memory
print(a is c)   # True  — c points to the same object as a
```

---

## 3. Examples

```python
x = 5
y = 5
print(x is y)    # True (small integers are cached/interned by Python)

list1 = [1, 2]
list2 = [1, 2]
print(list1 == list2)   # True  — same content
print(list1 is list2)   # False — different objects

list3 = list1
print(list1 is list3)   # True — same object reference
```

### Beginner caution about small integers/strings
```python
a = 256
b = 256
print(a is b)   # True (Python caches small ints, -5 to 256)

a = 1000
b = 1000
print(a is b)   # Often False (not guaranteed) — don't rely on this behavior!
```

**Rule of thumb:** Use `==` for comparing values. Only use `is` for identity checks (especially with `None`).

---

## 4. The Special Case of `None`

`None` is a singleton (only one `None` object exists), so always use `is` to compare against it:

```python
value = None

if value is None:        # ✅ correct, Pythonic way
    print("No value set")

if value == None:         # ⚠️ works, but not the recommended style
    print("No value set")
```

```python
if value is not None:
    print("Value exists:", value)
```

---

## 5. Knowledge Check

1. What is the difference between `==` and `is`?
2. Why might `a is b` be `False` even when `a == b` is `True`?
3. What is the recommended way to check if a variable is `None`?
4. If `c = a`, what does `a is c` return?

---

**Previous:** [← Membership Operators](./05-Membership-Operators.md)

🎉 **Operators track complete!** You've covered Arithmetic, Logical, Relational, Bitwise, Assignment, Membership, and Identity operators in Python.
