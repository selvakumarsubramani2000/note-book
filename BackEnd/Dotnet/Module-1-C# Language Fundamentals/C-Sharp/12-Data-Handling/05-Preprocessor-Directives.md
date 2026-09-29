# ⚙️ Preprocessor Directives in C#

> **Trainer's Note:** Preprocessor directives are special instructions that start with `#`. They guide the compiler before normal code compilation.

---

## 📑 Table of Contents
1. [What are Preprocessor Directives?](#1-what-are-preprocessor-directives)
2. [Common Directives](#2-common-directives)
3. [Conditional Compilation Example](#3-conditional-compilation-example)
4. [Practical Tips](#4-practical-tips)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What are Preprocessor Directives?

They are compiler instructions, not normal C# statements.

```csharp
#if DEBUG
    Console.WriteLine("Debug mode");
#endif
```

### Real-world analogy
```
Normal code = recipe steps for cooking
# directives = notes to the kitchen manager
  "Use this step only on festival days"
  before cooking starts
```

---

## 2. Common Directives

| Directive | Purpose |
|-----------|---------|
| `#define` / `#undef` | Define or remove a symbol |
| `#if` / `#elif` / `#else` / `#endif` | Conditional compilation |
| `#warning` | Emit compile warning |
| `#error` | Emit compile error |
| `#region` / `#endregion` | Collapse code blocks in editor |
| `#nullable` | Control nullable context |
| `#pragma warning` | Enable/disable specific warnings |
| `#line` | Special line number control (rare) |

### region example
```csharp
#region Validation Helpers
bool IsEmailValid(string email) => email.Contains("@");
bool IsPhoneValid(string phone) => phone.Length >= 10;
#endregion
```

Regions only help readability in IDE. They do not change runtime.

---

## 3. Conditional Compilation Example

```csharp
#define TRACE_MODE

#if TRACE_MODE
    Console.WriteLine("Tracing is ON");
#else
    Console.WriteLine("Tracing is OFF");
#endif

#if DEBUG
    Console.WriteLine("Running DEBUG build");
#elif RELEASE
    Console.WriteLine("Running RELEASE build");
#endif
```

### warning and error
```csharp
#warning TODO: Replace temp password before release

#if !READY_FOR_PROD
#error This build is not production-ready
#endif
```

### nullable control
```csharp
#nullable enable
string? name = null;

#nullable disable
string oldStyle = null;
```

### pragma warning
```csharp
#pragma warning disable CS0168 // unused variable
int temp;
#pragma warning restore CS0168
```

---

## 4. Practical Tips

### Good uses
- Debug-only logging
- Platform-specific code blocks
- Temporary compile guards
- Organize long files with `#region` carefully

### Avoid
- Too many symbols and complex `#if` forests
- Hiding important code inside confusing conditions
- Using regions instead of real design (small classes/methods)

### Beginner rule of thumb
```
Need different compile-time behavior → #if symbols
Need editor folding only            → #region
Need force attention while build    → #warning / #error
```

---

## 5. Knowledge Check

1. Do preprocessor directives execute at runtime?
2. What does `#if DEBUG ... #endif` do?
3. Difference between `#warning` and `#error`?
4. What is `#region` used for?
5. Give one practical use of conditional compilation.

---

**Previous:** [← Namespaces](./04-Namespaces-in-CSharp.md)  
**Next:** [Regular Expressions →](./06-Regular-Expressions.md)
