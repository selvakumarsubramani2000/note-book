# 📉 MIN()

> **Trainer's Note:** `MIN()` is the mirror of `MAX()` — it returns the **smallest** value in a column.

---

## 📑 Table of Contents
1. [What MIN Does](#1-what-min-does)
2. [Basic Examples](#2-basic-examples)
3. [MIN with GROUP BY](#3-min-with-group-by)
4. [MIN with Dates and Text](#4-min-with-dates-and-text)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What MIN Does

```sql
SELECT MIN(salary) AS lowest_salary
FROM Employees;
```

### Real-world analogy
```
MIN = scanning all price tags in a shop aisle
  and writing down only the cheapest one
```

---

## 2. Basic Examples

```sql
SELECT MIN(age) FROM Students;
SELECT MIN(unit_price) FROM Products;
SELECT MIN(score) FROM ExamResults WHERE exam_id = 10;
```

`NULL`s are skipped.

---

## 3. MIN with GROUP BY

```sql
SELECT department, MIN(salary) AS entry_salary
FROM Employees
GROUP BY department;
```

---

## 4. MIN with Dates and Text

```sql
SELECT MIN(order_date) AS first_order FROM Orders;   -- earliest date
SELECT MIN(name) FROM Students;                      -- first alphabetically
```

### Beginner tip
For “oldest person,” people sometimes confuse `MIN(age)` with `MAX(birth_date)`. Think about what “smallest” means for that column’s meaning.

---

## 5. Knowledge Check

1. What does `MIN(unit_price)` tell you?
2. Write SQL for the earliest hire date in `Employees`.
3. Write SQL for minimum score per `course_id`.
4. Does `MIN` count `NULL` as the smallest value?

---

**Previous:** [← MAX()](./02-MAX.md)
**Next:** [SUM() →](./04-SUM.md)
