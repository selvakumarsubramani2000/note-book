# Question 35: Why do we use joins? What types of joins are available?

## Answer

### What are SQL Joins?

**Joins** are used to combine rows from two or more tables based on a related column between them. They allow you to retrieve related data stored in different tables.

**Why use joins?** To avoid data redundancy and maintain normalized database structure.

---

## Why We Use Joins

### The Problem (Without Joins)

Imagine storing all data in one table:

```sql
-- ❌ BAD - Everything in one table (data redundancy)
CREATE TABLE Orders_Bad (
    OrderId INT,
    ProductName VARCHAR(100),
    ProductPrice DECIMAL,
    ProductCategory VARCHAR(50),
    CustomerName VARCHAR(100),
    CustomerEmail VARCHAR(100),
    CustomerAddress VARCHAR(200)
);

-- Problems:
-- 1. Same product info repeated for each order
-- 2. Same customer info repeated for each order
-- 3. Difficult to update (if product price changes, update many rows)
-- 4. Data inconsistency risks
```

### The Solution (With Joins)

```sql
-- ✅ GOOD - Normalized tables
CREATE TABLE Products (
    ProductId INT PRIMARY KEY,
    ProductName VARCHAR(100),
    Price DECIMAL,
    Category VARCHAR(50)
);

CREATE TABLE Customers (
    CustomerId INT PRIMARY KEY,
    CustomerName VARCHAR(100),
    Email VARCHAR(100),
    Address VARCHAR(200)
);

CREATE TABLE Orders (
    OrderId INT PRIMARY KEY,
    CustomerId INT,
    ProductId INT,
    Quantity INT,
    OrderDate DATE,
    FOREIGN KEY (CustomerId) REFERENCES Customers(CustomerId),
    FOREIGN KEY (ProductId) REFERENCES Products(ProductId)
);

-- Now use JOINs to combine data when needed
```

---

## Types of Joins

### 1. INNER JOIN (Most Common)

**Returns**: Only rows that have matching values in both tables

```sql
SELECT 
    o.OrderId,
    c.CustomerName,
    p.ProductName,
    o.Quantity,
    p.Price,
    (o.Quantity * p.Price) AS TotalPrice
FROM Orders o
INNER JOIN Customers c ON o.CustomerId = c.CustomerId
INNER JOIN Products p ON o.ProductId = p.ProductId;
```

**Visual:**
```
Customers Table        Orders Table          Result
┌─────────┬──────┐    ┌─────┬────────┐     ┌─────────┬─────┐
│CustId │Name  │    │OrdId│CustId  │     │Name     │OrdId│
├─────────┼──────┤    ├─────┼────────┤     ├─────────┼─────┤
│   1   │ John │    │ 101 │   1    │ --> │ John    │ 101 │
│   2   │ Jane │    │ 102 │   1    │ --> │ John    │ 102 │
│   3   │ Bob  │    │ 103 │   2    │ --> │ Jane    │ 103 │
└─────────┴──────┘    └─────┴────────┘     └─────────┴─────┘
(Bob has no orders, so not in result)
```

**Example:**
```sql
-- Get all orders with customer and product details
SELECT 
    o.OrderId,
    o.OrderDate,
    c.CustomerName,
    c.Email,
    p.ProductName,
    o.Quantity,
    p.Price,
    (o.Quantity * p.Price) AS Total
FROM Orders o
INNER JOIN Customers c ON o.CustomerId = c.CustomerId
INNER JOIN Products p ON o.ProductId = p.ProductId
WHERE o.OrderDate >= '2024-01-01'
ORDER BY o.OrderDate DESC;
```

---

### 2. LEFT JOIN (LEFT OUTER JOIN)

**Returns**: All rows from left table + matching rows from right table. If no match, NULL for right table columns.

```sql
SELECT 
    c.CustomerName,
    o.OrderId,
    o.OrderDate
FROM Customers c
LEFT JOIN Orders o ON c.CustomerId = o.CustomerId;
```

**Visual:**
```
Customers (LEFT)       Orders (RIGHT)         Result
┌─────────┬──────┐    ┌─────┬────────┐     ┌──────┬─────┐
│CustId │Name  │    │OrdId│CustId  │     │Name  │OrdId│
├─────────┼──────┤    ├─────┼────────┤     ├──────┼─────┤
│   1   │ John │    │ 101 │   1    │ --> │ John │ 101 │
│   2   │ Jane │    │ 103 │   2    │ --> │ Jane │ 103 │
│   3   │ Bob  │    └─────┴────────┘     │ Bob  │ NULL│ (No order)
└─────────┴──────┘                        └──────┴─────┘
(All customers shown, even if no orders)
```

**Example:**
```sql
-- Get all customers and their orders (including customers with no orders)
SELECT 
    c.CustomerId,
    c.CustomerName,
    COUNT(o.OrderId) AS TotalOrders,
    COALESCE(SUM(o.Quantity * p.Price), 0) AS TotalSpent
FROM Customers c
LEFT JOIN Orders o ON c.CustomerId = o.CustomerId
LEFT JOIN Products p ON o.ProductId = p.ProductId
GROUP BY c.CustomerId, c.CustomerName;

-- Find customers who have never placed an order
SELECT 
    c.CustomerId,
    c.CustomerName,
    c.Email
FROM Customers c
LEFT JOIN Orders o ON c.CustomerId = o.CustomerId
WHERE o.OrderId IS NULL;
```

---

### 3. RIGHT JOIN (RIGHT OUTER JOIN)

**Returns**: All rows from right table + matching rows from left table. If no match, NULL for left table columns.

```sql
SELECT 
    c.CustomerName,
    o.OrderId
FROM Customers c
RIGHT JOIN Orders o ON c.CustomerId = o.CustomerId;
```

**Note**: RIGHT JOIN is less commonly used. You can achieve the same result by swapping tables and using LEFT JOIN.

```sql
-- These are equivalent:
-- 1. RIGHT JOIN
SELECT * FROM Customers c
RIGHT JOIN Orders o ON c.CustomerId = o.CustomerId;

-- 2. LEFT JOIN (preferred - more readable)
SELECT * FROM Orders o
LEFT JOIN Customers c ON o.CustomerId = c.CustomerId;
```

---

### 4. FULL OUTER JOIN

**Returns**: All rows from both tables. NULL where there's no match.

```sql
SELECT 
    c.CustomerName,
    o.OrderId
FROM Customers c
FULL OUTER JOIN Orders o ON c.CustomerId = o.CustomerId;
```

**Visual:**
```
Result includes:
- All customers with orders
- All customers without orders (OrderId = NULL)
- All orders without customers (CustomerName = NULL)
```

**Example:**
```sql
-- Get all customers and all orders, showing mismatches
SELECT 
    c.CustomerId,
    c.CustomerName,
    o.OrderId,
    o.OrderDate
FROM Customers c
FULL OUTER JOIN Orders o ON c.CustomerId = o.CustomerId;
```

---

### 5. CROSS JOIN (Cartesian Product)

**Returns**: Every row from first table combined with every row from second table.

```sql
SELECT 
    c.CustomerName,
    p.ProductName
FROM Customers c
CROSS JOIN Products p;
```

**Result**: If 3 customers and 10 products → 30 rows (3 × 10)

**Use case**: Generate all possible combinations

**Example:**
```sql
-- Generate all possible product-size combinations
SELECT 
    p.ProductName,
    s.SizeName
FROM Products p
CROSS JOIN (
    SELECT 'Small' AS SizeName
    UNION ALL SELECT 'Medium'
    UNION ALL SELECT 'Large'
) s;
```

---

### 6. SELF JOIN

**Returns**: Join a table to itself

```sql
-- Employees table with ManagerId pointing to same table
SELECT 
    e.EmployeeName AS Employee,
    m.EmployeeName AS Manager
FROM Employees e
LEFT JOIN Employees m ON e.ManagerId = m.EmployeeId;
```

**Example:**
```sql
-- Find employees and their managers
CREATE TABLE Employees (
    EmployeeId INT PRIMARY KEY,
    EmployeeName VARCHAR(100),
    ManagerId INT
);

SELECT 
    e.EmployeeName AS Employee,
    COALESCE(m.EmployeeName, 'No Manager') AS Manager,
    e.Salary
FROM Employees e
LEFT JOIN Employees m ON e.ManagerId = m.EmployeeId;

-- Find employees who earn more than their manager
SELECT 
    e.EmployeeName AS Employee,
    e.Salary AS EmployeeSalary,
    m.EmployeeName AS Manager,
    m.Salary AS ManagerSalary
FROM Employees e
INNER JOIN Employees m ON e.ManagerId = m.EmployeeId
WHERE e.Salary > m.Salary;
```

---

## Real-World E-Commerce Example

```sql
-- Schema
CREATE TABLE Categories (
    CategoryId INT PRIMARY KEY,
    CategoryName VARCHAR(50)
);

CREATE TABLE Products (
    ProductId INT PRIMARY KEY,
    ProductName VARCHAR(100),
    CategoryId INT,
    Price DECIMAL(10,2),
    FOREIGN KEY (CategoryId) REFERENCES Categories(CategoryId)
);

CREATE TABLE Customers (
    CustomerId INT PRIMARY KEY,
    CustomerName VARCHAR(100),
    Email VARCHAR(100),
    City VARCHAR(50)
);

CREATE TABLE Orders (
    OrderId INT PRIMARY KEY,
    CustomerId INT,
    OrderDate DATE,
    TotalAmount DECIMAL(10,2),
    FOREIGN KEY (CustomerId) REFERENCES Customers(CustomerId)
);

CREATE TABLE OrderDetails (
    OrderDetailId INT PRIMARY KEY,
    OrderId INT,
    ProductId INT,
    Quantity INT,
    UnitPrice DECIMAL(10,2),
    FOREIGN KEY (OrderId) REFERENCES Orders(OrderId),
    FOREIGN KEY (ProductId) REFERENCES Products(ProductId)
);

-- Complex query with multiple joins
SELECT 
    o.OrderId,
    o.OrderDate,
    c.CustomerName,
    c.Email,
    c.City,
    p.ProductName,
    cat.CategoryName,
    od.Quantity,
    od.UnitPrice,
    (od.Quantity * od.UnitPrice) AS LineTotal
FROM Orders o
INNER JOIN Customers c ON o.CustomerId = c.CustomerId
INNER JOIN OrderDetails od ON o.OrderId = od.OrderId
INNER JOIN Products p ON od.ProductId = p.ProductId
INNER JOIN Categories cat ON p.CategoryId = cat.CategoryId
WHERE o.OrderDate BETWEEN '2024-01-01' AND '2024-12-31'
ORDER BY o.OrderDate DESC, o.OrderId, od.OrderDetailId;

-- Sales report by category
SELECT 
    cat.CategoryName,
    COUNT(DISTINCT o.OrderId) AS TotalOrders,
    SUM(od.Quantity) AS TotalItemsSold,
    SUM(od.Quantity * od.UnitPrice) AS TotalRevenue
FROM Categories cat
INNER JOIN Products p ON cat.CategoryId = p.CategoryId
INNER JOIN OrderDetails od ON p.ProductId = od.ProductId
INNER JOIN Orders o ON od.OrderId = o.OrderId
WHERE o.OrderDate >= '2024-01-01'
GROUP BY cat.CategoryId, cat.CategoryName
ORDER BY TotalRevenue DESC;

-- Customers who haven't ordered in the last 6 months
SELECT 
    c.CustomerId,
    c.CustomerName,
    c.Email,
    MAX(o.OrderDate) AS LastOrderDate,
    DATEDIFF(DAY, MAX(o.OrderDate), GETDATE()) AS DaysSinceLastOrder
FROM Customers c
LEFT JOIN Orders o ON c.CustomerId = o.CustomerId
GROUP BY c.CustomerId, c.CustomerName, c.Email
HAVING MAX(o.OrderDate) < DATEADD(MONTH, -6, GETDATE())
    OR MAX(o.OrderDate) IS NULL;
```

---

## Join Performance Tips

1. ✅ **Index foreign key columns**
2. ✅ **Use INNER JOIN when possible** (faster than OUTER JOIN)
3. ✅ **Filter early** with WHERE clause
4. ✅ **Avoid SELECT *** - specify only needed columns
5. ✅ **Join on indexed columns**
6. ❌ **Avoid functions on join columns** (prevents index usage)

---

## Summary

**Join Types:**
- **INNER JOIN** - Only matching rows (most common)
- **LEFT JOIN** - All from left + matches from right
- **RIGHT JOIN** - All from right + matches from left
- **FULL OUTER JOIN** - All from both tables
- **CROSS JOIN** - All combinations (Cartesian product)
- **SELF JOIN** - Table joined to itself

**Why use joins?**
- ✅ Eliminate data redundancy
- ✅ Maintain data integrity
- ✅ Normalize database structure
- ✅ Combine related data efficiently

Mastering joins is essential for effective database querying!
