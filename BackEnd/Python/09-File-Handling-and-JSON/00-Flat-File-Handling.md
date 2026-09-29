# 📄 Flat File Handling in Python

> **Trainer's Note:** A "flat file" is a plain text file (like `.txt` or `.csv`). Python lets you read from and write to these files easily using the built-in `open()` function.

---

## 📑 Table of Contents
1. [Opening a File](#1-opening-a-file)
2. [File Modes](#2-file-modes)
3. [Reading Files](#3-reading-files)
4. [Writing Files](#4-writing-files)
5. [The `with` Statement (Best Practice)](#5-the-with-statement-best-practice)
6. [Working with CSV Files](#6-working-with-csv-files)
7. [Knowledge Check](#7-knowledge-check)

---

## 1. Opening a File

```python
file = open("notes.txt", "r")   # open in read mode
print(file.read())
file.close()   # always close when done
```

### Real-world analogy
```
Opening a file = opening a notebook
Reading  = reading the pages
Writing  = writing new pages
Closing  = closing the notebook so others can use it too
```

---

## 2. File Modes

| Mode | Meaning |
|------|---------|
| `"r"` | Read (default) — file must exist |
| `"w"` | Write — creates file, **overwrites** if it exists |
| `"a"` | Append — adds to the end of the file |
| `"x"` | Create — fails if file already exists |
| `"r+"` | Read and write |

---

## 3. Reading Files

```python
with open("notes.txt", "r") as f:
    content = f.read()        # whole file as one string
    print(content)

with open("notes.txt", "r") as f:
    lines = f.readlines()     # list of lines
    print(lines)

with open("notes.txt", "r") as f:
    for line in f:            # loop line by line (memory efficient)
        print(line.strip())
```

---

## 4. Writing Files

```python
with open("notes.txt", "w") as f:
    f.write("Hello, Python!\n")
    f.write("This overwrites the old content.\n")

with open("notes.txt", "a") as f:
    f.write("This line gets appended.\n")   # doesn't erase old content
```

---

## 5. The `with` Statement (Best Practice)

`with` automatically closes the file for you, even if an error occurs.

```python
# Without 'with' -> must remember to close manually
f = open("notes.txt", "r")
data = f.read()
f.close()   # easy to forget!

# With 'with' -> file closes automatically
with open("notes.txt", "r") as f:
    data = f.read()
# file is already closed here
```

### Beginner tip
Always prefer `with open(...) as f:` over manual `open()`/`close()` — it's safer and cleaner.

---

## 6. Working with CSV Files

```python
import csv

# Writing a CSV file
with open("students.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Score"])
    writer.writerow(["Asha", 90])
    writer.writerow(["Ravi", 85])

# Reading a CSV file
with open("students.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
# ['Name', 'Score']
# ['Asha', '90']
# ['Ravi', '85']
```

---

## 7. Knowledge Check

1. What's the difference between `"w"` mode and `"a"` mode?
2. Why is `with open(...) as f:` preferred over manual `open()`/`close()`?
3. How would you read a file line by line instead of loading it all at once?
4. Write code to write a list of names to a text file, one name per line.

---

**Next:** [JSON Handling →](./01-JSON-Handling.md)
