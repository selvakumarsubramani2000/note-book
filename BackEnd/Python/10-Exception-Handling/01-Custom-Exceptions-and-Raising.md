# 🎯 Custom Exceptions and Raising Exceptions

> **Trainer's Note:** Sometimes the built-in exceptions (`ValueError`, `TypeError`, etc.) aren't specific enough for your application. You can create your **own exception types** and trigger them intentionally with `raise`.

---

## 📑 Table of Contents
1. [The `raise` Keyword](#1-the-raise-keyword)
2. [Raising Built-in Exceptions](#2-raising-built-in-exceptions)
3. [Creating Custom Exceptions](#3-creating-custom-exceptions)
4. [Re-raising Exceptions](#4-re-raising-exceptions)
5. [Exception Chaining with `from`](#5-exception-chaining-with-from)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. The `raise` Keyword

`raise` lets you **trigger** an exception on purpose, instead of waiting for Python to raise one naturally.

```python
def set_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    print(f"Age set to {age}")

set_age(25)    # Age set to 25
set_age(-5)    # ❌ ValueError: Age cannot be negative
```

### Real-world analogy
```
raise = pulling the emergency brake yourself
  You decide something is wrong (invalid input, broken rule)
  and stop execution immediately, with a clear message
```

---

## 2. Raising Built-in Exceptions

You can raise any built-in exception with a custom message.

```python
def withdraw(balance, amount):
    if amount > balance:
        raise ValueError(f"Insufficient funds: balance is {balance}, tried to withdraw {amount}")
    return balance - amount

try:
    withdraw(100, 150)
except ValueError as e:
    print(f"Transaction failed: {e}")
```

---

## 3. Creating Custom Exceptions

Custom exceptions are classes that inherit from `Exception` (or a more specific built-in exception).

```python
class InsufficientFundsError(Exception):
    """Raised when a withdrawal exceeds the available balance."""
    pass

class InvalidAmountError(Exception):
    """Raised when a deposit/withdrawal amount is invalid."""
    pass

def withdraw(balance, amount):
    if amount <= 0:
        raise InvalidAmountError("Amount must be positive")
    if amount > balance:
        raise InsufficientFundsError(f"Cannot withdraw {amount}, balance is only {balance}")
    return balance - amount

try:
    withdraw(500, 1000)
except InsufficientFundsError as e:
    print(f"Error: {e}")
except InvalidAmountError as e:
    print(f"Error: {e}")
```

### Adding extra data to a custom exception
```python
class InsufficientFundsError(Exception):
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Cannot withdraw {amount}, balance is only {balance}")

try:
    raise InsufficientFundsError(100, 250)
except InsufficientFundsError as e:
    print(e)              # Cannot withdraw 250, balance is only 100
    print(e.balance)      # 100
    print(e.amount)       # 250
```

---

## 4. Re-raising Exceptions

Sometimes you want to log/handle an exception partially, then let it propagate further using a bare `raise`.

```python
def process_data(data):
    try:
        return 100 / data
    except ZeroDivisionError:
        print("Logging: division by zero occurred")
        raise   # re-raises the SAME exception up the call stack

try:
    process_data(0)
except ZeroDivisionError:
    print("Caught it again in the outer block")
```

---

## 5. Exception Chaining with `from`

Shows that one exception happened **because of** another — useful for debugging.

```python
class ConfigError(Exception):
    pass

def load_config():
    try:
        return int("not-a-number")
    except ValueError as e:
        raise ConfigError("Failed to load configuration") from e

try:
    load_config()
except ConfigError as e:
    print(e)                # Failed to load configuration
    print(e.__cause__)      # invalid literal for int() with base 10: 'not-a-number'
```

### Beginner tip
Create custom exceptions when your application has specific error conditions that deserve their own name (e.g., `InsufficientFundsError`) — it makes error handling much clearer for anyone reading the code.

---

## 6. Knowledge Check

1. What does the `raise` keyword do?
2. How do you create a custom exception class in Python?
3. What is the difference between `raise` and `raise ... from ...`?
4. Write a custom exception `NegativeValueError` and raise it when a function receives a negative number.

---

**Previous:** [← Try, Except, Finally](./00-Try-Except-Finally.md)
**Next:** [Assertions →](./02-Assertions.md)
