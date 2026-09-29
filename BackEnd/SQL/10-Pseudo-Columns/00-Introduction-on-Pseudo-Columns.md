# 👻 Introduction on Pseudo Columns

> **Trainer's Note:** A **pseudo column** behaves like a table column in `SELECT`, but it is **not stored as real table data**. Oracle's classic examples are `ROWID` and `ROWNUM`.

---

## 📑 Table of Contents
1. [What Is a Pseudo Column?](#1-what-is-a-pseudo-column)
2. [Why Pseudo Columns Exist](#2-why-pseudo-columns-exist)
3. [The Two You Must Know in This Syllabus](#3-the-two-you-must-know-in-this-syllabus)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. What Is a Pseudo Column?

A pseudo column:
- can appear in a `SELECT` list like a normal column
- is provided by the database engine
- is **not** a physical column you created with `CREATE TABLE`

```sql
SELECT ROWID, ROWNUM, name
FROM Students;
```

`name` is a real column. `ROWID` and `ROWNUM` are pseudo columns.

### Real-world analogy
```
Real column   = the student's name printed on the folder
Pseudo column = sticky notes the librarian adds while searching
  (shelf address, temporary queue number) — helpful, not part of the folder contents
```

---

## 2. Why Pseudo Columns Exist

| Need | Pseudo column help |
|------|--------------------|
| Identify a physical row quickly | `ROWID` |
| Number rows as they are processed/returned | `ROWNUM` |
| Limit top-N style results (classic Oracle) | `ROWNUM` filter patterns |

They are especially important in **Oracle-focused** syllabi (including older 10g labs).

---

## 3. The Two You Must Know in This Syllabus

| Pseudo column | One-line meaning |
|---------------|------------------|
| `ROWID` | Internal address of a row |
| `ROWNUM` | Temporary sequential number assigned to rows in a result |

Other engines solve similar problems differently:
- Top-N: `LIMIT`, `TOP`, `FETCH FIRST`
- Stable row identity: primary keys (preferred in app design)

### Beginner tip
Use pseudo columns for learning Oracle labs and specific troubleshooting. For application design, still prefer real primary keys as your public row identifiers.

---

## 4. Knowledge Check

1. How is a pseudo column different from a normal table column?
2. Name the two pseudo columns in this syllabus section.
3. Are pseudo columns stored permanently by your `CREATE TABLE` definition?
4. Why does an Oracle course emphasize them more than a MySQL course might?

---

**Previous:** [← Nested Sub Query](../08-Sub-Query/05-Nested-Sub-Query.md)
**Next:** [ROWID →](./01-ROWID.md)
