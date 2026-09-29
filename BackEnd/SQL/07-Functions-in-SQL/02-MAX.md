# 📈 MAX()

> **Trainer's Note:** `MAX()` is a multi-row (aggregate) function that returns the **largest** value in a column.

---

## 📑 Table of Contents
1. [What MAX Does](#1-what-max-does)
2. [Basic Examples](#2-basic-examples)
3. [MAX with GROUP BY](#3-max-with-group-by)
4. [MAX in a Subquery](#4-max-in-a-subquery)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What MAX Does

```sql
SELECT MAX(salary) AS highest_salary
FROM Employees;
```

Works with numbers, dates, and (alphabetically) text.

### Real-world analogy
```
MAX = looking through a stack of score sheets
  and pulling out only the single highest score
```

---

## 2. Basic Examples

```sql
SELECT MAX(age) FROM Students;
SELECT MAX(order_date) FROM Orders;          -- most recent date
SELECT MAX(product_name) FROM Products;      -- last name alphabetically
```

`NULL` values are ignored.

---

## 3. MAX with GROUP BY

```sql
SELECT department, MAX(salary) AS top_salary
FROM Employees
GROUP BY department;
```

One maximum **per department**.

---

## 4. MAX in a Subquery

```sql
-- Employee(s) who earn the highest salary
SELECT name, salary
FROM Employees
WHERE salary = (SELECT MAX(salary) FROM Employees);
```

### Beginner tip
`MAX()` returns one summary value (or one per group). It does not automatically return the full row — pair it with a subquery or join if you need the related name/id.

---

## 5. Knowledge Check

1. What does `MAX(price)` return from a `Products` table?
2. Write SQL for the latest `created_at` in `Tickets`.
3. Write SQL for highest salary per `job_title`.
4. Why might `SELECT name, MAX(salary) FROM Employees` fail without `GROUP BY`?

---

**Previous:** [← Multi Row Functions](./01-Multi-Row-Functions.md)
**Next:** [MIN() →](./03-MIN.md)
