# Vendor Directory Application - Project Plan

## 📋 Project Overview

**Application Name**: Vendor Directory
**Tech Stack**: React + .NET 8 + SQLite (Dev) / Azure SQL (Production) + Azure
**Purpose**: Simple vendor management system for learning end-to-end development
**Target Completion**: 2-4 weeks (part-time)
**Database**: SQLite for development (no installation needed!)

---

## 🎯 Features & Requirements

### Core Features (MVP)

1. **User Authentication**
   - User registration
   - User login/logout
   - JWT-based authentication
   - Protected routes

2. **Vendor Management (CRUD)**
   - ✅ **Create**: Add new vendors
   - ✅ **Read**: View vendor list and details
   - ✅ **Update**: Edit vendor information
   - ✅ **Delete**: Remove vendors

3. **Vendor Information**
   - Vendor Name
   - Contact Person
   - Email
   - Phone Number
   - Address (Street, City, State, Zip, Country)
   - Status (Active/Inactive)
   - Category (Supplier, Manufacturer, Distributor)
   - Created Date
   - Notes

4. **Search & Filter**
   - Search by vendor name
   - Filter by status (Active/Inactive)
   - Filter by category

5. **Export**
   - Export vendor list to Excel/CSV

### User Roles

- **Admin**: Full access (CRUD all vendors)
- **User**: Read-only access (view vendors)

---

## 🗄️ Database Schema

### Tables

#### 1. Users Table
```sql
CREATE TABLE Users (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Email NVARCHAR(255) NOT NULL UNIQUE,
    PasswordHash NVARCHAR(500) NOT NULL,
    Name NVARCHAR(100) NOT NULL,
    Role NVARCHAR(50) NOT NULL DEFAULT 'User',
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE()
);
```

#### 2. Vendors Table
```sql
CREATE TABLE Vendors (
    Id INT PRIMARY KEY IDENTITY(1,1),
    VendorName NVARCHAR(200) NOT NULL,
    ContactPerson NVARCHAR(100),
    Email NVARCHAR(255),
    Phone NVARCHAR(50),
    Street NVARCHAR(200),
    City NVARCHAR(100),
    State NVARCHAR(50),
    ZipCode NVARCHAR(20),
    Country NVARCHAR(100),
    Status NVARCHAR(20) NOT NULL DEFAULT 'Active',
    Category NVARCHAR(50),
    Notes NVARCHAR(MAX),
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedAt DATETIME2,
    CreatedBy INT FOREIGN KEY REFERENCES Users(Id)
);
```

---

## 🎨 UI/UX Design (Simple Wireframes)

### Pages

1. **Login Page** (`/login`)
   - Email input
   - Password input
   - Login button
   - Link to Register

2. **Register Page** (`/register`)
   - Name input
   - Email input
   - Password input
   - Register button
   - Link to Login

3. **Dashboard** (`/dashboard`)
   - Welcome message
   - Quick stats (Total vendors, Active, Inactive)
   - Navigation to Vendor List

4. **Vendor List Page** (`/vendors`)
   - Search bar
   - Filter dropdowns (Status, Category)
   - Vendor table (Name, Contact, Email, Phone, Status, Actions)
   - Add Vendor button (Admin only)
   - Export button

5. **Add/Edit Vendor Page** (`/vendors/new` or `/vendors/:id/edit`)
   - Form with all vendor fields
   - Save button
   - Cancel button

6. **Vendor Details Page** (`/vendors/:id`)
   - Display all vendor information
   - Edit button (Admin only)
   - Delete button (Admin only)
   - Back to list button

---

## 🏗️ Architecture

### Backend (.NET 8 Web API)

**Project Structure**:
```
VendorDirectory.API/
├── Controllers/
│   ├── AuthController.cs
│   └── VendorsController.cs
├── Models/
│   ├── User.cs
│   └── Vendor.cs
├── DTOs/
│   ├── AuthDTOs.cs
│   └── VendorDTOs.cs
├── Services/
│   ├── IJwtService.cs
│   ├── JwtService.cs
│   ├── IVendorService.cs
│   └── VendorService.cs
├── Data/
│   └── ApplicationDbContext.cs
└── Program.cs
```

**API Endpoints**:
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user
- `GET /api/vendors` - Get all vendors (with search/filter)
- `GET /api/vendors/{id}` - Get vendor by ID
- `POST /api/vendors` - Create vendor (Admin only)
- `PUT /api/vendors/{id}` - Update vendor (Admin only)
- `DELETE /api/vendors/{id}` - Delete vendor (Admin only)
- `GET /api/vendors/export` - Export vendors to Excel

### Frontend (React 18)

**Project Structure**:
```
vendor-directory-frontend/
├── src/
│   ├── components/
│   │   ├── Auth/
│   │   │   ├── Login.jsx
│   │   │   └── Register.jsx
│   │   ├── Vendors/
│   │   │   ├── VendorList.jsx
│   │   │   ├── VendorForm.jsx
│   │   │   └── VendorDetails.jsx
│   │   ├── Layout/
│   │   │   ├── Navbar.jsx
│   │   │   └── ProtectedRoute.jsx
│   │   └── Dashboard.jsx
│   ├── context/
│   │   └── AuthContext.jsx
│   ├── services/
│   │   └── api.js
│   ├── App.jsx
│   └── main.jsx
```

---

## ⏱️ Development Timeline

| Phase | Tasks | Duration |
|-------|-------|----------|
| **Phase 1** | Planning & Design | ✅ Complete |
| **Phase 2** | Environment Setup | 1 day |
| **Phase 3** | Database Setup | 1 day |
| **Phase 4** | Backend API | 3-5 days |
| **Phase 5** | Frontend | 4-6 days |
| **Phase 6** | Testing | 2-3 days |
| **Phase 7** | Azure Deployment | 2-3 days |

**Total**: 2-4 weeks (part-time, 2-3 hours/day)

---

## 💰 Cost Estimate

### Development (Free)
- All tools are free (VS Code, .NET SDK, Node.js, SQL Server Express)

### Azure Deployment

**Option 1: Free Tier (Recommended for Learning)**
- Azure SQL Database (Free tier): $0/month
- Azure App Service (F1): $0/month
- Azure Static Web Apps: $0/month
- **Total: $0/month**

**Option 2: Basic Production**
- Azure SQL Database (Basic): ~$5/month
- Azure App Service (B1): ~$13/month
- Azure Static Web Apps: $0/month
- **Total: ~$18/month**

---

## 🚀 Next Steps

1. ✅ Review this plan
2. Set up development environment
3. Create database schema
4. Build backend API
5. Build frontend
6. Test locally
7. Deploy to Azure

---

**Ready to proceed?** Let's start with Phase 2: Environment Setup!

