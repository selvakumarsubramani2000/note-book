# 🔤 What Are Datatypes?

> **Trainer's Note:** A **datatype** tells the database what kind of value a column can store — numbers, text, dates, etc. Choosing the right type protects data quality and saves space.

---

## 📑 Table of Contents
1. [Why Datatypes Matter](#1-why-datatypes-matter)
2. [Common Datatype Families](#2-common-datatype-families)
3. [How to Choose a Type](#3-how-to-choose-a-type)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. Why Datatypes Matter

Every column in a table has a datatype.

```sql
CREATE TABLE Students (
    id     INT,
    name   VARCHAR(50),
    age    INT,
    joined DATE
);
```

If `age` is an `INT`, the database rejects `"twenty"` and stores only valid numbers. That is the datatype doing its job.

### Real-world analogy
```
Datatype = the shape of a slot on a form
  Age box only accepts digits
  Email box expects text
  Date box expects a calendar date
  The form itself rejects the wrong kind of entry
```

---

## 2. Common Datatype Families

| Family | Purpose | Typical examples |
|--------|---------|------------------|
| **Numeric** | Counts, prices, IDs | `INT`, `DECIMAL`, `NUMBER`, `FLOAT` |
| **Character / String** | Names, codes, free text | `CHAR`, `VARCHAR`, `TEXT`, `NVARCHAR` |
| **Date / Time** | Dates, timestamps | `DATE`, `TIME`, `DATETIME`, `TIMESTAMP` |
| **Boolean / Flag** | True/false style values | `BOOLEAN`, `BIT` (product-dependent) |
| **Binary** | Files/raw bytes (advanced) | `BLOB`, `VARBINARY` |

Exact names differ slightly between Oracle, MySQL, PostgreSQL, and SQL Server — the **idea** is the same.

---

## 3. How to Choose a Type

| Question | Prefer |
|----------|--------|
| Whole numbers only? | Integer type (`INT` / `NUMBER(n)`) |
| Money or exact decimals? | `DECIMAL` / `NUMERIC` (not float if exactness matters) |
| Short fixed codes (`YN`, country code)? | `CHAR` or short `VARCHAR` |
| Names / addresses of varying length? | `VARCHAR` |
| Only the calendar date? | `DATE` |
| Date + time of an event? | `DATETIME` / `TIMESTAMP` |

### Beginner tip
Don't store numbers that are **identifiers** you never calculate on (phone numbers, ZIP codes) as numeric if leading zeros matter — text is often safer.

---

## 4. Knowledge Check

1. What does a column datatype control?
2. Why is datatype important for data quality?
3. Which family would you use for a product price of `19.99`?
4. Give one reason not to store a phone number as a pure integer.

---

**Previous:** [← Brief on E.F. Codd](../01-Introduction/04-Brief-on-EF-Codd.md)
**Next:** [Datatypes — Types and Examples →](./01-Datatypes-Types-and-Examples.md)
