# 🔄 CRUD Operations in Django

> **Trainer's Note:** CRUD stands for Create, Read, Update, Delete — the four basic operations every data-driven application needs. Django makes all four straightforward using views, forms, and the ORM.

---

## 📑 Table of Contents
1. [What is CRUD?](#1-what-is-crud)
2. [Create](#2-create)
3. [Read](#3-read)
4. [Update](#4-update)
5. [Delete](#5-delete)
6. [Wiring Up URLs](#6-wiring-up-urls)
7. [Knowledge Check](#7-knowledge-check)

---

## 1. What is CRUD?

| Letter | Operation | HTTP Method (typical) | ORM equivalent |
|--------|-----------|------------------------|------------------|
| C | Create | POST | `Model.objects.create()` |
| R | Read | GET | `Model.objects.all()` / `.get()` |
| U | Update | POST/PUT | `instance.save()` |
| D | Delete | POST/DELETE | `instance.delete()` |

### Real-world analogy
```
CRUD = managing a library catalog
  Create -> add a new book record
  Read   -> look up book details
  Update -> correct a book's info
  Delete -> remove a book from the catalog
```

---

## 2. Create

```python
# app/views.py
from .models import Student
from .forms import StudentForm
from django.shortcuts import render, redirect

def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student-list")
    else:
        form = StudentForm()
    return render(request, "student_form.html", {"form": form})
```

---

## 3. Read

```python
def student_list(request):
    students = Student.objects.all()
    return render(request, "student_list.html", {"students": students})

def student_detail(request, pk):
    student = Student.objects.get(pk=pk)
    return render(request, "student_detail.html", {"student": student})
```

---

## 4. Update

```python
def student_update(request, pk):
    student = Student.objects.get(pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("student-list")
    else:
        form = StudentForm(instance=student)
    return render(request, "student_form.html", {"form": form})
```

---

## 5. Delete

```python
def student_delete(request, pk):
    student = Student.objects.get(pk=pk)
    if request.method == "POST":
        student.delete()
        return redirect("student-list")
    return render(request, "student_confirm_delete.html", {"student": student})
```

### Beginner tip
Always require `POST` (not `GET`) for delete/update actions — a `GET` request should never change data, since browsers, crawlers, and link previews can trigger `GET` requests unintentionally.

---

## 6. Wiring Up URLs

```python
# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("students/", views.student_list, name="student-list"),
    path("students/add/", views.student_create, name="student-create"),
    path("students/<int:pk>/", views.student_detail, name="student-detail"),
    path("students/<int:pk>/edit/", views.student_update, name="student-update"),
    path("students/<int:pk>/delete/", views.student_delete, name="student-delete"),
]
```

---

## 7. Knowledge Check

1. Which HTTP method should delete/update actions use, and why not `GET`?
2. Write the ORM call to fetch a single `Student` by primary key `pk`.
3. What does `instance=student` do when passed into a `ModelForm`?
4. Map each CRUD letter to its corresponding ORM method.

---

**Previous:** [← User Registration & Login](./04-User-Registration-and-Login.md)
**Next:** [Mail API Integration →](./06-Mail-API-Integration.md)
