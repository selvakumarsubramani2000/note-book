# 🔗 What Is a Join?

> **Trainer's Note:** A **join** combines rows from two or more tables based on a related column — usually a primary key / foreign key pair.

---

## 📑 Table of Contents
1. [Why Joins Exist](#1-why-joins-exist)
2. [The Basic Idea](#2-the-basic-idea)
3. [JOIN Syntax Skeleton](#3-join-syntax-skeleton)
4. [Join Key Checklist](#4-join-key-checklist)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Why Joins Exist

Relational design stores related data in **separate tables** to avoid duplication. Joins put those pieces back together at query time.

```
Students table has names
Orders table has student_id + item
Join answers: "Who ordered what?"
```

### Real-world analogy
```
Join = matching customer cards to order slips by Customer ID
  so you can print one combined report
```

---

## 2. The Basic Idea

```sql
SELECT s.name, o.item
FROM Students s
JOIN Orders o
  ON s.student_id = o.student_id;
```

For each order row, find the student row with the same `student_id`, and return combined columns.

---

## 3. JOIN Syntax Skeleton

```sql
SELECT ...
FROM table_a a
[INNER | LEFT | RIGHT | FULL] JOIN table_b b
  ON a.key_column = b.key_column
WHERE ...
```

Old Oracle-style comma joins also exist (`FROM a, b WHERE a.id = b.a_id`), but explicit `JOIN ... ON` is clearer for learning.

---

## 4. Join Key Checklist

| Check | Why |
|-------|-----|
| Are tables related by key columns? | Without a match condition you get a cartesian explosion |
| Do datatypes of key columns match? | Mismatched types cause failures or slow implicit conversions |
| Is the relationship 1-N or N-N? | Affects expected row counts |
| Do you need unmatched rows too? | Chooses INNER vs OUTER join |

### Beginner tip
If a join returns way more rows than expected, check whether your `ON` condition is missing or too loose.

---

## 5. Knowledge Check

1. What problem does a join solve?
2. Which columns typically appear in an `ON` clause?
3. Write a join skeleton between `Employees` and `Departments`.
4. What usually happens if you forget the join condition?

---

**Previous:** [← Pseudo Columns Working and Usage](../10-Pseudo-Columns/03-Working-and-Usage.md)
**Next:** [Types of Joins →](./01-Types-of-Joins.md)
