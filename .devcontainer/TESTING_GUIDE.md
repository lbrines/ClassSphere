# 🧪 ClassSphere Dev Containers - Testing Guide

**Última Actualización**: 2025-10-07 | **Tiempo estimado**: 15-20 minutos

---

## 📋 Pre-requisitos

Antes de comenzar, verifica que tienes:

- [ ] Docker Desktop corriendo (`docker info`)
- [ ] VS Code instalado
- [ ] Extensión "Dev Containers" instalada (ms-vscode-remote.remote-containers)
- [ ] Puertos 8080, 4200, 6379 disponibles
- [ ] Mínimo 8GB RAM disponible

---

## 🚀 Fase 1: Verificación Actual (Sin VS Code)

### 1.1 Verificar Servicios Corriendo

```bash
cd /home/lbrines/projects/AI/ClassSphere
docker-compose -f .devcontainer/docker-compose.yml ps
```

**✅ Resultado esperado**: Todos los servicios con estado `Up` o `Up (healthy)`

### 1.2 Ejecutar Health Check

```bash
bash .devcontainer/scripts/verify-health.sh
```

**✅ Resultado esperado**:
```
✅ Backend: HEALTHY
✅ Redis: HEALTHY
✅ Workspace: RUNNING
⚠️  Frontend: STARTING (o HEALTHY)
```

### 1.3 Verificar Endpoints

```bash
# Backend
curl http://localhost:8080/health
# Esperado: {"status":"ok"}

# Redis
docker exec classsphere-redis redis-cli ping
# Esperado: PONG

# Frontend (en navegador)
xdg-open http://localhost:4200
```

---

## 🎯 Fase 2: Abrir Dev Container en VS Code

### 2.1 Cerrar Contenedores Actuales

**IMPORTANTE**: VS Code creará nuevos contenedores cuando abras el Dev Container.

```bash
cd /home/lbrines/projects/AI/ClassSphere
docker-compose -f .devcontainer/docker-compose.yml down
```

### 2.2 Abrir Proyecto en VS Code

```bash
code /home/lbrines/projects/AI/ClassSphere
```

### 2.3 Abrir en Dev Container

**Opción 1 - Notificación automática**:
- VS Code detectará `.devcontainer/devcontainer.json`
- Click en "Reopen in Container" en la notificación

**Opción 2 - Comando manual**:
1. Presiona `F1`
2. Escribe: "Dev Containers: Reopen in Container"
3. Presiona Enter

**Opción 3 - Ícono**:
- Click en el ícono verde en la esquina inferior izquierda
- Selecciona "Reopen in Container"

### 2.4 Esperar Setup Inicial

**Durante el setup verás**:
- "Starting Dev Container..."
- Build de imágenes Docker (~3-5 min primera vez)
- Post-create script ejecutándose
- Instalación de extensiones VS Code

**✅ Completado cuando**:
- El ícono verde muestra "Dev Container: ClassSphere..."
- Terminal está disponible dentro del container

---

## 🔍 Fase 3: Verificación Dentro del Dev Container

### 3.1 Abrir Terminal Integrado

**En VS Code**:
- `` Ctrl + ` `` (backtick) o
- View → Terminal

**Verificar que estás dentro del container**:
```bash
pwd
# Esperado: /workspace

hostname
# Esperado: algo como "a055f309b698" (container ID)

whoami
# Esperado: root o vscode
```

### 3.2 Verificar Herramientas Instaladas

```bash
# Go
go version
# Esperado: go version go1.23.12 o superior

# Node & npm
node --version
# Esperado: v20.x.x

npm --version
# Esperado: 10.x.x

# Angular CLI
ng version
# Esperado: Angular CLI: 19.x.x

# Git
git --version
# Esperado: git version 2.x.x

# Redis CLI
redis-cli --version
# Esperado: redis-cli 7.x.x
```

### 3.3 Verificar Servicios desde Container

```bash
# Backend
curl http://backend:8080/health
# Esperado: {"status":"ok"}

# Frontend (puede tardar si está compilando)
curl -I http://frontend:4200
# Esperado: HTTP/1.1 200 OK (después de compilar)

# Redis
redis-cli -h redis ping
# Esperado: PONG
```

---

## 🛠️ Fase 4: Testing de Desarrollo

### 4.1 Backend Development

#### A) Navegar al Backend
```bash
cd /workspace/backend
ls -la
# Verificar que ves: cmd/, internal/, go.mod, etc.
```

#### B) Ejecutar Tests
```bash
go test ./...
# Esperado: PASS para todos los tests
```

#### C) Check Coverage
```bash
go test -coverprofile=coverage.out ./...
go tool cover -func=coverage.out | tail -5
# Esperado: ver cobertura ~94%
```

#### D) Lint Code
```bash
golangci-lint run ./...
# Esperado: Sin errores (o warnings menores)
```

### 4.2 Frontend Development

#### A) Navegar al Frontend
```bash
cd /workspace/frontend
ls -la
# Verificar que ves: src/, package.json, angular.json, etc.
```

#### B) Verificar Compilación Angular
```bash
# Ver logs del servidor dev
docker logs classsphere-frontend --tail 50
# Esperado: "Application bundle generation complete"
```

#### C) Ejecutar Tests Unitarios
```bash
npm test -- --watch=false --browsers=ChromeHeadless
# Esperado: Tests passed
```

#### D) Verificar en Navegador
En tu **máquina host** (no container):
```bash
xdg-open http://localhost:4200
```

**✅ Verificar**:
- Página carga correctamente
- No hay errores en console (F12)
- Login page visible

---

## 🎨 Fase 5: Testing de VS Code Extensions

### 5.1 Verificar Extensiones Instaladas

**En VS Code**:
1. Click en ícono Extensions (Ctrl+Shift+X)
2. Buscar "Installed"

**✅ Deberías ver instaladas**:
- [x] Go (golang.go)
- [x] Angular Language Service (angular.ng-template)
- [x] Playwright Test (ms-playwright.playwright)
- [x] Docker (ms-azuretools.vscode-docker)
- [x] GitLens (eamodio.gitlens)
- [x] Prettier (esbenp.prettier-vscode)
- [x] ESLint (dbaeumer.vscode-eslint)
- [x] Tailwind CSS IntelliSense (bradlc.vscode-tailwindcss)

### 5.2 Testing Go Extension

#### A) Abrir archivo Go
```bash
# En VS Code, abrir:
backend/cmd/api/main.go
```

**✅ Verificar**:
- Syntax highlighting funciona
- Imports se organizan automáticamente
- Hover sobre funciones muestra documentación
- Autocomplete funciona (escribe `fmt.` y espera sugerencias)

#### B) Format on Save
1. Hacer un cambio menor
2. Guardar (Ctrl+S)
3. **✅ Verificar**: Código se formatea automáticamente

### 5.3 Testing Angular Extension

#### A) Abrir archivo TypeScript
```bash
# En VS Code, abrir:
frontend/src/app/app.component.ts
```

**✅ Verificar**:
- TypeScript IntelliSense funciona
- Imports se autocompletan
- Errores de tipo se muestran en rojo

#### B) Abrir Template HTML
```bash
# En VS Code, abrir:
frontend/src/app/features/(auth)/login/login.component.html
```

**✅ Verificar**:
- Angular directives con syntax highlighting
- Autocomplete para directivas (*ngIf, *ngFor, etc.)

### 5.4 Testing Prettier

#### A) Abrir archivo desordenado
Crear archivo de prueba:
```typescript
// /workspace/test-prettier.ts
const x={a:1,b:2,c:3};function test(){return x;}
```

#### B) Format Document
1. Right-click → "Format Document"
2. O: Shift+Alt+F

**✅ Resultado esperado**:
```typescript
const x = { a: 1, b: 2, c: 3 };
function test() {
  return x;
}
```

---

## 🔥 Fase 6: Testing Hot Reload

### 6.1 Backend Hot Reload (Futuro - Air)

**Nota**: Air no está configurado aún, pero `go run` reinicia manualmente.

```bash
cd /workspace/backend

# Terminal 1: Correr backend
go run cmd/api/main.go

# Terminal 2: Test endpoint
curl http://localhost:8080/health
```

### 6.2 Frontend Hot Reload (Angular HMR)

#### A) Verificar HMR Activo
```bash
docker logs classsphere-frontend | grep HMR
# Esperado: "Component HMR has been enabled"
```

#### B) Testing Hot Reload
1. Abrir `frontend/src/app/app.component.ts`
2. Cambiar el título:
```typescript
title = 'ClassSphere - TESTING HMR';
```
3. Guardar archivo
4. **✅ Verificar**: Navegador se actualiza automáticamente (sin F5)

**Tiempo esperado**: < 2-3 segundos

---

## 🌐 Fase 7: Testing Ports & Connectivity

### 7.1 Verificar Port Forwarding

**En VS Code**:
1. View → Output
2. Seleccionar "Dev Containers" en dropdown

**✅ Buscar líneas como**:
```
Port forwarding 8080 -> 8080
Port forwarding 4200 -> 4200
Port forwarding 6379 -> 6379
```

### 7.2 Testing desde Host

**En tu máquina (fuera del container)**:

```bash
# Backend
curl http://localhost:8080/health

# Frontend
curl -I http://localhost:4200

# Redis
redis-cli -h localhost ping
```

**✅ Todos deberían funcionar** desde host gracias a port forwarding.

---

## 📊 Fase 8: Testing de Performance

### 8.1 Verificar Resource Usage

```bash
# Dentro del Dev Container
docker stats --no-stream
```

**✅ Verificar**:
- Backend: < 500 MB memory
- Frontend: < 1 GB memory
- Redis: < 50 MB memory
- Total: < 2 GB

### 8.2 Testing Build Speed

```bash
# Backend incremental build
cd /workspace/backend
time go build ./cmd/api

# Esperado: < 10 segundos
```

```bash
# Frontend incremental compilation
# Ya está corriendo con watch mode
# Cambiar un archivo y medir tiempo hasta reload
```

---

## 🐛 Troubleshooting Durante Testing

### Issue: Extensions no se instalan

**Solución**:
```bash
# En Command Palette (F1)
"Developer: Reload Window"
```

### Issue: Terminal no conecta

**Solución**:
```bash
# En Command Palette (F1)
"Dev Containers: Rebuild Container"
```

### Issue: Puertos no forward

**Solución**:
1. View → Ports
2. Verificar que 8080, 4200, 6379 están listados
3. Click derecho → "Forward Port" si falta alguno

### Issue: Frontend no compila

**Solución**:
```bash
# Dentro del container
cd /workspace/frontend
rm -rf node_modules
npm ci
docker-compose -f ../.devcontainer/docker-compose.yml restart frontend
```

---

## ✅ Checklist de Validación Final

### Infraestructura
- [ ] Docker containers corriendo (4 services)
- [ ] Health checks todos passing
- [ ] Port forwarding funcional

### VS Code Integration
- [ ] Dev Container conectado
- [ ] Terminal dentro del container
- [ ] 8 extensiones instaladas
- [ ] Settings aplicados

### Backend
- [ ] Go tools funcionando
- [ ] Tests passing
- [ ] Lint sin errores
- [ ] Health endpoint responding

### Frontend
- [ ] Angular compilado
- [ ] Dev server running
- [ ] HMR funcional
- [ ] Tests passing

### Developer Experience
- [ ] Format on save funciona
- [ ] Autocomplete activo
- [ ] Hot reload < 3s
- [ ] No errores en logs

---

## 📝 Reportar Resultados

Después de completar todos los tests, por favor comparte:

### ✅ Lo que funciona
```
- Backend healthy: ✅
- Frontend compiled: ✅
- Extensions installed: ✅
- Hot reload: ✅
etc...
```

### ❌ Issues encontrados
```
- Issue 1: Descripción
  - Logs relevantes
  - Pasos para reproducir
  
- Issue 2: ...
```

### 📊 Métricas
```
- Setup time: X minutos
- Memory usage: X GB
- Build time: X segundos
- Hot reload time: X segundos
```

---

## 🎯 Próximos Pasos

Si todo funciona correctamente:
1. ✅ **Día 1 y 2 validados**
2. 🚀 **Listo para desarrollo**
3. 📝 **Opcional**: Continuar con Día 3 (Security & Resources)

Si hay issues:
1. 📋 Documentar problemas
2. 🐛 Consultar TROUBLESHOOTING.md
3. 🔧 Aplicar fixes necesarios

---

**¡Feliz Testing!** 🎉

Si necesitas ayuda, consulta:
- `.devcontainer/TROUBLESHOOTING.md` - Guía detallada de problemas
- `.devcontainer/README.md` - Documentación completa
- Logs: `docker-compose logs -f`

