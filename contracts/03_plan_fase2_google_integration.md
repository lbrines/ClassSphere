---
title: "ClassSphere - Fase 2: Integración Google TDD"
version: "1.0"
type: "documentation"
date: "2025-10-04"
author: "Sistema de Contratos LLM"
related_files:
  - "01_plam_index.md"
  - "02_plan_fase1_fundaciones.md"
  - "04_plan_fase3_visualizacion.md"
---

[← Fase 1: Fundaciones](02_plan_fase1_fundaciones.md) | [Índice](01_plam_index.md) | [Siguiente → Fase 3: Visualización](04_plan_fase3_visualizacion.md)

# Fase 2: Integración Google TDD

## Objetivos de la Fase

Esta fase implementa la integración completa con Google Classroom API siguiendo metodología TDD:

1. **Backend Google**: Servicios de integración con Google Classroom API
2. **Frontend Google**: Componentes de visualización de datos de Google
3. **Modo Dual**: Sistema capaz de funcionar con API real o mocks
4. **Métricas y Dashboards**: Visualización de datos educativos por rol

## Duración Estimada: 8-10 días

### Distribución de Tareas

**Días 13-15: Backend Google**
- Tests para Google Classroom API
- Implementación GoogleService + ClassroomService
- Modo dual (Google/Mock)
- Endpoints dashboard por rol

**Días 16-18: Frontend Google**
- Tests para componentes Google
- Selector de modo + Lista de cursos
- Dashboards por rol con ApexCharts v5.3.5
- Métricas básicas y visualización

**Días 19-21: Métricas y Dashboards**
- Tests para métricas avanzadas
- KPIs educativos + agregaciones
- Dashboards interactivos
- Cache y optimización

**Días 22-23: Integración Google**
- Tests de integración completa
- Validación modo dual
- Performance tuning
- Documentación Google

## Estructura de Tests Backend

### Requisitos Técnicos Obligatorios

1. **Timeouts en Tests de API Externa**
   ```python
   # test_google_api.py
   @pytest.mark.asyncio
   async def test_fetch_courses_with_timeout():
       """Test fetch courses con timeout explícito"""
       google_service = GoogleService()
       result = await asyncio.wait_for(
           google_service.fetch_courses(),
           timeout=5.0  # Timeout más largo para API externa
       )
       assert isinstance(result, list)
       assert len(result) > 0
   ```

2. **Modo Dual (Real/Mock)**
   ```python
   # test_dual_mode.py
   def test_google_service_in_mock_mode():
       """Test servicio en modo mock"""
       google_service = GoogleService(mode="mock")
       courses = google_service.get_courses()
       assert len(courses) > 0
       # Verificar que los datos coinciden con los mocks
       assert courses[0]["id"] == "mock-course-001"
   
   def test_google_service_in_real_mode():
       """Test servicio en modo real"""
       # Skip si no hay credenciales disponibles
       if not os.getenv("GOOGLE_CREDENTIALS"):
           pytest.skip("Google credentials not available")
       
       google_service = GoogleService(mode="real")
       courses = google_service.get_courses()
       assert len(courses) > 0
       # Verificar estructura pero no valores específicos
       assert "id" in courses[0]
   ```

3. **Validación de Mocks con Documentación Oficial**
   ```python
   # test_mock_validation.py
   def test_course_mock_matches_google_schema():
       """Test que los mocks coinciden con el esquema oficial de Google"""
       mock_service = MockService()
       course = mock_service.get_course("mock-course-001")
       
       # Validar estructura según documentación oficial
       assert "id" in course
       assert "name" in course
       assert "section" in course
       assert "descriptionHeading" in course
       assert "room" in course
       assert "ownerId" in course
       assert "creationTime" in course
   ```

### Estructura de Directorios de Tests

```
backend/
└── tests/
    ├── unit/
    │   ├── services/
    │   │   ├── test_google_service.py
    │   │   ├── test_classroom_service.py
    │   │   └── test_metrics_service.py
    │   └── api/
    │       ├── test_google_endpoints.py
    │       └── test_dashboard_endpoints.py
    ├── integration/
    │   ├── test_google_integration.py
    │   └── test_dashboard_integration.py
    └── mocks/
        ├── google/
        │   ├── courses.json
        │   ├── students.json
        │   └── teachers.json
        └── test_mock_validation.py
```

### Tests Unitarios Críticos

```python
# test_classroom_service.py
@pytest.mark.asyncio
async def test_get_course_details():
    """Test obtener detalles de un curso"""
    classroom_service = ClassroomService()
    course_id = "mock-course-001"
    
    result = await asyncio.wait_for(
        classroom_service.get_course_details(course_id),
        timeout=3.0  # Timeout obligatorio
    )
    
    assert result is not None
    assert result["id"] == course_id
    assert "name" in result
    assert "teachers" in result
    assert "students" in result

@pytest.mark.asyncio
async def test_get_course_details_not_found():
    """Test obtener detalles de un curso inexistente"""
    classroom_service = ClassroomService()
    course_id = "non-existent-course"
    
    with pytest.raises(CourseNotFoundError):
        await asyncio.wait_for(
            classroom_service.get_course_details(course_id),
            timeout=3.0  # Timeout obligatorio
        )
```

### Tests de Integración

```python
# test_dashboard_integration.py
def test_teacher_dashboard_endpoint():
    """Test endpoint de dashboard para profesor"""
    client = TestClient(app)
    
    # Login como profesor
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "teacher@example.com", "password": "password"}
    )
    token = login_response.json()["data"]["token"]
    
    # Obtener dashboard
    response = client.get(
        "/api/v1/dashboards/teacher",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()["data"]
    assert "courses" in data
    assert "metrics" in data
    assert "recentActivity" in data
```

## Estructura de Tests Frontend

### Requisitos Técnicos Obligatorios

1. **Timeouts en Tests de Componentes**
   ```typescript
   // CourseList.test.tsx
   test('loads courses within timeout', async () => {
     render(<CourseList />);
     
     // Esperar carga con timeout
     await waitFor(() => {
       expect(screen.getByText('Course 1')).toBeInTheDocument();
     }, { timeout: 3000 });
   });
   ```

2. **Validación de Mocks**
   ```typescript
   // test_mock_validation.ts
   test('course mock matches Google schema', () => {
     const mockCourse = mockData.courses[0];
     
     // Validar estructura según documentación oficial
     expect(mockCourse).toHaveProperty('id');
     expect(mockCourse).toHaveProperty('name');
     expect(mockCourse).toHaveProperty('section');
     expect(mockCourse).toHaveProperty('descriptionHeading');
     expect(mockCourse).toHaveProperty('room');
     expect(mockCourse).toHaveProperty('ownerId');
     expect(mockCourse).toHaveProperty('creationTime');
   });
   ```

### Estructura de Directorios de Tests

```
frontend/
└── src/
    ├── components/
    │   ├── google/
    │   │   ├── CourseList.tsx
    │   │   ├── CourseList.test.tsx
    │   │   ├── ModeSelector.tsx
    │   │   └── ModeSelector.test.tsx
    │   └── dashboard/
    │       ├── TeacherDashboard.tsx
    │       └── TeacherDashboard.test.tsx
    ├── hooks/
    │   ├── useGoogleClassroom.ts
    │   └── useGoogleClassroom.test.ts
    └── mocks/
        └── google/
            ├── courses.ts
            └── students.ts
```

### Tests de Componentes

```typescript
// CourseList.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import CourseList from './CourseList';

// Mock de useGoogleClassroom
vi.mock('../../hooks/useGoogleClassroom', () => ({
  useGoogleClassroom: () => ({
    courses: [
      { id: 'course-1', name: 'Course 1' },
      { id: 'course-2', name: 'Course 2' }
    ],
    isLoading: false,
    error: null
  })
}));

describe('CourseList', () => {
  it('renders course list correctly', async () => {
    render(<CourseList />);
    
    // Esperar con timeout
    await waitFor(() => {
      expect(screen.getByText('Course 1')).toBeInTheDocument();
      expect(screen.getByText('Course 2')).toBeInTheDocument();
    }, { timeout: 2000 });
  });
  
  it('shows loading state', () => {
    // Override mock para estado de carga
    vi.mocked(useGoogleClassroom).mockReturnValue({
      courses: [],
      isLoading: true,
      error: null
    });
    
    render(<CourseList />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });
  
  it('shows error state', async () => {
    // Override mock para estado de error
    vi.mocked(useGoogleClassroom).mockReturnValue({
      courses: [],
      isLoading: false,
      error: 'Failed to load courses'
    });
    
    render(<CourseList />);
    expect(screen.getByText(/failed to load courses/i)).toBeInTheDocument();
  });
});
```

### Tests de Hooks

```typescript
// useGoogleClassroom.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { useGoogleClassroom } from './useGoogleClassroom';

// Mock de fetch
global.fetch = vi.fn();

describe('useGoogleClassroom', () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });
  
  it('fetches courses successfully', async () => {
    // Mock de respuesta exitosa
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        data: {
          courses: [
            { id: 'course-1', name: 'Course 1' },
            { id: 'course-2', name: 'Course 2' }
          ]
        }
      })
    } as Response);
    
    const { result } = renderHook(() => useGoogleClassroom());
    
    // Esperar con timeout
    await waitFor(() => {
      expect(result.current.courses).toHaveLength(2);
      expect(result.current.isLoading).toBe(false);
      expect(result.current.error).toBeNull();
    }, { timeout: 3000 });
  });
  
  it('handles fetch error', async () => {
    // Mock de respuesta con error
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error'
    } as Response);
    
    const { result } = renderHook(() => useGoogleClassroom());
    
    // Esperar con timeout
    await waitFor(() => {
      expect(result.current.courses).toHaveLength(0);
      expect(result.current.isLoading).toBe(false);
      expect(result.current.error).not.toBeNull();
    }, { timeout: 3000 });
  });
});
```

## Mocks de Google Classroom API

### Estructura de Mocks Validados

Los mocks deben seguir exactamente la estructura de la [API de Google Classroom](https://developers.google.com/workspace/classroom/reference/rest?hl=es-419):

```json
// mocks/google/courses.json
[
  {
    "id": "mock-course-001",
    "name": "Matemáticas Avanzadas",
    "section": "Sección A",
    "descriptionHeading": "Curso de matemáticas avanzadas",
    "description": "Este curso cubre álgebra, cálculo y estadística",
    "room": "Aula 101",
    "ownerId": "teacher-001",
    "creationTime": "2025-01-15T10:00:00.000Z",
    "updateTime": "2025-01-15T10:00:00.000Z",
    "enrollmentCode": "abc123",
    "courseState": "ACTIVE",
    "alternateLink": "https://classroom.google.com/c/mock-course-001",
    "teacherGroupEmail": "teacher-group@example.com",
    "courseGroupEmail": "course-group@example.com",
    "teacherFolder": {
      "id": "folder-001",
      "title": "Matemáticas Avanzadas",
      "alternateLink": "https://drive.google.com/drive/folders/folder-001"
    },
    "guardiansEnabled": true,
    "calendarId": "calendar-001"
  }
]
```

### Validación de Mocks

```python
# test_mock_validation.py
def test_course_mock_structure():
    """Validar estructura de mock de curso según API de Google"""
    with open("tests/mocks/google/courses.json", "r") as f:
        courses = json.load(f)
    
    course = courses[0]
    
    # Campos requeridos según documentación de Google Classroom API
    required_fields = [
        "id", "name", "section", "descriptionHeading", "description",
        "room", "ownerId", "creationTime", "updateTime", "enrollmentCode",
        "courseState", "alternateLink", "teacherGroupEmail", 
        "courseGroupEmail", "teacherFolder", "guardiansEnabled", "calendarId"
    ]
    
    for field in required_fields:
        assert field in course, f"Campo requerido '{field}' no encontrado"
    
    # Validar estructura de teacherFolder
    assert "id" in course["teacherFolder"]
    assert "title" in course["teacherFolder"]
    assert "alternateLink" in course["teacherFolder"]
```

## Comandos de Testing

### Backend Tests

```bash
# Tests unitarios de servicios Google
pytest tests/unit/services/test_google_service.py --cov=src.app.services.google_service

# Tests de integración de dashboards
pytest tests/integration/test_dashboard_integration.py

# Validación de mocks
pytest tests/mocks/test_mock_validation.py

# Tests completos con cobertura
pytest tests/ --cov=src --cov-report=term-missing
```

### Frontend Tests

```bash
# Tests de componentes Google
npm run test -- --testPathPattern=src/components/google

# Tests de hooks Google
npm run test -- --testPathPattern=src/hooks/useGoogleClassroom

# Tests completos con cobertura
npm run test -- --coverage
```

## Criterios de Aceptación

### Backend Google

- [ ] Integración completa con Google Classroom API
- [ ] Modo dual (real/mock) funcionando correctamente
- [ ] Endpoints para dashboards por rol
- [ ] Caché de datos de Google con Redis
- [ ] Tests con cobertura ≥90% en módulos críticos

### Frontend Google

- [ ] Componentes para visualización de cursos
- [ ] Selector de modo (real/mock)
- [ ] Dashboards por rol con ApexCharts
- [ ] Métricas educativas básicas
- [ ] Tests con cobertura ≥80%

### Integración Google

- [ ] Comunicación frontend-backend para datos de Google
- [ ] Manejo de errores de API
- [ ] Performance optimizada (<2s carga de dashboard)
- [ ] Tests de integración completos

## Referencias

Para más detalles sobre la implementación TDD con Google Classroom API, consultar:
- [API de Google Classroom](https://developers.google.com/workspace/classroom/reference/rest?hl=es-419)
- [Estrategia de Testing Unificada](principal/09_ClassSphere_testing.md)
- [TDD Best Practices](extra/TDD_BEST_PRACTICES.md)

---

[← Fase 1: Fundaciones](02_plan_fase1_fundaciones.md) | [Índice](01_plam_index.md) | [Siguiente → Fase 3: Visualización](04_plan_fase3_visualizacion.md)
