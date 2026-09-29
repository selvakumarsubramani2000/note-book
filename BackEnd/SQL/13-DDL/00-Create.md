# 🏗️ DDL — CREATE

> **Trainer's Note:** `CREATE` builds new database objects — most often tables, but also indexes, views, and more.

---

## 📑 Table of Contents
1. [CREATE TABLE](#1-create-table)
2. [CREATE with Constraints](#2-create-with-constraints)
3. [Other CREATE Objects](#3-other-create-objects)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. CREATE TABLE

```sql
CREATE TABLE Students (
    student_id INT,
    name       VARCHAR(50),
    email      VARCHAR(100),
    age        INT,
    joined_on  DATE
);
```

### Real-world analogy
```
CREATE TABLE = building a new labeled drawer
  and deciding what fields each folder inside will have
```

---

## 2. CREATE with Constraints

```sql
CREATE TABLE Students (
    student_id INT PRIMARY KEY,
    name       VARCHAR(50) NOT NULL,
    email      VARCHAR(100) UNIQUE,
    age        INT CHECK (age >= 0),
    dept_id    INT,
    CONSTRAINT fk_students_dept
        FOREIGN KEY (dept_id) REFERENCES Departments(dept_id)
);
```

---

## 3. Other CREATE Objects

```sql
CREATE INDEX idx_students_email ON Students(email);

CREATE VIEW vw_adult_students AS
SELECT student_id, name, age
FROM Students
WHERE age >= 18;
```

Exact object types depend on your RDBMS.

### Beginner tip
Design columns and constraints carefully up front — changing structure later is possible (`ALTER`) but messier once real data exists.

---

## 4. Knowledge Check

1. What does `CREATE TABLE` define?
2. Write a `CREATE TABLE` for `Courses(course_id, title, credits)`.
3. Add a primary key and `NOT NULL` title to that table definition.
4. Name two non-table objects you can also `CREATE`.

---

**Previous:** [← Correlated Sub Query](../12-Correlated-Sub-Query/00-Working-and-Examples.md)
**Next:** [RENAME →](./01-Rename.md)
