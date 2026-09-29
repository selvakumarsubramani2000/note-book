# 🔁 Looping Statements in Python

> **Trainer's Note:** Loops repeat a block of code multiple times, so you don't have to write the same instructions over and over. Python has two loop types: `for` and `while`.

---

## 📑 Table of Contents
1. [The `for` Loop](#1-the-for-loop)
2. [The `while` Loop](#2-the-while-loop)
3. [Looping with `range()`](#3-looping-with-range)
4. [Nested Loops](#4-nested-loops)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. The `for` Loop

Used to iterate over a sequence (list, string, tuple, range, etc.)

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)
```

### Real-world analogy
```
for loop = going through a checklist item by item
  "for each item in the list, do this task"
```

### Looping over a string
```python
for letter in "Python":
    print(letter)
```

---

## 2. The `while` Loop

Repeats **while** a condition remains true.

```python
count = 1

while count <= 5:
    print(count)
    count += 1
```

**Output:**
```
1
2
3
4
5
```

### Real-world analogy
```
while loop = "keep pouring water while the glass isn't full"
```

### Beginner caution: infinite loops
```python
# ❌ Dangerous — condition never becomes False
# while True:
#     print("forever")

# ✅ Always ensure the condition changes / has an exit
count = 0
while count < 5:
    print(count)
    count += 1   # without this, infinite loop!
```

---

## 3. Looping with `range()`

```python
for i in range(5):        # 0, 1, 2, 3, 4
    print(i)

for i in range(2, 6):     # 2, 3, 4, 5
    print(i)

for i in range(0, 10, 2): # 0, 2, 4, 6, 8 (step of 2)
    print(i)

for i in range(5, 0, -1): # 5, 4, 3, 2, 1 (countdown)
    print(i)
```

---

## 4. Nested Loops

```python
for i in range(1, 4):
    for j in range(1, 3):
        print(f"i={i}, j={j}")
```

**Output:**
```
i=1, j=1
i=1, j=2
i=2, j=1
i=2, j=2
i=3, j=1
i=3, j=2
```

### Real use case: multiplication table
```python
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i} x {j} = {i*j}")
    print("---")
```

---

## 5. Knowledge Check

1. What is the difference between `for` and `while` loops?
2. What does `range(2, 10, 2)` generate?
3. Write a `while` loop that counts down from 10 to 1.
4. What's the danger of forgetting to update a loop's condition variable?

---

**Previous:** [← Decisional Statements](./00-Decisional-Statements.md)
**Next:** [Break, Continue, and Pass →](./02-Break-Continue-Pass.md)
