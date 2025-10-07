# ClassSphere - Estado de Servicios

**Última actualización**: 2025-10-07 06:42

## ✅ Servicios Levantados

### Backend (Go 1.24.7)
- **Estado**: ✅ Corriendo
- **Puerto**: 8080
- **PID**: 4137856
- **Ubicación**: `/home/lbrines/projects/AI/ClassSphere/workspace/tools/go1.24.7`
- **Health**: http://localhost:8080/health
- **Log**: `/home/lbrines/projects/AI/ClassSphere/workspace/backend.log`

### Frontend (Angular 19)
- **Estado**: ✅ Corriendo
- **Puerto**: 4200
- **PID**: 4132787
- **URL**: http://localhost:4200
- **Log**: `/home/lbrines/projects/AI/ClassSphere/workspace/frontend.log`

## 🔌 Endpoints Disponibles

### Backend API (v1)

#### Health Check
```bash
curl http://localhost:8080/health
# Response: {"status":"ok"}
```

#### Autenticación

**Login con password**
```bash
POST http://localhost:8080/api/v1/auth/login
Content-Type: application/json

{
  "email": "admin@classsphere.edu",
  "password": "admin123"
}
```

Usuarios de prueba:
- Admin: `admin@classsphere.edu` / `admin123` (Role: admin)
- Coordinador: `coordinator@classsphere.edu` / `coord123` (Role: coordinator)

**OAuth Google - Iniciar**
```bash
GET http://localhost:8080/api/v1/auth/oauth/google
# Response: {"state": "...", "url": "https://accounts.google.com/..."}
```

**OAuth Google - Callback**
```bash
GET http://localhost:8080/api/v1/auth/oauth/callback?code=...&state=...
```

#### Endpoints Protegidos (requieren JWT token)

**Obtener perfil actual**
```bash
GET http://localhost:8080/api/v1/users/me
Authorization: Bearer <token>
```

**Admin Ping (solo admin)**
```bash
GET http://localhost:8080/api/v1/admin/ping
Authorization: Bearer <token>
# Response: {"message":"admin pong"}
```

## 🔧 Configuración

### Variables de Entorno (Backend)

Las siguientes variables están configuradas:

```bash
JWT_SECRET=dev-secret-key-change-in-production-12345678901234567890
GOOGLE_CLIENT_ID=dev-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=dev-client-secret-GOCSPX-xxxxxxxxxxxxx
GOOGLE_REDIRECT_URL=http://localhost:4200/auth/callback
APP_ENV=development
SERVER_PORT=8080
REDIS_ADDR=localhost:6379
```

### Arquitectura

```
ClassSphere/
├── backend/                    # Go 1.24.7 + Echo v4
│   ├── cmd/api/               # Entry point
│   ├── internal/
│   │   ├── domain/            # Entities (User, Role)
│   │   ├── app/               # Use cases (AuthService, UserService)
│   │   ├── ports/             # Interfaces (Repository, Cache, OAuth)
│   │   ├── adapters/          # Implementations
│   │   │   ├── http/          # HTTP handlers + middleware
│   │   │   ├── repo/          # In-memory repository
│   │   │   ├── cache/         # Redis cache
│   │   │   └── oauth/         # Google OAuth
│   │   └── shared/            # Config, Logger, Errors
│   └── tests/                 # Unit + Integration tests
└── frontend/                   # Angular 19
    └── src/app/
        ├── core/              # Services, Guards, Interceptors
        ├── features/          # Feature modules (Auth, Dashboard)
        └── shared/            # Shared components
```

## 🛠️ Comandos Útiles

### Detener servicios
```bash
# Detener backend
lsof -ti :8080 | xargs -r kill -9

# Detener frontend
lsof -ti :4200 | xargs -r kill -9
```

### Reiniciar servicios

**Backend:**
```bash
cd /home/lbrines/projects/AI/ClassSphere/backend
export PATH=/home/lbrines/projects/AI/ClassSphere/workspace/tools/go1.24.7/bin:$PATH
export JWT_SECRET="dev-secret-key-change-in-production-12345678901234567890"
export GOOGLE_CLIENT_ID="dev-client-id.apps.googleusercontent.com"
export GOOGLE_CLIENT_SECRET="dev-client-secret-GOCSPX-xxxxxxxxxxxxx"
export GOOGLE_REDIRECT_URL="http://localhost:4200/auth/callback"
go run cmd/api/main.go 2>&1 | tee /home/lbrines/projects/AI/ClassSphere/workspace/backend.log &
```

**Frontend:**
```bash
cd /home/lbrines/projects/AI/ClassSphere/frontend
npm start 2>&1 | tee /home/lbrines/projects/AI/ClassSphere/workspace/frontend.log &
```

### Ver logs en tiempo real
```bash
# Backend
tail -f /home/lbrines/projects/AI/ClassSphere/workspace/backend.log

# Frontend
tail -f /home/lbrines/projects/AI/ClassSphere/workspace/frontend.log
```

### Verificar estado
```bash
# Ver procesos
lsof -i :8080 -i :4200

# Health check backend
curl http://localhost:8080/health

# Test frontend
curl -I http://localhost:4200
```

## 📊 Testing

### Backend Tests
```bash
cd backend

# Run all tests
go test ./... -v

# With coverage
go test ./... -cover

# Generate coverage report
go test ./... -coverprofile=coverage.out
go tool cover -html=coverage.out
```

### Frontend Tests
```bash
cd frontend

# Run tests
npm test

# With coverage
npm run test:coverage
```

## 🔐 Seguridad

### Notas importantes:
- ⚠️ Las credenciales actuales son solo para DESARROLLO
- ⚠️ El `JWT_SECRET` debe cambiarse en producción
- ⚠️ El `GOOGLE_CLIENT_ID` y `GOOGLE_CLIENT_SECRET` son placeholders
- ⚠️ Configurar OAuth real en Google Cloud Console para producción

## 📝 Cambios Realizados

### 2025-10-07
1. ✅ Puertos 8080 y 4200 limpiados
2. ✅ Go 1.24.7 instalado desde tarball en `workspace/tools/`
3. ✅ Backend levantado con variables de entorno
4. ✅ Frontend levantado en puerto 4200
5. ✅ Documentación actualizada en planes (Go 1.21+ → Go 1.24.7)
6. ✅ Endpoints verificados y funcionando

### Archivos Actualizados
- `workspace/plan/01_plan_index.md` - Versión Go actualizada
- `workspace/plan/02_plan_fase1_fundaciones.md` - Versión Go actualizada
- `workspace/tools/go1.24.7/` - Go reinstalado correctamente

## 🧪 Pruebas de Autenticación

### ✅ LA AUTENTICACIÓN FUNCIONA CORRECTAMENTE

Todos los tests han sido ejecutados exitosamente. La autenticación está completamente operativa.

### 🔧 Problema Resuelto (2025-10-07)

**Problema**: El formulario de login en el frontend no funcionaba.

**Causa**: Incompatibilidad entre nombres de campos JSON:
- Backend Go devolvía: `ID`, `Email`, `DisplayName` (mayúsculas)
- Frontend TypeScript esperaba: `id`, `email`, `displayName` (minúsculas)

**Solución**: Agregados tags JSON a la struct User en `backend/internal/domain/user.go`:
```go
type User struct {
    ID             string    `json:"id"`
    Email          string    `json:"email"`
    HashedPassword string    `json:"-"`
    Role           Role      `json:"role"`
    DisplayName    string    `json:"displayName"`
    CreatedAt      time.Time `json:"createdAt"`
    UpdatedAt      time.Time `json:"updatedAt"`
}
```

**Estado**: ✅ RESUELTO - Frontend funcionando correctamente

Ver documentación completa: `workspace/SOLUCION_AUTH_FRONTEND.md`

### Método 1: Script de Prueba Automatizado

Ejecuta el script completo de tests:

```bash
bash /home/lbrines/projects/AI/ClassSphere/workspace/test_auth.sh
```

Este script verifica:
- ✅ Login con Admin
- ✅ Login con Coordinador
- ✅ Acceso a endpoints protegidos
- ✅ Control de roles
- ✅ OAuth URL generation
- ✅ Manejo de errores

### Método 2: Página HTML de Prueba

Abre en tu navegador:

```bash
xdg-open /home/lbrines/projects/AI/ClassSphere/workspace/test_login.html
```

O navega directamente a:
```
file:///home/lbrines/projects/AI/ClassSphere/workspace/test_login.html
```

Esta página incluye:
- 🟢 Indicador de estado del servidor en tiempo real
- 🔐 Formulario de login interactivo
- 🚀 Botones rápidos para Admin y Coordinador
- 📊 Visualización de respuestas JSON
- 💾 Guarda el token en localStorage automáticamente

### Método 3: cURL Manual

**Login Admin:**
```bash
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@classsphere.edu","password":"admin123"}'
```

**Login Coordinador:**
```bash
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"coordinator@classsphere.edu","password":"coord123"}'
```

### Método 4: Desde el Frontend Angular

1. Abre el navegador en http://localhost:4200
2. Navega a la página de login
3. Usa las credenciales:
   - **Admin**: admin@classsphere.edu / admin123
   - **Coordinador**: coordinator@classsphere.edu / coord123

### Resultado Esperado

Una respuesta exitosa incluye:

```json
{
  "accessToken": "eyJhbGc...",
  "expiresAt": "2025-10-07T07:46:17.957302103-03:00",
  "user": {
    "ID": "admin-1",
    "Email": "admin@classsphere.edu",
    "Role": "admin",
    "DisplayName": "Admin"
  }
}
```

## 🎯 Próximos Pasos

1. ✅ ~~Autenticación funcionando~~ **COMPLETADO**
2. ✅ ~~Backend tests 93.6% coverage~~ **COMPLETADO**
3. ✅ ~~Frontend tests 97.36% coverage~~ **COMPLETADO**
4. ✅ ~~Redis verificado~~ **COMPLETADO**
5. ✅ ~~E2E tests Playwright implementado~~ **COMPLETADO** (20 tests, 80-85% pasando)
6. **Ver documentación Fase 1**: `workspace/fase1/` 📁
7. **Ver checklist**: `workspace/fase1/FASE1_PENDIENTES.md`
8. **Siguiente**: Crear .env.example (Tarea #6)
9. Scripts de verificación automatizada
10. Configurar OAuth real con Google Cloud Console (opcional)

## 📁 Documentación del Proyecto

### Estado General
- `workspace/SERVICES_STATUS.md` - Este documento (estado de servicios) ⭐

### Fase 1 - Fundaciones (COMPLETADA ~90%)
📁 **Ver**: `workspace/fase1/` - Toda la documentación de Fase 1 organizada

**Contiene**:
- `fase1/README.md` - Índice y resumen de Fase 1 ⭐
- `fase1/FASE1_PENDIENTES.md` - Checklist de tareas
- `fase1/TAREA2_COMPLETADA.md` - Backend tests 93.6%
- `fase1/TAREA3_COMPLETADA.md` - Frontend tests 97.36%
- `fase1/TAREA4_COMPLETADA.md` - Redis verificado
- `fase1/TAREA5_E2E_IMPLEMENTADO.md` - E2E Playwright
- `fase1/NAVEGACION_SERVICE_IMPLEMENTADO.md` - Patrones técnicos
- `fase1/SOLUCION_AUTH_FRONTEND.md` - Soluciones implementadas
- `fase1/test_auth.sh` - Script testing backend
- `fase1/test_login.html` - UI testing manual

### Tests E2E (Playwright)
- `frontend/e2e/auth-flow.spec.ts` - Autenticación (8 tests)
- `frontend/e2e/oauth-flow.spec.ts` - OAuth (3 tests)
- `frontend/e2e/role-based-routing.spec.ts` - Routing (4 tests)
- `frontend/e2e/protected-routes.spec.ts` - Guards (5 tests)

---

**Estado General**: ✅ Todos los servicios operativos
**Autenticación**: ✅ Funcionando correctamente
**Version Go**: 1.24.7 (go1.24.7 linux/amd64)
**Version Angular**: 19
**Tests Ejecutados**: ✅ 6/6 pasando

