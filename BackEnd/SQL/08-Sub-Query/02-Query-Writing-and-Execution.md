# ✍️ Query Writing and Execution

> **Trainer's Note:** Writing subqueries well is a process: state the helper question, write the inner SQL, then wrap the outer question around it.

---

## 📑 Table of Contents
1. [A Simple Writing Recipe](#1-a-simple-writing-recipe)
2. [Worked Example](#2-worked-example)
3. [Execution and Validation Tips](#3-execution-and-validation-tips)
4. [Common Errors](#4-common-errors)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. A Simple Writing Recipe

1. **Write the business question in plain English**
2. **Underline the helper question**
3. **Write the helper as its own SELECT** and test it
4. **Write the outer SELECT** using the helper in `WHERE`/`FROM`/...
5. **Run and verify** with a small known dataset

```
Question: Students who scored above the batch average
Helper:   What is the batch average score?
Outer:    Students with score > that average
```

---

## 2. Worked Example

Business need: *List employees earning more than the company average salary.*

```sql
-- Step 1: helper only
SELECT AVG(salary) FROM Employees;

-- Step 2: full query
SELECT employee_id, name, salary
FROM Employees
WHERE salary > (SELECT AVG(salary) FROM Employees)
ORDER BY salary DESC;
```

Another pattern with `IN`:

```sql
-- Students who enrolled in course 101
SELECT name
FROM Students
WHERE student_id IN (
    SELECT student_id
    FROM Enrollments
    WHERE course_id = 101
);
```

---

## 3. Execution and Validation Tips

| Tip | Why |
|-----|-----|
| Run inner query alone first | Confirms helper returns expected shape |
| Check one-row vs many-row result | Decides between `=` and `IN`/`ANY`/`ALL` |
| Test on tiny tables | Easy to verify by eye |
| Compare with JOIN alternative later | Builds confidence and performance awareness |

### Real-world analogy
```
Writing subqueries = solving a word problem
  First compute the intermediate value on scrap paper,
  then use it in the final sentence
```

---

## 4. Common Errors

| Error / symptom | Likely cause |
|-----------------|--------------|
| Single-row subquery returns more than one row | Used `=` but inner query returned multiple rows |
| Empty outer result | Helper condition too strict, or no matching keys |
| Slow query | Correlated subquery over large tables without indexes |
| Wrong business answer | Helper aggregates the wrong population |

### Beginner tip
Alias tables clearly when both inner and outer touch similar tables — it reduces accidental column confusion.

---

## 5. Knowledge Check

1. What is the first thing to write before typing SQL for a subquery problem?
2. Why run the inner query alone?
3. Write SQL: products priced below average product price.
4. Name one common subquery execution error and its cause.

---

**Previous:** [← Working of Sub Query](./01-Working-of-Sub-Query.md)
**Next:** [Single Row Sub Query →](./03-Single-Row-Sub-Query.md)
