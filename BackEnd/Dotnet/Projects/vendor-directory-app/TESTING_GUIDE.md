# 🧪 Backend API Testing Guide

## ✅ Server Status

**Backend is running on:** `http://localhost:5000`  
**Swagger UI:** `http://localhost:5000/swagger` (Already opened in your browser!)

---

## 📋 Testing Workflow

Follow these steps to test the complete authentication and vendor management flow:

### **Step 1: Register a New User** 👤

1. In Swagger UI, find **`POST /api/auth/register`**
2. Click **"Try it out"**
3. Replace the request body with:

```json
{
  "email": "admin@vendordir.com",
  "password": "Admin123!",
  "name": "Admin User"
}
```

4. Click **"Execute"**
5. You should see **Response Code: 200** with message: `"User registered successfully"`

---

### **Step 2: Login to Get JWT Token** 🔐

1. Find **`POST /api/auth/login`**
2. Click **"Try it out"**
3. Use the same credentials:

```json
{
  "email": "admin@vendordir.com",
  "password": "Admin123!"
}
```

4. Click **"Execute"**
5. **Copy the token** from the response (it looks like: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`)

**Response will look like:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "admin@vendordir.com",
    "name": "Admin User",
    "role": "User"
  }
}
```

---

### **Step 3: Authorize Swagger with JWT Token** 🔓

1. At the top of Swagger UI, click the **"Authorize"** button (🔒 icon)
2. In the popup, enter: `Bearer <your-token-here>`
   - Example: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
3. Click **"Authorize"**
4. Click **"Close"**

Now you're authenticated! 🎉

---

### **Step 4: Test Vendor Endpoints** 📋

#### **4.1 Get All Vendors (Empty List)**

1. Find **`GET /api/vendors`**
2. Click **"Try it out"**
3. Click **"Execute"**
4. You should see **Response Code: 200** with an empty array `[]`

---

#### **4.2 Create a Vendor** ➕

**Note:** This requires Admin role. We need to manually update the user role in the database first.

**Option A: Update User Role to Admin (Recommended)**

1. Stop the server (Press Ctrl+C in the terminal running `dotnet run`)
2. Open the database file with a SQLite viewer or run this command:

```bash
# In PowerShell (from backend folder)
sqlite3 vendordirectory.db "UPDATE Users SET Role = 'Admin' WHERE Email = 'admin@vendordir.com';"
```

3. Restart the server: `dotnet run`
4. Login again to get a new token with Admin role
5. Re-authorize Swagger with the new token

**Option B: Test as Regular User (Read-Only)**

Skip creating vendors and only test the GET endpoints.

---

#### **4.3 Create Your First Vendor** (Admin only)

1. Find **`POST /api/vendors`**
2. Click **"Try it out"**
3. Use this sample data:

```json
{
  "vendorName": "Acme Corporation",
  "contactPerson": "John Smith",
  "email": "john@acme.com",
  "phone": "555-0100",
  "street": "123 Business Ave",
  "city": "New York",
  "state": "NY",
  "zipCode": "10001",
  "country": "USA",
  "status": "Active",
  "category": "Supplier",
  "notes": "Primary office supplies vendor"
}
```

4. Click **"Execute"**
5. You should see **Response Code: 201** with the created vendor data

---

#### **4.4 Get All Vendors (With Data)**

1. Go back to **`GET /api/vendors`**
2. Click **"Execute"**
3. You should now see your vendor in the list!

---

#### **4.5 Get Vendor by ID**

1. Find **`GET /api/vendors/{id}`**
2. Click **"Try it out"**
3. Enter `1` in the **id** field
4. Click **"Execute"**
5. You should see the vendor details

---

#### **4.6 Update a Vendor** (Admin only)

1. Find **`PUT /api/vendors/{id}`**
2. Click **"Try it out"**
3. Enter `1` in the **id** field
4. Modify the vendor data (e.g., change phone number):

```json
{
  "vendorName": "Acme Corporation",
  "contactPerson": "John Smith",
  "email": "john@acme.com",
  "phone": "555-0199",
  "street": "123 Business Ave",
  "city": "New York",
  "state": "NY",
  "zipCode": "10001",
  "country": "USA",
  "status": "Active",
  "category": "Supplier",
  "notes": "Updated contact information"
}
```

5. Click **"Execute"**
6. You should see **Response Code: 200** with updated data

---

#### **4.7 Test Search & Filters**

1. Go to **`GET /api/vendors`**
2. Try different filters:
   - **search:** `acme`
   - **status:** `Active`
   - **category:** `Supplier`
3. Click **"Execute"**

---

#### **4.8 Delete a Vendor** (Admin only)

1. Find **`DELETE /api/vendors/{id}`**
2. Click **"Try it out"**
3. Enter the vendor ID
4. Click **"Execute"**
5. You should see **Response Code: 200** with message: `"Vendor deleted successfully"`

---

## 🎯 Quick Testing Checklist

- [ ] Register a user
- [ ] Login and get JWT token
- [ ] Authorize Swagger with token
- [ ] Get all vendors (empty)
- [ ] Update user role to Admin (if testing create/update/delete)
- [ ] Create a vendor
- [ ] Get all vendors (with data)
- [ ] Get vendor by ID
- [ ] Update vendor
- [ ] Test search filters
- [ ] Delete vendor

---

## 🛠️ Troubleshooting

**Problem:** "401 Unauthorized" error
- **Solution:** Make sure you've authorized Swagger with the JWT token

**Problem:** "403 Forbidden" on create/update/delete
- **Solution:** Your user needs Admin role. Update the database as shown above.

**Problem:** Server not responding
- **Solution:** Check if `dotnet run` is still running in the terminal

---

## 📝 Next Steps

Once testing is complete:
1. ✅ Backend is verified and working
2. ⏭️ Ready to build the React frontend
3. ⏭️ Connect frontend to this API

---

**Happy Testing! 🚀**

