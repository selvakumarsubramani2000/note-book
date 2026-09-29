# gRPC Client Call Flow Documentation

## Overview
This document explains the complete call flow from a REST API client to the gRPC service in the Ashley Supplier system.

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CLIENT (Browser/API Consumer)                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ HTTP/REST
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│          REST DOMAIN GATEWAY (AshleySupplierSupplierRestDomainGateway)      │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  1. REST Controller Layer                                          │    │
│  │     - InquiryCommonController.cs                                   │    │
│  │     - Handles HTTP requests (GET/POST/PUT)                         │    │
│  │     - Validates route parameters & query strings                   │    │
│  │     - Returns HTTP responses                                       │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                 │                                            │
│                                 │ Calls                                      │
│                                 ▼                                            │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  2. Core Service Layer                                             │    │
│  │     - InquiryCommonCoreService.cs                                  │    │
│  │     - Business logic orchestration                                 │    │
│  │     - Builds gRPC request objects                                  │    │
│  │     - Passes CompanyCode for multi-tenancy                         │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                 │                                            │
│                                 │ Calls                                      │
│                                 ▼                                            │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  3. gRPC Client (Injected Dependency)                              │    │
│  │     - IInquiryCommonClient interface                               │    │
│  │     - Registered in DI container via AddGrpcClients()              │    │
│  └────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ gRPC/HTTP2 (over network)
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│           gRPC CLIENT LIBRARY (AshleySupplierSupplierGrpcService.Client)    │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  4. Domain Client Implementation                                   │    │
│  │     - InquiryCommonClient.cs                                       │    │
│  │     - Creates GrpcChannel to service URL                           │    │
│  │     - Wraps auto-generated stub                                    │    │
│  │     - Injects CompanyCode header via CreateHeaders()               │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                 │                                            │
│                                 │ Uses                                       │
│                                 ▼                                            │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  5. Auto-Generated gRPC Stub                                       │    │
│  │     - InquiryCommonService.InquiryCommonServiceClient              │    │
│  │     - Generated from .proto files                                  │    │
│  │     - Handles serialization/deserialization                        │    │
│  │     - Manages HTTP/2 transport                                     │    │
│  └────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ gRPC/HTTP2 (over network)
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│             gRPC SERVICE (AshleySupplierSupplierGrpcService.Server)         │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  6. gRPC Service Implementation                                    │    │
│  │     - InquiryCommonServiceGrpcImpl.cs                              │    │
│  │     - Extends InquiryCommonService.InquiryCommonServiceBase        │    │
│  │     - Extracts CompanyCode from headers                            │    │
│  │     - Logs requests/responses                                      │    │
│  │     - Handles exceptions → RpcException                            │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                 │                                            │
│                                 │ Calls                                      │
│                                 ▼                                            │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  7. Data Service / Repository Layer                                │    │
│  │     - IInquiryCommonDataService                                    │    │
│  │     - Executes stored procedures                                   │    │
│  │     - Maps database results to domain models                       │    │
│  └────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ SQL
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DATABASE (SQL Server)                                │
│                  Multi-tenant: AFI, IMP, AIMG databases                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Detailed Flow Example: GetStatuses

Let me show you a specific example with actual code flow:

### 1️⃣ REST Controller receives HTTP request
**File**: `InquiryCommonController.cs`
```csharp
[HttpGet("statuses/{companyCode}")]
public async Task<ActionResult<StatusResponse>> GetStatuses(
    [FromRoute] string companyCode,
    [FromQuery] string? correlationId = null)
{
    var response = await _coreService.GetStatuses(companyCode, correlationId);
    return Ok(response);
}
```

### 2️⃣ Core Service builds request and calls gRPC client
**File**: `InquiryCommonCoreService.cs`
```csharp
public async Task<StatusResponse> GetStatuses(string companyCode, string? correlationId = null)
{
    var request = new StatusRequest
    {
        CorrelationId = correlationId ?? Guid.NewGuid().ToString()
    };
    // Calls the injected IInquiryCommonClient
    return await _inquiryCommonClient.GetStatusesAsync(request, companyCode);
}
```

### 3️⃣ gRPC Client adds headers and calls stub
**File**: `InquiryCommonClient.cs`
```csharp
public async Task<StatusResponse> GetStatusesAsync(StatusRequest request, string companyCode)
{
    // Injects CompanyCode header for multi-tenant routing
    return await _stub.GetStatusesAsync(request, headers: CreateHeaders(companyCode));
}

private Metadata CreateHeaders(string companyCode)
{
    var headers = new Metadata
    {
        { "CompanyCode", companyCode }  // ← Multi-tenant routing key
    };
    return headers;
}
```

### 4️⃣ gRPC Service receives request and extracts headers
**File**: `InquiryCommonServiceGrpcImpl.cs`
```csharp
public override async Task<StatusResponse> GetStatuses(StatusRequest request, ServerCallContext context)
{
    // Extract CompanyCode from headers
    var companyCode = GetCompanyCodeFromHeaders(context);

    // Call Data Service with CompanyCode
    var statuses = await _dataService.GetStatusesAsync(companyCode);

    // Map to response
    var response = new StatusResponse
    {
        CorrelationId = request.CorrelationId,
        Success = true
    };

    foreach (var status in statuses)
    {
        response.Data.Add(new API.Status { ... });
    }

    return response;
}
```

---

## Key Configuration Points

### 🔧 gRPC Client Registration (Startup)
**File**: `GrpcClientExtensions.cs` (in REST Domain Gateway)

```csharp
public static IServiceCollection AddGrpcClients(
    this IServiceCollection services,
    IConfiguration configuration)
{
    // Get gRPC service URL from configuration
    var grpcServiceUrl = configuration["CoreServices:AshleySupplierSupplierGrpcService:Url"];

    // Register domain-specific gRPC clients as singletons
    services.AddSingleton<IInquiryCommonClient>(provider =>
        InquiryCommonClient.Of(grpcServiceUrl));  // ← Factory method creates client

    services.AddSingleton<ICreatePOCommonClient>(provider =>
        CreatePOCommonClient.Of(grpcServiceUrl));

    // ... more clients
}
```

**Configuration** (`appsettings.json`):
```json
{
  "CoreServices": {
    "AshleySupplierSupplierGrpcService": {
      "Url": "http://localhost:5001"
    }
  }
}
```

### 🔧 gRPC Service Registration (Startup)
**File**: `GrpcServiceExtensions.cs` (in gRPC Service Server)

```csharp
public static IServiceCollection AddGrpcWithInterceptors(this IServiceCollection services)
{
    services.AddGrpc(options =>
    {
        options.Interceptors.Add<ExceptionInterceptor>();  // ← Global exception handling
    });

    services.AddGrpcReflection();  // ← Enables reflection for tools like grpcurl
    return services;
}

public static WebApplication MapGrpcServices(this WebApplication app)
{
    // Map each domain-specific service
    app.MapGrpcService<InquiryCommonServiceGrpcImpl>();
    app.MapGrpcService<CreatePOCommonServiceGrpcImpl>();
    app.MapGrpcService<VendorProfileServiceGrpcImpl>();
    // ... more services

    return app;
}
```

---

## Multi-Tenancy Pattern

### 🏢 CompanyCode Header Flow

The system uses **CompanyCode** header for multi-tenant database routing:

```
Request: GET /api/inquiry-common/statuses/AFI
                                            ↑
                                       CompanyCode
                                            │
                                            ▼
CoreService extracts "AFI" from route parameter
                                            │
                                            ▼
gRPC Client injects header: { "CompanyCode": "AFI" }
                                            │
                                            ▼
gRPC Service reads header from context
                                            │
                                            ▼
DataService uses CompanyCode to select database connection string
                                            │
                                            ▼
Connects to AFI database (vs IMP or AIMG)
```

### 📊 Multi-Tenant Database Selection

**Pattern** in `InquiryCommonDataService.cs`:
```csharp
private string GetConnectionString(string companyCode)
{
    return companyCode.ToUpper() switch
    {
        "AFI" => _configuration.GetConnectionString("AFIDatabase"),
        "IMP" => _configuration.GetConnectionString("IMPDatabase"),
        "AIMG" => _configuration.GetConnectionString("AIMGDatabase"),
        _ => throw new ArgumentException($"Unknown company code: {companyCode}")
    };
}
```

---

## Transport Details

### 📡 Communication Protocol

| Layer | Protocol | Port | Format |
|-------|----------|------|--------|
| REST API → Gateway | HTTP/1.1 | 5000 | JSON |
| Gateway → gRPC Service | HTTP/2 (gRPC) | 5001 | Protobuf |
| gRPC Service → Database | TDS (SQL) | 1433 | Binary |

### 🔐 Headers Transmitted

**REST → Gateway**:
- `Authorization`: Bearer token (Keycloak JWT)
- `Content-Type`: application/json

**Gateway → gRPC Service**:
- `CompanyCode`: AFI / IMP / AIMG (multi-tenant routing)
- `grpc-timeout`: Request timeout
- `:authority`: gRPC service address

---

## Error Handling Flow

### ❌ Exception Propagation

```
Database Exception
       ↓
DataService catches → logs → throws
       ↓
gRPC Service catches → logs → throws RpcException
       ↓
gRPC Client receives → propagates to CoreService
       ↓
CoreService propagates to Controller
       ↓
Controller catches → returns HTTP 500 with error message
       ↓
Client receives JSON error response
```

**Example** in `InquiryCommonServiceGrpcImpl.cs`:
```csharp
catch (Exception ex)
{
    _logger.LogError(ex, "Error in GetStatuses: {Message}", ex.Message);
    throw new RpcException(new GrpcStatus(StatusCode.Internal,
        $"Error retrieving statuses: {ex.Message}"));
}
```

---

## File Locations Reference

### REST Domain Gateway
```
AshleySupplierSupplierRestDomainGateway.Server/
  ├── Controllers/
  │   └── InquiryCommonController.cs           ← REST endpoints
  ├── Extensions/
  │   └── GrpcClientExtensions.cs              ← Client registration
  └── Program.cs                                ← Startup configuration

AshleySupplierSupplierRestDomainGateway.Core/
  └── Services/
      └── InquiryCommonCoreService.cs          ← Business logic
```

### gRPC Client Library
```
AshleySupplierSupplierGrpcService.Client/
  └── Clients/
      └── InquiryCommonClient.cs               ← Client wrapper
```

### gRPC Service
```
AshleySupplierSupplierGrpcService.Server/
  ├── Grpc/
  │   └── InquiryCommonServiceGrpcImpl.cs      ← Service implementation
  ├── Extensions/
  │   └── GrpcServiceExtensions.cs             ← Service registration
  └── Startup.cs                                ← Configuration

AshleySupplierSupplierGrpcService.Core/
  └── Services/
      └── InquiryCommonDataService.cs          ← Data access
```

### Proto Definitions
```
AshleySupplierSupplierGrpcService.API/
  └── Protos/
      └── inquiry-common.proto                 ← gRPC contract
```

---

## Summary

The gRPC client call flow follows a **layered architecture**:

1. **REST Controller** - HTTP endpoint handler
2. **Core Service** - Business logic orchestration
3. **gRPC Client Interface** - Abstraction for testing
4. **gRPC Client Implementation** - Header injection + channel management
5. **Auto-generated Stub** - Protobuf serialization + HTTP/2 transport
6. **gRPC Service Implementation** - Request handling + header extraction
7. **Data Service** - Database access with multi-tenant routing

**Key Patterns**:
- ✅ Dependency Injection throughout
- ✅ Multi-tenancy via CompanyCode header
- ✅ Domain-driven separation (one client per domain)
- ✅ Factory pattern for client creation (`Client.Of(url)`)
- ✅ Exception interception at gRPC layer
- ✅ Correlation IDs for request tracing

