# 🧠 Brief on E.F. Codd

> **Trainer's Note:** Dr. **Edgar F. Codd** invented the relational model. Understanding a little about him (and his famous rules) helps you see why modern SQL databases look the way they do.

---

## 📑 Table of Contents
1. [Who Was E.F. Codd?](#1-who-was-ef-codd)
2. [What Did He Contribute?](#2-what-did-he-contribute)
3. [Codd's Rules (Beginner View)](#3-codds-rules-beginner-view)
4. [Why This Still Matters](#4-why-this-still-matters)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Who Was E.F. Codd?

**Edgar Frank "Ted" Codd** (1923–2003) was a computer scientist at IBM.

In 1970 he published a paper that introduced the **relational model** of data — the foundation of every modern RDBMS (Oracle, MySQL, PostgreSQL, SQL Server, and more).

### Real-world analogy
```
If modern SQL databases are cities full of well-planned roads,
E.F. Codd drew the original city plan:
  tables, keys, relationships, and logical access instead of physical file tricks
```

---

## 2. What Did He Contribute?

| Contribution | Simple meaning |
|--------------|----------------|
| **Relational model** | Data as tables related by values |
| **Separation of logical vs physical** | You query *what* you need, not *how* it's stored on disk |
| **Foundation for SQL** | Later languages (including SQL) were built to work with this model |
| **Codd's 12 rules** | A checklist for calling a system a "true" RDBMS |

Before Codd, many systems mixed storage layout and query logic tightly together. Changing disk layout often broke applications. The relational approach made data more independent and easier to query.

---

## 3. Codd's Rules (Beginner View)

Codd defined rules (often called **12 rules**, plus a foundation rule) describing what a "true" relational DBMS should support. You do **not** need to memorize all of them as a beginner — focus on the spirit:

| Idea from the rules | Beginner translation |
|---------------------|----------------------|
| Information is represented in tables | Everything useful is stored as row/column values |
| Guaranteed access | Every value is reachable by table + key + column |
| Systematic null handling | Missing data is handled consistently (`NULL`) |
| Active catalog | The database stores metadata about itself in tables |
| Comprehensive language | One language (like SQL) can define, query, update, secure |
| View updating / set operations | Work with whole sets of rows, not only one record at a time |
| Physical data independence | Apps shouldn't break if storage/indexes change |
| Logical data independence | Apps should survive reasonable table redesigns |
| Integrity independence | Rules live in the DB, not only in application code |
| Distribution independence | The user should not care if data is split across machines |
| Non-subversion | Low-level back doors shouldn't bypass integrity rules |

### Beginner tip
Treat Codd's rules as a quality checklist for RDBMS design — not as exam trivia you must recite word-for-word on day one.

---

## 4. Why This Still Matters

- Explains why SQL thinks in **sets of rows**, not "get the 3rd record on disk."
- Explains why we use **keys, constraints, and joins**.
- Helps you evaluate marketing claims: "relational" should mean more than "has tables."

When you later learn normalization, foreign keys, or ACID transactions, you are still standing on Codd's foundation.

---

## 5. Knowledge Check

1. Who proposed the relational model, and roughly when?
2. What is one practical benefit of separating logical data from physical storage?
3. Why is Codd relevant even if you mainly use MySQL or SQL Server today?
4. Name two "spirits" of Codd's rules (in plain English).

---

**Previous:** [← Introduction to RDBMS](./03-Introduction-to-RDBMS.md)
**Next:** [What are Datatypes? →](../02-Datatypes-and-Constraints/00-What-Are-Datatypes.md)
