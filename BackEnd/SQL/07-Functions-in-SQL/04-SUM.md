# ➕ SUM()

> **Trainer's Note:** `SUM()` adds numeric values across many rows into one total — perfect for revenue, quantity, and score totals.

---

## 📑 Table of Contents
1. [What SUM Does](#1-what-sum-does)
2. [Basic Examples](#2-basic-examples)
3. [SUM with Expressions](#3-sum-with-expressions)
4. [SUM with GROUP BY and HAVING](#4-sum-with-group-by-and-having)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What SUM Does

```sql
SELECT SUM(salary) AS payroll_total
FROM Employees;
```

Works on **numeric** columns (or numeric expressions). Ignores `NULL`.

### Real-world analogy
```
SUM = adding every amount on a stack of receipts
  to get one grand total at the bottom
```

---

## 2. Basic Examples

```sql
SELECT SUM(qty) FROM OrderItems;
SELECT SUM(credits) FROM Courses WHERE department = 'CS';
```

---

## 3. SUM with Expressions

```sql
SELECT SUM(qty * unit_price) AS revenue
FROM OrderItems;
```

SQL multiplies per row first, then sums the results.

---

## 4. SUM with GROUP BY and HAVING

```sql
SELECT student_id, SUM(qty * unit_price) AS spent
FROM OrderItems
GROUP BY student_id
HAVING SUM(qty * unit_price) > 1000;
```

### Beginner tip
`SUM` of an empty set of rows returns `NULL` in most engines (not `0`). Use `COALESCE(SUM(...), 0)` when you need zero instead.

---

## 5. Knowledge Check

1. What type of column is `SUM` designed for?
2. Write SQL for total `amount` in `Payments`.
3. Write SQL for revenue per `product_id` (`qty * price`).
4. Why might `SUM(col)` return `NULL` instead of `0`?

---

**Previous:** [← MIN()](./03-MIN.md)
**Next:** [AVG() →](./05-AVG.md)
