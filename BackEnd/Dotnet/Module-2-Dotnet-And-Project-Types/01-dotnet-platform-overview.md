# 🌐 .NET Platform Overview — The Engine Behind Your Backend

> **Trainer's Note:** You already know programming basics, OOP, and web ideas. Now meet the **platform** that runs your C# backend. This file answers: What is .NET? Why are there old and new names? What happens when your code runs?

---

## 📑 Table of Contents
1. [What is the .NET Platform?](#1-what-is-the-net-platform)
2. [The Big Pieces: SDK, Runtime, Libraries, Languages](#2-the-big-pieces-sdk-runtime-libraries-languages)
3. [.NET Framework vs .NET Core vs .NET (5+)](#3-net-framework-vs-net-core-vs-net-5)
4. [CLR — Common Language Runtime](#4-clr--common-language-runtime)
5. [C# Compiler Basics (Roslyn → IL → JIT)](#5-c-compiler-basics-roslyn--il--jit)
6. [Cross-Platform Nature of Modern .NET](#6-cross-platform-nature-of-modern-net)
7. [What You Install vs What You Ship](#7-what-you-install-vs-what-you-ship)
8. [LTS Versions and How to Choose](#8-lts-versions-and-how-to-choose)
9. [How This Connects to Backend Work](#9-how-this-connects-to-backend-work)
10. [Knowledge Check](#10-knowledge-check)

---

## 1. What is the .NET Platform?

**.NET** is a free, open-source **developer platform** from Microsoft for building many kinds of apps with languages like **C#**.

```
Think of .NET as a full kitchen, not one tool:

  🍳 Kitchen  = .NET platform
  👨‍🍳 Chef     = C# (or F# / VB)
  📖 Recipes = your application code
  🔥 Stove    = runtime (CLR) that actually cooks/runs code
  🧰 Tools    = Base Class Library (lists, HTTP, files, JSON…)
```

### What can you build?
| App type | Typical tech |
|----------|----------------|
| Backend Web APIs | ASP.NET Core Web API |
| Websites | ASP.NET Core MVC / Razor / Blazor |
| Desktop | WPF, WinForms, .NET MAUI |
| Mobile | .NET MAUI |
| Cloud / serverless | Azure Functions, containers |
| Libraries | Class Library projects shared by apps |
| Games | Unity uses C# |

For **this notebook**, the main destination is **ASP.NET Core Web API** — JSON APIs for web and mobile clients.

---

## 2. The Big Pieces: SDK, Runtime, Libraries, Languages

Beginners mix these four names. Separate them early.

| Piece | Simple meaning | Example |
|-------|----------------|---------|
| **Language** | How you write code | C# |
| **Libraries (BCL/FCL)** | Ready-made building blocks | `List<T>`, `HttpClient`, `String` |
| **Runtime** | Engine that runs apps | .NET Runtime + CLR |
| **SDK** | Toolkit for developers | compilers, `dotnet` CLI, templates |

```
┌──────────────────────────────────────────────┐
│                 Your C# App                  │
├──────────────────────────────────────────────┤
│  ASP.NET Core + NuGet packages (extra tools) │
├──────────────────────────────────────────────┤
│  Base Class Library (BCL)                    │
├──────────────────────────────────────────────┤
│  CLR / Runtime (runs IL, GC, security…)      │
├──────────────────────────────────────────────┤
│  Operating System (Windows / Linux / macOS)  │
└──────────────────────────────────────────────┘
```

### Easy memory tips
- **SDK** = what **you** install to **build** apps  
- **Runtime** = what a machine needs to **run** apps  
- **BCL** = free toolbox shipped with .NET  
- **NuGet** = extra packages you add (Serilog, EF Core, etc.)

---

## 3. .NET Framework vs .NET Core vs .NET (5+)

History caused confusing names. Here is the clean map.

### Timeline (simple story)
```
2002        .NET Framework 1.0     → Windows only, legacy enterprise
2016        .NET Core 1.0          → open source + cross-platform restart
2019        .NET Core 3.1          → popular LTS Core version
2020        .NET 5                 → one brand name again: just ".NET"
2021+       .NET 6, 7, 8, 9…       → modern unified platform
```

### Comparison table
| Topic | .NET Framework | .NET Core | .NET (5+) |
|-------|----------------|-----------|-----------|
| **Also called** | “Full Framework” | Core | Modern .NET |
| **OS support** | Windows only | Windows, Linux, macOS | Windows, Linux, macOS |
| **Open source** | Mostly no | Yes | Yes |
| **Ship model** | Installed on Windows machines | Side-by-side versions | Side-by-side versions |
| **Web stack** | ASP.NET (old), Web API 2 | ASP.NET Core | ASP.NET Core |
| **Performance** | Older design | Much faster | Fast + keeps improving |
| **New features** | Maintenance only | Merged into .NET 5+ | Active development |
| **Containers / cloud** | Awkward | Great | Best choice |
| **Use today for new APIs?** | No | No (move to .NET 8+) | **Yes** |

### Important branding fact
```
When people say ".NET" today in job posts, they almost always mean:
  modern .NET 6/7/8/9+   (not .NET Framework 4.x)
```

| If you hear… | They usually mean… |
|--------------|--------------------|
| .NET Framework 4.8 | Old Windows-only stack |
| .NET Core 3.1 | Transitional Core era |
| .NET 8 / .NET 9 | Current modern platform |
| ASP.NET Core | Modern web/API framework on modern .NET |
| ASP.NET MVC 5 | Old Framework-era web style |

### Why Microsoft changed direction
1. Cloud and Linux became normal  
2. Containers need small, fast, side-by-side runtimes  
3. One product family is easier than Framework + Core forever  
4. Open source invited community and cross-platform growth  

### Migration note (awareness only)
Many companies still run **.NET Framework** apps. New backend projects should start on **modern .NET (LTS)**. Migrating old Framework apps is a separate project — not your first week goal.

---

## 4. CLR — Common Language Runtime

The **CLR** is the **engine** that runs your .NET programs.

### What CLR does for you
| Job | Plain meaning |
|-----|---------------|
| **Load code** | Bring assemblies into memory |
| **JIT compile** | Convert IL to machine code for this CPU/OS |
| **Memory management (GC)** | Allocate objects; clean unused ones |
| **Type safety** | Help stop many invalid memory mistakes |
| **Exception handling** | Standard error mechanism |
| **Security / sandboxing ideas** | Safer execution model than raw native code |
| **Threading support** | Help run concurrent work |

```
Your C# source
     │
     ▼
  Compiler produces IL inside a DLL/EXE (assembly)
     │
     ▼
  CLR loads assembly
     │
     ▼
  JIT turns IL → native machine code
     │
     ▼
  CPU runs it, GC manages memory
```

### CLR in one analogy
```
IL code   = half-cooked meal (portable)
JIT       = final cooking on your stove
Machine code = food ready for this kitchen only
CLR       = the whole kitchen staff making that safe and fast
```

### Assemblies (very short)
- Compiled output is usually a **.dll** (library) or app host + dll  
- An **assembly** contains IL + metadata (types, versions)  
- Your API project references other assemblies (your class libraries + NuGet)

You do not manage CLR day to day — but knowing it exists explains performance, GC pauses, and “works on my machine / other OS” behavior.

---

## 5. C# Compiler Basics (Roslyn → IL → JIT)

C# does **not** go straight from your `.cs` file to CPU instructions.

### Two-step compilation
```
  Program.cs  (C# source)
       │
       │  1) Compile time  — Roslyn C# compiler
       ▼
  app.dll     (IL + metadata)     ← portable-ish intermediate
       │
       │  2) Run time      — JIT inside CLR
       ▼
  Native machine code for this OS/CPU
```

| Stage | Tool | Input | Output |
|-------|------|-------|--------|
| Compile | **Roslyn** (C# compiler) | `.cs` files | IL in assembly (`.dll`) |
| Run | **JIT** (in CLR) | IL | CPU instructions |

### Why Intermediate Language (IL / MSIL)?
1. **One compiler front-end world** for C# (and other .NET languages)  
2. **Portability** — same IL can run on Windows/Linux/macOS with the right runtime  
3. **Runtime optimizations** — JIT can optimize for the actual machine  
4. **Safety/metadata** — rich type info for tools, reflection, debugging  

### AOT note (awareness)
Modern .NET also supports **Ahead-of-Time** compilation in some scenarios (faster startup, native-ish publish). Most beginner Web APIs still use the normal JIT model first. Learn JIT path first.

### What `dotnet build` really does
```bash
dotnet build
```
- Restores packages if needed  
- Compiles C# → IL assemblies  
- Reports errors **before** the app runs (compile-time errors)

```bash
dotnet run
```
- Builds if needed  
- Starts the runtime  
- JIT compiles methods as they are used (simplifed view)

---

## 6. Cross-Platform Nature of Modern .NET

Modern .NET runs on:
- **Windows**
- **Linux**
- **macOS**

```
           same C# code
                │
        ┌───────┼───────┐
        ▼       ▼       ▼
     Windows  Linux   macOS
        │       │       │
        └───────┼───────┘
                ▼
        .NET Runtime + CLR
```

### What “cross-platform” means for backend work
| Area | Reality |
|------|---------|
| Language & most libraries | Same |
| ASP.NET Core Kestrel server | Works on all three |
| Path separators / file casing | Be careful on Linux (`\` vs `/`, case-sensitive files) |
| Some Windows-only APIs | Still exist — avoid for portable backends |
| Containers | Extremely common on Linux images |
| Deployment | Azure, AWS, on-prem Linux VMs, IIS on Windows — all possible |

### Practical beginner rules
1. Prefer **ASP.NET Core** + modern .NET for APIs  
2. Use `Path.Combine` instead of hard-coded `\`  
3. Do not assume Registry, full Framework APIs, or IIS-only features  
4. Test in Linux containers early if that is your production target  

### Same app, different machines
```
Dev laptop (Windows)  --dotnet run--> local API
CI agent (Linux)      --dotnet test--> automated checks
Prod server (Linux)   --container---> public API
```
That is the modern .NET backend lifestyle.

---

## 7. What You Install vs What You Ship

| On developer machine | On server / container |
|----------------------|------------------------|
| **.NET SDK** (build tools + templates + runtime) | Often **Runtime** only (or app is self-contained) |
| IDE / editor | No IDE required |
| Source code | Published output |

### Three publish styles (preview)
| Mode | Meaning |
|------|---------|
| **Framework-dependent** | App needs matching .NET runtime installed on host |
| **Self-contained** | App carries its own runtime (bigger folder, fewer host needs) |
| **Container image** | App + runtime base image shipped together (very common) |

You will practice publish commands later; for now just know **SDK ≠ what production must install**.

---

## 8. LTS Versions and How to Choose

Microsoft releases .NET versions on a cadence:

| Kind | Meaning | Example pattern |
|------|---------|-----------------|
| **LTS** (Long Term Support) | Supported longer — preferred for production | .NET 6, .NET 8, … |
| **STS** (Standard Term Support) | Shorter support — fine for learning/experiments | .NET 7, .NET 9, … |

### Beginner recommendation
```
Learning + real projects: prefer current LTS (e.g. .NET 8)
Playing with newest toys: STS is OK if you can upgrade later
```

Check versions on your machine:
```bash
dotnet --info
dotnet --list-sdks
dotnet --list-runtimes
```

---

## 9. How This Connects to Backend Work

| Platform idea | Backend impact |
|---------------|----------------|
| Modern .NET | ASP.NET Core Web API host |
| CLR + GC | Memory behavior under load |
| Roslyn compile | Fast feedback on type errors |
| Cross-platform | Linux containers in cloud |
| BCL + NuGet | HTTP, JSON, logging, EF Core |
| Assemblies | Split API + Domain + Infrastructure projects |

```
Browser / Mobile
      │ HTTPS + JSON
      ▼
 ASP.NET Core on modern .NET
      │
      ▼
 Your class libraries (business rules)
      │
      ▼
 Database / external services
```

**Next in this module:** install tools, learn `dotnet` CLI, then create real project types.

---

## 10. Knowledge Check

**Q1.** In plain words, what is .NET?  
**Q2.** What is the main OS difference between .NET Framework and modern .NET?  
**Q3.** SDK vs Runtime — which one do you need to *build* apps?  
**Q4.** What does the CLR do during program execution (name at least three jobs)?  
**Q5.** What are the two compilation stages from C# source to CPU code?  
**Q6.** Why does IL exist instead of compiling straight to machine code only?  
**Q7.** For a new company Web API in 2026, should you start on .NET Framework 4.8 or .NET 8 LTS?  
**Q8.** Name one cross-platform gotcha with file paths.

### Mini practice
1. Run `dotnet --info` on your machine  
2. Write down: SDK version(s), runtime version(s), OS  
3. In one paragraph, explain whether you are on modern .NET or only Framework tooling  

### Answers (short)
1. A platform to build and run apps (languages + libraries + runtime)  
2. Framework = Windows only; modern .NET = Windows/Linux/macOS  
3. SDK  
4. Load assemblies, JIT, GC, exceptions, type safety…  
5. Roslyn C# → IL; JIT → native code  
6. Portability, shared runtime services, optimizations, multi-language  
7. .NET 8 LTS (or current LTS)  
8. Linux paths are case-sensitive; use `Path.Combine`, avoid hard-coded `\`

---

## ✅ What You Should Feel Confident About

- [ ] Explain .NET as a platform, not “just a language”  
- [ ] Compare Framework vs Core vs modern .NET in one table  
- [ ] Describe CLR responsibilities at a beginner level  
- [ ] Sketch Roslyn → IL → JIT flow  
- [ ] Explain why modern .NET is cross-platform  
- [ ] Prefer LTS for real backend projects  

**Previous module:** Module 1 — C# Language Fundamentals  
**Next:** [02-tools-and-environment.md](./02-tools-and-environment.md) — SDK, IDEs, and the `dotnet` CLI.
