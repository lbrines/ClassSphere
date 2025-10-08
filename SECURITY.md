# ClassSphere Security

**Version**: 1.0  
**Last Updated**: 2025-10-08  
**Security Model**: Zero Trust

---

## 🎯 Security Overview

ClassSphere implements defense-in-depth security with multiple layers:

1. **Authentication**: JWT + OAuth 2.0 Google
2. **Authorization**: Role-Based Access Control (RBAC)
3. **Transport**: HTTPS (production)
4. **Input Validation**: All user inputs sanitized
5. **Rate Limiting**: 100 req/100s per user
6. **CORS**: Strict origin control
7. **Secrets Management**: External configuration

---

## 🔐 Authentication

### JWT (JSON Web Tokens)

**Algorithm**: HS256  
**Secret**: Environment variable `JWT_SECRET` (min 32 characters)  
**Expiry**: 60 minutes (configurable)

**Token Structure**:
```json
{
  "sub": "user-id",
  "email": "user@example.com",
  "role": "admin",
  "iss": "classsphere",
  "exp": 1696770000,
  "iat": 1696766400
}
```

**Security Features**:
- ✅ Cryptographically signed (prevents tampering)
- ✅ Expiry enforced (time-boxed access)
- ✅ Issuer validation (prevents token reuse)
- ✅ Role embedded (RBAC enforcement)

**Best Practices**:
- [ ] Use strong secret (≥32 random characters)
- [ ] Rotate JWT_SECRET periodically
- [ ] Set appropriate expiry (60 min recommended)
- [ ] Validate on every protected request

---

### OAuth 2.0 Google

**Flow**: Authorization Code with PKCE  
**Scopes**: openid, email, profile

**PKCE (Proof Key for Code Exchange)**:
```
1. Generate code_verifier (random 128 bytes)
2. Calculate code_challenge = SHA256(code_verifier)
3. Send code_challenge to Google
4. Google returns authorization code
5. Exchange code + code_verifier for tokens
```

**Security Features**:
- ✅ PKCE prevents authorization code interception
- ✅ State parameter prevents CSRF attacks
- ✅ Redirect URI validation
- ✅ Token exchange on backend (secret not exposed to frontend)

**Implementation**:
```go
// backend/internal/adapters/oauth/google_oauth.go
func (g *GoogleOAuth) AuthURL(state string, challenge string) string {
    return config.AuthCodeURL(state,
        oauth2.SetAuthURLParam("code_challenge", challenge),
        oauth2.SetAuthURLParam("code_challenge_method", "S256"),
    )
}
```

---

## 🛡️ Authorization

### Role-Based Access Control (RBAC)

**Roles** (hierarchical):
```
admin           → Full access
  ↓
coordinator     → Program-level access
  ↓
teacher         → Course-level access
  ↓
student         → Personal data only
```

**Implementation**:
```go
// Middleware
func RequireRole(allowedRoles ...domain.Role) echo.MiddlewareFunc {
    return func(next echo.HandlerFunc) echo.HandlerFunc {
        return func(c echo.Context) error {
            user := CurrentUser(c)
            
            for _, allowed := range allowedRoles {
                if user.Role == allowed {
                    return next(c)
                }
            }
            
            return echo.ErrForbidden
        }
    }
}

// Usage
api.GET("/admin/ping", handler, RequireRole(domain.RoleAdmin))
```

**Security Principle**: Enforce on backend (never trust frontend)

---

## 🔒 Secrets Management

### ❌ NEVER Do This

```bash
# ❌ Hardcoded in code
const JWT_SECRET = "my-secret-key"

# ❌ Committed to Git
.env with secrets committed

# ❌ Passed as build args
docker build --build-arg JWT_SECRET=secret .
```

### ✅ Best Practices

#### Development

```bash
# 1. Use .env file (git ignored)
# .env
JWT_SECRET=development-secret-key
GOOGLE_CLIENT_ID=dev-client-id

# 2. Load from environment
export JWT_SECRET="$(cat /secure/location/jwt_secret.txt)"

# 3. Use Dev Containers secrets
# devcontainer.json
{
  "remoteEnv": {
    "JWT_SECRET": "${localEnv:JWT_SECRET}"
  }
}
```

#### Production

```bash
# 1. Docker Secrets (Swarm/Kubernetes)
docker secret create jwt_secret jwt_secret.txt

# 2. Cloud Provider Secrets
# AWS: Secrets Manager
# GCP: Secret Manager
# Azure: Key Vault

# 3. Environment variables (from secure storage)
docker run -e JWT_SECRET="$(aws secretsmanager get-secret-value --secret-id prod/jwt-secret --query SecretString --output text)" ...
```

---

## 🚨 Common Vulnerabilities (Prevented)

### SQL Injection ✅ PREVENTED

**Why Safe**: Using prepared statements (future PostgreSQL migration)
```go
// ✅ SAFE: Parameterized query
db.Where("email = ?", email).First(&user)

// ❌ UNSAFE: String concatenation
db.Raw("SELECT * FROM users WHERE email = '" + email + "'")
```

**Current**: Memory repository (no SQL)

---

### XSS (Cross-Site Scripting) ✅ PREVENTED

**Frontend**: Angular sanitizes by default  
**Backend**: JSON responses (no HTML rendering)

```typescript
// ✅ Angular automatic sanitization
<div>{{ userInput }}</div>

// ⚠️ Bypass only when necessary (rare)
<div [innerHTML]="trustedHTML"></div>
```

---

### CSRF (Cross-Site Request Forgery) ✅ PREVENTED

**OAuth State Parameter**:
```go
// Generate random state
state := generateRandomString(32)

// Store in cache
cache.Set(ctx, "oauth:state:"+state, codeVerifier, 10*time.Minute)

// Validate on callback
cachedVerifier, err := cache.Get(ctx, "oauth:state:"+state)
if err != nil {
    return echo.ErrUnauthorized // Invalid state
}
```

**API**: Protected by JWT (no cookies, no CSRF risk)

---

### JWT Attacks ✅ MITIGATED

**Algorithm Confusion**: Fixed to HS256
```go
token, err := jwt.ParseWithClaims(tokenString, &Claims{},
    func(token *jwt.Token) (interface{}, error) {
        // Verify algorithm
        if token.Method.Alg() != jwt.SigningMethodHS256.Alg() {
            return nil, fmt.Errorf("unexpected signing method")
        }
        return []byte(jwtSecret), nil
    })
```

**Token Expiry**: Enforced
```go
if claims.ExpiresAt.Before(time.Now()) {
    return echo.ErrUnauthorized
}
```

---

## 🔍 Security Scanning

### Trivy (Vulnerability Scanner)

```bash
# Scan backend image
trivy image classsphere-backend:latest

# Scan with severity filter
trivy image --severity CRITICAL,HIGH classsphere-backend:latest

# Fail on CRITICAL
trivy image --exit-code 1 --severity CRITICAL classsphere-backend:latest
```

### golangci-lint (SAST)

```bash
# Run security linters
golangci-lint run --enable=gosec ./...

# Check for hardcoded credentials
golangci-lint run --enable=gosec --enable=goconst ./...
```

---

## 🛡️ Production Security Checklist

### Environment

- [ ] `APP_ENV=production`
- [ ] All secrets in secure storage (not .env files)
- [ ] JWT_SECRET rotated and stored securely
- [ ] Google OAuth credentials production-ready
- [ ] Redis password authentication enabled

### Network

- [ ] HTTPS/TLS enabled (nginx reverse proxy or load balancer)
- [ ] CORS restricted to production domains only
- [ ] Firewall rules configured (allow only 80/443)
- [ ] Internal services not exposed (Redis, database)

### Application

- [ ] Rate limiting enabled
- [ ] Input validation on all endpoints
- [ ] Error messages don't leak sensitive info
- [ ] Logging doesn't include secrets
- [ ] Health endpoint doesn't expose internal details

### Docker

- [ ] Running as non-root user
- [ ] Using minimal base images (alpine/distroless)
- [ ] No secrets in Dockerfile or layers
- [ ] Security scanning in CI/CD
- [ ] Images signed and verified

---

## 🔑 Password Security

### Storage

**Algorithm**: bcrypt  
**Cost**: 10 (default, adjustable for security/performance)

```go
// Hash password
hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)

// Verify password
err := bcrypt.CompareHashAndPassword(hashedPassword, []byte(inputPassword))
```

**Never**:
- [ ] Store passwords in plaintext
- [ ] Use MD5 or SHA1 for passwords
- [ ] Log passwords
- [ ] Return passwords in API responses

---

## 🌐 CORS Configuration

### Development

```go
e.Use(middleware.CORSWithConfig(middleware.CORSConfig{
    AllowOrigins: []string{"http://localhost:4200"},
    AllowMethods: []string{echo.GET, echo.POST, echo.PUT, echo.DELETE},
    AllowHeaders: []string{echo.HeaderAuthorization, echo.HeaderContentType},
    AllowCredentials: true,
}))
```

### Production

```go
e.Use(middleware.CORSWithConfig(middleware.CORSConfig{
    AllowOrigins: []string{
        "https://classsphere.com",
        "https://app.classsphere.com",
    },
    AllowMethods: []string{echo.GET, echo.POST, echo.PUT, echo.DELETE},
    AllowHeaders: []string{echo.HeaderAuthorization, echo.HeaderContentType},
    AllowCredentials: true,
    MaxAge: 3600,
}))
```

---

## 🚦 Rate Limiting

### Configuration

**Limits**:
- Public endpoints: 20 req/60s
- Authenticated endpoints: 100 req/100s per user

**Implementation**:
```go
e.Use(middleware.RateLimiter(middleware.NewRateLimiterMemoryStore(100)))
```

**Response** (429 Too Many Requests):
```json
{
  "message": "Rate limit exceeded. Try again in 45 seconds."
}
```

---

## 📝 Security Audit Log

### Events to Log

- [ ] Authentication attempts (success/failure)
- [ ] Authorization failures
- [ ] Rate limit violations
- [ ] Invalid JWT tokens
- [ ] OAuth errors
- [ ] Configuration changes

**Format**: Structured JSON logging
```go
logger.Warn("authentication failed",
    slog.String("email", email),
    slog.String("ip", clientIP),
    slog.String("reason", "invalid password"),
)
```

---

## 🔔 Incident Response

### Security Incident Procedure

1. **Detect**: Monitor logs, alerts, user reports
2. **Contain**: Disable affected accounts, rotate secrets
3. **Investigate**: Review logs, identify attack vector
4. **Remediate**: Patch vulnerability, deploy fix
5. **Document**: Post-mortem, lessons learned

---

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Go Security Checklist](https://github.com/Checkmarx/Go-SCP)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [OAuth 2.0 Security](https://tools.ietf.org/html/rfc6819)

---

**Version**: 1.0  
**Last Security Audit**: 2025-10-08  
**Next Review**: Monthly

