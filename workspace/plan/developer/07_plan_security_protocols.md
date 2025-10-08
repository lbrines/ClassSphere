---
id: "07"
title: "Security Protocols"
version: "4.0"
type: "support"
date: "2025-10-07"
---

# Security Protocols - Zero Trust

## Core Principles

1. **Never Trust, Always Verify**
2. **Least Privilege Access**
3. **Defense in Depth**
4. **Secure by Default**

## Security Layers

### 1. Authentication
- **JWT**: HS256 signing, 24h expiry, refresh rotation
- **OAuth 2.0**: PKCE + State validation, limited scopes
- **Secrets**: Environment variables only, never in code

### 2. Authorization (RBAC)
```
admin > coordinator > teacher > student
```
- Endpoint protection via middleware
- Resource-level permissions
- Role validation on every request

### 3. CORS
```go
AllowOrigins: []string{"http://localhost:4200", "https://app.classsphere.edu"}
AllowMethods: []string{GET, POST, PUT, DELETE}
AllowCredentials: true
```

### 4. Rate Limiting
- **Google API**: 100 requests / 100 seconds per user
- **API Endpoints**: 1000 requests / hour per IP
- **WebSocket**: 100 messages / minute per connection

## Security Scanning

### SAST (Static Application Security Testing)
```bash
# Go
go vet ./...
staticcheck ./...

# Angular
npm run lint
```

### SCA (Software Composition Analysis)
```bash
trivy fs . --severity CRITICAL,HIGH
```

### Secrets Detection
```bash
trivy config . --severity CRITICAL
```

## CI/CD Security Pipeline

```yaml
# .github/workflows/security.yml
- name: Run Trivy scan
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: 'fs'
    severity: 'CRITICAL,HIGH'
    exit-code: '1'  # Fail if vulnerabilities found
```

## Secure Coding Practices

### Input Validation
```go
// Always validate and sanitize
func ValidateInput(input string) error {
    if len(input) > 255 {
        return ErrInputTooLong
    }
    if !isAlphanumeric(input) {
        return ErrInvalidCharacters
    }
    return nil
}
```

### SQL Injection Prevention
```go
// Use parameterized queries
db.Query("SELECT * FROM users WHERE id = ?", userID)
```

### XSS Prevention
```typescript
// Angular sanitizes by default
// For manual: this.sanitizer.sanitize(SecurityContext.HTML, input)
```

## Environment Variables

**Required**:
- `JWT_SECRET`: 32+ chars, rotated every 90 days
- `GOOGLE_CLIENT_ID`: OAuth client ID
- `GOOGLE_CLIENT_SECRET`: OAuth secret
- `REDIS_PASSWORD`: Redis authentication (if used)

**Never Commit**:
- Secrets, API keys, passwords
- `.env` files (use `.env.example` as template)
- Google credentials JSON

## Incident Response

1. **Detection**: Automated alerts via monitoring
2. **Isolation**: Disable compromised accounts/tokens
3. **Investigation**: Review logs, identify scope
4. **Remediation**: Patch vulnerability, rotate secrets
5. **Documentation**: Post-mortem, lessons learned

---

**Reference**: See `../contracts/07_ClassSphere_api_endpoints.md` and `../contracts/11_ClassSphere_deployment.md`.

