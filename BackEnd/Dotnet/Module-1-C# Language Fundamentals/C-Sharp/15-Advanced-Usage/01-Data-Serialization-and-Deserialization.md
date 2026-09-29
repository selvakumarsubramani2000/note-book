# 🔄 Data Serialization & Deserialization in C#

> **Trainer's Note:** Serialization converts objects to a storable/transferable format. Deserialization rebuilds objects back. This is the backbone of APIs, cache, and files.

---

## 📑 Table of Contents
1. [What is Serialization?](#1-what-is-serialization)
2. [Common Formats](#2-common-formats)
3. [Practical JSON Flow](#3-practical-json-flow)
4. [Important Design Tips](#4-important-design-tips)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is Serialization?

```
Object in memory  →  Serialization  →  JSON/XML/bytes
JSON/XML/bytes    →  Deserialization →  Object in memory
```

### Real-world analogy
```
Serialize   = pack clothes into a suitcase for travel
Deserialize = unpack suitcase back into wardrobe at destination
```

Why needed:
- send data over network
- save data to disk
- store temporary state

---

## 2. Common Formats

| Format | Typical use |
|--------|-------------|
| JSON | REST APIs, web apps |
| XML | legacy integrations |
| Binary | special performance/storage cases |

For most learners and business apps, start with **JSON**.

---

## 3. Practical JSON Flow

```csharp
using System.Text.Json;

public class OrderDto
{
    public int Id { get; set; }
    public string Customer { get; set; } = "";
    public decimal Total { get; set; }
}

// Serialize
var order = new OrderDto { Id = 10, Customer = "Anu", Total = 250 };
string json = JsonSerializer.Serialize(order);

// Deserialize
OrderDto? restored = JsonSerializer.Deserialize<OrderDto>(json);
```

### Collection example
```csharp
List<OrderDto> orders =
[
    new OrderDto { Id = 1, Customer = "A", Total = 100 },
    new OrderDto { Id = 2, Customer = "B", Total = 200 }
];

string jsonList = JsonSerializer.Serialize(orders);
var back = JsonSerializer.Deserialize<List<OrderDto>>(jsonList);
```

### From HTTP body idea
```csharp
// In an API, framework often deserializes JSON body into your model automatically
// Example mental model:
// POST /orders  + JSON body  =>  OrderDto model
```

---

## 4. Important Design Tips

| Tip | Why |
|-----|-----|
| Use DTOs for transport | Don't expose every domain detail |
| Keep models public get/set (or compatible shape) | serializer can map properties |
| Prefer clear property names | fewer mapping surprises |
| Handle null carefully | external data can be incomplete |
| Version contracts carefully | clients depend on shape |

### Serialize vs map
Serialization is about format conversion.  
If property names differ a lot, use options/attributes/mapping intentionally.

### Security note
Never deserialize untrusted data into dangerous polymorphic settings without care. Keep first examples simple and strict.

---

## 5. Knowledge Check

1. Define serialization and deserialization in one line each.
2. Why do APIs need serialization?
3. Deserialize JSON into `List<Product>` — what generic type do you pass?
4. Why use DTO classes for transfer?

---

**Previous:** [← JSON & XML Handling](./00-JSON-and-XML-Handling.md)  
**Next:** [REST API Calls with HttpClient →](./02-REST-API-Calls-with-HttpClient.md)
