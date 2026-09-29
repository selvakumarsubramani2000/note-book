# 🗑️ DML — DELETE

> **Trainer's Note:** `DELETE` removes existing row(s). Like `UPDATE`, a missing `WHERE` can wipe the whole table.

---

## 📑 Table of Contents
1. [Basic DELETE](#1-basic-delete)
2. [DELETE with Conditions](#2-delete-with-conditions)
3. [DELETE vs TRUNCATE](#3-delete-vs-truncate)
4. [Foreign Key Blocking](#4-foreign-key-blocking)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Basic DELETE

```sql
DELETE FROM Students
WHERE student_id = 4;
```

### Real-world analogy
```
DELETE = removing specific folders from the drawer
  The drawer itself stays
```

---

## 2. DELETE with Conditions

```sql
DELETE FROM Orders
WHERE status = 'CANCELLED'
  AND order_date < DATE '2024-01-01';

-- Delete using a subquery list
DELETE FROM Students
WHERE student_id IN (
    SELECT student_id FROM InactiveStudents
);
```

---

## 3. DELETE vs TRUNCATE

| | DELETE | TRUNCATE |
|---|--------|----------|
| Can use WHERE | Yes | No |
| Row-by-row logging | Often yes | Bulk operation |
| Table structure | Kept | Kept |
| Typical category | DML | DDL-like |

Use `DELETE` when you need selective removal or triggers/logging behavior.

---

## 4. Foreign Key Blocking

```sql
-- May fail if Orders still reference this student
DELETE FROM Students WHERE student_id = 1;
```

Options:
- delete/update child rows first
- design ON DELETE CASCADE carefully (advanced)
- soft-delete with a `status` flag in apps

### Beginner tip
Preview first:

```sql
SELECT * FROM Students WHERE city = 'TestCity';
DELETE FROM Students WHERE city = 'TestCity';
```

---

## 5. Knowledge Check

1. Write SQL to delete order `9001`.
2. Why is `DELETE FROM Students;` dangerous?
3. When is `TRUNCATE` a better fit than `DELETE`?
4. Why might deleting a parent row fail?

---

**Previous:** [← UPDATE](./01-Update.md)
**Next:** [TCL COMMIT →](../15-TCL/00-Commit.md)
