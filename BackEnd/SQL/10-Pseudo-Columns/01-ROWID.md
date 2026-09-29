# 📍 ROWID

> **Trainer's Note:** `ROWID` is Oracle's internal row address — the fastest way for Oracle to locate a specific physical row.

---

## 📑 Table of Contents
1. [What ROWID Represents](#1-what-rowid-represents)
2. [Selecting ROWID](#2-selecting-rowid)
3. [Practical Use: Removing Exact Duplicates](#3-practical-use-removing-exact-duplicates)
4. [Cautions](#4-cautions)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What ROWID Represents

`ROWID` uniquely identifies a row's storage location inside a table (for normal heap tables in classic Oracle usage).

### Real-world analogy
```
ROWID = exact building + shelf + slot number of a folder
  Not the folder title — the physical place it currently sits
```

---

## 2. Selecting ROWID

```sql
SELECT ROWID, student_id, name
FROM Students
WHERE ROWNUM <= 5;
```

Each row gets a `ROWID` value even if you never created an `id` column (though real designs should still have a primary key).

---

## 3. Practical Use: Removing Exact Duplicates

When two rows look identical and you have no clean key, `ROWID` can keep one copy:

```sql
DELETE FROM Students
WHERE ROWID NOT IN (
    SELECT MIN(ROWID)
    FROM Students
    GROUP BY name, age, email
);
```

Meaning: group rows that share the same business values; keep the row with the minimum `ROWID`; delete the extras.

---

## 4. Cautions

| Caution | Why |
|---------|-----|
| ROWIDs can change in some maintenance scenarios | Don't treat them as forever-stable public IDs |
| App design should prefer primary keys | Portable and meaningful across systems |
| Not the same on non-Oracle databases | MySQL/Postgres don't expose Oracle `ROWID` |

### Beginner tip
Learn `ROWID` for Oracle labs and cleanup scripts. For application foreign keys and APIs, use your real `PRIMARY KEY` columns.

---

## 5. Knowledge Check

1. What does `ROWID` identify?
2. Write a query selecting `ROWID` and `name` from `Employees`.
3. How can `ROWID` help delete duplicate rows?
4. Should web APIs expose `ROWID` as the user identity? Why or why not?

---

**Previous:** [← Introduction on Pseudo Columns](./00-Introduction-on-Pseudo-Columns.md)
**Next:** [ROWNUM →](./02-ROWNUM.md)
