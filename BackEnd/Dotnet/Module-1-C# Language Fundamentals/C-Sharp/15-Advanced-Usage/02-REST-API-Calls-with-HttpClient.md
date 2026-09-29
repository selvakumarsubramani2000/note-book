# 🌐 REST API Calls with HttpClient in C#

> **Trainer's Note:** `HttpClient` is the standard way to call REST APIs from .NET apps. Learn GET/POST with JSON first — that covers most real work.

---

## 📑 Table of Contents
1. [What is HttpClient?](#1-what-is-httpclient)
2. [GET JSON Example](#2-get-json-example)
3. [POST JSON Example](#3-post-json-example)
4. [Best Practices](#4-best-practices)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is HttpClient?

`HttpClient` sends HTTP requests and receives responses.

```csharp
using var client = new HttpClient();
string result = await client.GetStringAsync("https://api.example.com/health");
```

### Real-world analogy
```
HttpClient = courier service
  GET  = ask "give me resource"
  POST = deliver a package (create data)
  PUT/PATCH = update package details
  DELETE = request removal
```

Namespace: `System.Net.Http`  
JSON body handling often uses `System.Text.Json`.

---

## 2. GET JSON Example

```csharp
using System.Net.Http.Json;

public class Todo
{
    public int Id { get; set; }
    public string Title { get; set; } = "";
    public bool Completed { get; set; }
}

using HttpClient client = new HttpClient
{
    BaseAddress = new Uri("https://jsonplaceholder.typicode.com/")
};

Todo? todo = await client.GetFromJsonAsync<Todo>("todos/1");
Console.WriteLine($"{todo?.Id}: {todo?.Title}");
```

### Manual style
```csharp
HttpResponseMessage response = await client.GetAsync("todos/1");
response.EnsureSuccessStatusCode();
string json = await response.Content.ReadAsStringAsync();
```

---

## 3. POST JSON Example

```csharp
using System.Net.Http.Json;

var newTodo = new { title = "Learn HttpClient", completed = false };
HttpResponseMessage response =
    await client.PostAsJsonAsync("todos", newTodo);

response.EnsureSuccessStatusCode();
string body = await response.Content.ReadAsStringAsync();
Console.WriteLine(body);
```

### Headers idea
```csharp
client.DefaultRequestHeaders.Add("Accept", "application/json");
// Authentication headers are common in real apps (Bearer tokens, etc.)
```

---

## 4. Best Practices

| Do | Why |
|----|-----|
| Prefer async calls (`await`) | non-blocking I/O |
| Reuse `HttpClient` (or `IHttpClientFactory`) | avoid socket exhaustion |
| Check status codes | fail clearly on API errors |
| Use DTOs + JSON helpers | clean request/response mapping |
| Set timeout / cancellation when needed | resilient apps |

### Beginner warning
Creating `new HttpClient()` for every tiny call in large systems is a bad habit.  
For learning console samples, one client is fine. In ASP.NET apps, prefer **IHttpClientFactory**.

### Error handling sketch
```csharp
try
{
    var data = await client.GetFromJsonAsync<Todo>("todos/1");
}
catch (HttpRequestException ex)
{
    Console.WriteLine($"HTTP failed: {ex.Message}");
}
```

---

## 5. Knowledge Check

1. What is the difference between GET and POST?
2. Which package helpers help with JSON on HttpClient (`GetFromJsonAsync`)?
3. Why should HttpClient be reused?
4. Write a mental model of calling an API and mapping JSON to a class.

---

**Previous:** [← Serialization](./01-Data-Serialization-and-Deserialization.md)  
**Next:** [Dependency Injection →](./03-Dependency-Injection.md)
