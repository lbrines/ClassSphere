# Contrato de Control - Dashboard Educativo (Versión Consolidada)

## Información del Proyecto
- **Proyecto**: Dashboard Educativo
- **Tipo**: Sistema de Gestión Educativa Full-Stack
- **Autor**: Sistema de Contratos LLM
- **Fecha**: 2025-09-30
- **Propósito**: Índice y guía de navegación para LLMs y desarrolladores
- **Versión**: 2.0 (Consolidación de etapas)

## 📚 Índice de Contratos

| # | Archivo | Descripción | Componente | Etapa |
|---|---------|-------------|------------|-------|
| 01 | `01_dashboard_educativo_backend_base.md` | Contrato base del backend con FastAPI | Backend | Base |
| 02 | `01_dashboard_educativo_fullstack_stage01_fundaciones_auth.md` | Fundaciones del sistema y autenticación | Full-Stack | Stage 1 |
| 03 | `02_dashboard_educativo_fullstack_stage02_google_dashboards.md` | Integración Google y dashboards básicos | Full-Stack | Stage 2 |
| 04 | `03_dashboard_educativo_fullstack_stage03_visualizacion_notificaciones.md` | Visualización avanzada y notificaciones | Full-Stack | Stage 3 |
| 05 | `04_dashboard_educativo_fullstack_stage04_integracion_testing.md` | Integración completa, testing y CI/CD | Full-Stack | Stage 4 |

## 🎯 Mapeo de Funcionalidades por Stage

### Stage 1: Fundaciones y Autenticación
- **Backend**: FastAPI base, autenticación JWT, OAuth 2.0, dataset mock
- **Frontend**: Next.js 15, login, layout responsivo, dashboard básico, i18n (inglés), flujo OAuth
- **Objetivo**: Base arquitectónica sólida con autenticación completa

### Stage 2: Integración Google y Dashboards Básicos
- **Backend**: Google Classroom API, modo dual (Google/Mock), métricas básicas
- **Frontend**: Selector de modo, lista de cursos, dashboards básicos por rol, visualizaciones esenciales
- **Objetivo**: Conexión con Google Classroom y visualización básica de datos

### Stage 3: Visualización Avanzada y Notificaciones
- **Backend**: Métricas avanzadas, analytics, caché, reportes, búsqueda, notificaciones push, websockets
- **Frontend**: Dashboards avanzados, ApexCharts, filtros interactivos, búsqueda contextual, notificaciones en tiempo real
- **Objetivo**: Visualización avanzada, búsqueda y comunicación en tiempo real

### Stage 4: Integración Completa y Calidad
- **Backend**: Sincronización completa, manejo de errores avanzado, tests E2E, performance, seguridad
- **Frontend**: Gestión avanzada de cursos/estudiantes/tareas, accesibilidad WCAG, tests visuales, PWA
- **Objetivo**: Integración robusta con Google, calidad y accesibilidad

## 🏗️ Arquitectura General

### Stack Tecnológico
- **Backend**: Python + FastAPI + MongoDB
- **Frontend**: Next.js 15 + TypeScript + Tailwind CSS
- **Integración**: Google Classroom API + OAuth 2.0
- **Testing**: pytest + Vitest + Playwright
- **CI/CD**: GitHub Actions + Docker

### Flujo de Desarrollo
1. **Base** → Fundaciones del sistema
2. **Stage 1** → Autenticación completa
3. **Stage 2** → Integración con Google y dashboards básicos
4. **Stage 3** → Visualización avanzada y notificaciones
5. **Stage 4** → Integración completa y calidad

## 🤖 Guía para LLMs

### Orden de Lectura Recomendado
1. **Leer este archivo primero** (00) para contexto general
2. **Contrato base** (01) para arquitectura backend
3. **Stages secuencialmente** (01-04) para desarrollo progresivo

### Puntos Clave a Considerar
- **Modo Dual**: Sistema funciona con Google Classroom o datos mock
- **Roles**: admin, coordinador, docente, estudiante
- **TDD**: Testing desde el inicio en todos los stages
- **Responsive**: Diseño móvil-first en todo el frontend
- **Accesibilidad**: WCAG 2.1 AA integrada en Stage 4
- **Idioma**: Inglés como idioma único de la interfaz y datos

### Contexto del Proyecto
- **Dominio**: Educación digital
- **Usuarios**: Instituciones educativas
- **Datos**: Cursos, estudiantes, tareas, calificaciones
- **Integración**: Google Classroom como fuente principal

## 📊 Dataset Mock

### Cursos de Ejemplo
1. **eCommerce Specialist** (~150 students)
2. **Digital Marketing Specialist** (~150 students)

### Tipos de Tareas
- **Initial Assessment**: Knowledge evaluation
- **Applied Practice**: Module exercises
- **Final Project**: Integrative deliverable

### Estados de Tareas
- **Submitted**: Completed on time
- **Pending**: Within deadline
- **Late**: Past deadline but accepted
- **Not Submitted**: No delivery

## 🚀 Quick Reference

### Comandos Principales
```bash
# Backend
python -m uvicorn app.main:app --reload
python -m pytest

# Frontend
npm run dev
npm run build
npm run test
```

### URLs Importantes
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

### Configuraciones Clave
- **Modo**: MOCK (desarrollo) / GOOGLE (producción)
- **Base de datos**: MongoDB local
- **Autenticación**: JWT tokens
- **CORS**: Configurado para frontend

## 📋 Criterios de Aceptación Globales

### Funcionalidad
- [ ] Sistema funciona en modo MOCK y GOOGLE
- [ ] Autenticación JWT implementada
- [ ] Roles de usuario funcionando
- [ ] Dashboards por rol implementados

### Calidad
- [ ] Cobertura de tests ≥70%
- [ ] Linting y formateo automático
- [ ] Documentación actualizada
- [ ] Performance optimizada

### Accesibilidad
- [ ] WCAG 2.1 AA compliance
- [ ] Navegación por teclado
- [ ] Screen reader compatible
- [ ] Contraste adecuado

## 🔄 Flujo de Implementación

1. **Implementar Stage 1** → Fundaciones y autenticación
2. **Testing Stage 1** → Validar fundaciones y autenticación
3. **Implementar Stage 2** → Google y dashboards básicos
4. **Testing Stage 2** → Validar integración y visualización
5. **Implementar Stage 3** → Visualización avanzada y notificaciones
6. **Testing Stage 3** → Validar experiencia de usuario
7. **Implementar Stage 4** → Integración completa y calidad
8. **Testing final** → Validación completa

## 📝 Notas para Desarrolladores

- **Commits atómicos**: Un commit por funcionalidad
- **Mensajes descriptivos**: Usar formato convencional
- **Testing primero**: TDD en todos los stages
- **Documentación**: Mantener actualizada
- **Performance**: Optimizar desde el inicio

---

**Este archivo sirve como punto de entrada para comprender el proyecto completo con estructura consolidada. Leer los contratos individuales para detalles específicos de implementación.**
