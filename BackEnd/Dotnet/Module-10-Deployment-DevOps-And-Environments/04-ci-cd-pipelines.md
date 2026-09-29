# 🔁 CI/CD Pipelines — Automate Build, Test, and Release

> **Trainer's Note:** Manual “publish from my laptop” doesn’t scale. **CI** validates every change; **CD** ships validated artifacts to environments. This file connects `dotnet test`, publish/Docker, and deployment stages into a beginner-friendly pipeline story.

---

## 📑 Table of Contents
1. [CI vs CD](#1-ci-vs-cd)
2. [Pipeline as a Factory](#2-pipeline-as-a-factory)
3. [Continuous Integration Stages](#3-continuous-integration-stages)
4. [Automating Build and Test](#4-automating-build-and-test)
5. [Static Analysis and Quality Gates](#5-static-analysis-and-quality-gates)
6. [Packaging Artifacts](#6-packaging-artifacts)
7. [Continuous Delivery vs Continuous Deployment](#7-continuous-delivery-vs-continuous-deployment)
8. [Environment Promotion Flow](#8-environment-promotion-flow)
9. [Example: GitHub Actions Sketch](#9-example-github-actions-sketch)
10. [Secrets, Approvals, and Safety](#10-secrets-approvals-and-safety)
11. [Knowledge Check](#11-knowledge-check)

---

## 1. CI vs CD

| Term | Meaning |
|------|---------|
| **CI — Continuous Integration** | Frequently merge changes; automated **build + test** on each change |
| **CD — Continuous Delivery** | Always have a releasable artifact; deploy to prod is a **business click/approval** |
| **CD — Continuous Deployment** | Every green main build **auto-deploys** to production |

```
CI:   change → validate
CD:   validated artifact → environments (with or without auto-prod)
```

Teams say “CD” for either delivery or deployment — clarify in conversation.

---

## 2. Pipeline as a Factory

```
Developer PR/push
        │
        ▼
┌─────────────────── CI ───────────────────┐
│ checkout → setup SDK → restore → build   │
│ → test → analyze → publish/docker build  │
└───────────────────┬──────────────────────┘
                    │ artifacts / image
                    ▼
┌─────────────────── CD ───────────────────┐
│ deploy Staging → smoke → approve → Prod  │
└──────────────────────────────────────────┘
```

| Input | Output |
|-------|--------|
| Source commit | Build status green/red |
| Green CI | Versioned artifact or container image |
| CD job | Running app on target env |

---

## 3. Continuous Integration Stages

Minimal CI for a .NET API:

| Stage | Command / action |
|-------|------------------|
| Checkout | Clone repo at commit SHA |
| Setup .NET | Install SDK (pin via `global.json`) |
| Restore | `dotnet restore` |
| Build | `dotnet build -c Release` |
| Test | `dotnet test -c Release` |
| (Optional) Analyze | analyzers, vulnerability scan |
| (Optional) Publish | `dotnet publish` or `docker build` |

### Triggers
| Event | Typical use |
|-------|-------------|
| Pull request | Validate before merge |
| Push to main | Keep main releasable; maybe deploy staging |
| Tag `v*` | Release pipeline |
| Schedule | Nightly full suite |

---

## 4. Automating Build and Test

```bash
dotnet restore
dotnet build -c Release --no-restore
dotnet test  -c Release --no-build --verbosity normal
```

### Filter and structure
```bash
dotnet test tests/Shop.Domain.Tests
dotnet test tests/Shop.Api.Tests
dotnet test --filter Category=Unit
```

### Fail the pipeline if tests fail
Non-zero exit code → CI red → block merge (with branch protection).

### Pin SDK
```json
// global.json
{
  "sdk": {
    "version": "8.0.400",
    "rollForward": "latestFeature"
  }
}
```

Reproducible agents beat “whatever SDK is installed.”

---

## 5. Static Analysis and Quality Gates

Beyond tests:

| Check | Purpose |
|-------|---------|
| Compiler warnings as errors | Prevent rot (`-warnaserror`) |
| Roslyn analyzers | Catch code issues |
| `dotnet format --verify-no-changes` | Style gate (optional) |
| `dotnet list package --vulnerable` | Known vulnerable packages |
| Coverage thresholds | Optional floor on critical projects |

```bash
dotnet build -c Release -warnaserror
dotnet list package --vulnerable --include-transitive
```

### Keep PR pipelines fast
```
PR CI (fast path):
  build + unit + critical integration

Nightly:
  full integration + e2e smoke + deeper scans
```

---

## 6. Packaging Artifacts

After green tests, produce something deployable:

### A) Folder publish artifact
```bash
dotnet publish src/Shop.Api -c Release -o artifacts/api
# zip artifacts/api and store as pipeline artifact
```

### B) Container image
```bash
docker build -t ghcr.io/org/shop-api:${GIT_SHA} .
docker push ghcr.io/org/shop-api:${GIT_SHA}
```

### Versioning artifacts
| Tag style | Example |
|-----------|---------|
| Git SHA | `shop-api:a1b2c3d` |
| Semver | `shop-api:1.4.0` |
| Build id | `shop-api:2026.03.21.88` |

Always know **which commit** is running in production.

---

## 7. Continuous Delivery vs Continuous Deployment

| Continuous **Delivery** | Continuous **Deployment** |
|-------------------------|---------------------------|
| Deploy **ready** anytime | Deploy **happens** automatically |
| Human approval for prod often | Prod auto if tests green |
| Common for regulated apps | Common for high-trust web products |

Both require strong CI confidence (Module 8 testing culture).

---

## 8. Environment Promotion Flow

```
Commit
  → CI green
  → Deploy Staging (auto)
  → Smoke tests on Staging
  → Manual approval
  → Deploy Production (same artifact!)
```

### Golden rule
**Same artifact** progresses through environments — don’t rebuild different bits “only for prod.”

| Bad | Good |
|-----|------|
| Rebuild from main later with new commits | Promote image `sha-a1b2` staging → prod |
| Hotfix only on server | Fix in git → new CI → redeploy |

### Smoke tests after deploy
```bash
curl -f https://staging-api.shop.com/health
curl -f https://staging-api.shop.com/api/products
# optional: login + one authorized call
```

---

## 9. Example: GitHub Actions Sketch

`.github/workflows/ci-cd.yml` (illustrative):

```yaml
name: shop-api-ci-cd

on:
  pull_request:
    branches: [ main ]
  push:
    branches: [ main ]

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-dotnet@v4
        with:
          global-json-file: global.json

      - name: Restore
        run: dotnet restore

      - name: Build
        run: dotnet build -c Release --no-restore

      - name: Test
        run: dotnet test -c Release --no-build --verbosity normal

      - name: Publish
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        run: dotnet publish src/Shop.Api -c Release --no-build -o artifacts/api

      - name: Upload artifact
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        uses: actions/upload-artifact@v4
        with:
          name: shop-api
          path: artifacts/api

  deploy-staging:
    needs: ci
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Download artifact
        uses: actions/download-artifact@v4
        with:
          name: shop-api
          path: artifacts/api
      - name: Deploy to staging
        run: echo "Deploy artifacts/api to staging host/App Service here"
        # real step: azure/webapps-deploy, kubectl, ssh, etc.
```

Azure DevOps, GitLab CI, and Jenkins use the same stage ideas with different YAML/UI.

### Docker-centric variant
CI builds/pushes image → CD sets image tag on App Service/K8s/ECS.

---

## 10. Secrets, Approvals, and Safety

### Pipeline secrets
| Secret | Storage |
|--------|---------|
| Deploy credentials | CI secret store / OIDC federation |
| Connection strings for smoke | Env-scoped secrets |
| NuGet private feed tokens | CI secrets |

Never echo secrets in logs.

### Environment protections
- Required reviewers for **production** environment  
- Branch protection: green CI before merge  
- Restrict who can approve prod  
- Separate staging/prod credentials  

### Rollback
| Strategy | Idea |
|----------|------|
| Previous image tag | Redeploy last known good SHA |
| Deployment slots | Swap back (App Service) |
| DB migrations | Expand/contract (Module 4) so rollback stays possible |

```
Safety loop:

  automated tests
    → limited prod credentials
    → approval gates
    → smoke tests
    → fast rollback path
```

---

## 11. Knowledge Check

**Q1.** CI vs Continuous Deployment in one sentence each?  
**Q2.** What are the essential CI commands for a .NET API?  
**Q3.** Why pin the SDK with `global.json`?  
**Q4.** Why promote the same artifact from staging to production?  
**Q5.** Name two quality checks beyond `dotnet test`.  
**Q6.** Where should deploy secrets live?  
**Q7.** What is a post-deploy smoke test?

### Mini practice
1. Ensure PR-triggered `dotnet restore/build/test` works in a workflow file  
2. Add publish on main and upload artifact (or docker build)  
3. Define staging vs production environments mentally with approval on prod  
4. Write smoke curl steps for `/health`  
5. Document your rollback plan (previous tag)  
6. Connect branch protection to require CI green  

### Answers (short)
1. CI validates every integrate; continuous deployment auto-ships green builds to prod  
2. restore, build, test (then publish/image)  
3. Reproducible builds across agents  
4. Guarantee what you tested is what you ship  
5. warnaserror, vulnerability scan, format, coverage…  
6. Pipeline secret store / cloud IAM — not the repo  
7. Quick real-environment check that the new deploy responds correctly  

---

## ✅ What You Should Feel Confident About

- [ ] Explain CI and CD clearly  
- [ ] Sketch a .NET PR pipeline (restore/build/test)  
- [ ] Add static analysis/vulnerability gates at a high level  
- [ ] Package publish folders or container images as artifacts  
- [ ] Describe staging → prod promotion with the same artifact  
- [ ] Keep secrets and approvals out of cowboy deploys  

**Previous:** [03-hosting-options-and-containers.md](./03-hosting-options-and-containers.md)

---

## 🚀 Module 10 Wrap-Up

You can take an ASP.NET Core Web API from laptop to production path:

| Skill | File |
|-------|------|
| Dev/Staging/Prod config, env vars, secrets | 01 |
| `dotnet publish`, FDD vs SCD, output files | 02 |
| IIS/Kestrel/Nginx, App Service, Docker multi-stage | 03 |
| CI build/test/analyze + CD release pipelines | 04 |

### Laptop → production checklist
- [ ] Environment name set correctly everywhere  
- [ ] Secrets from user-secrets/env/vault — never git  
- [ ] Release publish tested locally  
- [ ] Host chosen (IIS / proxy / PaaS / container)  
- [ ] Container image optional but consistent  
- [ ] CI runs tests on every PR  
- [ ] CD deploys the **same** artifact to staging then prod  
- [ ] Smoke tests + rollback plan  

```
Code + config
  → CI validates
  → publish/image
  → staging
  → approve
  → production
```

**Suggested next:** Observability in production (metrics/traces), infrastructure as code, Kubernetes basics, or a capstone releasing your sample API through a real pipeline.
