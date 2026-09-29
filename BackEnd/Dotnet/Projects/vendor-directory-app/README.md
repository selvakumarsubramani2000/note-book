# 🏢 Vendor Directory Application

A full-stack web application for managing vendor information, built with React, .NET 8, and SQLite.

## 📚 Learning Project

This is a hands-on learning project designed to teach end-to-end web application development, from database design to cloud deployment.

---

## 🎯 Features

- ✅ User Authentication (Register/Login with JWT)
- ✅ Vendor CRUD Operations (Create, Read, Update, Delete)
- ✅ Search & Filter Vendors
- ✅ Role-Based Access Control (Admin/User)
- ✅ Export to Excel/CSV
- ✅ Responsive Design (Mobile-friendly)

---

## 🛠️ Tech Stack

### Frontend
- **React 18** - UI framework
- **React Router** - Navigation
- **Axios** - HTTP client
- **Vite** - Build tool

### Backend
- **.NET 8** - Web API framework
- **Entity Framework Core** - ORM
- **SQLite** - Database (development)
- **JWT** - Authentication
- **BCrypt** - Password hashing

### Deployment
- **Azure Static Web Apps** - Frontend hosting
- **Azure App Service** - Backend hosting
- **Azure SQL Database** - Production database

---

## 📁 Project Structure

```
vendor-directory-app/
├── backend/                    # .NET 8 Web API
│   ├── Controllers/
│   ├── Models/
│   ├── Services/
│   └── Data/
├── frontend/                   # React application
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   └── services/
│   └── public/
├── docs/                       # Documentation
│   ├── PROJECT_PLAN.md
│   ├── UI_MOCKUPS.md
│   ├── DATABASE_OPTIONS.md
│   └── ENVIRONMENT_SETUP.md
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- ✅ .NET 8 SDK
- ✅ Node.js (v18+)
- ✅ Visual Studio Code
- ✅ Git

### Quick Environment Check

Run this PowerShell script to verify your setup:

```powershell
.\check-environment.ps1
```

Or manually check:

```bash
dotnet --version    # Should show 8.0.x
node --version      # Should show v18.x or v20.x
npm --version       # Should show 9.x or 10.x
git --version       # Should show 2.x
```

---

## 📖 Documentation

- **[Project Plan](PROJECT_PLAN.md)** - Complete project overview and timeline
- **[UI Mockups](UI_MOCKUPS.md)** - Design wireframes and components
- **[Database Options](DATABASE_OPTIONS.md)** - Database setup guide (SQLite vs Azure SQL)
- **[Environment Setup](ENVIRONMENT_SETUP.md)** - Development environment configuration

---

## 🗄️ Database

### Development: SQLite
- **No installation required!**
- File-based database (`vendordirectory.db`)
- Perfect for learning and development
- Easy to reset and recreate

### Production: Azure SQL Database
- Cloud-based SQL Server
- Free tier available for learning
- Easy migration from SQLite

See [DATABASE_OPTIONS.md](DATABASE_OPTIONS.md) for detailed comparison.

---

## 📅 Development Phases

| Phase | Status | Description |
|-------|--------|-------------|
| **Phase 1** | ✅ Complete | Planning & Design |
| **Phase 2** | 🔄 In Progress | Environment Setup |
| **Phase 3** | ⏳ Pending | Database Setup |
| **Phase 4** | ⏳ Pending | Backend API Development |
| **Phase 5** | ⏳ Pending | Frontend Development |
| **Phase 6** | ⏳ Pending | Testing & Integration |
| **Phase 7** | ⏳ Pending | Azure Deployment |

---

## 💰 Cost Estimate

### Development
- **All tools**: FREE

### Azure Deployment (Optional)

**Free Tier (Recommended for Learning):**
- Azure SQL Database: $0/month
- Azure App Service: $0/month
- Azure Static Web Apps: $0/month
- **Total: $0/month**

**Basic Production:**
- Azure SQL Database (Basic): ~$5/month
- Azure App Service (B1): ~$13/month
- Azure Static Web Apps: $0/month
- **Total: ~$18/month**

---

## ⏱️ Timeline

**Total Time**: 2-4 weeks (part-time, 2-3 hours/day)

- Planning & Design: ✅ Complete
- Environment Setup: 1 day
- Database Setup: 1 day
- Backend Development: 3-5 days
- Frontend Development: 4-6 days
- Testing: 2-3 days
- Deployment: 2-3 days

---

## 🎓 Learning Objectives

By completing this project, you will learn:

1. ✅ Full-stack web development
2. ✅ RESTful API design
3. ✅ Database design and SQL
4. ✅ Authentication & Authorization (JWT)
5. ✅ React component architecture
6. ✅ State management
7. ✅ Cloud deployment (Azure)
8. ✅ DevOps basics

---

## 🆘 Need Help?

- Check the documentation in the `docs/` folder
- Review the authentication guide: `topics/authentication-authorization/02-dotnet-react/guide-auth-dotnet-react.md`
- Ask questions as you go!

---

## 📝 Next Steps

1. ✅ Review project plan
2. ⏳ Install Node.js (if not already installed)
3. ⏳ Run environment check script
4. ⏳ Create backend project
5. ⏳ Set up database
6. ⏳ Build API endpoints
7. ⏳ Create React frontend
8. ⏳ Deploy to Azure

---

**Ready to start coding?** 🚀

Let's build something amazing!

