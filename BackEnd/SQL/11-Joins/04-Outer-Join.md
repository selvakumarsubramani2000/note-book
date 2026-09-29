# 🌅 Outer Join

> **Trainer's Note:** An **OUTER JOIN** keeps rows even when the other table has **no match**, filling missing side with `NULL`s.

---

## 📑 Table of Contents
1. [LEFT OUTER JOIN](#1-left-outer-join)
2. [RIGHT OUTER JOIN](#2-right-outer-join)
3. [FULL OUTER JOIN](#3-full-outer-join)
4. [Finding Non-Matches](#4-finding-non-matches)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. LEFT OUTER JOIN

Keeps **all rows from the left** table; attaches matching right rows when available.

```sql
SELECT s.name, o.item
FROM Students s
LEFT OUTER JOIN Orders o
  ON s.student_id = o.student_id;
```

Students without orders still appear; `o.item` is `NULL`.

`LEFT JOIN` is short for `LEFT OUTER JOIN`.

### Real-world analogy
```
LEFT JOIN = full guest list + gift info if they brought a gift
  Guests who brought nothing still stay on the list
```

---

## 2. RIGHT OUTER JOIN

Keeps **all rows from the right** table.

```sql
SELECT s.name, o.item
FROM Students s
RIGHT OUTER JOIN Orders o
  ON s.student_id = o.student_id;
```

Many teams prefer rewriting right joins as left joins by swapping table order for consistency.

---

## 3. FULL OUTER JOIN

Keeps rows when either side matches (unmatched sides get `NULL`). Support varies by product (Oracle/PostgreSQL yes; MySQL traditionally needs a UNION pattern).

```sql
SELECT *
FROM A
FULL OUTER JOIN B ON A.id = B.a_id;
```

---

## 4. Finding Non-Matches

```sql
-- Students with no orders
SELECT s.name
FROM Students s
LEFT JOIN Orders o ON s.student_id = o.student_id
WHERE o.order_id IS NULL;
```

### Beginner tip
`ON` defines the match. Putting the match condition only in `WHERE` with an outer join can accidentally turn it into an inner join.

---

## 5. Knowledge Check

1. What does LEFT JOIN keep that INNER JOIN drops?
2. Write a LEFT JOIN listing all departments and their employees (if any).
3. How do you find left rows with no match?
4. Difference between LEFT and FULL outer join?

---

**Previous:** [← Inner Join](./03-Inner-Join.md)
**Next:** [Self-Join →](./05-Self-Join.md)
