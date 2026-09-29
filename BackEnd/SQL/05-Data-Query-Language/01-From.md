# 📂 FROM

> **Trainer's Note:** `FROM` tells SQL **which table (or tables)** to read. Without it, the database doesn't know where the columns live.

---

## 📑 Table of Contents
1. [What FROM Does](#1-what-from-does)
2. [Single-Table FROM](#2-single-table-from)
3. [Table Aliases](#3-table-aliases)
4. [FROM with DUAL (Oracle)](#4-from-with-dual-oracle)
5. [Looking Ahead](#5-looking-ahead)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. What FROM Does

```sql
SELECT name, age
FROM Students;
```

| Clause | Job |
|--------|-----|
| `SELECT` | What to return |
| `FROM` | Where to get it |

### Real-world analogy
```
FROM = which drawer to open in the filing cabinet
  SELECT chooses the fields; FROM chooses the drawer
```

---

## 2. Single-Table FROM

```sql
SELECT product_name, unit_price
FROM Products;

SELECT * FROM Orders;
```

Table name must exist in your schema (and you need permission to read it).

---

## 3. Table Aliases

Short names make queries easier, especially once joins appear.

```sql
SELECT s.name, s.age
FROM Students s;

SELECT e.first_name, e.salary
FROM Employees e
WHERE e.salary > 50000;
```

`Students s` means: table `Students`, nickname `s`.

---

## 4. FROM with DUAL (Oracle)

Oracle requires a `FROM` clause even for simple expressions:

```sql
SELECT SYSDATE FROM DUAL;
SELECT 10 * 5 AS result FROM DUAL;
```

`DUAL` is a built-in one-row table used as a placeholder source.

---

## 5. Looking Ahead

Later, `FROM` will also include:
- joined tables (`FROM A JOIN B ON ...`)
- subqueries acting as temporary tables  
  `FROM (SELECT ...) t`

For now, master one-table `FROM` first.

### Beginner tip
If you get “invalid table name” / “table or view does not exist,” check spelling, schema, and that you’re connected to the right user/database.

---

## 6. Knowledge Check

1. What does `FROM` specify?
2. Write a query selecting all columns from `Courses`.
3. Why use a table alias like `FROM Employees e`?
4. What is `DUAL` used for in Oracle?

---

**Previous:** [← SELECT](./00-Select.md)
**Next:** [WHERE →](./02-Where.md)
