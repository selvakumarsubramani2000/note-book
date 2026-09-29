# 📝 Receiving Data from Front-End, GET/POST & Django Forms

> **Trainer's Note:** Websites need to collect data from users (sign-up, search, feedback). Django gives you three ways to do this: raw request data, the built-in `forms` module, and custom forms — each with validation support.

---

## 📑 Table of Contents
1. [GET and POST Methods](#1-get-and-post-methods)
2. [Receiving Data in a View](#2-receiving-data-in-a-view)
3. [Django's Built-in Forms Module](#3-djangos-built-in-forms-module)
4. [Custom Forms](#4-custom-forms)
5. [Validations on Forms](#5-validations-on-forms)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. GET and POST Methods

| Method | Purpose | Data visibility |
|--------|---------|------------------|
| `GET` | Requesting/reading data (search, view a page) | Appears in URL (`?q=python`) |
| `POST` | Submitting data that changes something (sign-up, login) | Sent in request body, not in URL |

### Real-world analogy
```
GET  = asking a librarian "show me books about Python" (just looking)
POST = filling out a library membership form and handing it in (submitting data)
```

---

## 2. Receiving Data in a View

```python
# app/views.py
from django.shortcuts import render, HttpResponse

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        message = request.POST.get("message")
        return HttpResponse(f"Thanks {name}, we received: {message}")
    return render(request, "contact.html")
```

```python
def search_view(request):
    query = request.GET.get("q", "")   # from URL: /search/?q=python
    return HttpResponse(f"Searching for: {query}")
```

```html
<!-- templates/contact.html -->
<form method="POST">
    {% csrf_token %}
    <input type="text" name="name">
    <textarea name="message"></textarea>
    <button type="submit">Send</button>
</form>
```

---

## 3. Django's Built-in Forms Module

Instead of manually reading `request.POST`, Django's `forms` module generates HTML fields and validates data for you.

```python
# app/forms.py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
```

```python
# app/views.py
from .forms import ContactForm

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            # process the cleaned, validated data
            return HttpResponse(f"Thanks {name}!")
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})
```

```html
<form method="POST">
    {% csrf_token %}
    {{ form }}
    <button type="submit">Send</button>
</form>
```

---

## 4. Custom Forms

You can fully customize field widgets, labels, and layout instead of relying on Django's defaults.

```python
class SignupForm(forms.Form):
    username = forms.CharField(
        label="Choose a username",
        widget=forms.TextInput(attrs={"placeholder": "e.g. asha_dev"})
    )
    password = forms.CharField(widget=forms.PasswordInput)
    age = forms.IntegerField(min_value=13, required=True)
```

---

## 5. Validations on Forms

Django validates automatically based on field types (`EmailField` checks email format, `IntegerField` checks numbers), and you can add **custom validation**.

```python
class SignupForm(forms.Form):
    username = forms.CharField(max_length=30)
    age = forms.IntegerField()

    def clean_username(self):
        username = self.cleaned_data["username"]
        if " " in username:
            raise forms.ValidationError("Username cannot contain spaces.")
        return username

    def clean_age(self):
        age = self.cleaned_data["age"]
        if age < 13:
            raise forms.ValidationError("You must be at least 13 years old.")
        return age
```

```python
form = SignupForm(request.POST)
if form.is_valid():
    print("All good!")
else:
    print(form.errors)   # dictionary of field-wise error messages
```

### Beginner tip
Always validate data on the **server side** (via forms), even if you also validate in JavaScript on the front end — browser validation can be bypassed.

---

## 6. Knowledge Check

1. What's the key difference between `GET` and `POST`?
2. How do you access submitted POST data in a Django view without using forms?
3. What does `form.is_valid()` do, and where does the cleaned data live afterward?
4. Write a custom `clean_<field>()` method that ensures an `email` field ends with `@company.com`.

---

**Previous:** [← Django Models](./00-Django-Models.md)
**Next:** [Model Forms & Sending Data to DB →](./02-Model-Forms-and-DB.md)
