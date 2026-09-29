# ✍️ Data Manipulation Language (DML)

> **Trainer's Note:** **DML** changes the **data** inside tables — insert new rows, update existing rows, delete rows.

---

## 📑 Table of Contents
1. [What DML Does](#1-what-dml-does)
2. [INSERT](#2-insert)
3. [UPDATE](#3-update)
4. [DELETE](#4-delete)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What DML Does

| Command | Purpose |
|---------|---------|
| `INSERT` | Add new row(s) |
| `UPDATE` | Change values in existing row(s) |
| `DELETE` | Remove existing row(s) |

Structure stays the same; only row contents change.

---

## 2. INSERT

```sql
-- Insert with column list (preferred)
INSERT INTO Students (student_id, name, age)
VALUES (1, 'Amy', 21);

-- Insert multiple rows (supported in most modern engines)
INSERT INTO Students (student_id, name, age) VALUES
(2, 'Raj', 23),
(3, 'Meera', 20);
```

---

## 3. UPDATE

```sql
-- ALWAYS use WHERE unless you truly mean "every row"
UPDATE Students
SET age = 22
WHERE student_id = 1;

UPDATE Students
SET name = 'Amy Sharma', age = 22
WHERE student_id = 1;
```

### Beginner tip
Forgetting `WHERE` on `UPDATE` is a classic disaster — it can rewrite the entire table.

---

## 4. DELETE

```sql
DELETE FROM Students
WHERE student_id = 3;

-- Deletes ALL rows (table structure remains)
DELETE FROM Students;
```

| Command | Effect |
|---------|--------|
| `DELETE FROM t WHERE ...` | Selected rows removed |
| `DELETE FROM t` | All rows removed |
| `TRUNCATE TABLE t` | All rows removed (usually faster; fewer row-level extras) |

### Real-world analogy
```
INSERT = add a new folder to the drawer
UPDATE = rewrite information on an existing folder label
DELETE = remove one or more folders
```

---

## 5. Knowledge Check

1. Which three commands make up core DML?
2. Write an `INSERT` for a student named `John`, age `19`, id `10`.
3. Why is `WHERE` critical in `UPDATE` and `DELETE`?
4. Does `DELETE FROM Students;` remove the `Students` table itself?

---

**Previous:** [← DDL](./01-DDL.md)
**Next:** [TCL →](./03-TCL.md)
