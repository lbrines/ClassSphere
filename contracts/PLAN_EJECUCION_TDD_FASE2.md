# Plan de Ejecución TDD: Fase 2 - Google Integration

---
**Autor**: Sistema de Planes de Ejecución TDD
**Fecha**: 2025-10-04
**Versión**: 1.0
**Fase**: Google Integration TDD (Días 13-23)
---

## Objetivo de la Fase

Implementar la integración completa con Google Classroom API siguiendo metodología TDD estricta, con modo dual (producción/mock), dashboards por rol y métricas básicas, garantizando la cobertura 100% en todos los componentes de integración.

## Principios TDD de la Fase 2

### Ciclo TDD Estricto para Integración

1. **Red**: Escribir test que falle para cada componente de integración
2. **Green**: Implementar código mínimo para integración funcional
3. **Refactor**: Optimizar integración manteniendo tests verdes

### Timeouts para Tests de Integración

Todos los tests de la Fase 2 tendrán timeouts específicos para servicios externos:

```python
# Tests unitarios de integración: 3 segundos máximo
@pytest.mark.asyncio(timeout=3.0)
async def test_google_classroom_service_unit():
    # Test code here
    pass

# Tests de integración con mocks: 5 segundos máximo
@pytest.mark.asyncio(timeout=5.0)
async def test_google_classroom_integration():
    # Test code here
    pass

# Tests de integración real (opcional): 10 segundos máximo
@pytest.mark.asyncio(timeout=10.0)
@pytest.mark.skipif(os.getenv("SKIP_REAL_API_TESTS") == "1", reason="Skipping real API tests")
async def test_google_classroom_real_api():
    # Test code here
    pass
```

### Mocks Validados con Documentación Oficial

Todos los mocks de Google Classroom API estarán validados con la [documentación oficial](https://developers.google.com/workspace/classroom/reference/rest?hl=es-419):

```python
@pytest.fixture
def mock_google_classroom_api():
    """Mock Google Classroom API con datos validados según documentación oficial"""
    mock_api = AsyncMock()
    
    # Cursos - https://developers.google.com/classroom/reference/rest/v1/courses
    mock_api.courses().list().execute.return_value = {
        "courses": [
            {
                "id": "123456789",
                "name": "Matemáticas 101",
                "section": "Período 2",
                "descriptionHeading": "Introducción a las Matemáticas",
                "description": "Un curso básico de matemáticas",
                "room": "301",
                "ownerId": "teacher_id_1",
                "creationTime": "2025-01-01T12:00:00.000Z",
                "updateTime": "2025-01-02T12:00:00.000Z",
                "enrollmentCode": "abc123",
                "courseState": "ACTIVE",
                "alternateLink": "https://classroom.google.com/c/MTIzNDU2Nzg5",
                "teacherGroupEmail": "matematicas101-teachers@example.com",
                "courseGroupEmail": "matematicas101-all@example.com",
                "teacherFolder": {
                    "id": "folder_id_1",
                    "title": "Matemáticas 101",
                    "alternateLink": "https://drive.google.com/drive/folders/folder_id_1"
                },
                "guardiansEnabled": True,
                "calendarId": "calendar_id_1"
            }
        ]
    }
    
    # Estudiantes - https://developers.google.com/classroom/reference/rest/v1/courses.students
    mock_api.courses().students().list().execute.return_value = {
        "students": [
            {
                "courseId": "123456789",
                "userId": "student_id_1",
                "profile": {
                    "id": "student_id_1",
                    "name": {
                        "givenName": "Juan",
                        "familyName": "Pérez",
                        "fullName": "Juan Pérez"
                    },
                    "emailAddress": "juan.perez@example.com",
                    "photoUrl": "https://example.com/photos/juan.jpg"
                }
            }
        ]
    }
    
    # Trabajos de clase - https://developers.google.com/classroom/reference/rest/v1/courses.courseWork
    mock_api.courses().courseWork().list().execute.return_value = {
        "courseWork": [
            {
                "id": "coursework_id_1",
                "courseId": "123456789",
                "title": "Tarea de Álgebra",
                "description": "Resolver ecuaciones de primer grado",
                "materials": [
                    {
                        "driveFile": {
                            "driveFile": {
                                "id": "file_id_1",
                                "title": "Ejercicios.pdf",
                                "alternateLink": "https://drive.google.com/file/d/file_id_1/view"
                            }
                        }
                    }
                ],
                "state": "PUBLISHED",
                "alternateLink": "https://classroom.google.com/c/MTIzNDU2Nzg5/a/coursework_id_1",
                "creationTime": "2025-01-10T10:00:00.000Z",
                "updateTime": "2025-01-10T10:00:00.000Z",
                "dueDate": {
                    "year": 2025,
                    "month": 1,
                    "day": 17
                },
                "dueTime": {
                    "hours": 23,
                    "minutes": 59
                },
                "maxPoints": 100,
                "workType": "ASSIGNMENT",
                "submissionModificationMode": "MODIFIABLE_UNTIL_TURNED_IN"
            }
        ]
    }
    
    return mock_api
```

## Plan de Implementación TDD

### Día 13-15: Google Classroom API TDD

#### Día 13: Configuración Google Classroom API

1. **Google Classroom API v1 configuración**
   - Test: Verificar configuración de API
   - Implementación: Configurar cliente de API
   - Refactor: Optimizar manejo de credenciales

2. **GoogleService implementación**
   - Test: Verificar funcionalidad básica
   - Implementación: Implementar servicio base
   - Refactor: Optimizar estructura

#### Día 14: ClassroomService TDD

1. **ClassroomService implementación**
   - Test: Verificar funcionalidad de servicio
   - Implementación: Implementar servicio completo
   - Refactor: Optimizar manejo de datos

2. **Modo dual (Google/Mock) con switching**
   - Test: Verificar cambio entre modos
   - Implementación: Implementar sistema de switching
   - Refactor: Optimizar detección automática

#### Día 15: Endpoints Básicos TDD

1. **Endpoints para cursos, estudiantes, assignments**
   - Test: Verificar funcionamiento de endpoints
   - Implementación: Implementar endpoints
   - Refactor: Optimizar respuestas

2. **Tests de integración con Google API**
   - Test: Verificar integración con mocks
   - Implementación: Implementar tests completos
   - Refactor: Optimizar cobertura

### Día 16-18: Dashboards por Rol TDD

#### Día 16: Endpoints Dashboard TDD

1. **Endpoints dashboard por rol (admin, coordinador, teacher, estudiante)**
   - Test: Verificar endpoints por rol
   - Implementación: Implementar endpoints específicos
   - Refactor: Optimizar filtrado de datos

2. **KPIs educativos (engagement, risk, performance)**
   - Test: Verificar cálculo de KPIs
   - Implementación: Implementar cálculos
   - Refactor: Optimizar algoritmos

#### Día 17: Métricas TDD

1. **Métricas agregadas y comparativas**
   - Test: Verificar cálculo de métricas
   - Implementación: Implementar métricas
   - Refactor: Optimizar rendimiento

2. **Cache Redis para optimización**
   - Test: Verificar funcionamiento de cache
   - Implementación: Implementar sistema de cache
   - Refactor: Optimizar estrategia de cache

#### Día 18: Rate Limiting TDD

1. **Rate limiting específico para Google API**
   - Test: Verificar funcionamiento de rate limiting
   - Implementación: Implementar sistema de rate limiting
   - Refactor: Optimizar parámetros

2. **Tests de rendimiento con cache**
   - Test: Verificar mejora de rendimiento
   - Implementación: Implementar tests de rendimiento
   - Refactor: Optimizar configuración

### Día 19-21: Frontend Google TDD

#### Día 19: UI Google TDD

1. **Selector de modo (Google/Mock)**
   - Test: Verificar funcionamiento de selector
   - Implementación: Implementar componente
   - Refactor: Optimizar UX

2. **Componentes Google (GoogleConnect, CourseList, ModeSelector)**
   - Test: Verificar renderizado de componentes
   - Implementación: Implementar componentes
   - Refactor: Optimizar UI

#### Día 20: Dashboards Frontend TDD

1. **Dashboards por rol con ApexCharts v5.3.5**
   - Test: Verificar renderizado de dashboards
   - Implementación: Implementar dashboards
   - Refactor: Optimizar visualización

2. **Hooks de Google (useGoogleClassroom, useMetrics)**
   - Test: Verificar funcionamiento de hooks
   - Implementación: Implementar hooks
   - Refactor: Optimizar manejo de estado

#### Día 21: Visualizaciones TDD

1. **Visualizaciones básicas (bar, line, pie charts)**
   - Test: Verificar renderizado de gráficos
   - Implementación: Implementar gráficos
   - Refactor: Optimizar interactividad

2. **Tests de integración frontend-backend**
   - Test: Verificar integración completa
   - Implementación: Implementar tests
   - Refactor: Optimizar cobertura

### Día 22-23: Métricas y Optimización TDD

#### Día 22: Métricas Avanzadas TDD

1. **Métricas avanzadas y predictivas**
   - Test: Verificar cálculo de métricas avanzadas
   - Implementación: Implementar algoritmos
   - Refactor: Optimizar precisión

2. **Dashboards interactivos con drill-down**
   - Test: Verificar funcionalidad de drill-down
   - Implementación: Implementar interactividad
   - Refactor: Optimizar UX

#### Día 23: Optimización TDD

1. **Cache y optimización de queries**
   - Test: Verificar mejora de rendimiento
   - Implementación: Implementar estrategias de cache
   - Refactor: Optimizar consultas

2. **Performance tuning (<2s dashboard load)**
   - Test: Verificar tiempo de carga
   - Implementación: Implementar optimizaciones
   - Refactor: Ajustar para cumplir objetivo de 2s

3. **Documentación Google integration**
   - Test: Verificar claridad de documentación
   - Implementación: Implementar documentación
   - Refactor: Optimizar ejemplos

## Criterios de Aceptación TDD Fase 2

- [ ] Mocks de Google API funcionan correctamente
- [ ] Modo dual switching sin errores
- [ ] Tests de OAuth completos
- [ ] Tests de Classroom API mockeados
- [ ] Performance <2s para carga de dashboards
- [ ] Cache Redis funciona correctamente

## Templates TDD Estándar

### Template para Tests de Google Classroom API

```python
"""
Test file for google_classroom_service.py

CRITICAL OBJECTIVES:
- Verify Google Classroom API integration
- Test mode switching (Google/Mock)

DEPENDENCIES:
- AsyncMock for Google API
- Mock data validated with official documentation
"""

import pytest
from unittest.mock import AsyncMock, patch
import os

from src.app.services.google_classroom_service import GoogleClassroomService
from src.app.core.config import settings

# BEGINNING: Critical tests for core functionality
@pytest.fixture
def mock_google_classroom_api():
    """Mock Google Classroom API con datos validados según documentación oficial"""
    mock_api = AsyncMock()
    
    # Cursos
    mock_api.courses().list().execute.return_value = {
        "courses": [
            {
                "id": "123456789",
                "name": "Matemáticas 101",
                "section": "Período 2",
                "descriptionHeading": "Introducción a las Matemáticas",
                "description": "Un curso básico de matemáticas",
                "room": "301",
                "ownerId": "teacher_id_1",
                "creationTime": "2025-01-01T12:00:00.000Z",
                "updateTime": "2025-01-02T12:00:00.000Z",
                "enrollmentCode": "abc123",
                "courseState": "ACTIVE",
                "alternateLink": "https://classroom.google.com/c/MTIzNDU2Nzg5",
                "teacherGroupEmail": "matematicas101-teachers@example.com",
                "courseGroupEmail": "matematicas101-all@example.com",
                "teacherFolder": {
                    "id": "folder_id_1",
                    "title": "Matemáticas 101",
                    "alternateLink": "https://drive.google.com/drive/folders/folder_id_1"
                },
                "guardiansEnabled": True,
                "calendarId": "calendar_id_1"
            }
        ]
    }
    
    return mock_api

@pytest.mark.asyncio(timeout=3.0)
async def test_get_courses(mock_google_classroom_api):
    # Arrange
    with patch('src.app.services.google_classroom_service.build_classroom_service') as mock_build:
        mock_build.return_value = mock_google_classroom_api
        service = GoogleClassroomService()
        
        # Act
        courses = await service.get_courses()
        
        # Assert
        assert len(courses) == 1
        assert courses[0]["id"] == "123456789"
        assert courses[0]["name"] == "Matemáticas 101"
        mock_google_classroom_api.courses().list().execute.assert_called_once()

# MIDDLE: Detailed implementation tests
@pytest.mark.asyncio(timeout=3.0)
async def test_mode_switching():
    # Arrange
    service = GoogleClassroomService()
    
    # Act & Assert: Default mode
    assert service.get_mode() == "google"  # Default mode
    
    # Act & Assert: Switch to mock mode
    await service.set_mode("mock")
    assert service.get_mode() == "mock"
    
    # Act & Assert: Switch back to google mode
    await service.set_mode("google")
    assert service.get_mode() == "google"
    
    # Act & Assert: Invalid mode
    with pytest.raises(ValueError):
        await service.set_mode("invalid")

@pytest.mark.asyncio(timeout=3.0)
async def test_mock_mode_data():
    # Arrange
    service = GoogleClassroomService()
    await service.set_mode("mock")
    
    # Act
    courses = await service.get_courses()
    
    # Assert
    assert len(courses) > 0
    assert "id" in courses[0]
    assert "name" in courses[0]

# END: Verification and next steps
@pytest.mark.asyncio(timeout=10.0)
@pytest.mark.skipif(os.getenv("SKIP_REAL_API_TESTS") == "1", reason="Skipping real API tests")
async def test_real_api_connection():
    # Arrange
    service = GoogleClassroomService()
    await service.set_mode("google")
    
    # Act
    try:
        health_status = await service.check_api_health()
        
        # Assert
        assert health_status is True
    except Exception as e:
        pytest.skip(f"Skipping real API test: {str(e)}")
```

### Template para Tests de Cache Redis

```python
"""
Test file for dashboard_cache.py

CRITICAL OBJECTIVES:
- Verify dashboard data caching
- Test cache invalidation

DEPENDENCIES:
- AsyncMock for Redis client
- Mock data for dashboards
"""

import pytest
import json
from unittest.mock import AsyncMock, patch
from datetime import datetime, timedelta

from src.app.services.dashboard_service import DashboardService
from src.app.core.cache import get_redis_client

# BEGINNING: Critical tests for core functionality
@pytest.fixture
def mock_dashboard_data():
    """Mock data for dashboard"""
    return {
        "summary": {
            "total_students": 120,
            "active_courses": 5,
            "assignments_pending": 25,
            "average_grade": 85.5
        },
        "charts": {
            "performance": [
                {"name": "Matemáticas", "value": 82},
                {"name": "Ciencias", "value": 88},
                {"name": "Historia", "value": 75},
                {"name": "Literatura", "value": 90}
            ]
        },
        "timestamp": datetime.now().isoformat()
    }

@pytest.mark.asyncio(timeout=3.0)
async def test_dashboard_cache_hit():
    # Arrange
    dashboard_service = DashboardService()
    mock_data = mock_dashboard_data()
    cache_key = "dashboard:admin:summary"
    
    with patch('src.app.core.cache.get_redis_client') as mock_get_redis:
        mock_redis = AsyncMock()
        mock_get_redis.return_value = mock_redis
        mock_redis.get.return_value = json.dumps(mock_data)
        
        # Act
        result = await dashboard_service.get_admin_dashboard(use_cache=True)
        
        # Assert
        assert result == mock_data
        mock_redis.get.assert_called_once_with(cache_key)

# MIDDLE: Detailed implementation tests
@pytest.mark.asyncio(timeout=3.0)
async def test_dashboard_cache_miss():
    # Arrange
    dashboard_service = DashboardService()
    mock_data = mock_dashboard_data()
    cache_key = "dashboard:admin:summary"
    
    with patch('src.app.core.cache.get_redis_client') as mock_get_redis, \
         patch('src.app.services.dashboard_service.DashboardService._generate_admin_dashboard') as mock_generate:
        mock_redis = AsyncMock()
        mock_get_redis.return_value = mock_redis
        mock_redis.get.return_value = None
        mock_generate.return_value = mock_data
        
        # Act
        result = await dashboard_service.get_admin_dashboard(use_cache=True)
        
        # Assert
        assert result == mock_data
        mock_redis.get.assert_called_once_with(cache_key)
        mock_generate.assert_called_once()
        mock_redis.set.assert_called_once()

@pytest.mark.asyncio(timeout=3.0)
async def test_dashboard_cache_invalidation():
    # Arrange
    dashboard_service = DashboardService()
    cache_key = "dashboard:admin:summary"
    
    with patch('src.app.core.cache.get_redis_client') as mock_get_redis:
        mock_redis = AsyncMock()
        mock_get_redis.return_value = mock_redis
        
        # Act
        await dashboard_service.invalidate_dashboard_cache("admin")
        
        # Assert
        mock_redis.delete.assert_called_once_with(cache_key)

# END: Verification and next steps
@pytest.mark.asyncio(timeout=3.0)
async def test_dashboard_performance():
    # Arrange
    dashboard_service = DashboardService()
    
    with patch('src.app.services.dashboard_service.DashboardService._generate_admin_dashboard') as mock_generate, \
         patch('src.app.core.cache.get_redis_client') as mock_get_redis:
        mock_redis = AsyncMock()
        mock_get_redis.return_value = mock_redis
        mock_redis.get.return_value = None
        mock_generate.return_value = mock_dashboard_data()
        
        # Act
        start_time = datetime.now()
        await dashboard_service.get_admin_dashboard(use_cache=True)
        end_time = datetime.now()
        
        # Assert
        duration = (end_time - start_time).total_seconds()
        assert duration < 2.0  # Performance requirement: <2s
```

### Template para Tests de Modo Dual

```python
"""
Test file for dual_mode_service.py

CRITICAL OBJECTIVES:
- Verify mode switching functionality
- Test automatic fallback to mock mode

DEPENDENCIES:
- AsyncMock for Google API
- Mock data for testing
"""

import pytest
from unittest.mock import AsyncMock, patch

from src.app.services.dual_mode_service import DualModeService
from src.app.core.config import settings

# BEGINNING: Critical tests for core functionality
@pytest.mark.asyncio(timeout=3.0)
async def test_default_mode():
    # Arrange
    service = DualModeService()
    
    # Act
    mode = service.get_current_mode()
    
    # Assert
    assert mode == "google"  # Default mode should be google

@pytest.mark.asyncio(timeout=3.0)
async def test_switch_to_mock_mode():
    # Arrange
    service = DualModeService()
    
    # Act
    await service.switch_mode("mock")
    mode = service.get_current_mode()
    
    # Assert
    assert mode == "mock"

# MIDDLE: Detailed implementation tests
@pytest.mark.asyncio(timeout=3.0)
async def test_automatic_fallback():
    # Arrange
    service = DualModeService()
    
    with patch('src.app.services.google_classroom_service.build_classroom_service') as mock_build:
        mock_build.side_effect = Exception("API not available")
        
        # Act
        await service.initialize()
        mode = service.get_current_mode()
        
        # Assert
        assert mode == "mock"  # Should fallback to mock mode

@pytest.mark.asyncio(timeout=3.0)
async def test_get_data_in_google_mode():
    # Arrange
    service = DualModeService()
    mock_google_data = {"courses": [{"id": "real_course_id", "name": "Real Course"}]}
    
    with patch('src.app.services.google_classroom_service.GoogleClassroomService.get_courses') as mock_get_courses:
        mock_get_courses.return_value = mock_google_data
        
        # Act
        await service.switch_mode("google")
        data = await service.get_courses()
        
        # Assert
        assert data == mock_google_data
        mock_get_courses.assert_called_once()

@pytest.mark.asyncio(timeout=3.0)
async def test_get_data_in_mock_mode():
    # Arrange
    service = DualModeService()
    mock_data = {"courses": [{"id": "mock_course_id", "name": "Mock Course"}]}
    
    with patch('src.app.services.mock_service.MockService.get_courses') as mock_get_courses:
        mock_get_courses.return_value = mock_data
        
        # Act
        await service.switch_mode("mock")
        data = await service.get_courses()
        
        # Assert
        assert data == mock_data
        mock_get_courses.assert_called_once()

# END: Verification and next steps
@pytest.mark.asyncio(timeout=3.0)
async def test_invalid_mode():
    # Arrange
    service = DualModeService()
    
    # Act & Assert
    with pytest.raises(ValueError):
        await service.switch_mode("invalid_mode")
```

## Entregables TDD Fase 2

1. **Código Backend**
   - GoogleService completo
   - ClassroomService completo
   - Modo dual (Google/Mock)
   - Endpoints para cursos, estudiantes, assignments
   - Endpoints dashboard por rol
   - Cache Redis para optimización

2. **Código Frontend**
   - Selector de modo (Google/Mock)
   - Componentes Google
   - Dashboards por rol
   - Hooks de Google
   - Visualizaciones básicas

3. **Tests**
   - Tests unitarios para servicios Google
   - Tests de integración con mocks
   - Tests de rendimiento
   - Tests de frontend
   - Cobertura 100% en módulos de integración

4. **Documentación**
   - Documentación de API Google
   - Documentación de componentes
   - Documentación de mocks
   - Documentación de modo dual

## Próximos Pasos

1. Validar cumplimiento de criterios de aceptación
2. Preparar transición a Fase 3: Visualización Avanzada TDD
3. Revisar y actualizar documentación
4. Optimizar pipeline CI/CD para Fase 3
