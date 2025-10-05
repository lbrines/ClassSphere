---
title: "ClassSphere - Fase 4: Integración Completa TDD"
version: "1.0"
type: "documentation"
date: "2025-10-04"
author: "Sistema de Contratos LLM"
related_files:
  - "01_plam_index.md"
  - "04_plan_fase3_visualizacion.md"
---

[← Fase 3: Visualización](04_plan_fase3_visualizacion.md) | [Índice](01_plam_index.md)

# Fase 4: Integración Completa TDD

## Objetivos de la Fase

Esta fase completa la integración del sistema y lo prepara para producción siguiendo metodología TDD:

1. **Google Completo**: Sincronización bidireccional, backup y webhooks
2. **Accesibilidad WCAG 2.2 AA**: Cumplimiento de estándares de accesibilidad
3. **Testing Exhaustivo**: E2E, performance, seguridad y carga
4. **Production Ready**: CI/CD, Docker, monitoreo y documentación

## Duración Estimada: 10-12 días

### Distribución de Tareas

**Días 35-37: Google Completo**
- Tests para sincronización bidireccional
- Implementación sync + backup + webhooks
- Resolución de conflictos
- Admin panel Google

**Días 38-40: Accesibilidad WCAG 2.2 AA**
- Tests de accesibilidad completos
- Implementación keyboard + screen reader
- High contrast + motor accessibility
- Validación automática + manual

**Días 41-43: Testing Completo**
- Tests E2E exhaustivos
- Performance + load testing
- Visual regression testing
- Security penetration testing

**Días 44-45: Production Ready**
- CI/CD pipeline completo
- Docker optimization + security
- Monitoring + alerting
- Documentation + runbooks

## Estructura de Tests Backend

### Requisitos Técnicos Obligatorios

1. **Timeouts en Tests de Sincronización**
   ```python
   # test_google_sync_service.py
   @pytest.mark.asyncio
   async def test_full_sync_with_timeout():
       """Test sincronización completa con timeout"""
       sync_service = GoogleSyncService()
       
       result = await asyncio.wait_for(
           sync_service.full_sync(),
           timeout=10.0  # Timeout más largo para sincronización completa
       )
       
       assert result["success"] is True
       assert "stats" in result
       assert result["stats"]["courses_synced"] > 0
       assert result["stats"]["students_synced"] > 0
   ```

2. **Tests de Resolución de Conflictos**
   ```python
   # test_conflict_resolution.py
   @pytest.mark.asyncio
   async def test_resolve_course_conflict():
       """Test resolución de conflictos en cursos"""
       conflict_service = ConflictResolutionService()
       
       # Crear conflicto simulado
       conflict = {
           "entity_type": "course",
           "entity_id": "course-001",
           "local_data": {"name": "Matemáticas Avanzadas", "updated_at": "2025-01-01T10:00:00Z"},
           "remote_data": {"name": "Matemáticas Avanzadas (Actualizado)", "updated_at": "2025-01-02T10:00:00Z"}
       }
       
       resolution = await asyncio.wait_for(
           conflict_service.resolve_conflict(conflict),
           timeout=3.0  # Timeout obligatorio
       )
       
       assert resolution["resolved"] is True
       assert resolution["resolution_type"] == "remote_wins"
       assert resolution["entity_id"] == "course-001"
   ```

3. **Tests de Webhooks**
   ```python
   # test_webhook_service.py
   @pytest.mark.asyncio
   async def test_process_course_update_webhook():
       """Test procesamiento de webhook de actualización de curso"""
       webhook_service = WebhookService()
       
       # Simular payload de webhook
       payload = {
           "event_type": "course.update",
           "course_id": "course-001",
           "update_time": "2025-01-15T10:00:00Z",
           "changes": ["name", "section"]
       }
       
       result = await asyncio.wait_for(
           webhook_service.process_webhook(payload),
           timeout=3.0  # Timeout obligatorio
       )
       
       assert result["success"] is True
       assert result["processed_changes"] == ["name", "section"]
       assert "sync_initiated" in result
   ```

### Estructura de Directorios de Tests

```
backend/
└── tests/
    ├── unit/
    │   ├── services/
    │   │   ├── test_google_sync_service.py
    │   │   ├── test_conflict_resolution.py
    │   │   └── test_backup_service.py
    │   └── api/
    │       ├── test_webhook_endpoints.py
    │       └── test_admin_endpoints.py
    ├── integration/
    │   ├── test_sync_flow_integration.py
    │   └── test_backup_restore_integration.py
    ├── performance/
    │   ├── test_sync_performance.py
    │   └── test_api_load.py
    └── security/
        ├── test_api_security.py
        └── test_auth_security.py
```

### Tests de Sincronización

```python
# test_google_sync_service.py
@pytest.mark.asyncio
async def test_incremental_sync():
    """Test sincronización incremental"""
    sync_service = GoogleSyncService()
    
    # Establecer última sincronización
    sync_service.set_last_sync_time("2025-01-01T00:00:00Z")
    
    result = await asyncio.wait_for(
        sync_service.incremental_sync(),
        timeout=5.0  # Timeout obligatorio
    )
    
    assert result["success"] is True
    assert "stats" in result
    assert "last_sync_time" in result
    assert result["sync_type"] == "incremental"

@pytest.mark.asyncio
async def test_sync_specific_course():
    """Test sincronización de curso específico"""
    sync_service = GoogleSyncService()
    course_id = "course-001"
    
    result = await asyncio.wait_for(
        sync_service.sync_course(course_id),
        timeout=3.0  # Timeout obligatorio
    )
    
    assert result["success"] is True
    assert result["course_id"] == course_id
    assert "students_synced" in result
    assert "assignments_synced" in result
```

### Tests de Backup y Restore

```python
# test_backup_service.py
@pytest.mark.asyncio
async def test_create_full_backup():
    """Test creación de backup completo"""
    backup_service = BackupService()
    
    result = await asyncio.wait_for(
        backup_service.create_full_backup(),
        timeout=5.0  # Timeout obligatorio
    )
    
    assert result["success"] is True
    assert "backup_id" in result
    assert "timestamp" in result
    assert "size_bytes" in result
    assert result["entities"]["courses"] > 0
    assert result["entities"]["students"] > 0

@pytest.mark.asyncio
async def test_restore_from_backup():
    """Test restauración desde backup"""
    backup_service = BackupService()
    
    # Crear backup primero
    backup = await backup_service.create_full_backup()
    backup_id = backup["backup_id"]
    
    # Restaurar desde backup
    result = await asyncio.wait_for(
        backup_service.restore_from_backup(backup_id),
        timeout=8.0  # Timeout más largo para restauración
    )
    
    assert result["success"] is True
    assert result["backup_id"] == backup_id
    assert "restored_entities" in result
    assert result["restored_entities"]["courses"] > 0
```

## Estructura de Tests Frontend

### Requisitos Técnicos Obligatorios

1. **Tests de Accesibilidad**
   ```typescript
   // SyncPanel.test.tsx
   test('meets accessibility standards', async () => {
     const { container } = render(<SyncPanel />);
     const results = await axe(container);
     
     // No debería tener violaciones de accesibilidad
     expect(results.violations).toHaveLength(0);
   });
   ```

2. **Tests de Keyboard Navigation**
   ```typescript
   // AdminPanel.test.tsx
   test('supports keyboard navigation', async () => {
     const user = userEvent.setup();
     render(<AdminPanel />);
     
     // Focus en el primer elemento
     await user.tab();
     expect(screen.getByTestId('sync-button')).toHaveFocus();
     
     // Focus en el segundo elemento
     await user.tab();
     expect(screen.getByTestId('backup-button')).toHaveFocus();
     
     // Focus en el tercer elemento
     await user.tab();
     expect(screen.getByTestId('settings-button')).toHaveFocus();
   });
   ```

3. **Tests de Screen Reader**
   ```typescript
   // ConflictResolver.test.tsx
   test('provides appropriate ARIA attributes', () => {
     render(<ConflictResolver conflicts={mockConflicts} />);
     
     // Verificar ARIA labels
     expect(screen.getByRole('heading', { name: /conflicts/i })).toBeInTheDocument();
     expect(screen.getByRole('table')).toHaveAttribute('aria-label', 'Conflicts to resolve');
     
     // Verificar ARIA live regions
     expect(screen.getByRole('status')).toHaveAttribute('aria-live', 'polite');
   });
   ```

### Estructura de Directorios de Tests

```
frontend/
└── src/
    ├── components/
    │   ├── admin/
    │   │   ├── SyncPanel.tsx
    │   │   ├── SyncPanel.test.tsx
    │   │   ├── ConflictResolver.tsx
    │   │   └── ConflictResolver.test.tsx
    │   └── a11y/
    │       ├── SkipLink.tsx
    │       ├── SkipLink.test.tsx
    │       ├── FocusTrap.tsx
    │       └── FocusTrap.test.tsx
    ├── hooks/
    │   ├── useSync.ts
    │   └── useSync.test.ts
    └── test/
        ├── e2e/
        │   ├── sync.spec.ts
        │   └── accessibility.spec.ts
        └── axe-helper.ts
```

### Tests de Componentes de Admin

```typescript
// SyncPanel.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import userEvent from '@testing-library/user-event';
import SyncPanel from './SyncPanel';
import { axe } from 'jest-axe';

// Mock de useSync
vi.mock('../../hooks/useSync', () => ({
  useSync: () => ({
    sync: vi.fn().mockResolvedValue({ success: true }),
    isLoading: false,
    lastSync: '2025-01-15T10:00:00Z',
    error: null
  })
}));

describe('SyncPanel', () => {
  it('renders sync panel correctly', () => {
    render(<SyncPanel />);
    
    expect(screen.getByText(/synchronization/i)).toBeInTheDocument();
    expect(screen.getByText(/last sync:/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sync now/i })).toBeInTheDocument();
  });
  
  it('initiates sync on button click', async () => {
    const user = userEvent.setup();
    const { sync } = useSync();
    
    render(<SyncPanel />);
    
    // Click en botón de sincronización
    const syncButton = screen.getByRole('button', { name: /sync now/i });
    await user.click(syncButton);
    
    // Verificar que se llamó a la función de sincronización
    expect(sync).toHaveBeenCalled();
  });
  
  it('shows loading state during sync', async () => {
    // Override mock para estado de carga
    vi.mocked(useSync).mockReturnValue({
      sync: vi.fn().mockResolvedValue({ success: true }),
      isLoading: true,
      lastSync: '2025-01-15T10:00:00Z',
      error: null
    });
    
    render(<SyncPanel />);
    
    expect(screen.getByText(/synchronizing/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sync now/i })).toBeDisabled();
  });
  
  it('meets accessibility standards', async () => {
    const { container } = render(<SyncPanel />);
    const results = await axe(container);
    
    // No debería tener violaciones de accesibilidad
    expect(results.violations).toHaveLength(0);
  });
});
```

### Tests de Componentes de Accesibilidad

```typescript
// SkipLink.test.tsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import userEvent from '@testing-library/user-event';
import SkipLink from './SkipLink';

describe('SkipLink', () => {
  it('renders skip link correctly', () => {
    render(<SkipLink targetId="main-content" />);
    
    const skipLink = screen.getByText(/skip to main content/i);
    expect(skipLink).toBeInTheDocument();
    expect(skipLink).toHaveAttribute('href', '#main-content');
  });
  
  it('becomes visible on focus', async () => {
    const user = userEvent.setup();
    render(<SkipLink targetId="main-content" />);
    
    const skipLink = screen.getByText(/skip to main content/i);
    
    // Inicialmente no visible
    expect(skipLink).not.toBeVisible();
    
    // Focus en el enlace
    await user.tab();
    expect(skipLink).toHaveFocus();
    expect(skipLink).toBeVisible();
    
    // Pierde focus
    await user.tab();
    expect(skipLink).not.toHaveFocus();
    expect(skipLink).not.toBeVisible();
  });
  
  it('moves focus to target element when activated', async () => {
    const user = userEvent.setup();
    
    // Crear elemento target
    const mainContent = document.createElement('main');
    mainContent.id = 'main-content';
    mainContent.tabIndex = -1; // Para poder recibir focus
    document.body.appendChild(mainContent);
    
    render(<SkipLink targetId="main-content" />);
    
    // Focus y activar skip link
    await user.tab();
    await user.keyboard('{Enter}');
    
    // Verificar que el focus se movió al elemento target
    expect(document.activeElement).toBe(mainContent);
    
    // Cleanup
    document.body.removeChild(mainContent);
  });
});
```

## Tests E2E

### Tests E2E con Playwright

```typescript
// sync.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Google Sync Flow', () => {
  test('admin can perform full sync', async ({ page }) => {
    // Login como admin
    await page.goto('/login');
    await page.fill('input[name="email"]', 'admin@example.com');
    await page.fill('input[name="password"]', 'admin123');
    await page.click('button[type="submit"]');
    
    // Navegar a panel de administración
    await page.click('a[href="/admin"]');
    
    // Verificar que estamos en la página de admin
    await expect(page).toHaveURL('/admin');
    
    // Click en tab de sincronización
    await page.click('button:has-text("Synchronization")');
    
    // Iniciar sincronización completa
    await page.click('button:has-text("Full Sync")');
    
    // Verificar mensaje de confirmación
    await page.waitForSelector('text=Are you sure you want to perform a full sync?');
    await page.click('button:has-text("Confirm")');
    
    // Verificar que aparece indicador de progreso
    await page.waitForSelector('text=Synchronizing...');
    
    // Esperar a que termine la sincronización (con timeout)
    await page.waitForSelector('text=Sync completed successfully', { timeout: 30000 });
    
    // Verificar estadísticas de sincronización
    await expect(page.locator('text=Courses synced:')).toBeVisible();
    await expect(page.locator('text=Students synced:')).toBeVisible();
  });
  
  test('system handles sync conflicts', async ({ page }) => {
    // Login y navegación a admin
    await page.goto('/login');
    await page.fill('input[name="email"]', 'admin@example.com');
    await page.fill('input[name="password"]', 'admin123');
    await page.click('button[type="submit"]');
    await page.click('a[href="/admin"]');
    
    // Ir a sección de conflictos
    await page.click('button:has-text("Conflicts")');
    
    // Verificar que hay conflictos listados
    await expect(page.locator('.conflict-item')).toHaveCount(2);
    
    // Resolver primer conflicto (usar versión remota)
    await page.click('.conflict-item:first-child button:has-text("Use Remote")');
    
    // Verificar que el conflicto se resolvió
    await page.waitForSelector('text=Conflict resolved');
    
    // Verificar que queda un conflicto
    await expect(page.locator('.conflict-item')).toHaveCount(1);
  });
});
```

### Tests de Accesibilidad E2E

```typescript
// accessibility.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility Compliance', () => {
  test('main dashboard meets WCAG 2.2 AA standards', async ({ page }) => {
    // Login
    await page.goto('/login');
    await page.fill('input[name="email"]', 'teacher@example.com');
    await page.fill('input[name="password"]', 'teacher123');
    await page.click('button[type="submit"]');
    
    // Navegar al dashboard
    await page.waitForURL('/dashboard');
    
    // Ejecutar análisis de accesibilidad
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();
    
    // Verificar que no hay violaciones
    expect(accessibilityScanResults.violations).toEqual([]);
  });
  
  test('keyboard navigation works correctly', async ({ page }) => {
    // Login
    await page.goto('/login');
    await page.fill('input[name="email"]', 'student@example.com');
    await page.fill('input[name="password"]', 'student123');
    await page.click('button[type="submit"]');
    
    // Navegar al dashboard
    await page.waitForURL('/dashboard');
    
    // Presionar Tab para navegar por los elementos
    await page.keyboard.press('Tab');
    
    // Verificar que el primer elemento navegable tiene focus
    const focusedElement = await page.evaluate(() => {
      const el = document.activeElement;
      return el ? el.tagName : null;
    });
    
    expect(focusedElement).not.toBeNull();
    
    // Navegar por todos los elementos interactivos
    let tabCount = 0;
    const maxTabs = 20; // Límite para evitar loop infinito
    
    while (tabCount < maxTabs) {
      await page.keyboard.press('Tab');
      tabCount++;
      
      // Verificar que siempre hay un elemento con focus
      const hasFocus = await page.evaluate(() => {
        return document.activeElement !== document.body;
      });
      
      expect(hasFocus).toBe(true);
    }
  });
});
```

## Comandos de Testing

### Backend Tests

```bash
# Tests de sincronización
pytest tests/unit/services/test_google_sync_service.py --cov=src.app.services.google_sync_service

# Tests de backup/restore
pytest tests/unit/services/test_backup_service.py --cov=src.app.services.backup_service

# Tests de performance
pytest tests/performance/ -v

# Tests de seguridad
pytest tests/security/ -v

# Tests completos con cobertura
pytest tests/ --cov=src --cov-report=term-missing
```

### Frontend Tests

```bash
# Tests de componentes de admin
npm run test -- --testPathPattern=src/components/admin

# Tests de componentes de accesibilidad
npm run test -- --testPathPattern=src/components/a11y

# Tests E2E
npm run test:e2e

# Tests de accesibilidad
npm run test:a11y

# Tests completos con cobertura
npm run test -- --coverage
```

## Criterios de Aceptación

### Google Completo

- [ ] Sincronización bidireccional con Google Classroom
- [ ] Sistema de backup y restore
- [ ] Webhooks para actualizaciones en tiempo real
- [ ] Resolución de conflictos
- [ ] Panel de administración para Google
- [ ] Tests con cobertura ≥90% en módulos críticos

### Accesibilidad WCAG 2.2 AA

- [ ] Navegación por teclado completa
- [ ] Compatibilidad con lectores de pantalla
- [ ] Contraste adecuado y modo alto contraste
- [ ] Textos alternativos para imágenes
- [ ] Estructura semántica correcta
- [ ] Tests de accesibilidad automatizados

### Testing Completo

- [ ] Tests E2E para todos los flujos críticos
- [ ] Tests de performance y carga
- [ ] Tests de seguridad
- [ ] Visual regression testing
- [ ] Cobertura global ≥80% líneas, ≥65% ramas
- [ ] Cobertura módulos críticos ≥90% líneas, ≥80% ramas

### Production Ready

- [ ] CI/CD pipeline completo
- [ ] Docker optimizado y seguro
- [ ] Sistema de monitoreo y alertas
- [ ] Documentación completa
- [ ] Runbooks para operaciones
- [ ] Scripts de deployment automatizados

## Referencias

Para más detalles sobre la implementación TDD para producción, consultar:
- [Estrategia de Testing Unificada](principal/09_ClassSphere_testing.md)
- [Plan de Implementación Unificado](principal/10_ClassSphere_plan_implementacion.md)
- [Configuración de Deployment Unificada](principal/11_ClassSphere_deployment.md)
- [TDD Best Practices](extra/TDD_BEST_PRACTICES.md)

---

[← Fase 3: Visualización](04_plan_fase3_visualizacion.md) | [Índice](01_plam_index.md)
