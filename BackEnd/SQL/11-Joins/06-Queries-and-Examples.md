# 🧪 Joins — Queries and Examples

> **Trainer's Note:** Practice patterns you will reuse constantly: customer+orders, filter after join, outer join “missing rows,” and self-join hierarchy.

---

## 📑 Table of Contents
1. [Sample Tables](#1-sample-tables)
2. [Example Pack](#2-example-pack)
3. [Common Mistakes](#3-common-mistakes)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. Sample Tables

```sql
-- Students(student_id, name, city)
-- Orders(order_id, student_id, item, amount)
-- Employees(employee_id, name, manager_id, department_id)
-- Departments(department_id, dept_name)
```

---

## 2. Example Pack

**A. Inner join with filter**
```sql
SELECT s.name, o.item, o.amount
FROM Students s
INNER JOIN Orders o ON s.student_id = o.student_id
WHERE o.amount >= 500
ORDER BY o.amount DESC;
```

**B. Left join — all students and order counts**
```sql
SELECT s.name, COUNT(o.order_id) AS order_count
FROM Students s
LEFT JOIN Orders o ON s.student_id = o.student_id
GROUP BY s.name
ORDER BY order_count DESC;
```

**C. Students with no orders**
```sql
SELECT s.name
FROM Students s
LEFT JOIN Orders o ON s.student_id = o.student_id
WHERE o.order_id IS NULL;
```

**D. Employees with department names**
```sql
SELECT e.name, d.dept_name
FROM Employees e
INNER JOIN Departments d ON e.department_id = d.department_id;
```

**E. Self-join managers**
```sql
SELECT e.name AS employee, m.name AS manager
FROM Employees e
LEFT JOIN Employees m ON e.manager_id = m.employee_id;
```

**F. Cartesian for size/color matrix**
```sql
SELECT c.color_name, z.size_code
FROM Colors c
CROSS JOIN Sizes z;
```

### Real-world analogy
```
These examples are like standard report requests:
  who bought what, who bought nothing, who reports to whom
```

---

## 3. Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing join condition | Add proper `ON` |
| Using `WHERE` right-column IS NULL incorrectly on INNER JOIN | Use LEFT JOIN first |
| Selecting huge `SELECT *` multi-joins | Pick needed columns |
| Forgetting aliases on self-join | Alias both sides clearly |

---

## 4. Knowledge Check

1. Write a join that lists department name with employee count.
2. Write a query for products never ordered (`Products` left join `OrderItems`).
3. Write a self-join for employee/manager.
4. Which join type builds all color/size pairs?

---

**Previous:** [← Self-Join](./05-Self-Join.md)
**Next:** [Correlated Sub Query — Working and Examples →](../12-Correlated-Sub-Query/00-Working-and-Examples.md)
