# 📌 SELECT

> **Trainer's Note:** `SELECT` is the heart of DQL — it tells the database **which columns or expressions** you want back.

---

## 📑 Table of Contents
1. [What SELECT Does](#1-what-select-does)
2. [Selecting Specific Columns](#2-selecting-specific-columns)
3. [SELECT *](#3-select-)
4. [Expressions and Aliases](#4-expressions-and-aliases)
5. [SELECT DISTINCT](#5-select-distinct)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. What SELECT Does

```sql
SELECT name, age
FROM Students;
```

`SELECT` chooses the **output shape**. It does not change stored data — it only reads.

### Real-world analogy
```
SELECT = choosing which fields to photocopy from each folder
  "Only Name and Age" instead of the entire folder contents
```

---

## 2. Selecting Specific Columns

```sql
SELECT product_name, unit_price FROM Products;
SELECT first_name, last_name, email FROM Employees;
```

List only what you need — clearer results and often better performance than grabbing everything.

---

## 3. SELECT *

```sql
SELECT * FROM Students;
```

Returns **all columns**. Great for exploration while learning; prefer named columns in real applications.

---

## 4. Expressions and Aliases

```sql
SELECT name,
       age,
       age + 1 AS age_next_year
FROM Students;

-- Oracle needs a table even for pure expressions
SELECT 1 + 1 AS two FROM DUAL;
```

`AS` renames the output heading (the table column itself is unchanged).

---

## 5. SELECT DISTINCT

```sql
SELECT DISTINCT city FROM Students;
```

Removes duplicate values from the result list.

### Beginner tip
`SELECT` is only half of the basic query — you still need `FROM` to say which table to read (next lesson).

---

## 6. Knowledge Check

1. What does `SELECT` control in a query?
2. Write a query that returns only `email` from `Users` (include `FROM`).
3. When is `SELECT *` useful, and when should you avoid it?
4. What does `SELECT DISTINCT department FROM Employees` return?

---

**Previous:** [← Working on Oracle 10g](../04-Software-Installation/01-Working-on-Oracle-10g.md)
**Next:** [FROM →](./01-From.md)
