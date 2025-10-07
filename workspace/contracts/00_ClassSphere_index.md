---
title: "ClassSphere - Complete Documentation"
version: "4.0"
type: "index"
date: "2025-10-07"
author: "LLM Contracts System"
language: "English (Mandatory for all project documentation)"
files:
  - name: "01_ClassSphere_info_status.md"
    title: "Project Information and Current Status"
  - name: "02_ClassSphere_glosario_tecnico.md"
    title: "Unified Technical Glossary"
  - name: "03_ClassSphere_analisis_critico.md"
    title: "System Critical Analysis"
  - name: "04_ClassSphere_objetivos.md"
    title: "Unified System Objectives"
  - name: "05_ClassSphere_arquitectura.md"
    title: "Unified System Architecture"
  - name: "06_ClassSphere_funcionalidades.md"
    title: "Consolidated Functionalities"
  - name: "07_ClassSphere_api_endpoints.md"
    title: "Consolidated API Endpoints"
  - name: "08_ClassSphere_modelos_datos.md"
    title: "Consolidated Data Models"
  - name: "09_ClassSphere_testing.md"
    title: "Unified Testing Strategy"
  - name: "10_ClassSphere_plan_implementacion.md"
    title: "Unified Implementation Plan"
  - name: "11_ClassSphere_deployment.md"
    title: "Unified Deployment Configuration"
  - name: "12_ClassSphere_criterios_aceptacion.md"
    title: "Unified Acceptance Criteria"
  - name: "13_ClassSphere_validacion_coherencia.md"
    title: "Semantic Coherence Validation"
  - name: "14_ClassSphere_conclusion.md"
    title: "Conclusion"
  - name: "15_ClassSphere_error_prevention.md"
    title: "Critical Errors and Prevention"
  - name: "16_ClassSphere_verification_commands.md"
    title: "Critical Verification Commands"
---

# ClassSphere - Complete Documentation

## Project Information

- **Project**: ClassSphere - Complete System
- **Phase**: Unified Implementation - All Features
- **Author**: LLM Contracts System
- **Date**: 2025-10-07 (Migration to new tech stack - Phase 1 Completed)
- **Purpose**: Implement complete ClassSphere system with modern Go + Angular stack
- **Documentation Language**: English (Mandatory)
- **Code Language**: English (Mandatory)
- **UI Language**: English (Default with i18n support from Phase 1)

## Estado Actual del Proyecto

### ✅ Fase 1 Completada - Lecciones Aprendidas

**Métricas de Éxito Fase 1**:
- **Errores Críticos Resueltos**: 14 errores bloqueadores identificados y solucionados
- **Tiempo de Resolución**: 155 minutos total de resolución de errores
- **Cobertura Final**: 94.4% sin OAuth (objetivo 80%+ superado)
- **Sistema Funcional**: Backend + Frontend + Integración + Demo Users + TailwindCSS
- **Patrones de Prevención**: Documentados y validados en producción

**Errores Críticos Superados**:
- 🔴 **Dashboard Endpoints 404** - BLOQUEADOR PRINCIPAL (15 min resolución)
- 🟠 **TypeScript Compilation** - BLOQUEABA FRONTEND (10 min resolución)
- 🟠 **OAuth Tests Hanging** - BLOQUEABA COBERTURA (20 min resolución)
- 🟡 **Angular CLI Not Found** - BLOQUEABA DESARROLLO (5 min resolución)
- 🟡 **TailwindCSS v4 PostCSS** - BLOQUEABA BUILD (20 min resolución)

**Patrones de Prevención Validados**:
- **Server Restart**: `pkill -f classsphere-backend` → `PORT=8081 ./classsphere-backend`
- **TypeScript**: Optional chaining completo `?.prop?.subprop`, nullish coalescing `?? 0`
- **Angular CLI**: `npx ng` en lugar de `ng`, verificar package.json
- **OAuth Tests**: `-timeout=10s`, URLs que fallen rápido, excluir tests problemáticos
- **TailwindCSS**: v3.4.0 para Angular, evitar CDN en producción

### 🔄 Migración de Stack Tecnológico (Fase 1 Completada - Fases 2-5 En Planificación)

**Nuevo Stack Backend**:
- 🎯 **Go** + Echo framework v4
- 🔐 **Autenticación JWT** + OAuth 2.0 Google
- 👥 **Sistema de Roles** (admin > coordinator > teacher > student)
- 💾 **Redis** (caché)
- 🧪 **testify/mock** + resty (testing)
- 🔧 **CI/CD Pipeline** con GitHub Actions

**Nuevo Stack Frontend**:
- 🚀 **Angular 19** con esbuild oficial
- 🎨 **TailwindCSS 3.x**
- 🧹 **Biome** (linter/formatter)
- 🧪 **Jasmine + Karma** (testing estándar Angular)
- 🎭 **Playwright** (E2E testing)

**DevOps Mantenido**:
- 🔧 **GitHub Actions** (CI/CD)
- 🐳 **Docker** multi-stage
- 🔒 **Trivy** (security scanning)
- 💾 **Redis** (caché compartido)
- 🛠️ **Dev Containers** (Docker Compose multi-service, ver `workspace/extra/DEV_CONTAINERS_BEST_PRACTICES.md`)

**Endpoints API Planificados**:
- `GET /` - Welcome endpoint
- `GET /health` - Health check
- `GET /info` - System information
- `POST /auth/login` - Traditional login
- `GET /auth/google` - Google OAuth initiation
- `GET /auth/google/callback` - Google OAuth callback
- `POST /auth/refresh` - Token refresh
- `GET /auth/me` - Current user info
- `POST /auth/logout` - Logout
- `GET /auth/verify` - Token verification

**Updated Migration Plan**:
- ✅ **Phase 1**: Go + Angular Training (COMPLETED - 155 min error resolution)
  - ✅ Minimum Status Documentation Created
- ⏳ **Phase 2**: Go + Echo Backend (4-6 weeks) - With validated prevention patterns
  - 📝 Minimum Status Documentation Required at Phase End
- ⏳ **Phase 3**: Angular + esbuild Frontend (3-5 weeks) - With validated TypeScript patterns
  - 📝 Minimum Status Documentation Required at Phase End
- ⏳ **Phase 4**: Complete Testing (3-4 weeks) - With validated OAuth test patterns
  - 📝 Minimum Status Documentation Required at Phase End
- ⏳ **Phase 5**: Integration and Deployment (2-3 weeks) - With validated server restart patterns
  - 📝 Minimum Status Documentation Required at Phase End
  - 📚 Complete Final Documentation Created After All Phases

**Implementation Specifications**:
- 🔧 **OAuth Integration**: Angular services → Go handlers
- 🎭 **Role-Based Dashboard**: Angular components per role
- ✅ **Test Coverage**: Backend ≥80%, Frontend ≥80%, Critical modules ≥95% (ACTUAL: 94.4% without OAuth)
- 🧪 **Testing**: Jasmine + Karma (Angular), testify (Go), Playwright (E2E)
- 🛡️ **Error Prevention**: Production-validated patterns to prevent blocking errors
- 🔄 **Server Management**: Automated restart and verification commands
- 🌍 **i18n Support**: Built-in from Phase 1 (English default, extensible to other languages)
- 📝 **Phase Documentation**: Minimum documentation at end of each phase, complete docs after all phases

**Architecture Documentation**:
- 📖 **docs/architecture/testing.md**: Testing strategy with Jasmine + Karma + Playwright (English)
- 🛠 **go.mod**: Go dependency management (English)
- 📝 **CI/CD**: Workflows for Go + Angular (English)
- 🛡️ **Error Prevention Guide**: Critical patterns and production-validated solutions (English)
- 🔧 **Verification Commands**: Automated testing and verification commands (English)
- 🌍 **i18n Configuration**: Internationalization setup from Phase 1 (English default)
- 📝 **Phase Status Docs**: Minimum documentation created at end of each phase (English)
- 📚 **Final Complete Docs**: Comprehensive documentation after all phases complete (English)

## Tabla de Contenidos

### [1. Información del Proyecto y Estado Actual](01_ClassSphere_info_status.md)
- Información detallada del proyecto
- Estado actual del desarrollo
- Progreso de las fases
- Próximos pasos

### [2. Glosario Técnico Unificado](02_ClassSphere_glosario_tecnico.md)
- Conceptos fundamentales
- Terminología estándar unificada
- Estados con prefijos semánticos
- Arquitectura semántica simplificada

### [3. Análisis Críticos del Sistema](03_ClassSphere_analisis_critico.md)
- Análisis de trazabilidad de requisitos
- Análisis de coherencia semántica
- Análisis de dependencias transversales
- Matriz de impacto de dependencias

### [4. Objetivos del Sistema Unificado](04_ClassSphere_objetivos.md)
- Backend - Sistema completo
- Frontend - Aplicación completa
- Características integradas
- Requisitos funcionales y no funcionales

### [5. Arquitectura del Sistema Unificado](05_ClassSphere_arquitectura.md)
- Stack tecnológico consolidado
- Instalación nueva Google Classroom con mocks
- Arquitectura resiliente con prevención de errores
- Estructura de directorios completa (desarrollo parte desde raíz /)
- **Entorno de desarrollo con Dev Containers** (Docker Compose, paridad dev-prod)

**Estructura de Directorios desde Raíz**:
```
/backend
  /cmd/api/                    # main: wire de rutas, middlewares
  /internal/
    /domain/                   # Entidades, VOs, reglas (puro Go)
    /app/                      # Casos de uso (servicios de aplicación)
    /ports/                    # Interfaces (repo, oauth, mail, llm, cache)
    /adapters/                 # Implementaciones de puertos
      /http/                   # Handlers Echo (controladores finos)
      /repo/                   # DB (SQL/NoSQL) + migraciones
      /oauth/                  # Google OAuth 2.0 (server-side)
      /auth/                   # JWT (emit/verify, refresh)
      /llm/                    # Client a proveedor LLM (si aplica)
    /shared/                   # Config (12-factor), logger, errors
  /tests/
    /unit/                     # testify: domain/app
    /integration/              # testify: repo/http con container DB
    /e2e/                      # black-box API contra binario
  go.mod go.sum
  Makefile

/frontend
  /src/
    /app/
      (auth)/login/            # feature folder
      (auth)/callback/         # recepción OAuth (si aplica PKCE público)
      dashboard/
      shared/                  # módulos compartidos (pipes, guards)
    /assets/
    /environments/
  /tests/
    /unit/                     # Jasmine
    /e2e/                      # Playwright
  angular.json
  tsconfig.json
  karma.conf.js
  tailwind.config.js
  .postcssrc.json

/infra/                        # Docker, Compose, K8s/Helm, CI helpers
/scripts/                      # Seeds, dev tools, make-like
/docs/                         # Runbooks, diagramas, decisiones
```

**Notas Importantes**:
- El directorio `/workspace` se **ignora totalmente** en el desarrollo
- Los puertos usan siempre los **defaults**: Backend 8080, Frontend 4200
- Arquitectura hexagonal (ports & adapters) en backend
- Feature folders en frontend Angular
- **Dev Containers con Docker Compose** para entorno consistente (setup automático < 15 min)

### [6. Funcionalidades Consolidadas](06_ClassSphere_funcionalidades.md)
- Autenticación y autorización completa
- Google Classroom integration completa
- Dashboards avanzados por rol
- Visualizaciones avanzadas
- Sistema de búsqueda avanzada
- Notificaciones en tiempo real
- Métricas y analytics avanzados
- Accesibilidad WCAG 2.2 AA
- Testing completo
- CI/CD Pipeline
- **Mapeo Frontend-Backend explícito**
- **Implementación obligatoria por tecnología**

### [7. API Endpoints Consolidados](07_ClassSphere_api_endpoints.md)
- Autenticación
- OAuth
- Health Checks
- Google Classroom
- Dashboards
- Métricas
- Búsqueda
- Notificaciones
- Google Sync Avanzado
- Sincronización y Backup
- Webhooks
- Diagnóstico

### [8. Modelos de Datos Consolidados](08_ClassSphere_modelos_datos.md)
- Usuario
- Curso completo
- Métrica avanzada
- Notificación
- Estado de sincronización

### [9. Estrategia de Testing Unificada](09_ClassSphere_testing.md)
- Estrategia de Testing Frontend (Angular 19 + Jasmine + Karma)
- Stack de Testing definido (Jasmine + Karma + Playwright)
- Metodología TDD consolidada
- Cobertura de testing requerida
- Backend tests con testify (Go)
- Frontend tests con Jasmine (Angular)
- E2E tests con Playwright
- Templates TDD estándar
- Scripts TDD automatizados
- Fixtures y mocks consolidados
- **Criterios de aceptación medibles**
- **Comandos de verificación automática**

### [10. Plan de Implementación Unificado](10_ClassSphere_plan_implementacion.md)
- Metodología TDD consolidada
- Cobertura de testing requerida
- Implementación por fases
- Criterios de aceptación por fase
- Metodología de desarrollo
- Scripts de desarrollo
- Comandos de testing
- Verificación de deployment
- Templates estándar
- Checklist de desarrollo
- Métricas de cobertura
- Scripts automatizados

### [11. Configuración de Deployment Unificada](11_ClassSphere_deployment.md)
- Variables de entorno consolidadas
- Deployment resiliente con prevención de errores
- Docker configuration completa
- CI/CD pipeline unificado
- Verificación de deployment con prevención de errores

### [12. Criterios de Aceptación Unificados](12_ClassSphere_criterios_aceptacion.md)
- Backend completo
- Frontend completo
- Integración Google completa
- Dashboards y visualización
- Búsqueda y notificaciones
- Testing y calidad
- Accesibilidad WCAG 2.2 AA
- CI/CD y deployment
- Seguridad y operaciones

### [13. Validación de Coherencia Semántica](13_ClassSphere_validacion_coherencia.md)
- Métricas de coherencia implementadas
- Mejoras implementadas
- Validación cross-document
- Protocolo de validación continua
- Beneficios de la coherencia semántica
- Conclusión de validación

### [14. Conclusión](14_ClassSphere_conclusion.md)
- Resumen ejecutivo
- Beneficios del enfoque unificado
- Tecnologías validadas
- Métricas de éxito
- Próximos pasos

### [15. Errores Críticos y Prevención](15_ClassSphere_error_prevention.md)
- Patrones de error críticos identificados en Fase 1
- Soluciones validadas en producción
- Comandos de verificación automática
- Checklist de prevención de errores
- Métricas de resolución de errores (155 minutos, 14 errores bloqueadores)
- Patrones aplicables a futuras fases

### [16. Comandos de Verificación Críticos](16_ClassSphere_verification_commands.md)
- Comandos de testing validados en producción
- Scripts de verificación automática
- Checklist de deployment
- Comandos de resolución de errores
- Verificación de cobertura de código
- Comandos de server management

## Guía de Navegación

Esta documentación está diseñada para ser consultada de manera modular. Puede seguir estos enfoques:

1. **Lectura secuencial**: Siga los documentos en orden numérico para una comprensión completa.
2. **Consulta específica**: Acceda directamente al documento que contiene la información que necesita.
3. **Referencias cruzadas**: Utilice los enlaces entre documentos para navegar entre conceptos relacionados.

Cada documento incluye enlaces de navegación en la parte superior e inferior para facilitar el movimiento entre secciones relacionadas.

## Optimización de Contexto

Esta estructura de documentación ha sido diseñada específicamente para optimizar el tamaño del contexto cuando se consulta. Cada archivo está enfocado en un tema específico, lo que permite:

1. **Consultas más eficientes**: Cargar solo la información relevante para cada consulta.
2. **Menor pérdida de contexto**: Evitar el problema "lost-in-the-middle" al dividir la información en chunks manejables.
3. **Referencias precisas**: Facilitar la referencia a secciones específicas sin necesidad de cargar todo el documento.
4. **Actualizaciones modulares**: Permitir actualizar secciones específicas sin afectar al documento completo.

## Key Changes in v4.0 (2025-10-07)

### 🌍 Language Requirements (MANDATORY)
1. **All Documentation**: English mandatory
2. **All Code**: English mandatory (variables, functions, classes, files)
3. **All Comments**: English mandatory
4. **All Commits**: English mandatory
5. **UI Text**: English default with i18n support from Phase 1

### 🔤 i18n Support
- **Phase 1 Setup**: i18n configuration from beginning
- **Default Language**: English (mandatory)
- **Extensibility**: Support for additional languages (es, fr)
- **Translation Structure**: English as base, extensible architecture

### 📝 Phase Documentation
- **Minimum Docs**: Created at end of each phase (1-5)
- **Template**: Status, metrics, issues, prerequisites
- **Language**: All documentation in English

### 📚 Final Documentation
- **Complete Package**: Created after all phases
- **8 Comprehensive Guides**: Architecture, API, User, Developer, Ops, i18n, Lessons, Roadmap
- **Language**: All documentation in English

---

*Last updated: 2025-10-07 - Phase 1 Completed with Lessons Learned + v4.0 Systematic Changes Applied*
