# 🔧 DDL — ALTER

> **Trainer's Note:** `ALTER` changes an existing table’s structure — add/drop/modify columns and constraints without dropping the whole table.

---

## 📑 Table of Contents
1. [Add a Column](#1-add-a-column)
2. [Modify a Column](#2-modify-a-column)
3. [Drop a Column](#3-drop-a-column)
4. [Add / Drop Constraints](#4-add--drop-constraints)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Add a Column

```sql
ALTER TABLE Students
ADD phone VARCHAR(20);

-- With default (syntax varies slightly)
ALTER TABLE Students
ADD status VARCHAR(20) DEFAULT 'ACTIVE';
```

---

## 2. Modify a Column

```sql
-- Oracle-style
ALTER TABLE Students
MODIFY age NUMBER(3);

-- SQL Server-style
-- ALTER TABLE Students ALTER COLUMN age INT NOT NULL;

-- PostgreSQL-style
-- ALTER TABLE students ALTER COLUMN age TYPE INT;
```

### Real-world analogy
```
ALTER = renovating drawers/labels on an existing cabinet
  instead of throwing the cabinet away and rebuilding it
```

---

## 3. Drop a Column

```sql
ALTER TABLE Students
DROP COLUMN phone;
```

Dropping a column **deletes that data permanently**.

---

## 4. Add / Drop Constraints

```sql
ALTER TABLE Students
ADD CONSTRAINT uq_students_email UNIQUE (email);

ALTER TABLE Orders
ADD CONSTRAINT fk_orders_student
FOREIGN KEY (student_id) REFERENCES Students(student_id);

ALTER TABLE Students
DROP CONSTRAINT uq_students_email;
```

If existing rows violate a new constraint, the `ALTER` fails until data is cleaned.

### Beginner tip
In team projects, put every `ALTER` in a versioned migration script so environments stay in sync.

---

## 5. Knowledge Check

1. What is the difference between `CREATE` and `ALTER`?
2. Write SQL to add `city VARCHAR(50)` to `Customers`.
3. Write SQL to add a unique constraint on `Customers.email`.
4. Why might adding `NOT NULL` to an existing column fail?

---

**Previous:** [← RENAME](./01-Rename.md)
**Next:** [TRUNCATE →](./03-Truncate.md)
