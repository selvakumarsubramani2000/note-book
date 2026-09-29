# 🖥️ Introduction to Shell (Python Interactive Shell)

> **Trainer's Note:** The Python Shell (also called REPL) lets you type Python code and see results instantly — perfect for quick experiments and learning.

---

## 📑 Table of Contents
1. [What is the Python Shell?](#1-what-is-the-python-shell)
2. [Opening the Shell](#2-opening-the-shell)
3. [Using the Shell](#3-using-the-shell)
4. [Shell vs Script File](#4-shell-vs-script-file)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is the Python Shell?

**REPL** = **R**ead **E**valuate **P**rint **L**oop.

You type one line of Python, press Enter, and see the result immediately — no need to save a file and run it separately.

### Real-world analogy
```
Shell        = calculator: type an expression, get instant answer
Script file  = a full recipe you follow start to finish, saved for later
```

---

## 2. Opening the Shell

### Windows / macOS / Linux terminal
```bash
python
```
or
```bash
python3
```

You will see something like:
```
Python 3.12.0 (main, ...)
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

The `>>>` is the **prompt** where you type code.

### Exit the shell
```python
exit()
```
or press `Ctrl + Z` then Enter (Windows) / `Ctrl + D` (macOS/Linux).

---

## 3. Using the Shell

### Simple expressions
```python
>>> 2 + 3
5
>>> "Hello" + " " + "World"
'Hello World'
```

### Variables persist during the session
```python
>>> x = 10
>>> y = 20
>>> x + y
30
```

### Multi-line blocks
```python
>>> if x > 5:
...     print("x is greater than 5")
...
x is greater than 5
```

The `...` prompt means Python is waiting for more lines of an indented block.

### Getting help
```python
>>> help(str)
```

---

## 4. Shell vs Script File

| Aspect | Shell (REPL) | Script File (`.py`) |
|--------|--------------|----------------------|
| Best for | Quick tests, learning | Real programs, reusable code |
| Saves code? | No (unless you copy it) | Yes, saved to disk |
| Runs line-by-line | Yes, immediately | Runs the whole file at once |
| Typical use | Try out a function quickly | Build actual applications |

### Beginner workflow
```
1) Use shell to experiment with small syntax questions
2) Once confident, write the real logic in a .py file
3) Run the file with: python filename.py
```

---

## 5. Knowledge Check

1. What does REPL stand for?
2. How do you start the Python interactive shell?
3. How do you exit the Python shell?
4. When would you prefer a script file over the shell?

---

**Previous:** [← Installation & Environment Settings](./01-Installation-and-Environment-Settings.md)

🎉 **Introduction track complete!** You now know what Python is, how to install it, and how to use the interactive shell.
