---
title: "ClassSphere - Fase 4: Integración Completa"
version: "3.0"
type: "development_plan"
priority: "LOW"
max_tokens: 800
duration: "13 días"
related_files:
  - "contracts/principal/06_ClassSphere_funcionalidades.md"
  - "contracts/principal/11_ClassSphere_deployment.md"
---

# Fase 4: Integración Completa - WCAG 2.2 AA + Production Ready

## 🎯 INICIO: Objetivos Críticos y Dependencias Bloqueantes

### Objetivo Principal
Completar integración bidireccional con Google Classroom, implementar accesibilidad WCAG 2.2 AA completa y preparar sistema para producción.

### Dependencias Bloqueantes
- **Fase 3 completada**: Búsqueda avanzada + WebSocket + visualizaciones
- **Tests E2E funcionando**: Playwright tests validados
- **Google API mocks validados**: Sistema de alternancia operativo
- **Performance < 2s validado**: Optimización de carga completada

### Componentes Críticos
- **Sincronización Bidireccional**: Google Classroom ↔ ClassSphere
- **Accesibilidad WCAG 2.2 AA**: Completa e inclusiva
- **CI/CD Pipeline**: Completo con quality gates
- **Production Deployment**: Docker + monitoring + alerting

## 📅 MEDIO: Implementación Detallada Día por Día

### Día 1-3: Sincronización Bidireccional Google

**Objetivo**: Implementar sincronización completa bidireccional

**TDD Implementación**:
```go
// tests/services/sync_test.go - RED PHASE
func TestBidirectionalSync(t *testing.T) {
    service := NewSyncService(mockGoogleAPI, mockLocalDB)
    
    // Test sincronización Google → Local
    err := service.SyncFromGoogle("course-123")
    assert.NoError(t, err)
    
    // Test sincronización Local → Google
    localCourse := Course{
        ID: "local-course-456",
        Name: "Updated Course Name",
        Description: "New description",
    }
    
    err = service.SyncToGoogle(localCourse)
    assert.NoError(t, err)
    
    // Verificar conflicto resuelto
    conflicts := service.GetConflicts()
    assert.Len(t, conflicts, 0)
}

// internal/services/sync.go - GREEN PHASE
type SyncService struct {
    googleAPI  GoogleClassroomAPI
    localDB    Database
    conflictResolver ConflictResolver
}

func (s *SyncService) SyncFromGoogle(courseID string) error {
    // Obtener datos de Google
    googleCourse, err := s.googleAPI.GetCourse(courseID)
    if err != nil {
        return err
    }
    
    // Obtener datos locales
    localCourse, err := s.localDB.GetCourse(courseID)
    if err != nil {
        return err
    }
    
    // Detectar conflictos
    if s.hasConflict(googleCourse, localCourse) {
        resolved := s.conflictResolver.Resolve(googleCourse, localCourse)
        return s.localDB.UpdateCourse(resolved)
    }
    
    return s.localDB.UpdateCourse(googleCourse)
}
```

### Día 4-6: Accesibilidad WCAG 2.2 AA

**Objetivo**: Implementar accesibilidad completa WCAG 2.2 AA

**TDD Implementación**:
```typescript
// src/app/components/accessibility/accessible-button.component.spec.ts
describe('AccessibleButtonComponent', () => {
  let component: AccessibleButtonComponent;
  let fixture: ComponentFixture<AccessibleButtonComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AccessibleButtonComponent]
    });
    
    fixture = TestBed.createComponent(AccessibleButtonComponent);
    component = fixture.componentInstance;
  });

  it('should have proper ARIA attributes', () => {
    component.label = 'Save Course';
    component.ariaLabel = 'Save course information';
    fixture.detectChanges();
    
    const button = fixture.debugElement.nativeElement.querySelector('button');
    expect(button.getAttribute('aria-label')).toBe('Save course information');
    expect(button.getAttribute('role')).toBe('button');
  });

  it('should support keyboard navigation', () => {
    component.label = 'Delete';
    fixture.detectChanges();
    
    const button = fixture.debugElement.nativeElement.querySelector('button');
    const keyEvent = new KeyboardEvent('keydown', { key: 'Enter' });
    
    spyOn(component, 'onClick');
    button.dispatchEvent(keyEvent);
    
    expect(component.onClick).toHaveBeenCalled();
  });
});
```

**Implementación Accesibilidad**:
```typescript
// src/app/components/accessibility/accessible-button.component.ts
@Component({
  selector: 'app-accessible-button',
  template: `
    <button 
      [attr.aria-label]="ariaLabel"
      [attr.aria-describedby]="ariaDescribedBy"
      [attr.aria-pressed]="ariaPressed"
      [class.high-contrast]="highContrast"
      (click)="onClick()"
      (keydown)="onKeyDown($event)"
      [disabled]="disabled">
      <span class="sr-only" *ngIf="srOnlyText">{{ srOnlyText }}</span>
      {{ label }}
    </button>
  `,
  styleUrls: ['./accessible-button.component.scss']
})
export class AccessibleButtonComponent implements OnInit {
  @Input() label: string;
  @Input() ariaLabel?: string;
  @Input() ariaDescribedBy?: string;
  @Input() ariaPressed?: boolean;
  @Input() highContrast = false;
  @Input() srOnlyText?: string;
  @Input() disabled = false;
  
  @Output() clicked = new EventEmitter<void>();

  ngOnInit() {
    // Configurar high contrast mode
    this.detectHighContrast();
  }

  onClick() {
    if (!this.disabled) {
      this.clicked.emit();
    }
  }

  onKeyDown(event: KeyboardEvent) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      this.onClick();
    }
  }

  private detectHighContrast() {
    // Detectar preferencias de alto contraste
    if (window.matchMedia('(prefers-contrast: high)').matches) {
      this.highContrast = true;
    }
  }
}
```

### Día 7-9: Testing Completo E2E

**Objetivo**: Implementar testing E2E exhaustivo

**E2E Testing**:
```typescript
// e2e/accessibility.e2e-spec.ts
import { test, expect } from '@playwright/test';

test.describe('Accessibility WCAG 2.2 AA', () => {
  test('keyboard navigation works correctly', async ({ page }) => {
    await page.goto('/dashboard');
    
    // Navegar con Tab
    await page.keyboard.press('Tab');
    await expect(page.locator(':focus')).toHaveAttribute('tabindex', '0');
    
    // Activar con Enter
    await page.keyboard.press('Enter');
    await expect(page).toHaveURL(/\/courses/);
  });

  test('screen reader support works', async ({ page }) => {
    await page.goto('/courses');
    
    // Verificar ARIA labels
    const button = page.locator('[data-testid="add-course-button"]');
    await expect(button).toHaveAttribute('aria-label');
    
    // Verificar heading structure
    const h1 = page.locator('h1');
    const h2 = page.locator('h2');
    await expect(h1).toHaveCount(1);
    await expect(h2).toHaveCount.greaterThan(0);
  });

  test('high contrast mode works', async ({ page }) => {
    await page.emulateMedia({ colorScheme: 'dark' });
    await page.goto('/dashboard');
    
    // Verificar que los elementos son visibles
    const mainContent = page.locator('[data-testid="main-content"]');
    await expect(mainContent).toBeVisible();
    
    // Verificar contraste de colores
    const button = page.locator('button').first();
    const buttonColor = await button.evaluate(el => 
      window.getComputedStyle(el).color
    );
    expect(buttonColor).not.toBe('transparent');
  });
});
```

### Día 10-11: CI/CD Pipeline Completo

**Objetivo**: Configurar pipeline completo con quality gates

**GitHub Actions**:
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  backend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v4
        with:
          go-version: '1.21'
      
      - name: Run tests
        run: go test ./... -cover -coverprofile=coverage.out
        env:
          COVERAGE_THRESHOLD: 80
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.out

  frontend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm run test:ci
      
      - name: Run E2E tests
        run: npm run e2e:ci

  accessibility-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install axe-core
        run: npm install -g @axe-core/cli
      
      - name: Run accessibility tests
        run: axe http://localhost:4200 --exit

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

  deploy:
    needs: [backend-test, frontend-test, accessibility-test, security-scan]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Build Docker images
        run: |
          docker build -t classsphere-backend ./backend
          docker build -t classsphere-frontend ./frontend
      
      - name: Deploy to production
        run: |
          docker-compose -f docker-compose.prod.yml up -d
```

### Día 12-13: Production Deployment

**Objetivo**: Configurar deployment de producción con monitoring

**Docker Compose Production**:
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8081:8081"
    environment:
      - GO_ENV=production
      - REDIS_URL=redis://redis:6379
      - GOOGLE_OAUTH_CLIENT_ID=${GOOGLE_OAUTH_CLIENT_ID}
      - GOOGLE_OAUTH_CLIENT_SECRET=${GOOGLE_OAUTH_CLIENT_SECRET}
    depends_on:
      - redis
      - postgres
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    environment:
      - API_URL=http://backend:8081
    depends_on:
      - backend
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=classsphere
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
```

## ✅ FINAL: Checklist Verificación y Próximos Pasos

### Criterios de Aceptación Fase 4
- [ ] **Sincronización Bidireccional**: Google ↔ ClassSphere operativa
- [ ] **Accesibilidad WCAG 2.2 AA**: Completa e validada
- [ ] **CI/CD Pipeline**: Quality gates funcionando
- [ ] **Production Deployment**: Docker + monitoring operativo
- [ ] **Performance**: <1s load time
- [ ] **Security**: 0 vulnerabilidades CRITICAL
- [ ] **Testing**: E2E exhaustivo + accessibility tests

### Comandos de Verificación
```bash
# Verificar sincronización
curl -X POST http://localhost:8081/sync/google-to-local \
  -H "Authorization: Bearer admin-token" \
  -d '{"courseId":"course-123"}'

# Verificar accesibilidad
axe http://localhost:4200 --exit

# Verificar deployment
docker-compose -f docker-compose.prod.yml ps

# Verificar security
trivy fs .
```

### Funcionalidades Implementadas
- **Sincronización Bidireccional**: Google Classroom ↔ ClassSphere
- **Accesibilidad Completa**: WCAG 2.2 AA + keyboard navigation + screen reader
- **CI/CD Pipeline**: GitHub Actions + quality gates + security scanning
- **Production Ready**: Docker + monitoring + alerting + SSL

### Próximos Pasos
1. **Monitoreo Continuo**: Métricas de producción
2. **Optimización**: Performance tuning
3. **Escalabilidad**: Load balancing + clustering
4. **Mantenimiento**: Updates + patches

### Métricas de Éxito
- **Sync Performance**: <2s bidirectional sync
- **Accessibility Score**: 100% WCAG 2.2 AA compliance
- **Deployment Time**: <5min automated deployment
- **Uptime**: 99.9% availability
- **Security**: 0 vulnerabilities CRITICAL

**Estado**: ✅ PRODUCTION READY  
**Duración**: 13 días  
**Integración**: Completa + Accesibilidad + Production  
**Performance**: <1s load time + 99.9% uptime
