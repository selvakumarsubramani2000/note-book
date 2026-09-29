# 🗺️ Introduction to ERD

> **Trainer's Note:** An **ER Diagram (Entity-Relationship Diagram)** is a visual blueprint of data: entities, attributes, and relationships — drawn before (or while) creating tables.

---

## 📑 Table of Contents
1. [What Is an ERD?](#1-what-is-an-erd)
2. [Core Building Blocks](#2-core-building-blocks)
3. [Relationship Cardinality](#3-relationship-cardinality)
4. [From ERD to Tables](#4-from-erd-to-tables)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What Is an ERD?

ERD = diagram showing:
- **what** things you store (entities)
- **what details** they have (attributes)
- **how** they connect (relationships)

### Real-world analogy
```
ERD = architectural floor plan for your data
  Tables/SQL are the construction after the plan is agreed
```

---

## 2. Core Building Blocks

| Symbol idea | Meaning | SQL counterpart |
|-------------|---------|-----------------|
| Entity | A noun/business object | Table |
| Attribute | Property of entity | Column |
| Key attribute | Unique identifier | Primary key |
| Relationship | Association between entities | FK + join path |

```
[STUDENT] ----enrolls in---- [COURSE]
   |                            |
 student_id                   course_id
 name                         title
```

---

## 3. Relationship Cardinality

| Type | Meaning | Example |
|------|---------|---------|
| **1:1** | one to one | Person ↔ Passport |
| **1:N** | one to many | Customer → Orders |
| **M:N** | many to many | Students ↔ Courses |

Many-to-many usually becomes a **bridge table** (Enrollment).

---

## 4. From ERD to Tables

1. Each entity → table  
2. Key attribute → primary key  
3. 1:N relationship → FK on the “many” side  
4. M:N relationship → new table with two FKs  
5. Add needed constraints and datatypes  

### Beginner tip
Draw the ERD first for any non-trivial app. Fixing a diagram is cheaper than fixing production tables later.

---

## 5. Knowledge Check

1. What three things does an ERD show?
2. Map entity/attribute/relationship to SQL objects.
3. What cardinality is Customer–Orders usually?
4. How do you implement M:N in relational tables?

---

**Previous:** [← Normalization Examples](../17-Normalization/02-Examples.md)
**Next:** [ERD Examples →](./01-Examples.md)
