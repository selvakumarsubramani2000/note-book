# 🚀 How to Build and Run the Backend

## 📍 Prerequisites

Make sure you're in the backend directory:
```bash
cd HandsOn/vendor-directory-app/backend
```

---

## 🏗️ Building the Backend

### **Option 1: Build Only (Compile without running)**
```bash
dotnet build
```

**What it does:**
- Compiles the C# code
- Checks for errors
- Creates DLL files in `bin/Debug/net9.0/`
- Does NOT run the application

**When to use:**
- To check if your code compiles
- Before committing code to Git
- To verify there are no syntax errors

---

### **Option 2: Restore Packages (if needed)**
```bash
dotnet restore
```

**What it does:**
- Downloads all NuGet packages
- Updates dependencies
- Fixes package reference issues

**When to use:**
- After cloning the project
- After adding new packages
- If you get "package not found" errors

---

## ▶️ Running the Backend

### **Option 1: Run (Build + Start)**
```bash
dotnet run
```

**What it does:**
- Builds the project (if needed)
- Starts the web server
- Runs on `http://localhost:5000`
- Keeps running until you press `Ctrl+C`

**Output you'll see:**
```
info: Microsoft.Hosting.Lifetime[14]
      Now listening on: http://localhost:5000
info: Microsoft.Hosting.Lifetime[0]
      Application started. Press Ctrl+C to shut down.
```

---

### **Option 2: Run with Hot Reload (Development)**
```bash
dotnet watch run
```

**What it does:**
- Same as `dotnet run`
- **Automatically restarts** when you change code
- Great for development!

**When to use:**
- During active development
- When making frequent code changes
- Testing changes quickly

---

### **Option 3: Run in Production Mode**
```bash
dotnet run --configuration Release
```

**What it does:**
- Builds with optimizations
- Runs in production mode
- Better performance

---

## 🛑 Stopping the Backend

### **If running in terminal:**
Press `Ctrl+C` in the terminal where `dotnet run` is running

### **If running in background:**
1. Find the process:
   ```bash
   # Windows PowerShell
   Get-Process -Name "VendorDirectory.API" | Stop-Process
   
   # Or find by port
   netstat -ano | findstr :5000
   # Then kill the process ID
   taskkill /PID <process-id> /F
   ```

---

## 🧹 Cleaning the Project

### **Clean build artifacts:**
```bash
dotnet clean
```

**What it does:**
- Removes `bin/` and `obj/` folders
- Cleans up compiled files
- Fresh start for building

**When to use:**
- Before rebuilding from scratch
- If you have build errors
- To save disk space

---

## 🔄 Complete Rebuild

```bash
dotnet clean
dotnet restore
dotnet build
dotnet run
```

Or in one line:
```bash
dotnet clean && dotnet restore && dotnet build && dotnet run
```

---

## 📊 Checking Build Information

### **Check .NET version:**
```bash
dotnet --version
```

### **List installed packages:**
```bash
dotnet list package
```

### **Check project info:**
```bash
dotnet --info
```

---

## 🌐 Accessing the Backend

Once running, you can access:

| URL | Description |
|-----|-------------|
| `http://localhost:5000` | Base API URL |
| `http://localhost:5000/swagger` | Swagger UI (API Documentation) |
| `http://localhost:5000/api/auth/login` | Example endpoint |
| `http://localhost:5000/api/vendors` | Example endpoint |

---

## 🐛 Troubleshooting

### **Problem: Port already in use**
```
Failed to bind to address http://127.0.0.1:5000: address already in use
```

**Solution:**
1. Stop the existing process using port 5000
2. Or change the port in `Properties/launchSettings.json`

---

### **Problem: Build errors**
```
Build FAILED
```

**Solution:**
```bash
dotnet clean
dotnet restore
dotnet build
```

---

### **Problem: Database not found**
```
SQLite Error: no such table: Users
```

**Solution:**
```bash
dotnet ef database update
```

---

### **Problem: Package errors**
```
error NU1202: Package X is not compatible
```

**Solution:**
```bash
dotnet restore --force
```

---

## 📝 Quick Reference

| Command | Purpose |
|---------|---------|
| `dotnet build` | Compile the code |
| `dotnet run` | Build and run |
| `dotnet watch run` | Run with auto-reload |
| `dotnet clean` | Remove build files |
| `dotnet restore` | Download packages |
| `dotnet test` | Run tests (when added) |
| `dotnet ef database update` | Update database |
| `dotnet ef migrations add <name>` | Create migration |

---

## 🎯 Typical Development Workflow

### **Starting your day:**
```bash
cd HandsOn/vendor-directory-app/backend
dotnet watch run
```

### **Making changes:**
1. Edit code in VS Code
2. Save file
3. Watch automatically reloads
4. Test in Swagger UI

### **Before committing:**
```bash
dotnet build
# Make sure it builds successfully
```

### **Ending your day:**
Press `Ctrl+C` to stop the server

---

## 🚀 Production Deployment

### **Build for production:**
```bash
dotnet publish -c Release -o ./publish
```

**What it does:**
- Creates optimized build
- Outputs to `./publish` folder
- Ready for deployment

---

**That's it! You're ready to build and run the backend! 🎉**

