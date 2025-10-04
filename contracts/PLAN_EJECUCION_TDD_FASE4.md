# Plan de Ejecución TDD: Fase 4 - Integración Completa

---
**Autor**: Sistema de Planes de Ejecución TDD
**Fecha**: 2025-10-04
**Versión**: 1.0
**Fase**: Integración Completa TDD (Días 35-45)
---

## Objetivo de la Fase

Implementar la integración completa del sistema con sincronización bidireccional, backup, accesibilidad WCAG 2.2 AA y preparación para producción, siguiendo metodología TDD estricta, garantizando la cobertura 100% en todos los componentes críticos.

## Principios TDD de la Fase 4

### Ciclo TDD Estricto para Integración Completa

1. **Red**: Escribir test que falle para cada componente de integración
2. **Green**: Implementar código mínimo para integración funcional
3. **Refactor**: Optimizar integración manteniendo tests verdes

### Timeouts para Tests de Integración Completa

Todos los tests de la Fase 4 tendrán timeouts específicos:

```python
# Tests unitarios de sincronización: 3 segundos máximo
@pytest.mark.asyncio(timeout=3.0)
async def test_sync_service_unit():
    # Test code here
    pass

# Tests de integración de sincronización: 8 segundos máximo
@pytest.mark.asyncio(timeout=8.0)
async def test_sync_integration():
    # Test code here
    pass

# Tests E2E: 15 segundos máximo
@pytest.mark.asyncio(timeout=15.0)
async def test_e2e_flow():
    # Test code here
    pass
```

### Puertos Fijos y Verificación

Verificación constante de puertos fijos:

```bash
echo "🔍 Verificación TDD: puertos 8000 y 3000..."
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "✅ Puerto 8000 ocupado por backend"
else
    echo "⚠️  Puerto 8000 libre. Iniciando backend..."
    cd backend && python -m uvicorn src.app.main:app --host 127.0.0.1 --port 8000 &
fi

if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null ; then
    echo "✅ Puerto 3000 ocupado por frontend"
else
    echo "⚠️  Puerto 3000 libre. Iniciando frontend..."
    cd frontend && npm run dev &
fi
```

## Plan de Implementación TDD

### Día 35-37: Google Completo TDD

#### Día 35: Sincronización Bidireccional TDD

1. **Sincronización bidireccional con Google Classroom**
   - Test: Verificar sincronización bidireccional
   - Implementación: Implementar servicio de sincronización
   - Refactor: Optimizar estrategia

2. **Detección de cambios y conflictos**
   - Test: Verificar detección de cambios
   - Implementación: Implementar algoritmo de detección
   - Refactor: Optimizar precisión

#### Día 36: Backup y Resolución de Conflictos TDD

1. **Sistema de backup automático y selectivo**
   - Test: Verificar creación y restauración de backups
   - Implementación: Implementar sistema de backup
   - Refactor: Optimizar almacenamiento

2. **Resolución de conflictos automática y manual**
   - Test: Verificar resolución de conflictos
   - Implementación: Implementar sistema de resolución
   - Refactor: Optimizar estrategias

#### Día 37: Webhooks y Admin Panel TDD

1. **Webhooks para eventos en tiempo real**
   - Test: Verificar recepción y procesamiento de webhooks
   - Implementación: Implementar sistema de webhooks
   - Refactor: Optimizar seguridad

2. **Admin panel Google con diagnósticos**
   - Test: Verificar funcionalidad del panel
   - Implementación: Implementar panel de administración
   - Refactor: Optimizar UX

### Día 38-40: Accesibilidad WCAG 2.2 AA TDD

#### Día 38: Navegación por Teclado TDD

1. **Keyboard navigation completa**
   - Test: Verificar navegación por teclado
   - Implementación: Implementar soporte completo
   - Refactor: Optimizar experiencia

2. **Focus management**
   - Test: Verificar gestión de focus
   - Implementación: Implementar sistema de focus
   - Refactor: Optimizar transiciones

#### Día 39: Screen Reader y Contraste TDD

1. **Screen reader support (ARIA + semantic HTML)**
   - Test: Verificar soporte para lectores de pantalla
   - Implementación: Implementar atributos ARIA
   - Refactor: Optimizar estructura semántica

2. **High contrast mode y color-blind friendly**
   - Test: Verificar modos de contraste
   - Implementación: Implementar temas alternativos
   - Refactor: Optimizar paletas de colores

#### Día 40: Accesibilidad Motora y Cognitiva TDD

1. **Motor accessibility (large targets, voice control)**
   - Test: Verificar accesibilidad motora
   - Implementación: Implementar targets grandes
   - Refactor: Optimizar interacción

2. **Cognitive accessibility (clear navigation, help text)**
   - Test: Verificar accesibilidad cognitiva
   - Implementación: Implementar navegación clara
   - Refactor: Optimizar textos de ayuda

### Día 41-43: Testing Completo TDD

#### Día 41: Tests E2E TDD

1. **Tests E2E exhaustivos con Playwright**
   - Test: Verificar flujos completos
   - Implementación: Implementar tests E2E
   - Refactor: Optimizar cobertura

2. **Cross-browser testing**
   - Test: Verificar compatibilidad entre navegadores
   - Implementación: Implementar tests específicos
   - Refactor: Optimizar soporte

#### Día 42: Performance Testing TDD

1. **Performance testing (load + stress + memory leaks)**
   - Test: Verificar rendimiento bajo carga
   - Implementación: Implementar tests de carga
   - Refactor: Optimizar puntos críticos

2. **Visual regression testing**
   - Test: Verificar consistencia visual
   - Implementación: Implementar tests de regresión
   - Refactor: Optimizar detección

#### Día 43: Security Testing TDD

1. **Security testing (OWASP + dependency scanning)**
   - Test: Verificar vulnerabilidades
   - Implementación: Implementar tests de seguridad
   - Refactor: Corregir vulnerabilidades

2. **Mobile testing completo**
   - Test: Verificar experiencia móvil
   - Implementación: Implementar tests específicos
   - Refactor: Optimizar responsive design

### Día 44-45: Production Ready TDD

#### Día 44: CI/CD y Docker TDD

1. **CI/CD pipeline completo con GitHub Actions**
   - Test: Verificar pipeline completo
   - Implementación: Implementar workflow
   - Refactor: Optimizar velocidad

2. **Docker optimization y security scanning**
   - Test: Verificar imágenes Docker
   - Implementación: Implementar optimizaciones
   - Refactor: Corregir vulnerabilidades

#### Día 45: Deployment y Documentación TDD

1. **Multi-environment setup (dev/staging/prod)**
   - Test: Verificar configuración de entornos
   - Implementación: Implementar configuraciones
   - Refactor: Optimizar variables de entorno

2. **Monitoring y alerting setup**
   - Test: Verificar sistema de monitoreo
   - Implementación: Implementar alertas
   - Refactor: Optimizar umbrales

3. **Documentation completa (user + admin + developer)**
   - Test: Verificar claridad de documentación
   - Implementación: Implementar documentación
   - Refactor: Optimizar ejemplos

## Criterios de Aceptación TDD Fase 4

- [ ] Tests end-to-end completos
- [ ] Tests de performance
- [ ] Tests de carga
- [ ] Tests de seguridad
- [ ] Sincronización bidireccional funciona correctamente
- [ ] Sistema de backup se ejecuta automáticamente
- [ ] Resolución de conflictos funciona
- [ ] Accesibilidad WCAG 2.2 AA validada
- [ ] CI/CD pipeline funciona sin errores
- [ ] Production deployment exitoso
- [ ] Monitoring y alerting configurados

## Templates TDD Estándar

### Template para Tests de Sincronización

```python
"""
Test file for sync_service.py

CRITICAL OBJECTIVES:
- Verify bidirectional synchronization with Google Classroom
- Test conflict detection and resolution

DEPENDENCIES:
- AsyncMock for Google API
- Mock data for synchronization
"""

import pytest
from unittest.mock import AsyncMock, patch
import datetime

from src.app.services.sync_service import SyncService
from src.app.core.config import settings

# BEGINNING: Critical tests for core functionality
@pytest.fixture
def mock_local_courses():
    """Mock local courses data"""
    return [
        {
            "id": "course1",
            "name": "Matemáticas 101",
            "section": "Período 2",
            "last_sync": datetime.datetime.now().isoformat(),
            "sync_status": "synced"
        },
        {
            "id": "course2",
            "name": "Ciencias 101",
            "section": "Período 1",
            "last_sync": datetime.datetime.now().isoformat(),
            "sync_status": "synced"
        }
    ]

@pytest.fixture
def mock_google_courses():
    """Mock Google Classroom courses data"""
    return {
        "courses": [
            {
                "id": "course1",
                "name": "Matemáticas 101 (Actualizado)",
                "section": "Período 2",
                "updateTime": datetime.datetime.now().isoformat()
            },
            {
                "id": "course3",
                "name": "Historia 101",
                "section": "Período 3",
                "updateTime": datetime.datetime.now().isoformat()
            }
        ]
    }

@pytest.mark.asyncio(timeout=3.0)
async def test_detect_changes(mock_local_courses, mock_google_courses):
    # Arrange
    sync_service = SyncService()
    
    with patch('src.app.services.google_classroom_service.GoogleClassroomService.get_courses') as mock_get_google, \
         patch('src.app.services.database_service.DatabaseService.get_courses') as mock_get_local:
        
        mock_get_google.return_value = mock_google_courses["courses"]
        mock_get_local.return_value = mock_local_courses
        
        # Act
        changes = await sync_service.detect_changes()
        
        # Assert
        assert "updated" in changes
        assert "new" in changes
        assert "deleted" in changes
        assert len(changes["updated"]) == 1
        assert changes["updated"][0]["id"] == "course1"
        assert len(changes["new"]) == 1
        assert changes["new"][0]["id"] == "course3"
        assert len(changes["deleted"]) == 1
        assert changes["deleted"][0]["id"] == "course2"

# MIDDLE: Detailed implementation tests
@pytest.mark.asyncio(timeout=3.0)
async def test_sync_to_google():
    # Arrange
    sync_service = SyncService()
    course_to_sync = {
        "id": "local_course",
        "name": "Local Course",
        "section": "Local Section"
    }
    
    with patch('src.app.services.google_classroom_service.GoogleClassroomService.create_course') as mock_create_course:
        mock_create_course.return_value = {
            "id": "google_course_id",
            "name": "Local Course",
            "section": "Local Section"
        }
        
        # Act
        result = await sync_service.sync_to_google(course_to_sync)
        
        # Assert
        assert result["id"] == "google_course_id"
        mock_create_course.assert_called_once()

@pytest.mark.asyncio(timeout=3.0)
async def test_sync_from_google():
    # Arrange
    sync_service = SyncService()
    course_to_sync = {
        "id": "google_course",
        "name": "Google Course",
        "section": "Google Section"
    }
    
    with patch('src.app.services.database_service.DatabaseService.create_course') as mock_create_course:
        mock_create_course.return_value = {
            "id": "google_course",
            "name": "Google Course",
            "section": "Google Section",
            "sync_status": "synced"
        }
        
        # Act
        result = await sync_service.sync_from_google(course_to_sync)
        
        # Assert
        assert result["sync_status"] == "synced"
        mock_create_course.assert_called_once()

# END: Verification and next steps
@pytest.mark.asyncio(timeout=3.0)
async def test_conflict_resolution():
    # Arrange
    sync_service = SyncService()
    conflict = {
        "entity_type": "course",
        "entity_id": "conflict_course",
        "local_data": {
            "name": "Local Name",
            "section": "Local Section",
            "last_sync": (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat()
        },
        "google_data": {
            "name": "Google Name",
            "section": "Google Section",
            "updateTime": datetime.datetime.now().isoformat()
        }
    }
    
    # Act
    resolution = await sync_service.resolve_conflict(conflict)
    
    # Assert
    assert resolution["resolution"] == "google_wins"
    assert resolution["entity_id"] == "conflict_course"
    assert "sync_actions" in resolution
```

### Template para Tests de Accesibilidad

```javascript
// AccessibilityTests.test.tsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { axe, toHaveNoViolations } from 'jest-axe';
import { Dashboard } from '../components/dashboard/Dashboard';

// Add custom matcher
expect.extend(toHaveNoViolations);

describe('Accessibility Tests', () => {
  // BEGINNING: Critical tests for core functionality
  test('dashboard should have no accessibility violations', async () => {
    // Arrange
    const mockData = {
      summary: {
        total_students: 120,
        active_courses: 5,
        assignments_pending: 25,
        average_grade: 85.5
      },
      charts: {
        performance: [
          { name: 'Matemáticas', value: 82 },
          { name: 'Ciencias', value: 88 },
          { name: 'Historia', value: 75 },
          { name: 'Literatura', value: 90 }
        ]
      }
    };
    
    // Act
    const { container } = render(<Dashboard data={mockData} />);
    
    // Assert
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
  
  test('keyboard navigation works correctly', () => {
    // Arrange
    const mockData = {
      summary: {
        total_students: 120,
        active_courses: 5,
        assignments_pending: 25,
        average_grade: 85.5
      },
      charts: {
        performance: [
          { name: 'Matemáticas', value: 82 },
          { name: 'Ciencias', value: 88 },
          { name: 'Historia', value: 75 },
          { name: 'Literatura', value: 90 }
        ]
      }
    };
    
    // Act
    render(<Dashboard data={mockData} />);
    
    // Tab to first interactive element
    const firstElement = screen.getByText('Ver detalles');
    firstElement.focus();
    
    // Assert
    expect(document.activeElement).toBe(firstElement);
    
    // Tab to next element
    fireEvent.keyDown(document.activeElement, { key: 'Tab' });
    
    // Assert next element is focused
    const nextElement = screen.getByText('Exportar datos');
    expect(document.activeElement).toBe(nextElement);
  });
  
  // MIDDLE: Detailed implementation tests
  test('screen reader text is present for charts', () => {
    // Arrange
    const mockData = {
      summary: {
        total_students: 120,
        active_courses: 5,
        assignments_pending: 25,
        average_grade: 85.5
      },
      charts: {
        performance: [
          { name: 'Matemáticas', value: 82 },
          { name: 'Ciencias', value: 88 },
          { name: 'Historia', value: 75 },
          { name: 'Literatura', value: 90 }
        ]
      }
    };
    
    // Act
    render(<Dashboard data={mockData} />);
    
    // Assert
    const srText = screen.getByText(/El gráfico muestra el rendimiento por materia/i);
    expect(srText).toBeInTheDocument();
    expect(srText).toHaveAttribute('aria-hidden', 'false');
  });
  
  test('high contrast mode works correctly', () => {
    // Arrange
    const mockData = {
      summary: {
        total_students: 120,
        active_courses: 5,
        assignments_pending: 25,
        average_grade: 85.5
      },
      charts: {
        performance: []
      }
    };
    
    // Act
    render(<Dashboard data={mockData} />);
    const contrastToggle = screen.getByLabelText('Activar modo de alto contraste');
    fireEvent.click(contrastToggle);
    
    // Assert
    const dashboard = screen.getByTestId('dashboard');
    expect(dashboard).toHaveClass('high-contrast');
  });
  
  // END: Verification and next steps
  test('ARIA landmarks are correctly implemented', () => {
    // Arrange
    const mockData = {
      summary: {
        total_students: 120,
        active_courses: 5,
        assignments_pending: 25,
        average_grade: 85.5
      },
      charts: {
        performance: []
      }
    };
    
    // Act
    render(<Dashboard data={mockData} />);
    
    // Assert
    expect(screen.getByRole('main')).toBeInTheDocument();
    expect(screen.getByRole('navigation')).toBeInTheDocument();
    expect(screen.getByRole('complementary')).toBeInTheDocument();
  });
});
```

### Template para Tests E2E

```javascript
// e2e/dashboard.spec.ts
import { test, expect } from '@playwright/test';

// BEGINNING: Critical tests for core functionality
test('user can view dashboard', async ({ page }) => {
  // Navigate to dashboard
  await page.goto('http://localhost:3000/dashboard');
  
  // Wait for dashboard to load
  await page.waitForSelector('[data-testid="dashboard-loaded"]');
  
  // Check dashboard title
  const title = await page.textContent('h1');
  expect(title).toContain('Dashboard');
  
  // Check summary cards are present
  const summaryCards = await page.$$('[data-testid="summary-card"]');
  expect(summaryCards.length).toBeGreaterThan(0);
});

test('user can switch between dashboard views', async ({ page }) => {
  // Navigate to dashboard
  await page.goto('http://localhost:3000/dashboard');
  
  // Wait for dashboard to load
  await page.waitForSelector('[data-testid="dashboard-loaded"]');
  
  // Click on teacher view
  await page.click('[data-testid="view-selector-teacher"]');
  
  // Check teacher view is active
  const activeView = await page.getAttribute('[data-testid="view-selector-teacher"]', 'aria-selected');
  expect(activeView).toBe('true');
  
  // Check teacher-specific content is visible
  const teacherContent = await page.isVisible('[data-testid="teacher-assignments"]');
  expect(teacherContent).toBe(true);
});

// MIDDLE: Detailed implementation tests
test('dashboard charts load correctly', async ({ page }) => {
  // Navigate to dashboard
  await page.goto('http://localhost:3000/dashboard');
  
  // Wait for dashboard to load
  await page.waitForSelector('[data-testid="dashboard-loaded"]');
  
  // Wait for charts to render
  await page.waitForSelector('[data-testid="performance-chart"] svg');
  
  // Check chart elements
  const chartSvg = await page.$('[data-testid="performance-chart"] svg');
  expect(chartSvg).not.toBeNull();
  
  // Check chart has data points
  const dataPoints = await page.$$('[data-testid="performance-chart"] .apexcharts-series path');
  expect(dataPoints.length).toBeGreaterThan(0);
});

test('user can filter dashboard data', async ({ page }) => {
  // Navigate to dashboard
  await page.goto('http://localhost:3000/dashboard');
  
  // Wait for dashboard to load
  await page.waitForSelector('[data-testid="dashboard-loaded"]');
  
  // Get initial count of items
  const initialCount = await page.$$eval('[data-testid="data-row"]', rows => rows.length);
  
  // Apply filter
  await page.fill('[data-testid="filter-input"]', 'Matemáticas');
  await page.click('[data-testid="apply-filter"]');
  
  // Wait for filtered results
  await page.waitForResponse(response => 
    response.url().includes('/api/dashboard/filter') && 
    response.status() === 200
  );
  
  // Get filtered count
  const filteredCount = await page.$$eval('[data-testid="data-row"]', rows => rows.length);
  
  // Filtered count should be less than initial count
  expect(filteredCount).toBeLessThan(initialCount);
});

// END: Verification and next steps
test('dashboard is accessible', async ({ page }) => {
  // Navigate to dashboard
  await page.goto('http://localhost:3000/dashboard');
  
  // Wait for dashboard to load
  await page.waitForSelector('[data-testid="dashboard-loaded"]');
  
  // Run accessibility scan
  const accessibilityScanResults = await page.evaluate(() => {
    // Note: This requires axe-core to be available in the page
    return new Promise(resolve => {
      // @ts-ignore
      axe.run(document.body, {}, (err, results) => {
        if (err) throw err;
        resolve(results);
      });
    });
  });
  
  // Check for violations
  expect(accessibilityScanResults.violations.length).toBe(0);
});
```

## Entregables TDD Fase 4

1. **Código Backend**
   - Sincronización bidireccional
   - Sistema de backup
   - Resolución de conflictos
   - Webhooks para eventos
   - Admin panel con diagnósticos

2. **Código Frontend**
   - Accesibilidad WCAG 2.2 AA
   - Soporte para screen readers
   - Modos de alto contraste
   - Navegación por teclado
   - Accesibilidad cognitiva

3. **Tests**
   - Tests E2E exhaustivos
   - Tests de performance
   - Tests de seguridad
   - Tests de accesibilidad
   - Tests de compatibilidad

4. **Documentación**
   - Documentación de usuario
   - Documentación de administrador
   - Documentación de desarrollador
   - Documentación de API

## Próximos Pasos

1. Validar cumplimiento de criterios de aceptación
2. Realizar deployment a producción
3. Configurar monitoreo y alertas
4. Entrenar a usuarios y administradores
5. Planificar mantenimiento y mejoras futuras
