# 🏛️ Django Models

> **Trainer's Note:** A Django Model is a Python class that represents a database table. Django's ORM (Object-Relational Mapper) lets you work with the database using plain Python code instead of writing raw SQL.

---

## 📑 Table of Contents
1. [What is Django?](#1-what-is-django)
2. [What is a Model?](#2-what-is-a-model)
3. [Defining a Model](#3-defining-a-model)
4. [Common Field Types](#4-common-field-types)
5. [Migrations](#5-migrations)
6. [Using the Model (ORM Basics)](#6-using-the-model-orm-basics)
7. [Knowledge Check](#7-knowledge-check)

---

## 1. What is Django?

Django is a high-level Python web framework that helps you build websites quickly using a "batteries-included" philosophy — it comes with an ORM, admin panel, forms, authentication, and more, built in.

### Real-world analogy
```
Django = a fully-furnished apartment
  Walls, plumbing, electricity, kitchen already built (ORM, admin, auth)
  You just move in your furniture (your business logic)
```

---

## 2. What is a Model?

A **Model** is a Python class (inside `models.py`) that maps to a database table. Each attribute of the class becomes a column in the table.

```
Model class      →  Database table
Model instance   →  A row in that table
Model field      →  A column in that table
```

---

## 3. Defining a Model

```python
# app/models.py
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    joined_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
```

This generates a `Student` table with columns: `id` (auto-created primary key), `name`, `email`, `age`, `joined_on`.

---

## 4. Common Field Types

| Field | Used for |
|-------|----------|
| `CharField(max_length=..)` | Short text (name, title) |
| `TextField()` | Long text (description, comments) |
| `IntegerField()` | Whole numbers |
| `FloatField()` | Decimal numbers |
| `BooleanField()` | True/False |
| `DateField()` / `DateTimeField()` | Dates and timestamps |
| `EmailField()` | Email addresses (validated) |
| `ForeignKey(Model, on_delete=...)` | Link to another table (relationship) |

```python
class Course(models.Model):
    title = models.CharField(max_length=150)

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(auto_now_add=True)
```

---

## 5. Migrations

Migrations are Django's way of turning your Python model code into actual database tables/columns.

```bash
python manage.py makemigrations   # generates migration files from model changes
python manage.py migrate          # applies migrations to the database
```

### Real-world analogy
```
Model change   = drawing a new blueprint
makemigrations = writing the construction plan
migrate        = actually building/renovating the house (database)
```

---

## 6. Using the Model (ORM Basics)

```python
# Create
student = Student(name="Asha", email="asha@example.com", age=21)
student.save()

# Or in one line
Student.objects.create(name="Ravi", email="ravi@example.com", age=22)

# Read
all_students = Student.objects.all()
one_student = Student.objects.get(id=1)
adults = Student.objects.filter(age__gte=18)

# Update
student = Student.objects.get(id=1)
student.age = 22
student.save()

# Delete
student.delete()
```

### Beginner tip
You almost never write raw SQL with Django's ORM — `objects.all()`, `.filter()`, `.get()`, `.create()`, `.delete()` cover most day-to-day database work.

---

## 7. Knowledge Check

1. What does a Django Model class represent in the database?
2. What is the purpose of `makemigrations` vs `migrate`?
3. Write a model `Book` with fields `title` (CharField) and `price` (FloatField).
4. What does `ForeignKey(Model, on_delete=models.CASCADE)` mean?

---

**Next:** [Receiving Data from Front-End & Forms →](./01-Forms-and-Data-Handling.md)
