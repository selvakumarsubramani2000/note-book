# 🏷️ DDL — RENAME

> **Trainer's Note:** `RENAME` changes the name of an existing object (commonly a table). Syntax is product-specific.

---

## 📑 Table of Contents
1. [Why Rename?](#1-why-rename)
2. [Oracle-Style RENAME](#2-oracle-style-rename)
3. [Other Databases](#3-other-databases)
4. [What Breaks When You Rename](#4-what-breaks-when-you-rename)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Why Rename?

Use rename when a table/column name is unclear, outdated, or inconsistent with naming standards.

### Real-world analogy
```
RENAME = changing the label on a filing cabinet drawer
  Contents stay; only the name tag changes
```

---

## 2. Oracle-Style RENAME

```sql
RENAME Students TO Learners;

-- Or older form still seen in labs
RENAME Students TO Learners;
```

Some Oracle versions also support:
```sql
ALTER TABLE Students RENAME TO Learners;
```

---

## 3. Other Databases

```sql
-- PostgreSQL / many engines
ALTER TABLE students RENAME TO learners;

-- Rename a column (PostgreSQL example)
ALTER TABLE learners RENAME COLUMN name TO full_name;

-- SQL Server style table rename
EXEC sp_rename 'Students', 'Learners';
```

Always check your product docs — rename is one of the least-standard DDL areas.

---

## 4. What Breaks When You Rename

| Dependent item | Risk |
|----------------|------|
| Application SQL | Queries still using old name fail |
| Views / procedures | May need recompile or rewrite |
| Scripts and reports | Hard-coded names break |
| Documentation | Becomes stale |

### Beginner tip
Prefer good names at `CREATE` time. Rename in shared databases only with a migration plan.

---

## 5. Knowledge Check

1. What does RENAME change, and what does it not change?
2. Write an Oracle-style rename of `Orders` to `CustomerOrders`.
3. Why can renaming a production table be risky?
4. Is rename syntax identical in every database?

---

**Previous:** [← CREATE](./00-Create.md)
**Next:** [ALTER →](./02-Alter.md)
