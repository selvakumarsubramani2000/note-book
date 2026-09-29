# 📊 AVG()

> **Trainer's Note:** `AVG()` returns the **average (mean)** of numeric values — total divided by the count of non-null values.

---

## 📑 Table of Contents
1. [What AVG Does](#1-what-avg-does)
2. [Basic Examples](#2-basic-examples)
3. [AVG with GROUP BY](#3-avg-with-group-by)
4. [AVG vs Manual Total/Count](#4-avg-vs-manual-totalcount)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What AVG Does

```sql
SELECT AVG(age) AS average_age
FROM Students;
```

`NULL` ages are ignored (not treated as zero).

### Real-world analogy
```
AVG = class average marks
  Add all scores, divide by how many scored papers you have
  (blank papers without scores don't count)
```

---

## 2. Basic Examples

```sql
SELECT AVG(salary) FROM Employees;
SELECT AVG(unit_price) FROM Products WHERE category = 'Books';
SELECT ROUND(AVG(score), 2) FROM ExamResults;   -- often round for display
```

---

## 3. AVG with GROUP BY

```sql
SELECT department, AVG(salary) AS avg_salary
FROM Employees
GROUP BY department
ORDER BY avg_salary DESC;
```

---

## 4. AVG vs Manual Total/Count

```sql
-- Same idea as AVG(salary), written manually
SELECT SUM(salary) / COUNT(salary) FROM Employees;
```

Use `COUNT(salary)` not `COUNT(*)` if you want to match `AVG`’s “ignore nulls” behavior.

### Beginner tip
`AVG` of integers may return a decimal depending on the database. Wrap with `ROUND` when you need a clean display value.

---

## 5. Knowledge Check

1. What does `AVG(score)` compute?
2. Write SQL for average order `amount` in `Orders`.
3. Write SQL for average salary per `city`.
4. Do `NULL` values lower the average as if they were zero?

---

**Previous:** [← SUM()](./04-SUM.md)
**Next:** [COUNT() →](./06-COUNT.md)
