# 📋 Multi Row Sub Query

> **Trainer's Note:** A **multi-row subquery** returns **multiple rows**. Compare using `IN`, `ANY`, `ALL`, or `EXISTS` — not bare `=`.

---

## 📑 Table of Contents
1. [Definition](#1-definition)
2. [IN and NOT IN](#2-in-and-not-in)
3. [ANY and ALL](#3-any-and-all)
4. [EXISTS](#4-exists)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Definition

```sql
SELECT name
FROM Students
WHERE student_id IN (SELECT student_id FROM Orders);
```

Inner query returns a **set of values**; outer query tests membership/comparison against that set.

### Real-world analogy
```
Multi-row subquery = asking for a whole guest list first
  then checking who from the city is on that list
```

---

## 2. IN and NOT IN

```sql
-- Students who placed at least one order
SELECT name FROM Students
WHERE student_id IN (SELECT student_id FROM Orders);

-- Students with no orders
SELECT name FROM Students
WHERE student_id NOT IN (
    SELECT student_id FROM Orders WHERE student_id IS NOT NULL
);
```

### Beginner tip
`NOT IN` with `NULL` inside the list can surprise you (whole condition becomes unknown). Filter nulls out of the subquery when using `NOT IN`.

---

## 3. ANY and ALL

```sql
-- Salary greater than at least one Sales salary
SELECT name, salary FROM Employees
WHERE salary > ANY (
    SELECT salary FROM Employees WHERE department = 'Sales'
);

-- Salary greater than every Sales salary
SELECT name, salary FROM Employees
WHERE salary > ALL (
    SELECT salary FROM Employees WHERE department = 'Sales'
);
```

| Operator | Meaning |
|----------|---------|
| `= ANY` | Same idea as `IN` |
| `> ANY` | Greater than at least one (greater than the smallest) |
| `> ALL` | Greater than every value (greater than the largest) |

---

## 4. EXISTS

```sql
SELECT s.name
FROM Students s
WHERE EXISTS (
    SELECT 1 FROM Orders o WHERE o.student_id = s.student_id
);
```

`EXISTS` is true if the subquery finds **any** matching row (often used for correlated checks).

---

## 5. Knowledge Check

1. Why can't you use plain `=` with a multi-row subquery?
2. Write SQL: employees in departments located in `'Chennai'` (via a subquery list of `department_id`).
3. Explain `> ALL` in plain English.
4. When is `EXISTS` a good choice?

---

**Previous:** [← Single Row Sub Query](./03-Single-Row-Sub-Query.md)
**Next:** [Nested Sub Query →](./05-Nested-Sub-Query.md)
