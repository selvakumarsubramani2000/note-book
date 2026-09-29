# 🏗️ Data Definition Language (DDL)

> **Trainer's Note:** **DDL** builds and reshapes database structure — tables, columns, constraints — not the row values inside them.

---

## 📑 Table of Contents
1. [What DDL Does](#1-what-ddl-does)
2. [CREATE](#2-create)
3. [ALTER](#3-alter)
4. [DROP and TRUNCATE](#4-drop-and-truncate)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What DDL Does

DDL answers: *"What objects exist, and what shape are they?"*

| Command | Purpose |
|---------|---------|
| `CREATE` | Make a new object (table, view, index...) |
| `ALTER` | Change an existing object's structure |
| `DROP` | Remove an object completely |
| `TRUNCATE` | Remove all rows from a table quickly (structure stays) |

---

## 2. CREATE

```sql
CREATE TABLE Students (
    student_id INT PRIMARY KEY,
    name       VARCHAR(50) NOT NULL,
    email      VARCHAR(100) UNIQUE,
    age        INT
);
```

Also used for views, indexes, etc.:
```sql
CREATE INDEX idx_students_name ON Students(name);
```

---

## 3. ALTER

```sql
-- Add a column
ALTER TABLE Students ADD phone VARCHAR(20);

-- Modify a column (syntax varies by product)
ALTER TABLE Students MODIFY age INT NOT NULL;

-- Drop a column
ALTER TABLE Students DROP COLUMN phone;
```

---

## 4. DROP and TRUNCATE

```sql
DROP TABLE Students;       -- table structure + data gone
TRUNCATE TABLE Students;   -- all rows deleted, empty table remains
```

| | `DELETE` (DML) | `TRUNCATE` (DDL-ish) | `DROP` (DDL) |
|---|----------------|----------------------|--------------|
| Removes rows | Yes (can be filtered) | Yes (all rows) | Yes (with table) |
| Removes table | No | No | Yes |
| WHERE clause | Yes | No | N/A |

### Real-world analogy
```
CREATE  = build a new cabinet
ALTER   = add/remove a drawer label slot
TRUNCATE = empty every folder but keep the cabinet
DROP    = haul the cabinet out of the building
```

### Beginner tip
`DROP` and `TRUNCATE` are hard to undo. In real systems, treat them as production-dangerous commands.

---

## 5. Knowledge Check

1. What does DDL stand for, and what does it manage?
2. Write a `CREATE TABLE` for `Teachers(id, name)`.
3. Difference between `DROP TABLE` and `TRUNCATE TABLE`?
4. Which command adds a new column to an existing table?

---

**Previous:** [← SQL Statements Overview](./00-SQL-Statements-Overview.md)
**Next:** [DML →](./02-DML.md)
