---
title: "ClassSphere - Fase 2: Google Classroom Integration"
version: "3.0"
type: "development_plan"
priority: "HIGH"
max_tokens: 1500
duration: "10 días"
related_files:
  - "contracts/principal/05_ClassSphere_arquitectura.md"
  - "contracts/principal/06_ClassSphere_funcionalidades.md"
---

# Fase 2: Google Classroom Integration - Modo Dual

## 🎯 INICIO: Objetivos Críticos y Dependencias Bloqueantes

### Objetivo Principal
Integrar Google Classroom API con sistema de mocks preconfigurados, implementando modo dual (Google/Mock) y dashboards específicos por rol.

### Dependencias Bloqueantes
- **Fase 1 completada**: Backend Go + Frontend Angular funcionando
- **OAuth 2.0 configurado**: Google OAuth funcionando
- **Sistema de roles**: admin > coordinator > teacher > student operativo
- **JWT tokens**: Autenticación funcionando
- **Google API credentials**: Configuradas y validadas

### Componentes Críticos
- **Google Classroom API**: Integración completa con fallback a mocks
- **Modo Dual**: Alternancia entre API real y mocks controlados
- **Dashboards por Rol**: 4 dashboards específicos implementados
- **Sistema de Mocks**: Datos preconfigurados para testing

## 📅 MEDIO: Implementación Detallada Día por Día

### Día 1-2: Google Classroom API Service

**Objetivo**: Implementar servicio base de Google Classroom API

**TDD Implementación**:
```go
// tests/services/google_classroom_test.go - RED PHASE
func TestGoogleClassroomService(t *testing.T) {
    service := NewGoogleClassroomService(mockGoogleAPI)
    
    // Test que falla inicialmente
    courses, err := service.GetCourses("teacher@school.edu")
    assert.NoError(t, err)
    assert.Len(t, courses, 3) // Mock data
}

// internal/services/google_classroom.go - GREEN PHASE
type GoogleClassroomService struct {
    client *classroom.Service
    mock   bool
}

func (s *GoogleClassroomService) GetCourses(teacherEmail string) ([]Course, error) {
    if s.mock {
        return s.getMockCourses(), nil
    }
    // Implementación real con Google API
    return s.client.Courses.List().TeacherId(teacherEmail).Do()
}
```

**Patrones de Prevención**:
- **AsyncMock**: Para métodos async de Google API
- **Error Handling**: Fallback automático a mocks
- **Timeout Configuration**: 30s para requests a Google API

### Día 3-4: Sistema de Mocks Preconfigurados

**Objetivo**: Crear sistema robusto de mocks para desarrollo y testing

**Implementación**:
```go
// internal/mocks/google_classroom_mock.go
type MockGoogleClassroom struct {
    courses []Course
    students []Student
    assignments []Assignment
}

func (m *MockGoogleClassroom) GetMockCourses() []Course {
    return []Course{
        {
            ID: "course-1",
            Name: "Mathematics 101",
            Teacher: "teacher@school.edu",
            Students: 25,
        },
        {
            ID: "course-2", 
            Name: "Science 201",
            Teacher: "teacher@school.edu",
            Students: 18,
        },
    }
}
```

**TDD Implementación**:
```go
// tests/mocks/google_classroom_mock_test.go
func TestMockGoogleClassroom(t *testing.T) {
    mock := NewMockGoogleClassroom()
    
    courses := mock.GetMockCourses()
    assert.Len(t, courses, 2)
    assert.Equal(t, "Mathematics 101", courses[0].Name)
    
    // Test alternancia modo dual
    service := NewGoogleClassroomService(nil)
    service.SetMockMode(true)
    
    courses, err := service.GetCourses("teacher@school.edu")
    assert.NoError(t, err)
    assert.Len(t, courses, 2)
}
```

### Día 5-6: Dashboards por Rol - Backend

**Objetivo**: Implementar endpoints específicos para cada rol

**TDD Implementación**:
```go
// tests/handlers/dashboard_test.go
func TestAdminDashboard(t *testing.T) {
    e := echo.New()
    req := httptest.NewRequest("GET", "/admin/dashboard", nil)
    req.Header.Set("Authorization", "Bearer admin-token")
    
    w := httptest.NewRecorder()
    c := e.NewContext(req, w)
    
    handler := NewDashboardHandler(mockGoogleService)
    err := handler.GetAdminDashboard(c)
    
    assert.NoError(t, err)
    assert.Equal(t, 200, w.Code)
    
    var response DashboardResponse
    json.Unmarshal(w.Body.Bytes(), &response)
    assert.Equal(t, "admin", response.UserRole)
    assert.NotEmpty(t, response.TotalCourses)
}

// internal/handlers/dashboard.go - GREEN PHASE
func (h *DashboardHandler) GetAdminDashboard(c echo.Context) error {
    user := c.Get("user").(*jwt.Token)
    claims := user.Claims.(*jwt.StandardClaims)
    
    if claims.Role != "admin" {
        return echo.NewHTTPError(403, "Forbidden")
    }
    
    dashboard := h.googleService.GetAdminDashboardData()
    return c.JSON(200, dashboard)
}
```

**Endpoints Implementados**:
- `GET /admin/dashboard` - Estadísticas globales
- `GET /coordinator/dashboard` - Gestión de cursos
- `GET /teacher/dashboard` - Cursos del profesor
- `GET /student/dashboard` - Cursos del estudiante

### Día 7-8: Dashboards por Rol - Frontend Angular

**Objetivo**: Crear componentes Angular específicos para cada rol

**TDD Implementación**:
```typescript
// src/app/components/dashboard/admin-dashboard.component.spec.ts
describe('AdminDashboardComponent', () => {
  let component: AdminDashboardComponent;
  let fixture: ComponentFixture<AdminDashboardComponent>;
  let mockDashboardService: jasmine.SpyObj<DashboardService>;

  beforeEach(() => {
    const spy = jasmine.createSpyObj('DashboardService', ['getAdminDashboard']);
    
    TestBed.configureTestingModule({
      declarations: [AdminDashboardComponent],
      providers: [
        { provide: DashboardService, useValue: spy }
      ]
    });
    
    fixture = TestBed.createComponent(AdminDashboardComponent);
    component = fixture.componentInstance;
    mockDashboardService = TestBed.inject(DashboardService) as jasmine.SpyObj<DashboardService>;
  });

  it('should load admin dashboard data', () => {
    const mockData = {
      totalCourses: 50,
      totalStudents: 500,
      totalTeachers: 25
    };
    
    mockDashboardService.getAdminDashboard.and.returnValue(of(mockData));
    
    component.ngOnInit();
    
    expect(mockDashboardService.getAdminDashboard).toHaveBeenCalled();
    expect(component.dashboardData).toEqual(mockData);
  });
});
```

**Componentes Implementados**:
- `AdminDashboardComponent` - Estadísticas globales
- `CoordinatorDashboardComponent` - Gestión de cursos
- `TeacherDashboardComponent` - Cursos del profesor  
- `StudentDashboardComponent` - Cursos del estudiante

### Día 9-10: Integración Completa y Testing

**Objetivo**: Integrar frontend con backend y validar funcionamiento completo

**TDD Implementación**:
```typescript
// e2e/dashboard.e2e-spec.ts
import { test, expect } from '@playwright/test';

test.describe('Dashboard Integration', () => {
  test('admin dashboard loads correctly', async ({ page }) => {
    await page.goto('/login');
    await page.fill('[data-testid="email"]', 'admin@classsphere.edu');
    await page.fill('[data-testid="password"]', 'secret');
    await page.click('[data-testid="login-button"]');
    
    await expect(page).toHaveURL('/admin/dashboard');
    await expect(page.locator('[data-testid="total-courses"]')).toBeVisible();
    await expect(page.locator('[data-testid="total-students"]')).toBeVisible();
  });

  test('teacher dashboard shows teacher courses', async ({ page }) => {
    await page.goto('/login');
    await page.fill('[data-testid="email"]', 'teacher@classsphere.edu');
    await page.fill('[data-testid="password"]', 'secret');
    await page.click('[data-testid="login-button"]');
    
    await expect(page).toHaveURL('/teacher/dashboard');
    await expect(page.locator('[data-testid="my-courses"]')).toBeVisible();
  });
});
```

## ✅ FINAL: Checklist Verificación y Próximos Pasos

### Criterios de Aceptación Fase 2
- [ ] **Google Classroom API**: Integración funcionando con fallback a mocks
- [ ] **Modo Dual**: Alternancia Google/Mock operativa
- [ ] **Admin Dashboard**: Estadísticas globales mostradas
- [ ] **Coordinator Dashboard**: Gestión de cursos implementada
- [ ] **Teacher Dashboard**: Cursos del profesor listados
- [ ] **Student Dashboard**: Cursos del estudiante accesibles
- [ ] **Testing**: Cobertura ≥80% en servicios Google
- [ ] **E2E Tests**: Playwright tests para dashboards

### Comandos de Verificación
```bash
# Verificar modo dual
curl -H "Authorization: Bearer admin-token" http://localhost:8081/admin/dashboard

# Verificar mocks
curl -H "X-Mock-Mode: true" http://localhost:8081/courses

# Verificar frontend
ng test --watch=false
ng e2e --configuration=ci

# Verificar cobertura
go test ./internal/services/... -cover
```

### Funcionalidades Implementadas
- **Google Classroom API**: Cursos, estudiantes, tareas
- **Modo Mock**: Datos preconfigurados para testing
- **Dashboards Específicos**: Por rol con datos relevantes
- **Autenticación**: JWT + OAuth integrado
- **Testing**: Unit + Integration + E2E

### Próximos Pasos
1. **Iniciar Fase 3**: Visualización avanzada
2. **Implementar búsqueda**: Multi-entidad con filtros
3. **WebSocket**: Notificaciones real-time
4. **Gráficos**: D3.js + interactividad

### Métricas de Éxito
- **API Integration**: Google Classroom funcionando
- **Mock System**: Alternancia fluida Google/Mock
- **Dashboard Performance**: <2s load time
- **Testing Coverage**: ≥80% servicios críticos
- **User Experience**: Dashboards específicos por rol

**Estado**: ✅ LISTO PARA FASE 3  
**Duración**: 10 días  
**Integración**: Google Classroom API + Modo Dual  
**Dashboards**: 4 roles específicos implementados
