# 🔍 Data Query Language (DQL)

> **Trainer's Note:** **DQL** is how you **read** data. In practice, that almost always means the `SELECT` statement — the skill you will use every day.

---

## 📑 Table of Contents
1. [What DQL Covers](#1-what-dql-covers)
2. [The SELECT Skeleton](#2-the-select-skeleton)
3. [DQL vs DML](#3-dql-vs-dml)
4. [Where DQL Goes Next in This Track](#4-where-dql-goes-next-in-this-track)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What DQL Covers

**DQL (Data Query Language)** focuses on retrieving data without changing it.

Core command:
```sql
SELECT ...
```

With optional clauses you will master next:
`FROM`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, joins, subqueries, etc.

---

## 2. The SELECT Skeleton

```sql
SELECT column1, column2
FROM table_name
WHERE condition
GROUP BY column1
HAVING group_condition
ORDER BY column1;
```

Minimal example:
```sql
SELECT name, age
FROM Students
WHERE age >= 18
ORDER BY name;
```

This query **reads** matching rows. It does not insert, update, or delete anything.

### Real-world analogy
```
DQL = asking the librarian questions
  "Show me students aged 18+"
  The librarian brings copies/info — nothing is thrown away or rewritten
```

---

## 3. DQL vs DML

| | DQL | DML |
|---|-----|-----|
| Main job | Read data | Change data |
| Typical command | `SELECT` | `INSERT`, `UPDATE`, `DELETE` |
| Changes rows? | No | Yes |

Some textbooks place `SELECT` under DML. This syllabus keeps **DQL** separate — useful for teaching "read path" vs "write path."

---

## 4. Where DQL Goes Next in This Track

After software setup, folder `05-Data-Query-Language` deep-dives each major clause:

- `SELECT` / `FROM`
- `WHERE`
- `GROUP BY` / `HAVING`
- `ORDER BY`

### Beginner tip
If you only practice one family heavily at the start, make it DQL. Strong `SELECT` skills unlock joins, subqueries, reports, and debugging later.

---

## 5. Knowledge Check

1. What does DQL stand for?
2. Which single command is the heart of DQL?
3. Does a normal `SELECT` change table data?
4. List three clauses often used with `SELECT`.

---

**Previous:** [← DCL](./04-DCL.md)
**Next:** [Software Installation →](../04-Software-Installation/00-Installing-and-Setup.md)
