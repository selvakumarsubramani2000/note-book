# 🚩 TCL — SAVEPOINT

> **Trainer's Note:** A **SAVEPOINT** is a named marker inside a transaction so you can undo only part of the work, not the entire transaction.

---

## 📑 Table of Contents
1. [Why SAVEPOINT Exists](#1-why-savepoint-exists)
2. [Creating and Rolling Back To a Savepoint](#2-creating-and-rolling-back-to-a-savepoint)
3. [Full Example](#3-full-example)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. Why SAVEPOINT Exists

Long transactions may have safe early steps and risky later steps. Savepoints let you keep the safe part if the later part fails.

### Real-world analogy
```
SAVEPOINT = bookmark in a multi-page office form
  If page 3 is wrong, rewind to the bookmark after page 2
  without discarding page 1 and 2 work
```

---

## 2. Creating and Rolling Back To a Savepoint

```sql
BEGIN TRANSACTION;

UPDATE ...;                 -- step A
SAVEPOINT sp_after_a;

UPDATE ...;                 -- step B
-- something wrong with step B
ROLLBACK TO SAVEPOINT sp_after_a;   -- undo B, keep A

COMMIT;                    -- finalize remaining work
```

Syntax variants:
- `ROLLBACK TO sp_after_a`
- `ROLLBACK TO SAVEPOINT sp_after_a`

---

## 3. Full Example

```sql
BEGIN TRANSACTION;

INSERT INTO Orders (order_id, student_id, item) VALUES (101, 1, 'Pen');
SAVEPOINT sp_order_created;

UPDATE Accounts SET balance = balance - 20 WHERE id = 1;
-- Suppose balance check fails in application logic:
ROLLBACK TO SAVEPOINT sp_order_created;

-- Decide either to fix and continue, or rollback entire transaction
ROLLBACK;   -- or COMMIT if remaining state is correct
```

### Beginner tip
Savepoints do not replace good design. Prefer small clear transactions when you can.

---

## 4. Knowledge Check

1. What problem does SAVEPOINT solve?
2. Write SQL creating savepoint `sp1` after an insert.
3. What does `ROLLBACK TO sp1` keep vs undo?
4. Does a savepoint permanently save data to disk by itself?

---

**Previous:** [← COMMIT](./00-Commit.md)
**Next:** [ROLLBACK →](./02-Rollback.md)
