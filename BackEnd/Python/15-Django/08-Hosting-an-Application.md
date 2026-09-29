# 🚀 Hosting a Django Application

> **Trainer's Note:** "Hosting" means making your Django app accessible on the internet instead of just `localhost`. This involves preparing settings for production, choosing a host, and deploying.

---

## 📑 Table of Contents
1. [Development vs Production](#1-development-vs-production)
2. [Production Settings Checklist](#2-production-settings-checklist)
3. [Common Hosting Options](#3-common-hosting-options)
4. [A Simple Deployment Flow](#4-a-simple-deployment-flow)
5. [Static Files in Production](#5-static-files-in-production)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. Development vs Production

| | Development (`runserver`) | Production |
|---|---|---|
| Server | Django's built-in dev server | Gunicorn/uWSGI + Nginx (or a PaaS) |
| `DEBUG` | `True` | `False` |
| Database | SQLite (often) | PostgreSQL/MySQL |
| Static files | Served automatically | Served by Nginx/CDN/WhiteNoise |

### Real-world analogy
```
Development server = a bicycle for practicing in your driveway
Production server   = a certified vehicle ready for public roads
                       (safety checks = DEBUG=False, real DB, proper web server)
```

---

## 2. Production Settings Checklist

```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ["yourdomain.com", "www.yourdomain.com"]
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]   # load from environment, not hardcoded

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ["DB_HOST"],
        "PORT": "5432",
    }
}
```

Never deploy with `DEBUG = True` — it can leak sensitive information (stack traces, settings) to visitors.

---

## 3. Common Hosting Options

| Platform | Type | Good for |
|----------|------|----------|
| **Render / Railway** | PaaS (Platform-as-a-Service) | Beginners, quick deploys |
| **Heroku** | PaaS | Simple apps, add-ons ecosystem |
| **PythonAnywhere** | Managed Python hosting | Learning, small projects |
| **AWS EC2 / DigitalOcean Droplet** | Raw VM | Full control, more setup work |
| **AWS Elastic Beanstalk / Azure App Service** | Managed cloud hosting | Production apps needing scale |

---

## 4. A Simple Deployment Flow

```bash
# 1. Install a production WSGI server
pip install gunicorn

# 2. Run the app with gunicorn instead of runserver
gunicorn myproject.wsgi:application --bind 0.0.0.0:8000

# 3. Collect static files
python manage.py collectstatic

# 4. Apply migrations on the production database
python manage.py migrate
```

A typical production stack: **Nginx** (handles incoming traffic, serves static files) → **Gunicorn** (runs your Django app) → **Django app** → **PostgreSQL**.

---

## 5. Static Files in Production

Django doesn't serve static files (CSS/JS/images) efficiently in production by default. Options:

```python
# settings.py
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"   # collectstatic gathers files here
```

- **WhiteNoise** — simplest option, serves static files directly from Django/Gunicorn.
- **Nginx** — serves static files itself, faster for larger production sites.
- **CDN (e.g., AWS CloudFront)** — best for large-scale apps with global users.

### Beginner tip
For a first deployment, a PaaS like **Render** or **Railway** is the easiest path — it handles the web server, HTTPS certificate, and process management for you, so you can focus on the Django app itself.

---

## 6. Knowledge Check

1. Why is `DEBUG = False` critical for a production deployment?
2. Name two common production hosting platforms suitable for beginners.
3. What does `python manage.py collectstatic` do?
4. What role does Gunicorn play in a typical production stack?

---

**Previous:** [← Git Basics](./07-Git-Basics.md)
**Next:** [Sessions and Cookies →](./09-Sessions-and-Cookies.md)
