# 🧰 How to Use Constraints

> **Trainer's Note:** Constraints are added at table creation time, or later with `ALTER TABLE`. This lesson shows both patterns and common error messages.

---

## 📑 Table of Contents
1. [Define Constraints at CREATE TIME](#1-define-constraints-at-create-time)
2. [Add Constraints Later with ALTER TABLE](#2-add-constraints-later-with-alter-table)
3. [Seeing Constraint Violations](#3-seeing-constraint-violations)
4. [Practical Guidelines](#4-practical-guidelines)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Define Constraints at CREATE TIME

```sql
CREATE TABLE Courses (
    course_id   INT PRIMARY KEY,
    course_code VARCHAR(10) NOT NULL UNIQUE,
    title       VARCHAR(100) NOT NULL,
    credits     INT CHECK (credits BETWEEN 1 AND 6)
);

CREATE TABLE Enrollments (
    enrollment_id INT PRIMARY KEY,
    student_id    INT NOT NULL,
    course_id     INT NOT NULL,
    CONSTRAINT fk_enroll_student
        FOREIGN KEY (student_id) REFERENCES Students(student_id),
    CONSTRAINT fk_enroll_course
        FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);
```

---

## 2. Add Constraints Later with ALTER TABLE

```sql
-- Add a unique rule after table already exists
ALTER TABLE Students
ADD CONSTRAINT uq_students_email UNIQUE (email);

-- Add a foreign key later
ALTER TABLE Orders
ADD CONSTRAINT fk_orders_student
FOREIGN KEY (student_id) REFERENCES Students(student_id);
```

If existing rows already break the new rule, the `ALTER` fails until you clean the data.

---

## 3. Seeing Constraint Violations

```sql
INSERT INTO Students (student_id, name, email)
VALUES (1, 'Amy', 'amy@example.com');

-- Duplicate primary key or unique email => error
INSERT INTO Students (student_id, name, email)
VALUES (1, 'Amy 2', 'amy@example.com');
```

Typical symptoms:
- error mentioning **unique constraint** / **primary key**
- error mentioning **foreign key constraint**
- error mentioning **check constraint**

Read the message — it usually names the constraint and the table.

---

## 4. Practical Guidelines

| Guideline | Why |
|-----------|-----|
| Always give important tables a primary key | Row identity + safer joins/updates |
| Prefer named constraints (`CONSTRAINT fk_...`) | Easier to drop/debug later |
| Put FKs on relationship columns | Stops orphan rows |
| Don't over-CHECK everything | Keep checks for true business invariants |
| Clean dirty data before adding new constraints | `ALTER` will refuse otherwise |

### Beginner tip
If a constraint keeps blocking you during learning labs, read the error first — it is often teaching you a real data-quality rule, not just "being annoying."

---

## 5. Knowledge Check

1. Write `CREATE TABLE` for `Departments(dept_id, dept_name)` with PK + unique name.
2. How do you add a foreign key to an existing table?
3. What happens if existing data violates a new `UNIQUE` constraint?
4. Why is naming constraints with `CONSTRAINT constraint_name` useful?

---

**Previous:** [← Constraints — Types and Examples](./04-Constraints-Types-and-Examples.md)
**Next:** [SQL Statements Overview →](../03-Statements-in-SQL/00-SQL-Statements-Overview.md)
