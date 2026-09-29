# 🔑 Data Control Language (DCL)

> **Trainer's Note:** **DCL** manages permissions — who is allowed to read, write, or change database objects.

---

## 📑 Table of Contents
1. [What DCL Does](#1-what-dcl-does)
2. [GRANT](#2-grant)
3. [REVOKE](#3-revoke)
4. [Least Privilege Principle](#4-least-privilege-principle)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What DCL Does

| Command | Purpose |
|---------|---------|
| `GRANT` | Give a user/role permission |
| `REVOKE` | Take a permission away |

Permissions can apply to tables, views, procedures, and more (exact options depend on the RDBMS).

---

## 2. GRANT

```sql
-- Let report_user read Students
GRANT SELECT ON Students TO report_user;

-- Let app_user read and write Orders
GRANT SELECT, INSERT, UPDATE ON Orders TO app_user;

-- Allow creating objects (example; privilege names vary)
GRANT CREATE TABLE TO dev_user;
```

---

## 3. REVOKE

```sql
REVOKE UPDATE ON Orders FROM app_user;
REVOKE SELECT ON Students FROM report_user;
```

### Real-world analogy
```
GRANT  = giving someone a key to a room or drawer
REVOKE = taking that key back
DCL    = the building's key-management desk
```

---

## 4. Least Privilege Principle

Give each account **only** the permissions it needs — nothing more.

| Account type | Typical rights |
|--------------|----------------|
| Reporting user | `SELECT` only |
| Application user | `SELECT/INSERT/UPDATE` on needed tables (often no `DROP`) |
| Admin/DBA | Broad rights, tightly controlled people |

### Beginner tip
In production, application accounts almost never need `DROP TABLE` or unrestricted DBA rights. Over-powered accounts turn small bugs into large incidents.

---

## 5. Knowledge Check

1. What do `GRANT` and `REVOKE` do?
2. Write a statement giving `analyst1` read access to `Orders`.
3. Why revoke unused permissions?
4. What does "least privilege" mean for a database login?

---

**Previous:** [← TCL](./03-TCL.md)
**Next:** [DQL →](./05-DQL.md)
