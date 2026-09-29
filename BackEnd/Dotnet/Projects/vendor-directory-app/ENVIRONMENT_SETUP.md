# Environment Setup Guide

## ✅ What You Already Have

- ✅ .NET 8 SDK
- ✅ Visual Studio Code
- ✅ Git

Great! You're almost ready to start coding!

---

## 📦 What You Still Need

### 1. Node.js (Required for React)

**What is it?**
- JavaScript runtime for running React development server
- Includes npm (Node Package Manager) for installing React packages

**Check if installed:**
```bash
node --version
npm --version
```

**If not installed:**

#### Windows:
1. Download from: https://nodejs.org/
2. Choose **LTS version** (Long Term Support) - Currently v20.x
3. Run installer with default settings
4. Restart terminal/VS Code

#### Verify installation:
```bash
node --version    # Should show v20.x.x or v18.x.x
npm --version     # Should show 10.x.x or higher
```

---

### 2. Database (Choose One)

**Recommended: SQLite** (No installation needed!)
- See `DATABASE_OPTIONS.md` for details
- Just a NuGet package - we'll install it when creating the backend

**Alternative: Azure SQL Database**
- Requires Azure account
- Free tier available
- See `DATABASE_OPTIONS.md` for setup

---

## 🔧 Optional Tools (Recommended)

### 1. Postman or Thunder Client

**What is it?**
- Tool for testing API endpoints
- Very useful for backend development

**Options:**

**A. Thunder Client (VS Code Extension)** - Recommended
```bash
# Install in VS Code:
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search "Thunder Client"
4. Click Install
```

**B. Postman (Standalone App)**
- Download from: https://www.postman.com/downloads/

---

### 2. React Developer Tools (Browser Extension)

**What is it?**
- Browser extension for debugging React apps

**Install:**
- **Chrome**: https://chrome.google.com/webstore (search "React Developer Tools")
- **Edge**: https://microsoftedge.microsoft.com/addons (search "React Developer Tools")
- **Firefox**: https://addons.mozilla.org (search "React Developer Tools")

---

### 3. VS Code Extensions (Recommended)

Open VS Code and install these extensions:

```
1. C# Dev Kit (Microsoft) - For .NET development
2. ESLint - JavaScript linting
3. Prettier - Code formatter
4. Thunder Client - API testing
5. SQLite Viewer - View SQLite database files
6. GitLens - Enhanced Git features
```

**How to install:**
1. Open VS Code
2. Click Extensions icon (Ctrl+Shift+X)
3. Search for each extension
4. Click Install

---

## ✅ Verification Checklist

Run these commands to verify everything is installed:

```bash
# .NET SDK
dotnet --version
# Expected: 8.0.x

# Node.js
node --version
# Expected: v18.x.x or v20.x.x

# npm
npm --version
# Expected: 9.x.x or 10.x.x

# Git
git --version
# Expected: 2.x.x
```

---

## 📁 Project Folder Structure

Let's organize our workspace:

```
HandsOn/
└── vendor-directory-app/
    ├── backend/              (We'll create this - .NET API)
    ├── frontend/             (We'll create this - React app)
    ├── docs/                 (Documentation)
    │   ├── PROJECT_PLAN.md
    │   ├── UI_MOCKUPS.md
    │   ├── DATABASE_OPTIONS.md
    │   └── ENVIRONMENT_SETUP.md
    └── README.md
```

---

## 🚀 Next Steps

Once you have Node.js installed, we'll:

1. ✅ Create the backend (.NET Web API)
2. ✅ Set up SQLite database
3. ✅ Create the frontend (React app)
4. ✅ Connect them together

---

## 🆘 Troubleshooting

### Node.js not found after installation
- **Solution**: Restart your terminal/VS Code
- **Check**: Make sure Node.js is in your PATH

### .NET command not found
- **Solution**: Reinstall .NET 8 SDK from https://dotnet.microsoft.com/download
- **Verify**: Run `dotnet --version`

### Port already in use
- **Backend (5000/5001)**: Another app is using the port
  - Solution: Stop other apps or change port in `launchSettings.json`
- **Frontend (3000/5173)**: Another React app is running
  - Solution: Stop other React apps or use different port

---

## 📝 Installation Summary

| Tool | Status | Required? | Purpose |
|------|--------|-----------|---------|
| .NET 8 SDK | ✅ Installed | Yes | Backend API |
| VS Code | ✅ Installed | Yes | Code editor |
| Git | ✅ Installed | Yes | Version control |
| Node.js | ⏳ Pending | Yes | React development |
| SQLite | ⏳ Pending | Yes | Database (NuGet package) |
| Thunder Client | ⏳ Optional | No | API testing |
| React DevTools | ⏳ Optional | No | React debugging |

---

## ✅ Ready to Code?

Once you have **Node.js** installed, you're ready to start building!

**Quick Check:**
```bash
# Run this command:
node --version && npm --version && dotnet --version && git --version

# If all show version numbers, you're ready! 🎉
```

---

**What's Next?**

Let me know when Node.js is installed, and we'll:
1. Create the backend project
2. Set up SQLite database
3. Build authentication API
4. Create React frontend

**Or if you already have Node.js**, let me know and we'll start coding immediately! 🚀

