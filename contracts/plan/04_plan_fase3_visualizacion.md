---
title: "ClassSphere - Fase 3: Visualización Avanzada"
version: "3.0"
type: "development_plan"
priority: "MEDIUM"
max_tokens: 1000
duration: "10 días"
related_files:
  - "contracts/principal/06_ClassSphere_funcionalidades.md"
  - "contracts/principal/05_ClassSphere_arquitectura.md"
---

# Fase 3: Visualización Avanzada - Búsqueda y WebSocket

## 🎯 INICIO: Objetivos Críticos y Dependencias Bloqueantes

### Objetivo Principal
Implementar búsqueda avanzada multi-entidad, notificaciones WebSocket real-time y visualizaciones interactivas con D3.js.

### Dependencias Bloqueantes
- **Fase 2 completada**: Google Classroom API + Dashboards funcionando
- **WebSocket support**: Configurado en backend Go
- **D3.js integrado**: Librería de visualización instalada
- **Dashboards base**: Componentes Angular funcionando
- **Sistema de roles**: Autenticación y autorización operativa

### Componentes Críticos
- **Búsqueda Avanzada**: Multi-entidad con filtros contextuales
- **Notificaciones WebSocket**: Real-time updates
- **Gráficos Interactivos**: D3.js + exportación
- **Sistema de Búsqueda**: Guardado y recuperación

## 📅 MEDIO: Implementación Detallada Día por Día

### Día 1-2: Sistema de Búsqueda Avanzada

**Objetivo**: Implementar búsqueda multi-entidad con filtros

**TDD Implementación**:
```go
// tests/services/search_test.go - RED PHASE
func TestAdvancedSearch(t *testing.T) {
    service := NewSearchService(mockDataStore)
    
    // Test que falla inicialmente
    results, err := service.Search("mathematics", []string{"courses", "students"}, SearchFilters{
        DateRange: "2024-01-01:2024-12-31",
        Role: "teacher",
    })
    
    assert.NoError(t, err)
    assert.Len(t, results.Courses, 3)
    assert.Len(t, results.Students, 15)
}

// internal/services/search.go - GREEN PHASE
type SearchService struct {
    dataStore DataStore
    indexer   SearchIndexer
}

func (s *SearchService) Search(query string, entities []string, filters SearchFilters) (*SearchResults, error) {
    results := &SearchResults{}
    
    for _, entity := range entities {
        switch entity {
        case "courses":
            courses, err := s.searchCourses(query, filters)
            if err != nil {
                return nil, err
            }
            results.Courses = courses
        case "students":
            students, err := s.searchStudents(query, filters)
            if err != nil {
                return nil, err
            }
            results.Students = students
        }
    }
    
    return results, nil
}
```

### Día 3-4: Notificaciones WebSocket

**Objetivo**: Implementar sistema de notificaciones real-time

**TDD Implementación**:
```go
// tests/websocket/notification_test.go
func TestWebSocketNotifications(t *testing.T) {
    server := httptest.NewServer(http.HandlerFunc(websocketHandler))
    defer server.Close()
    
    // Test conexión WebSocket
    wsURL := "ws" + server.URL[4:] + "/ws"
    conn, _, err := websocket.DefaultDialer.Dial(wsURL, nil)
    assert.NoError(t, err)
    defer conn.Close()
    
    // Test envío de notificación
    notification := Notification{
        Type: "course_update",
        Message: "New assignment posted",
        UserID: "teacher@school.edu",
    }
    
    err = conn.WriteJSON(notification)
    assert.NoError(t, err)
    
    // Test recepción
    var received Notification
    err = conn.ReadJSON(&received)
    assert.NoError(t, err)
    assert.Equal(t, "course_update", received.Type)
}
```

**Implementación WebSocket**:
```go
// internal/websocket/hub.go
type Hub struct {
    clients    map[*Client]bool
    broadcast  chan []byte
    register   chan *Client
    unregister chan *Client
}

func (h *Hub) Run() {
    for {
        select {
        case client := <-h.register:
            h.clients[client] = true
            
        case client := <-h.unregister:
            if _, ok := h.clients[client]; ok {
                delete(h.clients, client)
                close(client.send)
            }
            
        case message := <-h.broadcast:
            for client := range h.clients {
                select {
                case client.send <- message:
                default:
                    close(client.send)
                    delete(h.clients, client)
                }
            }
        }
    }
}
```

### Día 5-6: Gráficos Interactivos D3.js

**Objetivo**: Implementar visualizaciones interactivas con D3.js

**TDD Implementación**:
```typescript
// src/app/components/charts/line-chart.component.spec.ts
describe('LineChartComponent', () => {
  let component: LineChartComponent;
  let fixture: ComponentFixture<LineChartComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [LineChartComponent]
    });
    
    fixture = TestBed.createComponent(LineChartComponent);
    component = fixture.componentInstance;
  });

  it('should create line chart with data', () => {
    const mockData = [
      { date: '2024-01-01', value: 100 },
      { date: '2024-01-02', value: 120 },
      { date: '2024-01-03', value: 90 }
    ];
    
    component.data = mockData;
    component.ngOnInit();
    
    expect(component.chart).toBeDefined();
    expect(component.chart.selectAll('.line').size()).toBe(1);
  });

  it('should export chart as PNG', () => {
    component.data = mockData;
    component.ngOnInit();
    
    const exportSpy = spyOn(component, 'exportAsPNG');
    component.exportAsPNG();
    
    expect(exportSpy).toHaveBeenCalled();
  });
});
```

**Implementación D3.js**:
```typescript
// src/app/components/charts/line-chart.component.ts
export class LineChartComponent implements OnInit {
  @Input() data: any[];
  @Input() width = 800;
  @Input() height = 400;
  
  private chart: any;
  private svg: any;

  ngOnInit() {
    this.createChart();
    this.drawChart();
  }

  private createChart() {
    this.svg = d3.select('#chart-container')
      .append('svg')
      .attr('width', this.width)
      .attr('height', this.height);

    this.chart = this.svg.append('g')
      .attr('transform', `translate(50, 20)`);
  }

  private drawChart() {
    const xScale = d3.scaleTime()
      .domain(d3.extent(this.data, d => new Date(d.date)))
      .range([0, this.width - 100]);

    const yScale = d3.scaleLinear()
      .domain(d3.extent(this.data, d => d.value))
      .range([this.height - 40, 0]);

    const line = d3.line()
      .x(d => xScale(new Date(d.date)))
      .y(d => yScale(d.value));

    this.chart.append('path')
      .datum(this.data)
      .attr('class', 'line')
      .attr('d', line)
      .attr('fill', 'none')
      .attr('stroke', 'steelblue')
      .attr('stroke-width', 2);
  }

  exportAsPNG() {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    // Convert SVG to PNG
    const svgData = new XMLSerializer().serializeToString(this.svg.node());
    const img = new Image();
    
    img.onload = () => {
      canvas.width = this.width;
      canvas.height = this.height;
      ctx.drawImage(img, 0, 0);
      
      const link = document.createElement('a');
      link.download = 'chart.png';
      link.href = canvas.toDataURL();
      link.click();
    };
    
    img.src = 'data:image/svg+xml;base64,' + btoa(svgData);
  }
}
```

### Día 7-8: Sistema de Búsqueda Guardada

**Objetivo**: Implementar guardado y recuperación de búsquedas

**TDD Implementación**:
```go
// tests/services/saved_search_test.go
func TestSavedSearch(t *testing.T) {
    service := NewSavedSearchService(mockDB)
    
    // Test guardar búsqueda
    search := SavedSearch{
        Name: "Math Courses 2024",
        Query: "mathematics",
        Entities: []string{"courses"},
        Filters: SearchFilters{DateRange: "2024-01-01:2024-12-31"},
        UserID: "teacher@school.edu",
    }
    
    err := service.SaveSearch(search)
    assert.NoError(t, err)
    
    // Test recuperar búsquedas
    searches, err := service.GetUserSearches("teacher@school.edu")
    assert.NoError(t, err)
    assert.Len(t, searches, 1)
    assert.Equal(t, "Math Courses 2024", searches[0].Name)
}
```

### Día 9-10: Integración Completa y Testing

**Objetivo**: Integrar todos los componentes y validar funcionamiento

**E2E Testing**:
```typescript
// e2e/visualization.e2e-spec.ts
import { test, expect } from '@playwright/test';

test.describe('Visualization Features', () => {
  test('advanced search works correctly', async ({ page }) => {
    await page.goto('/search');
    
    await page.fill('[data-testid="search-input"]', 'mathematics');
    await page.selectOption('[data-testid="entity-select"]', 'courses');
    await page.fill('[data-testid="date-range"]', '2024-01-01:2024-12-31');
    await page.click('[data-testid="search-button"]');
    
    await expect(page.locator('[data-testid="search-results"]')).toBeVisible();
    await expect(page.locator('[data-testid="course-item"]')).toHaveCount(3);
  });

  test('websocket notifications work', async ({ page }) => {
    await page.goto('/dashboard');
    
    // Simular notificación
    await page.evaluate(() => {
      const ws = new WebSocket('ws://localhost:8081/ws');
      ws.onopen = () => {
        ws.send(JSON.stringify({
          type: 'test_notification',
          message: 'Test notification'
        }));
      };
    });
    
    await expect(page.locator('[data-testid="notification"]')).toBeVisible();
  });

  test('chart export works', async ({ page }) => {
    await page.goto('/analytics');
    
    await page.click('[data-testid="export-chart"]');
    
    // Verificar descarga
    const downloadPromise = page.waitForEvent('download');
    await page.click('[data-testid="export-png"]');
    const download = await downloadPromise;
    
    expect(download.suggestedFilename()).toBe('chart.png');
  });
});
```

## ✅ FINAL: Checklist Verificación y Próximos Pasos

### Criterios de Aceptación Fase 3
- [ ] **Búsqueda Avanzada**: Multi-entidad con filtros funcionando
- [ ] **WebSocket**: Notificaciones real-time operativas
- [ ] **Gráficos Interactivos**: D3.js + exportación implementados
- [ ] **Búsqueda Guardada**: Guardado y recuperación funcionando
- [ ] **Performance**: <1.5s load time
- [ ] **Testing**: Cobertura ≥80% en servicios críticos
- [ ] **E2E Tests**: Playwright tests para visualizaciones

### Comandos de Verificación
```bash
# Verificar búsqueda
curl -X POST http://localhost:8081/search \
  -H "Content-Type: application/json" \
  -d '{"query":"mathematics","entities":["courses"],"filters":{"dateRange":"2024-01-01:2024-12-31"}}'

# Verificar WebSocket
wscat -c ws://localhost:8081/ws

# Verificar frontend
ng test --watch=false
ng e2e --configuration=ci
```

### Funcionalidades Implementadas
- **Búsqueda Multi-entidad**: Cursos, estudiantes, tareas
- **Filtros Contextuales**: Por fecha, rol, tipo
- **Notificaciones Real-time**: WebSocket + broadcast
- **Gráficos Interactivos**: D3.js + exportación PNG/SVG
- **Búsqueda Guardada**: Persistencia y recuperación

### Próximos Pasos
1. **Iniciar Fase 4**: Integración completa
2. **Implementar accesibilidad**: WCAG 2.2 AA
3. **Sincronización bidireccional**: Google Classroom
4. **Performance optimization**: <1s load time

### Métricas de Éxito
- **Search Performance**: <500ms response time
- **WebSocket Latency**: <100ms notification delivery
- **Chart Rendering**: <200ms D3.js visualization
- **Testing Coverage**: ≥80% servicios críticos
- **User Experience**: Interactividad fluida

**Estado**: ✅ LISTO PARA FASE 4  
**Duración**: 10 días  
**Visualizaciones**: D3.js + WebSocket + Búsqueda Avanzada  
**Performance**: <1.5s load time garantizado
