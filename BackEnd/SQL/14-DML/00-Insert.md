# ✍️ DML — INSERT

> **Trainer's Note:** `INSERT` adds new row(s) into a table. Prefer explicit column lists so your SQL stays clear when the table structure evolves.

---

## 📑 Table of Contents
1. [Single-Row INSERT](#1-single-row-insert)
2. [Multi-Row INSERT](#2-multi-row-insert)
3. [INSERT ... SELECT](#3-insert--select)
4. [Common Errors](#4-common-errors)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Single-Row INSERT

```sql
INSERT INTO Students (student_id, name, age, email)
VALUES (1, 'Amy', 21, 'amy@example.com');
```

### Real-world analogy
```
INSERT = placing a brand-new folder into the drawer
  with values written on each required label field
```

---

## 2. Multi-Row INSERT

```sql
INSERT INTO Students (student_id, name, age) VALUES
(2, 'Raj', 23),
(3, 'Meera', 20),
(4, 'John', 22);
```

---

## 3. INSERT ... SELECT

Copy rows from one query/table into another:

```sql
INSERT INTO Alumni (student_id, name, email)
SELECT student_id, name, email
FROM Students
WHERE graduated = 'Y';
```

---

## 4. Common Errors

| Error | Cause |
|-------|-------|
| Missing required column | `NOT NULL` / no default |
| Duplicate primary key / unique | Key already exists |
| Datatype mismatch | Wrong value shape |
| FK violation | Parent key doesn’t exist |

### Beginner tip
Always list columns in `INSERT INTO t (col1, col2)` — relying on default column order is fragile.

---

## 5. Knowledge Check

1. Write an insert for course `(101, 'SQL Basics', 3)`.
2. Why list column names explicitly?
3. What does `INSERT ... SELECT` do?
4. Name two constraints that can block an insert.

---

**Previous:** [← DROP](../13-DDL/04-Drop.md)
**Next:** [UPDATE →](./01-Update.md)
