# Contrato Stage 1: Fundaciones y Autenticación - Dashboard Educativo

## Información del Proyecto
- **Proyecto**: Dashboard Educativo
- **Fase**: Stage 1 - Fundaciones y Autenticación Completa
- **Autor**: Sistema de Contratos LLM
- **Fecha**: 2025-09-30
- **Propósito**: Establecer la base arquitectónica del sistema con autenticación completa

##############################################
## Objetivos del Stage 1

### Backend Fundacional
- Configurar servidor Python + FastAPI básico
- Implementar estructura de proyecto y configuración
- Crear servicios Mock con dataset inicial
- Establecer API REST básica con envelope estándar
- Implementar autenticación JWT mock
- Configurar testing básico (unitarios e integración)

### Frontend Fundacional
- Configurar Next.js 15 con App Router + TypeScript
- Implementar estructura de componentes base
- Crear sistema de autenticación frontend
- Establecer comunicación con backend (API client)
- Implementar layout responsivo con Tailwind CSS
- Crear páginas principales (login, dashboard básico)
- Implementar sistema de internacionalización (i18n) con inglés como idioma base

### Backend - Autenticación Avanzada
- Implementar autenticación OAuth 2.0 con Google en Python
- Configurar manejo de tokens de acceso y refresh tokens
- Implementar middleware de autenticación OAuth
- Crear endpoints para flujo OAuth completo
- Configurar seguridad y validación de tokens

### Frontend - Flujo OAuth
- Implementar flujo OAuth en frontend con Next.js y React Query
- Crear componentes para autenticación OAuth
- Manejar estados de autenticación múltiples (JWT y OAuth)
- Implementar callback de OAuth
- Crear interfaz para gestión de cuentas y sesiones

##############################################
## Árbol de Directorios Completo

```
/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py
│   │   │   │   ├── oauth.py
│   │   │   │   └── health.py
│   │   │   └── router.py
│   │   ├── services/
│   │   │   ├── mock_service.py
│   │   │   ├── auth_service.py
│   │   │   └── oauth_service.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── exceptions.py
│   │   ├── middleware/
│   │   │   ├── auth_middleware.py
│   │   │   ├── oauth_middleware.py
│   │   │   └── validation_middleware.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── oauth_token.py
│   │   │   └── response.py
│   │   ├── schemas/
│   │   │   ├── user_schema.py
│   │   │   ├── oauth_schema.py
│   │   │   └── response_schema.py
│   │   ├── utils/
│   │   │   ├── logger.py
│   │   │   ├── response_helper.py
│   │   │   └── validation_helper.py
│   │   ├── data/
│   │   │   └── mock_users.json
│   │   └── main.py
│   ├── tests/
│   │   ├── unit/
│   │   │   ├── services/
│   │   │   └── endpoints/
│   │   └── integration/
│   │       └── test_auth.py
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── .env.example
│   └── .gitignore
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── (auth)/
│   │   │   │   ├── login/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── oauth/
│   │   │   │       ├── callback/
│   │   │   │       │   └── page.tsx
│   │   │   │       └── page.tsx
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx
│   │   │   ├── globals.css
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── components/
│   │   │   ├── ui/
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   └── Layout.tsx
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   ├── OAuthButton.tsx
│   │   │   │   └── AuthGuard.tsx
│   │   │   └── dashboard/
│   │   │       ├── DashboardHeader.tsx
│   │   │       └── StatsCard.tsx
│   │   ├── i18n/
│   │   │   ├── config.ts
│   │   │   ├── locales/
│   │   │   │   └── en.json
│   │   │   └── types.ts
│   │   ├── lib/
│   │   │   ├── api.ts
│   │   │   ├── auth.ts
│   │   │   ├── oauth.ts
│   │   │   └── utils.ts
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useOAuth.ts
│   │   │   ├── useApi.ts
│   │   │   └── useTranslation.ts
│   │   ├── types/
│   │   │   ├── auth.types.ts
│   │   │   ├── oauth.types.ts
│   │   │   └── api.types.ts
│   │   └── constants/
│   │       ├── api.constants.ts
│   │       └── oauth.constants.ts
│   ├── public/
│   │   ├── images/
│   │   └── icons/
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   └── .env.local.example
```

##############################################
## Funcionalidades del Stage 1

### Backend - Funcionalidades Core
1. **Servidor Base**
   - Express.js con TypeScript
   - Middleware de CORS, logging y manejo de errores
   - Configuración de entorno con dotenv
   - Health check endpoint

2. **Autenticación Completa**
   - JWT tokens para sesiones
   - OAuth 2.0 con Google
   - Middleware de autenticación
   - Roles básicos: admin, docente, estudiante
   - Endpoints: login, refresh, logout, oauth

3. **API REST Fundacional**
   - Envelope estándar `{data, meta, error?}`
   - Códigos HTTP apropiados
   - Validación de entrada
   - Manejo centralizado de errores

4. **Dataset Mock Inicial**
   - Usuarios de prueba (admin, docentes, estudiantes)
   - Estructura base para cursos y tareas
   - Datos realistas para testing

### Frontend - Funcionalidades Core
1. **Configuración Base**
   - Next.js 15 con App Router
   - TypeScript estricto
   - Bootstrap 5.3 integrado
   - Configuración de ESLint y Prettier

2. **Sistema de Autenticación Completo**
   - Formulario de login responsivo
   - Integración OAuth con Google
   - Manejo de tokens JWT
   - Protección de rutas
   - Persistencia de sesión
   - Selector de método de autenticación

3. **Layout y Navegación**
   - Layout principal responsivo
   - Navegación adaptativa (móvil/desktop)
   - Header con información de usuario
   - Sidebar colapsible

4. **Dashboard Básico**
   - Página principal post-login
   - Cards de estadísticas básicas
   - Navegación entre secciones
   - Indicadores de estado

5. **Sistema de Internacionalización (i18n)**
   - Arquitectura base para soporte multi-idioma
   - Inglés como idioma predeterminado
   - Componentes para traducción de textos
   - Hooks personalizados para acceso a traducciones
   - Estructura escalable para futuros idiomas

##############################################
## Endpoints del Stage 1

### Backend Endpoints
```
# Salud del sistema
GET /api/v1/health

# Autenticación JWT
POST /api/v1/auth/login
POST /api/v1/auth/refresh
POST /api/v1/auth/logout
GET /api/v1/auth/me

# Autenticación OAuth
GET /api/v1/oauth/google/url
GET /api/v1/oauth/google/callback
POST /api/v1/oauth/google/revoke
GET /api/v1/oauth/status

# Usuario actual
GET /api/v1/user/profile
```

### Respuestas Estándar
```json
// Éxito
{
  "data": { /* contenido */ },
  "meta": {
    "timestamp": "2025-09-25T13:15:00Z",
    "version": "1.0.0",
    "requestId": "uuid"
  }
}

// Error
{
  "error": {
    "code": "AUTH_INVALID_CREDENTIALS",
    "message": "Invalid credentials",
    "details": {}
  },
  "meta": {
    "timestamp": "2025-09-25T13:15:00Z",
    "version": "1.0.0",
    "requestId": "uuid"
  }
}
```

##############################################
## Dataset Mock del Stage 1

### Usuarios de Prueba
```json
{
  "users": [
    {
      "id": "admin-001",
      "email": "admin@educational.dashboard",
      "password": "admin123",
      "role": "administrator",
      "name": "System Administrator",
      "active": true
    },
    {
      "id": "coord-001",
      "email": "coordinator@educational.dashboard",
      "password": "coord123",
      "role": "coordinator",
      "name": "Maria Gonzalez",
      "active": true
    },
    {
      "id": "teacher-001",
      "email": "teacher1@educational.dashboard",
      "password": "teacher123",
      "role": "teacher",
      "name": "Carlos Rodriguez",
      "active": true
    },
    {
      "id": "student-001",
      "email": "student1@educational.dashboard",
      "password": "student123",
      "role": "student",
      "name": "Ana Martinez",
      "active": true
    }
  ]
}
```

### OAuth Tokens Mock
```json
{
  "oauth_tokens": [
    {
      "user_id": "teacher-001",
      "provider": "google",
      "access_token": "ya29.mock-token-teacher",
      "refresh_token": "1//mock-refresh-token-teacher",
      "expires_at": "2025-10-30T14:30:00Z",
      "scope": "https://www.googleapis.com/auth/classroom.courses.readonly"
    }
  ]
}
```

##############################################
## Testing del Stage 1

### Backend Tests
1. **Tests Unitarios**
   - `auth.service.test.ts`: Validar JWT y autenticación
   - `oauth.service.test.ts`: Validar flujo OAuth
   - `mock.service.test.ts`: Validar datos mock
   - `response.helper.test.ts`: Validar envelope de respuestas

2. **Tests de Integración**
   - `auth.integration.test.ts`: Endpoints de autenticación JWT
   - `oauth.integration.test.ts`: Endpoints de OAuth
   - `health.integration.test.ts`: Health check
   - `middleware.integration.test.ts`: Middleware de auth

### Frontend Tests
1. **Tests de Componentes**
   - `LoginForm.test.tsx`: Formulario de login
   - `OAuthButton.test.tsx`: Botón de OAuth
   - `AuthGuard.test.tsx`: Protección de rutas
   - `Layout.test.tsx`: Layout principal
   - `TranslatedText.test.tsx`: Componente de texto traducido

2. **Tests de Hooks**
   - `useAuth.test.ts`: Hook de autenticación JWT
   - `useOAuth.test.ts`: Hook de autenticación OAuth
   - `useTranslation.test.ts`: Hook de traducciones

##############################################
## Criterios de Aceptación (DoD) - Stage 1

### Backend
- [ ] Servidor FastAPI funcionando en puerto 8000
- [ ] Health check respondiendo correctamente
- [ ] Autenticación JWT implementada y funcionando
- [ ] Autenticación OAuth con Google implementada
- [ ] Middleware de auth protegiendo rutas
- [ ] Dataset mock cargado y accesible
- [ ] Envelope de respuesta estándar implementado
- [ ] Tests unitarios ≥70% cobertura
- [ ] Tests de integración para auth funcionando
- [ ] Logging estructurado configurado
- [ ] Variables de entorno configuradas
- [ ] Documentación Swagger/OpenAPI generada automáticamente

### Frontend
- [ ] Next.js 15 configurado y funcionando
- [ ] Página de login responsiva y funcional
- [ ] Flujo OAuth con Google implementado
- [ ] Dashboard básico accesible post-login
- [ ] Autenticación frontend integrada con backend
- [ ] Layout responsivo (móvil, tablet, desktop)
- [ ] Tailwind CSS integrado correctamente
- [ ] Protección de rutas implementada
- [ ] Sistema i18n implementado con inglés como idioma base
- [ ] Componentes utilizando sistema de traducciones
- [ ] Manejo de estados de carga y error con React Query
- [ ] Tests de componentes básicos funcionando con Vitest y RTL
- [ ] TypeScript sin errores

### Integración
- [ ] Frontend y backend comunicándose correctamente
- [ ] CORS configurado apropiadamente
- [ ] Tokens JWT funcionando end-to-end
- [ ] Flujo OAuth completo funcionando
- [ ] Manejo de errores consistente
- [ ] Sesiones persistiendo correctamente

##############################################
## Configuración de Desarrollo

### Backend (.env)
```env
ENVIRONMENT=development
PORT=8000
JWT_SECRET=dev-secret-key-change-in-production
JWT_EXPIRES_IN=24h
CORS_ORIGIN=http://localhost:3000
LOG_LEVEL=debug
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:3000/oauth/callback
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_NAME=Educational Dashboard
NEXT_PUBLIC_VERSION=1.0.0
NEXT_PUBLIC_DEFAULT_LOCALE=en
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
```

### Comandos de Desarrollo
```bash
# Backend
cd backend
python -m uvicorn app.main:app --reload  # Servidor en modo desarrollo
python -m pytest                        # Ejecutar tests
python -m pytest --watch                # Tests en modo watch

# Frontend
cd frontend
npm run dev          # Next.js en modo desarrollo
npm run build        # Build de producción
npm run test         # Ejecutar tests con Vitest

# Ambos (desde raíz)
./scripts/dev-all.sh  # Ambos servidores simultáneamente
```

##############################################
## Flujo de Trabajo del Stage 1

### Orden de Implementación
1. **Backend Base** (2-3 días)
   - Configurar servidor FastAPI + Python
   - Implementar autenticación JWT
   - Crear dataset mock inicial
   - Configurar tests básicos

2. **Backend OAuth** (2-3 días)
   - Implementar flujo OAuth con Google
   - Configurar manejo de tokens
   - Crear endpoints OAuth
   - Implementar tests OAuth

3. **Frontend Base** (2-3 días)
   - Configurar Next.js + TypeScript
   - Implementar login y layout
   - Integrar con backend auth
   - Crear dashboard básico

4. **Frontend OAuth** (2-3 días)
   - Implementar componentes OAuth
   - Crear flujo de callback
   - Manejar estados de autenticación
   - Implementar persistencia de sesión

5. **Integración y Testing** (2-3 días)
   - Conectar frontend con backend
   - Tests end-to-end básicos
   - Refinamiento de UX
   - Documentación básica

### Criterios de Finalización
- Todos los DoD completados
- Tests pasando con cobertura ≥70%
- Aplicación funcionando localmente
- Commit con mensaje: `[feature/contracts] Stage 1 foundations and auth completed`
- Registro en `workspace/status.md`

##############################################
## Notas de Implementación

1. **Prioridad en Simplicidad**: Mantener el código simple y bien estructurado
2. **Testing Desde el Inicio**: Implementar tests junto con funcionalidades
3. **Responsive Design**: Asegurar funcionamiento en móviles desde el inicio
4. **Seguridad Básica**: JWT, OAuth, validación de entrada, CORS apropiado
5. **Logging**: Implementar logging estructurado para debugging
6. **Error Handling**: Manejo consistente de errores en frontend y backend
7. **Internacionalización**: Separar textos del código usando sistema i18n
8. **Idioma Único**: Inglés como idioma base con estructura para expansión futura
9. **Autenticación Dual**: Soportar tanto JWT como OAuth de manera coherente

Este stage establece las fundaciones sólidas y el sistema de autenticación completo para el resto del proyecto.
