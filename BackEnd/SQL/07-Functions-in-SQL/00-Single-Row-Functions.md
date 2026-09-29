# 🔤 Single Row Functions

> **Trainer's Note:** A **single-row function** returns one result **per input row** — formatting text, rounding numbers, working with dates — without collapsing the result set.

---

## 📑 Table of Contents
1. [Single-Row vs Multi-Row](#1-single-row-vs-multi-row)
2. [Character Functions](#2-character-functions)
3. [Numeric Functions](#3-numeric-functions)
4. [Date Functions](#4-date-functions)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Single-Row vs Multi-Row

| | Single-row | Multi-row (aggregate) |
|---|------------|------------------------|
| Input | One row | Many rows |
| Output | One value per row | One value per group/table |
| Examples | `UPPER`, `ROUND`, `LENGTH` | `MAX`, `SUM`, `COUNT` |

### Real-world analogy
```
Single-row = stamp each envelope individually
Multi-row  = weigh the whole bundle once and write one total weight
```

---

## 2. Character Functions

```sql
SELECT UPPER(name) FROM Students;           -- AMY
SELECT LOWER(name) FROM Students;           -- amy
SELECT LENGTH(name) FROM Students;          -- character count
SELECT SUBSTR(name, 1, 3) FROM Students;    -- first 3 chars (Oracle-style)
SELECT TRIM('  hi  ') FROM DUAL;            -- 'hi'
```

---

## 3. Numeric Functions

```sql
SELECT ROUND(19.567, 2) FROM DUAL;   -- 19.57
SELECT TRUNC(19.567, 2) FROM DUAL;   -- 19.56 (Oracle TRUNC)
SELECT ABS(-15) FROM DUAL;           -- 15
SELECT MOD(10, 3) FROM DUAL;         -- 1
```

---

## 4. Date Functions

```sql
SELECT SYSDATE FROM DUAL;                 -- Oracle current date/time
-- SELECT NOW();                          -- MySQL
-- SELECT GETDATE();                      -- SQL Server

SELECT order_date + 7 FROM Orders;        -- Oracle date arithmetic style
```

### Beginner tip
Function names differ across products (`SUBSTR` vs `SUBSTRING`, `SYSDATE` vs `NOW`). Learn the concept once, then check your engine's reference for exact names.

---

## 5. Knowledge Check

1. Does `UPPER(name)` reduce the number of result rows?
2. Name two character single-row functions.
3. What does `ROUND(12.345, 2)` return?
4. Why might the same date function have different names in Oracle vs MySQL?

---

**Previous:** [← Operators](../06-Operators/00-Operators-Types-and-Examples.md)
**Next:** [Multi Row Functions →](./01-Multi-Row-Functions.md)
