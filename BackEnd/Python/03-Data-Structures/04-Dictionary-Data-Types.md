# 📖 Dictionary Data Type in Python

> **Trainer's Note:** A dictionary stores data as **key-value pairs** — like a real dictionary where a word (key) maps to its meaning (value). Fast lookups by key.

---

## 📑 Table of Contents
1. [Creating Dictionaries](#1-creating-dictionaries)
2. [Accessing and Modifying](#2-accessing-and-modifying)
3. [Common Dictionary Methods](#3-common-dictionary-methods)
4. [Looping Through a Dictionary](#4-looping-through-a-dictionary)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Creating Dictionaries

```python
student = {
    "name": "Selva",
    "age": 30,
    "city": "Chennai"
}

empty_dict = {}
print(type(student))   # <class 'dict'>
```

### Real-world analogy
```
Dictionary = a real language dictionary
  key   = word   ("name")
  value = meaning ("Selva")
```

---

## 2. Accessing and Modifying

```python
student = {"name": "Selva", "age": 30}

print(student["name"])          # Selva
print(student.get("age"))       # 30
print(student.get("email", "N/A"))  # "N/A" — safe default if key missing

student["age"] = 31             # update existing key
student["city"] = "Chennai"     # add new key
print(student)

del student["city"]             # remove a key
```

### Key lookup safety
```python
# print(student["email"])  # ❌ KeyError if key doesn't exist
print(student.get("email"))  # ✅ returns None instead of crashing
```

---

## 3. Common Dictionary Methods

```python
student = {"name": "Selva", "age": 30, "city": "Chennai"}

print(student.keys())     # dict_keys(['name', 'age', 'city'])
print(student.values())   # dict_values(['Selva', 30, 'Chennai'])
print(student.items())    # dict_items([('name', 'Selva'), ...])

student.pop("age")        # removes key "age" and returns its value
student.update({"grade": "A", "age": 32})  # add/update multiple keys
print(len(student))        # number of key-value pairs
print("name" in student)   # True — checks keys, not values
```

### Dictionary comprehension
```python
squares = {x: x * x for x in range(1, 6)}
print(squares)   # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```

---

## 4. Looping Through a Dictionary

```python
student = {"name": "Selva", "age": 30, "city": "Chennai"}

for key in student:
    print(key, "->", student[key])

for key, value in student.items():
    print(f"{key}: {value}")
```

**Output:**
```
name -> Selva
age -> 30
city -> Chennai
name: Selva
age: 30
city: Chennai
```

---

## 5. Knowledge Check

1. What are the two parts of every dictionary entry?
2. What happens if you access a missing key with `[]` vs `.get()`?
3. Write code to loop through a dictionary printing key and value.
4. What does `student.items()` return?

---

**Previous:** [← Tuple Data Types](./03-Tuple-Data-Types.md)
**Next:** [Slicing →](./05-Slicing.md)
