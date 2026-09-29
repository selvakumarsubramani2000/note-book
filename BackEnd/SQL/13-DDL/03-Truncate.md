# 🧹 DDL — TRUNCATE

> **Trainer's Note:** `TRUNCATE` removes **all rows** from a table quickly, but keeps the table structure. Treat it as a high-risk command.

---

## 📑 Table of Contents
1. [What TRUNCATE Does](#1-what-truncate-does)
2. [Syntax](#2-syntax)
3. [TRUNCATE vs DELETE vs DROP](#3-truncate-vs-delete-vs-drop)
4. [Cautions](#4-cautions)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What TRUNCATE Does

```sql
TRUNCATE TABLE Students;
```

Result:
- all data rows gone
- table shell (columns/constraints) remains
- usually **cannot filter** with `WHERE`

### Real-world analogy
```
TRUNCATE = empty every folder from a drawer in one sweep
  The drawer and label remain; papers are gone
```

---

## 2. Syntax

```sql
TRUNCATE TABLE OrderItems;
-- some engines: TRUNCATE OrderItems;
```

---

## 3. TRUNCATE vs DELETE vs DROP

| Command | Rows | Structure | WHERE? | Typical category |
|---------|------|-----------|--------|------------------|
| `DELETE FROM t` | Selected/all rows | Kept | Yes | DML |
| `TRUNCATE TABLE t` | All rows | Kept | No | DDL (commonly) |
| `DROP TABLE t` | Gone with table | Removed | N/A | DDL |

`TRUNCATE` is often faster than `DELETE` all rows because it deallocates data in bulk rather than logging every row delete (engine-dependent details).

---

## 4. Cautions

| Caution | Why |
|---------|-----|
| Hard to undo | Especially outside explicit recovery setups |
| FK references | May fail if child tables still reference rows |
| Identity/sequence behavior | Reset rules differ by product |
| Permissions | Often requires higher privileges than DELETE |

### Beginner tip
In labs, double-check the table name twice. In production, require backup + explicit approval before `TRUNCATE`.

---

## 5. Knowledge Check

1. Does `TRUNCATE` remove the table itself?
2. Can you `TRUNCATE` only rows where `status = 'OLD'`?
3. When would you choose `DELETE` over `TRUNCATE`?
4. Difference between `TRUNCATE TABLE t` and `DROP TABLE t`?

---

**Previous:** [← ALTER](./02-Alter.md)
**Next:** [DROP →](./04-Drop.md)
