# ⚙️ Installation & Environment Settings in Python

> **Trainer's Note:** Before writing any Python code, you need Python installed and a comfortable place (editor/IDE) to write it. This is a one-time setup.

---

## 📑 Table of Contents
1. [Installing Python](#1-installing-python)
2. [Verifying Installation](#2-verifying-installation)
3. [Choosing an Editor/IDE](#3-choosing-an-editoride)
4. [Virtual Environments](#4-virtual-environments)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Installing Python

### Windows
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download the latest **Python 3.x** installer
3. Run installer — **check "Add Python to PATH"** before clicking Install

### macOS
```bash
brew install python3
```

### Linux (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### Real-world analogy
```
Installing Python = installing a kitchen (stove + tools)
Writing scripts    = cooking recipes once the kitchen is ready
```

---

## 2. Verifying Installation

Open a terminal / command prompt and run:

```bash
python --version
```
or (on some systems):
```bash
python3 --version
```

Expected output (version may vary):
```
Python 3.12.0
```

Check `pip` (Python's package manager) too:
```bash
pip --version
```

If commands aren't recognized, revisit the PATH setting during installation.

---

## 3. Choosing an Editor/IDE

| Tool | Best for |
|------|----------|
| **VS Code** | Lightweight, extensions, most popular |
| **PyCharm** | Full-featured Python IDE |
| **Jupyter Notebook** | Data science, step-by-step experiments |
| **IDLE** | Comes bundled with Python, very basic |

### Recommended for beginners
- Install **VS Code**
- Add the **Python extension** (by Microsoft) for IntelliSense, debugging, linting

### Running a file in VS Code
```bash
python hello.py
```
Or use the built-in "Run Python File" button.

---

## 4. Virtual Environments

A **virtual environment** is an isolated Python setup per project, so package versions don't clash between projects.

### Real-world analogy
```
Global Python install = shared kitchen for the whole building
Virtual environment    = your own private kitchen for one recipe/project
```

### Create and use one
```bash
# Create
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install packages inside the venv
pip install requests

# Deactivate when done
deactivate
```

### Why it matters
- Avoids version conflicts between projects
- Keeps global Python installation clean
- Standard practice in real Python projects

---

## 5. Knowledge Check

1. Which command checks the installed Python version?
2. Name two popular Python code editors/IDEs.
3. Why do developers use virtual environments?
4. What command creates a virtual environment named `venv`?

---

**Previous:** [← Introduction to Python](./00-Introduction-to-Python.md)
**Next:** [Introduction to Shell →](./02-Introduction-to-Shell.md)
