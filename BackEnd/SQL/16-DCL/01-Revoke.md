# 🚫 DCL — REVOKE

> **Trainer's Note:** `REVOKE` removes previously granted privileges — essential when access should no longer exist.

---

## 📑 Table of Contents
1. [What REVOKE Does](#1-what-revoke-does)
2. [Basic Examples](#2-basic-examples)
3. [Partial Revokes](#3-partial-revokes)
4. [Operational Habits](#4-operational-habits)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What REVOKE Does

```sql
REVOKE SELECT ON Students FROM report_user;
```

After this, `report_user` should no longer be able to read `Students` (unless access still comes from another role/grant).

### Real-world analogy
```
REVOKE = taking the key back
  when someone changes team or no longer needs that drawer
```

---

## 2. Basic Examples

```sql
REVOKE INSERT, UPDATE ON Orders FROM app_user;
REVOKE ALL PRIVILEGES ON Students FROM temp_user;
```

---

## 3. Partial Revokes

```sql
-- User keeps SELECT, loses UPDATE
REVOKE UPDATE ON Orders FROM support_user;
```

Privileges can be layered (direct grant + role grant). Revoking one path may not remove all access if another path remains.

---

## 4. Operational Habits

| Habit | Why |
|-------|-----|
| Revoke on offboarding | Stops ex-employee access |
| Review unused grants | Shrinks attack surface |
| Prefer role-based grants | Easier revoke by role membership |
| Test after revoke | Confirm permission actually gone |

### Beginner tip
Security is not only GRANT. Timely REVOKE is half the job.

---

## 5. Knowledge Check

1. What does REVOKE reverse?
2. Write SQL revoking `DELETE` on `Customers` from `app_user`.
3. Why might a user still have access after one REVOKE?
4. When should you revoke privileges in a real workplace?

---

**Previous:** [← GRANT](./00-Grant.md)
**Next:** [Introduction to Normalization →](../17-Normalization/00-Introduction-to-Normalization.md)
