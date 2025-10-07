---
title: "ClassSphere - Unified Technical Glossary"
version: "4.0"
type: "documentation"
language: "English (Mandatory)"
date: "2025-10-07"
related_files:
  - "00_ClassSphere_index.md"
  - "01_ClassSphere_info_status.md"
  - "03_ClassSphere_analisis_critico.md"
---

[← Información del Proyecto](01_ClassSphere_info_status.md) | [Índice](00_ClassSphere_index.md) | [Siguiente → Análisis Críticos](03_ClassSphere_analisis_critico.md)

# Glosario Técnico Unificado

## Conceptos Fundamentales

### **Instalación Nueva Google Classroom**
**Definición**: Proceso de instalación desde cero de Google Classroom API con sistema de mocks preconfigurados para desarrollo y testing.

**Beneficios**:
- ✅ Instalación limpia sin dependencias de sistemas anteriores
- ✅ Testing robusto con mocks controlados para pruebas unitarias
- ✅ Despliegue flexible con alternancia entre mocks y API real
- ✅ Configuración rápida con mocks preconfigurados desde el inicio
- ✅ Debugging simplificado con datos de prueba predecibles

### **Template Method Pattern**
**Definición**: Patrón de diseño para estandarizar la construcción de mensajes de excepción, asegurando consistencia en el manejo de errores.

**Implementación**:
```python
class BaseAPIException(Exception):
    def _build_message(self, custom_message: str, default_message: str, **kwargs) -> str:
        """Template method para construcción de mensajes."""
        if custom_message and custom_message != default_message:
            return self._construct_custom_with_params(custom_message, **kwargs)
        return self._construct_automatic_message(default_message, **kwargs)
```

### **Error Prevention Protocols**
**Definición**: Metodología integral para prevenir errores comunes en desarrollo, incluyendo AsyncMock, CORS, warnings de deprecación y limpieza automática.

**Componentes**:
- AsyncMock para métodos async
- Tests simplificados de CORS
- Migración automática de APIs deprecadas
- Puerto 8000 como estándar arquitectónico
- Limpieza automática de procesos

### **Work Plan Development Rules (LLM 2024-2025)**
**Definición**: Reglas estrictas para crear planes de trabajo con LLMs basadas en papers de 2024-2025 sobre gestión de contexto y prevención de pérdida de información.

**Reglas de Context Window Management**:
```yaml
Chunking por Prioridad:
  CRITICAL: máximo 2000 tokens (autenticación, config, main.py)
  HIGH: máximo 1500 tokens (google_service, classroom_service)
  MEDIUM: máximo 1000 tokens (components, charts)
  LOW: máximo 800 tokens (admin, a11y)

Anti Lost-in-the-Middle Structure:
  inicio: objetivos críticos + dependencias bloqueantes
  medio: implementación detallada + casos de uso
  final: checklist verificación + próximos pasos
```

**Reglas de Logs Estructurados**:
```json
Template Obligatorio:
{
  "timestamp": "ISO 8601",
  "context_id": "unique-identifier",
  "token_count": "número",
  "context_priority": "CRITICAL|HIGH|MEDIUM|LOW",
  "status": "started|in_progress|completed|failed",
  "memory_management": {
    "chunk_position": "beginning|middle|end",
    "lost_in_middle_risk": "low|medium|high"
  }
}
```

**Contextual Retrieval Strategies (Anthropic 2024)**:
- Generar descripción contextualizada para cada chunk
- Usar RAG para conocimiento externo sin sobrecargar ventana interna
- Aplicar attention mechanisms en información crucial
- Implementar strategic truncation preservando elementos core

### **Quality Gates**
**Definición**: Criterios de validación obligatorios por fase que garantizan la calidad del sistema antes de avanzar al siguiente stage.

**Criterios por Fase**:
- **Fase 1**: Cobertura ≥100% módulos críticos, Performance <3s, 0 vulnerabilidades CRITICAL
- **Fase 2**: Performance <2s dashboard load, Google integration estable, Modo dual funcional
- **Fase 3**: Performance <1.5s load time, Accessibility básica, WebSocket estable
- **Fase 4**: Performance <1s load time, WCAG 2.2 AA completo, Production ready

## Terminología Estándar Unificada

### **Standard by Layer**
```
API Layer (Backend): English MANDATORY
├── User, Course, Assignment, Grade, Notification
├── UserRole, CourseStatus, AssignmentType
└── API endpoints, response schemas, error codes

UI Layer (Frontend): English MANDATORY
├── User, Course, Assignment, Grade, Notification
├── UserRole, CourseStatus, AssignmentType
└── Components, hooks, services
└── UI Text: English (Default with i18n support from Phase 1)

Documentation: English MANDATORY
├── All technical documentation in English
├── All code comments in English
├── All commit messages in English
├── All README files in English
└── User-facing content: English default with i18n extensibility

Code: English MANDATORY
├── Variable names in English
├── Function names in English
├── Class names in English
├── File names in English
└── All identifiers in English
```

### **Estados con Prefijos Semánticos**
```
Sincronización:
├── SYNC_COMPLETE: Sincronización completada exitosamente
├── SYNC_PENDING: Sincronización en proceso o pendiente
└── SYNC_ERROR: Error durante la sincronización

Autenticación:
├── AUTH_SUCCESS: Autenticación exitosa
├── AUTH_PENDING: Autenticación en proceso
└── AUTH_FAILED: Error de autenticación

Cursos:
├── COURSE_ACTIVE: Curso activo y disponible
├── COURSE_INACTIVE: Curso inactivo temporalmente
└── COURSE_ARCHIVED: Curso archivado (histórico)

Notificaciones:
├── NOTIF_SENT: Notificación enviada
├── NOTIF_DELIVERED: Notificación entregada
└── NOTIF_READ: Notificación leída por el usuario
```

### **Roles del Sistema**
- **Student**: Acceso de solo lectura a sus cursos asignados
- **Teacher**: Gestión completa de sus cursos asignados y estudiantes
- **Coordinator**: Supervisión de múltiples cursos y teachers
- **Admin**: Control total del sistema, usuarios y configuraciones

### **Modos de Operación**
- **Dual Mode**: Capacidad de alternar entre Google Classroom (producción) y Mock (desarrollo)
- **Google Mode**: Operación con datos reales de Google Classroom API
- **Mock Mode**: Operación con datos simulados para desarrollo y testing

## Arquitectura Semántica Simplificada

### **Puerto 8000 - Estándar Arquitectónico**
**Definición**: Puerto fijo obligatorio para el backend como estándar arquitectónico.

**Implementación**:
```python
# Servidor siempre en puerto 8000
if __name__ == "__main__":
    uvicorn.run(
        "src.app.main:app",
        host="127.0.0.1",
        port=8000,  # Puerto fijo arquitectónico
        reload=True
    )
```

### **Pydantic v2 - Migración Automática**
**Definición**: Migración transparente de Pydantic v1 a v2 con ConfigDict moderno.

**Implementación**:
```python
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    field_name: str = "default_value"
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )
```

### **FastAPI Lifespan - Context Manager Estándar**
**Definición**: Context manager moderno para manejo de ciclo de vida de la aplicación.

**Implementación**:
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    yield
    # Shutdown logic
```

## Referencias a Otros Documentos

- Para el análisis de dependencias, consulte [Análisis Críticos del Sistema](03_ClassSphere_analisis_critico.md).
- Para la implementación de la arquitectura, consulte [Arquitectura del Sistema](05_ClassSphere_arquitectura.md).
- Para los criterios de calidad, consulte [Criterios de Aceptación](12_ClassSphere_criterios_aceptacion.md).

---

[← Información del Proyecto](01_ClassSphere_info_status.md) | [Índice](00_ClassSphere_index.md) | [Siguiente → Análisis Críticos](03_ClassSphere_analisis_critico.md)
