# 🗃️ Introduction to RDBMS

> **Trainer's Note:** An **RDBMS** is a DBMS built on the relational model. Almost every "SQL database" you hear about is an RDBMS.

---

## 📑 Table of Contents
1. [What Is an RDBMS?](#1-what-is-an-rdbms)
2. [How RDBMS and SQL Fit Together](#2-how-rdbms-and-sql-fit-together)
3. [Popular RDBMS Products](#3-popular-rdbms-products)
4. [What You Typically Create in an RDBMS](#4-what-you-typically-create-in-an-rdbms)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What Is an RDBMS?

**RDBMS** = **Relational Database Management System**.

It is software that:
- stores data in **tables**
- supports **relationships** between tables using keys
- understands **SQL** (or a SQL dialect)
- enforces integrity, security, and transactions

```
Relational Model (the theory)
        +
     DBMS software
        =
      RDBMS product (Oracle, MySQL, PostgreSQL, SQL Server...)
```

---

## 2. How RDBMS and SQL Fit Together

| Piece | Role |
|-------|------|
| **RDBMS** | The engine that stores and manages relational data |
| **SQL** | The language you use to talk to that engine |

```sql
-- You write SQL...
SELECT name FROM Students WHERE age > 20;

-- ...the RDBMS parses it, finds matching rows, and returns the result
```

### Real-world analogy
```
RDBMS = the library building + staff + catalog system
SQL   = the sentences you use to ask the librarian for books
```

---

## 3. Popular RDBMS Products

| Product | Common use |
|---------|------------|
| **Oracle Database** | Large enterprise systems (this syllabus mentions Oracle 10g) |
| **MySQL** | Web apps, widely available hosting |
| **PostgreSQL** | Modern apps needing strong standards/features |
| **Microsoft SQL Server** | .NET / Windows enterprise environments |
| **SQLite** | Mobile apps, local/dev tools (file-based) |

Syntax is mostly similar, but each product has small differences (limits, date functions, `ROWNUM` vs `LIMIT`, etc.).

---

## 4. What You Typically Create in an RDBMS

| Object | Purpose |
|--------|---------|
| **Database / Schema** | Container for related objects |
| **Table** | Store rows of data |
| **View** | Saved query that looks like a table |
| **Index** | Speed up lookups |
| **Constraint** | Enforce rules (PK, FK, UNIQUE, CHECK) |
| **Stored procedure / function** | Saved reusable SQL logic |

### Beginner tip
Start by mastering **tables + SQL statements**. Views, indexes, and procedures become natural once basic querying feels comfortable.

---

## 5. Knowledge Check

1. Expand the acronym RDBMS.
2. What language do you normally use to interact with an RDBMS?
3. Name three popular RDBMS products.
4. Is "the relational model" the same thing as "Oracle Database"? Explain.

---

**Previous:** [← What is Relational Model?](./02-What-Is-Relational-Model.md)
**Next:** [Brief on E.F. Codd →](./04-Brief-on-EF-Codd.md)
