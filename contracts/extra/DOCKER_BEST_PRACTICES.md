# Docker Best Practices - Version Agnostic Guide
## Mejores Prácticas de Dockerización - Guía Universal

**Fecha de creación:** 2025-10-02  
**Basado en:** Docker Official Documentation, OWASP, Google Cloud, AWS Best Practices  
**Aplicable a:** Cualquier stack tecnológico (Python, Node.js, Go, Java, etc.)  
**Filosofía:** Principios atemporales, no atados a versiones específicas

---

## 📚 Fuentes Oficiales Consultadas

1. **Docker Official Documentation** - Best practices for writing Dockerfiles
2. **OWASP Container Security** - Security cheat sheet
3. **Google Cloud Run** - Container best practices
4. **AWS ECS/Fargate** - Container deployment guides
5. **CNCF (Cloud Native Computing Foundation)** - Cloud native patterns
6. **Snyk Container Security** - Vulnerability scanning guides

---

## 🎯 Filosofía de Dockerización

### Principios Fundamentales

1. **Inmutabilidad**: Los contenedores son efímeros y reemplazables
2. **Reproducibilidad**: Mismo Dockerfile = misma imagen en cualquier entorno
3. **Mínimalismo**: Solo incluir lo necesario para ejecutar
4. **Seguridad por diseño**: Menor superficie de ataque posible
5. **Optimización**: Imágenes pequeñas, rápidas de construir y desplegar

---

## 📦 1. SELECCIÓN DE IMÁGENES BASE

### 1.1 Tipos de Imágenes Base

#### Full Distribution
```dockerfile
# Ejemplo: debian, ubuntu, centos
FROM python:latest  # ⚠️ ~1GB, incluye compiladores y herramientas
```

**✅ Usar cuando:**
- Necesitas compilar dependencias nativas
- Desarrollo y debugging
- Compatibilidad máxima

**❌ Evitar para:**
- Producción (demasiado grande)
- Imágenes finales

#### Slim/Trimmed
```dockerfile
# Ejemplo: python-slim, node-slim
FROM python:slim  # ✅ ~150-200MB, runtime básico
```

**✅ Usar cuando:**
- Producción con dependencias Python puras
- Balance entre tamaño y compatibilidad
- La mayoría de casos de uso

#### Alpine
```dockerfile
# Ejemplo: alpine, python-alpine, node-alpine
FROM python:alpine  # ⚡ ~50MB, ultra-minimalista
```

**✅ Usar cuando:**
- Máxima optimización de tamaño
- Sin dependencias nativas complejas
- Microservicios

**⚠️ Cuidado con:**
- Incompatibilidades de musl libc vs glibc
- Dependencias que requieren gcc/build-tools
- Tiempos de build más largos (compilación)

#### Distroless (Google)
```dockerfile
# Imágenes sin shell, package manager
FROM gcr.io/distroless/python3
```

**✅ Usar cuando:**
- Seguridad máxima (sin shell = sin shell exploits)
- Producción de alto riesgo
- Cumplimiento normativo estricto

**❌ Evitar para:**
- Debugging (no hay shell)
- Desarrollo

### 1.2 Estrategia de Versionado

#### ❌ MAL: Tag Latest
```dockerfile
FROM python:latest      # Imprevisible, cambia sin aviso
FROM node:latest        # Puede romper builds existentes
```

#### ✅ BIEN: Versión Específica
```dockerfile
# Patrón: <imagen>:<major>.<minor>.<patch>-<variant>
FROM python:3.11.6-slim           # ✅ Reproducible
FROM node:18.17.1-alpine          # ✅ Predecible
FROM nginx:1.25.3-alpine          # ✅ Específico
```

#### ✅ BUENO: Major.Minor (con vigilancia)
```dockerfile
FROM python:3.11-slim    # ⚠️ Actualiza patches automáticamente
FROM node:18-alpine      # ⚠️ Útil pero requiere testing
```

**Recomendación**: Major.Minor para dependencias estables, Major.Minor.Patch para producción crítica.

### 1.3 Matriz de Decisión de Imagen Base

| Stack | Desarrollo | Staging | Producción |
|-------|-----------|---------|------------|
| **Python** | `python:X.Y-full` | `python:X.Y-slim` | `python:X.Y.Z-slim` o `alpine` |
| **Node.js** | `node:X.Y` | `node:X.Y-slim` | `node:X.Y.Z-alpine` |
| **Go** | `golang:X.Y` | `alpine` (compilado) | `scratch` o `distroless` |
| **Java** | `openjdk:X.Y` | `openjdk:X.Y-slim` | `openjdk:X.Y.Z-jre-slim` |
| **Nginx** | `nginx:X.Y` | `nginx:X.Y-alpine` | `nginx:X.Y.Z-alpine` |

---

## 🏗️ 2. MULTI-STAGE BUILDS

### 2.1 Concepto Fundamental

**Problema**: Herramientas de build aumentan tamaño innecesariamente en producción.

**Solución**: Separar build y runtime en stages diferentes.

### 2.2 Patrón Básico

```dockerfile
# ========================================
# Stage 1: Builder (build dependencies)
# ========================================
FROM <base-image>:<version> AS builder

# Instalar herramientas de compilación
RUN install_build_tools

# Copiar archivos de dependencias
COPY dependency_files ./

# Instalar dependencias
RUN install_dependencies

# Copiar código fuente
COPY source_code ./

# Compilar/Build
RUN build_application


# ========================================
# Stage 2: Runtime (solo lo necesario)
# ========================================
FROM <base-image>:<slim-version> AS runtime

# Crear usuario no-root
RUN create_app_user

# Copiar SOLO artefactos necesarios desde builder
COPY --from=builder /build/output /app/

# Cambiar a usuario no-root
USER app_user

# Comando de ejecución
CMD ["run_application"]
```

### 2.3 Ejemplo: Python Backend (FastAPI/Django/Flask)

```dockerfile
# ========================================
# Stage 1: Dependencies Builder
# ========================================
FROM python:slim AS builder

WORKDIR /build

# Instalar dependencias de compilación (si necesario)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copiar solo archivos de dependencias (cache optimization)
COPY requirements.txt .

# Instalar dependencias en directorio de usuario
RUN pip install --no-cache-dir --user -r requirements.txt


# ========================================
# Stage 2: Production Runtime
# ========================================
FROM python:slim AS production

WORKDIR /app

# Instalar solo runtime dependencies (no gcc)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Crear usuario no-privilegiado
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Copiar dependencias instaladas desde builder
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copiar código de aplicación
COPY --chown=appuser:appuser . .

# Configurar PATH para incluir paquetes de usuario
ENV PATH=/home/appuser/.local/bin:$PATH

# Cambiar a usuario no-root
USER appuser

# Exponer puerto (documentación, no abre puerto)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Comando de ejecución
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Beneficio**: ~850MB → ~180MB (79% reducción)

### 2.4 Ejemplo: Node.js Frontend (Next.js/React/Vue)

```dockerfile
# ========================================
# Stage 1: Dependencies Installation
# ========================================
FROM node:alpine AS deps

WORKDIR /app

# Copiar solo archivos de dependencias (mejor cache)
COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./

# Instalar dependencias según package manager detectado
RUN \
  if [ -f pnpm-lock.yaml ]; then \
    corepack enable pnpm && pnpm install --frozen-lockfile; \
  elif [ -f yarn.lock ]; then \
    yarn install --frozen-lockfile; \
  else \
    npm ci; \
  fi


# ========================================
# Stage 2: Application Builder
# ========================================
FROM node:alpine AS builder

WORKDIR /app

# Copiar node_modules desde stage deps
COPY --from=deps /app/node_modules ./node_modules

# Copiar código fuente
COPY . .

# Variables de entorno de build (si necesario)
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# Build de aplicación
RUN \
  if [ -f pnpm-lock.yaml ]; then \
    corepack enable pnpm && pnpm build; \
  elif [ -f yarn.lock ]; then \
    yarn build; \
  else \
    npm run build; \
  fi


# ========================================
# Stage 3: Production Runtime
# ========================================
FROM node:alpine AS runner

WORKDIR /app

ENV NODE_ENV=production

# Crear usuario no-root
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copiar SOLO archivos de producción
# Para Next.js con output: 'standalone'
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/public ./public

# Cambiar a usuario no-root
USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/api/health', (res) => { process.exit(res.statusCode === 200 ? 0 : 1) })"

# Comando de ejecución
CMD ["node", "server.js"]
```

**Beneficio**: ~1.2GB → ~120MB (90% reducción)

### 2.5 Ejemplo: Aplicación Compilada (Go/Rust)

```dockerfile
# ========================================
# Stage 1: Builder
# ========================================
FROM golang:latest AS builder

WORKDIR /build

# Copiar archivos de dependencias
COPY go.mod go.sum ./
RUN go mod download

# Copiar código fuente
COPY . .

# Compilar aplicación estática
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .


# ========================================
# Stage 2: Runtime (imagen mínima)
# ========================================
FROM scratch

# Copiar certificados SSL (si necesario para HTTPS)
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# Copiar binario compilado
COPY --from=builder /build/app /app

# Exponer puerto
EXPOSE 8080

# Comando de ejecución
ENTRYPOINT ["/app"]
```

**Beneficio**: ~800MB → ~10MB (99% reducción)

---

## 🔒 3. SEGURIDAD

### 3.1 Usuarios No-Root (CRÍTICO)

#### ❌ MAL: Ejecutar como Root
```dockerfile
FROM python:slim
COPY . /app
WORKDIR /app
CMD ["python", "app.py"]  # Ejecuta como root (UID 0)
```

**Riesgo**: Si atacante compromete contenedor, tiene permisos root.

#### ✅ BIEN: Crear y Usar Usuario No-Privilegiado
```dockerfile
FROM python:slim

# Crear grupo y usuario con UID/GID específicos
RUN groupadd -r appgroup -g 1000 && \
    useradd -r -u 1000 -g appgroup -m -s /bin/bash appuser

# Crear directorios con permisos apropiados
RUN mkdir -p /app && chown -R appuser:appgroup /app

WORKDIR /app

# Copiar archivos con ownership correcto
COPY --chown=appuser:appgroup . .

# Cambiar a usuario no-root ANTES de CMD
USER appuser

CMD ["python", "app.py"]  # Ejecuta como appuser (UID 1000)
```

#### Verificar Usuario
```bash
# Verificar que contenedor NO corre como root
docker run myimage id
# Debe mostrar: uid=1000(appuser) gid=1000(appgroup)
# NO debe mostrar: uid=0(root)
```

### 3.2 Gestión de Secretos

#### ❌ NUNCA HACER ESTO:
```dockerfile
# ❌ Secretos hardcoded en Dockerfile
ENV DB_PASSWORD=supersecret123
ENV API_KEY=abc123xyz

# ❌ Secretos en argumentos de build
ARG PRIVATE_KEY="-----BEGIN PRIVATE KEY-----..."

# ❌ Copiar archivos con secretos
COPY .env /app/.env
```

**Problema**: Secretos quedan en layers de imagen (permanentes, extraíbles).

#### ✅ SOLUCIONES SEGURAS:

##### Opción 1: Variables de Entorno en Runtime
```bash
# docker run
docker run -e DB_PASSWORD=$(cat secret.txt) myimage

# docker-compose
docker-compose run -e DB_PASSWORD=secret myimage
```

##### Opción 2: Docker Secrets (Swarm/Compose)
```yaml
# docker-compose.yml
services:
  app:
    image: myimage
    secrets:
      - db_password
      - api_key

secrets:
  db_password:
    external: true  # Gestionado externamente
  api_key:
    file: ./secrets/api_key.txt  # Archivo local (NO committear)
```

```dockerfile
# Dockerfile - leer secrets en runtime
FROM python:slim
# Secrets se montan en /run/secrets/ automáticamente
CMD ["sh", "-c", "export DB_PASSWORD=$(cat /run/secrets/db_password) && python app.py"]
```

##### Opción 3: Proveedores Externos
- **AWS Secrets Manager**
- **Azure Key Vault**
- **Google Secret Manager**
- **HashiCorp Vault**

```python
# app.py - obtener secrets desde proveedor
import boto3

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']

db_password = get_secret('prod/db/password')
```

### 3.3 Escaneo de Vulnerabilidades

#### Herramientas Recomendadas

##### Trivy (Open Source)
```bash
# Instalar
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh

# Escanear imagen
trivy image myimage:latest

# Escanear solo severidad CRITICAL y HIGH
trivy image --severity CRITICAL,HIGH myimage:latest

# Fallar build si hay CRITICAL
trivy image --exit-code 1 --severity CRITICAL myimage:latest
```

##### Docker Scan (Snyk)
```bash
# Escanear imagen
docker scan myimage:latest

# Escanear con severidad
docker scan --severity=high myimage:latest
```

##### Clair (Red Hat)
```bash
# Setup con docker-compose
docker-compose -f clair-compose.yml up -d

# Escanear
clairctl analyze myimage:latest
```

#### Integración CI/CD
```yaml
# .github/workflows/docker-security.yml
name: Docker Security Scan

on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build image
        run: docker build -t myimage:${{ github.sha }} .
      
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'myimage:${{ github.sha }}'
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'  # Fail if vulnerabilities found
      
      - name: Upload results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        if: always()
        with:
          sarif_file: 'trivy-results.sarif'
```

### 3.4 Minimizar Superficie de Ataque

```dockerfile
# ❌ MAL: Instalar paquetes innecesarios
FROM ubuntu:latest
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    wget \
    vim \
    nano \
    git \
    ssh \
    sudo

# ✅ BIEN: Solo lo necesario para runtime
FROM python:slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 && \  # Solo runtime library (no dev)
    rm -rf /var/lib/apt/lists/*  # Limpiar cache
```

**Principio**: Menos paquetes = menos CVEs potenciales

---

## ⚡ 4. OPTIMIZACIÓN DE TAMAÑO Y CACHE

### 4.1 Order Matters: Optimizar Layer Caching

Docker cachea layers. Si un layer cambia, todos los siguientes se invalidan.

#### ❌ MAL: Orden Subóptimo
```dockerfile
FROM python:slim

# Layer 1: Copia TODO (cambia frecuentemente)
COPY . /app  # ⚠️ Invalida cache en cada cambio de código

# Layer 2: Instala dependencias (cambia raramente)
WORKDIR /app
RUN pip install -r requirements.txt  # 🔄 Se reinstala innecesariamente
```

**Problema**: Cada cambio de código reinstala dependencias (lento).

#### ✅ BIEN: Orden Óptimo
```dockerfile
FROM python:slim

WORKDIR /app

# Layer 1: Copia SOLO archivos de dependencias (cambia raramente)
COPY requirements.txt .  # ✅ Cache se mantiene si requirements no cambia

# Layer 2: Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt  # ✅ Cacheado

# Layer 3: Copia código (cambia frecuentemente)
COPY . .  # ⚠️ Solo invalida este layer
```

**Beneficio**: Dependencias solo se reinstalan cuando `requirements.txt` cambia.

### 4.2 Combinar RUN Commands

Cada `RUN` crea un layer nuevo. Más layers = imagen más grande.

#### ❌ MAL: Múltiples RUN
```dockerfile
RUN apt-get update                    # Layer 1: ~50MB
RUN apt-get install -y curl           # Layer 2: +5MB
RUN apt-get install -y wget           # Layer 3: +3MB
RUN apt-get clean                     # Layer 4: NO reduce tamaño (layers inmutables)
RUN rm -rf /var/lib/apt/lists/*       # Layer 5: NO reduce tamaño

# Total: 58MB + metadata
```

**Problema**: Limpieza no reduce tamaño porque layers anteriores persisten.

#### ✅ BIEN: RUN Combinado
```dockerfile
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Total: 8MB (limpieza en mismo layer)
```

**Principio**: Crear + limpiar en mismo layer = tamaño mínimo

### 4.3 .dockerignore (OBLIGATORIO)

Equivalente a `.gitignore`, excluye archivos del build context.

```
# .dockerignore

# Dependencies
node_modules/
__pycache__/
*.pyc
*.pyo
.venv/
venv/
env/

# Git
.git/
.gitignore
.gitattributes

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
coverage/
htmlcov/
.tox/
*.test
test-results/

# CI/CD
.github/
.gitlab-ci.yml
.travis.yml

# Documentation
*.md
!README.md
docs/

# Logs
*.log
logs/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment files
.env
.env.*
!.env.example

# Build artifacts
dist/
build/
*.egg-info/
.next/
out/

# OS
.DS_Store
Thumbs.db
```

**Beneficio**: Reduce build context de ~500MB a ~50MB típicamente.

### 4.4 Técnicas Adicionales de Optimización

#### No Cachear Paquetes
```dockerfile
# Python
RUN pip install --no-cache-dir -r requirements.txt

# Node.js
RUN npm ci --omit=dev

# apt-get
RUN apt-get update && apt-get install -y --no-install-recommends \
    package && \
    rm -rf /var/lib/apt/lists/*
```

#### Usar COPY en vez de ADD
```dockerfile
# ❌ ADD tiene funcionalidad extra (descomprime .tar, descarga URLs)
ADD file.tar.gz /app/  # Puede comportarse inesperadamente

# ✅ COPY es explícito y predecible
COPY file.tar.gz /app/
RUN tar -xzf /app/file.tar.gz  # Control explícito
```

---

## 🏥 5. HEALTH CHECKS

### 5.1 Dockerfile HEALTHCHECK

```dockerfile
HEALTHCHECK [OPTIONS] CMD <command>

# Opciones:
#   --interval=DURATION (default: 30s)
#   --timeout=DURATION (default: 30s)
#   --start-period=DURATION (default: 0s)
#   --retries=N (default: 3)
```

### 5.2 Ejemplos por Stack

#### HTTP API (Python/Node.js/Go)
```dockerfile
# Opción 1: Con curl (si disponible)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Opción 2: Sin curl (Python)
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Opción 3: Sin curl (Node.js)
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (res) => process.exit(res.statusCode === 200 ? 0 : 1))"
```

#### Base de Datos
```dockerfile
# PostgreSQL
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
    CMD pg_isready -U postgres || exit 1

# MongoDB
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
    CMD mongo --eval "db.adminCommand('ping')" || exit 1

# Redis
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
    CMD redis-cli ping || exit 1
```

### 5.3 Endpoint de Health en Aplicación

```python
# Python (FastAPI)
@app.get("/health")
async def health_check():
    """
    Health check endpoint
    Returns 200 if service is healthy
    """
    checks = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {}
    }
    
    # Check database
    try:
        await db.execute("SELECT 1")
        checks["checks"]["database"] = "connected"
    except Exception as e:
        checks["checks"]["database"] = f"error: {str(e)}"
        checks["status"] = "unhealthy"
    
    # Check external API
    try:
        response = await httpx.get("https://api.external.com/ping", timeout=5)
        checks["checks"]["external_api"] = "available" if response.status_code == 200 else "unavailable"
    except Exception as e:
        checks["checks"]["external_api"] = f"error: {str(e)}"
        checks["status"] = "unhealthy"
    
    status_code = 200 if checks["status"] == "healthy" else 503
    return JSONResponse(content=checks, status_code=status_code)
```

```javascript
// Node.js (Express)
app.get('/health', async (req, res) => {
    const checks = {
        status: 'healthy',
        timestamp: new Date().toISOString(),
        checks: {}
    };
    
    // Check database
    try {
        await db.query('SELECT 1');
        checks.checks.database = 'connected';
    } catch (error) {
        checks.checks.database = `error: ${error.message}`;
        checks.status = 'unhealthy';
    }
    
    const statusCode = checks.status === 'healthy' ? 200 : 503;
    res.status(statusCode).json(checks);
});
```

---

## 🐳 6. DOCKER COMPOSE

### 6.1 Estructura de Archivos

```
project/
├── docker-compose.yml              # Base configuration
├── docker-compose.override.yml     # Local development (auto-merged)
├── docker-compose.dev.yml          # Development explicit
├── docker-compose.staging.yml      # Staging
├── docker-compose.prod.yml         # Production
└── .env.example                    # Template de variables
```

### 6.2 docker-compose.yml Base

```yaml
version: '3.8'

# ========================================
# Services
# ========================================
services:
  
  # Frontend Service
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      target: production  # Multi-stage target
    image: ${PROJECT_NAME:-myapp}-frontend:${VERSION:-latest}
    container_name: ${PROJECT_NAME:-myapp}-frontend
    restart: unless-stopped
    ports:
      - "${FRONTEND_PORT:-3000}:3000"
    environment:
      - NODE_ENV=${NODE_ENV:-production}
      - NEXT_PUBLIC_API_URL=${API_URL}
    healthcheck:
      test: ["CMD", "node", "-e", "require('http').get('http://localhost:3000/api/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    depends_on:
      backend:
        condition: service_healthy
    networks:
      - frontend-network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
  
  # Backend Service
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
      target: production
    image: ${PROJECT_NAME:-myapp}-backend:${VERSION:-latest}
    container_name: ${PROJECT_NAME:-myapp}-backend
    restart: unless-stopped
    ports:
      - "${BACKEND_PORT:-8000}:8000"
    environment:
      - ENVIRONMENT=${ENVIRONMENT:-production}
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    depends_on:
      database:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - frontend-network
      - backend-network
    volumes:
      - app-data:/app/data
      - app-logs:/app/logs
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
  
  # Database Service
  database:
    image: postgres:alpine
    container_name: ${PROJECT_NAME:-myapp}-db
    restart: unless-stopped
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend-network
    volumes:
      - db-data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d:ro
    secrets:
      - db_password
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
  
  # Redis Cache
  redis:
    image: redis:alpine
    container_name: ${PROJECT_NAME:-myapp}-redis
    restart: unless-stopped
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend-network
    volumes:
      - redis-data:/data
    logging:
      driver: "json-file"
      options:
        max-size: "5m"
        max-file: "2"

# ========================================
# Networks
# ========================================
networks:
  frontend-network:
    driver: bridge
  backend-network:
    driver: bridge
    internal: true  # No internet access

# ========================================
# Volumes
# ========================================
volumes:
  app-data:
    driver: local
  app-logs:
    driver: local
  db-data:
    driver: local
  redis-data:
    driver: local

# ========================================
# Secrets
# ========================================
secrets:
  db_password:
    file: ./secrets/db_password.txt
```

### 6.3 docker-compose.dev.yml (Development Override)

```yaml
version: '3.8'

services:
  frontend:
    build:
      target: development  # Override target
    volumes:
      - ./frontend:/app  # Hot reload
      - /app/node_modules  # Exclude node_modules
    environment:
      - NODE_ENV=development
    command: npm run dev
  
  backend:
    build:
      target: development
    volumes:
      - ./backend:/app  # Hot reload
      - /app/__pycache__  # Exclude cache
    environment:
      - ENVIRONMENT=development
      - DEBUG=true
    command: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
      - "5678:5678"  # Debug port
  
  database:
    ports:
      - "5432:5432"  # Expose para debugging
```

### 6.4 docker-compose.prod.yml (Production Override)

```yaml
version: '3.8'

services:
  frontend:
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
        max-file: "5"
  
  backend:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
  
  database:
    volumes:
      - /mnt/db-backup:/backup:ro  # Read-only backup mount
```

### 6.5 Comandos de Compose

```bash
# ========================================
# Development
# ========================================
# Start con override automático (dev)
docker-compose up -d

# Start con archivo específico
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Ver logs
docker-compose logs -f backend

# Rebuild específico
docker-compose up -d --build backend


# ========================================
# Production
# ========================================
# Start producción
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Scale service
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --scale backend=5


# ========================================
# Maintenance
# ========================================
# Stop todos los servicios
docker-compose down

# Stop y eliminar volúmenes (⚠️ CUIDADO)
docker-compose down -v

# Ver estado
docker-compose ps

# Ejecutar comando en servicio
docker-compose exec backend bash
docker-compose exec database psql -U postgres

# Ver recursos
docker-compose top
```

---

## 📊 7. RESOURCE LIMITS

### 7.1 Por qué Limitar Recursos

Sin límites, un contenedor puede:
- Consumir toda la RAM → OOM kill otros contenedores
- Usar 100% CPU → degradar sistema completo
- Llenar disco → crash del host

### 7.2 Docker Run

```bash
# CPU limits
docker run --cpus="1.5" myimage            # Max 1.5 CPUs
docker run --cpu-shares=512 myimage        # Priority relativa

# Memory limits
docker run -m 512m myimage                 # Max 512MB RAM
docker run -m 512m --memory-swap 1g myimage  # Max 512MB RAM + 512MB swap

# Combinado
docker run \
  --cpus="2.0" \
  -m 1g \
  --memory-swap 2g \
  --restart unless-stopped \
  myimage
```

### 7.3 Docker Compose

```yaml
services:
  app:
    image: myimage
    deploy:
      resources:
        limits:
          cpus: '2.0'        # Máximo 2 CPUs
          memory: 1G          # Máximo 1GB RAM
        reservations:
          cpus: '0.5'         # Mínimo garantizado
          memory: 256M
```

### 7.4 Matriz de Recomendaciones

| Service Type | CPU Limits | Memory Limits | Notes |
|--------------|-----------|---------------|-------|
| **Frontend (Node.js)** | 0.5-1.0 | 256M-512M | Ajustar según concurrencia |
| **Backend API** | 1.0-2.0 | 512M-2G | Depende de carga |
| **Worker/Queue** | 1.0-2.0 | 512M-1G | Por worker |
| **Database** | 2.0-4.0 | 2G-8G | No limitar si es único |
| **Redis/Cache** | 0.5-1.0 | 256M-1G | Según cache size |
| **Nginx/Proxy** | 0.25-0.5 | 128M-256M | Muy eficiente |

---

## 🔍 8. LOGGING & MONITORING

### 8.1 Logging Drivers

```yaml
services:
  app:
    logging:
      driver: "json-file"  # Default, parse-able
      options:
        max-size: "10m"    # Rotar cada 10MB
        max-file: "3"      # Mantener 3 archivos
        labels: "production"
        env: "APP_VERSION"
```

**Opciones de drivers:**
- `json-file`: Default, fácil parsing
- `syslog`: Enviar a syslog remoto
- `journald`: Systemd journal
- `gelf`: Graylog Extended Log Format
- `fluentd`: Fluentd collector
- `awslogs`: CloudWatch
- `gcplogs`: Google Cloud Logging

### 8.2 Formato de Logs Estructurados

```python
# Python - Logging estructurado JSON
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "service": "backend",
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)

# Configurar
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)
```

```javascript
// Node.js - Winston con formato JSON
const winston = require('winston');

const logger = winston.createLogger({
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  defaultMeta: { service: 'frontend' },
  transports: [
    new winston.transports.Console()
  ]
});

logger.info('User logged in', { userId: 123, method: 'OAuth' });
// Output: {"level":"info","message":"User logged in","service":"frontend","timestamp":"2025-10-02T12:00:00.000Z","userId":123,"method":"OAuth"}
```

### 8.3 Ver Logs

```bash
# Ver logs en tiempo real
docker logs -f container_name

# Ver últimas N líneas
docker logs --tail 100 container_name

# Ver logs con timestamps
docker logs -t container_name

# Ver logs entre fechas
docker logs --since 2025-10-01 --until 2025-10-02 container_name

# Compose
docker-compose logs -f backend
docker-compose logs --tail=50 backend frontend
```

---

## 🚀 9. CI/CD INTEGRATION

### 9.1 Pipeline Estándar

```
┌─────────────────┐
│ 1. Lint         │  hadolint, dockerfile_lint
├─────────────────┤
│ 2. Build        │  docker build multi-stage
├─────────────────┤
│ 3. Scan         │  Trivy, Snyk, Clair
├─────────────────┤
│ 4. Test         │  Run tests in container
├─────────────────┤
│ 5. Push         │  Registry (Docker Hub, ECR, GCR)
├─────────────────┤
│ 6. Deploy       │  Staging → Production
└─────────────────┘
```

### 9.2 GitHub Actions Example

```yaml
name: Docker Build & Deploy

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  
  # ========================================
  # Job 1: Lint Dockerfile
  # ========================================
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Lint Dockerfile (hadolint)
        uses: hadolint/hadolint-action@v3.1.0
        with:
          dockerfile: Dockerfile
          failure-threshold: warning
  
  # ========================================
  # Job 2: Build & Scan
  # ========================================
  build:
    needs: lint
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      security-events: write
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Log in to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix={{branch}}-
      
      - name: Build image
        uses: docker/build-push-action@v4
        with:
          context: .
          load: true  # Load para scanning local
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:buildcache
          cache-to: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:buildcache,mode=max
      
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ steps.meta.outputs.tags }}
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'  # Fail build si vulnerabilidades
      
      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        if: always()
        with:
          sarif_file: 'trivy-results.sarif'
      
      - name: Run tests in container
        run: |
          docker run --rm ${{ steps.meta.outputs.tags }} pytest
      
      - name: Push image
        if: github.event_name != 'pull_request'
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
  
  # ========================================
  # Job 3: Deploy (si push a main)
  # ========================================
  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          echo "Deploying to production..."
          # SSH to server, docker-compose pull, restart, etc.
```

### 9.3 Image Tagging Strategy

```bash
# Estrategias comunes:

# 1. SemVer (Semantic Versioning)
myapp:1.2.3
myapp:1.2
myapp:1

# 2. Git Commit SHA
myapp:sha-a1b2c3d

# 3. Branch name
myapp:main
myapp:develop

# 4. Build number
myapp:build-123

# 5. Timestamp
myapp:20251002-120000

# 6. Combinado (RECOMENDADO)
myapp:1.2.3-20251002-a1b2c3d
#     ^      ^         ^
#     version timestamp  commit
```

---

## 📋 10. CHECKLIST DE PRODUCCIÓN

### 10.1 Dockerfile

- [ ] **Multi-stage build** implementado
- [ ] **Imagen base específica** (no `latest`)
- [ ] **Imagen slim/alpine** para producción
- [ ] **Usuario no-root** creado y usado
- [ ] **`.dockerignore`** presente y completo
- [ ] **HEALTHCHECK** configurado
- [ ] **Layers minimizados** (RUN combinados)
- [ ] **Cache optimizado** (COPY orden correcto)
- [ ] **Secretos externalizados** (no en imagen)
- [ ] **Dependencies limpias** (--no-cache-dir, rm apt lists)
- [ ] **Labels** informativos (versión, maintainer, etc.)
- [ ] **EXPOSE** documentado
- [ ] **CMD/ENTRYPOINT** correcto

### 10.2 Security

- [ ] **Imagen escaneada** (0 CRITICAL vulnerabilities)
- [ ] **Usuario no-root verificado** (`docker run myimage id`)
- [ ] **Secrets en runtime** (no hardcoded)
- [ ] **Puertos mínimos** expuestos
- [ ] **Read-only filesystem** (si posible)
- [ ] **Capabilities dropped** (si posible)
- [ ] **No shells innecesarios** (distroless si posible)

### 10.3 Performance

- [ ] **Tamaño < 500MB** (idealmente < 200MB)
- [ ] **Build time < 5min**
- [ ] **Startup time < 30s**
- [ ] **Resource limits** configurados
- [ ] **Health checks** respondiendo < 2s

### 10.4 Observability

- [ ] **Health endpoint** implementado
- [ ] **Logging estructurado** (JSON)
- [ ] **Log rotation** configurado
- [ ] **Metrics exposed** (Prometheus/StatsD)
- [ ] **Tracing** instrumentado (opcional)

### 10.5 Docker Compose

- [ ] **Versiones específicas** de imágenes
- [ ] **Healthchecks** configurados
- [ ] **Resource limits** establecidos
- [ ] **Restart policies** definidas
- [ ] **Secrets** externalizados
- [ ] **Volúmenes** para persistencia
- [ ] **Redes aisladas** por función
- [ ] **Logging driver** configurado
- [ ] **Depends_on** con health conditions

---

## 🎓 11. ANTI-PATTERNS (Evitar)

### ❌ 1. Running as Root
```dockerfile
# MAL
FROM python
COPY . /app
CMD ["python", "app.py"]  # Ejecuta como root
```

### ❌ 2. Using :latest Tag
```dockerfile
# MAL
FROM python:latest  # Imprevisible
```

### ❌ 3. Installing Unnecessary Packages
```dockerfile
# MAL
RUN apt-get update && apt-get install -y \
    python3 curl wget vim git ssh sudo build-essential
```

### ❌ 4. Hardcoded Secrets
```dockerfile
# MAL
ENV API_KEY=abc123xyz
ENV DB_PASSWORD=supersecret
```

### ❌ 5. Single Large Stage
```dockerfile
# MAL - Todo en un stage
FROM python
RUN apt-get install build-essential gcc  # 500MB
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
# Imagen final: 1.2GB con herramientas de build innecesarias
```

### ❌ 6. Poor Layer Caching
```dockerfile
# MAL - Orden subóptimo
COPY . /app  # Cambia frecuentemente, invalida todo
RUN pip install -r requirements.txt  # Se reinstala siempre
```

### ❌ 7. No .dockerignore
```
# Sin .dockerignore
# Build context incluye: node_modules/ (500MB), .git/ (200MB), logs/ (100MB)
# Build context total: 800MB
# Tiempo de envío al daemon: 30s+
```

### ❌ 8. Exposing Unnecessary Ports
```dockerfile
# MAL
EXPOSE 22 3000 3306 5432 6379 8000 8080
```

### ❌ 9. No Health Checks
```yaml
# MAL - Sin healthcheck
services:
  app:
    image: myimage
    # No healthcheck = no auto-recovery
```

### ❌ 10. No Resource Limits
```yaml
# MAL
services:
  app:
    image: myimage
    # Sin limits = puede consumir todo el sistema
```

---

## 📚 12. RECURSOS Y REFERENCIAS

### Documentación Oficial

1. **Docker**
   - Best Practices: https://docs.docker.com/develop/dev-best-practices/
   - Dockerfile Reference: https://docs.docker.com/engine/reference/builder/
   - Multi-stage Builds: https://docs.docker.com/build/building/multi-stage/

2. **Security**
   - OWASP Container Security: https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html
   - CIS Docker Benchmark: https://www.cisecurity.org/benchmark/docker
   - Snyk Container Security: https://snyk.io/learn/container-security/

3. **Cloud Providers**
   - AWS ECS Best Practices: https://docs.aws.amazon.com/AmazonECS/latest/bestpracticesguide/
   - Google Cloud Run: https://cloud.google.com/run/docs/tips
   - Azure Container Instances: https://docs.microsoft.com/azure/container-instances/

### Herramientas Útiles

| Herramienta | Propósito | URL |
|-------------|-----------|-----|
| **hadolint** | Lint Dockerfiles | https://github.com/hadolint/hadolint |
| **Trivy** | Vulnerability scanning | https://github.com/aquasecurity/trivy |
| **dive** | Analizar layers de imagen | https://github.com/wagoodman/dive |
| **docker-slim** | Reducir tamaño de imágenes | https://github.com/docker-slim/docker-slim |
| **Portainer** | UI para gestión de containers | https://www.portainer.io/ |
| **Watchtower** | Auto-update de containers | https://github.com/containrrr/watchtower |

### Comandos Útiles

```bash
# ========================================
# Inspección y Debug
# ========================================
# Ver layers de imagen
docker history myimage

# Analizar tamaño por layer (con dive)
dive myimage

# Inspeccionar configuración de imagen
docker inspect myimage

# Ejecutar shell en container corriendo
docker exec -it container_name /bin/sh

# Ver procesos en container
docker top container_name

# Ver stats en tiempo real
docker stats


# ========================================
# Limpieza
# ========================================
# Eliminar containers detenidos
docker container prune

# Eliminar imágenes sin usar
docker image prune -a

# Eliminar volúmenes sin usar
docker volume prune

# Eliminar networks sin usar
docker network prune

# Limpieza completa (⚠️ CUIDADO)
docker system prune -a --volumes


# ========================================
# Build Optimization
# ========================================
# Build sin cache (debugging)
docker build --no-cache -t myimage .

# Build con BuildKit (más rápido)
DOCKER_BUILDKIT=1 docker build -t myimage .

# Build con target específico
docker build --target production -t myimage .


# ========================================
# Export/Import
# ========================================
# Exportar imagen a tar
docker save myimage:tag -o myimage.tar

# Importar imagen desde tar
docker load -i myimage.tar

# Exportar container a tar
docker export container_name -o container.tar

# Importar desde tar como imagen
docker import container.tar myimage:tag
```

---

## 🎯 13. CONCLUSIÓN

### Principios Clave para Recordar

1. **🏗️ Multi-stage builds**: Separa build de runtime (60-90% reducción tamaño)
2. **🔒 Seguridad first**: Usuario no-root, secrets externos, escaneo continuo
3. **⚡ Optimiza caching**: Orden correcto de COPY, RUN combinados
4. **📦 Minimalismo**: Solo lo necesario (slim/alpine/distroless)
5. **🏥 Health checks**: Siempre implementar endpoints de salud
6. **📊 Observabilidad**: Logs estructurados, métricas, tracing
7. **🎚️ Resource limits**: Proteger el sistema de runaway containers
8. **🔄 Reproducibilidad**: Versiones específicas, builds determinísticos

### Checklist Rápido

**Antes de cada build:**
- [ ] `.dockerignore` actualizado
- [ ] Secrets NO en código
- [ ] Usuario no-root configurado
- [ ] Health check implementado

**Antes de desplegar:**
- [ ] Imagen escaneada (trivy/snyk)
- [ ] Tests pasando en container
- [ ] Resource limits configurados
- [ ] Logs y monitoring listos

### ROI Esperado

| Métrica | Antes | Después | Mejora |
|---------|-------|---------|--------|
| Tamaño imagen | ~1GB | ~150MB | **85%** ↓ |
| Build time | 8 min | 2 min | **75%** ↓ |
| Deploy time | 5 min | 1 min | **80%** ↓ |
| Vulnerabilities | 80+ | <5 | **94%** ↓ |
| Incident rate | Alta | Baja | **70%** ↓ |

---

**Última actualización:** 2025-10-02  
**Versión del documento:** 1.0  
**Mantenedor:** Equipo DevOps  
**Licencia:** MIT

---

## 📝 Notas de Versión

### Filosofía de Versionado de Este Documento

Este documento usa principios y patrones universales, NO versiones específicas de software.

**Por qué agnóstico de versiones:**
- ✅ Atemporal - Válido por años
- ✅ Flexible - Aplica a cualquier stack
- ✅ Mantenible - No requiere actualizaciones constantes
- ✅ Educativo - Enseña principios, no comandos memorísticos

**Cómo usar este documento:**
1. Consulta documentación oficial de tu stack para versiones actuales
2. Aplica los principios aquí documentados
3. Adapta ejemplos a tu contexto específico
4. Mantén tus Dockerfiles bajo control de versiones

**Este documento evoluciona cuando:**
- Docker introduce nuevas features fundamentales
- Emergen nuevos patrones de seguridad críticos
- Best practices de la industria cambian significativamente

**NO evoluciona cuando:**
- Sale una nueva versión de Python/Node/etc.
- Herramientas específicas actualizan su CLI
- Cloud providers cambian pricing

---

**¿Dudas o sugerencias?** Abre un issue o PR en el repositorio del proyecto.

