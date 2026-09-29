# 🧪 ERD — Examples

> **Trainer's Note:** Two compact ER examples you can redraw on paper, then turn into `CREATE TABLE` statements.

---

## 📑 Table of Contents
1. [Example A — Campus System](#1-example-a--campus-system)
2. [Example B — Simple Shop](#2-example-b--simple-shop)
3. [Translate Example A to Tables](#3-translate-example-a-to-tables)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. Example A — Campus System

**Entities**
- STUDENT (`student_id`, name, email)
- COURSE (`course_id`, title, credits)
- INSTRUCTOR (`instructor_id`, name)
- DEPARTMENT (`dept_id`, dept_name)

**Relationships**
- DEPARTMENT 1 — N INSTRUCTOR  
- INSTRUCTOR 1 — N COURSE  
- STUDENT M — N COURSE (via ENROLLMENT)

```
DEPARTMENT 1----N INSTRUCTOR 1----N COURSE
                                      M
                                      |
                                      N
                                   STUDENT
                         (ENROLLMENT bridge in between)
```

---

## 2. Example B — Simple Shop

**Entities**
- CUSTOMER (`customer_id`, name, city)
- PRODUCT (`product_id`, name, unit_price)
- ORDER (`order_id`, order_date, customer_id)
- ORDER_ITEM (`order_id`, product_id, qty)

**Relationships**
- CUSTOMER 1 — N ORDER  
- ORDER 1 — N ORDER_ITEM  
- PRODUCT 1 — N ORDER_ITEM  

`ORDER_ITEM` resolves ORDER M—N PRODUCT.

### Real-world analogy
```
ERD Example B = retail notebook sketch:
  who buys, what ticket, which lines, which products
```

---

## 3. Translate Example A to Tables

```sql
CREATE TABLE Department (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Instructor (
    instructor_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    dept_id INT REFERENCES Department(dept_id)
);

CREATE TABLE Course (
    course_id INT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    credits INT,
    instructor_id INT REFERENCES Instructor(instructor_id)
);

CREATE TABLE Student (
    student_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE
);

CREATE TABLE Enrollment (
    student_id INT REFERENCES Student(student_id),
    course_id INT REFERENCES Course(course_id),
    grade VARCHAR(2),
    PRIMARY KEY (student_id, course_id)
);
```

### Beginner tip
When stuck drawing M:N, ask: “What event/table sits between these two nouns?” (Enrollment, OrderItem, Assignment, etc.)

---

## 4. Knowledge Check

1. In Example A, which table implements Student–Course M:N?
2. In Example B, which side of CUSTOMER–ORDER gets the FK?
3. Draw (in text) entities for a Library (Book, Member, Loan).
4. Write PK/FK choices for your Library sketch.

---

**Previous:** [← Introduction to ERD](./00-Introduction-to-ERD.md)

🎉 **SQL syllabus sections 11–18 from this image are complete** (NumPy/Pandas are separate non-SQL tracks).
