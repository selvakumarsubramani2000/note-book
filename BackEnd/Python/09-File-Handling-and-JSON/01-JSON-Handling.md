# 🔗 JSON Handling in Python

> **Trainer's Note:** JSON (JavaScript Object Notation) is a lightweight text format for exchanging data. Python's `json` module converts between Python objects and JSON text seamlessly.

---

## 📑 Table of Contents
1. [What is JSON?](#1-what-is-json)
2. [Python ↔ JSON Type Mapping](#2-python--json-type-mapping)
3. [Converting Python to JSON (`dumps`)](#3-converting-python-to-json-dumps)
4. [Converting JSON to Python (`loads`)](#4-converting-json-to-python-loads)
5. [Reading and Writing JSON Files](#5-reading-and-writing-json-files)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. What is JSON?

### Real-world analogy
```
JSON = a universal shipping label format
  Any system (Python, JavaScript, Java...) can read it
  because everyone agrees on the same simple structure
```

```json
{
  "name": "Asha",
  "age": 28,
  "is_student": false,
  "skills": ["Python", "SQL"]
}
```

---

## 2. Python ↔ JSON Type Mapping

| Python | JSON |
|--------|------|
| `dict` | object `{}` |
| `list`, `tuple` | array `[]` |
| `str` | string |
| `int`, `float` | number |
| `True` / `False` | `true` / `false` |
| `None` | `null` |

---

## 3. Converting Python to JSON (`dumps`)

`json.dumps()` converts a Python object into a **JSON string**.

```python
import json

person = {
    "name": "Asha",
    "age": 28,
    "is_student": False,
    "skills": ["Python", "SQL"]
}

json_string = json.dumps(person)
print(json_string)
print(type(json_string))   # <class 'str'>

# Pretty print
pretty = json.dumps(person, indent=4)
print(pretty)
```

---

## 4. Converting JSON to Python (`loads`)

`json.loads()` converts a **JSON string** back into a Python object.

```python
import json

json_string = '{"name": "Ravi", "age": 30, "skills": ["Java", "C#"]}'

data = json.loads(json_string)
print(type(data))     # <class 'dict'>
print(data["name"])   # Ravi
print(data["skills"]) # ['Java', 'C#']
```

---

## 5. Reading and Writing JSON Files

```python
import json

person = {"name": "Meena", "age": 24, "city": "Chennai"}

# Writing to a JSON file
with open("person.json", "w") as f:
    json.dump(person, f, indent=4)   # note: dump (no 's') -> writes to a file

# Reading from a JSON file
with open("person.json", "r") as f:
    loaded_data = json.load(f)       # note: load (no 's') -> reads from a file

print(loaded_data)
print(loaded_data["name"])   # Meena
```

### Quick reference: `s` vs no `s`
| Function | Works with |
|----------|-----------|
| `json.dumps()` | Python object → JSON **string** |
| `json.loads()` | JSON **string** → Python object |
| `json.dump()` | Python object → JSON **file** |
| `json.load()` | JSON **file** → Python object |

### Beginner tip
Think of the `s` as standing for "**s**tring." No `s` means you're working directly with a **file**.

---

## 6. Knowledge Check

1. What is the difference between `json.dumps()` and `json.dump()`?
2. What Python type does a JSON object (`{}`) become, and what type does a JSON array (`[]`) become?
3. Write code to convert a Python dictionary into a pretty-printed JSON string with 2-space indentation.
4. How would you read data from a file named `config.json` into a Python dictionary?

---

**Previous:** [← Flat File Handling](./00-Flat-File-Handling.md)
**Next:** [Pickle →](./02-Pickle.md)
