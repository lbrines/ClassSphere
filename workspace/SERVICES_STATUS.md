# ClassSphere - Estado de Servicios (Fase 2)

**Última actualización**: 2025-10-07 09:26

## 🟡 Situación General

| Servicio  | Estado    | Notas de arranque |
|-----------|-----------|-------------------|
| Backend (Go 1.24.7 + Echo v4) | ⬜ Detenido | `cd backend && ../workspace/tools/go1.24.7/bin/go run ./cmd/api` |
| Frontend (Angular 19) | ⬜ Detenido | `cd frontend && npm install && npm start` |
| Redis | ⚠️ no verificado en esta sesión | `redis-server` |

> No se dejaron procesos activos. Ejecuta los comandos de la tabla para iniciar cada servicio. Los puertos reservados continúan siendo **8080** (backend) y **4200** (frontend).

---

## 🔌 API Backend (http://localhost:8080/api/v1)

| Recurso | Método | Descripción |
|---------|--------|-------------|
| `/health` | GET | Heartbeat básico |
| `/auth/login` | POST | Login con email/password (roles seed: admin, coordinator, teacher, student) |
| `/auth/oauth/google` | GET | Inicio de flujo OAuth Google (state + url) |
| `/auth/oauth/callback` | GET | Callback OAuth (genera JWT y crea usuario teacher por defecto) |
| `/users/me` | GET | Perfil autenticado |
| `/admin/ping` | GET | Ping solo admin |
| `/google/courses?mode=mock` | GET | **Nuevo** snapshot Classroom según modo (mock/google) |
| `/dashboard/{admin|coordinator|teacher|student}?mode=mock` | GET | **Nuevo** dashboards específicos por rol |

### Usuarios semilla (password hash con bcrypt)

| Rol | Email | Password |
|-----|-------|----------|
| admin | `admin@classsphere.edu` | `admin123`
| coordinator | `coordinator@classsphere.edu` | `coord123`
| teacher | `teacher@classsphere.edu` | `teach123`
| student | `student@classsphere.edu` | `stud123`

> Recuerda enviar el header `Authorization: Bearer <token>` para endpoints protegidos.

---

## 🖥️ Frontend (http://localhost:4200)

Componentes clave habilitados para Fase 2:

- Selector de modo (`mock`/`google`) con refresco manual.
- Botón “Connect Google Classroom” que inicia OAuth (usa `window.open` en `_self`).
- Dashboards por rol (Admin, Coordinator, Teacher, Student) renderizados con `DashboardViewComponent` + ApexCharts wrapper.
- `ClassroomService` centraliza estado observable (modo actual, cursos, dashboards por rol).

Dependencias nuevas relevantes:

```bash
npm install apexcharts
```

(Aún no se incorpora `ng-apexcharts` por incompatibilidad de peer deps con Angular 19).

---

## 🔧 Variables de entorno

```bash
APP_ENV=development
SERVER_PORT=8080
JWT_SECRET=dev-secret-key-change-in-production-12345678901234567890
JWT_ISSUER=classsphere
JWT_EXPIRY_MINUTES=60
REDIS_ADDR=localhost:6379
GOOGLE_CLIENT_ID=dev-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=dev-client-secret-GOCSPX-xxxxxxxxxxxxx
GOOGLE_REDIRECT_URL=http://localhost:4200/auth/callback
GOOGLE_CREDENTIALS_FILE=/ruta/a/credenciales.json   # Obligatorio para modo google real
CLASSROOM_MODE=mock                                 # Valores soportados: mock | google
```

> Con `CLASSROOM_MODE=google` el backend intentará crear el cliente oficial Classroom (`google.golang.org/api/classroom/v1`). Si no encuentra credenciales válidas, degradará a dataset sample y registrará un warning.

---

## 🧩 Arquitectura relevante (Fase 2)

```
backend/
  internal/
    adapters/
      google/            # ClassroomService (google/mock) + datasets
      http/              # Nuevas rutas /google/courses y /dashboard/*
    app/
      classroom_service.go    # Agregación de dashboards por rol
      dashboard_models.go     # Payloads serializados hacia frontend
    domain/
      classroom.go        # Entidades de cursos, assignments, estudiantes
    ports/
      classroom.go        # Interface ClassroomProvider (google/mock)
    shared/
      integration.go      # Normalización de modos (mock/google)
      config.go           # Nuevos campos ClassroomMode / GoogleCredentials
frontend/
  src/app/
    core/services/classroom.service.ts       # Estado reactivo + llamadas API
    core/models/classroom.model.ts           # Tipos compartidos dashboards
    features/dashboard/components/           # Mode selector, Google connect, Chart wrapper
    features/dashboard/pages/*               # Dashboards por rol reutilizando DashboardView
    shared/components/apex-chart/            # Wrapper nativo para ApexCharts
```

---

## 🧪 Tests ejecutados en esta sesión

| Módulo | Comando | Resultado |
|--------|---------|-----------|
| Backend | `../workspace/tools/go1.24.7/bin/go test ./...` | ✅ OK |
| Frontend | `npm test -- --watch=false` | ✅ OK |

> Los tests de ClassroomService usan `HttpClientTestingModule` con fixtures `mock`/`google`. Los dashboards stubs moquean `ApexChartComponent` para evitar cargar ApexCharts real.

---

## 📋 Próximos pasos sugeridos

1. Proveer `GOOGLE_CREDENTIALS_FILE` y cambiar `CLASSROOM_MODE=google` para validar integración real.
2. Exponer los nuevos endpoints en la documentación pública / OpenAPI.
3. Añadir métricas reales al dashboard (ej. totales por Redis/HDD) y completar E2E Playwright para los cuatro roles.
4. Generar `.env.example` consolidado (pendiente Tarea #6).

---

## 📎 Referencias adicionales

- Scripts de autenticación manual backend: `workspace/fase1/test_auth.sh`
- UI de pruebas login: `workspace/fase1/test_login.html`
- Reportes Playwright (última ejecución): `frontend/test-results/`, `frontend/playwright-report/`

