# 🔐 Constraints — Types and Examples

> **Trainer's Note:** Learn the five core constraint types first — **PRIMARY KEY, FOREIGN KEY, UNIQUE, NOT NULL, CHECK**. These cover almost every beginner scenario.

---

## 📑 Table of Contents
1. [PRIMARY KEY](#1-primary-key)
2. [FOREIGN KEY](#2-foreign-key)
3. [UNIQUE and NOT NULL](#3-unique-and-not-null)
4. [CHECK](#4-check)
5. [DEFAULT (Related Idea)](#5-default-related-idea)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. PRIMARY KEY

Uniquely identifies each row. Cannot be `NULL`. Only one primary key per table (may be composite).

```sql
CREATE TABLE Students (
    student_id INT PRIMARY KEY,
    name VARCHAR(50)
);
```

---

## 2. FOREIGN KEY

A column (or set of columns) that **references** a primary key in another table — keeps relationships valid.

```sql
CREATE TABLE Orders (
    order_id   INT PRIMARY KEY,
    student_id INT,
    item       VARCHAR(50),
    CONSTRAINT fk_orders_student
        FOREIGN KEY (student_id) REFERENCES Students(student_id)
);
```

Trying to insert an order for a non-existent `student_id` fails.

---

## 3. UNIQUE and NOT NULL

```sql
CREATE TABLE Users (
    user_id INT PRIMARY KEY,
    email   VARCHAR(100) UNIQUE,   -- no duplicates
    name    VARCHAR(50) NOT NULL   -- required value
);
```

| Constraint | Meaning |
|------------|---------|
| `UNIQUE` | All non-null values must be different |
| `NOT NULL` | Column must always have a value |

`PRIMARY KEY` implies both uniqueness and not-null behavior.

---

## 4. CHECK

Validates a custom condition.

```sql
CREATE TABLE Products (
    product_id INT PRIMARY KEY,
    price DECIMAL(10,2) CHECK (price >= 0),
    stock INT CHECK (stock >= 0)
);
```

---

## 5. DEFAULT (Related Idea)

Not always grouped with "constraints" in every textbook, but commonly taught alongside them: supplies a value when insert omits the column.

```sql
CREATE TABLE Tickets (
    ticket_id INT PRIMARY KEY,
    status VARCHAR(20) DEFAULT 'OPEN'
);
```

### Real-world analogy
```
PK      = each citizen's unique ID card number
FK      = a form that must list a real existing citizen ID
UNIQUE  = no two people share the same registered email
NOT NULL = mandatory field on a form
CHECK   = "age must be 0 or more"
DEFAULT = if you leave Status blank, write OPEN automatically
```

---

## 6. Knowledge Check

1. What two guarantees does a primary key give you?
2. What does a foreign key prevent?
3. Write a `CHECK` that keeps `score` between 0 and 100.
4. Difference between `UNIQUE` and `PRIMARY KEY`?

---

**Previous:** [← What Are Constraints?](./03-What-Are-Constraints.md)
**Next:** [How to Use Constraints →](./05-How-to-Use-Constraints.md)
