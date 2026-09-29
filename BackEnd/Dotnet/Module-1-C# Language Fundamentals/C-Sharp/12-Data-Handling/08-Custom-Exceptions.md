# 🧾 Custom Exceptions in C#

> **Trainer's Note:** Built-in exceptions are useful, but business errors need clear names. Custom exceptions make failures meaningful in your domain.

---

## 📑 Table of Contents
1. [Why Custom Exceptions?](#1-why-custom-exceptions)
2. [Create a Custom Exception](#2-create-a-custom-exception)
3. [Throw and Catch Custom Exceptions](#3-throw-and-catch-custom-exceptions)
4. [Design Tips](#4-design-tips)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Why Custom Exceptions?

```csharp
throw new Exception("Not enough balance"); // too generic
```

Better:

```csharp
throw new InsufficientBalanceException("Not enough balance");
```

### Real-world analogy
```
Generic exception = "Something wrong"
Custom exception  = "Payment declined: insufficient balance"

Support team fixes faster with clear labels.
```

---

## 2. Create a Custom Exception

Derive from `Exception` (or a suitable base).

```csharp
public class InsufficientBalanceException : Exception
{
    public decimal Balance { get; }
    public decimal Amount { get; }

    public InsufficientBalanceException()
    { }

    public InsufficientBalanceException(string message)
        : base(message)
    { }

    public InsufficientBalanceException(string message, Exception inner)
        : base(message, inner)
    { }

    public InsufficientBalanceException(decimal balance, decimal amount)
        : base($"Balance {balance} is less than required amount {amount}")
    {
        Balance = balance;
        Amount = amount;
    }
}
```

### Naming style
- End with `Exception`
- Use clear business language: `OrderNotFoundException`, `InvalidCouponException`

---

## 3. Throw and Catch Custom Exceptions

```csharp
public class BankAccount
{
    public decimal Balance { get; private set; } = 500;

    public void Withdraw(decimal amount)
    {
        if (amount <= 0)
            throw new ArgumentOutOfRangeException(nameof(amount));

        if (amount > Balance)
            throw new InsufficientBalanceException(Balance, amount);

        Balance -= amount;
    }
}

try
{
    var acc = new BankAccount();
    acc.Withdraw(1000);
}
catch (InsufficientBalanceException ex)
{
    Console.WriteLine(ex.Message);
    Console.WriteLine($"Balance: {ex.Balance}, Tried: {ex.Amount}");
}
catch (Exception ex)
{
    Console.WriteLine($"Other error: {ex.Message}");
}
```

### Inner exception example
```csharp
try
{
    // low-level failure
}
catch (Exception ex)
{
    throw new PaymentProcessingException("Payment failed during gateway call", ex);
}
```

Inner exception keeps original technical details for logs.

---

## 4. Design Tips

| Tip | Why |
|-----|-----|
| Don't create too many custom exceptions | Keep set small and useful |
| Prefer specific catch for business errors | Clear handling paths |
| Add useful properties | Balance/Ids help debugging |
| Keep messages clear | Good for logs and APIs |
| Use built-in exceptions when enough | `ArgumentException` etc. still valid |

### When custom exception is worth it
```
Domain rule broken often (insufficient balance, seat already booked)
API needs distinct error code/type
Caller must handle this case specially
```

### When not needed
```
Simple null checks
Programming mistakes (use ArgumentNullException)
One-off rare generic failures
```

---

## 5. Knowledge Check

1. Why create custom exceptions instead of always using `Exception`?
2. What base class do custom exceptions usually inherit?
3. Why include multiple constructors (`message`, `inner`)?
4. Write a custom exception name for "product out of stock".
5. Give one property you might add to that exception.

---

**Previous:** [← Exception Handling](./07-Exception-Handling.md)  
**Next:** [File I/O →](./09-File-IO-in-CSharp.md)
