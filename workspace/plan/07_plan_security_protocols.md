---
id: "07"
title: "Security Protocols"
priority: "CRITICAL"
version: "1.0"
date: "2025-10-07"
---

# Security Protocols - ClassSphere

## Zero Trust Principle

**Never trust, always verify.** All code, especially AI-generated, must be verified before deployment.

## Security Layers

### 1. Authentication & Authorization
```yaml
JWT Tokens:
  - HS256 signing algorithm
  - 24-hour expiration
  - Refresh token rotation
  - Secure httpOnly cookies

OAuth 2.0 Google:
  - PKCE flow
  - State parameter validation
  - Secure redirect URLs
  - Token validation

Role-Based Access:
  - admin > coordinator > teacher > student
  - Middleware authorization
  - Endpoint-level permissions
```

### 2. Input Validation
- All user input sanitized
- Go struct validation with tags
- Angular reactive forms with validators
- SQL injection prevention (using parameterized queries)
- XSS prevention (Angular auto-escapes)

### 3. Rate Limiting
```go
// Rate limiting per endpoint
e.Use(middleware.RateLimiter(middleware.NewRateLimiterMemoryStore(20)))

// Custom per-user rate limits
type RateLimiter struct {
    requests map[string]int
    limit    int
}
```

### 4. CORS Configuration
```go
e.Use(middleware.CORSWithConfig(middleware.CORSConfig{
    AllowOrigins: []string{"http://localhost:4200"},
    AllowMethods: []string{"GET", "POST", "PUT", "DELETE"},
    AllowHeaders: []string{"Authorization", "Content-Type"},
    AllowCredentials: true,
}))
```

### 5. Secrets Management
- Never commit secrets to git
- Use environment variables
- .env files in .gitignore
- Kubernetes secrets in production

```bash
# .env.example
JWT_SECRET=change-me-in-production
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
REDIS_URL=redis://localhost:6379
```

## Security Scanning

### SAST (Static Application Security Testing)
```bash
# Trivy for Go
trivy fs --severity HIGH,CRITICAL ./backend

# Trivy for Docker images
trivy image classsphere-backend:latest
```

### SCA (Software Composition Analysis)
```bash
# Go dependencies
go list -m all | nancy sleuth

# npm audit
npm audit --audit-level=high
```

### Secrets Detection
```bash
# gitleaks
gitleaks detect --source . --verbose

# trufflehog
trufflehog filesystem . --only-verified
```

## Security Checklist

### Code Review
- [ ] No hardcoded secrets
- [ ] Input validation implemented
- [ ] Error messages don't leak sensitive info
- [ ] Authentication required on protected endpoints
- [ ] Authorization checks for role-based access
- [ ] Rate limiting configured
- [ ] CORS properly configured

### Deployment
- [ ] HTTPS enabled
- [ ] Security headers configured
- [ ] Secrets in environment variables
- [ ] Database credentials secured
- [ ] Redis password protected
- [ ] Trivy scan passed (0 critical vulnerabilities)

### CI/CD Pipeline
```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Trivy filesystem scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'
      
      - name: Run gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Run npm audit
        working-directory: ./frontend
        run: npm audit --audit-level=high
      
      - name: Run Go security check
        working-directory: ./backend
        run: go list -m all | nancy sleuth
```

## Incident Response

### If Secret Leaked
1. **Immediately rotate** compromised credentials
2. **Revoke** leaked tokens
3. **Audit** access logs
4. **Notify** affected users
5. **Document** incident

### If Vulnerability Found
1. **Assess** severity
2. **Patch** immediately if critical
3. **Test** fix thoroughly
4. **Deploy** patch
5. **Monitor** for exploitation attempts

---

**Last updated**: 2025-10-07  
**Security is everyone's responsibility.**

