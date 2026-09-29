# 🔑 Keywords in Python

> **Trainer's Note:** Keywords are reserved words with special meaning to Python. You cannot use them as variable, function, or class names.

---

## 📑 Table of Contents
1. [What are Keywords?](#1-what-are-keywords)
2. [List of Python Keywords](#2-list-of-python-keywords)
3. [Viewing Keywords Programmatically](#3-viewing-keywords-programmatically)
4. [Common Mistakes](#4-common-mistakes)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What are Keywords?

**Keywords** are words that already have a fixed meaning built into the Python language.

### Real-world analogy
```
Keywords = reserved parking spots
  labeled "if", "for", "class" etc.
  you cannot park (name) your own variable there
```

Python has around 35 keywords (count varies slightly per version).

---

## 2. List of Python Keywords

| Category | Keywords |
|----------|----------|
| Value keywords | `True`, `False`, `None` |
| Logical | `and`, `or`, `not`, `is`, `in` |
| Control flow | `if`, `elif`, `else`, `for`, `while`, `break`, `continue`, `pass` |
| Functions/classes | `def`, `return`, `class`, `lambda`, `yield` |
| Exception handling | `try`, `except`, `finally`, `raise` |
| Import | `import`, `from`, `as` |
| Scope | `global`, `nonlocal` |
| Async | `async`, `await` |
| Other | `del`, `with`, `assert`, `class`, `self` (not a keyword, but conventional)|

### Examples in context
```python
if True:
    pass          # placeholder, does nothing

for i in range(3):
    print(i)

def greet():
    return "Hello"
```

---

## 3. Viewing Keywords Programmatically

```python
import keyword

print(keyword.kwlist)
print(len(keyword.kwlist))

print(keyword.iskeyword("class"))   # True
print(keyword.iskeyword("data"))    # False
```

This is handy when you're unsure whether a word is safe to use as a variable name.

---

## 4. Common Mistakes

```python
class = "Python101"   # ❌ SyntaxError: 'class' is a keyword
```

```python
class_name = "Python101"   # ✅ valid — just add a suffix/prefix
```

| Mistake | Fix |
|---------|-----|
| `for = 5` | use `for_count = 5` |
| `type = "admin"` | use `user_type = "admin"` (note: `type` is a built-in, not a keyword, but still risky to override) |

### Beginner tip
Built-in function/type names (like `list`, `str`, `type`) are **not keywords**, but overriding them (e.g., `list = [1,2,3]`) shadows the built-in and can cause confusing bugs. Avoid it.

---

## 5. Knowledge Check

1. What is a Python keyword?
2. How do you list all Python keywords programmatically?
3. Is `data` a valid variable name? Is `class`?
4. Name three control-flow keywords.

---

**Previous:** [← Variables](./00-Variables.md)
**Next:** [Data Types →](./02-Data-Types.md)
