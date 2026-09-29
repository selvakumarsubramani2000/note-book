# 🌶️ Flask Framework Introduction

> **Trainer's Note:** Flask is a lightweight ("micro") Python web framework — unlike Django's "batteries-included" approach, Flask gives you a small core and lets you add only the pieces you need.

---

## 📑 Table of Contents
1. [Flask vs Django](#1-flask-vs-django)
2. [Installing Flask](#2-installing-flask)
3. [A Minimal Flask App](#3-a-minimal-flask-app)
4. [Routes and URL Parameters](#4-routes-and-url-parameters)
5. [Handling GET and POST](#5-handling-get-and-post)
6. [Templates with Jinja2](#6-templates-with-jinja2)
7. [Knowledge Check](#7-knowledge-check)

---

## 1. Flask vs Django

| | Django | Flask |
|---|--------|-------|
| Philosophy | "Batteries included" (ORM, admin, auth built in) | "Micro" — minimal core, add what you need |
| Best for | Larger apps needing structure fast | Small apps, APIs, full custom control |
| ORM | Built-in | Not included (commonly uses SQLAlchemy) |
| Admin panel | Built-in | Not included |
| Learning curve | Steeper initially, but very structured | Easier to start, but you assemble pieces yourself |

### Real-world analogy
```
Django = a fully-furnished apartment (move in and go)
Flask  = an empty room with great architecture (bring your own furniture)
```

---

## 2. Installing Flask

```bash
pip install Flask
```

---

## 3. A Minimal Flask App

```python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)
```

```bash
python app.py
# Visit http://127.0.0.1:5000/
```

That's a complete, runnable web app in under 10 lines — compare this to Django's multi-file project structure.

---

## 4. Routes and URL Parameters

```python
@app.route("/about")
def about():
    return "This is the About page."

@app.route("/user/<username>")
def show_user(username):
    return f"Hello, {username}!"

@app.route("/post/<int:post_id>")
def show_post(post_id):
    return f"Post number: {post_id}"
```

---

## 5. Handling GET and POST

```python
from flask import request

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        return f"Thanks, {name}!"
    return '''
        <form method="POST">
            <input type="text" name="name">
            <button type="submit">Send</button>
        </form>
    '''
```

```python
@app.route("/search")
def search():
    query = request.args.get("q", "")   # e.g. /search?q=python
    return f"Searching for: {query}"
```

---

## 6. Templates with Jinja2

Flask uses the **Jinja2** templating engine (similar concept to Django templates) — HTML files live in a `templates/` folder.

```python
from flask import render_template

@app.route("/greet/<name>")
def greet(name):
    return render_template("greet.html", name=name)
```

```html
<!-- templates/greet.html -->
<h1>Hello, {{ name }}!</h1>
{% if name == "Admin" %}
    <p>Welcome back, boss!</p>
{% endif %}
```

### Beginner tip
Choose **Flask** when you want full control and a lightweight footprint (APIs, small services, learning projects). Choose **Django** when you want a complete, structured toolkit (ORM, admin, auth) out of the box for larger applications.

---

## 7. Knowledge Check

1. What is the core philosophical difference between Flask and Django?
2. Write a Flask route `/product/<int:product_id>` that returns the product ID as text.
3. How do you read query string parameters (like `?q=python`) in a Flask view?
4. What templating engine does Flask use, and where do template files live by default?

---

**Previous:** [← Sessions and Cookies](./09-Sessions-and-Cookies.md)

🎉 **Django & Flask track complete!** You've learned Models, Forms & validation, Model Forms, Admin console, Auth (registration/login), CRUD, Mail API integration, Git basics, Hosting, Sessions/Cookies, and a Flask introduction.
