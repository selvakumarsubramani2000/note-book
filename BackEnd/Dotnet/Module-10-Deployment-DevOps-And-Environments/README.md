# Module 10 — Deployment, DevOps & Environments

> Take a production-ready ASP.NET Core Web API from **local config** through **publish**, **hosting/containers**, and **CI/CD**.

**Outcome:** Configure Dev/Staging/Production safely, publish FDD/SCD artifacts, host with IIS/Kestrel/cloud/Docker, and automate build–test–release pipelines.

---

## 📚 Contents

| # | File | What you learn |
|---|------|----------------|
| 01 | [01-configuration-for-environments.md](./01-configuration-for-environments.md) | Environments, appsettings, env vars, user secrets |
| 02 | [02-building-and-publishing.md](./02-building-and-publishing.md) | `dotnet publish`, FDD vs SCD, output anatomy |
| 03 | [03-hosting-options-and-containers.md](./03-hosting-options-and-containers.md) | IIS, Kestrel+Nginx, App Service, multi-stage Docker |
| 04 | [04-ci-cd-pipelines.md](./04-ci-cd-pipelines.md) | CI vs CD, automated test/build, release promotion |

---

## 🗺️ Learning path

```
01 Configure each environment (no secrets in git)
        │
        ▼
02 Publish a Release artifact (FDD/SCD)
        │
        ▼
03 Host it (IIS / proxy / cloud / container)
        │
        ▼
04 Automate with CI/CD (same artifact → staging → prod)
```

### Suggested hands-on build
1. Split config across Development/Production appsettings  
2. Store JWT/DB secrets in user-secrets  
3. `dotnet publish -c Release -o artifacts/api` and run the DLL  
4. Add a multi-stage Dockerfile; run on port 8080  
5. GitHub Actions/Azure DevOps: restore → build → test on PR  
6. On main: publish artifact or push image; sketch staging deploy  

---

## 🔗 Depends on

| Module | Why |
|--------|-----|
| Module 3 — Web API | Host model, configuration, middleware |
| Module 5 — Auth | JWT keys as secrets |
| Module 7 — Advanced | Logging/health for smoke tests |
| Module 8 — Testing | `dotnet test` in CI |
| Module 9 — Integrations | CORS origins per environment |

---

## ✅ Completion checklist

- [ ] Set and use `ASPNETCORE_ENVIRONMENT` correctly  
- [ ] Layer appsettings + env vars; keep secrets out of git  
- [ ] Publish Release builds and explain FDD vs SCD  
- [ ] Recognize deps.json / runtimeconfig / appsettings in output  
- [ ] Explain Kestrel behind IIS or Nginx  
- [ ] Build/run a multi-stage API container  
- [ ] Describe CI stages and CD promotion with one artifact  
- [ ] Plan smoke tests and rollback at a high level  

---

## ⏭️ Next

Production observability, infrastructure as code, Kubernetes, or a full capstone release of your sample Shop API.
