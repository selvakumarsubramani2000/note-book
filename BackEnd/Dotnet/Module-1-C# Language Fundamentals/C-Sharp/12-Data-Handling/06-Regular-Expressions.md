# 🔎 Regular Expressions in C#

> **Trainer's Note:** Regex is a pattern language for text. Use it to validate emails, extract numbers, replace formats, and search complex strings.

---

## 📑 Table of Contents
1. [What is Regex?](#1-what-is-regex)
2. [Basic C# Regex Usage](#2-basic-c-regex-usage)
3. [Common Patterns](#3-common-patterns)
4. [Match, Groups, Replace](#4-match-groups-replace)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is Regex?

**Regular Expression (Regex)** describes a text pattern.

```csharp
// Is this an email-like text?
Regex.IsMatch("selva@test.com", @"^[^@\s]+@[^@\s]+\.[^@\s]+$");
```

### Real-world analogy
```
Regex = metal detector pattern rules at airport
  rule can say: "accept ticket codes that start with TN and 6 digits"
  scanner checks text against rule
```

Namespace: `System.Text.RegularExpressions`

---

## 2. Basic C# Regex Usage

```csharp
using System.Text.RegularExpressions;

string input = "Order 12345 is ready";

bool hasDigits = Regex.IsMatch(input, @"\d+");
Console.WriteLine(hasDigits); // True

Match m = Regex.Match(input, @"\d+");
if (m.Success)
    Console.WriteLine(m.Value); // 12345
```

### Useful methods
| Method | Meaning |
|--------|---------|
| `IsMatch` | true/false if pattern found |
| `Match` | first match details |
| `Matches` | all matches |
| `Replace` | replace matched text |
| `Split` | split by pattern |

---

## 3. Common Patterns

| Pattern | Meaning | Example matches |
|---------|---------|-----------------|
| `\d` | digit | 0-9 |
| `\w` | word char | letters/digits/_ |
| `\s` | whitespace | space/tab/newline |
| `.` | any char (almost) | a, 1, @ |
| `+` | one or more | `\d+` → 123 |
| `*` | zero or more | |
| `?` | optional | `colou?r` |
| `^` / `$` | start / end | full-string anchors |
| `[A-Z]` | char range | uppercase |
| `{2,4}` | length range | 2 to 4 times |

### Practical checks
```csharp
bool isPin = Regex.IsMatch("600001", @"^\d{6}$");
bool isMobile = Regex.IsMatch("9876543210", @"^[6-9]\d{9}$");
bool isCode = Regex.IsMatch("TN-123", @"^[A-Z]{2}-\d{3}$");
```

Use verbatim strings `@"..."` so backslashes stay readable.

---

## 4. Match, Groups, Replace

### Groups
```csharp
string text = "Name: Selva, Age: 30";
Match match = Regex.Match(text, @"Name:\s*(?<name>\w+),\s*Age:\s*(?<age>\d+)");

if (match.Success)
{
    Console.WriteLine(match.Groups["name"].Value); // Selva
    Console.WriteLine(match.Groups["age"].Value);  // 30
}
```

### Replace
```csharp
string dirty = "Call 98765-43210 now";
string clean = Regex.Replace(dirty, @"\D", ""); // keep digits only
// 9876543210
```

### Multiple matches
```csharp
foreach (Match m in Regex.Matches("A1 B22 C3", @"\d+"))
    Console.WriteLine(m.Value); // 1 22 3
```

### Beginner tips
- Start simple; test patterns step by step
- Prefer built-in validators for complex email/phone when available
- Compiled regex can help performance in hot paths (`RegexOptions.Compiled`)
- Bad regex can be hard to read — add comments/samples nearby

```csharp
var re = new Regex(@"^\d{4}$", RegexOptions.Compiled);
Console.WriteLine(re.IsMatch("2026"));
```

---

## 5. Knowledge Check

1. What is regex used for?
2. Which namespace contains `Regex`?
3. What does `^\d{6}$` mean?
4. Difference between `Match` and `Matches`?
5. Write a pattern idea for a city code like `CHN-01`.

---

**Previous:** [← Preprocessor Directives](./05-Preprocessor-Directives.md)  
**Next:** [Exception Handling →](./07-Exception-Handling.md)
