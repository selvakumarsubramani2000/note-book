# 🛡️ What Are Constraints?

> **Trainer's Note:** Constraints are rules attached to tables/columns so invalid data is rejected automatically — your database's seatbelt.

---

## 📑 Table of Contents
1. [What Is a Constraint?](#1-what-is-a-constraint)
2. [Why Constraints Exist](#2-why-constraints-exist)
3. [Where Constraints Live](#3-where-constraints-live)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. What Is a Constraint?

A **constraint** is a rule the RDBMS enforces on data.

Examples of rules:
- Every student must have an `id`
- No two students share the same `email`
- `age` cannot be negative
- Every `order.student_id` must match a real student

```sql
CREATE TABLE Students (
    id    INT PRIMARY KEY,          -- constraint
    email VARCHAR(100) UNIQUE,      -- constraint
    age   INT CHECK (age >= 0)      -- constraint
);
```

If an `INSERT` or `UPDATE` breaks a constraint, the database **rejects** the change.

---

## 2. Why Constraints Exist

### Real-world analogy
```
Constraints = the rules printed on a registration form
  "ID required"
  "Email must be unique"
  "Age cannot be negative"
  The clerk (DBMS) refuses incomplete or illegal forms
```

| Without constraints | With constraints |
|---------------------|------------------|
| Duplicate emails creep in | Unique emails enforced |
| Orders point to missing students | Foreign keys block orphans |
| Negative stock values appear | CHECK rules stop them |
| App bugs silently corrupt data | Database defends the data |

Constraints protect data even if application code has a bug.

---

## 3. Where Constraints Live

Constraints can be defined:
- **Inline** next to a column
- **Table-level** after all columns (needed for multi-column rules)

```sql
CREATE TABLE Enrollments (
    student_id INT,
    course_id  INT,
    PRIMARY KEY (student_id, course_id)  -- table-level composite key
);
```

### Beginner tip
Put important business rules in the database when the rule must **always** be true, not only when one particular screen remembers to check it.

---

## 4. Knowledge Check

1. What is a constraint, in one sentence?
2. What happens when an `INSERT` violates a constraint?
3. Why aren't application-only validations enough?
4. Give one example rule you would enforce with a constraint.

---

**Previous:** [← How to Use Datatypes](./02-How-to-Use-Datatypes.md)
**Next:** [Constraints — Types and Examples →](./04-Constraints-Types-and-Examples.md)
