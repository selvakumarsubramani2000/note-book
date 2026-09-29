# 💣 DDL — DROP

> **Trainer's Note:** `DROP` permanently removes a database object (table, view, index, etc.). Structure and data both go away for tables.

---

## 📑 Table of Contents
1. [DROP TABLE](#1-drop-table)
2. [DROP Other Objects](#2-drop-other-objects)
3. [DROP vs TRUNCATE vs DELETE](#3-drop-vs-truncate-vs-delete)
4. [Dependency Issues](#4-dependency-issues)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. DROP TABLE

```sql
DROP TABLE Students;

-- Safer pattern in some engines
DROP TABLE IF EXISTS Students;
```

### Real-world analogy
```
DROP = haul the entire cabinet out of the building
  Not just empty it — remove it completely
```

---

## 2. DROP Other Objects

```sql
DROP VIEW vw_adult_students;
DROP INDEX idx_students_email;
DROP PROCEDURE sp_refresh_stats;   -- if your engine supports it this way
```

---

## 3. DROP vs TRUNCATE vs DELETE

| Goal | Command |
|------|---------|
| Remove some rows | `DELETE ... WHERE` |
| Empty table, keep definition | `TRUNCATE TABLE` |
| Remove table entirely | `DROP TABLE` |

---

## 4. Dependency Issues

```sql
-- May fail if Orders.student_id references Students
DROP TABLE Students;
```

Options (product-specific):
- drop child objects first
- drop constraints first
- use cascade options carefully (`CASCADE` where supported)

### Beginner tip
`DROP` is irreversible in normal app use. Prefer migrations and backups before dropping anything shared.

---

## 5. Knowledge Check

1. What does `DROP TABLE` remove?
2. Write SQL to drop a view named `vw_sales`.
3. Why might `DROP TABLE Parents` fail when children still reference it?
4. Choose: empty practice data but keep table for tomorrow’s lab — `DROP` or `TRUNCATE`?

---

**Previous:** [← TRUNCATE](./03-Truncate.md)
**Next:** [DML INSERT →](../14-DML/00-Insert.md)
