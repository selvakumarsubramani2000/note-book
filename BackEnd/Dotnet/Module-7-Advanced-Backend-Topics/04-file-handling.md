# 📁 File Handling — Uploads, Safe Validation, Storage & Downloads

> **Trainer's Note:** Files are bigger and riskier than JSON. Upload endpoints must enforce **size, type, and name safety**, store bytes somewhere durable, and stream downloads without loading entire files into RAM. Treat every upload as untrusted input.

---

## 📑 Table of Contents
1. [Multipart Uploads and IFormFile](#1-multipart-uploads-and-iformfile)
2. [Basic Upload Endpoint](#2-basic-upload-endpoint)
3. [Security Validations](#3-security-validations)
4. [Filename Hardening](#4-filename-hardening)
5. [Local Disk Storage](#5-local-disk-storage)
6. [Cloud Blob Storage (Azure / S3)](#6-cloud-blob-storage-azure--s3)
7. [Database vs Object Storage](#7-database-vs-object-storage)
8. [Serving and Streaming Files](#8-serving-and-streaming-files)
9. [Size Limits and Kestrel/Form Options](#9-size-limits-and-kestrelform-options)
10. [Virus Scanning and Async Processing](#10-virus-scanning-and-async-processing)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. Multipart Uploads and IFormFile

Browsers and clients send files as **`multipart/form-data`**.

```http
POST /api/products/5/images HTTP/1.1
Content-Type: multipart/form-data; boundary=----bound

------bound
Content-Disposition: form-data; name="file"; filename="keyboard.png"
Content-Type: image/png

<<binary>>
------bound--
```

In ASP.NET Core, use **`IFormFile`**:

```csharp
public interface IFormFile
{
    string ContentType { get; }
    string FileName { get; }
    long Length { get; }
    Stream OpenReadStream();
    // ...
}
```

| Property | Meaning |
|----------|---------|
| `FileName` | Client-provided name (untrusted!) |
| `ContentType` | Client-provided MIME (untrusted!) |
| `Length` | Size in bytes |
| `OpenReadStream()` | Read content stream |

---

## 2. Basic Upload Endpoint

```csharp
[ApiController]
[Route("api/files")]
[Authorize]
public class FilesController : ControllerBase
{
    private readonly IFileStorage _storage;
    private readonly ILogger<FilesController> _logger;

    public FilesController(IFileStorage storage, ILogger<FilesController> logger)
    {
        _storage = storage;
        _logger = logger;
    }

    [HttpPost("upload")]
    [RequestSizeLimit(5_000_000)] // 5 MB endpoint cap
    public async Task<ActionResult<FileUploadResult>> Upload(
        IFormFile file,
        CancellationToken ct)
    {
        if (file is null || file.Length == 0)
            return BadRequest(new { message = "File is required" });

        var saved = await _storage.SaveAsync(file, ct);
        _logger.LogInformation("Stored file {FileId} ({Bytes} bytes)", saved.Id, saved.SizeBytes);
        return CreatedAtAction(nameof(Download), new { id = saved.Id }, saved);
    }
}

public record FileUploadResult(Guid Id, string ContentType, long SizeBytes);
```

Multiple files:
```csharp
public async Task<IActionResult> UploadMany(List<IFormFile> files) { /* ... */ }
```

Or bind from a form DTO:
```csharp
public class UploadForm
{
    [Required]
    public IFormFile File { get; set; } = default!;
    public string? Caption { get; set; }
}
```

---

## 3. Security Validations

Never trust the client. Validate **before** writing to disk/cloud.

### Size
```csharp
const long MaxBytes = 5 * 1024 * 1024; // 5 MB
if (file.Length > MaxBytes)
    return BadRequest("File too large");
```

### Extension allow-list
```csharp
var ext = Path.GetExtension(file.FileName)?.ToLowerInvariant();
string[] allowed = [".jpg", ".jpeg", ".png", ".pdf"];
if (ext is null || !allowed.Contains(ext))
    return BadRequest("File type not allowed");
```

### Content-Type allow-list (still spoofable)
```csharp
string[] allowedMime = ["image/jpeg", "image/png", "application/pdf"];
if (!allowedMime.Contains(file.ContentType))
    return BadRequest("Content type not allowed");
```

### Content sniffing (stronger)
Read magic bytes (file signatures), e.g. PNG starts with `89 50 4E 47`.
Libraries and custom checks reduce “`evil.exe` renamed to `photo.png`” risk.

### Defense layers
| Check | Strength |
|-------|----------|
| Extension allow-list | Weak alone |
| Content-Type allow-list | Weak alone (client-set) |
| Magic-byte inspection | Stronger |
| Antivirus scan | Strong for malware |
| Re-encode images | Strips weird payloads |

```csharp
public static void EnsureAllowedImage(IFormFile file)
{
    if (file.Length <= 0 || file.Length > 5_000_000)
        throw new ValidationException("Invalid file size");

    var ext = Path.GetExtension(file.FileName).ToLowerInvariant();
    if (ext is not (".jpg" or ".jpeg" or ".png"))
        throw new ValidationException("Only JPG/PNG allowed");

    // optional: inspect header bytes from file.OpenReadStream()
}
```

---

## 4. Filename Hardening

Client filenames can contain:
- path traversal (`../../web.config`)
- odd unicode
- extremely long strings
- executable-looking names

### Safe approach
```csharp
var ext = Path.GetExtension(file.FileName)?.ToLowerInvariant() ?? "";
var safeName = $"{Guid.NewGuid():N}{ext}"; // ignore original name for storage
var originalForDisplay = Path.GetFileName(file.FileName); // strip paths only for display metadata
```

| Rule | Practice |
|------|----------|
| Don’t use raw `file.FileName` as disk path | Generate server names |
| Use `Path.GetFileName` if keeping display name | Removes directory parts |
| Store metadata in DB | id, content type, size, owner, hash |
| Keep files outside web root | Prevent direct arbitrary execution/serve |

---

## 5. Local Disk Storage

### Simple save
```csharp
public class LocalFileStorage : IFileStorage
{
    private readonly string _root;

    public LocalFileStorage(IConfiguration config)
    {
        _root = config["FileStorage:Root"] ?? Path.Combine(Path.GetTempPath(), "shop-files");
        Directory.CreateDirectory(_root);
    }

    public async Task<FileUploadResult> SaveAsync(IFormFile file, CancellationToken ct)
    {
        var id = Guid.NewGuid();
        var ext = Path.GetExtension(file.FileName)?.ToLowerInvariant() ?? "";
        var path = Path.Combine(_root, $"{id:N}{ext}");

        await using var stream = System.IO.File.Create(path);
        await file.CopyToAsync(stream, ct);

        return new FileUploadResult(id, file.ContentType, file.Length);
    }
}
```

### Pros / cons
| Local disk | |
|------------|---|
| Pros | Simple, cheap to start |
| Cons | Hard on multi-instance hosts; backups; not ideal for containers without volume; scaling pain |

For multi-node APIs, prefer shared object storage.

---

## 6. Cloud Blob Storage (Azure / S3)

### Concept
```
API receives upload
  → validates
  → streams to Azure Blob / AWS S3
  → stores blob URL/key in database
```

| Provider | Typical building block |
|----------|------------------------|
| **Azure** | Blob Storage container + blob key |
| **AWS** | S3 bucket + object key |
| **GCP** | Cloud Storage object |

### Benefits
- Durable and scalable  
- Works across many API instances  
- Lifecycle policies, CDN integration  
- Optional signed URLs for direct download/upload  

### Direct-to-cloud uploads (advanced)
```
Client → requests SAS/presigned URL from API
Client → uploads directly to blob/S3
API → records metadata after callback/complete
```
Offloads heavy bandwidth from your API.

### Implementation tip
Use official SDKs; stream `OpenReadStream()` to blob upload APIs; don’t buffer entire huge files in `byte[]` unless small and intentional.

Secrets for storage accounts/keys: **env/vault**, never git (Module 5/6 habits).

---

## 7. Database vs Object Storage

| Store file bytes in SQL | Store in blob + metadata in SQL |
|-------------------------|---------------------------------|
| Simple transactional coupling | Industry default for larger files |
| DB bloat / backup cost | Cheaper object storage tiers |
| OK for tiny files only | Scales to media libraries |

**Recommendation:** metadata in DB, bytes in disk/blob.

```csharp
public class StoredFile
{
    public Guid Id { get; set; }
    public string StorageKey { get; set; } = "";
    public string ContentType { get; set; } = "";
    public string? OriginalFileName { get; set; }
    public long SizeBytes { get; set; }
    public string OwnerUserId { get; set; } = "";
    public DateTime CreatedAtUtc { get; set; }
}
```

---

## 8. Serving and Streaming Files

### Return a file download
```csharp
[HttpGet("{id:guid}")]
public async Task<IActionResult> Download(Guid id, CancellationToken ct)
{
    var meta = await _db.Files.FindAsync([id], ct);
    if (meta is null) return NotFound();

    // authorization: only owner/admin
    var stream = await _storage.OpenReadAsync(meta.StorageKey, ct);
    return File(stream, meta.ContentType, meta.OriginalFileName ?? "download");
}
```

`File(...)` supports streams — ASP.NET Core writes response without loading whole content if streamed properly.

### Physical file helper
```csharp
return PhysicalFile(path, contentType, downloadName);
```

### Inline vs attachment
```csharp
// Content-Disposition controlled via File() overload / response headers
// inline: display in browser (PDF/image)
// attachment: force download
```

### Efficiency tips
1. Prefer streaming over `byte[]` for large files  
2. Enable range requests when serving media if needed  
3. Use CDN in front of public blobs  
4. Authenticate private downloads via API or short-lived signed URLs  
5. Set correct `Content-Type`  

### Don’t
```csharp
// ❌ read 2GB into memory
var bytes = await System.IO.File.ReadAllBytesAsync(path);
return File(bytes, "application/octet-stream");
```

---

## 9. Size Limits and Kestrel/Form Options

Defaults may block large uploads. Configure deliberately:

```csharp
builder.Services.Configure<FormOptions>(o =>
{
    o.MultipartBodyLengthLimit = 10_000_000; // 10 MB
});

builder.WebHost.ConfigureKestrel(o =>
{
    o.Limits.MaxRequestBodySize = 10_000_000;
});
```

Per-endpoint:
```csharp
[RequestSizeLimit(10_000_000)]
[RequestFormLimits(MultipartBodyLengthLimit = 10_000_000)]
public async Task<IActionResult> Upload(IFormFile file) { /* ... */ }
```

Only raise limits where required; don’t globally allow 2GB if not needed.

---

## 10. Virus Scanning and Async Processing

For higher security tiers:
1. Accept upload → store in **quarantine** area  
2. Background worker scans (clamav/cloud AV)  
3. On clean → move to real container + mark Available  
4. On dirty → delete + flag  

Fits Module 7 background jobs:

```
POST /files/upload → 201 + fileId (PendingScan)
worker scans → Available | Rejected
GET /files/{id} → 423/403 while pending, file when available
```

Also use workers for image resize/thumbnail generation after upload returns.

---

## 11. Knowledge Check

**Q1.** Why is `IFormFile.ContentType` not sufficient security alone?  
**Q2.** What should you use as the stored filename on disk/blob?  
**Q3.** Local disk vs blob storage for a 3-instance API farm?  
**Q4.** Why stream downloads instead of `ReadAllBytes`?  
**Q5.** Where should file bytes usually live vs metadata?  
**Q6.** Name three upload validations you should implement.  
**Q7.** How do background jobs improve large file pipelines?

### Mini practice
1. Build `POST /api/files/upload` accepting `IFormFile`  
2. Validate size + extension allow-list  
3. Save under a generated GUID filename outside wwwroot  
4. Store metadata in DB  
5. Implement authorized `GET` download via stream  
6. (Optional) Sketch Azure Blob keys + SAS flow on paper  

### Answers (short)
1. Client can spoof MIME headers  
2. Server-generated safe name (e.g. GUID + ext)  
3. Blob/shared storage — local disk isn’t shared  
4. Memory usage and scalability  
5. Bytes in object/disk storage; metadata in DB  
6. Size, extension/MIME/magic bytes, authz, name hardening…  
7. Scan/resize/process without blocking upload response  

---

## ✅ What You Should Feel Confident About

- [ ] Accept uploads with `IFormFile`  
- [ ] Validate size/type and harden filenames  
- [ ] Store files on disk or design for blob storage  
- [ ] Keep metadata in the database  
- [ ] Stream file responses efficiently  
- [ ] Configure request size limits intentionally  

**Previous:** [03-background-jobs-and-scheduling.md](./03-background-jobs-and-scheduling.md)  
**Next:** [05-security-best-practices.md](./05-security-best-practices.md) — OWASP-minded API hardening.
