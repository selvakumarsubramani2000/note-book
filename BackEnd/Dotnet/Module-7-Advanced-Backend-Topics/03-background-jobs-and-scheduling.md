# ⏱️ Background Jobs & Scheduling — Work Beyond a Single HTTP Request

> **Trainer's Note:** HTTP requests should stay **short**. Long work (emails, PDF generation, nightly cleanup, retries) belongs in **background processes**. ASP.NET Core gives you `IHostedService` / `BackgroundService`; serious systems often add Hangfire or Quartz.NET for queues and schedules.

---

## 📑 Table of Contents
1. [Why Background Work?](#1-why-background-work)
2. [Request Thread vs Background Work](#2-request-thread-vs-background-work)
3. [IHostedService Basics](#3-ihostedservice-basics)
4. [BackgroundService Pattern](#4-backgroundservice-pattern)
5. [DI Scopes Inside Background Services](#5-di-scopes-inside-background-services)
6. [Useful Worker Examples](#6-useful-worker-examples)
7. [Graceful Shutdown](#7-graceful-shutdown)
8. [Job Queues vs In-Process Loops](#8-job-queues-vs-in-process-loops)
9. [Hangfire Overview](#9-hangfire-overview)
10. [Quartz.NET Overview](#10-quartznet-overview)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. Why Background Work?

| Bad in the HTTP request | Better as background job |
|-------------------------|--------------------------|
| Generate 10k row export | Queue export → email link later |
| Call slow third-party with retries | Worker retries with backoff |
| Nightly purge of old logs | Scheduled job at 02:00 |
| Resize uploaded images | Process after upload returns quickly |
| Send order confirmation email | Fire-and-forget queue (still tracked!) |

```
Client                API                    Worker
  │  POST /orders       │                      │
  │ ──────────────────► │ save order           │
  │ ◄──── 201 quickly   │ enqueue "SendEmail"  │
  │                     │ ───────────────────► │
  │                     │                      │ send email / retry
```

Goal: **fast API responses** + **reliable async processing**.

---

## 2. Request Thread vs Background Work

```
HTTP request lifetime:
  start → controller/service → response → end
  (scoped DbContext disposed here)

Background work lifetime:
  runs on host process continuously or until job finishes
  must create its own DI scopes
```

Never do this:
```csharp
// ❌ fire-and-forget on request services without care
_ = Task.Run(async () =>
{
    await _db.SaveChangesAsync(); // scoped DbContext may be disposed!
});
```

Use hosted services or a real queue that outlives the request safely.

---

## 3. IHostedService Basics

`IHostedService` hooks into the generic host lifetime.

```csharp
public interface IHostedService
{
    Task StartAsync(CancellationToken cancellationToken);
    Task StopAsync(CancellationToken cancellationToken);
}
```

### Minimal custom hosted service
```csharp
public class StartupWarmupService : IHostedService
{
    private readonly ILogger<StartupWarmupService> _logger;

    public StartupWarmupService(ILogger<StartupWarmupService> logger)
        => _logger = logger;

    public Task StartAsync(CancellationToken cancellationToken)
    {
        _logger.LogInformation("Warmup checks running...");
        return Task.CompletedTask;
    }

    public Task StopAsync(CancellationToken cancellationToken)
    {
        _logger.LogInformation("Warmup service stopping");
        return Task.CompletedTask;
    }
}

// Program.cs
builder.Services.AddHostedService<StartupWarmupService>();
```

Most long-running loops use **`BackgroundService`** instead of raw `IHostedService`.

---

## 4. BackgroundService Pattern

`BackgroundService` is an abstract class with `ExecuteAsync`.

```csharp
public class QueuedWorkProbeService : BackgroundService
{
    private readonly ILogger<QueuedWorkProbeService> _logger;

    public QueuedWorkProbeService(ILogger<QueuedWorkProbeService> logger)
        => _logger = logger;

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("Worker started");

        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                // do periodic work
                _logger.LogDebug("Worker heartbeat");
            }
            catch (Exception ex) when (ex is not OperationCanceledException)
            {
                _logger.LogError(ex, "Worker iteration failed");
            }

            await Task.Delay(TimeSpan.FromSeconds(30), stoppingToken);
        }

        _logger.LogInformation("Worker stopping");
    }
}

builder.Services.AddHostedService<QueuedWorkProbeService>();
```

### Rules
1. Honor `stoppingToken`  
2. Catch per-iteration errors so one failure doesn’t kill the loop forever (unless you want crash)  
3. Don’t block with heavy sync I/O  
4. Use delays/timeouts thoughtfully  

---

## 5. DI Scopes Inside Background Services

Hosted services are usually **singletons**.  
`DbContext` is **scoped**.  
→ **Do not** inject `DbContext` directly into a hosted service constructor for repeated work.

### Correct pattern: `IServiceScopeFactory`
```csharp
public class OrderCleanupService : BackgroundService
{
    private readonly IServiceScopeFactory _scopeFactory;
    private readonly ILogger<OrderCleanupService> _logger;

    public OrderCleanupService(
        IServiceScopeFactory scopeFactory,
        ILogger<OrderCleanupService> logger)
    {
        _scopeFactory = scopeFactory;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            await using var scope = _scopeFactory.CreateAsyncScope();
            var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();

            var old = await db.Orders
                .Where(o => o.Status == "Draft" && o.CreatedAtUtc < DateTime.UtcNow.AddDays(-7))
                .ToListAsync(stoppingToken);

            if (old.Count > 0)
            {
                db.Orders.RemoveRange(old);
                await db.SaveChangesAsync(stoppingToken);
                _logger.LogInformation("Removed {Count} draft orders", old.Count);
            }

            await Task.Delay(TimeSpan.FromHours(1), stoppingToken);
        }
    }
}
```

```
HostedService (singleton)
   loop
     create scope
       resolve scoped services/DbContext
       work
     dispose scope
```

---

## 6. Useful Worker Examples

### A) Channel-based in-memory queue (simple)
```csharp
public interface IBackgroundTaskQueue
{
    ValueTask QueueAsync(Func<IServiceProvider, CancellationToken, ValueTask> workItem);
    ValueTask<Func<IServiceProvider, CancellationToken, ValueTask>> DequeueAsync(CancellationToken ct);
}
```

API enqueues work; `BackgroundService` dequeues and runs with a fresh scope.

Good for demos/single node. Messages die if process crashes — not durable.

### B) Periodic schedule with `PeriodicTimer`
```csharp
protected override async Task ExecuteAsync(CancellationToken stoppingToken)
{
    using var timer = new PeriodicTimer(TimeSpan.FromMinutes(5));
    while (await timer.WaitForNextTickAsync(stoppingToken))
    {
        await DoWorkAsync(stoppingToken);
    }
}
```

### C) Email sender worker
```
API writes EmailOutbox row (Pending)
Worker polls outbox → sends → marks Sent/Failed
```
Outbox pattern = reliable alternative to pure fire-and-forget.

---

## 7. Graceful Shutdown

When Kestrel/host stops:
1. `stoppingToken` cancels  
2. `StopAsync` runs  
3. In-flight work should finish or cancel quickly  

```csharp
protected override async Task ExecuteAsync(CancellationToken stoppingToken)
{
    try
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            await ProcessOnceAsync(stoppingToken);
        }
    }
    catch (OperationCanceledException) when (stoppingToken.IsCancellationRequested)
    {
        // expected on shutdown
    }
}
```

Don’t ignore cancellation and keep writing after host teardown.

Also configure shutdown timeout in host options when needed for longer jobs (careful on rolling deploys).

---

## 8. Job Queues vs In-Process Loops

| Approach | Durable? | Multi-node safe? | Best for |
|----------|----------|------------------|----------|
| `BackgroundService` loop | Only if you persist work (e.g. outbox table) | Possible with locking/leadership care | Simple periodic tasks |
| In-memory channel queue | No | No | Single instance demos |
| **Hangfire / queue products** | Yes (with storage) | Yes | Retries, dashboards, jobs |
| **Quartz.NET** | Yes (with ADO store) | Yes with clustering | Complex schedules/cron |
| Cloud queues (SQS, Azure Queue/Service Bus) | Yes | Yes | Cloud-native scale |

```
Production mental model:

  API persists intent (DB row / queue message)
  Worker processes intent with retries
  Poison messages isolated after N failures
```

---

## 9. Hangfire Overview

**Hangfire** is a popular library for background jobs in .NET with:
- fire-and-forget jobs  
- delayed jobs  
- recurring jobs  
- dashboard  
- retries  
- SQL Server/Redis storage options  

> Install only with approval if needed (`Hangfire.AspNetCore`, storage package).

### Conceptual usage
```csharp
// fire-and-forget
BackgroundJob.Enqueue<IEmailSender>(x => x.SendOrderEmailAsync(orderId));

// delayed
BackgroundJob.Schedule<IReportService>(
    x => x.BuildDailyReportAsync(),
    TimeSpan.FromHours(1));

// recurring
RecurringJob.AddOrUpdate<ICleanupService>(
    "purge-drafts",
    x => x.PurgeAsync(),
    Cron.Daily);
```

### Why teams like it
| Feature | Benefit |
|---------|---------|
| Dashboard | See succeeded/failed jobs |
| Automatic retries | Transient failures |
| Persistence | Survives app restarts |
| Recurring cron | Replaces DIY timers for many cases |

Still need care: job serialization, idempotent handlers, security of dashboard.

---

## 10. Quartz.NET Overview

**Quartz.NET** is a battle-tested scheduler (cron triggers, calendars, clustered scheduling).

| Concept | Meaning |
|---------|---------|
| Job | Unit of work class |
| Trigger | When the job runs (cron, simple intervals) |
| Scheduler | Engine that runs jobs |
| JobStore | RAM or database for clustering |

### Cron example idea
```
0 0 2 * * ?   → every day at 02:00:00
0 */15 * * * ? → every 15 minutes
```

### When Quartz fits
- Complex calendaring  
- Enterprise schedule definitions  
- Multiple job types with different triggers  
- Clustered schedulers with DB store  

### Hangfire vs Quartz (beginner view)
| | Hangfire | Quartz.NET |
|--|----------|------------|
| API style | Very ergonomic queues + dashboard | Scheduler-first, powerful |
| Recurring jobs | Easy | Excellent cron |
| Dashboard | Built-in classic strength | Needs custom or tools |
| Learning curve | Friendlier for many web teams | Steeper, very flexible |

Either can be production-grade. Pick based on team skills and needs; outbox + worker is a third valid pattern without extra productized job frameworks.

---

## 11. Knowledge Check

**Q1.** Why not run a 2-minute PDF export entirely inside the HTTP request?  
**Q2.** What is `BackgroundService`?  
**Q3.** Why shouldn’t you inject scoped `DbContext` into a singleton worker’s constructor for loop work?  
**Q4.** How do you resolve scoped services correctly in a worker?  
**Q5.** What makes an in-memory queue unsafe for critical emails?  
**Q6.** Name one Hangfire strength.  
**Q7.** Name one Quartz.NET strength.

### Mini practice
1. Create a `BackgroundService` that logs a heartbeat every 30 seconds  
2. Add a cleanup worker using `IServiceScopeFactory` + DbContext  
3. Stop the app and confirm cancellation is honored  
4. Design (on paper) an email outbox table flow  
5. Skim Hangfire or Quartz docs and write where you’d use each  

### Answers (short)
1. Slow UX, timeouts, fragile cancellation, poor scalability  
2. Base class for long-running hosted background loops  
3. Lifetime mismatch — captive dependency / disposed context issues  
4. `IServiceScopeFactory.CreateAsyncScope()` per iteration/job  
5. Process crash loses queued work; not shared across nodes  
6. Dashboard, retries, easy enqueue API…  
7. Flexible cron/scheduling, clustering job store…  

---

## ✅ What You Should Feel Confident About

- [ ] Explain when work should leave the HTTP request  
- [ ] Implement `BackgroundService` loops safely  
- [ ] Use `IServiceScopeFactory` for scoped DbContext/services  
- [ ] Honor shutdown cancellation  
- [ ] Contrast in-process workers vs Hangfire/Quartz/queues  
- [ ] Sketch a durable outbox/queue approach  

**Previous:** [02-caching.md](./02-caching.md)  
**Next:** [04-file-handling.md](./04-file-handling.md) — uploads, validation, storage, and downloads.
