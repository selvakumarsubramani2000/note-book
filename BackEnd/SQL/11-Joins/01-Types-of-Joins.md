# 🔀 Types of Joins

> **Trainer's Note:** The main join types are **INNER**, **LEFT OUTER**, **RIGHT OUTER**, **FULL OUTER**, plus **CROSS** and **SELF** joins as special cases.

---

## 📑 Table of Contents
1. [INNER JOIN](#1-inner-join)
2. [LEFT / RIGHT OUTER JOIN](#2-left--right-outer-join)
3. [FULL OUTER JOIN](#3-full-outer-join)
4. [CROSS JOIN and SELF JOIN](#4-cross-join-and-self-join)
5. [Choosing a Join Type](#5-choosing-a-join-type)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. INNER JOIN

Returns only rows with a match in **both** tables.

```sql
SELECT s.name, o.item
FROM Students s
INNER JOIN Orders o ON s.student_id = o.student_id;
```

Students with no orders disappear from this result. Orders with invalid/missing students also disappear.

---

## 2. LEFT / RIGHT OUTER JOIN

**LEFT JOIN** keeps all rows from the left table, and matching right rows (or `NULL`s if no match).

```sql
SELECT s.name, o.item
FROM Students s
LEFT JOIN Orders o ON s.student_id = o.student_id;
```

Students without orders still appear; `o.item` is `NULL` for them.

**RIGHT JOIN** is the mirror image (keeps all right-table rows). Many teams write everything as LEFT joins by swapping table order for readability.

---

## 3. FULL OUTER JOIN

Keeps rows when there is a match in either table (unmatched sides padded with `NULL`). Support varies by product.

```sql
SELECT *
FROM A
FULL OUTER JOIN B ON A.id = B.a_id;
```

---

## 4. CROSS JOIN and SELF JOIN

**CROSS JOIN** — every row of A paired with every row of B (cartesian product).

```sql
SELECT * FROM Colors CROSS JOIN Sizes;
```

**SELF JOIN** — a table joined to itself (useful for employee/manager hierarchies).

```sql
SELECT e.name AS employee, m.name AS manager
FROM Employees e
LEFT JOIN Employees m ON e.manager_id = m.employee_id;
```

### Real-world analogy
```
INNER = only people who both RSVP'd AND showed up
LEFT  = all invited people, with show-up info if available
CROSS = every shirt color with every size
SELF  = matching staff list to itself to find each person's manager
```

---

## 5. Choosing a Join Type

| Goal | Use |
|------|-----|
| Only matched pairs | `INNER JOIN` |
| All customers + orders if any | `LEFT JOIN` customers to orders |
| All combinations | `CROSS JOIN` (rarely in OLTP) |
| Hierarchy in one table | `SELF JOIN` |

### Beginner tip
Start every problem by asking: "Must unmatched left rows still appear?" If yes, you need an outer join, not inner.

---

## 6. Knowledge Check

1. What rows does `INNER JOIN` exclude?
2. Write a `LEFT JOIN` that lists all students and their orders (if any).
3. When do you need a self join?
4. Why is an accidental cross join dangerous on large tables?

---

**Previous:** [← What Is Join?](./00-What-Is-Join.md)
**Next:** [Cartesian Join →](./02-Cartesian-Join.md)
