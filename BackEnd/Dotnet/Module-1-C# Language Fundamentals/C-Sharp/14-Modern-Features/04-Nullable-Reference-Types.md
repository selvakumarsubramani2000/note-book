# ❓ Nullable Reference Types in C#

> **Trainer's Note:** Nullable reference types help catch null bugs earlier with compiler warnings. `string` means "should not be null"; `string?` means "null is allowed".

---

## 📑 Table of Contents
1. [Why NRT Exists](#1-why-nrt-exists)
2. [Enable and Basic Rules](#2-enable-and-basic-rules)
3. [Annotations and Null-Forgiving](#3-annotations-and-null-forgiving)
4. [Practical Habits](#4-practical-habits)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Why NRT Exists

Classic C# let any reference be null, so `NullReferenceException` was common.

Nullable Reference Types (from **C# 8**) add compile-time nullability intent.

### Real-world analogy
```
string  = seat reserved (guest expected)
string? = seat maybe empty (guest optional)
```

Related value-type nullables (`int?`) are different: those are `Nullable<T>`.  
NRT is about **reference types**.

---

## 2. Enable and Basic Rules

### Enable in project
```xml
<PropertyGroup>
  <Nullable>enable</Nullable>
</PropertyGroup>
```

### Meaning
```csharp
string name = "Selva";   // should not be null
string? note = null;     // may be null
```

Compiler warns if you assign null to non-nullable references or dereference maybe-null values unsafely.

```csharp
string? city = GetCity();
// Console.WriteLine(city.Length); // warning if not checked

if (city is not null)
    Console.WriteLine(city.Length); // safe
```

---

## 3. Annotations and Null-Forgiving

### Common annotations
```csharp
void Print(string text) { }          // expects non-null
void PrintMaybe(string? text) { }    // null allowed
```

### Null-forgiving operator `!`
Tells compiler: "I know this is not null."

```csharp
string? value = Maybe();
string definite = value!; // you take responsibility
```

Use carefully — it silences warnings, does not magically prevent null.

### null checks still matter
```csharp
ArgumentNullException.ThrowIfNull(value);
```

---

## 4. Practical Habits

| Habit | Benefit |
|-------|---------|
| Enable `<Nullable>enable</Nullable>` | earlier null warnings |
| Prefer `string` when value is required | clear intent |
| Use `string?` for optional data | honest API design |
| Check before use | avoid runtime crashes |
| Avoid overusing `!` | don't hide real risks |

### Beginner rule
```
Required data → non-nullable reference (string)
Optional data → nullable reference (string?)
Unknown legacy code → fix warnings gradually
```

---

## 5. Knowledge Check

1. Difference between `string` and `string?` with NRT enabled?
2. Does NRT fully remove null exceptions by itself?
3. What does the `!` operator mean?
4. How do you enable nullable reference types in a project file?

---

**Previous:** [← Top-level Statements](./03-Top-level-Statements.md)  
**Next:** [What's New in C# 11/12/13 →](./05-Whats-New-in-CSharp-11-12-13.md)
