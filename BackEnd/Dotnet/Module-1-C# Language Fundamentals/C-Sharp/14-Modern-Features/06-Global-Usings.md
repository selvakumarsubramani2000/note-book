# 🌐 Global Usings in C#

> **Trainer's Note:** Global usings let common namespaces apply across the project, so you don't repeat the same `using` lines in every file.

---

## 📑 Table of Contents
1. [What are Global Usings?](#1-what-are-global-usings)
2. [How to Declare Them](#2-how-to-declare-them)
3. [Implicit Usings](#3-implicit-usings)
4. [Good Practices](#4-good-practices)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What are Global Usings?

A **global using** is a namespace import for the whole project (or compilation unit set).

```csharp
global using System.Text;
global using System.Collections.Generic;
```

After that, many files can use `StringBuilder` / `List<T>` without local using lines.

### Real-world analogy
```
Normal using = bring tools into one room
Global using = stock tools in the whole house utility closet
```

---

## 2. How to Declare Them

### In a dedicated file (recommended)
`GlobalUsings.cs`:

```csharp
global using System;
global using System.Linq;
global using System.Collections.Generic;
```

### In any .cs file
You can place `global using` statements, but a dedicated file keeps intent clear.

### In project file
```xml
<ItemGroup>
  <Using Include="System.Net.Http" />
  <Using Include="System.Text.Json" />
</ItemGroup>
```

---

## 3. Implicit Usings

Modern SDK-style projects often enable **implicit usings**:

```xml
<ImplicitUsings>enable</ImplicitUsings>
```

The SDK then auto-imports common namespaces for the project type (console/web/etc.).

You still add global usings for project-specific common namespaces.

---

## 4. Good Practices

| Do | Don't |
|----|-------|
| Put common project usings in one file | Hide rare namespaces globally |
| Keep global list short and intentional | Import everything "just in case" |
| Prefer clarity for beginners reading one file | Make origin of types hard to discover |
| Combine with file-scoped namespaces cleanly | Create naming conflicts across domains |

### Beginner tip
If a namespace is used in 1–2 files only, keep local `using`.  
If used almost everywhere, consider global.

---

## 5. Knowledge Check

1. What problem do global usings solve?
2. Where is a good place to declare them?
3. What is the difference between global usings and implicit usings?
4. Give one example of a namespace that might deserve a global using in a web API.

---

**Previous:** [← What's New in C# 11/12/13](./05-Whats-New-in-CSharp-11-12-13.md)  
**Next:** [File-Scoped Namespaces →](./07-File-Scoped-Namespaces.md)
