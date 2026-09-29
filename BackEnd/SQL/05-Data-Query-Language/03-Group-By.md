# 📦 GROUP BY

> **Trainer's Note:** `GROUP BY` collapses rows into buckets (groups) so aggregate functions can summarize each bucket — totals per department, counts per city, and so on.

---

## 📑 Table of Contents
1. [Why GROUP BY Exists](#1-why-group-by-exists)
2. [Basic Syntax](#2-basic-syntax)
3. [Rules You Must Follow](#3-rules-you-must-follow)
4. [Multi-Column Grouping](#4-multi-column-grouping)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Why GROUP BY Exists

```sql
-- One total for the whole table
SELECT COUNT(*) FROM Orders;

-- Separate totals per student
SELECT student_id, COUNT(*) AS order_count
FROM Orders
GROUP BY student_id;
```

### Real-world analogy
```
GROUP BY = sorting exam papers into piles by class section,
then writing one summary sticky-note on each pile
```

---

## 2. Basic Syntax

```sql
SELECT department, AVG(salary) AS avg_salary
FROM Employees
GROUP BY department;
```

Flow:
1. Rows are collected from `FROM` / `WHERE`
2. Rows are placed into groups by `department`
3. `AVG(salary)` is computed **per group**

---

## 3. Rules You Must Follow

In the `SELECT` list with `GROUP BY`, each item must be either:
- included in the `GROUP BY` column list, or
- wrapped in an aggregate (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, ...)

```sql
-- Invalid in most engines: name is neither grouped nor aggregated
SELECT name, department, COUNT(*)
FROM Employees
GROUP BY department;
```

---

## 4. Multi-Column Grouping

```sql
SELECT department, job_title, COUNT(*) AS headcount
FROM Employees
GROUP BY department, job_title;
```

Creates a group for each unique pair `(department, job_title)`.

### Beginner tip
Filter individual rows with `WHERE` **before** grouping. Filter groups with `HAVING` **after** grouping (next lesson).

---

## 5. Knowledge Check

1. What does `GROUP BY` produce compared to a plain `SELECT`?
2. Write a query counting orders per `status`.
3. Why is `SELECT name, COUNT(*) ... GROUP BY department` usually invalid?
4. Give one multi-column grouping example idea from real life.

---

**Previous:** [← WHERE](./02-Where.md)
**Next:** [HAVING →](./04-Having.md)
