# 📝 DML — UPDATE

> **Trainer's Note:** `UPDATE` changes existing row values. Always decide the `WHERE` clause carefully — without it, every row can change.

---

## 📑 Table of Contents
1. [Basic UPDATE](#1-basic-update)
2. [Update Multiple Columns](#2-update-multiple-columns)
3. [UPDATE with Subquery](#3-update-with-subquery)
4. [Safety Habits](#4-safety-habits)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Basic UPDATE

```sql
UPDATE Students
SET age = 22
WHERE student_id = 1;
```

### Real-world analogy
```
UPDATE = rewriting one or more fields on folders
  that already exist in the drawer
```

---

## 2. Update Multiple Columns

```sql
UPDATE Students
SET name = 'Amy Sharma',
    email = 'amy.sharma@example.com',
    age = 22
WHERE student_id = 1;
```

---

## 3. UPDATE with Subquery

```sql
UPDATE Employees
SET salary = salary * 1.10
WHERE department_id = (
    SELECT department_id FROM Departments WHERE dept_name = 'IT'
);
```

```sql
-- Raise salaries below department average (correlated idea)
UPDATE Employees e
SET salary = salary * 1.05
WHERE salary < (
    SELECT AVG(x.salary) FROM Employees x
    WHERE x.department_id = e.department_id
);
```

(Support for correlated UPDATE syntax varies; the idea is widely taught.)

---

## 4. Safety Habits

| Habit | Why |
|-------|-----|
| Write `SELECT` with same `WHERE` first | Preview target rows |
| Use transactions | `ROLLBACK` if wrong |
| Avoid bare `UPDATE t SET ...` | Prevents full-table rewrite accidents |
| Prefer key-based filters | Precise targeting |

```sql
-- Preview
SELECT * FROM Students WHERE city = 'Chennai';
-- Then update
UPDATE Students SET city = 'CHENNAI' WHERE city = 'Chennai';
```

### Beginner tip
In training labs with auto-commit on, practice on tiny tables first.

---

## 5. Knowledge Check

1. What happens if `UPDATE` has no `WHERE`?
2. Write SQL to set `status = 'CLOSED'` for order `5001`.
3. Why preview with `SELECT` before updating?
4. Write an update that increases all `Products.unit_price` by 5%.

---

**Previous:** [← INSERT](./00-Insert.md)
**Next:** [DELETE →](./02-Delete.md)
