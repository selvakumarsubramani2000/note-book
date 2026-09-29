# Vendor Directory - UI Mockups

## 🎨 Design Principles

- **Simple & Clean**: Minimalist design, easy to navigate
- **Responsive**: Works on desktop, tablet, and mobile
- **Accessible**: WCAG 2.1 AA compliant
- **Consistent**: Uniform colors, fonts, and spacing

---

## 🎨 Color Scheme

```
Primary: #2563eb (Blue)
Secondary: #64748b (Slate)
Success: #10b981 (Green)
Danger: #ef4444 (Red)
Warning: #f59e0b (Amber)
Background: #f8fafc (Light Gray)
Text: #1e293b (Dark Slate)
```

---

## 📱 Page Mockups

### 1. Login Page

```
┌─────────────────────────────────────────┐
│         VENDOR DIRECTORY                │
│                                         │
│    ┌─────────────────────────────┐     │
│    │                             │     │
│    │         LOGIN               │     │
│    │                             │     │
│    │  Email:                     │     │
│    │  [___________________]      │     │
│    │                             │     │
│    │  Password:                  │     │
│    │  [___________________]      │     │
│    │                             │     │
│    │  [     LOGIN BUTTON    ]    │     │
│    │                             │     │
│    │  Don't have an account?     │     │
│    │  Register                   │     │
│    │                             │     │
│    └─────────────────────────────┘     │
│                                         │
└─────────────────────────────────────────┘
```

---

### 2. Dashboard Page

```
┌─────────────────────────────────────────────────────────┐
│  VENDOR DIRECTORY    Dashboard | Vendors | Logout       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Welcome, John Doe! (Admin)                            │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Total        │  │ Active       │  │ Inactive     │ │
│  │ Vendors      │  │ Vendors      │  │ Vendors      │ │
│  │              │  │              │  │              │ │
│  │    125       │  │    98        │  │    27        │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                         │
│  Quick Actions:                                         │
│  [+ Add Vendor]  [View All Vendors]  [Export Data]     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

### 3. Vendor List Page

```
┌─────────────────────────────────────────────────────────────────────┐
│  VENDOR DIRECTORY    Dashboard | Vendors | Logout                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Vendors                                      [+ Add Vendor]        │
│                                                                     │
│  Search: [____________]  Status: [All ▼]  Category: [All ▼]        │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Name          │ Contact    │ Email         │ Status │ Actions│  │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │ ABC Corp      │ John Smith │ j@abc.com     │ Active │ 👁 ✏ 🗑│  │
│  │ XYZ Ltd       │ Jane Doe   │ jane@xyz.com  │ Active │ 👁 ✏ 🗑│  │
│  │ 123 Inc       │ Bob Jones  │ bob@123.com   │ Inactive│ 👁 ✏ 🗑│  │
│  │ ...           │ ...        │ ...           │ ...    │ ...   │  │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Showing 1-10 of 125 vendors        [< Previous] [Next >]          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 4. Add/Edit Vendor Form

```
┌─────────────────────────────────────────────────────────┐
│  VENDOR DIRECTORY    Dashboard | Vendors | Logout       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Add New Vendor                                         │
│                                                         │
│  Vendor Information                                     │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Vendor Name: *                                  │   │
│  │ [_______________________________________]       │   │
│  │                                                 │   │
│  │ Contact Person:                                 │   │
│  │ [_______________________________________]       │   │
│  │                                                 │   │
│  │ Email: *                                        │   │
│  │ [_______________________________________]       │   │
│  │                                                 │   │
│  │ Phone:                                          │   │
│  │ [_______________________________________]       │   │
│  │                                                 │   │
│  │ Category: *                                     │   │
│  │ [Supplier ▼]                                    │   │
│  │                                                 │   │
│  │ Status: *                                       │   │
│  │ [Active ▼]                                      │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  Address                                                │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Street:                                         │   │
│  │ [_______________________________________]       │   │
│  │                                                 │   │
│  │ City:              State:        Zip:          │   │
│  │ [__________]       [_____]       [______]      │   │
│  │                                                 │   │
│  │ Country:                                        │   │
│  │ [_______________________________________]       │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  Notes                                                  │
│  ┌─────────────────────────────────────────────────┐   │
│  │ [                                               ]│   │
│  │ [                                               ]│   │
│  │ [                                               ]│   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  [  Save  ]  [  Cancel  ]                              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

### 5. Vendor Details Page

```
┌─────────────────────────────────────────────────────────┐
│  VENDOR DIRECTORY    Dashboard | Vendors | Logout       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [← Back to List]                                       │
│                                                         │
│  ABC Corporation                    [Edit] [Delete]     │
│  Status: ✅ Active                                      │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Contact Information                             │   │
│  │ ─────────────────────────────────────────────── │   │
│  │ Contact Person: John Smith                      │   │
│  │ Email: john.smith@abc.com                       │   │
│  │ Phone: +1 (555) 123-4567                        │   │
│  │                                                 │   │
│  │ Address                                         │   │
│  │ ─────────────────────────────────────────────── │   │
│  │ 123 Main Street                                 │   │
│  │ New York, NY 10001                              │   │
│  │ United States                                   │   │
│  │                                                 │   │
│  │ Additional Information                          │   │
│  │ ─────────────────────────────────────────────── │   │
│  │ Category: Supplier                              │   │
│  │ Created: Jan 15, 2026                           │   │
│  │ Last Updated: Feb 1, 2026                       │   │
│  │                                                 │   │
│  │ Notes                                           │   │
│  │ ─────────────────────────────────────────────── │   │
│  │ Preferred supplier for office supplies.        │   │
│  │ Net 30 payment terms.                           │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Component Breakdown

### Reusable Components

1. **Button** - Primary, Secondary, Danger variants
2. **Input** - Text, Email, Password, TextArea
3. **Select** - Dropdown with options
4. **Card** - Container for content
5. **Table** - Data display with sorting
6. **Modal** - Confirmation dialogs
7. **Alert** - Success/Error messages
8. **Navbar** - Top navigation
9. **Badge** - Status indicators

---

## 📱 Responsive Breakpoints

- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

---

**Next**: Let's implement these designs in React!

