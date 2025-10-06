# ClassSphere - Sistema de Gestión Educativa

## 🎯 Descripción del Proyecto

ClassSphere es una plataforma educativa integral que integra Google Classroom con un sistema de gestión personalizado, diseñado para mejorar la experiencia educativa tanto para estudiantes como para profesores y coordinadores.

## 🚀 Características Principales

### ✅ Fase 1 - Fundaciones (COMPLETADA)
- **Autenticación Completa**: JWT + OAuth 2.0 Google
- **Frontend Angular 19**: Interfaz moderna y responsive
- **Backend Go**: API REST con Echo framework
- **Base de Datos**: SQLite con GORM
- **Caché**: Redis para optimización
- **Testing**: Coverage parcial implementado

### 🔄 Fase 2 - Google Integration (EN DESARROLLO)
- Integración completa con Google Classroom API
- Sincronización bidireccional de datos
- Dashboards por rol (estudiante, profesor, coordinador, admin)

### 📊 Fase 3 - Visualización (PLANIFICADA)
- Sistema de búsqueda avanzada
- Notificaciones en tiempo real
- Gráficos interactivos y analytics

### 🔗 Fase 4 - Integración (PLANIFICADA)
- Sincronización bidireccional completa
- Accesibilidad WCAG 2.2 AA
- CI/CD pipeline completo

## 🛠️ Stack Tecnológico

### Backend
- **Go 1.21+** con Echo v4
- **JWT** para autenticación
- **OAuth 2.0** Google integration
- **SQLite** con GORM
- **Redis** para caché
- **Testify** para testing

### Frontend
- **Angular 19** con esbuild
- **TailwindCSS** para estilos
- **ReactiveForms** para validación
- **Jasmine + Karma** para testing

### DevOps
- **Docker** multi-stage
- **GitHub Actions** (planificado)
- **Trivy** security scanning (planificado)

## 📋 Estado Actual - Fase 1

### ✅ Completado
- [x] **OAuth Google**: Implementación completa con botón y flujo
- [x] **Login Mejorado**: Validación visual, idioma inglés, UX profesional
- [x] **Backend API**: Endpoints de autenticación y dashboards
- [x] **Frontend Coverage**: 100% en componentes principales
- [x] **Performance**: <2s tiempo de respuesta
- [x] **Security**: Análisis básico de vulnerabilidades

### ⚠️ En Progreso
- [ ] **Backend Coverage**: 53.5% (objetivo: 100%)
- [ ] **E2E Tests**: Implementación pendiente
- [ ] **CI/CD Pipeline**: Configuración pendiente

### ❌ Pendiente
- [ ] **Documentación API**: Swagger/OpenAPI
- [ ] **Testing E2E**: Playwright setup
- [ ] **Security Scan**: Trivy integration
- [ ] **Performance Monitoring**: Métricas avanzadas

## 🚀 Instalación y Configuración

### Prerrequisitos
- Go 1.21+
- Node.js 20+
- Redis (opcional para desarrollo)
- Google OAuth credentials

### Backend Setup
```bash
cd backend
go mod tidy
go run main.go
```

### Frontend Setup
```bash
cd frontend/classsphere-frontend
npm install
npm start
```

### Variables de Entorno
```bash
# Backend (.env)
JWT_SECRET=your-super-secret-jwt-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8080/auth/google/callback
FRONTEND_URL=http://localhost:4200
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
go test -cover ./...
```

### Frontend Tests
```bash
cd frontend/classsphere-frontend
npm test -- --code-coverage
```

### Verificación Completa
```bash
./scripts/check-fase1-criteria.sh
```

## 📊 Métricas Actuales

| Métrica | Valor | Objetivo | Estado |
|---------|-------|----------|---------|
| **Backend Coverage** | 53.5% | 100% | 🟡 |
| **Frontend Coverage** | 100% | 100% | ✅ |
| **Performance Backend** | 0.0004s | <2s | ✅ |
| **Performance Frontend** | 0.003s | <2s | ✅ |
| **OAuth Google** | 100% | 100% | ✅ |
| **E2E Tests** | 0% | 100% | ❌ |
| **CI/CD Pipeline** | 0% | 100% | ❌ |

## 🔧 Comandos Útiles

### Desarrollo
```bash
# Iniciar backend
cd backend && go run main.go

# Iniciar frontend
cd frontend/classsphere-frontend && npm start

# Verificar coverage
cd backend && go test -cover ./...
```

### Testing
```bash
# Tests backend
go test -v ./...

# Tests frontend
npm test

# Verificación completa
./scripts/check-fase1-criteria.sh
```

## 📁 Estructura del Proyecto

```
ClassSphere/
├── backend/                 # API Go con Echo
│   ├── auth/               # Autenticación JWT
│   ├── oauth/              # OAuth Google
│   ├── handlers/           # Controladores HTTP
│   ├── models/             # Modelos de datos
│   ├── config/             # Configuración
│   ├── cache/              # Redis cache
│   └── database/           # Base de datos
├── frontend/               # Angular 19
│   └── classsphere-frontend/
│       ├── src/app/
│       │   ├── components/ # Componentes UI
│       │   └── services/   # Servicios Angular
│       └── e2e/            # Tests E2E
├── contracts/              # Documentación del proyecto
└── scripts/                # Scripts de utilidad
```

## 🎯 Próximos Pasos

### Inmediatos (Fase 1 - Completar)
1. **Aumentar Backend Coverage** a 100%
2. **Implementar E2E Tests** con Playwright
3. **Configurar CI/CD** con GitHub Actions
4. **Security Scan** con Trivy

### Fase 2 - Google Integration
1. **Google Classroom API** integration
2. **Sincronización** de cursos y estudiantes
3. **Dashboards** específicos por rol
4. **Modo dual** (Google/Mock)

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Contacto

- **Proyecto**: ClassSphere
- **Versión**: 1.0.0
- **Estado**: Fase 1 - Fundaciones (En desarrollo)

---

**Última actualización**: Octubre 2025
**Coverage Backend**: 53.5%
**Coverage Frontend**: 100%
**Performance**: ✅ <2s
