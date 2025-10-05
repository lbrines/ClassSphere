---
title: "ClassSphere - Protocolos de Seguridad"
version: "1.0"
type: "strategy_document"
context_priority: "CRITICAL"
date: "2025-10-05"
---

[← Plan Principal](01_plan_index.md)

# Protocolos de Seguridad (Cero Confianza)

## Principio de Cero Confianza

**Regla fundamental:** Tratar todo código generado por IA como input de desarrollador junior.

### Verificaciones Obligatorias

1. **Comprensión completa**: Entender qué hace el código y por qué es seguro
2. **Revisión manual**: Revisar cada componente generado
3. **Testing exhaustivo**: Tests de seguridad específicos
4. **Escaneo automático**: Múltiples herramientas de análisis

## Escaneo Automático Obligatorio

### 1. SAST (Static Application Security Testing)

**Backend - Bandit:**
```bash
# Instalar
pip install bandit

# Ejecutar
bandit -r backend/src/ -ll

# Con reporte
bandit -r backend/src/ -ll -f json -o security-report.json
```

**Backend - Semgrep:**
```bash
# Instalar
pip install semgrep

# Ejecutar
semgrep --config=auto backend/src/

# Reglas específicas
semgrep --config=p/owasp-top-ten backend/src/
```

**Frontend - ESLint Security:**
```bash
# Instalar
npm install --save-dev eslint-plugin-security

# Configurar .eslintrc.json
{
  "plugins": ["security"],
  "extends": ["plugin:security/recommended"]
}

# Ejecutar
npm run lint
```

### 2. SCA (Software Composition Analysis)

**Backend - Safety:**
```bash
# Instalar
pip install safety

# Ejecutar
safety check

# Con reporte
safety check --json > dependencies-report.json
```

**Backend - pip-audit:**
```bash
# Instalar
pip install pip-audit

# Ejecutar
pip-audit

# Con fix automático
pip-audit --fix
```

**Frontend - npm audit:**
```bash
# Ejecutar
npm audit

# Fix automático
npm audit fix

# Fix forzado (cuidado)
npm audit fix --force
```

### 3. Detección de Secretos

**TruffleHog:**
```bash
# Instalar
pip install trufflehog

# Escanear filesystem
trufflehog filesystem backend/ --json

# Escanear Git history
trufflehog git file://. --since-commit HEAD~10
```

**GitLeaks:**
```bash
# Instalar
brew install gitleaks

# Escanear
gitleaks detect --source . --verbose

# Pre-commit hook
gitleaks protect --staged
```

### 4. Container Security

**Trivy:**
```bash
# Instalar
brew install aquasecurity/trivy/trivy

# Escanear imagen
trivy image classsphere-backend:latest

# Escanear con severidad
trivy image --severity HIGH,CRITICAL classsphere-backend:latest

# Escanear filesystem
trivy fs backend/
```

## Prompt Engineering de Seguridad

### Template Obligatorio para Generación de Código

```
"Genera [componente] con los siguientes requisitos de seguridad:

1. Validación de entrada:
   - Sanitización de todos los inputs
   - Validación de tipos con Pydantic/TypeScript
   - Límites de tamaño de datos

2. Autenticación y Autorización:
   - JWT tokens con expiración
   - Verificación de roles en cada endpoint
   - Rate limiting implementado

3. Seguridad de Datos:
   - Hash de contraseñas con bcrypt
   - Encriptación de datos sensibles
   - No exponer información en errores

4. Protección contra Ataques:
   - CSRF protection
   - XSS prevention
   - SQL injection prevention (usar ORMs)
   - Path traversal prevention

5. Logging y Monitoreo:
   - Log de eventos de seguridad
   - No logear datos sensibles
   - Alertas para actividad sospechosa

6. Dependencias:
   - Usar versiones específicas
   - Verificar vulnerabilidades conocidas
   - Actualizar regularmente"
```

### Ejemplos de Prompts Seguros

**Para endpoints:**
```
"Crea un endpoint POST /api/v1/users que:
- Valide email con regex estricto
- Requiera contraseña mínimo 8 caracteres
- Implemente rate limiting (5 requests/minuto)
- Hash password con bcrypt
- Retorne 201 sin exponer datos sensibles
- Maneje errores sin revelar información del sistema"
```

**Para componentes frontend:**
```
"Crea un componente LoginForm que:
- Valide inputs antes de enviar
- Sanitice datos de usuario
- Maneje tokens de forma segura (httpOnly cookies)
- Implemente CSRF protection
- Muestre errores genéricos al usuario
- No exponga información técnica en errores"
```

## Checklist de Seguridad por Fase

### Fase 1 - Fundaciones
- [ ] JWT tokens con expiración configurada
- [ ] Passwords hasheados con bcrypt (cost factor ≥12)
- [ ] CORS configurado correctamente
- [ ] Rate limiting en endpoints de auth
- [ ] Validación de entrada con Pydantic
- [ ] Secrets en variables de entorno
- [ ] HTTPS en producción
- [ ] Security headers configurados

### Fase 2 - Google Integration
- [ ] OAuth 2.0 con PKCE implementado
- [ ] State validation en OAuth
- [ ] Tokens Google almacenados de forma segura
- [ ] Scopes mínimos necesarios
- [ ] Validación de tokens Google
- [ ] Rate limiting en endpoints Google
- [ ] Manejo seguro de errores API

### Fase 3 - Visualización
- [ ] WebSocket con autenticación
- [ ] Validación de mensajes WebSocket
- [ ] XSS prevention en búsqueda
- [ ] Sanitización de inputs de búsqueda
- [ ] Rate limiting en búsqueda
- [ ] Validación de filtros

### Fase 4 - Integración
- [ ] Backup encriptado
- [ ] Logs sin datos sensibles
- [ ] Webhooks con signature validation
- [ ] Acceso admin con 2FA (opcional)
- [ ] Audit trail completo
- [ ] Security monitoring activo

## Configuración de Security Headers

**Backend - FastAPI Middleware:**
```python
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://classsphere.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    max_age=3600,
)

# Trusted hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["classsphere.com", "*.classsphere.com"]
)

# Security headers
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response
```

**Frontend - Next.js Headers:**
```javascript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on'
          },
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=63072000; includeSubDomains; preload'
          },
          {
            key: 'X-Frame-Options',
            value: 'SAMEORIGIN'
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff'
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block'
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin'
          }
        ]
      }
    ]
  }
}
```

## Pipeline de Seguridad CI/CD

```yaml
name: Security Scan

on: [push, pull_request]

jobs:
  security-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: SAST - Bandit
        run: |
          pip install bandit
          bandit -r backend/src/ -ll
      
      - name: SCA - Safety
        run: |
          pip install safety
          safety check
      
      - name: Secrets - TruffleHog
        run: |
          pip install trufflehog
          trufflehog filesystem backend/ --json

  security-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: npm audit
        run: |
          cd frontend
          npm audit --audit-level=high
      
      - name: ESLint Security
        run: |
          cd frontend
          npm run lint

  container-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build images
        run: docker-compose build
      
      - name: Trivy scan
        run: |
          docker run aquasec/trivy image \
            --severity HIGH,CRITICAL \
            classsphere-backend:latest
```

## Manejo Seguro de Secretos

### Variables de Entorno
```bash
# .env (NUNCA commitear)
SECRET_KEY=generate-with-openssl-rand-hex-32
GOOGLE_CLIENT_SECRET=from-google-cloud-console
DATABASE_URL=postgresql://user:pass@localhost/db

# Generar SECRET_KEY seguro
openssl rand -hex 32
```

### GitHub Secrets
```bash
# Configurar en GitHub
gh secret set SECRET_KEY
gh secret set GOOGLE_CLIENT_SECRET
gh secret set DATABASE_URL
```

### Docker Secrets
```yaml
# docker-compose.yml
services:
  backend:
    secrets:
      - secret_key
      - google_client_secret

secrets:
  secret_key:
    file: ./secrets/secret_key.txt
  google_client_secret:
    file: ./secrets/google_client_secret.txt
```

## Comandos de Verificación de Seguridad

```bash
# Scan completo backend
bandit -r backend/src/ -ll && \
safety check && \
trufflehog filesystem backend/ --json

# Scan completo frontend
cd frontend && \
npm audit && \
npm run lint

# Scan containers
trivy image classsphere-backend:latest && \
trivy image classsphere-frontend:latest

# Verificar secrets en Git history
gitleaks detect --source . --verbose

# Test de penetración básico (OWASP ZAP)
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t http://localhost:8000
```

## Respuesta a Incidentes

### Protocolo de Respuesta

1. **Detección**: Identificar el incidente
2. **Contención**: Aislar el sistema afectado
3. **Erradicación**: Eliminar la amenaza
4. **Recuperación**: Restaurar servicios
5. **Lecciones aprendidas**: Documentar y mejorar

### Contactos de Emergencia
```yaml
Security Team:
  - Email: security@classsphere.edu
  - Phone: +1-XXX-XXX-XXXX
  - Slack: #security-incidents

Escalation:
  - Level 1: Team Lead
  - Level 2: CTO
  - Level 3: CEO
```

---

[← Plan Principal](01_plan_index.md)
