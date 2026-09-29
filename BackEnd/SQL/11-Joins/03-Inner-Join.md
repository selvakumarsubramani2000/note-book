# 🔗 Inner Join

> **Trainer's Note:** An **INNER JOIN** returns only rows that have a **match in both** tables based on the join condition.

---

## 📑 Table of Contents
1. [What INNER JOIN Returns](#1-what-inner-join-returns)
2. [Basic Syntax](#2-basic-syntax)
3. [Multiple Matches](#3-multiple-matches)
4. [Multi-Table INNER JOIN](#4-multi-table-inner-join)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What INNER JOIN Returns

```
Students                 Orders
id | name                id | student_id | item
1  | Amy                 10 | 1          | Book
2  | Raj                 11 | 1          | Pen
3  | Meera               12 | 2          | Bag

INNER JOIN on student_id => Amy-Book, Amy-Pen, Raj-Bag
Meera has no order => Meera is excluded
```

### Real-world analogy
```
INNER JOIN = only customers who both exist in the customer list
AND have at least one matching order slip
```

---

## 2. Basic Syntax

```sql
SELECT s.name, o.item, o.order_id
FROM Students s
INNER JOIN Orders o
  ON s.student_id = o.student_id;
```

`JOIN` without a keyword usually means `INNER JOIN` in most databases.

---

## 3. Multiple Matches

One student with three orders produces **three** result rows (one per matching pair). That is expected — not a bug.

---

## 4. Multi-Table INNER JOIN

```sql
SELECT s.name, c.course_name, e.grade
FROM Students s
INNER JOIN Enrollments e ON s.student_id = e.student_id
INNER JOIN Courses c ON e.course_id = c.course_id;
```

### Beginner tip
Always write the `ON` condition. Filtering related logic can go in `WHERE`, but the relationship itself belongs in `ON`.

---

## 5. Knowledge Check

1. Does INNER JOIN keep unmatched left-table rows?
2. Write an INNER JOIN between `Employees` and `Departments`.
3. Why can one left row appear many times in the result?
4. What happens to students with zero orders in an INNER JOIN to Orders?

---

**Previous:** [← Cartesian Join](./02-Cartesian-Join.md)
**Next:** [Outer Join →](./04-Outer-Join.md)
