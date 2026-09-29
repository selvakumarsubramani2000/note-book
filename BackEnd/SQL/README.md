# SQL Beginner Track — Master Index

> Complete curriculum map for `BackEnd/SQL/`: **18 modules**, **69 concept files**, ordered for new learners.

---

## Overview

This track teaches SQL from first principles through joins, subqueries, DDL/DML/TCL/DCL command depth, normalization, and ER diagrams. Content is beginner-friendly: real-world analogies, SQL examples, and Knowledge Checks.

| | |
|---|---|
| **Root** | `BackEnd/SQL/` |
| **Modules** | `01` … `08`, then `10` … `18` (no `09` in syllabus) |
| **Files** | 69 markdown lessons |
| **Style** | One concept per file (or tight topic group) |
| **Site** | Docusaurus **SQL Beginner Track** via `copy-notes.ps1` / `sidebars.js` |

### How to use this index

1. Follow modules **top to bottom** (learning order).  
2. Inside a module, open files by numeric prefix (`00`, `01`, …).  
3. Each lesson links **Previous / Next** for linear reading.  
4. Use this README as the campus map when jumping topics.

---

## Learning path (high level)

```text
Intro & theory → Datatypes/Constraints → Statement families
→ Tooling → DQL clauses → Operators → Functions
→ Subqueries → Pseudo columns → Joins → Correlated subquery
→ DDL / DML / TCL / DCL (command-level) → Normalization → ERD
```

---

## Module index

| # | Folder | Focus | Files |
|---|--------|--------|------:|
| 01 | [Introduction](#01-introduction) | Database, DBMS, relational model, RDBMS, Codd | 5 |
| 02 | [Datatypes and Constraints](#02-datatypes-and-constraints) | Types, usage, constraint rules | 6 |
| 03 | [Statements in SQL](#03-statements-in-sql) | DDL/DML/TCL/DCL/DQL overview | 6 |
| 04 | [Software Installation](#04-software-installation) | Setup & Oracle 10g lab context | 2 |
| 05 | [Data Query Language](#05-data-query-language) | SELECT … ORDER BY | 6 |
| 06 | [Operators](#06-operators) | Arithmetic, compare, logical, special | 1 |
| 07 | [Functions in SQL](#07-functions-in-sql) | Single-row, multi-row, aggregates | 7 |
| 08 | [Sub Query](#08-sub-query) | Intro through nested types | 6 |
| 10 | [Pseudo Columns](#10-pseudo-columns) | ROWID, ROWNUM, usage | 4 |
| 11 | [Joins](#11-joins) | Types + practice examples | 7 |
| 12 | [Correlated Sub Query](#12-correlated-sub-query) | Working & examples | 1 |
| 13 | [DDL](#13-ddl) | CREATE … DROP | 5 |
| 14 | [DML](#14-dml) | INSERT, UPDATE, DELETE | 3 |
| 15 | [TCL](#15-tcl) | COMMIT, SAVEPOINT, ROLLBACK | 3 |
| 16 | [DCL](#16-dcl) | GRANT, REVOKE | 2 |
| 17 | [Normalization](#17-normalization) | 1NF–3NF + walkthrough | 3 |
| 18 | [ER Diagrams](#18-er-diagrams) | ERD intro + examples | 2 |

**Start here:** [01-Introduction/00-What-Is-Database.md](./01-Introduction/00-What-Is-Database.md)

---

## 01-Introduction

Foundations before any query syntax.

| File | Topic | Summary |
|------|--------|---------|
| [00-What-Is-Database.md](./01-Introduction/00-What-Is-Database.md) | What is a database? | Organized data store vs files/spreadsheets |
| [01-What-Is-DBMS.md](./01-Introduction/01-What-Is-DBMS.md) | DBMS | Software that manages storage, access, integrity |
| [02-What-Is-Relational-Model.md](./01-Introduction/02-What-Is-Relational-Model.md) | Relational model | Tables, rows, columns, keys, relationships |
| [03-Introduction-to-RDBMS.md](./01-Introduction/03-Introduction-to-RDBMS.md) | RDBMS | Relational engines + SQL; popular products |
| [04-Brief-on-EF-Codd.md](./01-Introduction/04-Brief-on-EF-Codd.md) | E.F. Codd | Relational model origin and rules (spirit) |

---

## 02-Datatypes-and-Constraints

Column types and integrity rules.

| File | Topic | Summary |
|------|--------|---------|
| [00-What-Are-Datatypes.md](./02-Datatypes-and-Constraints/00-What-Are-Datatypes.md) | What are datatypes? | Why columns need types |
| [01-Datatypes-Types-and-Examples.md](./02-Datatypes-and-Constraints/01-Datatypes-Types-and-Examples.md) | Types & examples | Numeric, string, date/time catalog |
| [02-How-to-Use-Datatypes.md](./02-Datatypes-and-Constraints/02-How-to-Use-Datatypes.md) | How to use | CREATE/INSERT patterns and pitfalls |
| [03-What-Are-Constraints.md](./02-Datatypes-and-Constraints/03-What-Are-Constraints.md) | What are constraints? | Rules the engine enforces |
| [04-Constraints-Types-and-Examples.md](./02-Datatypes-and-Constraints/04-Constraints-Types-and-Examples.md) | Types & examples | PK, FK, UNIQUE, NOT NULL, CHECK |
| [05-How-to-Use-Constraints.md](./02-Datatypes-and-Constraints/05-How-to-Use-Constraints.md) | How to use | CREATE/ALTER constraints, violations |

---

## 03-Statements-in-SQL

Five command families (map of SQL).

| File | Topic | Summary |
|------|--------|---------|
| [00-SQL-Statements-Overview.md](./03-Statements-in-SQL/00-SQL-Statements-Overview.md) | Overview | DDL, DML, TCL, DCL, DQL at a glance |
| [01-DDL.md](./03-Statements-in-SQL/01-DDL.md) | DDL | Structure: CREATE, ALTER, DROP, TRUNCATE |
| [02-DML.md](./03-Statements-in-SQL/02-DML.md) | DML | Data change: INSERT, UPDATE, DELETE |
| [03-TCL.md](./03-Statements-in-SQL/03-TCL.md) | TCL | COMMIT, ROLLBACK, SAVEPOINT |
| [04-DCL.md](./03-Statements-in-SQL/04-DCL.md) | DCL | GRANT, REVOKE |
| [05-DQL.md](./03-Statements-in-SQL/05-DQL.md) | DQL | SELECT as the read path |

---

## 04-Software-Installation

Lab setup (Oracle-oriented syllabus, modern alternatives noted).

| File | Topic | Summary |
|------|--------|---------|
| [00-Installing-and-Setup.md](./04-Software-Installation/00-Installing-and-Setup.md) | Installing & setup | Engine + client + smoke tests |
| [01-Working-on-Oracle-10g.md](./04-Software-Installation/01-Working-on-Oracle-10g.md) | Working on Oracle 10g | Classic lab workflow, DUAL, VARCHAR2 |

---

## 05-Data-Query-Language

Core DQL clauses — one file each.

| File | Topic | Summary |
|------|--------|---------|
| [00-Select.md](./05-Data-Query-Language/00-Select.md) | SELECT | Columns, `*`, aliases, DISTINCT |
| [01-From.md](./05-Data-Query-Language/01-From.md) | FROM | Source table, aliases, DUAL |
| [02-Where.md](./05-Data-Query-Language/02-Where.md) | WHERE | Row filters, AND/OR, NULL |
| [03-Group-By.md](./05-Data-Query-Language/03-Group-By.md) | GROUP BY | Buckets for aggregates |
| [04-Having.md](./05-Data-Query-Language/04-Having.md) | HAVING | Filter groups after aggregation |
| [05-Order-By.md](./05-Data-Query-Language/05-Order-By.md) | ORDER BY | Sort final results |

---

## 06-Operators

| File | Topic | Summary |
|------|--------|---------|
| [00-Operators-Types-and-Examples.md](./06-Operators/00-Operators-Types-and-Examples.md) | Operators | Arithmetic, comparison, logical, BETWEEN/IN/LIKE, concat |

---

## 07-Functions-in-SQL

| File | Topic | Summary |
|------|--------|---------|
| [00-Single-Row-Functions.md](./07-Functions-in-SQL/00-Single-Row-Functions.md) | Single-row | Per-row text/number/date functions |
| [01-Multi-Row-Functions.md](./07-Functions-in-SQL/01-Multi-Row-Functions.md) | Multi-row | Aggregate family overview |
| [02-MAX.md](./07-Functions-in-SQL/02-MAX.md) | MAX() | Largest value |
| [03-MIN.md](./07-Functions-in-SQL/03-MIN.md) | MIN() | Smallest value |
| [04-SUM.md](./07-Functions-in-SQL/04-SUM.md) | SUM() | Total of numerics |
| [05-AVG.md](./07-Functions-in-SQL/05-AVG.md) | AVG() | Mean of numerics |
| [06-COUNT.md](./07-Functions-in-SQL/06-COUNT.md) | COUNT() | Row / non-null / distinct counts |

---

## 08-Sub-Query

| File | Topic | Summary |
|------|--------|---------|
| [00-Introduction-to-Sub-Query.md](./08-Sub-Query/00-Introduction-to-Sub-Query.md) | Introduction | Nested query idea and placements |
| [01-Working-of-Sub-Query.md](./08-Sub-Query/01-Working-of-Sub-Query.md) | Working | Inside-out execution; independent vs correlated preview |
| [02-Query-Writing-and-Execution.md](./08-Sub-Query/02-Query-Writing-and-Execution.md) | Writing & execution | Recipe, validation, common errors |
| [03-Single-Row-Sub-Query.md](./08-Sub-Query/03-Single-Row-Sub-Query.md) | Single-row | One value; `=` `>` etc. |
| [04-Multi-Row-Sub-Query.md](./08-Sub-Query/04-Multi-Row-Sub-Query.md) | Multi-row | `IN` / `ANY` / `ALL` / `EXISTS` |
| [05-Nested-Sub-Query.md](./08-Sub-Query/05-Nested-Sub-Query.md) | Nested | Multiple levels, inside-out reading |

---

## 10-Pseudo-Columns

Oracle-flavored virtual columns (syllabus has no topic 09).

| File | Topic | Summary |
|------|--------|---------|
| [00-Introduction-on-Pseudo-Columns.md](./10-Pseudo-Columns/00-Introduction-on-Pseudo-Columns.md) | Introduction | Not stored columns; engine-provided |
| [01-ROWID.md](./10-Pseudo-Columns/01-ROWID.md) | ROWID | Physical row address; cleanup patterns |
| [02-ROWNUM.md](./10-Pseudo-Columns/02-ROWNUM.md) | ROWNUM | Temporary sequence; Top-N pattern |
| [03-Working-and-Usage.md](./10-Pseudo-Columns/03-Working-and-Usage.md) | Working & usage | Side-by-side lab tasks |

---

## 11-Joins

| File | Topic | Summary |
|------|--------|---------|
| [00-What-Is-Join.md](./11-Joins/00-What-Is-Join.md) | What is a join? | Combine related tables via keys |
| [01-Types-of-Joins.md](./11-Joins/01-Types-of-Joins.md) | Types overview | Inner/outer/cross/self map |
| [02-Cartesian-Join.md](./11-Joins/02-Cartesian-Join.md) | Cartesian / CROSS | All combinations; accidental products |
| [03-Inner-Join.md](./11-Joins/03-Inner-Join.md) | INNER JOIN | Matches only |
| [04-Outer-Join.md](./11-Joins/04-Outer-Join.md) | OUTER JOIN | LEFT/RIGHT/FULL; unmatched rows |
| [05-Self-Join.md](./11-Joins/05-Self-Join.md) | Self-join | Table joined to itself |
| [06-Queries-and-Examples.md](./11-Joins/06-Queries-and-Examples.md) | Queries & examples | Practice pack and mistakes |

---

## 12-Correlated-Sub-Query

| File | Topic | Summary |
|------|--------|---------|
| [00-Working-and-Examples.md](./12-Correlated-Sub-Query/00-Working-and-Examples.md) | Working & examples | Outer-row references; EXISTS; performance notes |

---

## 13-DDL

Command-level data definition (deeper than module 03 overview).

| File | Topic | Summary |
|------|--------|---------|
| [00-Create.md](./13-DDL/00-Create.md) | CREATE | Tables and related objects |
| [01-Rename.md](./13-DDL/01-Rename.md) | RENAME | Rename tables/objects (vendor variants) |
| [02-Alter.md](./13-DDL/02-Alter.md) | ALTER | Add/modify/drop columns & constraints |
| [03-Truncate.md](./13-DDL/03-Truncate.md) | TRUNCATE | Fast empty table; no WHERE |
| [04-Drop.md](./13-DDL/04-Drop.md) | DROP | Remove objects permanently |

---

## 14-DML

| File | Topic | Summary |
|------|--------|---------|
| [00-Insert.md](./14-DML/00-Insert.md) | INSERT | Single, multi-row, INSERT…SELECT |
| [01-Update.md](./14-DML/01-Update.md) | UPDATE | SET changes; WHERE safety |
| [02-Delete.md](./14-DML/02-Delete.md) | DELETE | Remove rows; vs TRUNCATE; FK blocks |

---

## 15-TCL

| File | Topic | Summary |
|------|--------|---------|
| [00-Commit.md](./15-TCL/00-Commit.md) | COMMIT | Make transaction permanent |
| [01-Savepoint.md](./15-TCL/01-Savepoint.md) | SAVEPOINT | Partial rollback markers |
| [02-Rollback.md](./15-TCL/02-Rollback.md) | ROLLBACK | Undo uncommitted work |

---

## 16-DCL

| File | Topic | Summary |
|------|--------|---------|
| [00-Grant.md](./16-DCL/00-Grant.md) | GRANT | Give privileges; least privilege |
| [01-Revoke.md](./16-DCL/01-Revoke.md) | REVOKE | Remove privileges |

---

## 17-Normalization

| File | Topic | Summary |
|------|--------|---------|
| [00-Introduction-to-Normalization.md](./17-Normalization/00-Introduction-to-Normalization.md) | Introduction | Why normalize; anomalies |
| [01-Types-of-Normal-Forms.md](./17-Normalization/01-Types-of-Normal-Forms.md) | Types of NFs | 1NF, 2NF, 3NF (+ awareness beyond) |
| [02-Examples.md](./17-Normalization/02-Examples.md) | Examples | Messy table walked to 3NF |

---

## 18-ER-Diagrams

| File | Topic | Summary |
|------|--------|---------|
| [00-Introduction-to-ERD.md](./18-ER-Diagrams/00-Introduction-to-ERD.md) | Introduction to ERD | Entities, attributes, relationships, cardinality |
| [01-Examples.md](./18-ER-Diagrams/01-Examples.md) | Examples | Campus & shop ERDs → CREATE TABLE |

**End of track:** [18-ER-Diagrams/01-Examples.md](./18-ER-Diagrams/01-Examples.md)

---

## Suggested study waves

| Wave | Modules | Goal |
|------|---------|------|
| **A — Foundations** | 01–04 | Vocabulary, types, constraints, tooling |
| **B — Query core** | 05–07 | SELECT fluency, operators, functions |
| **C — Multi-table logic** | 08, 10–12 | Subqueries, pseudo columns, joins, correlation |
| **D — Change & control** | 13–16 | Structure/data/tx/security commands |
| **E — Design** | 17–18 | Normalized schemas and ER thinking |

---

## Related notes

| Resource | Role |
|----------|------|
| [`Topics.md`](../../Topics.md) (repo root) | Master curriculum coverage tracker |
| `Notes-Web-Site/sidebars.js` | Website sidebar labels for this track |
| `Notes-Web-Site/copy-notes.ps1` | Syncs these files into `docs/backend/sql/` |
| `BackEnd/SQL-Learning/` (if present) | Older consolidated SQL Learning notes (separate) |

---

## Counts

| Item | Count |
|------|------:|
| Modules (folders) | 17 |
| Concept markdown files | 69 |
| First lesson | `01-Introduction/00-What-Is-Database.md` |
| Last lesson | `18-ER-Diagrams/01-Examples.md` |

Happy querying.
