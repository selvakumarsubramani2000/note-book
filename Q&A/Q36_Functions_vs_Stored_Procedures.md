# Question 36: What is the difference between a function and a stored procedure? When would you use each?

## Answer

### Quick Overview

**Stored Procedures** and **Functions** are both stored in the database, but they have different purposes and capabilities.

**Simple Answer:**
- **Stored Procedure**: Performs an action (INSERT, UPDATE, DELETE)
- **Function**: Calculates and returns a value

---

## Key Differences Table

| Feature | Stored Procedure | Function |
|---------|-----------------|----------|
| **Purpose** | Perform actions | Calculate and return value |
| **Return Value** | Optional (via OUT parameters) | Must return a value |
| **Return Type** | Multiple values possible | Single value or table |
| **DML Operations** | ✅ Can use INSERT, UPDATE, DELETE | ❌ Cannot modify data (in functions) |
| **Called From** | EXECUTE/EXEC statement | SELECT, WHERE, JOIN clauses |
| **Transactions** | ✅ Can manage transactions | ❌ Cannot use transactions |
| **Exception Handling** | ✅ TRY...CATCH supported | Limited exception handling |
| **Use in SELECT** | ❌ Cannot use in SELECT | ✅ Can use in SELECT |

---

## Stored Procedures

### What is a Stored Procedure?

A **stored procedure** is a set of SQL statements stored in the database that can be executed as a unit. Think of it as a **saved script** that performs operations.

### Creating a Stored Procedure

```sql
-- Simple stored procedure
CREATE PROCEDURE GetAllProducts
AS
BEGIN
    SELECT ProductId, ProductName, Price, StockQuantity
    FROM Products
    ORDER BY ProductName;
END;

-- Execute
EXEC GetAllProducts;
```

### With Parameters

```sql
CREATE PROCEDURE GetProductsByCategory
    @CategoryId INT,
    @MinPrice DECIMAL(10,2) = 0  -- Default value
AS
BEGIN
    SELECT ProductId, ProductName, Price, Category
    FROM Products
    WHERE CategoryId = @CategoryId
      AND Price >= @MinPrice
    ORDER BY Price;
END;

-- Execute
EXEC GetProductsByCategory @CategoryId = 1, @MinPrice = 50.00;
EXEC GetProductsByCategory 1, 50.00;  -- Positional parameters
```

### With OUTPUT Parameters

```sql
CREATE PROCEDURE CreateOrder
    @CustomerId INT,
    @TotalAmount DECIMAL(10,2),
    @OrderId INT OUTPUT  -- Output parameter
AS
BEGIN
    INSERT INTO Orders (CustomerId, OrderDate, TotalAmount, Status)
    VALUES (@CustomerId, GETDATE(), @TotalAmount, 'Pending');
    
    SET @OrderId = SCOPE_IDENTITY();  -- Get newly created ID
    
    SELECT @OrderId AS NewOrderId;
END;

-- Execute with OUTPUT
DECLARE @NewOrderId INT;
EXEC CreateOrder 
    @CustomerId = 1, 
    @TotalAmount = 199.99, 
    @OrderId = @NewOrderId OUTPUT;

SELECT @NewOrderId;  -- Use the returned value
```

### Complex Example: E-Commerce Order

```sql
CREATE PROCEDURE ProcessOrder
    @CustomerId INT,
    @ProductId INT,
    @Quantity INT,
    @OrderId INT OUTPUT,
    @ErrorMessage VARCHAR(255) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Check stock
        DECLARE @StockQuantity INT, @Price DECIMAL(10,2);
        
        SELECT @StockQuantity = StockQuantity, @Price = Price
        FROM Products
        WHERE ProductId = @ProductId;
        
        IF @StockQuantity < @Quantity
        BEGIN
            SET @ErrorMessage = 'Insufficient stock';
            ROLLBACK TRANSACTION;
            RETURN -1;
        END
        
        -- Create order
        INSERT INTO Orders (CustomerId, OrderDate, TotalAmount, Status)
        VALUES (@CustomerId, GETDATE(), @Price * @Quantity, 'Processing');
        
        SET @OrderId = SCOPE_IDENTITY();
        
        -- Create order details
        INSERT INTO OrderDetails (OrderId, ProductId, Quantity, UnitPrice)
        VALUES (@OrderId, @ProductId, @Quantity, @Price);
        
        -- Update stock
        UPDATE Products
        SET StockQuantity = StockQuantity - @Quantity
        WHERE ProductId = @ProductId;
        
        COMMIT TRANSACTION;
        SET @ErrorMessage = 'Success';
        RETURN 0;
        
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
            
        SET @ErrorMessage = ERROR_MESSAGE();
        RETURN -1;
    END CATCH
END;

-- Usage
DECLARE @OrderId INT, @ErrorMsg VARCHAR(255);
EXEC ProcessOrder 
    @CustomerId = 1,
    @ProductId = 5,
    @Quantity = 2,
    @OrderId = @OrderId OUTPUT,
    @ErrorMessage = @ErrorMsg OUTPUT;

PRINT 'Order ID: ' + CAST(@OrderId AS VARCHAR);
PRINT 'Message: ' + @ErrorMsg;
```

---

## Functions

### Types of Functions

1. **Scalar Functions** - Return a single value
2. **Table-Valued Functions** - Return a table

### Scalar Functions

```sql
-- Calculate discount
CREATE FUNCTION CalculateDiscount
(
    @Price DECIMAL(10,2),
    @DiscountPercent DECIMAL(5,2)
)
RETURNS DECIMAL(10,2)
AS
BEGIN
    DECLARE @DiscountAmount DECIMAL(10,2);
    SET @DiscountAmount = @Price * (@DiscountPercent / 100);
    RETURN @DiscountAmount;
END;

-- Usage in SELECT
SELECT 
    ProductName,
    Price,
    dbo.CalculateDiscount(Price, 10) AS Discount,
    Price - dbo.CalculateDiscount(Price, 10) AS FinalPrice
FROM Products;
```

### More Scalar Function Examples

```sql
-- Calculate age from birth date
CREATE FUNCTION CalculateAge
(
    @BirthDate DATE
)
RETURNS INT
AS
BEGIN
    RETURN DATEDIFF(YEAR, @BirthDate, GETDATE());
END;

-- Usage
SELECT 
    CustomerName,
    BirthDate,
    dbo.CalculateAge(BirthDate) AS Age
FROM Customers;

-- Format phone number
CREATE FUNCTION FormatPhoneNumber
(
    @Phone VARCHAR(10)
)
RETURNS VARCHAR(14)
AS
BEGIN
    RETURN '(' + SUBSTRING(@Phone, 1, 3) + ') ' + 
           SUBSTRING(@Phone, 4, 3) + '-' + 
           SUBSTRING(@Phone, 7, 4);
END;

SELECT dbo.FormatPhoneNumber('5551234567');  -- Returns: (555) 123-4567
```

### Table-Valued Functions

```sql
-- Inline Table-Valued Function (faster)
CREATE FUNCTION GetProductsByPriceRange
(
    @MinPrice DECIMAL(10,2),
    @MaxPrice DECIMAL(10,2)
)
RETURNS TABLE
AS
RETURN
(
    SELECT ProductId, ProductName, Price, CategoryId
    FROM Products
    WHERE Price BETWEEN @MinPrice AND @MaxPrice
);

-- Usage
SELECT * FROM dbo.GetProductsByPriceRange(10.00, 100.00);

-- Use in JOIN
SELECT 
    c.CategoryName,
    p.ProductName,
    p.Price
FROM Categories c
INNER JOIN dbo.GetProductsByPriceRange(50, 200) p
    ON c.CategoryId = p.CategoryId;
```

### Multi-Statement Table-Valued Function

```sql
CREATE FUNCTION GetCustomerOrderSummary
(
    @CustomerId INT
)
RETURNS @OrderSummary TABLE
(
    OrderId INT,
    OrderDate DATE,
    TotalAmount DECIMAL(10,2),
    ItemCount INT
)
AS
BEGIN
    INSERT INTO @OrderSummary
    SELECT 
        o.OrderId,
        o.OrderDate,
        o.TotalAmount,
        COUNT(od.OrderDetailId) AS ItemCount
    FROM Orders o
    INNER JOIN OrderDetails od ON o.OrderId = od.OrderId
    WHERE o.CustomerId = @CustomerId
    GROUP BY o.OrderId, o.OrderDate, o.TotalAmount;
    
    RETURN;
END;

-- Usage
SELECT * FROM dbo.GetCustomerOrderSummary(1);
```

---

## When to Use Each

### Use Stored Procedures When:

✅ **Modifying Data** (INSERT, UPDATE, DELETE)
```sql
CREATE PROCEDURE DeleteOldOrders
    @DaysOld INT
AS
BEGIN
    DELETE FROM Orders
    WHERE OrderDate < DATEADD(DAY, -@DaysOld, GETDATE())
      AND Status = 'Completed';
END;
```

✅ **Complex Business Logic**
```sql
CREATE PROCEDURE MonthlyReporting
AS
BEGIN
    -- Multiple operations
    UPDATE Statistics SET LastRun = GETDATE();
    INSERT INTO Reports SELECT * FROM CurrentMonthData;
    DELETE FROM TempData WHERE Processed = 1;
    EXEC SendEmailNotification;
END;
```

✅ **Transaction Management**
```sql
CREATE PROCEDURE TransferFunds
    @FromAccount INT,
    @ToAccount INT,
    @Amount DECIMAL(10,2)
AS
BEGIN
    BEGIN TRANSACTION;
    
    UPDATE Accounts SET Balance = Balance - @Amount WHERE AccountId = @FromAccount;
    UPDATE Accounts SET Balance = Balance + @Amount WHERE AccountId = @ToAccount;
    
    COMMIT TRANSACTION;
END;
```

✅ **Multiple Return Values**
```sql
CREATE PROCEDURE GetOrderStats
    @CustomerId INT,
    @TotalOrders INT OUTPUT,
    @TotalSpent DECIMAL(10,2) OUTPUT
AS
BEGIN
    SELECT 
        @TotalOrders = COUNT(*),
        @TotalSpent = SUM(TotalAmount)
    FROM Orders
    WHERE CustomerId = @CustomerId;
END;
```

---

### Use Functions When:

✅ **Calculations in SELECT**
```sql
SELECT 
    ProductName,
    Price,
    dbo.CalculateTax(Price, 0.08) AS Tax
FROM Products;
```

✅ **Computed Columns**
```sql
ALTER TABLE Orders
ADD TotalWithTax AS (TotalAmount + dbo.CalculateTax(TotalAmount, 0.08));
```

✅ **WHERE Clause Filtering**
```sql
SELECT *
FROM Customers
WHERE dbo.CalculateAge(BirthDate) >= 18;
```

✅ **Reusable Calculations**
```sql
CREATE FUNCTION GetFullName
(
    @FirstName VARCHAR(50),
    @LastName VARCHAR(50)
)
RETURNS VARCHAR(101)
AS
BEGIN
    RETURN @LastName + ', ' + @FirstName;
END;

SELECT dbo.GetFullName(FirstName, LastName) AS FullName
FROM Employees;
```

---

## Real-World Example: E-Commerce System

```sql
-- FUNCTION: Calculate order total
CREATE FUNCTION CalculateOrderTotal
(
    @OrderId INT
)
RETURNS DECIMAL(10,2)
AS
BEGIN
    DECLARE @Total DECIMAL(10,2);
    
    SELECT @Total = SUM(Quantity * UnitPrice)
    FROM OrderDetails
    WHERE OrderId = @OrderId;
    
    RETURN ISNULL(@Total, 0);
END;

-- STORED PROCEDURE: Create order
CREATE PROCEDURE CreateOrderWithItems
    @CustomerId INT,
    @ProductIds VARCHAR(MAX),  -- Comma-separated: "1,2,3"
    @Quantities VARCHAR(MAX),  -- Comma-separated: "2,1,3"
    @OrderId INT OUTPUT
AS
BEGIN
    BEGIN TRANSACTION;
    
    -- Create order
    INSERT INTO Orders (CustomerId, OrderDate, Status)
    VALUES (@CustomerId, GETDATE(), 'Pending');
    
    SET @OrderId = SCOPE_IDENTITY();
    
    -- Add order items (simplified - would need string parsing)
    -- ... insert order details ...
    
    -- Update total using function
    UPDATE Orders
    SET TotalAmount = dbo.CalculateOrderTotal(@OrderId)
    WHERE OrderId = @OrderId;
    
    COMMIT TRANSACTION;
END;
```

---

## Best Practices

### Stored Procedures:
1. ✅ Use for data modifications
2. ✅ Use for complex workflows
3. ✅ Include error handling (TRY...CATCH)
4. ✅ Use transactions when needed
5. ✅ Name with verb prefix (Get, Create, Update, Delete)

### Functions:
1. ✅ Use for calculations
2. ✅ Keep functions deterministic when possible
3. ✅ Avoid complex logic
4. ✅ Don't modify data
5. ✅ Name with descriptive calculation name

---

## Summary

**Stored Procedure:**
- **Purpose**: Perform actions
- **Can**: Modify data, use transactions, return multiple values
- **Use for**: Business logic, data modifications, workflows

**Function:**
- **Purpose**: Calculate and return value
- **Can**: Be used in SELECT, WHERE, JOIN
- **Use for**: Calculations, formatting, filtering

Choose based on what you need to accomplish!
