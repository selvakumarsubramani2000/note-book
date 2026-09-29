# 📧 Integration of Mail API in Django

> **Trainer's Note:** Most real applications need to send emails — welcome messages, password resets, notifications. Django has built-in email support, and can also integrate with third-party mail APIs (SendGrid, Mailgun, AWS SES).

---

## 📑 Table of Contents
1. [Django's Built-in Email Support](#1-djangos-built-in-email-support)
2. [Configuring an SMTP Backend](#2-configuring-an-smtp-backend)
3. [Sending a Simple Email](#3-sending-a-simple-email)
4. [Sending HTML Emails](#4-sending-html-emails)
5. [Using a Third-Party Mail API](#5-using-a-third-party-mail-api)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. Django's Built-in Email Support

Django provides `django.core.mail` with functions to send email without installing anything extra — you just need an SMTP server (Gmail, Outlook, or a transactional email service).

### Real-world analogy
```
django.core.mail = a pre-installed mailbox slot in your app
  You just tell it which post office (SMTP server) to use
```

---

## 2. Configuring an SMTP Backend

```python
# settings.py
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your_email@gmail.com"
EMAIL_HOST_PASSWORD = "your_app_password"   # use environment variables, never hardcode!
DEFAULT_FROM_EMAIL = "your_email@gmail.com"
```

### Security tip
Never commit real credentials to source control. Load `EMAIL_HOST_PASSWORD` from an environment variable or a secrets manager.

---

## 3. Sending a Simple Email

```python
from django.core.mail import send_mail

send_mail(
    subject="Welcome to our site!",
    message="Thanks for signing up.",
    from_email="your_email@gmail.com",
    recipient_list=["newuser@example.com"],
    fail_silently=False,
)
```

```python
# Inside a view, e.g. right after registration
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_mail(
                "Welcome!",
                f"Hi {user.username}, welcome aboard!",
                "your_email@gmail.com",
                [user.email],
            )
            return redirect("login")
```

---

## 4. Sending HTML Emails

```python
from django.core.mail import EmailMultiAlternatives

def send_welcome_html_email(user):
    subject = "Welcome!"
    text_content = f"Hi {user.username}, welcome aboard!"
    html_content = f"<h1>Hi {user.username}</h1><p>Welcome aboard!</p>"

    email = EmailMultiAlternatives(subject, text_content, "your_email@gmail.com", [user.email])
    email.attach_alternative(html_content, "text/html")
    email.send()
```

---

## 5. Using a Third-Party Mail API

For production apps, services like **SendGrid**, **Mailgun**, or **AWS SES** offer better deliverability, analytics, and scale than raw SMTP. They typically work via:
1. An API key (instead of SMTP username/password)
2. A Python SDK or simple HTTP request

```python
# Example: SendGrid via their Python SDK
import sendgrid
from sendgrid.helpers.mail import Mail

def send_via_sendgrid(to_email, subject, content):
    message = Mail(
        from_email="your_email@example.com",
        to_emails=to_email,
        subject=subject,
        plain_text_content=content,
    )
    sg = sendgrid.SendGridAPIClient("YOUR_API_KEY")   # keep this in env variables
    response = sg.send(message)
    return response.status_code
```

### Beginner tip
Start with Django's built-in SMTP email for learning and small projects. Move to a transactional mail API (SendGrid/Mailgun/SES) once you need reliable delivery, tracking, and higher sending volume.

---

## 6. Knowledge Check

1. What Django setting configures which SMTP server to use for sending mail?
2. Why should email credentials never be hardcoded in `settings.py`?
3. What does `EmailMultiAlternatives` let you do that `send_mail()` doesn't?
4. Name one advantage of using a third-party mail API over raw SMTP.

---

**Previous:** [← CRUD Operations](./05-CRUD-Operations.md)
**Next:** [Git Basics →](./07-Git-Basics.md)
