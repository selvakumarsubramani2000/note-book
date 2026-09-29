# 📋 Datatypes — Types and Examples

> **Trainer's Note:** This lesson lists the practical datatypes you will use most as a beginner, with short examples you can type in any RDBMS lab.

---

## 📑 Table of Contents
1. [Numeric Types](#1-numeric-types)
2. [Character Types](#2-character-types)
3. [Date and Time Types](#3-date-and-time-types)
4. [Quick Reference Table](#4-quick-reference-table)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Numeric Types

```sql
-- Integers
id INT                 -- whole numbers
quantity NUMBER(5)     -- Oracle-style number, up to 5 digits

-- Decimals (exact)
price DECIMAL(10, 2)   -- 10 digits total, 2 after decimal  e.g. 12345678.90
salary NUMERIC(12, 2)
```

| Type idea | Good for |
|-----------|----------|
| `INT` / small integers | IDs, counts, ages |
| `DECIMAL(p,s)` / `NUMBER(p,s)` | Money, precise measurements |
| Floating types | Scientific values where tiny rounding is OK |

---

## 2. Character Types

```sql
code   CHAR(3)         -- fixed length, e.g. 'USA' (padded if shorter)
name   VARCHAR(100)    -- variable length up to 100 characters
notes  TEXT / CLOB     -- long free-form text (product-specific name)
```

| Type idea | Behavior |
|-----------|----------|
| `CHAR(n)` | Always uses length `n` (pads with spaces) |
| `VARCHAR(n)` | Uses only as much space as the actual string (up to `n`) |
| Large text types | For paragraphs, descriptions, logs |

### Beginner tip
For most name/email/title columns, prefer **`VARCHAR`**. Use `CHAR` mainly for true fixed-width codes.

---

## 3. Date and Time Types

```sql
birth_date   DATE
created_at   TIMESTAMP     -- date + time (and often timezone support)
order_time   DATETIME      -- common in MySQL / SQL Server naming
```

```sql
-- Example inserts (syntax varies slightly by product)
INSERT INTO Events (title, event_date) VALUES ('Launch', '2026-09-22');
```

---

## 4. Quick Reference Table

| Need | Typical type |
|------|--------------|
| Student ID | `INT` / `NUMBER` |
| Full name | `VARCHAR(100)` |
| Country code `IN` | `CHAR(2)` |
| Price `99999999.99` | `DECIMAL(10,2)` |
| Birth date | `DATE` |
| Login timestamp | `TIMESTAMP` / `DATETIME` |
| Active flag | `BOOLEAN` or `CHAR(1)` / `BIT` |

Exact keywords differ:
- Oracle often uses `VARCHAR2`, `NUMBER`, `DATE`
- SQL Server uses `VARCHAR`, `INT`, `DECIMAL`, `DATETIME2`
- MySQL/PostgreSQL use familiar `VARCHAR`, `INT`, `DECIMAL`, `TIMESTAMP`

---

## 5. Knowledge Check

1. When would you choose `DECIMAL` over `INT`?
2. What is the practical difference between `CHAR(10)` and `VARCHAR(10)`?
3. Which type family stores `2026-09-22`?
4. Propose datatypes for columns: `sku`, `unit_price`, `in_stock_count`, `created_on`.

---

**Previous:** [← What Are Datatypes?](./00-What-Are-Datatypes.md)
**Next:** [How to Use Datatypes →](./02-How-to-Use-Datatypes.md)
