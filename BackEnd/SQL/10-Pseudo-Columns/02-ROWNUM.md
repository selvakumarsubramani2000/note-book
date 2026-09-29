# 🔢 ROWNUM

> **Trainer's Note:** `ROWNUM` assigns a temporary sequence number to rows **as Oracle retrieves them**. It is commonly used for Top-N queries in older Oracle SQL.

---

## 📑 Table of Contents
1. [What ROWNUM Does](#1-what-rownum-does)
2. [Basic Filter](#2-basic-filter)
3. [The ORDER BY Trap](#3-the-order-by-trap)
4. [Correct Top-N Pattern](#4-correct-top-n-pattern)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What ROWNUM Does

```sql
SELECT ROWNUM, name, age
FROM Students;
```

`ROWNUM` starts at 1 and increases for each row returned in that query execution. It is **not** a stored column.

### Real-world analogy
```
ROWNUM = numbering people as they walk through a doorway
  1st person through gets 1, 2nd gets 2...
  Re-run the line differently, numbers can be assigned in a different walk order
```

---

## 2. Basic Filter

```sql
-- First five rows Oracle happens to return
SELECT * FROM Students WHERE ROWNUM <= 5;
```

Important: `WHERE ROWNUM = 1` can work for one row.  
`WHERE ROWNUM > 1` does **not** work as beginners expect, because row numbers are assigned as rows qualify.

---

## 3. The ORDER BY Trap

```sql
-- Often NOT the "top 5 oldest" students
SELECT * FROM Students
WHERE ROWNUM <= 5
ORDER BY age DESC;
```

`ROWNUM` is assigned **before** `ORDER BY` is applied in this pattern, so you may sort only an arbitrary first five rows.

---

## 4. Correct Top-N Pattern

Sort first in an inner query, then apply `ROWNUM` outside:

```sql
SELECT *
FROM (
    SELECT name, age
    FROM Students
    ORDER BY age DESC
)
WHERE ROWNUM <= 5;
```

Modern Oracle also supports `FETCH FIRST n ROWS ONLY`; many other databases use `LIMIT`/`TOP`. For this syllabus, master the classic `ROWNUM` pattern.

### Beginner tip
Whenever Top-N needs a specific order, remember: **sort in a subquery, then cut with `ROWNUM`**.

---

## 5. Knowledge Check

1. Is `ROWNUM` stored in the table permanently?
2. Why is `WHERE ROWNUM <= 5 ORDER BY age DESC` unreliable for "5 oldest"?
3. Write a correct Top-3 highest salaries query using a subquery + `ROWNUM`.
4. Name one modern alternative to `ROWNUM` Top-N syntax.

---

**Previous:** [← ROWID](./01-ROWID.md)
**Next:** [Working and Usage →](./03-Working-and-Usage.md)
