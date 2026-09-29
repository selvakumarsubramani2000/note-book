# 🛠️ Django Admin Console

> **Trainer's Note:** Django automatically generates a full admin website for managing your data — add, edit, delete, search — without writing any HTML or views yourself.

---

## 📑 Table of Contents
1. [What is the Admin Console?](#1-what-is-the-admin-console)
2. [Creating a Superuser](#2-creating-a-superuser)
3. [Registering a Model](#3-registering-a-model)
4. [Customizing the Admin View](#4-customizing-the-admin-view)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is the Admin Console?

Every Django project ships with `/admin/` — a ready-made dashboard for managing database records visually.

### Real-world analogy
```
Django Admin = a free back-office control panel that comes with the building
  You don't build the reception desk yourself — it's already there,
  you just decide which rooms (models) it can access
```

---

## 2. Creating a Superuser

```bash
python manage.py createsuperuser
# Prompts for username, email, password
```

Then log in at `http://127.0.0.1:8000/admin/` with those credentials.

---

## 3. Registering a Model

By default, models don't show up in the admin — you must **register** them.

```python
# app/admin.py
from django.contrib import admin
from .models import Student

admin.site.register(Student)
```

Now `Student` records can be viewed, added, edited, and deleted directly from `/admin/`.

---

## 4. Customizing the Admin View

Use `ModelAdmin` to control which columns show, add search/filtering, etc.

```python
# app/admin.py
from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "age")   # columns shown in the list view
    search_fields = ("name", "email")          # adds a search box
    list_filter = ("age",)                     # adds a sidebar filter

admin.site.register(Student, StudentAdmin)
```

### Beginner tip
The admin console is a huge productivity boost during development — you can inspect and fix data without writing a single custom view, and it's often used internally by non-developer staff (e.g., content editors) in production too.

---

## 5. Knowledge Check

1. What command creates an admin superuser account?
2. Why doesn't a model appear in `/admin/` automatically?
3. What does `list_display` control in a `ModelAdmin` class?
4. Register a `Book` model in the admin with search enabled on its `title` field.

---

**Previous:** [← Model Forms & Sending Data to DB](./02-Model-Forms-and-DB.md)
**Next:** [User Registration & Login →](./04-User-Registration-and-Login.md)
