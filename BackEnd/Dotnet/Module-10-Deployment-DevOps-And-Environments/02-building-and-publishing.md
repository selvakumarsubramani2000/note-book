# 📦 Building & Publishing — From Source to Deployable Output

> **Trainer's Note:** `dotnet build` compiles for development. **`dotnet publish`** prepares the app to run on a server or in a container. Know **framework-dependent** vs **self-contained**, and what lands in the publish folder (DLLs, deps, runtimeconfig, static assets).

---

## 📑 Table of Contents
1. [Build vs Publish](#1-build-vs-publish)
2. [dotnet publish Command](#2-dotnet-publish-command)
3. [Framework-Dependent Deployment (FDD)](#3-framework-dependent-deployment-fdd)
4. [Self-Contained Deployment (SCD)](#4-self-contained-deployment-scd)
5. [FDD vs SCD Comparison](#5-fdd-vs-scd-comparison)
6. [RID and Target OS](#6-rid-and-target-os)
7. [Publish Output Anatomy](#7-publish-output-anatomy)
8. [Configuration and appsettings at Publish Time](#8-configuration-and-appsettings-at-publish-time)
9. [ReadyToRun, Single-File, Trimming (Awareness)](#9-readytorun-single-file-trimming-awareness)
10. [Smoke-Testing Published Output](#10-smoke-testing-published-output)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. Build vs Publish

| Command | Purpose |
|---------|---------|
| `dotnet restore` | Download NuGet packages |
| `dotnet build` | Compile → binaries under `bin/` |
| `dotnet test` | Run tests against build |
| `dotnet publish` | Produce a **deployable** folder/file set |

```
Source
  → restore
  → build (and test in CI)
  → publish
  → copy folder / container image / zip to host
  → run
```

`publish` can include:
- compiled assemblies  
- dependencies  
- runtime (optional)  
- static web assets  
- config files needed to start  

---

## 2. dotnet publish Command

### Basic
```bash
dotnet publish src/Shop.Api/Shop.Api.csproj -c Release -o artifacts/api
```

| Flag | Meaning |
|------|---------|
| `-c Release` | Release configuration (optimized) |
| `-o <path>` | Output folder |
| `--no-build` | Publish existing build (CI optimization) |
| `-r <rid>` | Runtime identifier (for self-contained / RID-specific) |
| `--self-contained true/false` | Bundle runtime or not |
| `-p:PublishSingleFile=true` | Single-file publish (optional) |

### Example CI-friendly sequence
```bash
dotnet restore
dotnet build -c Release --no-restore
dotnet test  -c Release --no-build
dotnet publish src/Shop.Api/Shop.Api.csproj -c Release --no-build -o artifacts/api
```

---

## 3. Framework-Dependent Deployment (FDD)

**FDD** = you ship **your app + dependencies**, but the machine/container already has the **.NET runtime** installed.

```bash
dotnet publish -c Release -o artifacts/api --self-contained false
```

```
Server has:  .NET 8 ASP.NET runtime
You deploy:  Shop.Api.dll + deps
Start:       dotnet Shop.Api.dll
```

### Pros
| Pro | Why it matters |
|-----|----------------|
| Smaller deploy size | Runtime not copied |
| Shared runtime patching | Host updates runtime |
| Simple for many cloud hosts | App Service often provides runtime |

### Cons
| Con | Detail |
|-----|--------|
| Runtime must match | Need correct major/minor on host |
| Not fully portable USB-style | Won’t run without runtime |

### Typical start
```bash
dotnet Shop.Api.dll
# or set ASPNETCORE_URLS / env first
```

---

## 4. Self-Contained Deployment (SCD)

**SCD** = publish **includes the .NET runtime** for a target OS/architecture.

```bash
dotnet publish -c Release -o artifacts/api \
  --self-contained true \
  -r linux-x64
```

```
You deploy:  app + runtime for linux-x64
Host needs:  matching OS/arch (no separate .NET install required)
Start:       ./Shop.Api   (native host)  or executable name on Windows
```

### Pros
| Pro | Why |
|-----|-----|
| No runtime pre-install | Great for locked-down servers / simple VMs |
| Predictable runtime version | You shipped it |

### Cons
| Con | Why |
|-----|-----|
| Much larger output | Runtime bulk |
| Patching story | Rebuild/redeploy to get runtime fixes |
| Per-OS build | Need correct RID |

---

## 5. FDD vs SCD Comparison

| Topic | Framework-dependent | Self-contained |
|-------|---------------------|----------------|
| Output size | Smaller | Larger |
| Host needs .NET installed? | **Yes** | No (for that RID) |
| Start command | `dotnet MyApp.dll` | App host executable |
| Patch runtime independently | Easier on host | Redeploy app |
| Common on | App Service, containers base images with runtime | Minimal VMs, some desktop/tools |
| Containers | Often FDD on `aspnet` runtime image | Or SDK→runtime multi-stage still FDD-ish |

### Beginner recommendation
- **Cloud App Service / standard containers:** framework-dependent is common  
- **Bare VM without runtime control:** self-contained  
- **Docker multi-stage (next file):** usually publish FDD into runtime image  

---

## 6. RID and Target OS

**RID** = Runtime Identifier.

| RID | Target |
|-----|--------|
| `win-x64` | Windows 64-bit |
| `linux-x64` | Linux 64-bit |
| `linux-arm64` | Linux ARM64 |
| `osx-arm64` | macOS Apple Silicon |

```bash
dotnet publish -c Release -r linux-x64 --self-contained true -o artifacts/api-linux
```

Pick RID to match **where the app runs**, not necessarily where you build (cross-publish is supported for many targets).

---

## 7. Publish Output Anatomy

A typical framework-dependent Web API publish folder contains:

| Item | Role |
|------|------|
| `Shop.Api.dll` | Your main assembly |
| `Shop.Api.pdb` | Symbols (optional in prod; useful for debugging) |
| `*.dll` | Your libraries + NuGet dependencies |
| `Shop.Api.deps.json` | Dependency graph / runtime resolution data |
| `Shop.Api.runtimeconfig.json` | Runtime options / tfm / shared framework |
| `web.config` | Present for IIS hosting scenarios |
| `appsettings*.json` | Configuration files copied to output |
| `wwwroot/` | Static files if any |
| `Shop.Api.staticwebassets*` | Static web asset manifests when applicable |

```
artifacts/api/
  Shop.Api.dll
  Shop.Api.deps.json
  Shop.Api.runtimeconfig.json
  appsettings.json
  appsettings.Production.json
  Microsoft.*.dll
  ... other deps ...
  web.config          (IIS)
```

### deps.json (idea)
Tells .NET which assemblies and versions belong to the app.

### runtimeconfig.json (idea)
```json
{
  "runtimeOptions": {
    "tfm": "net8.0",
    "framework": {
      "name": "Microsoft.AspNetCore.App",
      "version": "8.0.0"
    }
  }
}
```
Framework-dependent apps declare the shared framework they need.

### Self-contained extras
Many more runtime native binaries and a larger host executable layout.

---

## 8. Configuration and appsettings at Publish Time

Publish copies content files according to project settings. Usually `appsettings.json` **is included**.

```
Published appsettings.Production.json = non-secret defaults
Real secrets = environment variables at runtime
```

| Do | Don't |
|----|-------|
| Publish non-secret config | Bake production passwords into output |
| Set env on host | Assume `launchSettings` applies |
| Use Release config | Deploy Debug builds casually |

### ASPNETCORE_URLS
Published Kestrel listens based on:
```bash
ASPNETCORE_URLS=http://0.0.0.0:8080
```
or host reverse-proxy setup.

---

## 9. ReadyToRun, Single-File, Trimming (Awareness)

Advanced publish flags (know names; use when needed):

| Option | Intent |
|--------|--------|
| **ReadyToRun** | Precompile IL for faster startup |
| **Single-file** | Bundle into one executable |
| **Trimmed** | Remove unused code (careful with reflection) |
| **AOT** | Native ahead-of-time (special constraints) |

```bash
dotnet publish -c Release -r win-x64 --self-contained true \
  -p:PublishSingleFile=true \
  -p:PublishReadyToRun=true
```

Web APIs often start with **normal FDD publish** before exploring these.

---

## 10. Smoke-Testing Published Output

```bash
dotnet publish src/Shop.Api -c Release -o artifacts/api
cd artifacts/api
set ASPNETCORE_ENVIRONMENT=Production
set ASPNETCORE_URLS=http://localhost:8080
dotnet Shop.Api.dll
```

Then:
```bash
curl http://localhost:8080/health
curl http://localhost:8080/api/products
```

### Checklist
- [ ] Starts without missing assembly errors  
- [ ] Correct environment name  
- [ ] Connection string present via env  
- [ ] HTTPS/proxy headers OK behind reverse proxy  
- [ ] Static files load if needed  
- [ ] Version/commit visible in logs optional  

---

## 11. Knowledge Check

**Q1.** Difference between `build` and `publish`?  
**Q2.** FDD vs SCD — which includes the .NET runtime?  
**Q3.** How do you usually start an FDD published Web API?  
**Q4.** What is a RID?  
**Q5.** Purpose of `.deps.json` and `.runtimeconfig.json`?  
**Q6.** Should production secrets be inside the publish folder?  
**Q7.** Why publish `-c Release` for deployment?

### Mini practice
1. `dotnet publish` your API to `artifacts/api` as FDD  
2. List the folder and identify dll/deps/runtimeconfig/appsettings  
3. Run the published DLL locally with Production env  
4. Publish self-contained for `win-x64` or `linux-x64` into another folder  
5. Compare folder sizes  

### Answers (short)
1. Build compiles; publish produces deployable output  
2. Self-contained  
3. `dotnet Shop.Api.dll` (with env/urls set)  
4. Runtime Identifier targeting OS/arch  
5. Dependency graph + runtime framework options  
6. No — inject via env/vault at runtime  
7. Optimizations and non-debug production defaults  

---

## ✅ What You Should Feel Confident About

- [ ] Run `dotnet publish` with Release output  
- [ ] Choose FDD vs SCD for a scenario  
- [ ] Explain RID at a basic level  
- [ ] Recognize key publish folder files  
- [ ] Keep secrets out of published artifacts  
- [ ] Smoke-test a published build locally  

**Previous:** [01-configuration-for-environments.md](./01-configuration-for-environments.md)  
**Next:** [03-hosting-options-and-containers.md](./03-hosting-options-and-containers.md) — IIS, Kestrel/Nginx, Azure, Docker.
