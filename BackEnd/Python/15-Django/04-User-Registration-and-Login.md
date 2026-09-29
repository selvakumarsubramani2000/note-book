# 🔐 User Registration & Login in Django

> **Trainer's Note:** Django ships with a built-in authentication system (`django.contrib.auth`) that handles user accounts, password hashing, login, and logout — you rarely need to build this from scratch.

---

## 📑 Table of Contents
1. [Django's Built-in User Model](#1-djangos-built-in-user-model)
2. [User Registration](#2-user-registration)
3. [Login Creation](#3-login-creation)
4. [Logout](#4-logout)
5. [Protecting Views (Login Required)](#5-protecting-views-login-required)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. Django's Built-in User Model

Django comes with a ready-made `User` model (in `django.contrib.auth.models`) that already has `username`, `password` (hashed), `email`, `is_active`, etc.

### Real-world analogy
```
Building your own auth system = building your own door lock from scratch
Django's auth system          = installing a certified, tested lock
                                  (password hashing, sessions already handled securely)
```

---

## 2. User Registration

```python
# app/forms.py
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
```

```python
# app/views.py
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()   # creates user with hashed password automatically
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})
```

`UserCreationForm` automatically hashes the password — you never store or handle plain-text passwords yourself.

---

## 3. Login Creation

```python
# app/views.py
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)   # starts the session
            return redirect("dashboard")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")
```

`authenticate()` checks the username/password against the stored hash; `login()` creates the session that keeps the user logged in across requests.

---

## 4. Logout

```python
from django.contrib.auth import logout

def logout_view(request):
    logout(request)   # clears the session
    return redirect("login")
```

---

## 5. Protecting Views (Login Required)

```python
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")
def dashboard_view(request):
    return render(request, "dashboard.html", {"user": request.user})
```

Any user who isn't logged in gets redirected to `/login/` automatically.

### Beginner tip
Always use Django's built-in `authenticate()`/`login()`/`logout()` functions and `UserCreationForm` rather than writing your own password comparison logic — Django handles secure hashing (PBKDF2/Argon2) and session management for you.

---

## 6. Knowledge Check

1. Why should you avoid writing your own password hashing logic?
2. What does `authenticate()` return if the credentials are wrong?
3. What does the `@login_required` decorator do?
4. What is the difference between `login()` and `authenticate()`?

---

**Previous:** [← Admin Console](./03-Admin-Console.md)
**Next:** [CRUD Operations →](./05-CRUD-Operations.md)
