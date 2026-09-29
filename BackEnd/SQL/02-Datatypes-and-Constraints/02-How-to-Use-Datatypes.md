# 🛠️ How to Use Datatypes

> **Trainer's Note:** Datatypes show up when you **create** tables and when you **insert/update** values. Mismatched types are a top beginner error.

---

## 📑 Table of Contents
1. [Declaring Types When Creating Tables](#1-declaring-types-when-creating-tables)
2. [Inserting Values Correctly](#2-inserting-values-correctly)
3. [Common Beginner Mistakes](#3-common-beginner-mistakes)
4. [Changing a Column Type](#4-changing-a-column-type)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Declaring Types When Creating Tables

```sql
CREATE TABLE Products (
    product_id   INT,
    product_name VARCHAR(80),
    unit_price   DECIMAL(10, 2),
    created_on   DATE
);
```

Each column name is followed by its datatype (and optional size/precision).

### Real-world analogy
```
CREATE TABLE = designing a paper form
  Each blank has a type: number box, text line, date field
  People filling the form must match those blanks
```

---

## 2. Inserting Values Correctly

```sql
INSERT INTO Products (product_id, product_name, unit_price, created_on)
VALUES (1, 'Notebook', 12.50, '2026-01-15');
```

| Column | Value shape |
|--------|-------------|
| Numeric columns | No quotes: `12.50`, `1` |
| Text columns | Quotes: `'Notebook'` |
| Date columns | Quoted date string in a format the DB accepts |

```sql
-- Wrong type example (will fail or auto-coerce dangerously)
INSERT INTO Products (product_id, product_name, unit_price, created_on)
VALUES ('one', 100, 'cheap', 'not-a-date');
```

---

## 3. Common Beginner Mistakes

| Mistake | Why it hurts |
|---------|--------------|
| Using `VARCHAR` for everything | Can't do proper math/sorting on "numbers" stored as text |
| Using float for money | Rounding surprises (`0.1 + 0.2` style issues) |
| Too-small `VARCHAR(5)` for names | Valid data gets truncated or rejected |
| Storing dates as `VARCHAR` | Breaks date math, sorting, and validation |

### Beginner tip
If you need to add, average, or compare magnitudes, store a **number**. If you need calendar logic (add 7 days, filter by month), store a **date/time type**.

---

## 4. Changing a Column Type

```sql
-- Example shape (exact syntax varies by product)
ALTER TABLE Products
MODIFY unit_price DECIMAL(12, 2);   -- Oracle-style flavor

-- SQL Server style often looks like:
-- ALTER TABLE Products ALTER COLUMN unit_price DECIMAL(12, 2);
```

Be careful: changing types can fail if existing rows contain values that don't fit the new type.

---

## 5. Knowledge Check

1. Write a `CREATE TABLE` for `Employees` with `id`, `full_name`, `salary`, `hire_date`.
2. Should string values in `INSERT` be quoted? What about integers?
3. Why is storing prices as `FLOAT` risky?
4. What can go wrong if you shrink a `VARCHAR(100)` column to `VARCHAR(10)` when long names already exist?

---

**Previous:** [← Datatypes — Types and Examples](./01-Datatypes-Types-and-Examples.md)
**Next:** [What Are Constraints? →](./03-What-Are-Constraints.md)
