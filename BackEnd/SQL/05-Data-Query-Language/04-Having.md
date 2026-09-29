# 🎯 HAVING

> **Trainer's Note:** `HAVING` filters **groups** after `GROUP BY`. If `WHERE` is a bouncer for individual rows, `HAVING` is a bouncer for whole groups.

---

## 📑 Table of Contents
1. [HAVING vs WHERE](#1-having-vs-where)
2. [Basic HAVING Example](#2-basic-having-example)
3. [Combined Query Pattern](#3-combined-query-pattern)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. HAVING vs WHERE

| | `WHERE` | `HAVING` |
|---|---------|----------|
| Filters | Individual rows | Groups |
| Works with aggregates? | No (before grouping) | Yes (`COUNT`, `SUM`, ...) |
| Runs | Before `GROUP BY` | After `GROUP BY` |

```sql
-- WHERE filters rows first, HAVING filters groups later
SELECT student_id, COUNT(*) AS order_count
FROM Orders
WHERE status = 'PAID'          -- row filter
GROUP BY student_id
HAVING COUNT(*) >= 3;          -- group filter
```

### Real-world analogy
```
WHERE  = remove individual unreadable exam papers first
GROUP BY = pile remaining papers by student
HAVING = keep only piles that have 3 or more papers
```

---

## 2. Basic HAVING Example

```sql
SELECT department, AVG(salary) AS avg_sal
FROM Employees
GROUP BY department
HAVING AVG(salary) > 70000;
```

Only departments whose average salary exceeds 70000 appear in the result.

---

## 3. Combined Query Pattern

```sql
SELECT column, AGG(column)
FROM table
WHERE row_condition
GROUP BY column
HAVING group_condition
ORDER BY column;
```

### Beginner tip
If your condition uses `COUNT(...)`, `SUM(...)`, `AVG(...)`, it almost certainly belongs in `HAVING`, not `WHERE`.

---

## 4. Knowledge Check

1. Does `HAVING` filter rows or groups?
2. Rewrite in words: `GROUP BY city HAVING COUNT(*) > 10`.
3. Can `WHERE COUNT(*) > 10` replace `HAVING COUNT(*) > 10`? Why/why not?
4. Write a query showing products with total sold quantity at least 100 (`order_items(product_id, qty)`).

---

**Previous:** [← GROUP BY](./03-Group-By.md)
**Next:** [ORDER BY →](./05-Order-By.md)
