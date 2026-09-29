# 🧪 Normalization — Examples

> **Trainer's Note:** Walk one messy table through 1NF → 2NF → 3NF so the rules become concrete.

---

## 📑 Table of Contents
1. [Starting Messy Table](#1-starting-messy-table)
2. [To 1NF](#2-to-1nf)
3. [To 2NF](#3-to-2nf)
4. [To 3NF](#4-to-3nf)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. Starting Messy Table

**OrderSheet** (unnormalized idea):

| OrderID | CustomerName | CustomerCity | Items |
|---------|--------------|--------------|-------|
| 100 | Amy | Chennai | Pen, Bag |
| 101 | Raj | Bengaluru | Book |

Problems: multi-valued `Items`, repeated customer details across many orders later.

---

## 2. To 1NF

Atomic values; one item per row.

**OrderLine_1NF**

| OrderID | CustomerName | CustomerCity | Item |
|---------|--------------|--------------|------|
| 100 | Amy | Chennai | Pen |
| 100 | Amy | Chennai | Bag |
| 101 | Raj | Bengaluru | Book |

Still duplicates customer city/name for every line.

---

## 3. To 2NF

Assume composite idea around order+item, and remove attributes that belong only to Order or only to Customer.

**Customers**  
| CustomerID | CustomerName | CustomerCity |  
| 1 | Amy | Chennai |  
| 2 | Raj | Bengaluru |

**Orders**  
| OrderID | CustomerID |  
| 100 | 1 |  
| 101 | 2 |

**OrderItems**  
| OrderID | Item |  
| 100 | Pen |  
| 100 | Bag |  
| 101 | Book |

---

## 4. To 3NF

If we also stored `CityPincode` on Customers and `CityName` determined pincode via city attributes redundantly, we might split Cities. Simple version already close to 3NF when:

- customer facts live in Customers
- order facts live in Orders
- line facts live in OrderItems
- no non-key column determines another non-key column inappropriately

**Optional product catalog improvement**

**Products(ProductID, ProductName)**  
**OrderItems(OrderID, ProductID, Qty)**

### Real-world analogy
```
Messy spreadsheet → separate customer cards, order headers, and line-item lists
```

### Beginner tip
After splitting, always define keys/foreign keys so the relationships stay enforceable.

---

## 5. Knowledge Check

1. What changed when moving to 1NF in the example?
2. Why create a separate Customers table?
3. Draw (in words) the final tables and keys.
4. What anomaly is reduced by storing city once per customer?

---

**Previous:** [← Types of Normal Forms](./01-Types-of-Normal-Forms.md)
**Next:** [Introduction to ERD →](../18-ER-Diagrams/00-Introduction-to-ERD.md)
