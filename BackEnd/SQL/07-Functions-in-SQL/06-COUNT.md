# 🔢 COUNT()

> **Trainer's Note:** `COUNT()` answers “how many?” — rows, non-null values, or distinct values depending on how you write it.

---

## 📑 Table of Contents
1. [COUNT(*) vs COUNT(column)](#1-count-vs-countcolumn)
2. [COUNT(DISTINCT ...)](#2-countdistinct-)
3. [COUNT with WHERE and GROUP BY](#3-count-with-where-and-group-by)
4. [COUNT with HAVING](#4-count-with-having)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. COUNT(*) vs COUNT(column)

```sql
SELECT COUNT(*) FROM Students;           -- every row
SELECT COUNT(email) FROM Students;       -- rows where email is not NULL
```

| Form | Counts |
|------|--------|
| `COUNT(*)` | All rows (nulls in other columns don't matter) |
| `COUNT(col)` | Non-null values in `col` only |

### Real-world analogy
```
COUNT(*)     = how many folders are in the drawer
COUNT(email) = how many folders have an email written on them
```

---

## 2. COUNT(DISTINCT ...)

```sql
SELECT COUNT(DISTINCT city) FROM Students;
SELECT COUNT(DISTINCT student_id) FROM Orders;
```

Counts unique values (nulls still ignored).

---

## 3. COUNT with WHERE and GROUP BY

```sql
SELECT COUNT(*) FROM Orders WHERE status = 'PAID';

SELECT department, COUNT(*) AS headcount
FROM Employees
GROUP BY department;
```

---

## 4. COUNT with HAVING

```sql
SELECT student_id, COUNT(*) AS order_count
FROM Orders
GROUP BY student_id
HAVING COUNT(*) >= 3;
```

### Beginner tip
Filtering on `COUNT(...)` belongs in `HAVING`, not `WHERE`, because the count exists only after grouping.

---

## 5. Knowledge Check

1. Difference between `COUNT(*)` and `COUNT(phone)`?
2. Write SQL for number of employees in department `'IT'`.
3. Write SQL for how many distinct products appear in `OrderItems`.
4. Write SQL for students who placed at least 2 orders.

---

**Previous:** [← AVG()](./05-AVG.md)
**Next:** [Introduction to Sub Query →](../08-Sub-Query/00-Introduction-to-Sub-Query.md)
