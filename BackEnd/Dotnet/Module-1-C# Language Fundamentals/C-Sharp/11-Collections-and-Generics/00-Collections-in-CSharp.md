# 📚 Collections in C#

> **Trainer's Note:** A collection stores many items in one place and gives ready methods to add, remove, search, and loop. This is the map of the whole Collections & Generics folder.

---

## 📑 Table of Contents
1. [What is a Collection?](#1-what-is-a-collection)
2. [Why Collections Instead of Only Arrays?](#2-why-collections-instead-of-only-arrays)
3. [Two Main Collection Families](#3-two-main-collection-families)
4. [How to Choose a Collection](#4-how-to-choose-a-collection)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is a Collection?

A **collection** is an object that holds a group of items and supports common operations.

```csharp
List<string> cities = new List<string>();
cities.Add("Chennai");
cities.Add("Mumbai");
```

### Real-world analogy
```
Variable   = one bottle
Array      = fixed rack (size decided early)
Collection = smart storeroom
             add, remove, search, count anytime
```

### Common operations (same idea in most collections)
| Action | Typical methods |
|--------|------------------|
| Add | `Add`, `Push`, `Enqueue` |
| Remove | `Remove`, `Pop`, `Dequeue` |
| Count | `Count` |
| Search | `Contains`, key lookup |
| Loop | `foreach` |
| Clear | `Clear()` |

---

## 2. Why Collections Instead of Only Arrays?

| Need | Array | Collection |
|------|-------|------------|
| Grow later | Hard (fixed size) | Many grow automatically |
| Insert/remove middle | Manual work | Ready methods |
| Key-based lookup | Not natural | Dictionary family |
| Unique values only | Manual checks | HashSet / SortedSet |
| LIFO / FIFO behavior | Manual | Stack / Queue |

Arrays are still useful for fixed same-type data. Collections shine when size and behavior change.

---

## 3. Two Main Collection Families

```
System.Collections                 → older, non-generic
  ArrayList, Hashtable, Stack, Queue (non-generic)

System.Collections.Generic         → modern, type-safe (preferred)
  List<T>, Dictionary<TKey,TValue>, HashSet<T>,
  Stack<T>, Queue<T>, LinkedList<T>, SortedList, SortedSet...
```

### Beginner rule
> For new code, prefer **generic collections** (`List<int>`, `Dictionary<string,int>`).  
> Learn non-generic ones for old code and interviews.

---

## 4. How to Choose a Collection

| If you need... | Use | Guide |
|----------------|-----|-------|
| Growable list by index | `List<T>` | List |
| Key sorted + value | `SortedList` | SortedList |
| Unique values, fast check | `HashSet<T>` | HashSet |
| Unique + sorted values | `SortedSet<T>` | SortedSet |
| Fast key → value | `Dictionary` | Dictionary |
| Key → value, keys sorted | `SortedDictionary` | SortedDictionary |
| Old non-generic map | `Hashtable` | Hashtable |
| Last-In-First-Out | `Stack<T>` | Stack |
| First-In-First-Out | `Queue<T>` | Queue |
| Node chain insert/remove | `LinkedList<T>` | LinkedList |

### Tiny examples
```csharp
List<int> marks = new() { 80, 90 };
Dictionary<int, string> students = new() { [101] = "Anu" };
Stack<string> undo = new(); undo.Push("type A");
Queue<string> line = new(); line.Enqueue("Ticket-1");
```

---

## 5. Knowledge Check

1. What problem do collections solve?
2. Name one non-generic and one generic collection.
3. Which collection fits "unique email IDs only"?
4. Which collection fits browser Back history (latest first)?
5. Which collection fits a customer service waiting line?

---

**Next:** [Collection Class →](./01-Collection-Class-in-CSharp.md)
