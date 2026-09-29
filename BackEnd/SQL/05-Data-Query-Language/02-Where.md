# 🔍 WHERE

> **Trainer's Note:** `WHERE` filters rows so you get only the records that match your condition — the heart of targeted queries.

---

## 📑 Table of Contents
1. [Filtering with WHERE](#1-filtering-with-where)
2. [Comparison Operators](#2-comparison-operators)
3. [AND, OR, NOT](#3-and-or-not)
4. [NULL Checks](#4-null-checks)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Filtering with WHERE

```sql
SELECT name, age
FROM Students
WHERE age >= 18;
```

Without `WHERE`, every row is returned. With `WHERE`, only rows that make the condition true are kept.

### Real-world analogy
```
WHERE = telling the librarian:
  "From the Students drawer, only folders where Age is 18 or more"
```

---

## 2. Comparison Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `=` | Equal | `age = 21` |
| `!=` or `<>` | Not equal | `status <> 'CLOSED'` |
| `>` `<` `>=` `<=` | Comparisons | `price > 100` |

```sql
SELECT * FROM Products WHERE unit_price < 50;
SELECT * FROM Students WHERE name = 'Amy';
```

---

## 3. AND, OR, NOT

```sql
SELECT * FROM Students
WHERE age >= 18 AND age <= 25;

SELECT * FROM Orders
WHERE status = 'OPEN' OR status = 'PENDING';

SELECT * FROM Employees
WHERE NOT department = 'HR';
```

Use parentheses when mixing `AND`/`OR` so intent is clear:
```sql
WHERE department = 'IT' AND (city = 'Chennai' OR city = 'Bengaluru')
```

---

## 4. NULL Checks

```sql
-- Correct
SELECT * FROM Students WHERE email IS NULL;
SELECT * FROM Students WHERE email IS NOT NULL;

-- Wrong: never matches NULL rows
SELECT * FROM Students WHERE email = NULL;
```

### Beginner tip
`NULL` means "unknown." Unknown is not equal to anything — not even another unknown — so use `IS NULL` / `IS NOT NULL`.

---

## 5. Knowledge Check

1. What does `WHERE` do in a `SELECT`?
2. Write a filter for employees with salary above 50000.
3. Difference between `AND` and `OR`?
4. Why is `WHERE email = NULL` incorrect?

---

**Previous:** [← FROM](./01-From.md)
**Next:** [GROUP BY →](./03-Group-By.md)
