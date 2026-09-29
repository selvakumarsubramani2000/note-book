# ⏭️ Break, Continue, and Pass in Python

> **Trainer's Note:** These three keywords give you fine control over loop execution — stop early, skip an iteration, or do nothing at all (placeholder).

---

## 📑 Table of Contents
1. [`break` Statement](#1-break-statement)
2. [`continue` Statement](#2-continue-statement)
3. [`pass` Statement](#3-pass-statement)
4. [Combining with Loops](#4-combining-with-loops)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. `break` Statement

Immediately exits the loop entirely.

```python
for number in range(1, 10):
    if number == 5:
        break
    print(number)
```

**Output:**
```
1
2
3
4
```

### Real-world analogy
```
break = pulling the emergency stop cord on a train
  loop stops completely, no more iterations run
```

### Real use case: search and stop
```python
numbers = [4, 8, 15, 16, 23, 42]
target = 15

for num in numbers:
    if num == target:
        print("Found it!")
        break
```

---

## 2. `continue` Statement

Skips the rest of the current iteration and moves to the next one.

```python
for number in range(1, 6):
    if number == 3:
        continue
    print(number)
```

**Output:**
```
1
2
4
5
```

### Real-world analogy
```
continue = skipping one song on a playlist, then resuming
  the loop itself keeps going
```

### Real use case: skip invalid data
```python
scores = [85, -1, 90, -1, 78]

for score in scores:
    if score < 0:
        continue   # skip invalid entries
    print(f"Valid score: {score}")
```

---

## 3. `pass` Statement

Does nothing — a placeholder when a statement is syntactically required but no action is needed yet.

```python
for number in range(5):
    if number == 3:
        pass   # TODO: handle this case later
    print(number)
```

### Real-world analogy
```
pass = an empty placeholder box labeled "fill me in later"
```

### Common use: stub functions/classes
```python
def upcoming_feature():
    pass   # not implemented yet, but no syntax error

class Placeholder:
    pass
```

---

## 4. Combining with Loops

```python
for i in range(1, 11):
    if i % 2 == 0:
        continue        # skip even numbers
    if i > 7:
        break            # stop once i exceeds 7
    print(i)
```

**Output:**
```
1
3
5
7
```

### `else` clause on loops (bonus)
The `else` block runs only if the loop completes **without** hitting `break`:

```python
for number in [1, 3, 5, 7]:
    if number % 2 == 0:
        print("Found an even number!")
        break
else:
    print("No even numbers found")   # runs since break never triggered
```

---

## 5. Knowledge Check

1. What is the difference between `break` and `continue`?
2. When would you use `pass`?
3. Write a loop that prints numbers 1–10 but stops as soon as it hits 6.
4. What does the `else` clause on a `for` loop do?

---

**Previous:** [← Looping Statements](./01-Looping-Statements.md)

🎉 **Control Statements track complete!** You've covered Decisional Statements, Looping Statements, and Break/Continue/Pass.
