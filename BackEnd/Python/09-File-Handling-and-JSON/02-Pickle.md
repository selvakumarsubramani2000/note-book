# 🥒 Pickle in Python

> **Trainer's Note:** Pickling is Python's way of converting *any* Python object (lists, dicts, custom classes...) into bytes so it can be saved to a file or sent elsewhere, and later restored exactly as it was.

---

## 📑 Table of Contents
1. [What is Pickling?](#1-what-is-pickling)
2. [Pickling (Saving) an Object](#2-pickling-saving-an-object)
3. [Unpickling (Loading) an Object](#3-unpickling-loading-an-object)
4. [Pickling Custom Objects](#4-pickling-custom-objects)
5. [Pickle vs JSON](#5-pickle-vs-json)
6. [Security Warning](#6-security-warning)
7. [Knowledge Check](#7-knowledge-check)

---

## 1. What is Pickling?

### Real-world analogy
```
Pickle = vacuum-sealing food to store it exactly as-is
  Pickling   = seal the object into bytes for storage
  Unpickling = open the seal and get the object back, unchanged
```

---

## 2. Pickling (Saving) an Object

```python
import pickle

data = {"name": "Asha", "scores": [90, 85, 88], "passed": True}

with open("data.pkl", "wb") as f:   # 'wb' = write binary
    pickle.dump(data, f)

print("Object pickled successfully!")
```

---

## 3. Unpickling (Loading) an Object

```python
import pickle

with open("data.pkl", "rb") as f:   # 'rb' = read binary
    loaded_data = pickle.load(f)

print(loaded_data)          # {'name': 'Asha', 'scores': [90, 85, 88], 'passed': True}
print(type(loaded_data))    # <class 'dict'> -> exact original type restored
```

---

## 4. Pickling Custom Objects

Pickle can even save **class instances**, not just built-in types like `dict` or `list`.

```python
import pickle

class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

student = Student("Ravi", "A")

# Save the object
with open("student.pkl", "wb") as f:
    pickle.dump(student, f)

# Load it back
with open("student.pkl", "rb") as f:
    loaded_student = pickle.load(f)

print(loaded_student.name, loaded_student.grade)   # Ravi A
```

---

## 5. Pickle vs JSON

| Aspect | Pickle | JSON |
|--------|--------|------|
| Format | Binary (not human-readable) | Text (human-readable) |
| Works with | Any Python object (classes, sets, etc.) | Only basic types (dict, list, str, number, bool, null) |
| Cross-language | Python only | Universal (any language) |
| Use case | Saving Python-specific data/state | Sharing data across systems |

### Beginner tip
Use **JSON** when data needs to be shared with other systems or languages. Use **Pickle** when you only need to save/restore Python objects for use within Python itself.

---

## 6. Security Warning

```
⚠️ Never unpickle data from an untrusted source!
   Pickle can execute arbitrary code during unpickling,
   which makes it a security risk if the file came from someone else.
```

```python
# Safe: only unpickle files YOU created and trust
with open("my_own_data.pkl", "rb") as f:
    data = pickle.load(f)   # ✅ safe, trusted source
```

---

## 7. Knowledge Check

1. What does "pickling" an object mean?
2. Why must files be opened in binary mode (`"wb"`/`"rb"`) when using pickle?
3. When would you choose Pickle over JSON, and vice versa?
4. Why is it risky to unpickle data from an untrusted source?

---

**Previous:** [← JSON Handling](./01-JSON-Handling.md)

🎉 **File Handling & JSON track complete!** You've learned flat file I/O, JSON serialization, and object pickling.
