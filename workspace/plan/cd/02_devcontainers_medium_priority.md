---
id: "devcontainers-02"
title: "ClassSphere Dev Containers - Day 3: Security & Resource Management"
version: "1.0"
priority: "MEDIUM"
tokens: "<1000"
date: "2025-10-07"
context_id: "medium-devcontainers-day3"
previous: "01_devcontainers_high_priority.md"
next: "03_devcontainers_low_priority.md"
---

# Day 3: Security & Resource Management (MEDIUM Priority)

## 🎯 INICIO: Security Objectives

### Context ID Tracking

```json
{
  "context_id": "medium-devcontainers-day3",
  "priority": "MEDIUM",
  "token_budget": 1000,
  "memory_management": {
    "chunk_position": "middle",
    "lost_in_middle_risk": "medium"
  }
}
```

### Security Targets

| Security Item | Status | Action |
|---|---|---|
| Non-root user | ⚠️ Partial | Complete all containers |
| Secrets management | ❌ Missing | Implement .env strategy |
| Vulnerability scan | ❌ Missing | Add Trivy workflow |
| Resource limits | ⚠️ Basic | Fine-tune per service |

---

## 📅 MEDIO: Implementation

### 3.1 Non-Root User (All Containers)

**Verify Dockerfiles have USER directive**:

```dockerfile
# All Dockerfiles must include:
RUN adduser -D -u 1000 vscode
USER vscode
```

### 3.2 Secrets Management

**File**: `.devcontainer/.env.example`

```bash
# Copy to .env and customize
JWT_SECRET=your-secret-here
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-secret
```

**Add to .gitignore**:
```
.devcontainer/.env
```

**Update docker-compose.yml**:
```yaml
services:
  backend:
    env_file: .env
```

### 3.3 Resource Limits (Fine-Tuned)

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
  
  frontend:
    deploy:
      resources:
        limits:
          cpus: '1.5'
          memory: 1G
  
  redis:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
```

### 3.4 Trivy Security Scan

**File**: `.devcontainer/scripts/security-scan.sh`

```bash
#!/bin/bash
echo "🔒 Running Trivy security scan..."

trivy image classsphere-backend:latest \
  --severity CRITICAL,HIGH \
  --exit-code 1

trivy image classsphere-frontend:latest \
  --severity CRITICAL,HIGH \
  --exit-code 1

echo "✅ Security scan complete"
```

---

## ✅ FINAL: Security Validation

### Day 3 Checklist

- [ ] All containers run as non-root
- [ ] Secrets in .env file (not committed)
- [ ] Resource limits configured
- [ ] Trivy scan shows 0 CRITICAL
- [ ] Total memory usage < 4GB

### Validation Commands

```bash
# Verify non-root
docker exec classsphere-backend whoami  # Should be 'vscode'

# Check resource usage
docker stats --no-stream

# Run security scan
bash .devcontainer/scripts/security-scan.sh
```

**Token Usage**: 950 / 1,000 tokens (MEDIUM priority limit)

