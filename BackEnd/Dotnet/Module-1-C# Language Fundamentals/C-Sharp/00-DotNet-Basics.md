# 🌐 .NET Basics — What Runs Your C# Code

> **Trainer's Note:** Before writing C# code, you need to understand the "engine" that runs it. Think of this as learning how a car works before you drive it. Simple words, real pictures in your mind, no heavy jargon.

---

## 📑 Table of Contents
1. [What is .NET?](#1-what-is-net)
2. [Introduction to .NET, FCL, and CLR](#2-introduction-to-net-fcl-and-clr)
3. [.NET History](#3-net-history)
4. [Compilation Process — MSIL and JIT](#4-compilation-process--msil-and-jit)
5. [.NET CLR Deep Dive](#5-net-clr-deep-dive)
6. [.NET Assembly](#6-net-assembly)
7. [Shared Assembly](#7-shared-assembly)
8. [Knowledge Check](#8-knowledge-check)

---

## 1. What is .NET?

**.NET** is a **platform** from Microsoft that lets you build many kinds of applications using languages like **C#**.

```
Think of .NET like a big kitchen:

  🍳 Kitchen (.NET Platform)
     ├── Stoves & tools  →  Runtime that runs your code (CLR)
     ├── Recipe books    →  Ready-made libraries (FCL / BCL)
     └── Chefs           →  Languages: C#, F#, VB.NET

  Your app = the meal you cook using the kitchen tools.
```

### What can you build with .NET?
| Type | Example |
|------|---------|
| Web APIs | Online order systems |
| Websites | Company portals |
| Desktop apps | Billing software |
| Mobile apps | .NET MAUI apps |
| Cloud apps | Azure Functions |
| Games | Games with Unity (uses C#) |

**.NET is free, open-source, and runs on Windows, Linux, and macOS.**

---

## 2. Introduction to .NET, FCL, and CLR

Three names you will hear again and again:

| Name | Full Form | Simple Meaning |
|------|-----------|----------------|
| **.NET** | — | The whole platform (kitchen) |
| **CLR** | Common Language Runtime | The engine that **runs** your code |
| **FCL / BCL** | Framework / Base Class Library | Ready-made tools (string, list, file, date…) |

```
┌─────────────────────────────────────────────┐
│                 Your C# App                 │
├─────────────────────────────────────────────┤
│   FCL / BCL  (lists, files, web, database)  │  ← ready tools
├─────────────────────────────────────────────┤
│   CLR        (runs code, manages memory)    │  ← engine
├─────────────────────────────────────────────┤
│   OS         (Windows / Linux / macOS)      │
└─────────────────────────────────────────────┘
```

### FCL (Framework Class Library)
A huge set of **ready-made classes** so you don't rebuild everything from zero.
- `System.String` → text
- `System.Collections.Generic.List<T>` → lists
- `System.IO` → files and folders
- `System.Net.Http` → call APIs

### CLR (Common Language Runtime)
The **runtime engine**. It loads your program, runs it, manages memory, and handles errors safely.

---

## 3. .NET History (Simple Timeline)

| Year | Version | Simple Story |
|------|---------|--------------|
| 2002 | .NET Framework 1.0 | First release — Windows only |
| 2005–2010 | Framework 2.0 → 4.0 | Got bigger and better on Windows |
| 2016 | .NET Core 1.0 | New design — open source + cross-platform |
| 2019 | .NET Core 3.1 | Stable for many real projects |
| 2020 | **.NET 5** | One brand name: just ".NET" |
| 2021+ | .NET 6, 7, 8, 9… | One platform for web, desktop, mobile, cloud |

### Easy memory tip
```
Old:  .NET Framework  → Windows only
New:  .NET Core → .NET 5+  → Windows + Linux + macOS
Today when people say ".NET", they usually mean modern .NET (5/6/7/8+).
```

---

## 4. Compilation Process — MSIL and JIT

Your C# code does **not** go straight to machine code. It goes through 2 steps.

### 🍳 Cooking analogy
```
1. You write a recipe in C#          →  Source code (.cs)
2. Chef prep kitchen (compile)       →  Roslyn compiler
3. Half-cooked dish ready to finish  →  MSIL / IL (in a .dll or .exe)
4. Final cooking on your stove       →  JIT converts IL → machine code
5. Serve the meal                    →  App runs on your machine
```

### Step by step

```
  Your C# Code (.cs)
         │
         ▼  C# Compiler (Roslyn)
  MSIL / IL  +  Metadata   (saved in Assembly: .dll / .exe)
         │
         ▼  When you RUN the app
  JIT Compiler (inside CLR)
         │
         ▼
  Native Machine Code (CPU understands this)
         │
         ▼
  Program Runs
```

| Term | Meaning |
|------|---------|
| **MSIL / IL** | Microsoft Intermediate Language — half-compiled code that any .NET app can use |
| **JIT** | Just-In-Time compiler — converts IL to machine code **when the app runs** |
| **Metadata** | Info about classes, methods, types stored inside the assembly |

**Why this 2-step design?**
- Same IL can run on different machines (Windows/Linux/macOS)
- Different languages (C#, F#, VB) can all become IL and work together

---

## 5. .NET CLR Deep Dive

**CLR = Common Language Runtime** — the heart of .NET.

### What does the CLR do?

| Job | Simple explanation |
|-----|--------------------|
| **Load assemblies** | Brings your .dll/.exe into memory |
| **JIT compile** | Turns IL into machine code |
| **Memory management** | Gives memory, and cleans unused objects (Garbage Collection) |
| **Type safety** | Stops invalid type mistakes |
| **Exception handling** | Manages try/catch style errors |
| **Security** | Helps control what code is allowed to do |
| **Thread management** | Helps run work in parallel |

### Real-world picture
```
CLR is like a smart factory manager:

  - Workers arrive     → Load your assemblies
  - Assign machines    → JIT compiles methods when needed
  - Clean the floor    → Garbage Collector frees unused memory
  - Safety rules       → Type safety + exception handling
  - Shift planning     → Thread management
```

### Garbage Collection (GC) — quick idea
You create objects. When you stop using them, the **GC** later removes them and frees memory. You usually **don't** free memory by hand in C# (unlike old C/C++ for many cases).

---

## 6. .NET Assembly

An **Assembly** is the **packaged output** of your code after compilation.

```
Your .cs files  →  Compiler  →  Assembly (.dll or .exe)
```

### What is inside an assembly?
```
┌──────────────────────────────┐
│         ASSEMBLY             │
│  ┌────────────────────────┐  │
│  │ Manifest (ID info)     │  │  name, version, culture, files
│  ├────────────────────────┤  │
│  │ MSIL / IL code         │  │  your actual logic
│  ├────────────────────────┤  │
│  │ Metadata               │  │  types, methods, properties
│  ├────────────────────────┤  │
│  │ Resources (optional)   │  │  images, strings, files
│  └────────────────────────┘  │
└──────────────────────────────┘
```

### Types of assemblies
| Type | File | Meaning |
|------|------|---------|
| **Executable** | `.exe` | Can start as a program |
| **Library** | `.dll` | Code library used by other apps |

### Why assemblies matter
- Versioning (1.0.0 vs 2.0.0)
- Reuse code across projects
- Security and identity information
- Deployment unit (what you ship)

**Simple line:** Assembly = your compiled package of code + info about that code.

---

## 7. Shared Assembly

### Private vs Shared Assembly

| | **Private Assembly** | **Shared Assembly** |
|---|----------------------|---------------------|
| **Where used** | One application only | Many applications |
| **Where stored** | App folder | Global place (historically GAC) |
| **Versioning** | Simple | Strong version control needed |
| **Example** | Your project’s `Helper.dll` | Common library used by many apps |

### Real-world analogy
```
Private assembly  =  Your personal water bottle (only you use it)
Shared assembly   =  Office water cooler (many people use the same one)
```

### Shared assembly key points
1. **Used by multiple applications**
2. Needs a **strong name** (unique identity: name + version + culture + public key)
3. Older .NET Framework used the **GAC (Global Assembly Cache)** to store shared assemblies
4. In **modern .NET**, we mostly share libraries using **NuGet packages** (still "shared code", better workflow)

```
Old style (.NET Framework):
  Shared DLL → installed in GAC → many Windows apps use it

Modern style (.NET):
  Shared library → published as NuGet package → many projects install it
```

### Strong Name (simple idea)
A strong name is like an official stamp so Windows/.NET can trust:
- which company made the DLL
- which version it is
- that the file was not changed secretly

---

## 8. Knowledge Check

1. In one sentence, what is .NET?
2. What is the difference between **CLR** and **FCL**?
3. Why does C# compile first to **MSIL**, not directly to machine code?
4. What job does the **JIT** compiler do?
5. What is an **assembly**?
6. How is a **shared assembly** different from a **private assembly**?
7. In modern .NET, what is the common way to share libraries between many projects?

---

**Next:** [C# Fundamentals →](./01-CSharp-Fundamentals.md)
