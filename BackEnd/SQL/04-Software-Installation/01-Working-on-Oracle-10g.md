# 🗄️ Working on Oracle 10g

> **Trainer's Note:** Older SQL courses often standardized on **Oracle 10g**. This page shows the day-to-day workflow those labs expected, plus how to map it to newer tools.

---

## 📑 Table of Contents
1. [What "Working on Oracle 10g" Meant](#1-what-working-on-oracle-10g-meant)
2. [Typical Lab Workflow](#2-typical-lab-workflow)
3. [Useful Starter Commands](#3-useful-starter-commands)
4. [Oracle-Specific Habits You Will See](#4-oracle-specific-habits-you-will-see)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What "Working on Oracle 10g" Meant

In campus/training labs, students usually:
1. Logged into a lab machine or local Oracle install
2. Opened **SQL*Plus** or **SQL Developer**
3. Connected as a student/hr/scott-style training user
4. Ran scripts from the syllabus (`CREATE`, `INSERT`, `SELECT`)

Oracle 10g is outdated for new production systems, but many textbook examples and interview questions still show Oracle-flavored syntax.

---

## 2. Typical Lab Workflow

```
1. Start Oracle service / confirm DB is up
2. Open client (SQL*Plus / SQL Developer)
3. Connect with username/password/service
4. Set your working schema if needed
5. Run CREATE/INSERT practice scripts
6. Run SELECT queries for exercises
7. COMMIT when instructed
8. DROP practice objects at the end (if required)
```

### Real-world analogy
```
Working on Oracle lab =
  badge into the building (login),
  sit at your desk (schema),
  do exercises in your notebook (SQL worksheet),
  hand in results (query output)
```

---

## 3. Useful Starter Commands

```sql
-- Who am I?
SELECT USER FROM DUAL;

-- Current date
SELECT SYSDATE FROM DUAL;

-- List my tables
SELECT table_name FROM user_tables;

-- Describe a table (SQL*Plus)
DESC Students;

-- Simple create + query
CREATE TABLE demo_items (
    id   NUMBER PRIMARY KEY,
    name VARCHAR2(50)
);

INSERT INTO demo_items VALUES (1, 'Pen');
COMMIT;

SELECT * FROM demo_items;
```

---

## 4. Oracle-Specific Habits You Will See

| Habit | Notes |
|-------|-------|
| `FROM DUAL` | Oracle needs a table even for expressions; `DUAL` is the built-in one-row table |
| `VARCHAR2` | Preferred variable string type in Oracle |
| `NUMBER` | General numeric type |
| `ROWNUM`, `ROWID` | Pseudo columns covered later in this track |
| `||` concatenation | Common string join operator |

### Beginner tip
If your classroom still uses Oracle 10g images, follow the lab connection sheet exactly. If you self-study, Oracle XE or Live SQL is usually a safer modern substitute while keeping Oracle syntax familiarity.

---

## 5. Knowledge Check

1. Name two client tools commonly used with Oracle labs.
2. What is `DUAL` used for?
3. Write a query that returns the current Oracle user.
4. Why might a modern learner use Oracle XE/Live SQL instead of 10g?

---

**Previous:** [← Installing and Setup](./00-Installing-and-Setup.md)
**Next:** [SELECT →](../05-Data-Query-Language/00-Select.md)
