# 🔢 C# Indexers

> **Trainer's Note:** An indexer lets your class behave like an array or dictionary. Instead of `obj.GetItem(0)`, you write `obj[0]`. Clean and natural.

---

## 📑 Table of Contents
1. [What is an Indexer?](#1-what-is-an-indexer)
2. [C# Indexers — Basic Usage](#2-c-indexers--basic-usage)
3. [Indexer vs Property vs Array](#3-indexer-vs-property-vs-array)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. What is an Indexer?

An **indexer** is a special class member that lets objects be accessed with **`[]` index syntax**, like arrays.

```csharp
StudentList list = new StudentList();
list[0] = "Selva";          // looks like an array
string name = list[0];
```

### Real-world analogy
```
Without indexer:
  Library.GetBookByShelfNumber(3)

With indexer:
  Library[3]

  Same idea as opening locker number 3 with a key tag.
```

### Why indexers are useful
- Your custom class can store a collection inside
- Outside code can access items with simple `obj[i]`
- You control validation, bounds checks, and storage logic

---

## 2. C# Indexers — Basic Usage

### Syntax
```csharp
public returnType this[parameterType index]
{
    get { /* return value */ }
    set { /* store value */ }
}
```

`this` is required. The class itself becomes indexable.

### Simple example
```csharp
public class WeekDays
{
    private string[] days = new string[7];

    public string this[int index]
    {
        get
        {
            if (index < 0 || index >= days.Length)
                throw new IndexOutOfRangeException("Invalid day index");
            return days[index];
        }
        set
        {
            if (index < 0 || index >= days.Length)
                throw new IndexOutOfRangeException("Invalid day index");
            days[index] = value;
        }
    }

    public int Length => days.Length;
}
```

### Use it
```csharp
WeekDays week = new WeekDays();
week[0] = "Monday";
week[1] = "Tuesday";
Console.WriteLine(week[0]); // Monday
```

### Read-only indexer
```csharp
public string this[int index]
{
    get { return days[index]; }
    // no set → read-only
}
```

### Expression-bodied indexer
```csharp
public string this[int i]
{
    get => days[i];
    set => days[i] = value;
}
```

### Indexer with string key (dictionary style)
```csharp
public class PhoneBook
{
    private Dictionary<string, string> contacts = new();

    public string this[string name]
    {
        get => contacts.ContainsKey(name) ? contacts[name] : "Not found";
        set => contacts[name] = value;
    }
}

PhoneBook book = new PhoneBook();
book["Selva"] = "9876543210";
Console.WriteLine(book["Selva"]);
```

---

## 3. Indexer vs Property vs Array

| Point | Property | Indexer | Array |
|-------|----------|---------|-------|
| Access style | `obj.Name` | `obj[i]` / `obj["key"]` | `arr[i]` |
| Parameters | None | One or more | Index only |
| Can overload? | No (by params) | Yes | Language feature |
| Best for | Single named value | Collection-like access | Fixed same-type storage |

### Beginner rule of thumb
```
One value with a clear name     → Property   (student.Name)
Many values by position/key     → Indexer    (students[0], book["Selva"])
Simple fixed list of same type  → Array      (int[] marks)
```

---

## 4. Knowledge Check

1. What keyword is used to declare an indexer in C#?
2. Write a simple read/write indexer for `string this[int index]`.
3. When do you choose an indexer instead of a normal property?
4. Can an indexer use a string key? Give one example idea.

---

**Previous:** [← Tuples in C#](../Tuples/00-CSharp-Tuple.md)
**Next:** [Multidimensional Indexers →](./01-Multidimensional-Indexers.md)
