---
title: "ClassSphere - Fase 2: Google Integration con Coverage 100%"
version: "1.0"
type: "plan_fase"
date: "2025-10-05"
priority: "HIGH"
max_tokens: 1500
duration: "10 días"
---

# Fase 2: Google Integration con Coverage 100%

## 🎯 INICIO: Objetivos y Dependencias

### Objetivo de la Fase
Integrar Google Classroom API con sistema de mocks y dashboards por rol, manteniendo **Coverage 100%**.

### Dependencias Bloqueantes
- ✅ Fase 1 completada (100% coverage)
- ✅ OAuth 2.0 configurado y funcionando
- ✅ Sistema de roles implementado
- ✅ JWT tokens validados
- ✅ Google API credentials activas

### Criterios de Aceptación (Coverage 100%)
- [ ] Google Classroom API: 100% coverage con mocks
- [ ] Modo dual (Google/Mock): 100% coverage
- [ ] Dashboards por rol: 100% coverage (4 roles)
- [ ] Métricas básicas: 100% coverage
- [ ] Integration tests: 100% endpoints

## 📅 MEDIO: Implementación

### Día 1-2: Google Classroom Service (Coverage 100%)

**TDD: Google Service con Mocks**
```go
// backend/services/google_test.go
func TestGoogleClassroomService(t *testing.T) {
    mockClient := &MockGoogleClient{}
    service := NewGoogleClassroomService(mockClient)
    
    // Test list courses
    courses, err := service.ListCourses("user123")
    assert.NoError(t, err)
    assert.Len(t, courses, 3)
}

func TestGoogleServiceWithMockMode(t *testing.T) {
    service := NewGoogleClassroomService(nil)
    service.SetMockMode(true)
    
    courses, err := service.ListCourses("user123")
    assert.NoError(t, err)
    assert.Len(t, courses, 5) // Mock data
}
```

**Coverage**: 100% en google_service.go

### Día 3-4: Dashboards por Rol (Coverage 100%)

**TDD: Admin Dashboard Component**
```typescript
// frontend/src/app/dashboards/admin/admin-dashboard.component.spec.ts
describe('AdminDashboardComponent', () => {
  it('should display all metrics', () => {
    component.metrics = mockAdminMetrics;
    fixture.detectChanges();
    
    expect(fixture.nativeElement.querySelector('.total-users')).toBeTruthy();
    expect(fixture.nativeElement.querySelector('.total-courses')).toBeTruthy();
  });
  
  it('should load data on init', () => {
    spyOn(service, 'getAdminMetrics').and.returnValue(of(mockMetrics));
    component.ngOnInit();
    expect(service.getAdminMetrics).toHaveBeenCalled();
  });
});
```

**Coverage**: 100% en 4 dashboards (admin, coordinator, teacher, student)

### Día 5-7: Métricas y Visualización (Coverage 100%)

**TDD: Metrics Service**
```go
func TestCalculateCourseMetrics(t *testing.T) {
    service := NewMetricsService()
    
    metrics := service.CalculateCourseMetrics(mockCourses)
    
    assert.Equal(t, 10, metrics.TotalStudents)
    assert.Equal(t, 85.5, metrics.AverageGrade)
}
```

**Coverage**: 100% en metrics_service.go

### Día 8-10: Integration Tests (Coverage 100%)

**E2E: Dashboard Flows**
```typescript
test('admin can view all dashboards', async ({ page }) => {
  await loginAsAdmin(page);
  await page.goto('/dashboard/admin');
  await expect(page.locator('.admin-metrics')).toBeVisible();
});
```

**Coverage**: 100% flujos críticos

## ✅ FINAL: Verificación

### Checklist Fase 2
- [ ] Google API: 100% coverage
- [ ] Dashboards: 100% coverage (4 roles)
- [ ] E2E: 100% flujos dashboard
- [ ] CI/CD: Pipeline verde

### Comandos de Verificación
```bash
go test ./services/google/... -cover
ng test --include='**/dashboard/**' --code-coverage
npx playwright test e2e/dashboard/
```

---

**Estado Fase 2**: ✅ LISTA para Coverage 100%
**Próximo**: Fase 3 - Visualización Avanzada
