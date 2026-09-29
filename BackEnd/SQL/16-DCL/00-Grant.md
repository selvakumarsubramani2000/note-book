# 🔑 DCL — GRANT

> **Trainer's Note:** `GRANT` gives a user or role permission to perform actions on database objects.

---

## 📑 Table of Contents
1. [What GRANT Does](#1-what-grant-does)
2. [Common Privilege Examples](#2-common-privilege-examples)
3. [GRANT with GRANT OPTION](#3-grant-with-grant-option)
4. [Least Privilege](#4-least-privilege)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What GRANT Does

```sql
GRANT SELECT ON Students TO report_user;
```

`report_user` may now read `Students`, but not necessarily insert/update/delete.

### Real-world analogy
```
GRANT = giving someone a labeled key
  "This key opens the Students drawer for reading only"
```

---

## 2. Common Privilege Examples

```sql
GRANT SELECT, INSERT ON Orders TO app_user;
GRANT UPDATE (status) ON Orders TO support_user;  -- column-level where supported
GRANT ALL PRIVILEGES ON Students TO admin_user;   -- use sparingly
GRANT CREATE TABLE TO dev_user;                   -- system privilege examples vary
```

---

## 3. GRANT with GRANT OPTION

```sql
GRANT SELECT ON Students TO lead_user WITH GRANT OPTION;
```

Allows `lead_user` to pass that privilege to others — powerful, so restrict carefully.

---

## 4. Least Privilege

| Account | Typical grants |
|---------|----------------|
| Reporting | `SELECT` |
| Application | needed DML only on required tables |
| Developer sandbox | broader in non-prod only |
| DBA | administrative rights, tightly controlled |

### Beginner tip
In production, prefer roles (`GRANT ... TO role`, then assign role to users) for cleaner permission management.

---

## 5. Knowledge Check

1. What does `GRANT SELECT ON t TO u` allow?
2. Write a grant giving `analyst1` read access to `Orders` and `Customers`.
3. Why avoid `ALL PRIVILEGES` for app logins?
4. What is least privilege?

---

**Previous:** [← ROLLBACK](../15-TCL/02-Rollback.md)
**Next:** [REVOKE →](./01-Revoke.md)
