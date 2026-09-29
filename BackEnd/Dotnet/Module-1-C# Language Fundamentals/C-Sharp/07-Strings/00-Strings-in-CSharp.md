# 🔤 Strings in C#

> **Trainer's Note:** Almost every app works with text — names, messages, paths, JSON. Start with string basics and immutability first.

---

## 📑 Table of Contents
1. [What is a String?](#1-what-is-a-string)
2. [Immutability](#2-immutability)
3. [Create Strings](#3-create-strings)
4. [String Interpolation](#4-string-interpolation)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is a String?

A **string** is a sequence of characters used for text.

```csharp
string name = "Selva";
string empty = "";
string message = "Hello, " + name;
```

In C#, `string` is an alias for `System.String`. Both mean the same thing.

### Real-world analogy
```
string = a printed name card

  Once printed, the card itself does not change.
  To change the name, you print a NEW card.
  (That is why string is immutable.)
```

---

## 2. Immutability

Strings are **immutable** — you cannot change the original content in place.

```csharp
string s = "Hi";
s = s + " there";   // creates a NEW string in memory
// old "Hi" is left for garbage collection
```

So every "change" actually builds a **new** string.

---

## 3. Create Strings

```csharp
string a = "Hello";
string b = new string('A', 5);     // "AAAAA"
string c = string.Empty;           // same as ""
char[] letters = { 'C', '#', '!' };
string d = new string(letters);    // "C#!"
```

---

## 4. String Interpolation

Modern and clean way to insert values into text:

```csharp
string city = "Chennai";
int year = 2026;
string text = $"I live in {city}, year {year}";
// I live in Chennai, year 2026
```

### What next in this folder
| File | Topic |
|------|--------|
| Verbatim `@` | paths and multi-line text |
| String Class | ready helper methods |
| StringBuilder | efficient building in loops |
| String vs StringBuilder | when to choose which |

---

## 5. Knowledge Check

1. Why do we say strings are immutable in C#?
2. Are `string` and `System.String` different types?
3. Write an interpolated string with your name and city.
4. What happens memory-wise when you do `s = s + "x"` many times?

---

**Previous:** [← ArrayList in C#](../ArrayList/00-ArrayList-in-CSharp.md)
**Next:** [Verbatim String Literal →](./01-Verbatim-String-Literal.md)
