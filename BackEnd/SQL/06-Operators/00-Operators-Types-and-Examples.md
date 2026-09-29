# ➕ Operators — Types and Examples

> **Trainer's Note:** SQL operators are symbols/keywords that compare values, combine conditions, calculate numbers, and match patterns. This page is your operator map.

---

## 📑 Table of Contents
1. [Arithmetic Operators](#1-arithmetic-operators)
2. [Comparison Operators](#2-comparison-operators)
3. [Logical Operators](#3-logical-operators)
4. [Special Operators](#4-special-operators)
5. [Concatenation](#5-concatenation)
6. [Knowledge Check](#6-knowledge-check)

---

## 1. Arithmetic Operators

| Op | Meaning | Example |
|----|---------|---------|
| `+` | Add | `price + tax` |
| `-` | Subtract | `salary - deduction` |
| `*` | Multiply | `qty * unit_price` |
| `/` | Divide | `total / count` |
| `%` / `MOD` | Remainder | `MOD(10,3)` → `1` |

```sql
SELECT product_name, qty * unit_price AS line_total
FROM OrderItems;
```

---

## 2. Comparison Operators

`=`, `!=` / `<>`, `>`, `<`, `>=`, `<=`

```sql
SELECT * FROM Employees WHERE salary >= 50000;
```

---

## 3. Logical Operators

| Op | Meaning |
|----|---------|
| `AND` | All conditions true |
| `OR` | At least one condition true |
| `NOT` | Negates a condition |

```sql
SELECT * FROM Students
WHERE age >= 18 AND city = 'Chennai';
```

---

## 4. Special Operators

```sql
-- BETWEEN (inclusive range)
SELECT * FROM Products WHERE price BETWEEN 100 AND 500;

-- IN (match any in list)
SELECT * FROM Students WHERE city IN ('Chennai', 'Bengaluru', 'Hyderabad');

-- LIKE (pattern match)
SELECT * FROM Students WHERE name LIKE 'A%';   -- starts with A
SELECT * FROM Students WHERE name LIKE '%an%'; -- contains an

-- IS NULL / IS NOT NULL
SELECT * FROM Students WHERE phone IS NULL;
```

| LIKE wildcard | Meaning |
|---------------|---------|
| `%` | Any number of characters |
| `_` | Exactly one character |

---

## 5. Concatenation

```sql
-- Oracle / standard-ish
SELECT first_name || ' ' || last_name AS full_name FROM Employees;

-- SQL Server often uses +
-- SELECT first_name + ' ' + last_name ...

-- Portable function form
SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM Employees;
```

### Real-world analogy
```
Arithmetic  = calculator keys
Comparison  = yes/no measuring stick
Logical     = combining multiple checklist rules
LIKE        = search-with-wildcards in a catalog
```

### Beginner tip
Operator precedence: `*` `/` before `+` `-`. Use parentheses whenever a mixed expression feels ambiguous.

---

## 6. Knowledge Check

1. Write an expression for order line total (`qty * price`).
2. Difference between `AND` and `OR`?
3. What does `name LIKE '_a%'` mean?
4. Why use `IS NULL` instead of `= NULL`?

---

**Previous:** [← ORDER BY](../05-Data-Query-Language/04-Order-By.md)
**Next:** [Single Row Functions →](../07-Functions-in-SQL/00-Single-Row-Functions.md)
