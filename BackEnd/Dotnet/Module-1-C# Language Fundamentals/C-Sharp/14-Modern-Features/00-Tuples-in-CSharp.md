# 📦 Tuples in C# (Modern Features)

> **Trainer's Note:** Tuples are already covered in detail in the dedicated Tuples track. This page is the Modern Features entry point so you can start here and jump to the full guides.

---

## Why Tuples Are a Modern Feature

From **C# 7**, language-level tuple support (ValueTuple) made multi-return values clean and readable.

```csharp
(bool ok, string message) = Validate(age);
```

### Real-world analogy
```
Tuple = takeaway bag with labeled slots
  receipt + name + total together
  no need to build a full suitcase (class) for temporary packing
```

---

## Full Tuples Track (already created)

Use these detailed guides:

| Guide | Path |
|-------|------|
| C# Tuple intro | [../Tuples/00-CSharp-Tuple.md](../Tuples/00-CSharp-Tuple.md) |
| Tuple Class | [../Tuples/01-Tuple-Class.md](../Tuples/01-Tuple-Class.md) |
| ValueTuple | [../Tuples/02-ValueTuple.md](../Tuples/02-ValueTuple.md) |
| ValueTuple Struct | [../Tuples/03-ValueTuple-Struct.md](../Tuples/03-ValueTuple-Struct.md) |

### Quick modern example
```csharp
(int Id, string Name) person = (101, "Selva");
Console.WriteLine($"{person.Id} - {person.Name}");

(bool ok, string msg) Login(string u, string p)
    => u == "admin" ? (true, "Welcome") : (false, "Denied");
```

### Beginner rule
> Prefer **named ValueTuple** for temporary multi-return values.  
> Prefer a **class/record** when the shape is a real business model used in many places.

---

## Knowledge Check

1. Which tuple style is preferred in modern C#?
2. Write a ValueTuple return with `success` and `message`.
3. When should you create a class instead of a tuple?

---

**Next:** [Records in C# →](./01-Records-in-CSharp.md)
