# 📜 SQL Statements Overview

> **Trainer's Note:** SQL commands are grouped into families. Learning the five families first makes every new statement easier to place.

---

## 📑 Table of Contents
1. [The Five Families](#1-the-five-families)
2. [Quick Map with Examples](#2-quick-map-with-examples)
3. [How Beginners Should Study Them](#3-how-beginners-should-study-them)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. The Five Families

| Family | Full name | Purpose |
|--------|-----------|---------|
| **DDL** | Data Definition Language | Define/change structure (tables, etc.) |
| **DML** | Data Manipulation Language | Change data inside tables |
| **TCL** | Transaction Control Language | Confirm or undo a group of changes |
| **DCL** | Data Control Language | Permissions (who can do what) |
| **DQL** | Data Query Language | Read/select data |

Some teachers fold DQL into DML. This syllabus lists DQL separately — both views are common.

---

## 2. Quick Map with Examples

| Family | Typical commands |
|--------|------------------|
| DDL | `CREATE`, `ALTER`, `DROP`, `TRUNCATE` |
| DML | `INSERT`, `UPDATE`, `DELETE` |
| TCL | `COMMIT`, `ROLLBACK`, `SAVEPOINT` |
| DCL | `GRANT`, `REVOKE` |
| DQL | `SELECT` |

```sql
CREATE TABLE Students (...);     -- DDL
INSERT INTO Students ...;        -- DML
SELECT * FROM Students;          -- DQL
COMMIT;                          -- TCL
GRANT SELECT ON Students TO app_user;  -- DCL
```

### Real-world analogy
```
DDL  = building/renovating the filing cabinets
DML  = putting papers in, updating papers, throwing papers away
DQL  = reading/searching the papers
TCL  = stamping a batch of changes "final" or "cancel the batch"
DCL  = giving or taking away keys to rooms/cabinets
```

---

## 3. How Beginners Should Study Them

Suggested order in this track:
1. Understand all five names (this page)
2. Practice **DQL** heavily (`SELECT`) — daily skill
3. Practice **DML** (`INSERT/UPDATE/DELETE`)
4. Learn **DDL** to create your own tables
5. Add **TCL** when multi-step changes must be atomic
6. Learn **DCL** when working with real users/roles

### Beginner tip
If you remember only one thing: **`SELECT` reads**, **`INSERT/UPDATE/DELETE` change rows**, **`CREATE/ALTER/DROP` change structure**.

---

## 4. Knowledge Check

1. Which family does `ALTER TABLE` belong to?
2. Is `SELECT` DQL or DDL?
3. Which family controls permissions?
4. Match: `ROLLBACK` → ? and `INSERT` → ?

---

**Previous:** [← How to Use Constraints](../02-Datatypes-and-Constraints/05-How-to-Use-Constraints.md)
**Next:** [DDL →](./01-DDL.md)
