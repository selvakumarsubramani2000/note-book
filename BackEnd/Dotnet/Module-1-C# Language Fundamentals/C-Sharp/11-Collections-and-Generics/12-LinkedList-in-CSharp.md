# 🔗 LinkedList in C#

> **Trainer's Note:** LinkedList stores items as connected nodes. Great when you insert/remove around a known node often. For simple indexed lists, `List<T>` is usually enough.

---

## 📑 Table of Contents
1. [What is LinkedList?](#1-what-is-linkedlist)
2. [Basic Usage](#2-basic-usage)
3. [Node Insert / Remove](#3-node-insert--remove)
4. [LinkedList vs List](#4-linkedlist-vs-list)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is LinkedList?

`LinkedList<T>` is a chain of nodes. Each node knows previous and next.

- Namespace: `System.Collections.Generic`
- Fast insert/remove near a known node
- No heavy array shifting like middle list inserts
- No direct fast random index model like `list[1000]`

### Real-world analogy
```
LinkedList = train compartments
Each coach linked to next and previous
Easy to attach/remove a coach if you hold that link
Finding coach number 100 still needs walking the chain
```

---

## 2. Basic Usage

```csharp
using System.Collections.Generic;

LinkedList<string> train = new LinkedList<string>();
train.AddLast("Engine");
train.AddLast("CoachA");
train.AddLast("CoachB");
train.AddFirst("Inspector");

foreach (string c in train)
    Console.WriteLine(c);
```

### Ends
```csharp
Console.WriteLine(train.First?.Value);
Console.WriteLine(train.Last?.Value);
Console.WriteLine(train.Count);
```

---

## 3. Node Insert / Remove

```csharp
LinkedListNode<string>? nodeA = train.Find("CoachA");
if (nodeA != null)
{
    train.AddAfter(nodeA, "CoachA2");
    train.AddBefore(nodeA, "CoachA0");
}

train.Remove("CoachB");
train.RemoveFirst();
train.RemoveLast();
```

### Walk node by node
```csharp
LinkedListNode<string>? current = train.First;
while (current != null)
{
    Console.WriteLine(current.Value);
    current = current.Next;
}
```

### Useful members
| Member | Meaning |
|--------|---------|
| `AddFirst` / `AddLast` | insert ends |
| `AddBefore` / `AddAfter` | insert relative to node |
| `Remove` / `RemoveFirst` / `RemoveLast` | delete |
| `Find` / `FindLast` | locate node |
| `First` / `Last` | end nodes |
| `Count` | size |
| `Clear` | empty |

---

## 4. LinkedList vs List

| Point | List&lt;T&gt; | LinkedList&lt;T&gt; |
|-------|---------------|---------------------|
| Access by index | excellent | weak/not main design |
| Add at end | excellent | good |
| Insert/remove middle with node ref | costlier shifts | efficient nearby edits |
| Memory layout | array-backed | node objects + links |
| Everyday default | **yes** | special cases |

### Beginner rule
```
Most business lists                     → List<T>
Playlist/editor chain with many splices → LinkedList<T>
Latest-first                            → Stack
Oldest-first                            → Queue
```

### Good LinkedList cases
- Music playlist reorder operations
- Navigation sequences
- Custom buffers where you hold node references

---

## 5. Knowledge Check

1. What does each LinkedList node store besides value?
2. Difference between `AddLast` and `AddAfter`?
3. How do you find a node by value?
4. When is List better than LinkedList?
5. Write a LinkedList with 3 cities and print them.

---

**Previous:** [← Queue](./11-Queue-in-CSharp.md)

🎉 **Completed!** You now have a full separate Collections & Generics track with one clear file for every major collection type.
