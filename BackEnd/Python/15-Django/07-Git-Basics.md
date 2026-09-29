# 🌳 Git Basics for a Django Project

> **Trainer's Note:** Git is a version control system that tracks changes to your code over time, so you can collaborate with others and safely undo mistakes. Every real-world project — Django or otherwise — is managed with Git.

---

## 📑 Table of Contents
1. [What is Git?](#1-what-is-git)
2. [Setting Up a Repository](#2-setting-up-a-repository)
3. [The Basic Workflow](#3-the-basic-workflow)
4. [Branching](#4-branching)
5. [`.gitignore` for Django Projects](#5-gitignore-for-django-projects)
6. [Working with Remotes (GitHub)](#6-working-with-remotes-github)
7. [Knowledge Check](#7-knowledge-check)

---

## 1. What is Git?

Git records **snapshots** of your project (commits) so you can review history, compare changes, and revert if something breaks.

### Real-world analogy
```
Git = a time machine with save-points for your code
  Each commit = a save-point you can travel back to
  Branches    = alternate timelines you can experiment in safely
```

---

## 2. Setting Up a Repository

```bash
cd my_django_project
git init                        # start tracking this folder with Git
git add .                       # stage all files
git commit -m "Initial commit"  # save the first snapshot
```

---

## 3. The Basic Workflow

```bash
git status                 # see what's changed
git add <file>              # stage a specific file
git add .                   # stage everything
git commit -m "message"     # save a snapshot with a description
git log                     # view commit history
git diff                    # see line-by-line changes not yet staged
```

### Daily loop
```
1. Make code changes
2. git status  -> see what changed
3. git add .   -> stage changes
4. git commit -m "Add student CRUD views"
5. Repeat
```

---

## 4. Branching

Branches let you work on a feature without affecting the main codebase.

```bash
git branch feature/login-page      # create a new branch
git checkout feature/login-page    # switch to it
# or in one step:
git checkout -b feature/login-page

# ... make changes, commit ...

git checkout main                  # switch back to main
git merge feature/login-page       # bring the feature's changes into main
```

---

## 5. `.gitignore` for Django Projects

Never commit virtual environments, secrets, or generated files.

```gitignore
# .gitignore
venv/
__pycache__/
*.pyc
db.sqlite3
.env
staticfiles/
*.log
```

### Beginner tip
Store secrets like `SECRET_KEY`, database passwords, and API keys in a `.env` file (loaded via a library like `python-dotenv`), and make sure `.env` is in `.gitignore` — never commit real secrets to Git.

---

## 6. Working with Remotes (GitHub)

```bash
git remote add origin https://github.com/username/my-django-project.git
git push -u origin main         # push local commits to GitHub

git pull origin main             # fetch and merge latest changes from GitHub
git clone https://github.com/username/my-django-project.git   # copy an existing repo
```

### Real-world analogy
```
Local repo  = your personal notebook
Remote repo (GitHub) = a shared notebook the whole team can read/write to
push  = copying your notes into the shared notebook
pull  = copying the shared notebook's updates into yours
```

---

## 7. Knowledge Check

1. What is the difference between `git add` and `git commit`?
2. Why should `db.sqlite3` and `venv/` be listed in `.gitignore`?
3. What command creates and switches to a new branch in one step?
4. What is the difference between `git push` and `git pull`?

---

**Previous:** [← Mail API Integration](./06-Mail-API-Integration.md)
**Next:** [Hosting an Application →](./08-Hosting-an-Application.md)
