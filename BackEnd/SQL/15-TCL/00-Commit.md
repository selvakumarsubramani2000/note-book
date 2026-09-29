# ✅ TCL — COMMIT

> **Trainer's Note:** `COMMIT` makes the current transaction’s changes **permanent**. After commit, a normal `ROLLBACK` cannot undo them.

---

## 📑 Table of Contents
1. [What COMMIT Does](#1-what-commit-does)
2. [Basic Pattern](#2-basic-pattern)
3. [When to Commit](#3-when-to-commit)
4. [Auto-Commit Modes](#4-auto-commit-modes)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What COMMIT Does

```sql
BEGIN TRANSACTION;          -- start (syntax varies)
UPDATE Accounts SET balance = balance - 100 WHERE id = 1;
UPDATE Accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;                     -- both changes become permanent
```

### Real-world analogy
```
COMMIT = stamping a multi-step form packet as FINAL
  Once stamped and filed, the office treats it as official record
```

---

## 2. Basic Pattern

```sql
INSERT INTO Orders (order_id, student_id, item) VALUES (20, 1, 'Book');
UPDATE Students SET last_order_on = CURRENT_DATE WHERE student_id = 1;
COMMIT;
```

---

## 3. When to Commit

| Situation | Guidance |
|-----------|----------|
| Related statements all succeeded | Commit once as a unit |
| Long interactive lab with many trials | Commit intentional checkpoints only |
| Unsure about results | Don’t commit yet — verify with SELECT |

---

## 4. Auto-Commit Modes

Some tools commit every statement automatically. Others keep an open transaction until `COMMIT`/`ROLLBACK`.

### Beginner tip
Before practicing `UPDATE`/`DELETE`, check whether your client is in auto-commit mode. It changes how `COMMIT` feels.

---

## 5. Knowledge Check

1. What does `COMMIT` finalize?
2. Can you `ROLLBACK` a change after a successful `COMMIT` (normally)?
3. Write a tiny transaction with one insert and a commit.
4. Why commit once after several related statements instead of after each?

---

**Previous:** [← DELETE](../14-DML/02-Delete.md)
**Next:** [SAVEPOINT →](./01-Savepoint.md)
