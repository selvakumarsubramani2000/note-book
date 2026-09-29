# 🖨️ Print Statements in Python

> **Trainer's Note:** `print()` is how your program talks back to the user. It's one of the first functions every beginner learns — but it has many useful options beyond just printing text.

---

## 📑 Table of Contents
1. [Basic Printing](#1-basic-printing)
2. [`sep` and `end` Parameters](#2-sep-and-end-parameters)
3. [String Formatting in Print](#3-string-formatting-in-print)
4. [Printing Special Characters](#4-printing-special-characters)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Basic Printing

```python
print("Hello, World!")
print(42)
print(3.14)
print(True)

name = "Selva"
age = 30
print(name, age)   # multiple values, separated by a space by default
```

### Real-world analogy
```
print() = a megaphone your program uses to announce information
```

---

## 2. `sep` and `end` Parameters

```python
print("apple", "banana", "cherry", sep=", ")
# Output: apple, banana, cherry

print("Hello", end=" ")
print("World")
# Output: Hello World   (both on same line, because end=" " replaces the default newline)

for i in range(5):
    print(i, end=" ")
# Output: 0 1 2 3 4
```

### Default behavior
```python
print("A")   # end="\n" by default → moves to next line
print("B")
# Output:
# A
# B
```

---

## 3. String Formatting in Print

### f-strings (recommended, Python 3.6+)
```python
name = "Selva"
age = 30
print(f"My name is {name} and I am {age} years old.")

price = 49.999
print(f"Price: ${price:.2f}")   # Price: $50.00 (2 decimal places)
```

### `.format()` method
```python
print("My name is {} and I am {} years old.".format(name, age))
print("{0} is {1} - again {0}".format(name, age))   # reuse by index
```

### Old-style `%` formatting (still seen in legacy code)
```python
print("My name is %s and I am %d years old." % (name, age))
```

---

## 4. Printing Special Characters

```python
print("Line1\nLine2")     # \n = newline
print("Col1\tCol2")       # \t = tab
print("She said \"Hi\"")  # \" = escaped quote
print('It\'s Python')     # \' = escaped apostrophe
print("C:\\Users\\Selva") # \\ = literal backslash

# Raw string (ignores escape sequences) — useful for file paths/regex
print(r"C:\Users\Selva")   # prints exactly: C:\Users\Selva
```

### Printing a table-like layout
```python
print(f"{'Name':<10}{'Age':<5}")
print(f"{'Selva':<10}{30:<5}")
```

**Output:**
```
Name      Age  
Selva     30   
```

---

## 5. Knowledge Check

1. What does `sep=", "` do in a `print()` call?
2. Write a print statement that keeps output on the same line instead of a new line.
3. Format a float `price = 12.3456` to show only 2 decimal places using an f-string.
4. What does the escape sequence `\t` do?

---

**Previous:** [← Input Statements](./00-Input-Statements.md)

🎉 **IO-Statements track complete!** You now know how to take input from users and display formatted output.
