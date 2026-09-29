# 📊 Multi Row Functions

> **Trainer's Note:** **Multi-row functions** (aggregate functions) take many values and return one summary — the syllabus highlights `MAX`, `MIN`, `SUM`, `AVG`, and `COUNT`.

---

## 📑 Table of Contents
1. [What Multi-Row Functions Do](#1-what-multi-row-functions-do)
2. [MAX and MIN](#2-max-and-min)
3. [SUM and AVG](#3-sum-and-avg)
4. [COUNT](#4-count)
5. [With GROUP BY](#5-with-group-by)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. What Multi-Row Functions Do

```sql
SELECT
    COUNT(*) AS total_students,
    MAX(age) AS oldest,
    MIN(age) AS youngest,
    SUM(age) AS age_sum,
    AVG(age) AS age_avg
FROM Students;
```

One result row summarizing the whole table (unless `GROUP BY` creates multiple groups).

### Real-world analogy
```
Multi-row functions = summary statistics on a class list
  How many students? Oldest? Youngest? Average age?
```

---

## 2. MAX and MIN

```sql
SELECT MAX(salary) FROM Employees;
SELECT MIN(order_date) FROM Orders;
```

Works with numbers, dates, and (lexicographically) strings.

---

## 3. SUM and AVG

```sql
SELECT SUM(unit_price * qty) AS revenue FROM OrderItems;
SELECT AVG(salary) FROM Employees WHERE department = 'IT';
```

`AVG` ignores `NULL`s and returns the mean of remaining values.

---

## 4. COUNT

```sql
SELECT COUNT(*) FROM Students;            -- every row
SELECT COUNT(email) FROM Students;        -- non-NULL emails only
SELECT COUNT(DISTINCT city) FROM Students; -- unique cities
```

| Form | Counts |
|------|--------|
| `COUNT(*)` | Rows |
| `COUNT(col)` | Non-null values in `col` |
| `COUNT(DISTINCT col)` | Unique non-null values |

---

## 5. With GROUP BY

```sql
SELECT department,
       COUNT(*) AS headcount,
       AVG(salary) AS avg_salary,
       MAX(salary) AS top_salary
FROM Employees
GROUP BY department;
```

### Beginner tip
`NULL` values are ignored by most aggregates (`COUNT(*)` is the common exception because it counts rows, not column values).

---

## 6. Knowledge Check

1. List the five multi-row functions from this syllabus topic.
2. Difference between `COUNT(*)` and `COUNT(email)`?
3. Write a query for average price in `Products`.
4. Write a query for highest and lowest salary per department.

---

**Previous:** [← Single Row Functions](./00-Single-Row-Functions.md)
**Next:** [MAX() →](./02-MAX.md)
