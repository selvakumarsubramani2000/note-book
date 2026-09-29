# 🚀 Hosting Options & Containers — IIS, Kestrel, Cloud, Docker

> **Trainer's Note:** After `dotnet publish`, something must **run** your API. Options range from **IIS** on Windows, to **Kestrel** behind Nginx, to **Azure App Service**, to **Docker containers**. Learn the shapes first; production details vary by company.

---

## 📑 Table of Contents
1. [Hosting Big Picture](#1-hosting-big-picture)
2. [Kestrel — The In-Process Web Server](#2-kestrel--the-in-process-web-server)
3. [IIS on Windows](#3-iis-on-windows)
4. [Kestrel Behind a Reverse Proxy (Nginx/Apache)](#4-kestrel-behind-a-reverse-proxy-nginxapache)
5. [Cloud Hosting Fundamentals (Azure App Service)](#5-cloud-hosting-fundamentals-azure-app-service)
6. [Why Containers?](#6-why-containers)
7. [Docker Concepts for .NET Devs](#7-docker-concepts-for-net-devs)
8. [Multi-Stage Dockerfile for a Web API](#8-multi-stage-dockerfile-for-a-web-api)
9. [Build and Run Locally](#9-build-and-run-locally)
10. [Container Config and Good Habits](#10-container-config-and-good-habits)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. Hosting Big Picture

```
Clients
   │
   ▼
[ Optional: CDN / API Gateway / Load balancer ]
   │
   ▼
[ Reverse proxy / Platform front door ]  ← IIS / Nginx / App Service front end
   │
   ▼
[ Kestrel + your ASP.NET Core app ]
   │
   ▼
[ DB / Redis / external APIs ]
```

| Hosting style | You manage |
|---------------|------------|
| IIS + ASP.NET Core Module | Windows server, app pool, reverse to Kestrel or in-process |
| Linux VM + Nginx + Kestrel | Process, proxy, TLS, updates |
| Azure App Service | Less OS; more app settings & deploy |
| Containers + orchestrator | Image, env, scaling, networking |

All of them ultimately run your published app with Kestrel (or platform-equivalent).

---

## 2. Kestrel — The In-Process Web Server

**Kestrel** is the cross-platform web server built into ASP.NET Core.

```csharp
// default in WebApplication — Kestrel is included
var app = builder.Build();
app.Run(); // listens on configured URLs
```

| Topic | Notes |
|-------|-------|
| Protocols | HTTP/1.1, HTTP/2 (and more as configured) |
| URLs | `ASPNETCORE_URLS`, `applicationUrl`, `UseUrls` |
| Production | Often **behind** a reverse proxy for TLS termination |

```bash
ASPNETCORE_URLS=http://0.0.0.0:8080
dotnet Shop.Api.dll
```

Binding `0.0.0.0` is common in containers so the port is reachable outside the container network namespace.

---

## 3. IIS on Windows

Classic enterprise Windows hosting:

```
Internet
  → IIS (HTTP.sys, site bindings, TLS certs)
  → ASP.NET Core Module
  → your app (in-process or out-of-process Kestrel)
```

### Typical setup pieces
| Piece | Role |
|-------|------|
| IIS site | Host name, HTTPS binding |
| Application pool | Identity, recycling |
| `web.config` | Present in publish output for ANCM |
| ASP.NET Core Hosting Bundle | Installs module + runtime support |

### Publish for IIS
Often framework-dependent publish + deploy folder to site root (or CI zip deploy).

### Pros / cons
| Pros | Cons |
|------|------|
| Familiar in Windows shops | Windows-only |
| Mature TLS/admin tooling | Ops overhead vs PaaS |
| Integrated Windows auth scenarios | Less “container native” by default |

---

## 4. Kestrel Behind a Reverse Proxy (Nginx/Apache)

On Linux, common pattern:

```
Client → Nginx (443 TLS) → http://127.0.0.1:5000 Kestrel
```

### Why reverse proxy?
| Benefit | Detail |
|---------|--------|
| TLS termination | Certs at Nginx |
| Static files / caching | Optional |
| Request buffering | Protects app |
| Multiple apps/ports | Path/host routing |
| Hardening | Only proxy exposed publicly |

### Forwarded headers
When proxy terminates TLS, app must trust `X-Forwarded-*` headers carefully:

```csharp
builder.Services.Configure<ForwardedHeadersOptions>(o =>
{
    o.ForwardedHeaders = ForwardedHeaders.XForwardedFor | ForwardedHeaders.XForwardedProto;
});
app.UseForwardedHeaders();
```
Misconfiguration can break HTTPS redirects or security.

### Nginx sketch (conceptual)
```nginx
server {
  listen 443 ssl;
  server_name api.shop.com;
  # ssl_certificate ...;

  location / {
    proxy_pass         http://127.0.0.1:5000;
    proxy_http_version 1.1;
    proxy_set_header   Host $host;
    proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header   X-Forwarded-Proto $scheme;
  }
}
```

Apache `ProxyPass` plays a similar role.

---

## 5. Cloud Hosting Fundamentals (Azure App Service)

**Azure App Service** is a common PaaS for .NET APIs:

```
git/GitHub Actions/Azure DevOps
        │ deploy
        ▼
 App Service plan (compute)
        │
        ▼
 Your Web App (Windows or Linux)
        │ app settings / connection strings
        ▼
 Azure SQL / other services
```

### What you typically configure
| Setting | Example |
|---------|---------|
| Runtime stack | .NET 8 |
| App settings | `ASPNETCORE_ENVIRONMENT`, `Jwt__Key` |
| Connection strings | ShopDb |
| HTTPS custom domain | api.shop.com |
| Scale | Instance count / plan size |
| Deployment slots | Staging slot swap |

### Mental model vs VM
| App Service | You don’t manage full OS patching the same way |
| VM + Nginx | You own more of the stack |

Other clouds have analogs (AWS Elastic Beanstalk/ECS, GCP Cloud Run, etc.). Concepts transfer: **runtime, env config, HTTPS, scale, deploy pipeline**.

---

## 6. Why Containers?

**Container** = packaged app + dependencies + defined start command, isolated with shared OS kernel.

```
"Works on my machine" → ship the machine-ish environment as an image
```

| Benefit | Detail |
|---------|--------|
| Consistency | Dev/stage/prod same image |
| Isolation | Fewer “install .NET 8” surprises on host |
| Density | Many containers per VM |
| Orchestration ready | Kubernetes, Swarm, cloud container services |
| CI-friendly | Build image → push registry → deploy |

---

## 7. Docker Concepts for .NET Devs

| Term | Meaning |
|------|---------|
| **Image** | Immutable template (layers) |
| **Container** | Running instance of an image |
| **Dockerfile** | Recipe to build an image |
| **Registry** | Image storage (Docker Hub, ACR, ECR) |
| **Volume** | Persistent/mounted files |
| **Port publish** | `-p host:container` |

```
Dockerfile → docker build → image → docker run → container
```

Official Microsoft images (examples):
- `mcr.microsoft.com/dotnet/sdk` — build  
- `mcr.microsoft.com/dotnet/aspnet` — run ASP.NET apps  

---

## 8. Multi-Stage Dockerfile for a Web API

Multi-stage builds keep final images **small**: compile in SDK stage, run on ASP.NET runtime stage.

```dockerfile
# ========== build stage ==========
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# copy csproj first for restore layer caching
COPY ["Shop.Api/Shop.Api.csproj", "Shop.Api/"]
RUN dotnet restore "Shop.Api/Shop.Api.csproj"

COPY . .
WORKDIR /src/Shop.Api
RUN dotnet publish "Shop.Api.csproj" -c Release -o /app/publish --no-restore

# ========== final stage ==========
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app

# non-root user recommended in real hardeninng
# USER app

ENV ASPNETCORE_URLS=http://+:8080
EXPOSE 8080

COPY --from=build /app/publish .
ENTRYPOINT ["dotnet", "Shop.Api.dll"]
```

### Why multi-stage?
| Stage | Contains |
|-------|----------|
| `build` | SDK + source + intermediate objects |
| `final` | Runtime + published output only |

Final image does **not** need the SDK.

Adjust paths to match your solution layout (often copy solution and restore at root).

---

## 9. Build and Run Locally

```bash
# from folder containing Dockerfile
docker build -t shop-api:local .

docker run --rm -p 8080:8080 \
  -e ASPNETCORE_ENVIRONMENT=Development \
  -e ConnectionStrings__ShopDb="..." \
  -e Jwt__Key="DEV_ONLY_KEY" \
  shop-api:local
```

Test:
```bash
curl http://localhost:8080/health
```

### Useful commands
```bash
docker images
docker ps
docker logs <container>
docker stop <container>
```

---

## 10. Container Config and Good Habits

| Habit | Why |
|-------|-----|
| Config via env vars | 12-factor friendly |
| Don’t bake secrets into image | Images get copied |
| Listen on non-privileged port | e.g. 8080 |
| Multi-stage publish | Smaller attack surface |
| Tag images with version/git sha | Traceability |
| Health endpoint | Orchestrator probes |
| Read-only root FS where possible | Hardening |
| One process per container | Clear lifecycle |
| Log to stdout | Platform collects logs |

```
Orchestrator
  → sets env secrets
  → runs container image:gitsha
  → probes GET /health
  → scrapes stdout logs
```

### Compose sketch (optional local stack)
```yaml
# docker-compose.yml (idea)
services:
  api:
    build: .
    ports: ["8080:8080"]
    environment:
      ASPNETCORE_ENVIRONMENT: Development
      ConnectionStrings__ShopDb: Server=db;...
    depends_on: [db]
  db:
    image: postgres:16
    # env/password for local only
```

---

## 11. Knowledge Check

**Q1.** What is Kestrel’s role in ASP.NET Core?  
**Q2.** Why put Nginx/IIS in front of Kestrel in production?  
**Q3.** Name two App Service settings you’d configure for a real API.  
**Q4.** Why multi-stage Docker builds for .NET?  
**Q5.** Which base image is typically used to *run* an ASP.NET app?  
**Q6.** How should containers receive production secrets?  
**Q7.** Why set `ASPNETCORE_URLS=http://+:8080` in containers?

### Mini practice
1. Identify how your workplace/prod host would run the API (IIS, Linux+Nginx, App Service, K8s)  
2. Write a multi-stage Dockerfile for your Web API  
3. `docker build` and `docker run -p 8080:8080`  
4. Pass connection string via `-e`  
5. Hit a health/products endpoint from the host  
6. Confirm secrets are not in the Dockerfile  

### Answers (short)
1. Cross-platform web server that actually serves HTTP for the app  
2. TLS, routing, hardening, ops features  
3. Env name, connection strings, JWT keys, custom domain, scale…  
4. Build with SDK, run slim runtime image  
5. `mcr.microsoft.com/dotnet/aspnet`  
6. Runtime env/orchestrator secret injection — not image layers  
7. Bind all interfaces on container port so published ports work  

---

## ✅ What You Should Feel Confident About

- [ ] Explain Kestrel + reverse proxy topology  
- [ ] Contrast IIS, Linux proxy, and App Service at a high level  
- [ ] Describe why containers help consistency  
- [ ] Read/write a multi-stage .NET Dockerfile  
- [ ] Build and run an API container locally  
- [ ] Configure containers with env vars, not baked secrets  

**Previous:** [02-building-and-publishing.md](./02-building-and-publishing.md)  
**Next:** [04-ci-cd-pipelines.md](./04-ci-cd-pipelines.md) — automate build, test, and deploy.
