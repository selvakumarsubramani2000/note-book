# 📄 JSON & XML Handling in C#

> **Trainer's Note:** Almost every modern app exchanges data as JSON. XML still appears in older systems and some enterprise APIs. Learn both at a practical level.

---

## 📑 Table of Contents
1. [JSON vs XML (Simple Picture)](#1-json-vs-xml-simple-picture)
2. [JSON with System.Text.Json](#2-json-with-systemtextjson)
3. [XML Basics in C#](#3-xml-basics-in-c)
4. [When to Use Which](#4-when-to-use-which)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. JSON vs XML (Simple Picture)

| Point | JSON | XML |
|-------|------|-----|
| Style | Lightweight text | Tag-based markup |
| Common in | REST APIs, web apps | Older SOAP/enterprise feeds |
| Readability | Usually easier | More verbose |
| .NET tools | `System.Text.Json`, Newtonsoft.Json | `XmlSerializer`, `XDocument` |

### Real-world analogy
```
JSON = short chat message with clear fields
XML  = formal stamped document with opening/closing seals
```

---

## 2. JSON with System.Text.Json

```csharp
using System.Text.Json;

public class Product
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
    public decimal Price { get; set; }
}

var product = new Product { Id = 1, Name = "Pen", Price = 10 };

// Object → JSON string
string json = JsonSerializer.Serialize(product);
// {"Id":1,"Name":"Pen","Price":10}

// JSON string → Object
Product? back = JsonSerializer.Deserialize<Product>(json);
Console.WriteLine(back?.Name);
```

### Useful options
```csharp
var options = new JsonSerializerOptions
{
    WriteIndented = true,
    PropertyNamingPolicy = JsonNamingPolicy.CamelCase
};

string pretty = JsonSerializer.Serialize(product, options);
```

### Read/Write JSON file
```csharp
await File.WriteAllTextAsync("product.json", json);
string fromFile = await File.ReadAllTextAsync("product.json");
var loaded = JsonSerializer.Deserialize<Product>(fromFile);
```

---

## 3. XML Basics in C#

### Serialize with XmlSerializer
```csharp
using System.Xml.Serialization;

var product = new Product { Id = 1, Name = "Pen", Price = 10 };
var serializer = new XmlSerializer(typeof(Product));

using var writer = new StreamWriter("product.xml");
serializer.Serialize(writer, product);
```

### Read XML with XDocument
```csharp
using System.Xml.Linq;

XDocument doc = XDocument.Load("product.xml");
string? name = doc.Root?.Element("Name")?.Value;
Console.WriteLine(name);
```

### Tiny XML shape idea
```xml
<Product>
  <Id>1</Id>
  <Name>Pen</Name>
  <Price>10</Price>
</Product>
```

---

## 4. When to Use Which

| Situation | Prefer |
|-----------|--------|
| New REST APIs | JSON |
| Browser/mobile clients | JSON |
| Existing enterprise XML contracts | XML |
| Config/data interchange with legacy systems | often XML |
| Human-edited lightweight files | JSON is usually simpler |

### Beginner tips
- Start with `System.Text.Json` for new .NET work
- Match property names carefully (case / naming policy)
- Validate input before deserialize when data is external
- Keep models simple for first learning

---

## 5. Knowledge Check

1. What is one main difference between JSON and XML?
2. Which namespace is used for `JsonSerializer`?
3. Write code idea: serialize a `Customer` object to JSON.
4. When might you still need XML?

---

**Next:** [Data Serialization & Deserialization →](./01-Data-Serialization-and-Deserialization.md)
