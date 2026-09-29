# 💿 Installing and Setup of Software

> **Trainer's Note:** This syllabus originally used **Oracle 10g**. The concepts below apply to setting up any beginner SQL environment. Prefer a free modern option if Oracle 10g is unavailable.

---

## 📑 Table of Contents
1. [What You Need](#1-what-you-need)
2. [Setup Checklist](#2-setup-checklist)
3. [Oracle-Oriented Notes](#3-oracle-oriented-notes)
4. [Modern Free Alternatives](#4-modern-free-alternatives)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What You Need

To practice SQL you need:
1. An **RDBMS engine** (server or local database)
2. A **client tool** to type SQL and see results
3. A sample **user/schema** where you can create tables safely

### Real-world analogy
```
RDBMS engine = the kitchen stove and ingredients
Client tool  = your knife, pan, and recipe notebook
Schema/user  = your own cutting board workspace
```

---

## 2. Setup Checklist

| Step | Done when... |
|------|----------------|
| Install RDBMS | Service/instance starts without errors |
| Install client | You can open a SQL worksheet/editor |
| Connect | Host, port, service/DB name, user, password work |
| Smoke test | `SELECT 1;` or equivalent returns a row |
| Create practice table | `CREATE TABLE` succeeds in your schema |

```sql
-- First connection smoke test ideas
SELECT 1 FROM DUAL;     -- Oracle classic
SELECT 1;               -- many other engines
```

---

## 3. Oracle-Oriented Notes

Classic syllabus tooling:
- **Oracle Database** (historically 10g in older courses)
- Client options of the era: SQL*Plus, SQL Developer

Typical connection ingredients:
- Host / port
- Service name or SID
- Username / password

After login, confirm your user and available tables:
```sql
SELECT USER FROM DUAL;
SELECT table_name FROM user_tables;
```

### Beginner tip
Use a **practice user** — never learn DDL/DML on a production schema.

---

## 4. Modern Free Alternatives

If Oracle 10g is not practical on your machine:

| Option | Good for |
|--------|----------|
| **Oracle XE** (modern Express) | Staying close to Oracle SQL |
| **Oracle Live SQL** (browser) | No local install |
| **MySQL + MySQL Workbench** | Common web-dev path |
| **PostgreSQL + pgAdmin/DBeaver** | Standards-friendly learning |
| **SQL Server Express + SSMS/Azure Data Studio** | .NET-friendly path |
| **SQLite + DB Browser** | Absolute lightest local start |

The **language concepts** in this track (SELECT, joins, constraints, subqueries) transfer across all of them. Only a few product-specific items (like `ROWNUM`/`ROWID`) are Oracle-flavored.

---

## 5. Knowledge Check

1. What two pieces of software do you need to practice SQL?
2. What is a safe smoke-test query after connecting?
3. Why avoid practicing on a production database?
4. Name one modern alternative if Oracle 10g is unavailable.

---

**Previous:** [← DQL](../03-Statements-in-SQL/05-DQL.md)
**Next:** [Working on Oracle 10g →](./01-Working-on-Oracle-10g.md)
