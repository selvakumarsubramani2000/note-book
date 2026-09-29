# ↩️ TCL — ROLLBACK

> **Trainer's Note:** `ROLLBACK` cancels uncommitted changes in the current transaction — your safety net when something goes wrong.

---

## 📑 Table of Contents
1. [What ROLLBACK Does](#1-what-rollback-does)
2. [Full Transaction Rollback](#2-full-transaction-rollback)
3. [Rollback to Savepoint](#3-rollback-to-savepoint)
4. [Limits of ROLLBACK](#4-limits-of-rollback)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What ROLLBACK Does

```sql
BEGIN TRANSACTION;
DELETE FROM Students WHERE city = 'Temp';
-- Oops, wrong filter
ROLLBACK;   -- students restored (if not yet committed)
```

### Real-world analogy
```
ROLLBACK = shredding an unfinished form packet
  before it is stamped FINAL (COMMIT)
```

---

## 2. Full Transaction Rollback

```sql
BEGIN TRANSACTION;
UPDATE Accounts SET balance = balance - 100 WHERE id = 1;
UPDATE Accounts SET balance = balance + 100 WHERE id = 9999; -- fails / wrong id
ROLLBACK;  -- undo both sides of the attempted transfer
```

---

## 3. Rollback to Savepoint

```sql
BEGIN TRANSACTION;
UPDATE ...;                 -- keep
SAVEPOINT sp1;
UPDATE ...;                 -- discard this part
ROLLBACK TO sp1;
COMMIT;
```

---

## 4. Limits of ROLLBACK

| Cannot normally undo | Why |
|----------------------|-----|
| Changes already `COMMIT`ted | Permanently recorded |
| Some DDL in some engines | Auto-commit behavior differs |
| Work in another session already committed | Not yours to roll back |

### Beginner tip
Pair risky DML practice with explicit transactions: try → verify SELECT → `COMMIT` or `ROLLBACK`.

---

## 5. Knowledge Check

1. What does `ROLLBACK` undo?
2. Write a transaction that updates a row and then rolls back.
3. Difference between `ROLLBACK` and `ROLLBACK TO savepoint`?
4. Can rollback reverse a committed delete?

---

**Previous:** [← SAVEPOINT](./01-Savepoint.md)
**Next:** [DCL GRANT →](../16-DCL/00-Grant.md)
