# 💳 Transaction Control Language (TCL)

> **Trainer's Note:** **TCL** controls whether a group of data changes becomes permanent or is undone — essential for "all or nothing" operations.

---

## 📑 Table of Contents
1. [What Is a Transaction?](#1-what-is-a-transaction)
2. [COMMIT](#2-commit)
3. [ROLLBACK](#3-rollback)
4. [SAVEPOINT](#4-savepoint)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What Is a Transaction?

A **transaction** is a set of one or more SQL statements treated as one unit.

```sql
BEGIN TRANSACTION;     -- start (syntax varies: BEGIN, START TRANSACTION, etc.)

UPDATE Accounts SET balance = balance - 100 WHERE id = 1;
UPDATE Accounts SET balance = balance + 100 WHERE id = 2;

COMMIT;                -- make both permanent
-- or ROLLBACK;        -- undo both
```

### Real-world analogy
```
Transaction = a bank transfer form with two lines:
  1) deduct from A
  2) credit to B
Either BOTH lines complete, or NEITHER should stick
```

---

## 2. COMMIT

```sql
COMMIT;
```

Saves all changes made in the current transaction permanently.

---

## 3. ROLLBACK

```sql
ROLLBACK;
```

Cancels all uncommitted changes in the current transaction.

```sql
BEGIN TRANSACTION;
UPDATE Products SET stock = stock - 1 WHERE product_id = 10;
-- something looks wrong...
ROLLBACK;   -- stock change discarded
```

---

## 4. SAVEPOINT

A named marker inside a transaction so you can undo only part of the work.

```sql
BEGIN TRANSACTION;
UPDATE ...;                 -- step A
SAVEPOINT sp1;
UPDATE ...;                 -- step B
ROLLBACK TO sp1;         -- undo step B, keep step A
COMMIT;                  -- finalize what remains
```

| Command | Meaning |
|---------|---------|
| `COMMIT` | Make changes permanent |
| `ROLLBACK` | Undo entire current transaction |
| `SAVEPOINT name` | Mark a mid-point |
| `ROLLBACK TO name` | Undo back to that mid-point |

### Beginner tip
Some environments auto-commit every statement. In learning tools and enterprise DBs, always know whether you are in auto-commit mode before experimenting with `UPDATE`/`DELETE`.

---

## 5. Knowledge Check

1. What problem do transactions solve?
2. Difference between `COMMIT` and `ROLLBACK`?
3. When is `SAVEPOINT` useful?
4. Write a tiny transaction that updates two rows and commits.

---

**Previous:** [← DML](./02-DML.md)
**Next:** [DCL →](./04-DCL.md)
