# 📐 Introduction to Normalization

> **Trainer's Note:** **Normalization** is the process of organizing tables to reduce duplicate data and avoid update anomalies — while keeping relationships clear.

---

## 📑 Table of Contents
1. [Why Normalize?](#1-why-normalize)
2. [Anomalies Explained](#2-anomalies-explained)
3. [The Big Idea](#3-the-big-idea)
4. [Normalization Is a Journey](#4-normalization-is-a-journey)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Why Normalize?

Unnormalized tables often store the same fact many times.

```
Bad wide table:
OrderID | CustomerName | CustomerCity | Product1 | Product2 | Product3
```

Problems: wasted space, inconsistent copies, hard queries, painful changes.

### Real-world analogy
```
Normalization = stop rewriting a customer's full address
  on every order slip; keep one customer card and reference it
```

---

## 2. Anomalies Explained

| Anomaly | Example problem |
|---------|-----------------|
| **Insert anomaly** | Can’t add a new course until a student enrolls |
| **Update anomaly** | Customer city changes → must edit many rows, some missed |
| **Delete anomaly** | Deleting last student in a department loses department info |

---

## 3. The Big Idea

1. Identify repeated groups and repeated facts  
2. Split into related tables  
3. Connect with keys  
4. Ensure each fact lives in one sensible place  

```
Customers (customer data once)
Orders (order header)
OrderItems (one row per product line)
```

---

## 4. Normalization Is a Journey

Common teaching ladder:
- 1NF
- 2NF
- 3NF
- (later: BCNF and beyond)

Most business apps aim for **3NF** (with occasional deliberate denormalization for performance/reporting).

### Beginner tip
Normalization is design quality, not a SQL command. You apply it when designing tables, then implement with `CREATE TABLE` + keys.

---

## 5. Knowledge Check

1. What is the main goal of normalization?
2. Give one example of an update anomaly.
3. Does normalization usually create more tables or fewer?
4. Is normalization a DDL keyword you run once?

---

**Previous:** [← REVOKE](../16-DCL/01-Revoke.md)
**Next:** [Types of Normal Forms →](./01-Types-of-Normal-Forms.md)
