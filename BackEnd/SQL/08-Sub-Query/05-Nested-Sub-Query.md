# 🧱 Nested Sub Query

> **Trainer's Note:** A **nested subquery** means a subquery inside another subquery — multiple levels of helper questions.

---

## 📑 Table of Contents
1. [What Nesting Means](#1-what-nesting-means)
2. [Worked Example](#2-worked-example)
3. [How to Read Nested SQL](#3-how-to-read-nested-sql)
4. [When Nesting Gets Too Deep](#4-when-nesting-gets-too-deep)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What Nesting Means

```sql
SELECT name
FROM Employees
WHERE department_id = (
    SELECT department_id
    FROM Departments
    WHERE location_id = (
        SELECT location_id
        FROM Locations
        WHERE city = 'Chennai'
    )
);
```

Three layers:
1. Innermost: city → `location_id`
2. Middle: `location_id` → `department_id`
3. Outer: `department_id` → employee names

### Real-world analogy
```
Nested subquery = chained questions
  "Which city code is Chennai?"
  "Which department sits in that location?"
  "Which employees belong to that department?"
```

---

## 2. Worked Example

Business question: *Students enrolled in any course taught by instructor `'Dr. Rao'`.*

```sql
SELECT name
FROM Students
WHERE student_id IN (
    SELECT student_id
    FROM Enrollments
    WHERE course_id IN (
        SELECT course_id
        FROM Courses
        WHERE instructor = 'Dr. Rao'
    )
);
```

---

## 3. How to Read Nested SQL

Always evaluate **inside-out**:
1. Run the deepest `( ... )`
2. Use its result in the parent subquery
3. Use that result in the outermost query

Test each level alone when debugging.

---

## 4. When Nesting Gets Too Deep

| Symptom | Better approach later |
|---------|------------------------|
| Hard to read 3–4 levels | JOINs or CTEs (`WITH`) |
| Repeated same subquery | CTE reused twice |
| Correlated + nested mix | Simplify step by step |

### Beginner tip
Nesting is fine for learning and small queries. In production code, clarity often wins — same logic as joins/CTEs is OK if it’s easier to maintain.

---

## 5. Knowledge Check

1. What makes a subquery “nested”?
2. In what order should you evaluate nested subqueries?
3. Write a 2-level nested query idea in plain English (your own domain).
4. Name one alternative when nesting becomes unreadable.

---

**Previous:** [← Multi Row Sub Query](./04-Multi-Row-Sub-Query.md)
**Next:** [Introduction on Pseudo Columns →](../10-Pseudo-Columns/00-Introduction-on-Pseudo-Columns.md)
