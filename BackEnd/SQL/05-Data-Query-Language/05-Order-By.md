# ↕️ ORDER BY

> **Trainer's Note:** `ORDER BY` sorts the final result set. It does not change how rows are stored — only how they are returned to you.

---

## 📑 Table of Contents
1. [Ascending and Descending](#1-ascending-and-descending)
2. [Sort by Multiple Columns](#2-sort-by-multiple-columns)
3. [ORDER BY with Aliases and Positions](#3-order-by-with-aliases-and-positions)
4. [Typical Full DQL Pattern](#4-typical-full-dql-pattern)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Ascending and Descending

```sql
SELECT name, age
FROM Students
ORDER BY age ASC;     -- ascending (default)

SELECT name, age
FROM Students
ORDER BY age DESC;    -- descending
```

### Real-world analogy
```
ORDER BY = stacking returned folders alphabetically or by age
before handing them to you
```

---

## 2. Sort by Multiple Columns

```sql
SELECT department, name, salary
FROM Employees
ORDER BY department ASC, salary DESC;
```

Meaning:
1. Sort by department A→Z
2. Within the same department, highest salary first

---

## 3. ORDER BY with Aliases and Positions

```sql
SELECT name AS student_name, age
FROM Students
ORDER BY student_name;

-- Position numbers work in many engines (less readable)
SELECT name, age FROM Students ORDER BY 2 DESC;
```

Prefer column names/aliases over position numbers in real code.

---

## 4. Typical Full DQL Pattern

```sql
SELECT student_id, COUNT(*) AS order_count
FROM Orders
WHERE status = 'PAID'
GROUP BY student_id
HAVING COUNT(*) >= 2
ORDER BY order_count DESC;
```

Clause order matters and is usually taught as:
`SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY`

### Beginner tip
`ORDER BY` is applied last to the final answer set. Sorting earlier intermediate steps is the engine's job, not something you force with clause order.

---

## 5. Knowledge Check

1. Does `ORDER BY` permanently re-sort the table on disk?
2. Write a query listing products by price high to low.
3. What does `ORDER BY city, name` mean?
4. Place these in correct logical clause order: `HAVING`, `WHERE`, `ORDER BY`, `GROUP BY`.

---

**Previous:** [← HAVING](./04-Having.md)
**Next:** [Operators — Types and Examples →](../06-Operators/00-Operators-Types-and-Examples.md)
