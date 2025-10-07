---
title: "ClassSphere - Protocolos de Seguridad"
version: "3.0"
type: "development_plan"
related_files:
  - "contracts/principal/09_ClassSphere_testing.md"
  - "contracts/extra/SOFTWARE_PROJECT_BEST_PRACTICES.md"
---

# Protocolos de Seguridad - Principio de Cero Confianza

## Principio de Cero Confianza

### Definición
Nunca confiar, siempre verificar. Cada request, cada usuario, cada operación debe ser autenticada y autorizada explícitamente.

### Implementación
- **Autenticación obligatoria**: JWT + OAuth 2.0 Google con PKCE
- **Autorización granular**: Sistema de roles jerárquico
- **Validación estricta**: Go structs con tags + Angular validators
- **Auditoría completa**: Logs estructurados de todas las operaciones

## Autenticación y Autorización

### JWT Implementation
```go
// internal/auth/jwt.go
type JWTClaims struct {
    Email string `json:"email"`
    Role  string `json:"role"`
    UserID string `json:"user_id"`
    jwt.StandardClaims
}

func GenerateJWT(user *User) (string, error) {
    claims := &JWTClaims{
        Email: user.Email,
        Role:  user.Role,
        UserID: user.ID,
        StandardClaims: jwt.StandardClaims{
            ExpiresAt: time.Now().Add(time.Hour * 24).Unix(),
            IssuedAt:  time.Now().Unix(),
            Issuer:    "classsphere",
        },
    }
    
    token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
    return token.SignedString([]byte(os.Getenv("JWT_SECRET")))
}
```

### OAuth 2.0 Google con PKCE
```go
// internal/auth/oauth.go
type GoogleOAuth struct {
    ClientID     string
    ClientSecret string
    RedirectURL  string
    Scopes       []string
}

func (g *GoogleOAuth) GeneratePKCE() (string, string, error) {
    // Generate code verifier
    verifier := make([]byte, 32)
    if _, err := rand.Read(verifier); err != nil {
        return "", "", err
    }
    
    codeVerifier := base64.URLEncoding.WithPadding(base64.NoPadding).EncodeToString(verifier)
    
    // Generate code challenge
    hash := sha256.Sum256([]byte(codeVerifier))
    codeChallenge := base64.URLEncoding.WithPadding(base64.NoPadding).EncodeToString(hash[:])
    
    return codeVerifier, codeChallenge, nil
}
```

### Sistema de Roles Jerárquico
```go
// internal/auth/roles.go
type Role string

const (
    RoleAdmin      Role = "admin"
    RoleCoordinator Role = "coordinator"
    RoleTeacher    Role = "teacher"
    RoleStudent    Role = "student"
)

var roleHierarchy = map[Role]int{
    RoleAdmin:      4,
    RoleCoordinator: 3,
    RoleTeacher:    2,
    RoleStudent:    1,
}

func (r Role) CanAccess(targetRole Role) bool {
    return roleHierarchy[r] >= roleHierarchy[targetRole]
}
```

## Escaneo Automático de Seguridad

### SAST (Static Application Security Testing)
```yaml
# .github/workflows/security.yml
name: Security Scanning

on: [push, pull_request]

jobs:
  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Gosec
        uses: securecodewarrior/github-action-gosec@master
        with:
          args: './...'
      
      - name: Run Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/secrets
            p/owasp-top-ten
```

### SCA (Software Composition Analysis)
```yaml
  sca:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Run npm audit
        run: |
          cd frontend
          npm audit --audit-level moderate
```

### Secrets Detection
```yaml
  secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Run TruffleHog
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: main
          head: HEAD
          extra_args: --debug --only-verified
```

## Prompt Engineering de Seguridad

### Principios de Seguridad en Prompts
1. **Validación de Input**: Siempre validar y sanitizar inputs
2. **Principio de Menor Privilegio**: Mínimos permisos necesarios
3. **Defensa en Profundidad**: Múltiples capas de seguridad
4. **Auditoría Continua**: Monitoreo y logging de seguridad

### Templates de Seguridad
```go
// internal/middleware/security.go
func SecurityMiddleware() echo.MiddlewareFunc {
    return func(next echo.HandlerFunc) echo.HandlerFunc {
        return func(c echo.Context) error {
            // Rate limiting
            if !rateLimiter.Allow(c.RealIP()) {
                return echo.NewHTTPError(429, "Too Many Requests")
            }
            
            // CORS
            c.Response().Header().Set("Access-Control-Allow-Origin", "*")
            c.Response().Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
            c.Response().Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
            
            // Security headers
            c.Response().Header().Set("X-Content-Type-Options", "nosniff")
            c.Response().Header().Set("X-Frame-Options", "DENY")
            c.Response().Header().Set("X-XSS-Protection", "1; mode=block")
            c.Response().Header().Set("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
            
            return next(c)
        }
    }
}
```

## Pipeline de Seguridad CI/CD

### Pre-commit Hooks
```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🔒 Running security checks..."

# Check for secrets
if grep -r "password\|secret\|key" --include="*.go" --include="*.ts" . | grep -v "test\|mock"; then
    echo "❌ Potential secrets found in code"
    exit 1
fi

# Check for hardcoded URLs
if grep -r "http://\|https://" --include="*.go" --include="*.ts" . | grep -v "localhost\|test"; then
    echo "❌ Hardcoded URLs found"
    exit 1
fi

# Run security tests
go test ./internal/security/... -v
if [ $? -ne 0 ]; then
    echo "❌ Security tests failed"
    exit 1
fi

echo "✅ Security checks passed"
```

### CI/CD Security Pipeline
```yaml
# .github/workflows/security-pipeline.yml
name: Security Pipeline

on: [push, pull_request]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run security tests
        run: |
          go test ./internal/security/... -v
          npm run test:security
      
      - name: SAST Scanning
        run: |
          gosec ./...
          semgrep --config=auto .
      
      - name: SCA Scanning
        run: |
          trivy fs .
          npm audit --audit-level moderate
      
      - name: Secrets Detection
        run: |
          trufflehog filesystem . --only-verified
      
      - name: Upload security results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

## Validación de Seguridad

### Tests de Seguridad
```go
// tests/security/auth_test.go
func TestJWTSecurity(t *testing.T) {
    // Test token expiration
    user := &User{Email: "test@example.com", Role: "admin"}
    token, err := GenerateJWT(user)
    assert.NoError(t, err)
    
    // Test invalid token
    invalidToken := "invalid.token.here"
    _, err = ValidateJWT(invalidToken)
    assert.Error(t, err)
    
    // Test expired token
    expiredToken := generateExpiredToken(user)
    _, err = ValidateJWT(expiredToken)
    assert.Error(t, err)
}

func TestRoleAuthorization(t *testing.T) {
    // Test admin can access all roles
    assert.True(t, RoleAdmin.CanAccess(RoleStudent))
    assert.True(t, RoleAdmin.CanAccess(RoleTeacher))
    assert.True(t, RoleAdmin.CanAccess(RoleCoordinator))
    
    // Test student cannot access admin
    assert.False(t, RoleStudent.CanAccess(RoleAdmin))
    
    // Test teacher can access student
    assert.True(t, RoleTeacher.CanAccess(RoleStudent))
}
```

### Tests de Penetración
```typescript
// e2e/security.e2e-spec.ts
import { test, expect } from '@playwright/test';

test.describe('Security Tests', () => {
  test('should prevent SQL injection', async ({ page }) => {
    await page.goto('/login');
    
    // Attempt SQL injection
    await page.fill('[data-testid="email"]', "admin@test.com'; DROP TABLE users; --");
    await page.fill('[data-testid="password"]', 'password');
    await page.click('[data-testid="login-button"]');
    
    // Should show error, not crash
    await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
  });

  test('should prevent XSS attacks', async ({ page }) => {
    await page.goto('/search');
    
    // Attempt XSS
    await page.fill('[data-testid="search-input"]', '<script>alert("XSS")</script>');
    await page.click('[data-testid="search-button"]');
    
    // Should not execute script
    await expect(page.locator('script')).toHaveCount(0);
  });

  test('should enforce HTTPS in production', async ({ page }) => {
    await page.goto('http://localhost:4200');
    
    // Should redirect to HTTPS
    await expect(page).toHaveURL(/^https:/);
  });
});
```

## Monitoreo de Seguridad

### Logs de Seguridad
```go
// internal/security/logger.go
type SecurityLogger struct {
    logger *log.Logger
}

func (sl *SecurityLogger) LogAuthAttempt(email, ip string, success bool) {
    event := SecurityEvent{
        Timestamp: time.Now(),
        Type: "auth_attempt",
        Email: email,
        IP: ip,
        Success: success,
        Severity: getSeverity(success),
    }
    
    sl.logger.Printf("SECURITY: %+v", event)
}

func (sl *SecurityLogger) LogSuspiciousActivity(activity string, details map[string]interface{}) {
    event := SecurityEvent{
        Timestamp: time.Now(),
        Type: "suspicious_activity",
        Activity: activity,
        Details: details,
        Severity: "HIGH",
    }
    
    sl.logger.Printf("SECURITY: %+v", event)
}
```

### Alertas de Seguridad
```yaml
# monitoring/security-alerts.yml
alerts:
  - name: "Multiple Failed Login Attempts"
    condition: "rate(auth_failures[5m]) > 5"
    severity: "WARNING"
    action: "block_ip"
  
  - name: "Unusual API Usage"
    condition: "rate(api_requests[1m]) > 100"
    severity: "CRITICAL"
    action: "throttle"
  
  - name: "Security Scan Failure"
    condition: "security_scan_failed == 1"
    severity: "CRITICAL"
    action: "block_deployment"
```

## Comandos de Verificación

### Verificación de Seguridad
```bash
# Run security tests
go test ./internal/security/... -v

# Run SAST scanning
gosec ./...
semgrep --config=auto .

# Run SCA scanning
trivy fs .
npm audit --audit-level moderate

# Run secrets detection
trufflehog filesystem . --only-verified

# Check security headers
curl -I https://classsphere.com

# Test authentication
curl -X POST https://api.classsphere.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@classsphere.edu","password":"secret"}'
```

### Verificación de Compliance
```bash
# Check OAuth implementation
curl -X GET https://api.classsphere.com/auth/google

# Verify JWT tokens
jwt decode <token>

# Check role permissions
curl -X GET https://api.classsphere.com/admin/dashboard \
  -H "Authorization: Bearer <student-token>"
# Should return 403 Forbidden

# Test rate limiting
for i in {1..10}; do
  curl -X POST https://api.classsphere.com/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"test@example.com","password":"wrong"}'
done
# Should return 429 Too Many Requests
```

## Métricas de Seguridad

### KPIs de Seguridad
- **Vulnerabilidades CRITICAL**: 0
- **Vulnerabilidades HIGH**: 0
- **Vulnerabilidades MEDIUM**: ≤5
- **Cobertura de tests de seguridad**: ≥95%
- **Tiempo de respuesta a incidentes**: <1 hora
- **Compliance**: 100% OAuth 2.0 + JWT + PKCE

### Dashboard de Seguridad
```typescript
// src/app/components/security/security-dashboard.component.ts
export class SecurityDashboardComponent implements OnInit {
  securityMetrics = {
    vulnerabilities: {
      critical: 0,
      high: 0,
      medium: 2,
      low: 5
    },
    authAttempts: {
      successful: 1250,
      failed: 23,
      blocked: 5
    },
    apiUsage: {
      requests: 15420,
      errors: 12,
      rateLimited: 3
    }
  };

  ngOnInit() {
    this.loadSecurityMetrics();
  }

  private loadSecurityMetrics() {
    this.securityService.getMetrics().subscribe(metrics => {
      this.securityMetrics = metrics;
    });
  }
}
```

**Estado**: ✅ PROTOCOLOS DE SEGURIDAD COMPLETOS  
**Principio**: Cero Confianza implementado  
**Escaneo**: SAST + SCA + Secrets Detection  
**Pipeline**: CI/CD con quality gates de seguridad  
**Compliance**: 100% OAuth 2.0 + JWT + PKCE
