# 🛠️ Pseudo Columns — Working and Usage

> **Trainer's Note:** This wrap-up shows how `ROWID` and `ROWNUM` appear together in real lab tasks and when to choose each.

---

## 📑 Table of Contents
1. [Side-by-Side Comparison](#1-side-by-side-comparison)
2. [Common Lab Tasks](#2-common-lab-tasks)
3. [Usage Guidelines](#3-usage-guidelines)
4. [Quick Practice Set](#4-quick-practice-set)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Side-by-Side Comparison

| | `ROWID` | `ROWNUM` |
|---|---------|----------|
| Meaning | Physical row address | Temporary result sequence number |
| Stable for app identity? | No (prefer PK) | No |
| Typical use | Locate/delete specific physical rows | Limit Top-N rows |
| Assigned when | Exists for stored rows | During query execution |

```sql
SELECT ROWNUM AS rn, ROWID, name
FROM Students
WHERE ROWNUM <= 10;
```

---

## 2. Common Lab Tasks

**Task A — preview first rows**
```sql
SELECT * FROM Employees WHERE ROWNUM <= 10;
```

**Task B — top salaries**
```sql
SELECT *
FROM (
    SELECT name, salary FROM Employees ORDER BY salary DESC
)
WHERE ROWNUM <= 5;
```

**Task C — keep one row per duplicate group**
```sql
DELETE FROM Contacts
WHERE ROWID NOT IN (
    SELECT MIN(ROWID) FROM Contacts GROUP BY email
);
```

---

## 3. Usage Guidelines

| Do | Don't |
|----|-------|
| Use `ROWNUM` for Oracle Top-N practice | Assume `ROWNUM` equals a permanent rank column |
| Use `ROWID` for cleanup scripts in Oracle | Use `ROWID` as a foreign key in applications |
| Prefer PK/FK design for relationships | Build business logic that depends on physical addresses |
| Remember product differences | Expect identical pseudo columns in MySQL/SQL Server |

### Real-world analogy
```
ROWID  = warehouse bin location label
ROWNUM = temporary ticket number handed out while lining up for service
Both are useful operationally; neither replaces a person's permanent ID card (PK)
```

---

## 4. Quick Practice Set

1. Display first 8 rows of `Orders` using `ROWNUM`.
2. Display top 3 most expensive products correctly (order + `ROWNUM`).
3. Select `ROWID` with `product_id` from `Products`.
4. Explain when duplicate deletion via `MIN(ROWID)` is appropriate.

---

## 5. Knowledge Check

1. Which pseudo column helps Top-N queries in classic Oracle SQL?
2. Which helps identify a physical row for cleanup?
3. Why should primary keys still exist if `ROWID` already uniquely identifies rows?
4. Write the safe Top-N pattern in two layers (inner/outer).

---

**Previous:** [← ROWNUM](./02-ROWNUM.md)
**Next:** [What Is Join? →](../11-Joins/00-What-Is-Join.md)
