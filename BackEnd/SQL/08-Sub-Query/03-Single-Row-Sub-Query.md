# 1️⃣ Single Row Sub Query

> **Trainer's Note:** A **single-row subquery** returns exactly **one row and one column** — a single value you can compare with `=`, `>`, `<`, `>=`, or `<=`.

---

## 📑 Table of Contents
1. [Definition](#1-definition)
2. [Basic Examples](#2-basic-examples)
3. [Common Operators](#3-common-operators)
4. [What Goes Wrong](#4-what-goes-wrong)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Definition

```sql
SELECT name, salary
FROM Employees
WHERE salary = (SELECT MAX(salary) FROM Employees);
```

The inner query must produce **one scalar value**.

### Real-world analogy
```
Single-row subquery = asking for one number first
  "What is the highest salary?" → then "Who earns exactly that?"
```

---

## 2. Basic Examples

```sql
-- Older than average age
SELECT name, age FROM Students
WHERE age > (SELECT AVG(age) FROM Students);

-- Products at the lowest price
SELECT * FROM Products
WHERE unit_price = (SELECT MIN(unit_price) FROM Products);

-- Hired on the earliest hire date
SELECT name FROM Employees
WHERE hire_date = (SELECT MIN(hire_date) FROM Employees);
```

---

## 3. Common Operators

| Operator | Use with single-row result |
|----------|----------------------------|
| `=` | Equal to the value |
| `>` `<` `>=` `<=` | Compare to the value |
| `<>` / `!=` | Not equal to the value |

```sql
SELECT name FROM Employees
WHERE department_id = (
    SELECT department_id FROM Departments WHERE dept_name = 'Sales'
);
```

(This works only if `'Sales'` matches **one** department row.)

---

## 4. What Goes Wrong

| Problem | Result |
|---------|--------|
| Inner query returns **many rows** | Error: single-row subquery returns more than one row |
| Inner query returns **zero rows** | Comparison becomes unknown → outer rows filtered out (`=`) |
| Used `=` where a list was needed | Should use multi-row form with `IN` |

### Beginner tip
If your helper question naturally returns a **list** (many IDs), use a multi-row subquery — not a single-row one.

---

## 5. Knowledge Check

1. How many rows and columns should a single-row subquery return?
2. Write SQL: students whose age equals the maximum age.
3. Which operators are safe with a single-row subquery?
4. What error appears if the subquery returns multiple salaries?

---

**Previous:** [← Query Writing and Execution](./02-Query-Writing-and-Execution.md)
**Next:** [Multi Row Sub Query →](./04-Multi-Row-Sub-Query.md)
