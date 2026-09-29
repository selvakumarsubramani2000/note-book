# 🪞 Self-Join

> **Trainer's Note:** A **self-join** joins a table to **itself** — essential for hierarchies like employee → manager or category → parent category.

---

## 📑 Table of Contents
1. [Why Self-Join?](#1-why-self-join)
2. [Employee–Manager Example](#2-employee–manager-example)
3. [Pair Comparisons Inside One Table](#3-pair-comparisons-inside-one-table)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. Why Self-Join?

When related values live in the **same** table, you need two nicknames for that table in one query.

### Real-world analogy
```
Self-join = one company directory used twice
  Copy A = employee names
  Copy B = manager names
  Match employee.manager_id to manager.employee_id
```

---

## 2. Employee–Manager Example

```sql
SELECT
    e.name AS employee_name,
    m.name AS manager_name
FROM Employees e
LEFT JOIN Employees m
  ON e.manager_id = m.employee_id
ORDER BY e.name;
```

`LEFT JOIN` keeps employees who have no manager (e.g., CEO).

```sql
-- Only people who have a manager
SELECT e.name AS employee_name, m.name AS manager_name
FROM Employees e
INNER JOIN Employees m ON e.manager_id = m.employee_id;
```

---

## 3. Pair Comparisons Inside One Table

```sql
-- Pairs of students in the same city (each pair once)
SELECT a.name AS student_a, b.name AS student_b, a.city
FROM Students a
INNER JOIN Students b
  ON a.city = b.city
 AND a.student_id < b.student_id;
```

The `a.student_id < b.student_id` condition avoids duplicate reverse pairs and self-pairing.

### Beginner tip
Always give **clear aliases** (`e`/`m`, `a`/`b`). Without aliases, a self-join is nearly unreadable.

---

## 4. Knowledge Check

1. What does a self-join mean?
2. Write a self-join that shows each employee with their manager’s name.
3. Why are table aliases required in a self-join?
4. Give one non-hierarchy self-join example (your own idea).

---

**Previous:** [← Outer Join](./04-Outer-Join.md)
**Next:** [Queries and Examples →](./06-Queries-and-Examples.md)
