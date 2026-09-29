# 📝 Assignment Operators in Python

> **Trainer's Note:** Assignment operators store values into variables. Python has a compact "combine and assign" shorthand for arithmetic and bitwise updates.

---

## 📑 Table of Contents
1. [Basic Assignment](#1-basic-assignment)
2. [Compound Assignment Operators](#2-compound-assignment-operators)
3. [Examples](#3-examples)
4. [Walrus Operator (Bonus)](#4-walrus-operator-bonus)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Basic Assignment

```python
x = 10   # assigns 10 to x
```

### Real-world analogy
```
Assignment = writing a value onto a labeled sticky note
  x = 10  →  sticky note "x" now shows 10
```

---

## 2. Compound Assignment Operators

| Operator | Equivalent to | Example |
|----------|----------------|---------|
| `+=` | `x = x + y` | `x += 5` |
| `-=` | `x = x - y` | `x -= 5` |
| `*=` | `x = x * y` | `x *= 5` |
| `/=` | `x = x / y` | `x /= 5` |
| `//=` | `x = x // y` | `x //= 5` |
| `%=` | `x = x % y` | `x %= 5` |
| `**=` | `x = x ** y` | `x **= 2` |
| `&=` | `x = x & y` | `x &= 3` |
| `\|=` | `x = x \| y` | `x \|= 3` |
| `^=` | `x = x ^ y` | `x ^= 3` |
| `<<=` | `x = x << y` | `x <<= 1` |
| `>>=` | `x = x >> y` | `x >>= 1` |

---

## 3. Examples

```python
x = 10

x += 5     # x = 15
x -= 3     # x = 12
x *= 2     # x = 24
x //= 5    # x = 4
x **= 2    # x = 16
print(x)   # 16
```

### Real use case: running total
```python
total = 0
prices = [100, 250, 75]

for price in prices:
    total += price     # same as: total = total + price

print(total)   # 425
```

### Real use case: countdown
```python
count = 5
while count > 0:
    print(count)
    count -= 1
print("Liftoff!")
```

---

## 4. Walrus Operator (Bonus)

Python 3.8+ introduced `:=`, the **walrus operator**, which assigns a value *and* returns it in the same expression:

```python
# Without walrus
data = input("Enter something: ")
if data:
    print(f"You entered: {data}")

# With walrus (assign + check in one line)
if (data := input("Enter something: ")):
    print(f"You entered: {data}")
```

Useful in loops to avoid calling a function twice:

```python
numbers = [1, 2, 3, 4, 5, 6]
results = [y for x in numbers if (y := x * 2) > 5]
print(results)   # [6, 8, 10, 12]
```

---

## 5. Knowledge Check

1. What does `x += 5` mean?
2. Rewrite `x = x * 3` using a compound assignment operator.
3. What does the walrus operator `:=` do?
4. Write code using `+=` to sum a list of numbers.

---

**Previous:** [← Bitwise Operators](./03-Bitwise-Operators.md)
**Next:** [Membership Operators →](./05-Membership-Operators.md)
