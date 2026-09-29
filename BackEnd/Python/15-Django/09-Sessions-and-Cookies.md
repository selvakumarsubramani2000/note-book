# 🍪 Sessions and Cookies in Django

> **Trainer's Note:** HTTP is "stateless" — the server forgets you between requests. Cookies and sessions are how a website remembers who you are (e.g., staying logged in) across multiple page loads.

---

## 📑 Table of Contents
1. [Why Do We Need Sessions/Cookies?](#1-why-do-we-need-sessionscookies)
2. [Cookies](#2-cookies)
3. [Sessions](#3-sessions)
4. [Using Sessions in Django](#4-using-sessions-in-django)
5. [Session Settings](#5-session-settings)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. Why Do We Need Sessions/Cookies?

Every HTTP request is independent — the server has no built-in memory of previous requests from the same user. Cookies and sessions solve this "statelessness" problem.

### Real-world analogy
```
Stateless HTTP = a shop clerk who forgets you the moment you walk out the door
Cookie/Session = a wristband you get at check-in
  the clerk sees the wristband next time and remembers who you are
```

---

## 2. Cookies

A **cookie** is a small piece of data the server asks the browser to store, and the browser sends it back on every subsequent request.

```python
# Setting a cookie
from django.http import HttpResponse

def set_theme(request):
    response = HttpResponse("Theme set!")
    response.set_cookie("theme", "dark", max_age=30*24*60*60)  # 30 days
    return response

# Reading a cookie
def show_theme(request):
    theme = request.COOKIES.get("theme", "light")   # default: "light"
    return HttpResponse(f"Current theme: {theme}")
```

Cookies are stored **on the browser** — good for small, non-sensitive preferences (theme, language), but not secure enough for storing passwords or sensitive session data directly.

---

## 3. Sessions

A **session** stores data **on the server**; the browser only holds a small session ID cookie (`sessionid`) that points to that server-side data. This is what Django's login system uses.

### Real-world analogy
```
Cookie only        = writing your full order on a sticky note you carry around
Session (Django)   = the restaurant keeps your full order in their system,
                      you just carry a numbered ticket (session ID) to identify it
```

---

## 4. Using Sessions in Django

```python
# Storing data in the session
def add_to_cart(request):
    cart = request.session.get("cart", [])
    cart.append("item123")
    request.session["cart"] = cart   # saved server-side automatically
    return HttpResponse("Item added!")

# Reading data from the session
def view_cart(request):
    cart = request.session.get("cart", [])
    return HttpResponse(f"Cart: {cart}")

# Clearing session data
def checkout(request):
    request.session.pop("cart", None)
    return HttpResponse("Checked out!")

# Fully logging out / clearing everything
def logout_view(request):
    request.session.flush()   # deletes all session data + generates new session ID
    return HttpResponse("Logged out")
```

Django's built-in `login()`/`logout()` functions (from `django.contrib.auth`) use sessions internally — that's how a logged-in user stays logged in across page requests.

---

## 5. Session Settings

```python
# settings.py
SESSION_COOKIE_AGE = 1209600           # session lifetime in seconds (default: 2 weeks)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True # end session when browser closes
SESSION_COOKIE_SECURE = True           # only send session cookie over HTTPS (production)
SESSION_COOKIE_HTTPONLY = True         # prevents JavaScript from reading the cookie (security)
```

### Beginner tip
Use **sessions** for anything sensitive or server-trusted (login state, shopping cart tied to a user), and **cookies alone** only for small, non-sensitive client-side preferences.

---

## 6. Knowledge Check

1. Why is HTTP described as "stateless," and what problem do cookies/sessions solve?
2. Where is session data actually stored — browser or server?
3. What does `request.session.flush()` do?
4. Why should `SESSION_COOKIE_HTTPONLY` be enabled in production?

---

**Previous:** [← Hosting an Application](./08-Hosting-an-Application.md)
**Next:** [Flask Framework Introduction →](./10-Flask-Introduction.md)
