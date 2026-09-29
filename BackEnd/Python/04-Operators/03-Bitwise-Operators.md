# 🧮 Bitwise Operators in Python

> **Trainer's Note:** Bitwise operators work on the individual binary bits of integers. They're less common in everyday beginner code but essential for low-level work, flags, and performance tricks.

---

## 📑 Table of Contents
1. [List of Bitwise Operators](#1-list-of-bitwise-operators)
2. [Binary Refresher](#2-binary-refresher)
3. [Examples](#3-examples)
4. [Practical Use Cases](#4-practical-use-cases)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. List of Bitwise Operators

| Operator | Name | Example |
|----------|------|---------|
| `&` | AND | `5 & 3` |
| `\|` | OR | `5 \| 3` |
| `^` | XOR | `5 ^ 3` |
| `~` | NOT (complement) | `~5` |
| `<<` | Left shift | `5 << 1` |
| `>>` | Right shift | `5 >> 1` |

### Real-world analogy
```
Bitwise operators = flipping individual light switches in a row
  each bit = one switch (0 = off, 1 = on)
```

---

## 2. Binary Refresher

```
5  = 0000 0101
3  = 0000 0011
```

Bitwise operations work on these binary representations, bit by bit.

```python
print(bin(5))   # '0b101'
print(bin(3))   # '0b11'
```

---

## 3. Examples

```python
a = 5    # 0101
b = 3    # 0011

print(a & b)   # 1   (0001) — AND: both bits must be 1
print(a | b)   # 7   (0111) — OR: either bit is 1
print(a ^ b)   # 6   (0110) — XOR: bits differ
print(~a)      # -6         — NOT: inverts all bits (two's complement)
print(a << 1)  # 10  (1010) — shift bits left (multiply by 2)
print(a >> 1)  # 2   (0010) — shift bits right (divide by 2)
```

### Shift as multiply/divide by powers of 2
```python
x = 4
print(x << 2)   # 16  (4 * 2^2)
print(x >> 1)   # 2   (4 / 2^1)
```

---

## 4. Practical Use Cases

| Use case | How bitwise helps |
|----------|--------------------|
| Permission flags | Combine flags with `\|`, check with `&` |
| Fast even/odd check | `n & 1 == 0` → even |
| Toggle a bit | `x ^= mask` |
| Low-level networking/graphics | Manipulate raw byte data |

```python
# Fast even/odd check
n = 10
if n & 1 == 0:
    print("Even")
else:
    print("Odd")
```

```python
# Combine permission flags
READ = 1     # 0001
WRITE = 2    # 0010
EXECUTE = 4  # 0100

permissions = READ | WRITE   # 0011 → 3
print(permissions & WRITE)   # 2 (truthy) → WRITE permission is set
print(permissions & EXECUTE) # 0 (falsy)  → EXECUTE not set
```

### Beginner note
For everyday application logic, you'll rarely need bitwise operators — but they're valuable to recognize when reading systems-level or optimized code.

---

## 5. Knowledge Check

1. What does `5 & 3` evaluate to?
2. What does the `<<` operator do?
3. Write a bitwise expression to check if a number `n` is odd.
4. Name one real use case for bitwise operators.

---

**Previous:** [← Relational Operators](./02-Relational-Operators.md)
**Next:** [Assignment Operators →](./04-Assignment-Operators.md)
