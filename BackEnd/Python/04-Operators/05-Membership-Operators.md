# 🔍 Membership Operators in Python

> **Trainer's Note:** Membership operators (`in`, `not in`) check whether a value exists inside a collection — string, list, tuple, set, or dictionary keys.

---

## 📑 Table of Contents
1. [List of Membership Operators](#1-list-of-membership-operators)
2. [Examples with Different Collections](#2-examples-with-different-collections)
3. [Practical Use Cases](#3-practical-use-cases)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. List of Membership Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `in` | True if value exists in the collection | `"a" in "cat"` → `True` |
| `not in` | True if value does NOT exist | `"z" not in "cat"` → `True` |

### Real-world analogy
```
in     = checking if a name is on the guest list
not in = checking if a name is NOT on the guest list
```

---

## 2. Examples with Different Collections

### String
```python
text = "Hello Python"
print("Python" in text)      # True
print("Java" not in text)    # True
```

### List
```python
fruits = ["apple", "banana", "cherry"]
print("banana" in fruits)     # True
print("mango" in fruits)      # False
```

### Tuple
```python
colors = ("red", "green", "blue")
print("green" in colors)      # True
```

### Set
```python
numbers = {1, 2, 3, 4}
print(3 in numbers)           # True (very fast lookup)
```

### Dictionary (checks keys by default)
```python
student = {"name": "Selva", "age": 30}
print("name" in student)        # True (checks keys)
print("Selva" in student)       # False (not checking values)
print("Selva" in student.values())  # True — check values explicitly
```

---

## 3. Practical Use Cases

### Validating user input
```python
valid_roles = ["admin", "user", "guest"]
role = "manager"

if role not in valid_roles:
    print("Invalid role!")
else:
    print("Role accepted")
```

### Avoiding duplicate entries
```python
cart = ["pen", "book"]
item = "pen"

if item not in cart:
    cart.append(item)
print(cart)   # ['pen', 'book'] — no duplicate added
```

### Searching characters
```python
password = "MyP@ssw0rd"
has_special = "@" in password
print(has_special)   # True
```

---

## 4. Knowledge Check

1. What does `"x" in "text"` check?
2. Write code to check if `"apple"` is NOT in a list `fruits`.
3. Does `in` on a dictionary check keys or values by default?
4. How would you check if a value exists among a dictionary's values?

---

**Previous:** [← Assignment Operators](./04-Assignment-Operators.md)
**Next:** [Identity Operators →](./06-Identity-Operators.md)
