# 📦 Package Management with NuGet in C#

> **Trainer's Note:** NuGet is the package manager for .NET. It lets you add shared libraries (JSON, logging, testing, etc.) instead of writing everything yourself.

---

## 📑 Table of Contents
1. [What is NuGet?](#1-what-is-nuget)
2. [Add / Remove Packages](#2-add--remove-packages)
3. [Where Packages Are Recorded](#3-where-packages-are-recorded)
4. [Practical Tips](#4-practical-tips)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is NuGet?

**NuGet** delivers reusable .NET libraries as packages.

Examples:
- `Newtonsoft.Json`
- `Serilog`
- `xunit`
- `Swashbuckle.AspNetCore`

### Real-world analogy
```
NuGet = app store for code libraries
  install package
  update package
  remove package you no longer need
```

---

## 2. Add / Remove Packages

### Using .NET CLI
```bash
dotnet add package Newtonsoft.Json
dotnet add package Serilog

dotnet remove package Newtonsoft.Json
dotnet restore
```

### Using Visual Studio
- right-click project → **Manage NuGet Packages**
- Browse / Installed / Updates tabs

### Using Package Manager Console
```powershell
Install-Package Newtonsoft.Json
Uninstall-Package Newtonsoft.Json
```

---

## 3. Where Packages Are Recorded

In modern SDK-style projects, packages appear in the `.csproj` file:

```xml
<ItemGroup>
  <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
  <PackageReference Include="xunit" Version="2.6.0" />
</ItemGroup>
```

### Restore
```bash
dotnet restore
```

Downloads/resolves packages so the project can build.

### Private feeds (concept)
Companies may use private NuGet feeds for internal packages.  
Public packages usually come from nuget.org.

---

## 4. Practical Tips

| Tip | Why |
|-----|-----|
| Add only needed packages | smaller surface and fewer conflicts |
| Prefer maintained packages | security/support |
| Pin versions intentionally | reproducible builds |
| Read package docs quickly | correct setup (especially DI/logging) |
| Commit csproj package refs | team shares dependencies |

### Common beginner flow
```
1) Create project
2) dotnet add package ...
3) write code using package APIs
4) dotnet build / dotnet test / run app
```

### Troubleshooting basics
- package not found → check name/feed
- version conflict → review package versions
- restore failed → network/feed auth issues

---

## 5. Knowledge Check

1. What is NuGet used for?
2. Which command adds a package with CLI?
3. Where are package references stored in modern projects?
4. Why is `dotnet restore` important?
5. Give 2 examples of packages you might add to a web API.

---

**Previous:** [← Unit Testing](./04-Unit-Testing-NUnit-xUnit-MSTest.md)

🎉 **Advanced Usage track complete!** JSON/XML, serialization, HttpClient, DI, unit testing frameworks, and NuGet package management are now separate practical guides.
