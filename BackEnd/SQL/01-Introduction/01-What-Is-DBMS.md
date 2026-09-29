# ⚙️ What Is a Database Management System (DBMS)?

> **Trainer's Note:** A database is the data. A **DBMS** is the software that stores, organizes, secures, and lets you work with that data.

---

## 📑 Table of Contents
1. [Database vs DBMS](#1-database-vs-dbms)
2. [What Does a DBMS Do?](#2-what-does-a-dbms-do)
3. [Types of DBMS (High Level)](#3-types-of-dbms-high-level)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. Database vs DBMS

| Term | Meaning | Analogy |
|------|---------|---------|
| **Database** | The organized data itself | The books and folders in a library |
| **DBMS** | Software that manages the database | The librarian + catalog system |

Examples of DBMS software: Oracle, MySQL, PostgreSQL, SQL Server, SQLite.

```
You  -->  SQL query  -->  DBMS  -->  reads/writes the Database
```

You almost never "open the data files" directly. You talk to the DBMS, and the DBMS handles storage, locking, recovery, and access control.

---

## 2. What Does a DBMS Do?

| Responsibility | Simple meaning |
|----------------|----------------|
| **Storage** | Saves data on disk in an efficient format |
| **Retrieval** | Finds and returns the rows you asked for |
| **Update** | Inserts, updates, deletes safely |
| **Concurrency** | Lets many users work without corrupting data |
| **Security** | Login, permissions (who can see/change what) |
| **Integrity** | Enforces rules (constraints, transactions) |
| **Backup/Recovery** | Protects data if power fails or a disk dies |

### Real-world analogy
```
DBMS = a full library management system
  Not just shelves of books, but also:
  check-in/check-out rules, member cards, search catalog,
  and alarms if someone tries to steal a book
```

---

## 3. Types of DBMS (High Level)

| Type | How data is organized | Common examples |
|------|----------------------|-----------------|
| **Relational (RDBMS)** | Tables with rows/columns + relationships | Oracle, MySQL, PostgreSQL, SQL Server |
| **Document** | JSON-like documents | MongoDB |
| **Key-Value** | Simple key → value pairs | Redis |
| **Graph** | Nodes and relationships | Neo4j |

This curriculum focuses on the **relational** model and **SQL**, because that is still the core skill for most backend developers.

### Beginner tip
When people say "database" in job postings, they often mean **RDBMS + SQL** unless they explicitly say NoSQL.

---

## 4. Knowledge Check

1. What is the difference between a database and a DBMS?
2. Name three things a DBMS handles for you that plain files do not.
3. List two examples of RDBMS software.
4. Why do developers usually send SQL to a DBMS instead of editing data files by hand?

---

**Previous:** [← What Is a Database?](./00-What-Is-Database.md)
**Next:** [What is Relational Model? →](./02-What-Is-Relational-Model.md)
