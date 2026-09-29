# 🛠️ Tools & Environment — SDK, IDEs, and the `dotnet` CLI

> **Trainer's Note:** Great backend skills still need a working toolbox. This file gets your machine ready: install the SDK, pick an editor, and learn the `dotnet` commands you will use every day.

---

## 📑 Table of Contents
1. [What You Need on Your Machine](#1-what-you-need-on-your-machine)
2. [Installing the .NET SDK and Runtime](#2-installing-the-net-sdk-and-runtime)
3. [Verify the Install](#3-verify-the-install)
4. [IDEs and Editors Overview](#4-ides-and-editors-overview)
5. [The `dotnet` CLI — Your Daily Driver](#5-the-dotnet-cli--your-daily-driver)
6. [Essential Commands Deep Dive](#6-essential-commands-deep-dive)
7. [Project Templates](#7-project-templates)
8. [Solutions and Folder Structure](#8-solutions-and-folder-structure)
9. [Useful Daily Workflow](#9-useful-daily-workflow)
10. [Troubleshooting Setup Problems](#10-troubleshooting-setup-problems)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. What You Need on Your Machine

| Piece | Required? | Purpose |
|-------|-----------|---------|
| **.NET SDK** | Yes | Build, run, test, publish; includes CLI + compilers |
| **Runtime** | Included with SDK | Runs apps (SDK install already has runtimes) |
| **IDE / Editor** | Strongly yes | Write and debug code comfortably |
| **Git** | Yes for real work | Version control |
| **Browser** | Yes | Call Swagger UI / test APIs |
| **Docker** | Optional later | Containers for production-like runs |

```
Minimum happy path for this notebook:
  1) Install .NET SDK (LTS)
  2) Install VS Code or Visual Studio
  3) Open terminal → dotnet --info works
  4) Create a Web API → dotnet run
```

---

## 2. Installing the .NET SDK and Runtime

### Official source
Download from Microsoft’s .NET download page: choose the current **LTS SDK** for your OS (Windows / Linux / macOS).

### Windows (common options)
1. **Installer (beginner-friendly):** download SDK `.exe` and install  
2. **Visual Studio Installer:** workload “ASP.NET and web development” includes the SDK  
3. **Winget** (if you use it):
```powershell
winget install Microsoft.DotNet.SDK.8
```
> Version numbers change — prefer current LTS when you install.

### What the SDK gives you
```
.NET SDK install
  ├── compilers (Roslyn)
  ├── dotnet CLI
  ├── templates (console, webapi, classlib…)
  └── runtimes needed to build/run locally
```

### Runtime-only installs
Servers sometimes install **ASP.NET Core Runtime** without the full SDK.  
Developers should install the **SDK**.

### Side-by-side versions
You can have multiple SDKs installed:
```
SDK 8.0.x
SDK 9.0.x
```
A project’s target framework (in `.csproj`) decides what it builds against. A `global.json` file can pin the SDK version for a repo.

---

## 3. Verify the Install

Open a **new** terminal after installing:

```bash
dotnet --version
dotnet --info
dotnet --list-sdks
dotnet --list-runtimes
```

### What good looks like
| Command | You should see |
|---------|----------------|
| `dotnet --version` | Something like `8.0.x` or `9.0.x` |
| `dotnet --list-sdks` | At least one SDK path |
| `dotnet --list-runtimes` | `Microsoft.NETCore.App` and often `Microsoft.AspNetCore.App` |

### If `dotnet` is not recognized
1. Close and reopen the terminal (PATH refresh)  
2. Confirm SDK install completed  
3. On Windows, check PATH includes the dotnet folder (often `C:\Program Files\dotnet\`)  
4. Restart the machine if PATH still stale  

---

## 4. IDEs and Editors Overview

All three below can build professional .NET backends. Pick based on OS, budget, and taste.

### Comparison
| Tool | Best for | Strengths | Watch-outs |
|------|----------|-----------|------------|
| **Visual Studio** (Windows primarily) | Full .NET / enterprise | Deep debugger, designers, integrated profilers, templates | Heavier install; Mac edition differs |
| **VS Code** | Lightweight + cross-platform | Fast, extensions, great terminal workflow | Needs C# extension setup; less “all-in-one” |
| **JetBrains Rider** | Cross-platform power users | Excellent inspections, refactorings, UX | Commercial license |

### Visual Studio — quick notes
- Workload to tick: **ASP.NET and web development**
- Great for F5 debugging, multiple startup projects, solution explorer comfort
- Common in Windows enterprise teams

### Visual Studio Code — quick notes
Install:
1. VS Code  
2. Extension: **C# Dev Kit** (or C# extension ecosystem from Microsoft)  

Typical flow:
```
Open folder → terminal → dotnet new / build / run → debugger via launch config
```
Excellent if you already live in VS Code for frontend + backend monorepos.

### JetBrains Rider — quick notes
- Strong on Windows, Linux, macOS  
- Feels “IDE complete” like Visual Studio, but cross-platform  
- Very good at detecting code smells early  

### Beginner recommendation
| If you are on… | Start with… |
|----------------|-------------|
| Windows and want guided UI | **Visual Studio** |
| Any OS and like terminal + light editor | **VS Code + C# Dev Kit** |
| Any OS and want maximum IDE assistance | **Rider** |

> The `dotnet` CLI works the same under all of them. Learn CLI — you stay portable.

---

## 5. The `dotnet` CLI — Your Daily Driver

The **`dotnet`** command-line interface creates, builds, runs, tests, and publishes projects without clicking menus.

```
dotnet <command> [options]
```

### Why CLI matters for backend devs
- Same commands in local terminal, CI pipelines, and containers  
- Faster than wizard-only workflows once you know them  
- Easy to script  

### Command map (mental model)
```
Create     → dotnet new
Restore    → dotnet restore   (download NuGet packages)
Build      → dotnet build
Run        → dotnet run
Test       → dotnet test
Add package→ dotnet add package
Publish    → dotnet publish
Clean      → dotnet clean
```

`dotnet run` and `dotnet build` often restore automatically — you still should know `restore` exists.

---

## 6. Essential Commands Deep Dive

### `dotnet new` — create from template
```bash
dotnet new list                 # see templates
dotnet new console -n HelloCli  # console app named HelloCli
dotnet new webapi -n Shop.Api   # ASP.NET Core Web API
dotnet new classlib -n Shop.Domain
dotnet new sln -n Shop          # solution file
dotnet new gitignore            # .gitignore for .NET
```

Useful flags:
| Flag | Meaning |
|------|---------|
| `-n` / `--name` | Project/folder name |
| `-o` / `--output` | Output directory |
| `-f net8.0` | Target framework |
| `--use-controllers` | Web API with controllers (template dependent) |

### `dotnet build` — compile
```bash
dotnet build
dotnet build --configuration Release
```
- Debug = default local development  
- Release = optimized production-oriented build  

### `dotnet run` — build + execute
```bash
dotnet run
dotnet run --project .\src\Shop.Api\Shop.Api.csproj
dotnet run --urls http://localhost:5080
```

Pass app arguments after `--`:
```bash
dotnet run -- --option value
```

### `dotnet restore` — get packages
```bash
dotnet restore
```
Reads package references from `.csproj` / packages lock files and downloads from NuGet.

### `dotnet clean` — remove build outputs
```bash
dotnet clean
```

### `dotnet test` — run unit tests
```bash
dotnet test
```

### `dotnet add` / `dotnet reference`
```bash
dotnet add package Newtonsoft.Json
dotnet add app/Shop.Api package Serilog.AspNetCore
dotnet add app/Shop.Api reference core/Shop.Domain/Shop.Domain.csproj
```

### `dotnet publish` — prepare deployable output
```bash
dotnet publish -c Release -o .\publish
```

### Get help anytime
```bash
dotnet -h
dotnet new -h
dotnet build -h
```

---

## 7. Project Templates

Templates are starter skeletons. You do not begin from an empty folder every time.

### Common templates for this journey
| Template short name | Creates | When to use |
|---------------------|---------|-------------|
| `console` | Console app | Learning C#, utilities, jobs |
| `classlib` | Class library | Domain/business logic DLLs |
| `webapi` | ASP.NET Core Web API | **Main backend target** |
| `web` | Minimal empty web app | Simple HTTP apps |
| `mvc` | MVC website | Server-rendered UI |
| `xunit` / `nunit` / `mstest` | Test project | Unit/integration tests |
| `sln` | Solution file | Group many projects |
| `gitignore` | .gitignore | Git hygiene |
| `editorconfig` | Editor config | Consistent formatting |

```bash
dotnet new list
```

### Web API template flavors (concept)
Depending on SDK version, `webapi` may default to **Minimal APIs** and/or offer **controllers**. Both are valid. This notebook will focus on APIs generally; controllers vs minimal is a later deep dive.

---

## 8. Solutions and Folder Structure

### Project vs Solution
| Term | File | Meaning |
|------|------|---------|
| **Project** | `Something.csproj` | One buildable unit (API, library, tests) |
| **Solution** | `Something.sln` | Bucket that groups many projects |

```
Shop.sln
  ├── src/
  │    ├── Shop.Api/             (webapi project)
  │    ├── Shop.Application/     (classlib)
  │    └── Shop.Domain/          (classlib)
  └── tests/
       └── Shop.Tests/           (xunit project)
```

### Create a small solution from CLI
```bash
mkdir Shop
cd Shop
dotnet new sln -n Shop

dotnet new webapi -n Shop.Api -o src/Shop.Api
dotnet new classlib -n Shop.Domain -o src/Shop.Domain
dotnet new xunit -n Shop.Tests -o tests/Shop.Tests

dotnet sln add src/Shop.Api/Shop.Api.csproj
dotnet sln add src/Shop.Domain/Shop.Domain.csproj
dotnet sln add tests/Shop.Tests/Shop.Tests.csproj

dotnet add src/Shop.Api reference src/Shop.Domain/Shop.Domain.csproj
dotnet add tests/Shop.Tests reference src/Shop.Api/Shop.Api.csproj
```

### Why solutions matter
- One place to open the whole system in an IDE  
- Build/test multiple projects together  
- Clear boundaries: API host vs pure business logic libraries  

---

## 9. Useful Daily Workflow

### First-time machine
```bash
dotnet --info
# install IDE / C# extension if needed
```

### Start a learning API
```bash
dotnet new webapi -n Demo.Api -o Demo.Api
cd Demo.Api
dotnet run
```
Open the printed HTTPS/HTTP URL (and `/swagger` when available).

### Edit → run loop
```
Change code
   → save
   → terminal: dotnet run   (or IDE Run/Debug)
   → call endpoint from browser / Swagger / HTTP file
```

### Before you push code
```bash
dotnet build
dotnet test
```

### Configuration files you will see soon
| File | Role |
|------|------|
| `*.csproj` | Project settings & package references |
| `*.sln` | Solution grouping |
| `appsettings.json` | App configuration |
| `launchSettings.json` | Local run URLs / profiles (dev) |
| `global.json` | Pin SDK version (optional) |
| `nuget.config` | Package sources (optional) |

---

## 10. Troubleshooting Setup Problems

| Problem | Likely fix |
|---------|------------|
| `dotnet` not found | Reopen terminal; fix PATH; reinstall SDK |
| Wrong SDK version building project | Install needed SDK; check `global.json` |
| Port already in use | Change URLs (`--urls`) or stop other process |
| HTTPS certificate trust warning (dev) | `dotnet dev-certs https --trust` (Windows/macOS) |
| Restore failed | Check internet, NuGet feed, package name/version |
| IDE cannot load project | Open folder with `.sln`, install C# workload/extension |
| Build works in CLI but not IDE | IDE using different environment; restart IDE, check SDK list |

### Trust dev HTTPS certificate (common on first Web API)
```bash
dotnet dev-certs https --trust
```

---

## 11. Knowledge Check

**Q1.** Do developers install the SDK or only the runtime? Why?  
**Q2.** Name three IDEs/editors commonly used for .NET.  
**Q3.** What does `dotnet new webapi -n Shop.Api` do?  
**Q4.** Difference between a `.csproj` and a `.sln`?  
**Q5.** Which command compiles your code without necessarily starting the server forever-loop of attention: `build` or `run`?  
**Q6.** How do you add a NuGet package from CLI?  
**Q7.** Why is learning the CLI valuable even if you love Visual Studio click menus?  
**Q8.** What command lists installed SDKs?

### Mini practice
1. Install/verify SDK with `dotnet --info`  
2. Create a solution `LearnModule2`  
3. Add a `console` project and a `classlib` project  
4. Add the classlib as a project reference to the console app  
5. `dotnet build` the solution and `dotnet run` the console project  

### Answers (short)
1. SDK — includes compilers, templates, CLI to build  
2. Visual Studio, VS Code, Rider  
3. Scaffolds a new Web API project named Shop.Api  
4. `.csproj` = one project; `.sln` = group of projects  
5. `dotnet build` (compile). `run` builds and starts execution  
6. `dotnet add package PackageName`  
7. Same commands work in CI/containers; skill transfers across machines  
8. `dotnet --list-sdks`

---

## ✅ What You Should Feel Confident About

- [ ] Install and verify the .NET SDK  
- [ ] Choose an IDE/editor that fits your OS and style  
- [ ] Use `dotnet new`, `build`, `run`, `add package`  
- [ ] Create a solution and add multiple projects  
- [ ] Explain project vs solution  
- [ ] Fix common setup issues (PATH, dev certs, ports)  

**Previous:** [01-dotnet-platform-overview.md](./01-dotnet-platform-overview.md)  
**Next:** [03-project-types.md](./03-project-types.md) — console, class libraries, Web API, `.csproj`, and NuGet.
