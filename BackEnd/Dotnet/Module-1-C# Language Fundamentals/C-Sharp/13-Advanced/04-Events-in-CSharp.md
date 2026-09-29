# 📢 C# Events

> **Trainer's Note:** Events are a safe publish-subscribe layer over delegates. Publisher raises an event; subscribers react.

---

## 📑 Table of Contents
1. [What is an Event?](#1-what-is-an-event)
2. [Publisher and Subscriber Example](#2-publisher-and-subscriber-example)
3. [EventHandler Pattern](#3-eventhandler-pattern)
4. [Rules and Tips](#4-rules-and-tips)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is an Event?

An **event** notifies interested listeners when something happens.

```csharp
public event Action? OrderPlaced;
```

### Real-world analogy
```
Event = doorbell
Publisher = visitor presses bell
Subscribers = people at home who react
  one opens door
  one checks camera
```

Events prevent outsiders from fully replacing the invocation list like a raw public delegate.

---

## 2. Publisher and Subscriber Example

```csharp
public class OrderService
{
    public event Action<string>? OrderPlaced;

    public void Place(string orderId)
    {
        Console.WriteLine($"Placing {orderId}");
        OrderPlaced?.Invoke(orderId); // raise event safely
    }
}

void SendEmail(string id) => Console.WriteLine($"Email for {id}");
void WriteLog(string id) => Console.WriteLine($"Log for {id}");

var service = new OrderService();
service.OrderPlaced += SendEmail;
service.OrderPlaced += WriteLog;

service.Place("ORD-1001");
```

Unsubscribe:

```csharp
service.OrderPlaced -= SendEmail;
```

---

## 3. EventHandler Pattern

.NET standard pattern:

```csharp
public class PriceChangedEventArgs : EventArgs
{
    public decimal OldPrice { get; }
    public decimal NewPrice { get; }

    public PriceChangedEventArgs(decimal oldPrice, decimal newPrice)
    {
        OldPrice = oldPrice;
        NewPrice = newPrice;
    }
}

public class Product
{
    public event EventHandler<PriceChangedEventArgs>? PriceChanged;

    private decimal price;
    public decimal Price
    {
        get => price;
        set
        {
            if (price == value) return;
            var old = price;
            price = value;
            PriceChanged?.Invoke(this, new PriceChangedEventArgs(old, value));
        }
    }
}
```

```csharp
product.PriceChanged += (sender, e) =>
{
    Console.WriteLine($"{e.OldPrice} -> {e.NewPrice}");
};
```

---

## 4. Rules and Tips

| Tip | Why |
|-----|-----|
| Use `?.Invoke` | avoid null when no subscribers |
| Unsubscribe when done | prevent memory leaks |
| Prefer `EventHandler`/`EventHandler<T>` | standard and clear |
| Publisher raises, subscribers handle | keep responsibilities clean |
| Don't overuse events | simple callbacks/methods may be enough |

### Delegate vs Event
```
Delegate = can be called/assigned more freely
Event    = restricted access, better for notifications
```

---

## 5. Knowledge Check

1. What problem do events solve?
2. How do you subscribe and unsubscribe?
3. Why use `OrderPlaced?.Invoke(...)`?
4. What is `EventArgs` used for?
5. Give one real example of publisher/subscriber.

---

**Previous:** [← Delegates](./03-Delegates-in-CSharp.md)  
**Next:** [Generics →](./05-Generics-in-CSharp.md)
