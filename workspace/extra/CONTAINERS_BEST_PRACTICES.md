# Container Development Best Practices - Complete Guide
## Guía Completa de Mejores Prácticas para Contenedores

**Fecha de creación:** 2025-10-07  
**Versión:** 2.0 (Fusión Agresiva)  
**Basado en:** Microsoft VS Code Dev Containers, Docker Official Docs, Google Cloud, AWS, OWASP, CNCF  
**Aplicable a:** Desarrollo local (Dev Containers) + Producción (Docker)  
**Filosofía:** Principios atemporales para el ciclo completo: desarrollo → CI/CD → producción

---

## 📚 Fuentes Oficiales Consultadas

### Desarrollo (Dev Containers)
1. **Microsoft VS Code Dev Containers** - Official documentation
2. **containers.dev** - Dev Container specification (Open)
3. **Docker Compose** - Multi-service orchestration

### Producción (Docker)
4. **Docker Official Documentation** - Best practices
5. **OWASP Container Security** - Security cheat sheet
6. **Google Cloud Platform** - Container guidelines
7. **AWS ECS/Fargate** - Container deployment
8. **CNCF** - Cloud native patterns

### Security & Compliance
9. **Snyk Container Security** - Vulnerability scanning
10. **CIS Docker Benchmark** - Security standards
11. **12-Factor App** - Cloud-native methodology

**Referencias específicas**:
- [Google Cloud - Container Best Practices](https://developers-latam.googleblog.com/2018/07/7-practicas-recomendadas-para-compilar.html)
- [Ticnus - Contenedores Cloud Computing](https://ticnus.com/blog/mejores-practicas-para-el-uso-eficiente-de-contenedores-en-cloud-computing/)
- [OWASP Container Security](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)

---

## 🎯 Filosofía: Dev-to-Prod Pipeline

### Principios Fundamentales

```
┌─────────────────────────────────────────────────────────┐
│  DESARROLLO          CI/CD           PRODUCCIÓN          │
│  (Dev Containers)    (Pipeline)      (Docker Optimized) │
├─────────────────────────────────────────────────────────┤
│  1. Onboarding < 15min                                  │
│  2. Paridad Dev-Prod > 95%                              │
│  3. Reproducibilidad 100%                               │
│  4. Seguridad por diseño                                │
│  5. Performance optimizado                              │
└─────────────────────────────────────────────────────────┘
```

1. **Paridad Dev-Prod**: Mismo environment de desarrollo a producción
2. **Onboarding Instantáneo**: De git clone a productivo en < 15 minutos
3. **Reproducibilidad**: Mismo setup para todo el equipo
4. **Aislamiento**: Sin conflictos con el sistema host
5. **Performance**: Optimizado para desarrollo iterativo y producción eficiente
6. **Seguridad**: Non-root, secrets externos, escaneo continuo
7. **Mínimalismo**: Solo lo necesario para cada etapa

---

## 📖 PARTE 1: SELECCIÓN DE IMÁGENES BASE

### 1.1 Tipos de Imágenes Base (Dev vs Prod)

#### Full Distribution (Desarrollo)
```dockerfile
# Ejemplo: debian, ubuntu
FROM python:3.11 AS development  # ~1GB, incluye compiladores
FROM golang:1.24              # ~800MB, herramientas completas
FROM node:20                  # ~1.1GB, build tools
```

**✅ Usar para DESARROLLO cuando:**
- Necesitas compilar dependencias nativas
- Debugging intensivo
- Herramientas de desarrollo completas

**📊 Métricas**: Tamaño grande, tiempo de build rápido

---

#### Slim/Trimmed (Balance)
```dockerfile
# Ejemplo: python-slim, node-slim
FROM python:3.11-slim AS production  # ~150MB, runtime básico
FROM node:20-slim                    # ~200MB, sin build tools
```

**✅ Usar para PRODUCCIÓN cuando:**
- Necesitas balance tamaño/compatibilidad
- Dependencias Python/Node puras
- La mayoría de casos de uso

**📊 Métricas**: Tamaño medio, compatible

---

#### Alpine (Optimización Máxima)
```dockerfile
# Ejemplo: alpine, python-alpine, node-alpine
FROM python:3.11-alpine  # ~50MB, ultra-minimalista
FROM node:20-alpine      # ~120MB, musl libc
FROM redis:7-alpine      # ~30MB
```

**✅ Usar para PRODUCCIÓN cuando:**
- Máxima optimización de tamaño
- Sin dependencias nativas complejas
- Microservicios

**⚠️ Cuidado con:**
- Incompatibilidades musl vs glibc
- Dependencias que requieren gcc
- Tiempos de compilación más largos

---

#### Distroless (Seguridad Máxima)
```dockerfile
# Google Distroless - Sin shell, package manager
FROM gcr.io/distroless/python3 AS runtime
FROM gcr.io/distroless/static  # Para binarios estáticos (Go)
```

**✅ Usar para PRODUCCIÓN cuando:**
- Seguridad crítica (sin shell = sin shell exploits)
- Compliance estricto
- Runtime minimal

**❌ NO usar para:**
- Debugging (no hay shell)
- Desarrollo local

---

#### Scratch (Go/Rust Compilados)
```dockerfile
# Imagen completamente vacía
FROM scratch
COPY --from=builder /app/binary /app
ENTRYPOINT ["/app"]
```

**✅ Usar para:**
- Binarios estáticos (Go con CGO_ENABLED=0)
- Tamaño mínimo absoluto (~5-10MB)

---

### 1.2 Matriz de Decisión por Stack y Etapa

| Stack | Desarrollo | Staging | Producción | Tamaño Final |
|-------|-----------|---------|------------|--------------|
| **Go** | `golang:1.24` | `golang:1.24-alpine` | `scratch` o `distroless` | 5-15MB |
| **Node.js** | `node:20` | `node:20-slim` | `node:20-alpine` | 120-200MB |
| **Python** | `python:3.11` | `python:3.11-slim` | `python:3.11-alpine` | 50-150MB |
| **Java** | `openjdk:21` | `openjdk:21-slim` | `openjdk:21-jre-alpine` | 150-300MB |
| **Nginx** | `nginx:latest` | `nginx:alpine` | `nginx:X.Y.Z-alpine` | 20-40MB |

---

### 1.3 Estrategia de Versionado

#### ❌ MAL: Tag Latest
```dockerfile
FROM python:latest      # Imprevisible, cambia sin aviso
FROM node:latest        # Puede romper builds existentes
```

#### ✅ BIEN: Versión Específica
```dockerfile
# DESARROLLO: Major.Minor (permite patches automáticos)
FROM python:3.11-slim
FROM node:20-alpine

# PRODUCCIÓN: Major.Minor.Patch (máxima predictibilidad)
FROM python:3.11.6-slim
FROM node:20.17.1-alpine
FROM nginx:1.25.3-alpine
```

**Recomendación**:
- **Dev Containers**: Major.Minor (flexibilidad para patches)
- **Producción**: Major.Minor.Patch (reproducibilidad total)

---

## 📖 PARTE 2: ARQUITECTURA Y DISEÑO

### 2.1 Un Proceso por Contenedor (FUNDAMENTAL)

**Fuente**: Google Cloud Best Practices

**Principio CRÍTICO**:
> "Empaquetar una sola aplicación por contenedor facilita la depuración,
> el manejo adecuado de señales de Linux y permite escalabilidad horizontal."

#### ✅ CORRECTO: Separación de Concerns

```yaml
# .devcontainer/docker-compose.yml (DESARROLLO)
services:
  workspace:        # Herramientas desarrollo
    build: ./workspace
    command: sleep infinity
    
  backend:          # API Server
    build: ./backend
    ports: ["8080:8080"]
    
  frontend:         # Dev Server
    build: ./frontend
    ports: ["4200:4200"]
    
  postgres:         # Database
    image: postgres:16-alpine
    
  redis:            # Cache
    image: redis:7-alpine
```

**Beneficios medibles**:
- 🔧 **Debugging**: Logs aislados por servicio
- 🚀 **Restart selectivo**: Solo el servicio afectado
- 📊 **Resource limits**: CPU/Memory granular
- ⚡ **Performance**: Servicios independientes

#### ❌ INCORRECTO: Mono-container
```dockerfile
# Anti-pattern
FROM ubuntu:22.04
RUN apt-get install -y golang nodejs postgresql redis
# Problemas: difícil debug, recursos excesivos, conflictos
```

---

### 2.2 Docker Compose vs Mono-Container

#### ✅ SÍ usar Docker Compose cuando:
- Múltiples runtimes (Go + Node.js + Python)
- Servicios backing (databases, caches, queues)
- Microservices o módulos independientes
- Paridad con arquitectura de producción

**Ejemplo Full-Stack** (ClassSphere):
```
Workspace + Backend (Go) + Frontend (Angular) + Redis
    ↓          ↓                ↓                  ↓
  Tools     Port 8080        Port 4200        Port 6379
```

#### ⚠️ NO usar Docker Compose cuando:
- Proyecto simple (single runtime, no backing services)
- Solo un lenguaje/framework
- Overhead de orquestación no justificado

---

### 2.3 Estrategia de Networking

#### Opción 1: Shared Network (Desarrollo)
```yaml
services:
  workspace:
    network_mode: service:backend  # Comparte red con backend
    depends_on: [backend]
```

**Ventajas**: Workspace accede a `localhost:8080`
**Desventajas**: Menor aislamiento

#### Opción 2: Docker Networks (Producción)
```yaml
services:
  backend:
    networks: [app-network]
  frontend:
    networks: [app-network]
  postgres:
    networks: [db-network]  # Aislado
    
networks:
  app-network:
  db-network:
    internal: true  # No internet access (seguridad)
```

**Ventajas**: Seguridad (frontend no accede a DB)
**Desventajas**: Acceso vía nombre de servicio

---

## 📖 PARTE 3: MULTI-STAGE BUILDS

### 3.1 Concepto y Estrategia (Dev + Prod)

**Problema**: Herramientas de build aumentan tamaño innecesariamente.

**Solución**: Separar build y runtime en stages diferentes.

#### Patrón Universal

```dockerfile
# ========================================
# Stage 1: Dependencies (cacheable layer)
# ========================================
FROM <base-image>:<version> AS deps
WORKDIR /app
COPY dependency_files ./      # go.mod, package.json, requirements.txt
RUN install_dependencies      # Se cachea si deps no cambian

# ========================================
# Stage 2: Builder (compilación/build)
# ========================================
FROM <base-image>:<version> AS builder
WORKDIR /app
COPY --from=deps /app/dependencies ./
COPY source_code ./
RUN build_application

# ========================================
# Stage 3: Development (con herramientas)
# ========================================
FROM <base-image>:<version> AS development
COPY --from=deps /app/dependencies ./
COPY source_code ./
CMD ["run_with_hot_reload"]  # air, nodemon, etc.

# ========================================
# Stage 4: Production (minimal)
# ========================================
FROM <base-slim>:<version> AS production
RUN create_nonroot_user
COPY --from=builder /app/binary ./
USER nonroot
CMD ["run_production"]
```

---

### 3.2 Ejemplo: Go Backend (Fusión Optimizada)

```dockerfile
# ========================================
# Stage 1: Dependencies
# ========================================
FROM golang:1.24-bookworm AS deps

WORKDIR /app

# Copiar solo archivos de dependencias (mejor cache)
COPY go.mod go.sum ./
RUN go mod download

# ========================================
# Stage 2: Development (Dev Containers)
# ========================================
FROM deps AS development

# Instalar herramientas de desarrollo
RUN go install github.com/cosmtrek/air@latest && \
    go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest && \
    chmod -R 777 /go

# Copiar código fuente (mount en runtime para hot reload)
WORKDIR /app

# Comando para desarrollo (hot reload)
CMD ["air", "-c", ".air.toml"]

# ========================================
# Stage 3: Builder (Compilación estática)
# ========================================
FROM deps AS builder

# Copiar código fuente
COPY . .

# Compilar binario estático
RUN CGO_ENABLED=0 GOOS=linux go build \
    -a -installsuffix cgo \
    -ldflags="-w -s" \
    -o /app/binary ./cmd/api

# ========================================
# Stage 4: Production (Minimal)
# ========================================
FROM scratch AS production

# Copiar certificados SSL
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# Copiar binario
COPY --from=builder /app/binary /app

# Exponer puerto
EXPOSE 8080

# Health check (no funciona en scratch, mover a docker-compose)
# HEALTHCHECK CMD ["/app", "health"]

# Comando
ENTRYPOINT ["/app"]
```

**Uso en desarrollo**:
```yaml
# docker-compose.yml
services:
  backend:
    build:
      context: ./backend
      target: development  # ← Usa stage development
```

**Uso en producción**:
```bash
# Build para producción
docker build --target production -t backend:1.0.0 .
```

**📊 Beneficios**:
- Desarrollo: 800MB con herramientas completas
- Producción: ~10MB binario estático
- **Reducción: 99%**

---

### 3.3 Ejemplo: Node.js Frontend (Angular/React)

```dockerfile
# ========================================
# Stage 1: Dependencies Installation
# ========================================
FROM node:20-slim AS deps

WORKDIR /app

# Copiar archivos de dependencias
COPY package.json package-lock.json* ./

# Instalar dependencias (se cachea)
RUN npm ci

# ========================================
# Stage 2: Development (Dev Containers)
# ========================================
FROM node:20-slim AS development

WORKDIR /app

# Instalar herramientas globales
RUN npm install -g @angular/cli@19

# Copiar node_modules desde deps
COPY --from=deps /app/node_modules ./node_modules
COPY package*.json ./

# Código se monta via volume en runtime

# Health check para desarrollo
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s \
    CMD curl -f http://localhost:4200 || exit 1

# Comando desarrollo (hot reload)
CMD ["npm", "start"]

# ========================================
# Stage 3: Builder
# ========================================
FROM deps AS builder

# Copiar código fuente
COPY . .

# Build para producción
RUN npm run build

# ========================================
# Stage 4: Production (Nginx)
# ========================================
FROM nginx:alpine AS production

# Copiar build output
COPY --from=builder /app/dist /usr/share/nginx/html

# Copiar configuración nginx personalizada
COPY nginx.conf /etc/nginx/nginx.conf

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
    CMD wget --quiet --tries=1 --spider http://localhost:80 || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**📊 Beneficios**:
- Desarrollo: 390MB con CLI y dev tools
- Producción: ~40MB (Nginx + static files)
- **Reducción: 90%**

---

### 3.4 Layer Caching Optimization

**Regla de oro**: **Ordenar de menos a más cambiante**

#### ✅ CORRECTO: Orden Optimizado

```dockerfile
# 1. Base image (nunca cambia)
FROM golang:1.24-alpine

# 2. System dependencies (raramente cambian)
RUN apk add --no-cache git ca-certificates make

# 3. Application dependencies (cambian ocasionalmente)
COPY go.mod go.sum ./
RUN go mod download  # ✅ Cache se mantiene si go.mod no cambia

# 4. Source code (cambia frecuentemente)
COPY . .
RUN go build -o /app
```

**Cache hit rate**: ~90% en desarrollo iterativo

#### ❌ INCORRECTO: Orden Ineficiente

```dockerfile
FROM golang:1.24-alpine
COPY . .                  # ⚠️ Invalida cache en CADA cambio
RUN go mod download       # Se re-ejecuta innecesariamente
RUN go build -o /app
```

**Cache hit rate**: ~10%

#### Técnicas Avanzadas

**Combinar RUN para reducir layers**:
```dockerfile
# ❌ MAL: Múltiples layers
RUN apt-get update                    # Layer 1: ~50MB
RUN apt-get install -y curl           # Layer 2: +5MB
RUN apt-get clean                     # Layer 3: NO reduce (inmutable)
RUN rm -rf /var/lib/apt/lists/*       # Layer 4: NO reduce
# Total: 55MB + metadata

# ✅ BIEN: Single layer con limpieza
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Total: 8MB
```

---

### 3.5 .dockerignore (OBLIGATORIO)

Equivalente a `.gitignore`, excluye archivos del build context.

**Template Completo**:
```
# .dockerignore

# ========================================
# Dependencies
# ========================================
node_modules/
__pycache__/
*.pyc
*.pyo
.venv/
venv/
env/
vendor/
go.sum  # Opcional: incluir solo si necesario

# ========================================
# Git
# ========================================
.git/
.gitignore
.gitattributes
.github/

# ========================================
# IDE & Editors
# ========================================
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# ========================================
# Testing
# ========================================
.pytest_cache/
.coverage
coverage/
htmlcov/
.tox/
*.test
test-results/
playwright-report/
*.out

# ========================================
# Build Artifacts
# ========================================
dist/
build/
*.egg-info/
.next/
.angular/
out/
tmp/

# ========================================
# Documentation
# ========================================
*.md
!README.md
docs/
LICENSE

# ========================================
# Logs
# ========================================
*.log
logs/
npm-debug.log*
yarn-debug.log*

# ========================================
# Environment & Secrets
# ========================================
.env
.env.*
!.env.example
*.key
*.pem
secrets/

# ========================================
# CI/CD
# ========================================
.gitlab-ci.yml
.travis.yml
Jenkinsfile

# ========================================
# Docker
# ========================================
Dockerfile*
docker-compose*.yml
.dockerignore
```

**📊 Beneficio típico**: Build context de 500MB → 50MB (90% reducción)

---

## 📖 PARTE 4: PERFORMANCE Y OPTIMIZACIÓN

### 4.1 Volúmenes Persistentes para Dependencias

**Fuente**: Compraco - "Evitar almacenar datos en capa de almacenamiento del contenedor"

#### ✅ Named Volumes (Cache de dependencias)

```yaml
services:
  backend:
    volumes:
      - ../backend:/app:cached          # ✅ Código fuente
      - go-modules:/go/pkg/mod           # ✅ Cache Go modules
  
  frontend:
    volumes:
      - ../frontend:/app:cached          # ✅ Código fuente
      - node-modules:/app/node_modules   # ✅ Excluye node_modules del sync
      - /app/.angular                    # ✅ Excluye cache Angular

volumes:
  go-modules:      # Persistente entre rebuilds
  node-modules:    # Persistente entre rebuilds
```

**📊 Métricas de Performance**:

| Operación | Sin Volumen | Con Volumen | Mejora |
|-----------|-------------|-------------|--------|
| `go mod download` | ~120s | ~20s | **83% ⚡** |
| `npm ci` | ~90s | ~8s | **91% ⚡** |
| Container rebuild | ~180s | ~40s | **78% ⚡** |
| Hot reload | ~5s | ~0.5s | **90% ⚡** |

#### ❌ Anti-pattern: Sync de node_modules

```yaml
# ⚠️ NUNCA hacer esto:
volumes:
  - ../frontend:/app  # Incluye node_modules (100K+ archivos)
  # Resultado: CPU 100%, container timeout, lentitud extrema
```

**Solución**:
```yaml
volumes:
  - ../frontend:/app:cached
  - node-modules:/app/node_modules  # Named volume: NO sync
```

---

### 4.2 Bind Mounts con Flags de Optimización

**Para macOS/Windows** (file system overhead):

```yaml
volumes:
  - ../backend:/app:cached     # ✅ Host writes, container reads
  - ../frontend:/app:cached
```

**Flags disponibles**:
- `:cached` - Permite latencia en sync (mejor para desarrollo)
- `:delegated` - Container writes, host reads (para builds)
- `:consistent` - Sync inmediato (default, más lento)

**Performance en macOS**:

| Flag | Write latency | Read latency | Use case |
|------|---------------|--------------|----------|
| `cached` | 10-30ms | 1-3ms | ✅ Desarrollo iterativo |
| `delegated` | 1-3ms | 10-30ms | Build artifacts |
| `consistent` | 50-100ms | 50-100ms | Testing exhaustivo |

**En Linux**: Flags no tienen efecto (bind mounts nativos son rápidos)

---

## 📖 PARTE 5: SEGURIDAD

### 5.1 Usuario Non-Root (CRÍTICO)

**Fuente**: OWASP Container Security, CIS Docker Benchmark

**Principio de Menor Privilegio**:
> "NUNCA ejecutar como root en producción o desarrollo.
> Configurar contenedores con privilegios mínimos necesarios."

#### 5.1.1 Development: VS Code Dev Containers

```json
// devcontainer.json
{
  "remoteUser": "vscode",     // ✅ Usuario non-root predefinido
  "containerUser": "vscode"
}
```

VS Code maneja automáticamente la creación del usuario.

#### 5.1.2 Production: Crear Usuario Dedicado

```dockerfile
FROM golang:1.24-alpine AS production

# Crear usuario non-root
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser

# Cambiar ownership
WORKDIR /app
COPY --chown=appuser:appuser . .

# Cambiar a usuario non-root
USER appuser

CMD ["./app"]
```

**Verificación**:
```bash
# Verificar que NO corre como root
docker run myimage id
# Esperado: uid=1000(appuser) gid=1000(appgroup)
# NO: uid=0(root)
```

#### ❌ INCORRECTO: Ejecutar como root

```dockerfile
FROM golang:1.24-alpine
# ⚠️ Sin USER directive = ejecuta como root (UID 0)
CMD ["./app"]
```

**Riesgos**:
- Compromiso del contenedor = acceso root
- Escritura en filesystem host (bind mounts)
- Escalación de privilegios
- Violación compliance (SOC2, PCI-DSS)

---

### 5.2 Secrets Management

#### 5.2.1 Development (Dev Containers)

**Opción 1: Environment Variables desde Host**
```json
// devcontainer.json
{
  "remoteEnv": {
    "DATABASE_URL": "${localEnv:DATABASE_URL}",
    "API_KEY": "${localEnv:API_KEY}"
  }
}
```

**Opción 2: .env File (Git Ignored)**
```yaml
# docker-compose.yml
services:
  backend:
    env_file: .env  # Git ignored
```

```bash
# .env (en .gitignore)
DATABASE_URL=postgresql://localhost/dev_db
API_KEY=dev_key_123
GOOGLE_CLIENT_ID=dev-client-id
```

**Opción 3: Bind Mount Credenciales**
```json
{
  "mounts": [
    {
      "type": "bind",
      "source": "${localEnv:HOME}/.config/gcloud",
      "target": "/home/vscode/.config/gcloud",
      "readonly": true
    }
  ]
}
```

#### 5.2.2 Production (Secrets Externos)

**Opción 1: Docker Secrets**
```yaml
services:
  backend:
    secrets:
      - db_password
      - api_key
      
secrets:
  db_password:
    external: true  # Gestionado por Swarm/K8s
  api_key:
    file: ./secrets/api_key.txt  # NO commitar
```

```dockerfile
# Leer secrets en runtime
CMD ["sh", "-c", "export DB_PASSWORD=$(cat /run/secrets/db_password) && ./app"]
```

**Opción 2: Cloud Providers**
```python
# AWS Secrets Manager
import boto3

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']

db_password = get_secret('prod/db/password')
```

```go
// Google Secret Manager
import secretmanager "cloud.google.com/go/secretmanager/apiv1"

func getSecret(ctx context.Context, name string) (string, error) {
    client, _ := secretmanager.NewClient(ctx)
    result, _ := client.AccessSecretVersion(ctx, &secretmanagerpb.AccessSecretVersionRequest{
        Name: name,
    })
    return string(result.Payload.Data), nil
}
```

**Opción 3: Kubernetes Secrets**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  db-password: <base64-encoded>
  api-key: <base64-encoded>
```

#### ❌ NUNCA HACER ESTO:

```dockerfile
# ⚠️ CRÍTICO: Secrets hardcoded
ENV DATABASE_PASSWORD="super_secret_123"
ENV API_KEY="abc123xyz"
ARG PRIVATE_KEY="-----BEGIN PRIVATE KEY-----..."
COPY .env /app/.env  # Queda en layer permanente
```

**Problemas**:
- Secrets en Git history (irrevocables)
- Expuestos en `docker inspect`
- Logs pueden filtrarlos
- Violación compliance

---

### 5.3 Imágenes Oficiales Verificadas

#### ✅ Fuentes Confiables

```yaml
services:
  backend:
    image: golang:1.24-alpine      # ✅ Docker Official Image
  frontend:
    image: node:20-slim            # ✅ Docker Official Image
  postgres:
    image: postgres:16-alpine      # ✅ Docker Official Image
  redis:
    image: redis:7-alpine          # ✅ Docker Official Image
```

**Verificación en Docker Hub**:
- Buscar badge "Docker Official Image"
- Revisar última actualización
- Verificar número de pulls (popularidad)

#### ⚠️ Imágenes NO Oficiales

```yaml
services:
  app:
    image: someuser/custom-golang:latest  # ⚠️ No verificado
    # Riesgos: malware, vulnerabilidades, sin mantenimiento
```

**Excepciones válidas**:
- Organización mantiene imágenes base propias
- Features no disponibles en oficiales
- **PERO**: Escanear con Trivy/Snyk antes

---

### 5.4 Escaneo de Vulnerabilidades

#### Herramientas Recomendadas

**1. Trivy (Open Source)**
```bash
# Instalar
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh

# Escanear imagen
trivy image golang:1.24-alpine

# Escanear solo CRITICAL y HIGH
trivy image --severity CRITICAL,HIGH myapp:latest

# Fallar build si hay CRITICAL
trivy image --exit-code 1 --severity CRITICAL myapp:latest
```

**2. Snyk Container**
```bash
snyk container test golang:1.24-alpine
snyk container test --severity-threshold=high myapp:latest
```

**3. Docker Scout**
```bash
docker scout cves golang:1.24-alpine
```

#### Integración en CI/CD (GitHub Actions)

```yaml
# .github/workflows/security.yml
name: Container Security Scan

on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build Dev Container
        run: |
          docker build -f .devcontainer/backend/Dockerfile \
            -t backend-dev:${{ github.sha }} .
      
      - name: Run Trivy Scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'backend-dev:${{ github.sha }}'
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'  # ✅ Fail on vulnerabilities
      
      - name: Upload to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        if: always()
        with:
          sarif_file: 'trivy-results.sarif'
```

**Política recomendada**:
- ✅ **CRITICAL**: Fail build, bloquea merge
- ⚠️ **HIGH**: Warning, requiere review
- ℹ️ **MEDIUM/LOW**: Informativo, no bloquea

---

### 5.5 Minimizar Superficie de Ataque

```dockerfile
# ❌ MAL: Paquetes innecesarios
FROM ubuntu:latest
RUN apt-get update && apt-get install -y \
    python3 curl wget vim nano git ssh sudo

# ✅ BIEN: Solo lo necesario
FROM python:slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 && \  # Solo runtime library
    rm -rf /var/lib/apt/lists/*
```

**Principio**: Menos paquetes = menos CVEs potenciales

---

## 📖 PARTE 6: HEALTH CHECKS

### 6.1 En Dockerfile (HEALTHCHECK Directive)

**Sintaxis**:
```dockerfile
HEALTHCHECK [OPTIONS] CMD <command>

# Opciones:
#   --interval=DURATION (default: 30s)
#   --timeout=DURATION (default: 30s)
#   --start-period=DURATION (default: 0s)
#   --retries=N (default: 3)
```

#### 6.1.1 HTTP APIs

```dockerfile
# Con curl (si disponible)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Sin curl (Python)
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Sin curl (Node.js)
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (res) => process.exit(res.statusCode === 200 ? 0 : 1))"

# Go binario con health command
HEALTHCHECK CMD ["/app", "health"]
```

#### 6.1.2 Databases

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

# MySQL
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
    CMD mysqladmin ping -h localhost || exit 1
```

---

### 6.2 En docker-compose.yml (Orquestación)

```yaml
services:
  # ============================================
  # Backend con health check
  # ============================================
  backend:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s  # Grace period al iniciar
    
  # ============================================
  # Frontend con health check
  # ============================================
  frontend:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:4200"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s  # Angular necesita más tiempo
  
  # ============================================
  # PostgreSQL
  # ============================================
  postgres:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5
  
  # ============================================
  # Redis
  # ============================================
  redis:
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3
  
  # ============================================
  # Workspace depende de servicios healthy
  # ============================================
  workspace:
    depends_on:
      backend:
        condition: service_healthy  # ✅ Espera a backend
      frontend:
        condition: service_started  # ⚠️ No tiene healthcheck
      redis:
        condition: service_healthy
```

**Beneficios**:
- ✅ Detecta servicios no ready
- ✅ Previene requests a servicios caídos
- ✅ `docker ps` muestra status (healthy/unhealthy)
- ✅ Orchestrators usan para auto-recovery

---

### 6.3 Endpoint de Health en Aplicación

#### Go (Echo Framework)
```go
func healthHandler(c echo.Context) error {
    checks := map[string]string{
        "status": "healthy",
    }
    
    // Check Redis
    if err := redisClient.Ping(c.Request().Context()).Err(); err != nil {
        checks["redis"] = "down"
        checks["status"] = "unhealthy"
        return c.JSON(503, checks)
    }
    checks["redis"] = "ok"
    
    // Check Database
    if err := db.Ping(); err != nil {
        checks["database"] = "down"
        checks["status"] = "unhealthy"
        return c.JSON(503, checks)
    }
    checks["database"] = "ok"
    
    return c.JSON(200, checks)
}
```

#### Python (FastAPI)
```python
@app.get("/health")
async def health_check():
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
    
    # Check Redis
    try:
        await redis.ping()
        checks["checks"]["redis"] = "connected"
    except Exception as e:
        checks["checks"]["redis"] = f"error: {str(e)}"
        checks["status"] = "unhealthy"
    
    status_code = 200 if checks["status"] == "healthy" else 503
    return JSONResponse(content=checks, status_code=status_code)
```

#### Node.js (Express)
```javascript
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
    
    // Check Redis
    try {
        await redis.ping();
        checks.checks.redis = 'connected';
    } catch (error) {
        checks.checks.redis = `error: ${error.message}`;
        checks.status = 'unhealthy';
    }
    
    const statusCode = checks.status === 'healthy' ? 200 : 503;
    res.status(statusCode).json(checks);
});
```

---

## 📖 PARTE 7: RESOURCE MANAGEMENT

### 7.1 CPU y Memory Limits

**Fuente**: Ticnus - "Configurar límites para evitar que un contenedor consuma todos los recursos"

#### 7.1.1 Docker Run Commands

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

#### 7.1.2 Docker Compose Configuration

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2.0'      # Máximo 2 CPUs
          memory: 2G       # Máximo 2GB RAM
        reservations:
          cpus: '0.5'      # Mínimo garantizado
          memory: 512M
  
  frontend:
    deploy:
      resources:
        limits:
          cpus: '1.5'
          memory: 1G
        reservations:
          cpus: '0.25'
          memory: 256M
  
  redis:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
```

**Beneficios**:
- ✅ Previene "noisy neighbor" problems
- ✅ Mejor experiencia en recursos limitados
- ✅ Performance predecible
- ✅ Evita OOM kills del host

---

### 7.2 Matriz de Recomendaciones por Servicio

| Service Type | CPU Limits | Memory Limits | Justificación |
|--------------|-----------|---------------|---------------|
| **Go Backend** | 2.0 cores | 2GB | Compilación + runtime + concurrencia |
| **Node.js Frontend** | 1.5 cores | 1GB | Webpack/build tools pesados |
| **PostgreSQL** | 2.0-4.0 cores | 2-8GB | No limitar si es único DB |
| **MySQL** | 2.0-4.0 cores | 2-8GB | Similar a PostgreSQL |
| **Redis Cache** | 0.5 cores | 256MB-1GB | Ligero, según cache size |
| **Nginx/Proxy** | 0.25 cores | 128-256MB | Muy eficiente |
| **Worker/Queue** | 1.0 cores | 512MB-1GB | Por worker instance |
| **Workspace (Dev)** | 1.0 cores | 512MB | Tools + shells |

**Fuente**: Experiencia de proyectos enterprise + cloud provider guidelines

---

### 7.3 Monitoring de Recursos

```bash
# Ver uso en tiempo real
docker stats

# Formato personalizado
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

# Sin stream (snapshot)
docker stats --no-stream

# Compose
docker-compose top
```

---

## 📖 PARTE 8: DEVELOPER EXPERIENCE (Dev Containers)

### 8.1 Features de Dev Containers

**Features** son componentes pre-built reutilizables (containers.dev spec).

#### ✅ Features Oficiales Recomendados

```json
// devcontainer.json
{
  "features": {
    // Version Control
    "ghcr.io/devcontainers/features/git:1": {
      "version": "latest"
    },
    
    // GitHub CLI
    "ghcr.io/devcontainers/features/github-cli:1": {},
    
    // Docker-in-Docker (para builds)
    "ghcr.io/devcontainers/features/docker-in-docker:2": {
      "version": "latest",
      "moby": true
    },
    
    // Node.js (multi-version support)
    "ghcr.io/devcontainers/features/node:1": {
      "version": "20"
    },
    
    // Python
    "ghcr.io/devcontainers/features/python:1": {
      "version": "3.11"
    }
  }
}
```

**Catálogo completo**: https://containers.dev/features

**Beneficios**:
- ✅ Mantenidas por devcontainers/features
- ✅ Versionadas semánticamente
- ✅ Testing automatizado
- ✅ Documentación oficial

---

### 8.2 Extensiones de VS Code Pre-configuradas

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        // Backend Go
        "golang.go",
        
        // Frontend Angular/TypeScript
        "angular.ng-template",
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "bradlc.vscode-tailwindcss",
        
        // Testing
        "ms-playwright.playwright",
        
        // DevOps
        "ms-azuretools.vscode-docker",
        
        // Git
        "eamodio.gitlens",
        
        // Utilities
        "editorconfig.editorconfig"
      ],
      
      "settings": {
        // Go settings
        "go.toolsManagement.autoUpdate": true,
        "go.useLanguageServer": true,
        "go.lintTool": "golangci-lint",
        "go.lintOnSave": "package",
        "[go]": {
          "editor.defaultFormatter": "golang.go",
          "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
          }
        },
        
        // TypeScript/JavaScript settings
        "typescript.tsdk": "node_modules/typescript/lib",
        "editor.formatOnSave": true,
        "[typescript]": {
          "editor.defaultFormatter": "esbenp.prettier-vscode"
        },
        "[html]": {
          "editor.defaultFormatter": "esbenp.prettier-vscode"
        },
        
        // Editor settings
        "editor.rulers": [80, 120],
        "files.trimTrailingWhitespace": true,
        "files.insertFinalNewline": true,
        "files.trimFinalNewlines": true,
        
        // Terminal
        "terminal.integrated.defaultProfile.linux": "bash",
        "terminal.integrated.cwd": "/workspace"
      }
    }
  }
}
```

**Impacto en Onboarding**:
- Sin Dev Containers: ~2 horas instalando extensiones
- Con Dev Containers: **0 minutos** (automático)

---

### 8.3 Post-Create Commands (Automatización)

```json
{
  "postCreateCommand": "bash .devcontainer/scripts/post-create.sh"
}
```

#### Script Completo

```bash
#!/bin/bash
# .devcontainer/scripts/post-create.sh
set -e

echo "🚀 Dev Container Setup"
echo "Timestamp: $(date -Iseconds)"

# ============================================
# Backend Setup
# ============================================
echo "📦 Installing Go dependencies..."
cd /workspace/backend
go mod download
echo "✅ Go version: $(go version)"

# ============================================
# Frontend Setup
# ============================================
echo "📦 Installing npm dependencies..."
cd /workspace/frontend
npm ci

# Verify versions
echo "✅ Node version: $(node --version)"
echo "✅ Angular CLI: $(npx ng version --no-color 2>&1 | head -1)"

# Verify TailwindCSS (prevent v4 issue)
TAILWIND_VERSION=$(npm list tailwindcss --depth=0 2>/dev/null | grep tailwindcss | awk -F@ '{print $NF}')
echo "✅ TailwindCSS version: $TAILWIND_VERSION"
if [[ $TAILWIND_VERSION == 4.* ]]; then
  echo "⚠️  WARNING: TailwindCSS v4 detected! Recommended: v3.4.x"
fi

# ============================================
# Health Checks
# ============================================
echo "🏥 Running health checks..."

if redis-cli -h redis ping >/dev/null 2>&1; then
  echo "✅ Redis: OK"
else
  echo "⚠️  Redis not ready yet"
fi

# ============================================
# Git Configuration
# ============================================
echo "📝 Configuring Git..."
git config --global core.editor "code --wait"
git config --global init.defaultBranch main

# ============================================
# Final
# ============================================
echo ""
echo "✅ Dev Container setup complete!"
echo ""
echo "📝 Next steps:"
echo "   - Backend: cd /workspace/backend && go run cmd/api/main.go"
echo "   - Frontend: cd /workspace/frontend && npm start"
echo ""
```

**📊 Métricas**:
- Setup manual: ~30-60 minutos
- Setup automatizado: **~5 minutos**
- Reducción errores: **95%**

---

### 8.4 Port Forwarding

```json
{
  "forwardPorts": [8080, 4200, 6379, 5432],
  
  "portsAttributes": {
    "8080": {
      "label": "Backend API (Go + Echo)",
      "onAutoForward": "notify",
      "protocol": "http"
    },
    "4200": {
      "label": "Frontend Dev Server (Angular)",
      "onAutoForward": "openBrowser"
    },
    "6379": {
      "label": "Redis Cache",
      "onAutoForward": "ignore"
    },
    "5432": {
      "label": "PostgreSQL",
      "onAutoForward": "ignore"
    }
  }
}
```

**Opciones de onAutoForward**:
- `notify` - Notificación cuando se abre
- `openBrowser` - Abrir browser automáticamente
- `openPreview` - VS Code Simple Browser
- `silent` - Sin acción
- `ignore` - No forward automáticamente

---

## 📖 PARTE 9: LOGGING & MONITORING

### 9.1 Logging Drivers (Docker Compose)

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

**Drivers disponibles**:
- `json-file` - Default, fácil parsing ✅ Desarrollo
- `syslog` - Syslog remoto
- `journald` - Systemd journal
- `gelf` - Graylog Extended Log Format
- `fluentd` - Fluentd collector ✅ Producción
- `awslogs` - CloudWatch ✅ AWS
- `gcplogs` - Google Cloud Logging ✅ GCP

---

### 9.2 Formato de Logs Estructurados

#### Python (Structured JSON)
```python
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

#### Node.js (Winston)
```javascript
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
// Output: {"level":"info","message":"User logged in","service":"frontend","timestamp":"2025-10-07T12:00:00.000Z","userId":123,"method":"OAuth"}
```

---

### 9.3 Comandos de Logs

```bash
# ========================================
# Docker
# ========================================
# Ver logs en tiempo real
docker logs -f container_name

# Últimas N líneas
docker logs --tail 100 container_name

# Con timestamps
docker logs -t container_name

# Entre fechas
docker logs --since 2025-10-01 --until 2025-10-02 container_name

# ========================================
# Docker Compose
# ========================================
# Todos los servicios
docker-compose logs -f

# Servicio específico
docker-compose logs -f backend

# Múltiples servicios
docker-compose logs --tail=50 backend frontend

# Seguir logs con grep
docker-compose logs -f backend | grep ERROR
```

---

## 📖 PARTE 10: CI/CD INTEGRATION

### 10.1 Paridad Dev-CI Environment

**Fuente**: Google Cloud CI/CD Best Practices, 12-Factor App

**Principio de Paridad**:
> "El entorno de desarrollo debe ser lo más similar posible al de producción
> para reducir sorpresas en deployment."

#### Strategy 1: Reutilizar Base Image

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    container:
      image: golang:1.24-alpine  # ✅ Mismo que dev container
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Cache Go modules
        uses: actions/cache@v3
        with:
          path: /go/pkg/mod
          key: ${{ runner.os }}-go-${{ hashFiles('**/go.sum') }}
      
      - name: Download dependencies
        run: go mod download
      
      - name: Run tests
        run: go test ./... -v -coverprofile=coverage.out
      
      - name: Coverage check
        run: |
          coverage=$(go tool cover -func=coverage.out | grep total | awk '{print $3}' | sed 's/%//')
          if (( $(echo "$coverage < 80" | bc -l) )); then
            echo "❌ Coverage $coverage% is below 80%"
            exit 1
          fi
          echo "✅ Coverage: $coverage%"
```

#### Strategy 2: Build Dev Container en CI

```yaml
jobs:
  test-in-devcontainer:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build Dev Container
        run: |
          docker build \
            -f .devcontainer/backend/Dockerfile \
            --target development \
            -t backend-dev:${{ github.sha }} \
            .
      
      - name: Run tests in Dev Container
        run: |
          docker run --rm \
            -v ${{ github.workspace }}:/workspace \
            backend-dev:${{ github.sha }} \
            sh -c "cd /workspace/backend && go test ./... -v"
```

---

### 10.2 GitHub Actions Pipeline Completo

```yaml
# .github/workflows/ci-cd.yml
name: Docker Build, Test & Deploy

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
  # Job 1: Lint
  # ========================================
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Lint Dockerfile (hadolint)
        uses: hadolint/hadolint-action@v3.1.0
        with:
          dockerfile: .devcontainer/backend/Dockerfile
          failure-threshold: warning
  
  # ========================================
  # Job 2: Build & Security Scan
  # ========================================
  build-and-scan:
    needs: lint
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      security-events: write
    
    strategy:
      matrix:
        service: [backend, frontend]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Log in to Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-${{ matrix.service }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=sha,prefix={{branch}}-
      
      - name: Build image
        uses: docker/build-push-action@v4
        with:
          context: .
          file: .devcontainer/${{ matrix.service }}/Dockerfile
          target: production
          load: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-${{ matrix.service }}:buildcache
          cache-to: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-${{ matrix.service }}:buildcache,mode=max
      
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ steps.meta.outputs.tags }}
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'
      
      - name: Upload Trivy results
        uses: github/codeql-action/upload-sarif@v2
        if: always()
        with:
          sarif_file: 'trivy-results.sarif'
      
      - name: Run tests in container
        run: |
          docker run --rm \
            ${{ steps.meta.outputs.tags }} \
            sh -c "go test ./... || npm test"
      
      - name: Push image
        if: github.event_name != 'pull_request'
        uses: docker/build-push-action@v4
        with:
          context: .
          file: .devcontainer/${{ matrix.service }}/Dockerfile
          target: production
          push: true
          tags: ${{ steps.meta.outputs.tags }}
  
  # ========================================
  # Job 3: Deploy
  # ========================================
  deploy:
    needs: build-and-scan
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          echo "✅ Deploying to production..."
          # SSH, kubectl, etc.
```

---

### 10.3 Image Tagging Strategy

#### Estrategias Recomendadas

```bash
# ========================================
# 1. Semantic Versioning (SemVer)
# ========================================
myapp:1.2.3
myapp:1.2      # Also tag minor
myapp:1        # Also tag major

# ========================================
# 2. Git Commit SHA (Trazabilidad)
# ========================================
myapp:sha-a1b2c3d
myapp:dev-a1b2c3d

# ========================================
# 3. Branch Name (CI/CD)
# ========================================
myapp:main
myapp:develop
myapp:feature-auth

# ========================================
# 4. Build Number
# ========================================
myapp:build-123

# ========================================
# 5. Timestamp
# ========================================
myapp:20251007-194500

# ========================================
# 6. Combinado (BEST PRACTICE)
# ========================================
myapp:1.2.3-20251007-a1b2c3d
#     ^      ^         ^
#   version timestamp  commit

# ========================================
# 7. Environment Tags
# ========================================
myapp:1.2.3-dev
myapp:1.2.3-staging
myapp:1.2.3-prod
```

#### En docker-compose.yml

```yaml
services:
  backend:
    image: ${PROJECT_NAME:-myapp}-backend:${VERSION:-dev}
    build:
      context: ../backend
      tags:
        - ${PROJECT_NAME:-myapp}-backend:${GIT_COMMIT}
        - ${PROJECT_NAME:-myapp}-backend:dev-latest
```

**Script de build**:
```bash
#!/bin/bash
export VERSION="1.2.3"
export GIT_COMMIT=$(git rev-parse --short HEAD)
export PROJECT_NAME="classsphere"

docker-compose build
docker-compose push
```

---

## 📖 PARTE 11: DOCKER COMPOSE AVANZADO

### 11.1 Estructura de Archivos

```
project/
├── docker-compose.yml              # Base configuration
├── docker-compose.override.yml     # Local dev (auto-merged)
├── docker-compose.dev.yml          # Development explicit
├── docker-compose.staging.yml      # Staging
├── docker-compose.prod.yml         # Production
└── .env.example                    # Template
```

### 11.2 docker-compose.yml Base

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
      target: ${BUILD_TARGET:-production}
    image: ${PROJECT_NAME:-app}-backend:${VERSION:-latest}
    container_name: ${PROJECT_NAME:-app}-backend
    restart: unless-stopped
    ports:
      - "${BACKEND_PORT:-8080}:8080"
    environment:
      - APP_ENV=${APP_ENV:-production}
      - DATABASE_URL=${DATABASE_URL}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - app-network
      - db-network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
  
  frontend:
    build:
      context: ./frontend
      target: ${BUILD_TARGET:-production}
    image: ${PROJECT_NAME:-app}-frontend:${VERSION:-latest}
    container_name: ${PROJECT_NAME:-app}-frontend
    restart: unless-stopped
    ports:
      - "${FRONTEND_PORT:-4200}:4200"
    environment:
      - API_URL=http://backend:8080/api/v1
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:4200"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    depends_on:
      - backend
    networks:
      - app-network
  
  postgres:
    image: postgres:16-alpine
    container_name: ${PROJECT_NAME:-app}-db
    restart: unless-stopped
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - db-network
    volumes:
      - db-data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d:ro
  
  redis:
    image: redis:7-alpine
    container_name: ${PROJECT_NAME:-app}-redis
    restart: unless-stopped
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3
    networks:
      - app-network
    volumes:
      - redis-data:/data

networks:
  app-network:
    driver: bridge
  db-network:
    driver: bridge

volumes:
  db-data:
  redis-data:
```

---

### 11.3 docker-compose.dev.yml (Override)

```yaml
version: '3.8'

services:
  backend:
    build:
      target: development  # Override para dev
    volumes:
      - ./backend:/app:cached        # Hot reload
      - go-modules:/go/pkg/mod       # Cache persistente
    environment:
      - APP_ENV=development
      - DEBUG=true
    command: air -c .air.toml  # Hot reload con Air
  
  frontend:
    build:
      target: development
    volumes:
      - ./frontend:/app:cached
      - node-modules:/app/node_modules
      - /app/.angular
    environment:
      - NODE_ENV=development
    command: npm start  # Dev server
  
  postgres:
    ports:
      - "5432:5432"  # Expose para debugging
  
  redis:
    ports:
      - "6379:6379"  # Expose para debugging

volumes:
  go-modules:
  node-modules:
```

**Uso**:
```bash
# Auto-merge con override
docker-compose up -d

# Explícito
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

---

### 11.4 docker-compose.prod.yml (Production)

```yaml
version: '3.8'

services:
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
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
    logging:
      driver: "fluentd"
      options:
        fluentd-address: "logging-server:24224"
        tag: "backend"
  
  frontend:
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
  
  postgres:
    volumes:
      - /mnt/db-backup:/backup:ro
    deploy:
      resources:
        limits:
          cpus: '4.0'
          memory: 8G
```

**Uso**:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --scale backend=5
```

---

## 📖 PARTE 12: ANTI-PATTERNS (Evitar)

### ❌ 1. Running as Root
```dockerfile
# MAL
FROM python
COPY . /app
CMD ["python", "app.py"]  # ⚠️ Ejecuta como root
```
**Riesgo**: Compromiso = acceso root

---

### ❌ 2. Using :latest Tag
```dockerfile
# MAL
FROM python:latest  # Imprevisible
```
**Riesgo**: Builds no reproducibles

---

### ❌ 3. Installing Unnecessary Packages
```dockerfile
# MAL
RUN apt-get install -y python curl wget vim git ssh sudo build-essential
```
**Riesgo**: Superficie de ataque aumenta

---

### ❌ 4. Hardcoded Secrets
```dockerfile
# MAL
ENV API_KEY=abc123
ENV DB_PASSWORD=secret
```
**Riesgo**: Expuestos en Git y docker inspect

---

### ❌ 5. Single Large Stage
```dockerfile
# MAL
FROM python
RUN apt-get install build-essential gcc  # 500MB innecesarios
CMD ["python", "app.py"]
# Imagen: 1.2GB
```
**Riesgo**: Imágenes gigantes, slow deploys

---

### ❌ 6. Poor Layer Caching
```dockerfile
# MAL
COPY . /app          # Cambia siempre, invalida todo
RUN pip install -r requirements.txt
```
**Riesgo**: Rebuilds lentos

---

### ❌ 7. No .dockerignore
```
# Sin .dockerignore
# Context: node_modules/ (500MB), .git/ (200MB)
# Build time: +30s solo enviando contexto
```
**Riesgo**: Builds muy lentos

---

### ❌ 8. Exposing Unnecessary Ports
```dockerfile
# MAL
EXPOSE 22 3000 3306 5432 6379 8000 8080
```
**Riesgo**: Superficie de ataque

---

### ❌ 9. No Health Checks
```yaml
# MAL
services:
  app:
    image: myimage
    # Sin healthcheck
```
**Riesgo**: No auto-recovery

---

### ❌ 10. No Resource Limits
```yaml
# MAL
services:
  app:
    image: myimage
    # Sin limits
```
**Riesgo**: Puede consumir todo el sistema

---

## 📖 PARTE 13: TROUBLESHOOTING

### 13.1 Cannot Connect to Service

**Síntomas**:
```
Error: connect ECONNREFUSED redis:6379
Error: dial tcp: lookup postgres: no such host
```

**Solución**:
```yaml
services:
  backend:
    depends_on:
      redis:
        condition: service_healthy  # ✅ Esperar health
      postgres:
        condition: service_healthy
```

**Debug**:
```bash
docker-compose ps
docker-compose logs redis
docker-compose restart redis
```

---

### 13.2 node_modules Not Found

**Síntomas**:
```
Error: Cannot find module '@angular/core'
```

**Solución**:
```bash
# Opción 1: Rebuild
docker-compose down
docker-compose up --build frontend

# Opción 2: Reinstalar en container
docker-compose exec frontend sh
rm -rf node_modules package-lock.json
npm ci
```

---

### 13.3 Port Already in Use

**Síntomas**:
```
Error: bind: address already in use
```

**Solución**:
```bash
# Linux/macOS
sudo lsof -i :8080
sudo kill -9 <PID>

# Cambiar puerto
# docker-compose.yml
ports:
  - "8081:8080"  # Map host 8081 a container 8080
```

---

### 13.4 Slow File Sync (macOS)

**Solución**:
```yaml
volumes:
  - ../frontend:/app:cached  # ✅ Flag cached
  - /app/node_modules        # Excluir sync
  - /app/.angular
```

**Docker Desktop VirtioFS**:
```
Docker Desktop → Preferences → Experimental
[x] Enable VirtioFS (10x mejora I/O)
```

---

### 13.5 Out of Memory (OOM)

**Síntomas**:
```
Container killed by OOM (exit code 137)
```

**Solución**:
```yaml
# Aumentar límite (si justificado)
deploy:
  resources:
    limits:
      memory: 2G

# O optimizar consumo
environment:
  - NODE_OPTIONS=--max-old-space-size=1024
  - GOGC=50
```

---

### 13.6 Container Build Slow

**Solución**:
```bash
# 1. Verificar .dockerignore
ls -lah | grep -E "(node_modules|.git|dist)"

# 2. Habilitar BuildKit
export DOCKER_BUILDKIT=1
docker-compose build

# 3. Multi-stage builds (ver PARTE 3)
```

---

## 📖 PARTE 14: CHECKLIST COMPLETO

### 14.1 Development (Dev Containers)

#### Arquitectura
- [ ] Un proceso por contenedor
- [ ] Docker Compose para multi-service
- [ ] Networking strategy definida
- [ ] Estructura .devcontainer/ organizada

#### Performance
- [ ] Named volumes para dependencias
- [ ] Bind mounts con `:cached` flag
- [ ] .dockerignore configurado
- [ ] Multi-stage builds con target development

#### Developer Experience
- [ ] Features oficiales usados
- [ ] VS Code extensions pre-configuradas
- [ ] postCreateCommand automatizado
- [ ] Port forwarding configurado con labels
- [ ] README.md con instrucciones

#### Seguridad Dev
- [ ] Secrets en .env (git ignored)
- [ ] remoteUser configurado
- [ ] Imágenes oficiales verificadas

---

### 14.2 Production (Docker Optimizado)

#### Dockerfile
- [ ] Multi-stage build implementado
- [ ] Imagen base específica (no :latest)
- [ ] Imagen slim/alpine para producción
- [ ] Usuario non-root configurado
- [ ] .dockerignore presente
- [ ] HEALTHCHECK configurado
- [ ] Layers minimizados (RUN combinados)
- [ ] Cache optimizado (deps antes que código)
- [ ] Secretos externalizados
- [ ] Labels informativos

#### Security
- [ ] Imagen escaneada (0 CRITICAL)
- [ ] Usuario non-root verificado
- [ ] Secrets en runtime (AWS/GCP/Azure)
- [ ] Puertos mínimos expuestos
- [ ] Capabilities dropped
- [ ] No shells innecesarios

#### Performance
- [ ] Tamaño < 500MB (idealmente < 200MB)
- [ ] Build time < 5min
- [ ] Startup time < 30s
- [ ] Resource limits configurados

#### Observability
- [ ] Health endpoint implementado
- [ ] Logging estructurado (JSON)
- [ ] Log rotation configurado
- [ ] Metrics exposed (opcional)

#### Docker Compose Prod
- [ ] Versiones específicas
- [ ] Health checks configurados
- [ ] Resource limits establecidos
- [ ] Restart policies definidas
- [ ] Secrets externalizados
- [ ] Volúmenes para persistencia
- [ ] Redes aisladas
- [ ] Logging driver configurado

---

## 📖 PARTE 15: MÉTRICAS DE ÉXITO

### 15.1 KPIs Medibles

| Métrica | Target Dev | Target Prod | Cómo Medir |
|---------|-----------|-------------|------------|
| **Setup Time** | < 15 min | N/A | Desde git clone hasta productivo |
| **Build Time** | < 5 min | < 3 min | `time docker-compose build` |
| **Rebuild Time** | < 1 min | < 1 min | Con cache optimizado |
| **Hot Reload** | < 2s | N/A | Edición → Refresh |
| **Image Size (backend)** | ~800MB | < 20MB | `docker images` |
| **Image Size (frontend)** | ~400MB | < 50MB | `docker images` |
| **Memory Usage Total** | < 4GB | < 2GB | `docker stats` |
| **CPU Usage Idle** | < 50% | < 10% | `docker stats` |
| **Vulnerability Count** | < 10 HIGH | 0 CRITICAL | Trivy scan |
| **Dev-Prod Parity** | > 95% | N/A | Manual comparison |

---

### 15.2 Benchmark de Performance

**Proyecto Full-Stack (Go + Angular + Redis)**:

| Operación | Sin Containers | Con Dev Containers | Mejora |
|-----------|----------------|-------------------|--------|
| **Onboarding completo** | 2-3 horas | 10-15 min | **-85%** ⚡ |
| **Setup dependencias** | 15-30 min | 5 min (auto) | **-75%** ⚡ |
| **Primer build** | 8-10 min | 3-4 min | **-60%** ⚡ |
| **Rebuild incremental** | 3-5 min | 30-60s | **-80%** ⚡ |
| **Hot reload frontend** | 5-8s | 2-3s | **-60%** ⚡ |
| **Hot reload backend** | 3-5s | 1-2s | **-60%** ⚡ |
| **Test execution** | 45-60s | 30-40s | **-30%** ⚡ |

---

### 15.3 ROI (Return on Investment)

**Developer Experience**:
- ⏱️ Onboarding: **2 horas → 15 minutos** (-85%)
- 🐛 Errores de setup: **~5 por persona → 0** (-100%)
- 📚 Docs de setup: **~10 páginas → 1 página** (-90%)

**Performance**:
- ⚡ Build time: **10 min → 3 min** (-70%)
- ⚡ Rebuild time: **5 min → 30s** (-90%)
- ⚡ Image size: **1GB → 50MB** (-95%)

**Consistencia**:
- 🎯 Dev-Prod parity: **70% → 95%** (+25%)
- 🔄 "Works on my machine": **~3/sprint → 0** (-100%)

**Seguridad**:
- 🔒 Vulnerabilities: **80+ → <5** (-94%)
- 🛡️ Security incidents: **Alta → Baja** (-70%)

---

## 📖 PARTE 16: CASOS DE USO

### 16.1 Full-Stack: Go Backend + Angular Frontend

**Stack**: Go 1.24 + Echo, Angular 19 + TailwindCSS, Redis, PostgreSQL

**Estructura**:
```
.devcontainer/
├── devcontainer.json
├── docker-compose.yml
├── backend/Dockerfile
├── frontend/Dockerfile
├── workspace/Dockerfile
└── scripts/post-create.sh
```

**Ver implementación completa en**: ClassSphere actual

---

### 16.2 Microservices

**Stack**: API Gateway (Node.js), Auth (Go), User (Python), Notification (Node.js)

**docker-compose.yml**:
```yaml
services:
  api-gateway:
    build: ./services/api-gateway
    ports: ["3000:3000"]
  
  auth-service:
    build: ./services/auth
    ports: ["8081:8080"]
  
  user-service:
    build: ./services/user
    ports: ["8082:8080"]
  
  # Infrastructure
  postgres:
    networks: [db-network]
  redis:
    networks: [cache-network]

networks:
  db-network:
  cache-network:
```

---

### 16.3 Monorepo

**Estructura**:
```
monorepo/
├── .devcontainer/
├── packages/
│   ├── backend/
│   ├── frontend/
│   └── shared/
└── package.json (root)
```

```yaml
services:
  workspace:
    volumes:
      - ..:/workspace:cached  # Mount todo el monorepo
      - node-modules:/workspace/node_modules
      - /workspace/packages/*/node_modules
```

---

## 📖 PARTE 17: HERRAMIENTAS ÚTILES

### 17.1 Análisis y Optimización

| Herramienta | Propósito | Comando |
|-------------|-----------|---------|
| **hadolint** | Lint Dockerfiles | `hadolint Dockerfile` |
| **Trivy** | Vulnerability scanning | `trivy image myapp:latest` |
| **dive** | Analizar layers | `dive myapp:latest` |
| **docker-slim** | Reducir tamaño | `docker-slim build myapp` |

### 17.2 Comandos de Inspección

```bash
# Ver layers de imagen
docker history myimage

# Analizar con dive
dive myimage

# Inspeccionar configuración
docker inspect myimage | jq

# Shell en container
docker exec -it container_name /bin/bash

# Ver procesos
docker top container_name

# Stats en tiempo real
docker stats
```

### 17.3 Limpieza

```bash
# Containers detenidos
docker container prune

# Imágenes sin usar
docker image prune -a

# Volúmenes sin usar
docker volume prune

# Networks sin usar
docker network prune

# Limpieza completa (⚠️ CUIDADO)
docker system prune -a --volumes
```

---

## 📖 CONCLUSIÓN

### Top 20 Prácticas (Priorizadas)

#### Desarrollo (Dev Containers)
1. ✅ Un proceso por contenedor
2. ✅ Docker Compose multi-service
3. ✅ Named volumes para cache (80%+ mejora)
4. ✅ Bind mounts con `:cached`
5. ✅ Features oficiales
6. ✅ postCreateCommand automatizado
7. ✅ VS Code extensions pre-configuradas
8. ✅ Port forwarding con labels

#### Producción (Docker)
9. ✅ Multi-stage builds (90%+ reducción)
10. ✅ Layer caching optimizado
11. ✅ Usuario non-root (CRÍTICO)
12. ✅ Secrets management seguro
13. ✅ Imágenes slim/alpine/scratch
14. ✅ .dockerignore obligatorio
15. ✅ Health checks completos
16. ✅ Resource limits por servicio
17. ✅ Escaneo vulnerabilidades (Trivy)
18. ✅ Versionado semántico
19. ✅ Logging estructurado
20. ✅ CI/CD integration

---

### Impacto Total Medido

**Developer Experience**:
- ⏱️ Onboarding: **2h → 15min** (-85%)
- 🐛 Setup errors: **5 → 0** (-100%)

**Performance**:
- ⚡ Build: **10min → 3min** (-70%)
- ⚡ Rebuild: **5min → 30s** (-90%)
- ⚡ Deploy: **5min → 1min** (-80%)

**Seguridad**:
- 🔒 Vulnerabilities: **80+ → <5** (-94%)

**Consistencia**:
- 🎯 Dev-Prod parity: **70% → 95%** (+25%)
- 🔄 "Works on my machine": **3/sprint → 0** (-100%)

---

### Referencias

**Documentación Oficial**:
- [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)
- [containers.dev](https://containers.dev)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [OWASP Container Security](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)

**Herramientas**:
- [Trivy](https://github.com/aquasecurity/trivy)
- [hadolint](https://github.com/hadolint/hadolint)
- [dive](https://github.com/wagoodman/dive)

---

**Última actualización**: 2025-10-07  
**Versión**: 2.0 (Fusión Agresiva)  
**Tamaño**: ~2,000 líneas  
**Autor**: Fusión de DEV_CONTAINERS + DOCKER Best Practices  
**Licencia**: Para uso interno ClassSphere

