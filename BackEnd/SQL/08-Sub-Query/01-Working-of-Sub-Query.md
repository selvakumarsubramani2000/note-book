# ⚙️ Working of Sub Query

> **Trainer's Note:** Understanding **execution order** prevents confusion. Most non-correlated subqueries run once and hand their result to the outer query.

---

## 📑 Table of Contents
1. [Inside-Out Execution](#1-inside-out-execution)
2. [Independent vs Correlated](#2-independent-vs-correlated)
3. [Scalar Result Example Walkthrough](#3-scalar-result-example-walkthrough)
4. [List Result Example Walkthrough](#4-list-result-example-walkthrough)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Inside-Out Execution

For a normal (non-correlated) subquery:

```
1) Run innermost query
2) Get its result (one value or a set of values)
3) Plug that result into the outer query
4) Run the outer query
```

```sql
SELECT name
FROM Employees
WHERE salary > (SELECT AVG(salary) FROM Employees);
```

Step A: average salary computed once (example: `65000`).  
Step B: outer query becomes conceptually `WHERE salary > 65000`.

---

## 2. Independent vs Correlated

| Type | Behavior |
|------|----------|
| **Independent / nested normal** | Inner query does not need outer row values; usually runs once |
| **Correlated** | Inner query references outer row columns; conceptually re-runs per outer row |

```sql
-- Correlated: compares each employee to their own department average
SELECT e.name, e.salary, e.department
FROM Employees e
WHERE e.salary > (
    SELECT AVG(salary)
    FROM Employees
    WHERE department = e.department
);
```

### Real-world analogy
```
Independent = ask once for the school-wide average, reuse it
Correlated  = for each student, ask the average of THAT student's class
```

---

## 3. Scalar Result Example Walkthrough

```sql
SELECT * FROM Products
WHERE price = (SELECT MAX(price) FROM Products);
```

1. Inner finds maximum price  
2. Outer returns product(s) matching that price

---

## 4. List Result Example Walkthrough

```sql
SELECT name FROM Students
WHERE student_id IN (SELECT student_id FROM Orders);
```

1. Inner collects all `student_id`s that appear in orders  
2. Outer returns student names whose IDs are in that list

### Beginner tip
If a subquery should return one value but returns many, single-row operators like `=` will error. That leads into single-row vs multi-row types next.

---

## 5. Knowledge Check

1. In what order do you mentally evaluate a normal nested query?
2. What makes a subquery correlated?
3. Walk through `WHERE id IN (SELECT ...) ` in two steps.
4. Why might a correlated subquery be slower on large tables?

---

**Previous:** [← Introduction to Sub Query](./00-Introduction-to-Sub-Query.md)
**Next:** [Query Writing and Execution →](./02-Query-Writing-and-Execution.md)
