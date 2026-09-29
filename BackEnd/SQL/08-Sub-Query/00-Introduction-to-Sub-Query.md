# 🪆 Introduction to Sub Query

> **Trainer's Note:** A **subquery** is a query nested inside another query. You use it when the main question depends on an answer you must calculate first.

---

## 📑 Table of Contents
1. [What Is a Subquery?](#1-what-is-a-subquery)
2. [Why Subqueries Exist](#2-why-subqueries-exist)
3. [Where a Subquery Can Appear](#3-where-a-subquery-can-appear)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. What Is a Subquery?

```sql
SELECT name, age
FROM Students
WHERE age > (SELECT AVG(age) FROM Students);
```

Inner query finds average age. Outer query returns students older than that average.

### Real-world analogy
```
Subquery = asking a helper question first
  Helper: "What is the class average age?"
  Main:   "Who is older than that number?"
```

---

## 2. Why Subqueries Exist

| Need | Subquery helps by... |
|------|----------------------|
| Compare to a calculated value | average, max, min from same/other table |
| Filter with a list of values | IDs returned from another query |
| Build a temporary result | use inner query as a derived table |

They keep logic in one SQL statement instead of requiring manual intermediate results.

---

## 3. Where a Subquery Can Appear

| Location | Role |
|----------|------|
| `WHERE` | Filter using computed value/list |
| `FROM` | Act like a temporary table |
| `SELECT` list | Compute a per-row scalar value |
| `HAVING` | Filter groups using a nested calculation |

```sql
-- FROM subquery (derived table)
SELECT dept, avg_sal
FROM (
    SELECT department AS dept, AVG(salary) AS avg_sal
    FROM Employees
    GROUP BY department
) t
WHERE avg_sal > 60000;
```

### Beginner tip
Read subqueries **inside-out**: solve the inner parentheses first, then the outer query.

---

## 4. Knowledge Check

1. What is a subquery in one sentence?
2. In the average-age example, which query runs first?
3. Name two clauses where a subquery can appear.
4. Invent a plain-English question that naturally needs a subquery.

---

**Previous:** [← Multi Row Functions](../07-Functions-in-SQL/01-Multi-Row-Functions.md)
**Next:** [Working of Sub Query →](./01-Working-of-Sub-Query.md)
