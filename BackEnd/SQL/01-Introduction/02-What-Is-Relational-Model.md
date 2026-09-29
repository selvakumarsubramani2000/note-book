# 🔗 What Is the Relational Model?

> **Trainer's Note:** The relational model is the idea that data lives in **tables**, and tables connect through **shared key values** — not through messy nested file structures.

---

## 📑 Table of Contents
1. [Core Idea](#1-core-idea)
2. [Tables, Rows, and Columns](#2-tables-rows-and-columns)
3. [Relationships via Keys](#3-relationships-via-keys)
4. [Why the Relational Model Matters](#4-why-the-relational-model-matters)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Core Idea

In the **relational model**, all data is stored as **relations** — better known in practice as **tables**.

Each table has:
- a fixed set of **columns** (attributes)
- zero or more **rows** (records / tuples)

Tables can be linked when a value in one table matches a value in another.

### Real-world analogy
```
Relational model = customer cards + order slips
  Customer card has CustomerID
  Order slip also stores CustomerID
  Match the IDs  =>  you know which customer placed which order
```

---

## 2. Tables, Rows, and Columns

```
Students
+----+--------+-----+
| id | name   | age |
+----+--------+-----+
| 1  | Amy    | 21  |
| 2  | Raj    | 23  |
+----+--------+-----+
```

| Term | Meaning |
|------|---------|
| **Table / Relation** | The whole grid (e.g., `Students`) |
| **Column / Attribute** | A property (e.g., `name`, `age`) |
| **Row / Tuple / Record** | One complete entry (Amy's row) |
| **Cell / Value** | One value at a row+column intersection |

---

## 3. Relationships via Keys

```
Students                         Orders
+----+--------+                  +----+------------+--------+
| id | name   |                  | id | student_id | item   |
+----+--------+                  +----+------------+--------+
| 1  | Amy    |  <-------------  | 10 | 1          | Book   |
| 2  | Raj    |  <-------------  | 11 | 2          | Pen    |
+----+--------+                  +----+------------+--------+
```

- `Students.id` uniquely identifies each student (primary key idea).
- `Orders.student_id` points to a student (foreign key idea).
- The **relationship** is the match between those values.

Common relationship types:
- **One-to-Many** — one student, many orders (most common)
- **One-to-One** — one user, one profile
- **Many-to-Many** — students and courses (usually needs a third table)

---

## 4. Why the Relational Model Matters

| Benefit | Explanation |
|---------|-------------|
| **Less duplication** | Store a student once; reference them many times |
| **Consistency** | Update a name in one place |
| **Flexible queries** | Join tables to answer new questions without redesigning storage |
| **Clear structure** | Easy for teams and tools to understand |

### Beginner tip
If you catch yourself copying the same customer name into 50 order rows "just in case," the relational model is pushing you to store the customer once and reference the ID instead.

---

## 5. Knowledge Check

1. What are the three main pieces of a table in the relational model?
2. How do two tables usually get "related"?
3. Give a real-world one-to-many example.
4. Why is storing the same student name repeatedly in every order a bad idea?

---

**Previous:** [← What Is DBMS?](./01-What-Is-DBMS.md)
**Next:** [Introduction to RDBMS →](./03-Introduction-to-RDBMS.md)
