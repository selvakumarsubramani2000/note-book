# 🔤 String Data Type in Python

> **Trainer's Note:** Strings hold text data. Python strings are immutable — once created, their content can't change in place; operations return new strings.

---

## 📑 Table of Contents
1. [Creating Strings](#1-creating-strings)
2. [String Immutability](#2-string-immutability)
3. [Common String Methods](#3-common-string-methods)
4. [String Formatting](#4-string-formatting)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Creating Strings

```python
s1 = 'Hello'
s2 = "World"
s3 = '''Triple quoted
multi-line string'''
s4 = str(123)   # "123"
```

### Real-world analogy
```
String = a sentence written on paper
  you can read it, copy it, combine it
  but you cannot edit one letter directly on the original paper
```

---

## 2. String Immutability

```python
name = "Selva"
# name[0] = "K"     # ❌ TypeError: strings are immutable

name = "K" + name[1:]   # ✅ create a new string
print(name)              # "Kelva"
```

Every "modifying" operation actually returns a **new** string object.

---

## 3. Common String Methods

```python
text = "  Hello Python World  "

print(text.strip())          # "Hello Python World" (removes whitespace)
print(text.lower())          # "  hello python world  "
print(text.upper())          # "  HELLO PYTHON WORLD  "
print(text.replace("Python", "C#"))  # "  Hello C# World  "
print(text.split())          # ['Hello', 'Python', 'World']
print("-".join(["a", "b", "c"]))     # "a-b-c"
print(text.strip().startswith("Hello"))  # True
print(text.strip().endswith("World"))    # True
print("Python" in text)      # True
print(text.find("Python"))   # index position
print(len(text))             # length including spaces
```

### Indexing and length
```python
word = "Python"
print(word[0])     # P
print(word[-1])    # n (last character)
print(len(word))   # 6
```

---

## 4. String Formatting

### f-strings (recommended, Python 3.6+)
```python
name = "Anu"
age = 30
print(f"{name} is {age} years old")
```

### `.format()` method
```python
print("{} is {} years old".format(name, age))
```

### `%` operator (older style)
```python
print("%s is %d years old" % (name, age))
```

### Escape characters
```python
print("Line1\nLine2")   # newline
print("Tab\tSpace")     # tab
print("She said \"Hi\"")  # escaped quotes
```

---

## 5. Knowledge Check

1. Are Python strings mutable or immutable?
2. Write an f-string that prints a variable `city`.
3. What does `"hello".upper()` return?
4. How do you check if a substring exists in a string?

---

**Next:** [List Data Types →](./01-List-Data-Types.md)
