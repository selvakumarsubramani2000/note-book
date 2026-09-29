# 💾 Sending Data to the Database & Model Forms

> **Trainer's Note:** Once a form is validated, the data usually needs to be saved into the database. Django's `ModelForm` connects a form directly to a Model, so you don't have to manually copy each field.

---

## 📑 Table of Contents
1. [Sending Validated Data to the DB (Manual Way)](#1-sending-validated-data-to-the-db-manual-way)
2. [What is a ModelForm?](#2-what-is-a-modelform)
3. [Creating a ModelForm](#3-creating-a-modelform)
4. [Saving a ModelForm](#4-saving-a-modelform)
5. [Updating an Existing Record](#5-updating-an-existing-record)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. Sending Validated Data to the DB (Manual Way)

Using a regular `forms.Form`, you manually take the cleaned data and create a model instance yourself.

```python
def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            Message.objects.create(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                text=form.cleaned_data["message"],
            )
    return render(request, "contact.html", {"form": form})
```

This works, but repeats field names twice — once in the form, once when saving. **`ModelForm`** removes that repetition.

---

## 2. What is a ModelForm?

A `ModelForm` automatically generates form fields **based on a Model**, and can save directly to the database with `.save()`.

### Real-world analogy
```
Regular Form  = a blank sheet of paper you design yourself
ModelForm     = a pre-printed form that already matches your filing cabinet's folders (Model fields)
```

---

## 3. Creating a ModelForm

```python
# app/models.py
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
```

```python
# app/forms.py
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["name", "email", "age"]   # or fields = "__all__"
```

---

## 4. Saving a ModelForm

```python
# app/views.py
from .forms import StudentForm

def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()   # automatically inserts a new row!
            return redirect("student-list")
    else:
        form = StudentForm()
    return render(request, "add_student.html", {"form": form})
```

`form.save()` does exactly what `Student.objects.create(...)` would have done — but without manually listing every field.

---

## 5. Updating an Existing Record

Pass `instance=` to edit an existing object instead of creating a new one.

```python
def edit_student(request, student_id):
    student = Student.objects.get(id=student_id)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()   # updates the existing row
            return redirect("student-list")
    else:
        form = StudentForm(instance=student)   # pre-fills the form with existing data

    return render(request, "edit_student.html", {"form": form})
```

### Beginner tip
`ModelForm` also runs your Model's field validation automatically (e.g., `max_length`, `unique=True`), so you get consistent validation whether data comes from a form, the admin panel, or the ORM directly.

---

## 6. Knowledge Check

1. What problem does `ModelForm` solve compared to a plain `forms.Form`?
2. What does `form.save()` do when the form has no `instance=` argument?
3. How do you pre-fill a `ModelForm` with an existing database record for editing?
4. Write a `ModelForm` for a `Book` model with fields `title` and `price`.

---

**Previous:** [← Forms and Data Handling](./01-Forms-and-Data-Handling.md)
**Next:** [Admin Console →](./03-Admin-Console.md)
