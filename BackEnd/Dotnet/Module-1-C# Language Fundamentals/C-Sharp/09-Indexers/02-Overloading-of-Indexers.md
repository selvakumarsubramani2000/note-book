# 🔁 C# — Overloading of Indexers

> **Trainer's Note:** Indexer overloading means defining more than one indexer in the same class with different parameter lists — just like method overloading.

---

## 📑 Table of Contents
1. [What is Indexer Overloading?](#1-what-is-indexer-overloading)
2. [Overloaded Indexers Example](#2-overloaded-indexers-example)
3. [Overloading Rules](#3-overloading-rules)
4. [Knowledge Check](#4-knowledge-check)

---

## 1. What is Indexer Overloading?

**Indexer overloading** = multiple `this[...]` members in one class, each with a different parameter list.

### Real-world analogy
```
Same shop counter, different ways to find an item:
  shop[0]        → by shelf number
  shop["Pen"]    → by item name
  shop[2, 3]     → by row and column
```

---

## 2. Overloaded Indexers Example

```csharp
public class ProductShelf
{
    private string[] byIndex = new string[5];
    private Dictionary<string, string> byName = new();
    private string[,] grid = new string[3, 3];

    // Overload 1: int index
    public string this[int index]
    {
        get => byIndex[index];
        set => byIndex[index] = value;
    }

    // Overload 2: string key
    public string this[string name]
    {
        get => byName.ContainsKey(name) ? byName[name] : "N/A";
        set => byName[name] = value;
    }

    // Overload 3: two ints (multidimensional)
    public string this[int row, int col]
    {
        get => grid[row, col];
        set => grid[row, col] = value;
    }
}
```

### Use all overloads
```csharp
ProductShelf shelf = new ProductShelf();

shelf[0] = "Notebook";          // int indexer
shelf["Pen"] = "Blue ink pen";  // string indexer
shelf[1, 2] = "Marker";         // 2D indexer

Console.WriteLine(shelf[0]);     // Notebook
Console.WriteLine(shelf["Pen"]); // Blue ink pen
Console.WriteLine(shelf[1, 2]);  // Marker
```

---

## 3. Overloading Rules

| Rule | Meaning |
|------|---------|
| Different parameter list | Number/type of parameters must differ |
| Same class | Multiple `this[...]` indexers allowed |
| Return type alone is not enough | Cannot overload only by return type |
| Compiler picks match | Based on arguments you pass in `obj[...]` |

### Valid vs invalid
```csharp
// ✅ Valid overloads
this[int i]
this[string key]
this[int r, int c]

// ❌ Invalid — only return type differs
// public int this[int i] { get; set; }
// public string this[int i] { get; set; }
```

### Beginner tip
```
Need one access style only     → one indexer is enough
Need int + name + grid access  → overload indexers carefully
Keep each overload's purpose clear
```

---

## 4. Knowledge Check

1. What does indexer overloading mean?
2. Can two indexers differ only by return type? Why?
3. Write three overload signatures: int, string, and 2D int.
4. Which overload is called for `shelf["Pen"]`?

---

**Previous:** [← Multidimensional Indexers](./01-Multidimensional-Indexers.md)  
**Next:** [Properties in C# →](../Properties/00-Properties-in-CSharp.md)

🎉 **Indexers track complete!** Basics, multi-dimension access, and overloading are now separate clear guides.
