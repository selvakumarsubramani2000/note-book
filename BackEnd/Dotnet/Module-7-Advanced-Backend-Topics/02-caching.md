# ⚡ Caching — Faster Reads Without Always Hitting the Database

> **Trainer's Note:** Caching stores expensive results nearby for a while. Done well, APIs feel instant. Done poorly, users see **stale** or wrong data. Learn `IMemoryCache` first, then distributed Redis patterns and invalidation discipline.

---

## 📑 Table of Contents
1. [Why Cache?](#1-why-cache)
2. [Cache Placement in an API](#2-cache-placement-in-an-api)
3. [In-Memory Caching with IMemoryCache](#3-in-memory-caching-with-imemorycache)
4. [Absolute vs Sliding Expiration](#4-absolute-vs-sliding-expiration)
5. [Memory Pressure and Size Limits](#5-memory-pressure-and-size-limits)
6. [Distributed Caching Concepts](#6-distributed-caching-concepts)
7. [Redis as a Distributed Cache](#7-redis-as-a-distributed-cache)
8. [Cache Invalidation Patterns](#8-cache-invalidation-patterns)
9. [Stale Data and Consistency Pitfalls](#9-stale-data-and-consistency-pitfalls)
10. [What (Not) to Cache](#10-what-not-to-cache)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. Why Cache?

```
Without cache (every request):
  API → SQL → map DTO → response

With cache (hot path):
  API → memory/Redis hit → response
         ↘ miss → SQL → store in cache → response
```

| Benefit | Trade-off |
|---------|-----------|
| Lower DB load | Complexity |
| Lower latency | Possible stale reads |
| Smoother spikes | Memory/Redis cost |
| Protect slow dependencies | Invalidation bugs |

Cache is not free correctness — it is a **performance tool**.

---

## 2. Cache Placement in an API

Common layers:

| Layer | Example |
|-------|---------|
| Client/browser HTTP cache | `Cache-Control` on GET responses |
| CDN | Static/media |
| API output cache | Framework output caching |
| Application cache | `IMemoryCache` / Redis around services |
| Database | Query store, buffer pool (DB’s own) |

This file focuses on **application caching** inside ASP.NET Core services.

```
Controller → Service
               ├── try get cache
               ├── on miss: repository/DB
               └── set cache
```

---

## 3. In-Memory Caching with IMemoryCache

`IMemoryCache` stores data in the **current process memory**.

### Register
```csharp
builder.Services.AddMemoryCache();
```

### Basic usage
```csharp
public class ProductReadService
{
    private readonly IMemoryCache _cache;
    private readonly IProductRepository _repo;

    public ProductReadService(IMemoryCache cache, IProductRepository repo)
    {
        _cache = cache;
        _repo = repo;
    }

    public async Task<ProductDto?> GetAsync(int id, CancellationToken ct)
    {
        var key = $"product:{id}";

        if (_cache.TryGetValue(key, out ProductDto? cached) && cached is not null)
            return cached;

        var product = await _repo.GetDtoAsync(id, ct);
        if (product is null) return null;

        _cache.Set(key, product, TimeSpan.FromMinutes(5));
        return product;
    }
}
```

### GetOrCreateAsync pattern
```csharp
var dto = await _cache.GetOrCreateAsync($"product:{id}", async entry =>
{
    entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5);
    entry.Size = 1; // if size limit enabled
    return await _repo.GetDtoAsync(id, ct);
});
```

---

## 4. Absolute vs Sliding Expiration

| Type | Behavior | Good for |
|------|----------|----------|
| **Absolute** | Expires at a fixed time after insert | Data that must refresh periodically |
| **Sliding** | Expires after idle period; each access resets idle timer | Hot keys that should live while actively used |

```csharp
var options = new MemoryCacheEntryOptions()
    .SetAbsoluteExpiration(TimeSpan.FromMinutes(10))
    .SetSlidingExpiration(TimeSpan.FromMinutes(2));

// Entry dies at absolute max 10 min,
// or earlier if not touched for 2 min.
_cache.Set(key, value, options);
```

### Mental model
```
Absolute:  created 12:00 → gone by 12:10 regardless of hits

Sliding:   last hit 12:07 + 2 min idle → gone 12:09
           (unless also capped by absolute)
```

You can combine both: sliding for activity, absolute as a hard ceiling.

---

## 5. Memory Pressure and Size Limits

In-process cache competes with your app for RAM.

### Set size limits
```csharp
builder.Services.AddMemoryCache(options =>
{
    options.SizeLimit = 1024; // abstract units you define
});

var entryOptions = new MemoryCacheEntryOptions
{
    Size = 1,
    AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5)
};
```

When over limit, cache evicts entries based on policy/priority/compaction.

### Priority
```csharp
entryOptions.SetPriority(CacheItemPriority.High);
```

| Priority | Meaning |
|----------|---------|
| Low | Evict first under pressure |
| Normal | Default |
| High | Keep longer |
| NeverRemove | Avoid unless expired/explicit remove (use carefully) |

### Callbacks
```csharp
entryOptions.RegisterPostEvictionCallback((key, value, reason, state) =>
{
    // logging/metrics: why was it removed?
});
```

### Multi-instance warning
```
Server A memory cache ≠ Server B memory cache

Load balancer:
  request1 → A (warm cache)
  request2 → B (cold cache)
```
For multi-node farms, use **distributed cache** for shared hot data.

---

## 6. Distributed Caching Concepts

**Distributed cache** = external store shared by all API instances.

```
┌─────────┐   ┌─────────┐   ┌─────────┐
│ Api #1  │   │ Api #2  │   │ Api #3  │
└────┬────┘   └────┬────┘   └────┬────┘
     │             │             │
     └─────────────┼─────────────┘
                   ▼
              Redis / NCache / SQL
```

### IDistributedCache abstraction
ASP.NET Core provides `IDistributedCache` with implementations:
- Redis  
- SQL Server  
- NCache  
- etc.

Values are typically **byte[]** / strings — you serialize DTOs (JSON).

---

## 7. Redis as a Distributed Cache

**Redis** is an in-memory data store commonly used as a distributed cache.

> Install packages only with your approval if needed, e.g.:
```bash
dotnet add package Microsoft.Extensions.Caching.StackExchangeRedis
```

### Configure
```csharp
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = builder.Configuration.GetConnectionString("Redis");
    options.InstanceName = "Shop:"; // key prefix
});
```

```json
{
  "ConnectionStrings": {
    "Redis": "localhost:6379"
  }
}
```

### Usage
```csharp
public class ProductCache
{
    private readonly IDistributedCache _cache;

    public ProductCache(IDistributedCache cache) => _cache = cache;

    public async Task<ProductDto?> GetAsync(int id, CancellationToken ct)
    {
        var key = $"product:{id}";
        var json = await _cache.GetStringAsync(key, ct);
        if (json is null) return null;
        return JsonSerializer.Deserialize<ProductDto>(json);
    }

    public async Task SetAsync(ProductDto dto, CancellationToken ct)
    {
        var key = $"product:{dto.Id}";
        var json = JsonSerializer.Serialize(dto);
        await _cache.SetStringAsync(key, json, new DistributedCacheEntryOptions
        {
            AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5)
        }, ct);
    }

    public Task RemoveAsync(int id, CancellationToken ct)
        => _cache.RemoveAsync($"product:{id}", ct);
}
```

### Redis notes
- Network hop cost exists (still usually faster than heavy SQL)  
- Plan connection security (TLS, auth password, private network)  
- Keys need naming conventions and TTLs  
- Don’t store secrets in cache casually  

---

## 8. Cache Invalidation Patterns

**Invalidation** = making sure updates don’t leave old values forever.

### 1) Time-to-live (TTL) only
```
Set with 5 minute absolute expiry
Pros: simple
Cons: stale until TTL ends
```

### 2) Remove on write (explicit)
```csharp
public async Task UpdateAsync(Product product, CancellationToken ct)
{
    await _repo.UpdateAsync(product, ct);
    await _cache.RemoveAsync($"product:{product.Id}", ct);
    // optionally Remove list keys too
}
```

### 3) Versioned keys / cache busting
```
product:42:v=18
When product updates, bump version (or include updatedAt in key strategy)
```

### 4) Cache-aside (lazy load) — most common
```
Read:  get cache → miss → DB → set cache
Write: update DB → invalidate key
```

### 5) Write-through (less common beginner)
```
Write updates DB and cache together
```

### List/query keys are hard
```
product:42                         easy to invalidate
products:search=phone&page=2       many variants — hard
```
Strategies: short TTL for query lists, or invalidate known prefixes carefully, or cache only single-item reads.

---

## 9. Stale Data and Consistency Pitfalls

| Problem | Symptom | Mitigation |
|---------|---------|------------|
| Stale read | UI shows old price after update | Invalidate on write; shorter TTL |
| Cache stampede | Many misses hit DB together | Hard/soft timeouts, locks, stampede protection |
| Partial invalidation | Item updated, list still old | Invalidate related keys or short list TTL |
| Server-local inconsistency | Different nodes different data | Distributed cache |
| Caching authorized data under global key | User A sees User B data | Include user/tenant in key; never cache cross-user private data under shared keys |

### Private data key example
```csharp
// ✅
var key = $"orders:user:{userId}:page:{page}";

// ❌
var key = $"orders:page:{page}"; // mixes users
```

### Stampede sketch
When a hot key expires, 500 requests may rebuild it simultaneously. Advanced patterns: single-flight locks, early refresh, probabilistic early expiration.

---

## 10. What (Not) to Cache

### Good candidates
- Reference data (categories, countries)  
- Hot product details with acceptable staleness  
- Expensive computation results  
- Downstream API responses with TTL  

### Bad / careful candidates
- Highly transactional balances you must always get right  
- Per-request unique data  
- Huge payloads that thrash memory  
- Secrets  
- Personalized data without user in the key  

### HTTP caching tip
Even without Redis, correct `Cache-Control` on public GETs helps browsers/CDNs. Private authenticated responses usually `Cache-Control: no-store`.

---

## 11. Knowledge Check

**Q1.** What problem does caching solve, and what problem can it create?  
**Q2.** Absolute vs sliding expiration?  
**Q3.** Why can `IMemoryCache` be wrong for a 5-node web farm?  
**Q4.** What is cache-aside?  
**Q5.** How do you invalidate after updating a product?  
**Q6.** Why must user id appear in keys for private order lists?  
**Q7.** Name one good and one bad cache candidate.

### Mini practice
1. Add `IMemoryCache` around product-by-id reads (5 min absolute)  
2. Invalidate key on update/delete  
3. Log cache hit vs miss  
4. (Optional) Swap to `IDistributedCache` + Redis locally  
5. Demonstrate stale list data if only item keys are removed  

### Answers (short)
1. Faster/cheaper reads; can serve stale/wrong data  
2. Fixed lifetime vs idle-based extension  
3. Each process has separate memory — not shared  
4. Read cache, on miss load store and populate; write invalidates  
5. Remove `product:{id}` (and related keys) after successful DB update  
6. Prevent leaking another user’s data via shared key  
7. Good: categories; Bad: live bank balance without strict rules  

---

## ✅ What You Should Feel Confident About

- [ ] Use `IMemoryCache` with expiration options  
- [ ] Explain absolute vs sliding expiry  
- [ ] Account for memory pressure and multi-instance limits  
- [ ] Describe Redis/`IDistributedCache` role  
- [ ] Apply cache-aside + invalidate-on-write  
- [ ] Avoid stale/private-data key mistakes  

**Previous:** [01-logging-and-monitoring.md](./01-logging-and-monitoring.md)  
**Next:** [03-background-jobs-and-scheduling.md](./03-background-jobs-and-scheduling.md) — hosted services and job processors.
