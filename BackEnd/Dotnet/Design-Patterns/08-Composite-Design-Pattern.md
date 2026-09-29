# 🌳 Composite Design Pattern (C# / .NET)

> **Trainer's Note:** Composite is perfect for **tree-like data** — folders/files, menus/submenus, org charts. The magic: you treat a single item and a whole group the SAME way.

---

## 📑 Table of Contents
1. [What is the Composite Pattern?](#1-what-is-the-composite-pattern)
2. [Real-World Analogy](#2-real-world-analogy)
3. [C# Implementation](#3-c-implementation)
4. [Where Used in Real .NET Projects](#4-where-used-in-real-net-projects)
5. [Common Mistakes](#5-common-mistakes)

---

## 1. What is the Composite Pattern?

**Composite** lets you treat **individual objects** and **groups (compositions) of objects** through the **same interface** — so client code doesn't need to know if it's dealing with one item or a whole tree of items.

### 🎯 The Problem It Solves

```
File system has FILES and FOLDERS.
A folder can contain files AND other folders (nested infinitely).

❌ Without Composite: you write separate code to handle
   "a single file" vs "a folder containing many files"
   → lots of if/else, type-checking, recursive special cases

✅ With Composite: both File and Folder implement the SAME
   interface (e.g., GetSize()), so your code just calls
   item.GetSize() without caring if it's a file or folder.
```

---

## 2. Real-World Analogy

### 📁 Windows File Explorer

```
Root Folder
├── Report.docx           (single File)
├── Photos (Folder)
│   ├── vacation.jpg       (single File)
│   └── family.jpg         (single File)
└── Projects (Folder)
    └── Notes (Folder)
        └── todo.txt        (single File)

When you check "Folder Properties → Size", Windows adds up
sizes of ALL files inside, no matter how deeply nested.
It treats a FILE and a FOLDER-FULL-OF-FILES using the SAME
"give me your size" operation.
```

**Composite Pattern = Build tree structures where individual objects ("leaves") and groups of objects ("composites") are treated uniformly through a common interface.**

---

## 3. C# Implementation

```csharp
// Step 1: Common interface for both File (leaf) and Folder (composite)
public interface IFileSystemItem
{
    string Name { get; }
    long GetSize();      // in KB
    void Display(int depth = 0);
}

// Step 2: Leaf - a single File (cannot contain other items)
public class FileItem : IFileSystemItem
{
    public string Name { get; }
    private readonly long _sizeKb;

    public FileItem(string name, long sizeKb)
    {
        Name = name;
        _sizeKb = sizeKb;
    }

    public long GetSize() => _sizeKb;

    public void Display(int depth = 0)
    {
        Console.WriteLine($"{new string('-', depth * 2)} 📄 {Name} ({_sizeKb} KB)");
    }
}

// Step 3: Composite - a Folder that can contain Files AND other Folders
public class FolderItem : IFileSystemItem
{
    public string Name { get; }
    private readonly List<IFileSystemItem> _children = new();

    public FolderItem(string name)
    {
        Name = name;
    }

    public void Add(IFileSystemItem item) => _children.Add(item);

    // Recursively sums size of ALL children (files AND sub-folders)
    public long GetSize()
    {
        long total = 0;
        foreach (var child in _children)
            total += child.GetSize();   // Works for BOTH File and Folder!
        return total;
    }

    public void Display(int depth = 0)
    {
        Console.WriteLine($"{new string('-', depth * 2)} 📁 {Name}/");
        foreach (var child in _children)
            child.Display(depth + 1);   // Recursion handles nested folders
    }
}
```

### Using It:

```csharp
var root = new FolderItem("Root");
var photos = new FolderItem("Photos");
var projects = new FolderItem("Projects");
var notes = new FolderItem("Notes");

photos.Add(new FileItem("vacation.jpg", 2500));
photos.Add(new FileItem("family.jpg", 3200));
notes.Add(new FileItem("todo.txt", 5));
projects.Add(notes);

root.Add(new FileItem("Report.docx", 800));
root.Add(photos);
root.Add(projects);

root.Display();
// 📁 Root/
// -- 📄 Report.docx (800 KB)
// -- 📁 Photos/
// ---- 📄 vacation.jpg (2500 KB)
// ---- 📄 family.jpg (3200 KB)
// -- 📁 Projects/
// ---- 📁 Notes/
// ------ 📄 todo.txt (5 KB)

Console.WriteLine($"Total size: {root.GetSize()} KB");
// Total size: 6505 KB  (calculated recursively, no matter how deep!)
```

### 💡 Key Idea
> Client code calls `root.GetSize()` **without knowing or caring** whether `root` contains a single file or a deeply nested tree of folders. `FileItem` (leaf) and `FolderItem` (composite) both honor the same `IFileSystemItem` contract.

---

## 4. Where Used in Real .NET Projects

| Real .NET Example | Why Composite? |
|--------------------|------------------|
| WPF/WinForms UI controls (`Control` containing child `Controls`) | A `Panel` (composite) can contain `Button`s (leaves) or other `Panel`s |
| `System.Windows.Forms.Control.Controls` collection | Treats a single control and a container of controls uniformly |
| Menu / Sub-menu structures | A `MenuItem` can contain other `MenuItem`s (nested menus) |
| Organization chart / Category-Subcategory trees | Employee (leaf) vs Manager with a team (composite) |

---

## 5. Common Mistakes

| Mistake | Why It's Wrong |
|---------|-----------------|
| ❌ Adding "Add()/Remove()" methods to the leaf class too | Leaf nodes (like `FileItem`) shouldn't pretend to hold children — keep the interface focused on shared operations only |
| ❌ Using `if (item is FolderItem)` checks in client code | Defeats the purpose — client code should treat all items the same via the interface |
| ❌ Forgetting recursion in the composite's methods | `GetSize()`/`Display()` must call the same method on each child to handle deep nesting |
| ❌ Using Composite for flat, non-hierarchical data | If there's no real "tree" structure, Composite adds unnecessary complexity |

---

## ✅ Quick Recap

| Concept | Key Takeaway |
|---------|--------------|
| **Composite Pattern** | Treats individual objects and groups of objects through the same interface |
| **Real Analogy** | Windows folder containing files and other folders |
| **Key Benefit** | Simplifies client code when working with tree-like/nested structures |
| **Real Use Case** | UI control hierarchies, nested menus, file systems |

---

**Previous → [Bridge Design Pattern](./07-Bridge-Design-Pattern.md)**
**Next → [Decorator Design Pattern](./09-Decorator-Design-Pattern.md)**
