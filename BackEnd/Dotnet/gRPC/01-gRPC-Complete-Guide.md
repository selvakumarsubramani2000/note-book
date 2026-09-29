# 📘 gRPC - Complete Developer Guide

## Why This Guide?
Your team is using **gRPC + REST Gateway** for migrating a legacy ASP application.
This guide explains what gRPC is, why your team chose it, and how it works with REST.

---

## Table of Contents
1. [What is gRPC?](#1-what-is-grpc)
2. [The Problem gRPC Solves](#2-the-problem-grpc-solves)
3. [How gRPC Works](#3-how-grpc-works)
4. [Protocol Buffers (Protobuf)](#4-protocol-buffers---the-language-of-grpc)
5. [gRPC Communication Types](#5-grpc-communication-types)
6. [gRPC vs REST - Detailed Comparison](#6-grpc-vs-rest---detailed-comparison)
7. [Why gRPC + REST Gateway?](#7-why-grpc--rest-gateway-for-your-migration)
8. [gRPC + REST Gateway Architecture](#8-grpc--rest-gateway---how-it-works)
9. [gRPC in ASP.NET Core (.NET)](#9-grpc-in-aspnet-core)
10. [Real-World Migration Pattern](#10-legacy-asp-migration-pattern)
11. [When NOT to Use gRPC](#11-when-not-to-use-grpc)
12. [Key Terminology](#12-key-terminology)

---

## 1. What is gRPC?

**gRPC** = **g**oogle **R**emote **P**rocedure **C**all

gRPC is a modern, high-performance framework for building APIs. Instead of sending
HTTP requests like REST, gRPC lets you **call a function on a remote server as if
it were a local function call**.

```
Traditional REST:
  Client → HTTP POST /api/vendors/create (JSON body) → Server
  Client ← HTTP 200 (JSON response) ← Server

gRPC:
  Client → vendorService.CreateVendor(request) → Server
  Client ← VendorResponse ← Server
  (Feels like calling a local function!)
```

### Who Created It?
- Built by **Google** in 2015 (internally used since 2001 as "Stubby")
- Now an open-source project under **CNCF** (Cloud Native Computing Foundation)
- Used by: Google, Netflix, Slack, Microsoft, Dropbox, Cisco, and many more

### Key Features at a Glance:
```
✅ Built on HTTP/2          → Faster than REST (HTTP/1.1)
✅ Uses Protocol Buffers    → Binary format (smaller & faster than JSON)
✅ Strongly typed contracts → .proto files define the API
✅ Code generation          → Auto-generates client & server code
✅ Bi-directional streaming → Real-time data flow
✅ Language agnostic        → Works across C#, Java, Go, Python, etc.
```

---

## 2. The Problem gRPC Solves

### Why Not Just Use REST?

REST works great for many cases, but has limitations for **microservices and
high-performance internal communication**:

```
Problem 1: PERFORMANCE
━━━━━━━━━━━━━━━━━━━━━
REST: JSON is text-based → Large payloads, slow to parse
gRPC: Protobuf is binary → 5-10x smaller, 10x faster to parse

Example: A Vendor object
  JSON:  {"id":1,"vendorName":"Acme Corp","status":"Active"} = ~58 bytes
  Proto: [binary encoded] = ~20 bytes (65% smaller!)

Problem 2: NO CONTRACT ENFORCEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REST: Client guesses the API shape, Swagger helps but isn't enforced
gRPC: .proto file IS the contract → compiler catches mistakes

Problem 3: HTTP/1.1 LIMITATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REST: One request per connection, text headers repeated every time
gRPC: HTTP/2 multiplexing → many requests on ONE connection, compressed headers

Problem 4: NO STREAMING
━━━━━━━━━━━━━━━━━━━━━━━
REST: Request → Response (one shot). Need WebSockets for real-time
gRPC: Built-in streaming (server-push, client-push, bi-directional)
```

---

## 3. How gRPC Works

### The Flow:
```
Step 1: Define your API in a .proto file
         ↓
Step 2: Protobuf compiler (protoc) generates code
         ↓
Step 3: Server implements the generated interface
         ↓
Step 4: Client calls generated client stub
         ↓
Step 5: gRPC handles serialization, HTTP/2 transport, everything!
```

### Visual Architecture:
```
┌─────────────────┐                        ┌─────────────────┐
│   Client App    │                        │   Server App    │
│  (C#, Java...)  │                        │  (C#, Java...)  │
│                 │                        │                 │
│  ┌───────────┐  │      HTTP/2 +          │  ┌───────────┐  │
│  │ Generated │  │      Protobuf          │  │ Generated │  │
│  │  Client   │──┼──────────────────────▶ │  │  Server   │  │
│  │  Stub     │  │   Binary, Fast,        │  │  Base     │  │
│  │           │◀─┼──────────────────────  │  │  Class    │  │
│  └───────────┘  │   Multiplexed          │  └───────────┘  │
└─────────────────┘                        └─────────────────┘
        ▲                                          ▲
        │              ┌──────────┐                │
        └──────────────│  .proto  │────────────────┘
                       │   file   │
                       │ (shared) │
                       └──────────┘
```

### HTTP/2 - Why It Matters:
```
HTTP/1.1 (REST):                    HTTP/2 (gRPC):
┌──────────────────┐                ┌──────────────────┐
│ Request 1 ──────▶│                │ Req 1 ──────────▶│
│ Response 1 ◀─────│                │ Req 2 ──────────▶│
│ Request 2 ──────▶│                │ Req 3 ──────────▶│
│ Response 2 ◀─────│                │ Resp 2 ◀─────────│
│ Request 3 ──────▶│                │ Resp 1 ◀─────────│
│ Response 3 ◀─────│                │ Resp 3 ◀─────────│
└──────────────────┘                └──────────────────┘
Sequential (SLOW)                   Multiplexed (FAST)
One at a time                       All at once on 1 connection
```


---

## 4. Protocol Buffers - The Language of gRPC

Protocol Buffers (Protobuf) is the **serialization format** gRPC uses. Think of it
as a replacement for JSON, but binary (machine-readable, not human-readable).

### Example: Defining a Vendor Service

```protobuf
// File: vendor.proto
// This is the CONTRACT between client and server

syntax = "proto3";                    // Use Protobuf version 3
package vendordirectory;              // Namespace
option csharp_namespace = "VendorDirectory.Grpc";  // C# namespace

// ── Message Definitions (like C# classes) ──────────────────

// Request to create a vendor
message CreateVendorRequest {
    string vendor_name = 1;           // Field number 1 (not value!)
    string category = 2;              // Field number 2
    string email = 3;
    string state = 4;
    string phone = 5;
}

// Vendor response
message VendorResponse {
    int32 id = 1;
    string vendor_name = 2;
    string category = 3;
    string email = 4;
    string state = 5;
    string status = 6;
    string created_at = 7;
}

// Request with just an ID
message GetVendorRequest {
    int32 id = 1;
}

// List of vendors
message VendorListResponse {
    repeated VendorResponse vendors = 1;   // "repeated" = array/list
    int32 total_count = 2;
}

// Empty message (for requests with no parameters)
message Empty {}

// ── Service Definition (like a C# interface) ───────────────

service VendorService {
    // Unary RPCs (request → response, like REST)
    rpc CreateVendor (CreateVendorRequest) returns (VendorResponse);
    rpc GetVendor (GetVendorRequest) returns (VendorResponse);
    rpc ListVendors (Empty) returns (VendorListResponse);
    rpc UpdateVendor (UpdateVendorRequest) returns (VendorResponse);
    rpc DeleteVendor (GetVendorRequest) returns (Empty);
}
```

### 🔢 Field Numbers Are Important!
```protobuf
message VendorResponse {
    int32 id = 1;              // 1, 2, 3... are FIELD NUMBERS, not values!
    string vendor_name = 2;    // Used for binary encoding
    string category = 3;       // NEVER change a field number after deployment!
}

// ✅ Adding new fields is safe (backward compatible)
message VendorResponse {
    int32 id = 1;
    string vendor_name = 2;
    string category = 3;
    string website = 8;        // New field with NEW number → safe!
}

// ❌ NEVER reuse or change field numbers → breaks existing clients!
```

### Protobuf Data Types:
```
Protobuf Type    → C# Type        → SQL Server Type
─────────────────────────────────────────────────────
int32            → int             → INT
int64            → long            → BIGINT
float            → float           → REAL
double           → double          → FLOAT
bool             → bool            → BIT
string           → string          → NVARCHAR
bytes            → ByteString      → VARBINARY
repeated T       → RepeatedField<T>→ (list/array)
google.protobuf.Timestamp → DateTimeOffset → DATETIME2
```

### JSON vs Protobuf - Size Comparison:
```
JSON (REST):
{
  "id": 1,
  "vendorName": "Acme Corporation",
  "category": "Supplier",
  "status": "Active",
  "state": "NY",
  "email": "contact@acme.com"
}
≈ 156 bytes (text, human-readable)

Protobuf (gRPC):
08 01 12 10 41 63 6D 65 20 43 6F 72 70 6F 72 61
74 69 6F 6E 1A 08 53 75 70 70 6C 69 65 72 22 06
...
≈ 62 bytes (binary, ~60% smaller!)
```

---

## 5. gRPC Communication Types

gRPC supports **4 types** of communication — a major advantage over REST.

### Type 1: Unary RPC (Most Common - Like REST)
```
Client sends ONE request → Server sends ONE response

Client ──── Request ────▶ Server
Client ◀── Response ───── Server

Use: CRUD operations, simple queries
```
```protobuf
rpc GetVendor (GetVendorRequest) returns (VendorResponse);
```

### Type 2: Server Streaming
```
Client sends ONE request → Server sends MANY responses (stream)

Client ──── Request ──────────▶ Server
Client ◀── Response 1 ───────── Server
Client ◀── Response 2 ───────── Server
Client ◀── Response 3 ───────── Server
Client ◀── (stream complete) ── Server

Use: Large data exports, live feeds, real-time stock prices
```
```protobuf
rpc ListAllVendors (Empty) returns (stream VendorResponse);
```
```csharp
// C# Server - sending a stream
public override async Task ListAllVendors(Empty request,
    IServerStreamWriter<VendorResponse> responseStream, ServerCallContext context)
{
    var vendors = await _dbContext.Vendors.ToListAsync();
    foreach (var vendor in vendors)
    {
        await responseStream.WriteAsync(MapToResponse(vendor));
    }
}

// C# Client - consuming the stream
using var call = client.ListAllVendors(new Empty());
await foreach (var vendor in call.ResponseStream.ReadAllAsync())
{
    Console.WriteLine($"Received: {vendor.VendorName}");
}
```

### Type 3: Client Streaming
```
Client sends MANY requests → Server sends ONE response

Client ──── Request 1 ──▶ Server
Client ──── Request 2 ──▶ Server
Client ──── Request 3 ──▶ Server
Client ──── (done) ─────▶ Server
Client ◀── Response ───── Server

Use: Bulk upload vendors, file upload in chunks, sensor data
```
```protobuf
rpc BulkCreateVendors (stream CreateVendorRequest) returns (BulkResponse);
```

### Type 4: Bidirectional Streaming
```
Client and Server send streams SIMULTANEOUSLY

Client ──── Request 1 ──▶ Server
Client ◀── Response 1 ─── Server
Client ──── Request 2 ──▶ Server
Client ◀── Response 2 ─── Server

Use: Chat apps, real-time collaboration, multiplayer games
```
```protobuf
rpc VendorChat (stream ChatMessage) returns (stream ChatMessage);
```

### Summary:
```
┌─────────────────────┬─────────────────────────────────────────┐
│ Type                │ Use Case                                │
├─────────────────────┼─────────────────────────────────────────┤
│ Unary               │ CRUD operations, simple queries (90%)   │
│ Server Streaming    │ Large exports, live feeds, notifications│
│ Client Streaming    │ Bulk uploads, file uploads              │
│ Bidirectional       │ Chat, real-time sync, gaming            │
└─────────────────────┴─────────────────────────────────────────┘
```

---

## 6. gRPC vs REST - Detailed Comparison

This is the KEY section to understand why your team chose gRPC.

```
┌──────────────────────┬──────────────────────────┬──────────────────────────┐
│ Feature              │ REST                     │ gRPC                     │
├──────────────────────┼──────────────────────────┼──────────────────────────┤
│ Protocol             │ HTTP/1.1 (mostly)        │ HTTP/2                   │
│ Data Format          │ JSON (text)              │ Protobuf (binary)        │
│ Payload Size         │ Large (verbose)          │ Small (~60% less)        │
│ Speed                │ Slower                   │ 5-10x faster             │
│ API Contract         │ Swagger/OpenAPI (opt.)   │ .proto file (required)   │
│ Code Generation      │ Optional (tools needed)  │ Built-in (protoc)        │
│ Streaming            │ Not native (WebSocket)   │ Built-in (4 types)       │
│ Browser Support      │ ✅ Full support          │ ❌ Limited (needs proxy) │
│ Human Readable       │ ✅ JSON is readable      │ ❌ Binary, not readable  │
│ Caching              │ ✅ HTTP caching          │ ❌ No built-in caching   │
│ Tooling              │ Postman, curl, browser   │ grpcurl, BloomRPC        │
│ Learning Curve       │ Easy                     │ Moderate                 │
│ Best For             │ Public APIs, Web apps    │ Microservices, Internal  │
└──────────────────────┴──────────────────────────┴──────────────────────────┘
```

### Performance Benchmark (Typical):
```
Operation: Send 10,000 requests with vendor data

REST + JSON:
  ⏱ Time: ~4.2 seconds
  📦 Total data transferred: ~1.5 MB
  🔗 Connections: 10,000 separate HTTP connections

gRPC + Protobuf:
  ⏱ Time: ~0.8 seconds (5x faster!)
  📦 Total data transferred: ~0.5 MB (3x smaller!)
  🔗 Connections: 1 multiplexed HTTP/2 connection
```

### When to Use REST vs gRPC:
```
Use REST when:
  ✅ Building public APIs (consumed by external developers)
  ✅ Browser clients need direct access (React, Angular, etc.)
  ✅ Simple CRUD applications
  ✅ API needs to be easily testable (Postman, curl)
  ✅ Team is more familiar with REST

Use gRPC when:
  ✅ Microservice-to-microservice communication (internal)
  ✅ High performance / low latency required
  ✅ Real-time streaming needed
  ✅ Polyglot environment (C#, Java, Go services talking)
  ✅ Strong API contracts are critical
  ✅ Mobile apps with limited bandwidth
```

---

## 7. Why gRPC + REST Gateway for Your Migration?

### ⭐ This is the most relevant section for your team's work!

Your team chose **gRPC + REST Gateway** because it gives you the **best of both worlds**:
- **gRPC** for fast internal microservice communication
- **REST Gateway** so existing clients (web browsers, mobile apps, legacy systems)
  can still use familiar REST/JSON APIs

### The Problem: Legacy ASP Migration
```
BEFORE (Legacy ASP Application):
┌────────────────────────────────────────────────────┐
│              Monolithic ASP Application             │
│                                                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │ Vendor   │ │ Order    │ │ User     │          │
│  │ Logic    │ │ Logic    │ │ Logic    │  All in  │
│  │          │ │          │ │          │  ONE big │
│  └──────────┘ └──────────┘ └──────────┘  app!    │
│                                                    │
│  ┌─────────────────────────────────────┐          │
│  │        Single Database              │          │
│  └─────────────────────────────────────┘          │
└────────────────────────────────────────────────────┘

Problems:
❌ Can't scale individual features
❌ One bug can crash everything
❌ Hard to deploy (deploy entire app for a small change)
❌ Technology locked (stuck with old ASP)
❌ Team bottleneck (everyone works in same codebase)
```

```
AFTER (Microservices with gRPC + REST Gateway):
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Browsers/Mobile ──▶ REST Gateway ──▶ gRPC Services    │
│                      (JSON ↔ gRPC)                      │
│                                                         │
│  ┌──────────────┐                                      │
│  │ REST Gateway │ ← Translates JSON↔Protobuf           │
│  │ (Envoy/YARP) │                                      │
│  └──────┬───────┘                                      │
│         │ gRPC (fast, binary)                          │
│    ┌────┴────┬──────────┬──────────┐                   │
│    ▼         ▼          ▼          ▼                   │
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────────┐              │
│ │Vendor│ │Order │ │User  │ │Notification│             │
│ │Service│ │Service│ │Service│ │Service   │             │
│ │(gRPC)│ │(gRPC)│ │(gRPC)│ │(gRPC)    │              │
│ └──┬───┘ └──┬───┘ └──┬───┘ └──────────┘              │
│    ▼        ▼        ▼                                 │
│  [DB 1]  [DB 2]   [DB 3]   ← Each service owns its DB│
└─────────────────────────────────────────────────────────┘

Benefits:
✅ Scale each service independently
✅ Deploy services independently
✅ Different teams own different services
✅ Use best technology per service
✅ One service crash doesn't kill others
```

### Why Not Just Use REST Between Microservices?
```
Scenario: User places an order

With REST between services (SLOW):
  Order Service ─── HTTP/JSON ──▶ Vendor Service (validate vendor)
  Order Service ─── HTTP/JSON ──▶ User Service (validate user)
  Order Service ─── HTTP/JSON ──▶ Inventory Service (check stock)
  Order Service ─── HTTP/JSON ──▶ Notification Service (send email)

  Total overhead: 4 × JSON serialization + 4 × HTTP/1.1 connections
  ⏱ ~120ms total latency

With gRPC between services (FAST):
  Order Service ─── gRPC/Protobuf ──▶ Vendor Service
  Order Service ─── gRPC/Protobuf ──▶ User Service
  Order Service ─── gRPC/Protobuf ──▶ Inventory Service
  Order Service ─── gRPC/Protobuf ──▶ Notification Service

  Total overhead: 4 × Protobuf (binary) + 1 multiplexed HTTP/2
  ⏱ ~25ms total latency (5x faster!)
```

### Why Still Need REST Gateway?
```
Problem: Browsers can't speak gRPC directly!

Browser (JavaScript) ──── gRPC ────▶ Server    ❌ Doesn't work!
Browser (JavaScript) ──── REST/JSON ──▶ Server  ✅ Works!

Solution: REST Gateway translates between the two

Browser ─── REST/JSON ──▶ Gateway ─── gRPC ──▶ Service
  (Web app sends JSON)    (Converts)   (Binary, fast)
```

---

## 8. gRPC + REST Gateway - How It Works

### Gateway Options for .NET:

```
Option 1: gRPC-Web (Microsoft built-in)
  → .NET middleware that translates gRPC-Web ↔ gRPC
  → Good for Blazor/browser apps calling gRPC services

Option 2: gRPC JSON Transcoding (ASP.NET Core 7+) ⭐ RECOMMENDED
  → Built into ASP.NET Core, auto-creates REST endpoints from .proto
  → No separate gateway needed! Single service serves both gRPC AND REST

Option 3: Envoy Proxy
  → Standalone proxy that translates REST ↔ gRPC
  → Used heavily in Kubernetes environments
  → Language agnostic

Option 4: YARP (Yet Another Reverse Proxy) by Microsoft
  → .NET-based reverse proxy for routing/load balancing
  → Can sit in front of gRPC services
```

### gRPC JSON Transcoding - The .NET Way (Easiest for your team):

```protobuf
// vendor.proto — Add HTTP annotations for REST mapping
import "google/api/annotations.proto";

service VendorService {
    rpc GetVendor (GetVendorRequest) returns (VendorResponse) {
        option (google.api.http) = {
            get: "/api/v1/vendors/{id}"      // ← REST endpoint auto-created!
        };
    }

    rpc CreateVendor (CreateVendorRequest) returns (VendorResponse) {
        option (google.api.http) = {
            post: "/api/v1/vendors"
            body: "*"
        };
    }

    rpc ListVendors (ListVendorsRequest) returns (VendorListResponse) {
        option (google.api.http) = {
            get: "/api/v1/vendors"
        };
    }

    rpc UpdateVendor (UpdateVendorRequest) returns (VendorResponse) {
        option (google.api.http) = {
            put: "/api/v1/vendors/{id}"
            body: "*"
        };
    }

    rpc DeleteVendor (GetVendorRequest) returns (Empty) {
        option (google.api.http) = {
            delete: "/api/v1/vendors/{id}"
        };
    }
}
```

### What Happens:
```
With JSON Transcoding, ONE service serves BOTH:

gRPC Clients (internal services):
  vendorClient.GetVendor(new GetVendorRequest { Id = 1 })
  → Binary/Protobuf over HTTP/2 → FAST!

REST Clients (browsers, Postman, legacy apps):
  GET /api/v1/vendors/1
  → JSON over HTTP/1.1 → Compatible!

Same server, same code, same .proto file — TWO protocols!
```

### Flow Diagram:
```
┌──────────────┐     REST (JSON)     ┌─────────────────────────┐
│  Browser /   │ ──── GET /api/v1/ ─▶│                         │
│  React App   │ ◀── JSON response ──│   ASP.NET Core Server   │
└──────────────┘                     │                         │
                                     │  ┌───────────────────┐  │
┌──────────────┐     gRPC (Proto)    │  │  VendorService    │  │
│  Order       │ ── GetVendor() ───▶ │  │  (implements      │  │
│  Service     │ ◀─ VendorResponse ──│  │   .proto file)    │  │
│  (internal)  │                     │  └───────────────────┘  │
└──────────────┘                     │                         │
                                     │  JSON Transcoding       │
┌──────────────┐     gRPC (Proto)    │  middleware handles     │
│  Notification│ ── GetVendor() ───▶ │  the translation!       │
│  Service     │ ◀─ VendorResponse ──│                         │
└──────────────┘                     └─────────────────────────┘
```

---

## 9. gRPC in ASP.NET Core

### Setting Up a gRPC Service in .NET:

```csharp
// 1. Create project
// dotnet new grpc -n VendorService

// 2. Program.cs
var builder = WebApplication.CreateBuilder(args);

// Add gRPC service
builder.Services.AddGrpc();

// Add JSON transcoding (for REST gateway)
builder.Services.AddGrpcJsonTranscoding();

// Add Swagger for REST endpoints
builder.Services.AddGrpcSwagger();
builder.Services.AddSwaggerGen();

var app = builder.Build();

app.UseSwagger();
app.UseSwaggerUI();

// Map gRPC service
app.MapGrpcService<VendorServiceImpl>();

app.Run();
```

```csharp
// 3. Implement the service (VendorServiceImpl.cs)
public class VendorServiceImpl : VendorService.VendorServiceBase
{
    private readonly AppDbContext _db;

    public VendorServiceImpl(AppDbContext db) => _db = db;

    // Implement the GetVendor RPC
    public override async Task<VendorResponse> GetVendor(
        GetVendorRequest request, ServerCallContext context)
    {
        var vendor = await _db.Vendors.FindAsync(request.Id);

        if (vendor == null)
            throw new RpcException(new Status(
                StatusCode.NotFound, $"Vendor {request.Id} not found"));

        return new VendorResponse
        {
            Id = vendor.Id,
            VendorName = vendor.VendorName,
            Category = vendor.Category,
            Status = vendor.Status
        };
    }

    // Implement CreateVendor RPC
    public override async Task<VendorResponse> CreateVendor(
        CreateVendorRequest request, ServerCallContext context)
    {
        var vendor = new Vendor
        {
            VendorName = request.VendorName,
            Category = request.Category,
            Email = request.Email,
            Status = "Active",
            CreatedAt = DateTime.UtcNow
        };

        _db.Vendors.Add(vendor);
        await _db.SaveChangesAsync();

        return new VendorResponse
        {
            Id = vendor.Id,
            VendorName = vendor.VendorName,
            Status = vendor.Status
        };
    }
}
```

```csharp
// 4. Client calling the gRPC service from another .NET service
// Install: dotnet add package Grpc.Net.Client

using var channel = GrpcChannel.ForAddress("https://localhost:5001");
var client = new VendorService.VendorServiceClient(channel);

// Call gRPC method (feels like a local function call!)
var vendor = await client.GetVendorAsync(
    new GetVendorRequest { Id = 1 });

Console.WriteLine($"Vendor: {vendor.VendorName}");
```

### gRPC Error Handling (Status Codes):
```
gRPC Status Code    → HTTP Equivalent   → When to Use
────────────────────────────────────────────────────────
OK                  → 200               → Success
NOT_FOUND           → 404               → Resource doesn't exist
ALREADY_EXISTS      → 409               → Duplicate creation
INVALID_ARGUMENT    → 400               → Bad request data
PERMISSION_DENIED   → 403               → Not authorized
UNAUTHENTICATED     → 401               → No valid credentials
INTERNAL            → 500               → Server error
UNAVAILABLE         → 503               → Service down
DEADLINE_EXCEEDED   → 504               → Timeout
```

---

## 10. Legacy ASP Migration Pattern

### Phased Migration Strategy (What Your Team is Likely Doing):

```
Phase 1: Strangler Fig Pattern
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Gradually replace the monolith, one feature at a time.

Step 1: Put a REST Gateway in front of the legacy app
┌──────────┐     ┌───────────┐     ┌─────────────────┐
│ Clients  │────▶│  Gateway  │────▶│ Legacy ASP App   │
│          │◀────│  (YARP)   │◀────│ (still handles   │
└──────────┘     └───────────┘     │  everything)     │
                                   └─────────────────┘

Step 2: Extract Vendor feature into a gRPC microservice
┌──────────┐     ┌───────────┐     ┌─────────────────┐
│ Clients  │────▶│  Gateway  │──┬─▶│ Legacy ASP App   │
│          │◀────│           │◀─┤  │ (minus vendors)  │
└──────────┘     └───────────┘  │  └─────────────────┘
                                │
                                │  ┌─────────────────┐
                                ├─▶│ Vendor Service   │
                                │  │ (new gRPC)       │
                                └──└─────────────────┘

Step 3: Extract more features...
┌──────────┐     ┌───────────┐     ┌─────────────────┐
│ Clients  │────▶│  Gateway  │──┬─▶│ Legacy ASP App   │
│          │◀────│           │  │  │ (getting smaller)│
└──────────┘     └───────────┘  │  └─────────────────┘
                                ├─▶ Vendor Service (gRPC)
                                ├─▶ Order Service (gRPC)
                                ├─▶ User Service (gRPC)
                                └─▶ Notification Service (gRPC)

Step 4: Legacy app fully replaced → Remove it!
```

### Why This Pattern Works:
```
✅ Zero downtime migration — old app keeps running
✅ Gradual — migrate one feature at a time, low risk
✅ Rollback — if new service fails, gateway routes back to legacy
✅ Team can work in parallel — different teams build different services
✅ Test independently — each service has its own tests
✅ No "big bang" rewrite — which almost always fails!
```

### Real Example: Migrating the Vendor Module
```
Legacy ASP (Before):
  /vendors.asp?action=list        → Inline SQL + HTML in one file
  /vendors.asp?action=create      → Form post, server-side rendering
  /vendors.asp?action=update&id=1 → Mixed business logic + UI

New Architecture (After):
  Frontend: React SPA
    → GET /api/v1/vendors         → REST (via Gateway)
    → POST /api/v1/vendors        → REST (via Gateway)

  Gateway translates to:
    → vendorService.ListVendors() → gRPC (internal, fast)
    → vendorService.CreateVendor()→ gRPC (internal, fast)

  Other internal services call directly:
    → orderService calls vendorService.GetVendor() → gRPC (no gateway!)
```

---

## 11. When NOT to Use gRPC

```
❌ Simple CRUD web apps with only browser clients
   → REST is simpler and browsers support it natively

❌ Public APIs consumed by third-party developers
   → REST/JSON is universally understood, gRPC requires special tooling

❌ When human readability of data is important
   → JSON is readable in logs/debugging; Protobuf binary is not

❌ When you need HTTP caching (CDN, browser cache)
   → REST leverages HTTP caching; gRPC doesn't

❌ Very small teams with simple architecture
   → gRPC adds complexity; not worth it for 1-2 services

❌ When all clients are web browsers
   → gRPC-Web exists but adds complexity vs plain REST
```

---

## 12. Key Terminology

```
┌─────────────────────┬────────────────────────────────────────────────┐
│ Term                │ Meaning                                        │
├─────────────────────┼────────────────────────────────────────────────┤
│ gRPC                │ Google Remote Procedure Call framework          │
│ Protobuf            │ Protocol Buffers - binary serialization format  │
│ .proto file         │ Contract file defining messages and services    │
│ protoc              │ Protobuf compiler - generates code from .proto  │
│ Stub                │ Auto-generated client code for calling services │
│ Channel             │ Connection to a gRPC server                     │
│ RPC                 │ Remote Procedure Call - calling remote function  │
│ Unary               │ Single request → single response                │
│ Streaming           │ Continuous flow of messages                     │
│ HTTP/2              │ Transport protocol used by gRPC                 │
│ Multiplexing        │ Multiple requests on one connection             │
│ JSON Transcoding    │ Auto-translate between REST/JSON and gRPC       │
│ Envoy               │ Proxy for routing, load balancing, translation  │
│ YARP                │ Microsoft's .NET reverse proxy                  │
│ Strangler Fig       │ Migration pattern: gradually replace monolith   │
│ Service Mesh        │ Infrastructure layer for service communication  │
│ Deadline            │ Timeout for a gRPC call                         │
│ Metadata            │ Headers/context sent with gRPC calls            │
│ Interceptor         │ Middleware for gRPC (like ASP.NET middleware)    │
│ Reflection          │ gRPC service discovery (like Swagger for gRPC)  │
└─────────────────────┴────────────────────────────────────────────────┘
```

---

## 📝 Quick Summary for Your Team Discussion

```
Q: Why did we choose gRPC?
A: For fast, type-safe communication between our new microservices.
   5-10x faster than REST for internal service-to-service calls.

Q: Why do we still need REST?
A: Browsers can't speak gRPC. The REST Gateway translates
   JSON ↔ Protobuf so web apps and external clients still work.

Q: How does the migration work?
A: Strangler Fig Pattern — we put a gateway in front of the legacy app,
   extract one feature at a time into gRPC services, and gradually
   route traffic to the new services until the legacy app is empty.

Q: What do I need to learn?
A: 1. Protocol Buffers (.proto files) — defining messages & services
   2. gRPC service implementation in C#/ASP.NET Core
   3. How JSON Transcoding maps REST ↔ gRPC
   4. Error handling with gRPC status codes
```

---

**Related: [SQL Learning Guide →](../sql-learning/01-SQL-Basics.md)**