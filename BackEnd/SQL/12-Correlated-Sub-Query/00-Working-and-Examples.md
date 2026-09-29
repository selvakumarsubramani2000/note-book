# 🔄 Correlated Sub Query — Working and Examples

> **Trainer's Note:** A **correlated subquery** references columns from the outer query. It is evaluated **once per outer row** (conceptually), not once for the whole statement.

---

## 📑 Table of Contents
1. [How Correlation Works](#1-how-correlation-works)
2. [Classic Salary vs Department Average](#2-classic-salary-vs-department-average)
3. [EXISTS Pattern](#3-exists-pattern)
4. [NOT EXISTS Pattern](#4-not-exists-pattern)
5. [Performance Notes](#5-performance-notes)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. How Correlation Works

```sql
SELECT e.name, e.salary, e.department
FROM Employees e
WHERE e.salary > (
    SELECT AVG(salary)
    FROM Employees
    WHERE department = e.department   -- outer reference
);
```

For each outer employee `e`, the inner query recalculates that employee’s department average.

### Real-world analogy
```
Normal subquery   = one school-wide average, reused for everyone
Correlated subquery = for each student, compute THAT class's average, then compare
```

---

## 2. Classic Salary vs Department Average

```sql
SELECT e.name, e.department, e.salary
FROM Employees e
WHERE e.salary > (
    SELECT AVG(x.salary)
    FROM Employees x
    WHERE x.department = e.department
)
ORDER BY e.department, e.salary DESC;
```

---

## 3. EXISTS Pattern

```sql
-- Students who have at least one paid order
SELECT s.name
FROM Students s
WHERE EXISTS (
    SELECT 1
    FROM Orders o
    WHERE o.student_id = s.student_id
      AND o.status = 'PAID'
);
```

`EXISTS` stops when it finds the first matching inner row — often efficient with indexes.

---

## 4. NOT EXISTS Pattern

```sql
-- Students with no orders
SELECT s.name
FROM Students s
WHERE NOT EXISTS (
    SELECT 1 FROM Orders o WHERE o.student_id = s.student_id
);
```

This is often safer than `NOT IN` when nulls may appear.

---

## 5. Performance Notes

| Point | Guidance |
|-------|----------|
| Can be slower on huge tables | Inner work repeats per outer row |
| Indexes help | Index join/filter columns used in correlation |
| Alternatives | Often rewritable as JOIN + GROUP BY |
| Still valuable | Clear for “exists / not exists” business rules |

### Beginner tip
If a correlated subquery is slow, try expressing the same question as a join and compare results + runtime.

---

## 6. Knowledge Check

1. What makes a subquery correlated?
2. Write a correlated query: products priced above their category average.
3. Write `EXISTS` for customers who placed an order in 2026.
4. Why is `NOT EXISTS` often preferred over `NOT IN`?

---

**Previous:** [← Joins Queries and Examples](../11-Joins/06-Queries-and-Examples.md)
**Next:** [DDL CREATE →](../13-DDL/00-Create.md)
