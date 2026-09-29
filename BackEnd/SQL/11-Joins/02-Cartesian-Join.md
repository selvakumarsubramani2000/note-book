# ⊗ Cartesian Join (CROSS JOIN)

> **Trainer's Note:** A **Cartesian join** pairs every row of one table with every row of another. It is powerful for generating combinations — and dangerous when accidental.

---

## 📑 Table of Contents
1. [What Is a Cartesian Join?](#1-what-is-a-cartesian-join)
2. [Syntax](#2-syntax)
3. [When It Is Useful](#3-when-it-is-useful)
4. [Accidental Cartesian Products](#4-accidental-cartesian-products)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What Is a Cartesian Join?

If table A has 3 rows and table B has 4 rows, a Cartesian join returns **3 × 4 = 12** rows.

### Real-world analogy
```
Cartesian join = every shirt color with every size
  Red-S, Red-M, Red-L, Blue-S, Blue-M, Blue-L, ...
```

---

## 2. Syntax

```sql
-- Explicit
SELECT c.color_name, s.size_code
FROM Colors c
CROSS JOIN Sizes s;

-- Older style (comma join without a real join condition)
SELECT c.color_name, s.size_code
FROM Colors c, Sizes s;
```

---

## 3. When It Is Useful

| Use case | Example |
|----------|---------|
| Generate all combinations | colors × sizes, days × rooms |
| Build a calendar/grid scaffold | dates × employees |
| Test data generation | simple combinatorial sets |

```sql
SELECT d.day_name, r.room_name
FROM Days d
CROSS JOIN Rooms r;
```

---

## 4. Accidental Cartesian Products

```sql
-- Dangerous: forgot the join condition
SELECT s.name, o.item
FROM Students s, Orders o;
```

If Students has 1,000 rows and Orders has 10,000 rows, you get **10,000,000** rows.

### Beginner tip
If a join suddenly returns a huge row count, check for a missing `ON` / `WHERE` relationship condition.

---

## 5. Knowledge Check

1. How many rows do 5 × 6 tables produce with a Cartesian join?
2. Write a `CROSS JOIN` between `Products` and `Warehouses`.
3. Why is an accidental Cartesian product risky?
4. Name one legitimate use of a Cartesian join.

---

**Previous:** [← Types of Joins](./01-Types-of-Joins.md)
**Next:** [Inner Join →](./03-Inner-Join.md)
