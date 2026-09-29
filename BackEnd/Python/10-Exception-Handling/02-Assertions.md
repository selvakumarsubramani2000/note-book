# ✅ Assertions in Python

> **Trainer's Note:** An `assert` statement is a quick sanity check — it says "I believe this condition is true; if it's not, stop immediately because something is fundamentally wrong."

---

## 📑 Table of Contents
1. [What is an Assertion?](#1-what-is-an-assertion)
2. [Basic `assert` Syntax](#2-basic-assert-syntax)
3. [Assertions with Custom Messages](#3-assertions-with-custom-messages)
4. [Assertions vs Exceptions](#4-assertions-vs-exceptions)
5. [When to Use (and Not Use) Assertions](#5-when-to-use-and-not-use-assertions)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. What is an Assertion?

### Real-world analogy
```
assert = a smoke detector for your code
  It's not meant to handle everyday problems (like user typos)
  It's meant to catch things that should NEVER happen if your code is correct
```

---

## 2. Basic `assert` Syntax

```python
assert condition
```

If `condition` is `False`, Python raises an `AssertionError` and stops.

```python
def calculate_average(numbers):
    assert len(numbers) > 0   # sanity check: list should never be empty here
    return sum(numbers) / len(numbers)

print(calculate_average([10, 20, 30]))   # 20.0
print(calculate_average([]))             # ❌ AssertionError
```

---

## 3. Assertions with Custom Messages

```python
def calculate_average(numbers):
    assert len(numbers) > 0, "The list of numbers must not be empty"
    return sum(numbers) / len(numbers)

calculate_average([])
# AssertionError: The list of numbers must not be empty
```

```python
def set_discount(percent):
    assert 0 <= percent <= 100, f"Invalid discount: {percent}"
    print(f"Discount set to {percent}%")

set_discount(50)    # Discount set to 50%
set_discount(150)   # ❌ AssertionError: Invalid discount: 150
```

---

## 4. Assertions vs Exceptions

| Aspect | `assert` | `raise` / `try-except` |
|--------|----------|------------------------|
| Purpose | Catch **programmer bugs** / impossible states | Handle **expected** runtime problems (bad input, missing file) |
| Can be disabled | Yes — skipped when Python runs with `-O` (optimize) flag | No — always active |
| Typical use | Internal checks, debugging | User input validation, file/network errors |

```python
# Good use of assert: internal invariant that should always hold
def get_grade(score):
    assert isinstance(score, (int, float)), "score must be a number"
    if score >= 90:
        return "A"
    return "B"

# Better handled with exceptions: expected, recoverable user input error
def get_age_from_input(user_input):
    try:
        age = int(user_input)
    except ValueError:
        raise ValueError("Please enter a valid number for age")
    return age
```

---

## 5. When to Use (and Not Use) Assertions

**Use assertions for:**
- Checking internal assumptions during development ("this should never be negative here")
- Validating function preconditions/postconditions while debugging
- Writing quick sanity checks in tests

**Avoid assertions for:**
- Validating user input (use `if`/`raise` instead — assertions can be disabled in production with `python -O`)
- Anything your program *must* enforce no matter what

```python
# ❌ Risky: don't rely on assert for critical business logic
def withdraw(balance, amount):
    assert amount <= balance   # this check could be skipped with -O!
    return balance - amount

# ✅ Better: use a real exception for critical checks
def withdraw(balance, amount):
    if amount > balance:
        raise ValueError("Insufficient funds")
    return balance - amount
```

### Beginner tip
Think of `assert` as a debugging tool you leave in your code to catch bugs early, not as a replacement for proper input validation or error handling.

---

## 6. Knowledge Check

1. What happens when an `assert` statement's condition evaluates to `False`?
2. Why should assertions not be used to validate user input?
3. What command-line flag can disable all assertions in Python, and what risk does that create?
4. Write an assertion that checks a variable `temperature` is between -50 and 50 (inclusive), with a helpful error message.

---

**Previous:** [← Custom Exceptions & Raising](./01-Custom-Exceptions-and-Raising.md)

🎉 **Exception Handling track complete!** You've learned try/except/finally, custom exceptions, raising exceptions, and assertions.
