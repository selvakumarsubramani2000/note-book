# Question 33: How do you define a many-to-many table relationship?

## Answer

### What is a Many-to-Many Relationship?

A **many-to-many relationship** exists when:
- One record in Table A can relate to many records in Table B
- One record in Table B can relate to many records in Table A

**Example**: Students and Courses
- One student can enroll in many courses
- One course can have many students

---

## The Problem: You Cannot Directly Create Many-to-Many

```sql
-- ❌ This doesn't work directly in relational databases
Students → ← Courses
```

You need an intermediate table (also called: **junction table**, **bridge table**, **linking table**, or **associative table**).

---

## Solution: Junction Table

### Example 1: Students and Courses

```sql
-- Table 1: Students
CREATE TABLE Students (
    StudentId INT PRIMARY KEY IDENTITY(1,1),
    StudentName VARCHAR(100) NOT NULL,
    Email VARCHAR(100),
    EnrollmentDate DATE
);

-- Table 2: Courses
CREATE TABLE Courses (
    CourseId INT PRIMARY KEY IDENTITY(1,1),
    CourseName VARCHAR(100) NOT NULL,
    Credits INT,
    Instructor VARCHAR(100)
);

-- Junction Table: StudentCourses (links Students and Courses)
CREATE TABLE StudentCourses (
    StudentCourseId INT PRIMARY KEY IDENTITY(1,1),
    StudentId INT NOT NULL,
    CourseId INT NOT NULL,
    EnrollmentDate DATE DEFAULT GETDATE(),
    Grade VARCHAR(2),
    
    -- Foreign Keys
    FOREIGN KEY (StudentId) REFERENCES Students(StudentId),
    FOREIGN KEY (CourseId) REFERENCES Courses(CourseId),
    
    -- Prevent duplicate enrollments
    CONSTRAINT UQ_Student_Course UNIQUE (StudentId, CourseId)
);
```

**Relationship:**
```
Students (1) ←→ (*) StudentCourses (*) ←→ (1) Courses
```

---

## Inserting Data

```sql
-- Insert students
INSERT INTO Students (StudentName, Email, EnrollmentDate)
VALUES 
    ('John Doe', 'john@example.com', '2024-01-15'),
    ('Jane Smith', 'jane@example.com', '2024-01-16'),
    ('Bob Johnson', 'bob@example.com', '2024-01-17');

-- Insert courses
INSERT INTO Courses (CourseName, Credits, Instructor)
VALUES 
    ('Database Systems', 3, 'Dr. Smith'),
    ('Web Development', 4, 'Prof. Brown'),
    ('Data Structures', 3, 'Dr. Johnson');

-- Enroll students in courses
INSERT INTO StudentCourses (StudentId, CourseId, EnrollmentDate, Grade)
VALUES 
    (1, 1, '2024-01-20', 'A'),   -- John → Database Systems
    (1, 2, '2024-01-20', 'B+'),  -- John → Web Development
    (2, 1, '2024-01-21', 'A-'),  -- Jane → Database Systems
    (2, 3, '2024-01-21', 'A'),   -- Jane → Data Structures
    (3, 2, '2024-01-22', 'B');   -- Bob → Web Development
```

---

## Querying Many-to-Many Relationships

### Get all courses for a specific student

```sql
SELECT 
    s.StudentName,
    c.CourseName,
    c.Credits,
    c.Instructor,
    sc.EnrollmentDate,
    sc.Grade
FROM Students s
INNER JOIN StudentCourses sc ON s.StudentId = sc.StudentId
INNER JOIN Courses c ON sc.CourseId = c.CourseId
WHERE s.StudentId = 1;
```

### Get all students in a specific course

```sql
SELECT 
    c.CourseName,
    s.StudentName,
    s.Email,
    sc.Grade
FROM Courses c
INNER JOIN StudentCourses sc ON c.CourseId = sc.CourseId
INNER JOIN Students s ON sc.StudentId = s.StudentId
WHERE c.CourseId = 1
ORDER BY s.StudentName;
```

### Get students with their course count

```sql
SELECT 
    s.StudentId,
    s.StudentName,
    COUNT(sc.CourseId) AS TotalCourses,
    STRING_AGG(c.CourseName, ', ') AS Courses
FROM Students s
LEFT JOIN StudentCourses sc ON s.StudentId = sc.StudentId
LEFT JOIN Courses c ON sc.CourseId = c.CourseId
GROUP BY s.StudentId, s.StudentName;
```

---

## Real-World Example: E-Commerce (Products and Orders)

```sql
-- Products table
CREATE TABLE Products (
    ProductId INT PRIMARY KEY IDENTITY(1,1),
    ProductName VARCHAR(100) NOT NULL,
    Price DECIMAL(10,2) NOT NULL,
    StockQuantity INT DEFAULT 0
);

-- Orders table
CREATE TABLE Orders (
    OrderId INT PRIMARY KEY IDENTITY(1,1),
    CustomerId INT NOT NULL,
    OrderDate DATETIME DEFAULT GETDATE(),
    TotalAmount DECIMAL(10,2),
    Status VARCHAR(20)
);

-- Junction table: OrderDetails (many-to-many between Orders and Products)
CREATE TABLE OrderDetails (
    OrderDetailId INT PRIMARY KEY IDENTITY(1,1),
    OrderId INT NOT NULL,
    ProductId INT NOT NULL,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(10,2) NOT NULL,
    Discount DECIMAL(5,2) DEFAULT 0,
    
    FOREIGN KEY (OrderId) REFERENCES Orders(OrderId) ON DELETE CASCADE,
    FOREIGN KEY (ProductId) REFERENCES Products(ProductId),
    
    -- Prevent duplicate products in same order
    CONSTRAINT UQ_Order_Product UNIQUE (OrderId, ProductId)
);

-- Insert sample data
INSERT INTO Products (ProductName, Price, StockQuantity)
VALUES 
    ('Laptop', 999.99, 50),
    ('Mouse', 29.99, 200),
    ('Keyboard', 79.99, 150);

INSERT INTO Orders (CustomerId, OrderDate, Status)
VALUES 
    (1, '2024-05-01', 'Completed'),
    (2, '2024-05-02', 'Processing');

INSERT INTO OrderDetails (OrderId, ProductId, Quantity, UnitPrice, Discount)
VALUES 
    (1, 1, 1, 999.99, 0),      -- Order 1: 1 Laptop
    (1, 2, 2, 29.99, 10),      -- Order 1: 2 Mice with 10% discount
    (2, 2, 1, 29.99, 0),       -- Order 2: 1 Mouse
    (2, 3, 1, 79.99, 5);       -- Order 2: 1 Keyboard with 5% discount

-- Query: Get order with all products
SELECT 
    o.OrderId,
    o.OrderDate,
    o.Status,
    p.ProductName,
    od.Quantity,
    od.UnitPrice,
    od.Discount,
    (od.Quantity * od.UnitPrice * (1 - od.Discount/100)) AS LineTotal
FROM Orders o
INNER JOIN OrderDetails od ON o.OrderId = od.OrderId
INNER JOIN Products p ON od.ProductId = p.ProductId
WHERE o.OrderId = 1;
```

---

## Example: Social Media (Users Following Users)

```sql
-- Self-referencing many-to-many
CREATE TABLE Users (
    UserId INT PRIMARY KEY IDENTITY(1,1),
    Username VARCHAR(50) NOT NULL UNIQUE,
    Email VARCHAR(100),
    CreatedDate DATETIME DEFAULT GETDATE()
);

-- Junction table for followers/following
CREATE TABLE UserFollowers (
    FollowId INT PRIMARY KEY IDENTITY(1,1),
    FollowerId INT NOT NULL,      -- User who is following
    FollowingId INT NOT NULL,     -- User being followed
    FollowedDate DATETIME DEFAULT GETDATE(),
    
    FOREIGN KEY (FollowerId) REFERENCES Users(UserId),
    FOREIGN KEY (FollowingId) REFERENCES Users(UserId),
    
    -- A user can follow another user only once
    CONSTRAINT UQ_Follower_Following UNIQUE (FollowerId, FollowingId),
    
    -- A user cannot follow themselves
    CONSTRAINT CK_No_Self_Follow CHECK (FollowerId <> FollowingId)
);

-- Insert users
INSERT INTO Users (Username, Email)
VALUES 
    ('john_doe', 'john@example.com'),
    ('jane_smith', 'jane@example.com'),
    ('bob_wilson', 'bob@example.com');

-- Create follow relationships
INSERT INTO UserFollowers (FollowerId, FollowingId)
VALUES 
    (1, 2),  -- John follows Jane
    (1, 3),  -- John follows Bob
    (2, 1),  -- Jane follows John
    (3, 1);  -- Bob follows John

-- Get all users that John follows
SELECT 
    u.Username AS Following
FROM UserFollowers uf
INNER JOIN Users u ON uf.FollowingId = u.UserId
WHERE uf.FollowerId = 1;

-- Get all users who follow John
SELECT 
    u.Username AS Follower
FROM UserFollowers uf
INNER JOIN Users u ON uf.FollowerId = u.UserId
WHERE uf.FollowingId = 1;

-- Get follower and following counts
SELECT 
    u.Username,
    COUNT(DISTINCT followers.FollowerId) AS FollowerCount,
    COUNT(DISTINCT following.FollowingId) AS FollowingCount
FROM Users u
LEFT JOIN UserFollowers followers ON u.UserId = followers.FollowingId
LEFT JOIN UserFollowers following ON u.UserId = following.FollowerId
GROUP BY u.UserId, u.Username;
```

---

## Example: Tags System (Posts and Tags)

```sql
CREATE TABLE Posts (
    PostId INT PRIMARY KEY IDENTITY(1,1),
    Title VARCHAR(200) NOT NULL,
    Content TEXT,
    AuthorId INT,
    CreatedDate DATETIME DEFAULT GETDATE()
);

CREATE TABLE Tags (
    TagId INT PRIMARY KEY IDENTITY(1,1),
    TagName VARCHAR(50) NOT NULL UNIQUE
);

-- Junction table
CREATE TABLE PostTags (
    PostTagId INT PRIMARY KEY IDENTITY(1,1),
    PostId INT NOT NULL,
    TagId INT NOT NULL,
    
    FOREIGN KEY (PostId) REFERENCES Posts(PostId) ON DELETE CASCADE,
    FOREIGN KEY (TagId) REFERENCES Tags(TagId),
    
    CONSTRAINT UQ_Post_Tag UNIQUE (PostId, TagId)
);

-- Insert data
INSERT INTO Tags (TagName) VALUES ('Technology'), ('Programming'), ('Database');
INSERT INTO Posts (Title, Content, AuthorId) 
VALUES ('SQL Tutorial', 'Learn SQL basics...', 1);

INSERT INTO PostTags (PostId, TagId) VALUES (1, 1), (1, 2), (1, 3);

-- Get all tags for a post
SELECT t.TagName
FROM Posts p
INNER JOIN PostTags pt ON p.PostId = pt.PostId
INNER JOIN Tags t ON pt.TagId = t.TagId
WHERE p.PostId = 1;

-- Get all posts with a specific tag
SELECT p.Title, p.CreatedDate
FROM Tags t
INNER JOIN PostTags pt ON t.TagId = pt.TagId
INNER JOIN Posts p ON pt.PostId = p.PostId
WHERE t.TagName = 'Programming';
```

---

## Entity Framework Core Implementation

```csharp
// Models
public class Student
{
    public int StudentId { get; set; }
    public string StudentName { get; set; }
    
    // Navigation property
    public ICollection<StudentCourse> StudentCourses { get; set; }
}

public class Course
{
    public int CourseId { get; set; }
    public string CourseName { get; set; }
    
    // Navigation property
    public ICollection<StudentCourse> StudentCourses { get; set; }
}

// Junction entity
public class StudentCourse
{
    public int StudentCourseId { get; set; }
    public int StudentId { get; set; }
    public int CourseId { get; set; }
    public DateTime EnrollmentDate { get; set; }
    public string Grade { get; set; }
    
    // Navigation properties
    public Student Student { get; set; }
    public Course Course { get; set; }
}

// DbContext
public class SchoolContext : DbContext
{
    public DbSet<Student> Students { get; set; }
    public DbSet<Course> Courses { get; set; }
    public DbSet<StudentCourse> StudentCourses { get; set; }
    
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<StudentCourse>()
            .HasOne(sc => sc.Student)
            .WithMany(s => s.StudentCourses)
            .HasForeignKey(sc => sc.StudentId);
        
        modelBuilder.Entity<StudentCourse>()
            .HasOne(sc => sc.Course)
            .WithMany(c => c.StudentCourses)
            .HasForeignKey(sc => sc.CourseId);
        
        modelBuilder.Entity<StudentCourse>()
            .HasIndex(sc => new { sc.StudentId, sc.CourseId })
            .IsUnique();
    }
}
```

---

## Best Practices

1. ✅ **Always use a junction table** for many-to-many
2. ✅ **Add UNIQUE constraint** on foreign key combination
3. ✅ **Include additional columns** in junction table (date, status, etc.)
4. ✅ **Use meaningful junction table name** (StudentCourses, not StudentCourse)
5. ✅ **Add CASCADE DELETE** carefully
6. ✅ **Index foreign keys** for performance

---

## Summary

**Many-to-Many Relationship:**
- Requires a **junction table** (bridge table)
- Junction table contains foreign keys to both tables
- Junction table can have additional columns
- Queried using **two INNER JOINs**

**Structure:**
```
Table A (1) ←→ (*) Junction Table (*) ←→ (1) Table B
```

Essential for modeling complex relationships in normalized databases!
