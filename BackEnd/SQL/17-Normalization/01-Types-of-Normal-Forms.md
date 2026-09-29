# 🧱 Types of Normal Forms

> **Trainer's Note:** Normal forms are checklist levels. Learn **1NF → 2NF → 3NF** deeply; that covers almost every beginner interview and design review.

---

## 📑 Table of Contents
1. [1NF — First Normal Form](#1-1nf--first-normal-form)
2. [2NF — Second Normal Form](#2-2nf--second-normal-form)
3. [3NF — Third Normal Form](#3-3nf--third-normal-form)
4. [Beyond 3NF (Awareness)](#4-beyond-3nf-awareness)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. 1NF — First Normal Form

Rules of thumb:
- atomic (single) values in each cell
- no repeating groups/arrays in one column
- each row uniquely identifiable

```
Not 1NF:
StudentID | Name | Phones
1 | Amy | 999..., 888...

1NF:
StudentID | Name
1 | Amy

StudentID | Phone
1 | 999...
1 | 888...
```

---

## 2. 2NF — Second Normal Form

- Must already be in 1NF
- No partial dependency on part of a composite key

```
Enrollment (StudentID, CourseID, StudentName, CourseName, Grade)
Problem: StudentName depends only on StudentID (part of key)

Split:
Students(StudentID, StudentName)
Courses(CourseID, CourseName)
Enrollment(StudentID, CourseID, Grade)
```

---

## 3. 3NF — Third Normal Form

- Must already be in 2NF
- No transitive dependency (non-key → non-key)

```
Employee(EmpID, DeptID, DeptName)
Problem: DeptName depends on DeptID, not directly on EmpID

Split:
Employee(EmpID, DeptID)
Department(DeptID, DeptName)
```

### Real-world analogy
```
1NF = one fact per cell
2NF = facts about the whole key, not half the key
3NF = non-key facts don't depend on other non-key facts
```

---

## 4. Beyond 3NF (Awareness)

| Form | Short idea |
|------|------------|
| **BCNF** | Stricter handle on determinant/key issues |
| **4NF / 5NF** | Multi-valued / join dependency cases (advanced) |

For this syllabus level, mastering 1NF–3NF is the goal.

### Beginner tip
If every non-key attribute depends on “the key, the whole key, and nothing but the key,” you’re in good 3NF shape.

---

## 5. Knowledge Check

1. What does 1NF forbid?
2. What kind of dependency does 2NF remove?
3. What kind of dependency does 3NF remove?
4. Give a one-line memory phrase for 3NF.

---

**Previous:** [← Introduction to Normalization](./00-Introduction-to-Normalization.md)
**Next:** [Normalization Examples →](./02-Examples.md)
