---
title: "ClassSphere - Fase 3: Visualización Avanzada TDD"
version: "1.0"
type: "documentation"
date: "2025-10-04"
author: "Sistema de Contratos LLM"
related_files:
  - "01_plam_index.md"
  - "03_plan_fase2_google_integration.md"
  - "05_plan_fase4_integracion.md"
---

[← Fase 2: Integración Google](03_plan_fase2_google_integration.md) | [Índice](01_plam_index.md) | [Siguiente → Fase 4: Integración Completa](05_plan_fase4_integracion.md)

# Fase 3: Visualización Avanzada TDD

## Objetivos de la Fase

Esta fase implementa funcionalidades avanzadas de visualización y experiencia de usuario siguiendo metodología TDD:

1. **Backend Avanzado**: Búsqueda, notificaciones y WebSockets
2. **Frontend Avanzado**: UI avanzada y gráficos interactivos
3. **Visualización Completa**: Dashboards personalizables con D3.js y ApexCharts
4. **Experiencia de Usuario**: Optimización mobile y accesibilidad básica

## Duración Estimada: 8-10 días

### Distribución de Tareas

**Días 24-26: Backend Avanzado**
- Tests para búsqueda + notificaciones + WebSocket
- Implementación de servicios avanzados
- Métricas predictivas + insights
- Sistema de alertas inteligentes

**Días 27-29: Frontend Avanzado**
- Tests para búsqueda + notificaciones + gráficos avanzados
- Implementación UI avanzada
- Widgets personalizables + drill-down
- Notificaciones tiempo real

**Días 30-32: Visualización Completa**
- Tests para D3.js + ApexCharts avanzado
- Gráficos interactivos + exportación
- Dashboards personalizables
- Performance optimization

**Días 33-34: Integración Avanzada**
- Tests E2E para flujos avanzados
- WebSocket testing + performance
- Mobile optimization
- Accessibility básica

## Estructura de Tests Backend

### Requisitos Técnicos Obligatorios

1. **Timeouts en Tests WebSocket**
   ```python
   # test_websocket.py
   @pytest.mark.asyncio
   async def test_websocket_connection():
       """Test conexión WebSocket con timeout"""
       async with websockets.connect("ws://localhost:8000/ws") as websocket:
           # Enviar mensaje
           await websocket.send(json.dumps({"type": "subscribe", "channel": "notifications"}))
           
           # Recibir respuesta con timeout
           response = await asyncio.wait_for(
               websocket.recv(),
               timeout=2.0  # Timeout obligatorio
           )
           
           data = json.loads(response)
           assert data["type"] == "subscription_success"
   ```

2. **Tests de Búsqueda Avanzada**
   ```python
   # test_search_service.py
   @pytest.mark.asyncio
   async def test_search_with_complex_query():
       """Test búsqueda avanzada con query compleja"""
       search_service = SearchService()
       query = {
           "text": "matemáticas",
           "filters": {
               "course_state": "active",
               "date_range": {
                   "start": "2025-01-01",
                   "end": "2025-12-31"
               },
               "teacher_id": "teacher-001"
           },
           "sort": {"field": "relevance", "order": "desc"},
           "page": 1,
           "limit": 10
       }
       
       result = await asyncio.wait_for(
           search_service.search(query),
           timeout=3.0  # Timeout obligatorio
       )
       
       assert "results" in result
       assert "total" in result
       assert "page" in result
       assert len(result["results"]) > 0
   ```

3. **Tests de Notificaciones en Tiempo Real**
   ```python
   # test_notification_service.py
   @pytest.mark.asyncio
   async def test_send_notification():
       """Test envío de notificación en tiempo real"""
       notification_service = NotificationService()
       notification = {
           "user_id": "user-001",
           "type": "course_update",
           "title": "Curso actualizado",
           "message": "El curso ha sido actualizado",
           "data": {
               "course_id": "course-001",
               "update_type": "material_added"
           }
       }
       
       result = await asyncio.wait_for(
           notification_service.send_notification(notification),
           timeout=2.0  # Timeout obligatorio
       )
       
       assert result["success"] is True
       assert "notification_id" in result
   ```

### Estructura de Directorios de Tests

```
backend/
└── tests/
    ├── unit/
    │   ├── services/
    │   │   ├── test_search_service.py
    │   │   ├── test_notification_service.py
    │   │   └── test_websocket_service.py
    │   └── api/
    │       ├── test_search_endpoints.py
    │       └── test_notification_endpoints.py
    ├── integration/
    │   ├── test_search_integration.py
    │   └── test_notifications_integration.py
    └── websocket/
        ├── test_websocket_connection.py
        └── test_websocket_notifications.py
```

### Tests Unitarios Críticos

```python
# test_search_service.py
@pytest.mark.asyncio
async def test_search_with_pagination():
    """Test búsqueda con paginación"""
    search_service = SearchService()
    
    # Primera página
    result_page1 = await asyncio.wait_for(
        search_service.search({"text": "curso", "page": 1, "limit": 2}),
        timeout=2.0  # Timeout obligatorio
    )
    
    # Segunda página
    result_page2 = await asyncio.wait_for(
        search_service.search({"text": "curso", "page": 2, "limit": 2}),
        timeout=2.0  # Timeout obligatorio
    )
    
    assert len(result_page1["results"]) == 2
    assert len(result_page2["results"]) == 2
    assert result_page1["results"][0]["id"] != result_page2["results"][0]["id"]
    assert result_page1["page"] == 1
    assert result_page2["page"] == 2

@pytest.mark.asyncio
async def test_search_with_filters():
    """Test búsqueda con filtros"""
    search_service = SearchService()
    
    result = await asyncio.wait_for(
        search_service.search({
            "text": "curso",
            "filters": {"teacher_id": "teacher-001"}
        }),
        timeout=2.0  # Timeout obligatorio
    )
    
    assert len(result["results"]) > 0
    for item in result["results"]:
        assert item["teacher_id"] == "teacher-001"
```

### Tests de WebSockets

```python
# test_websocket_notifications.py
@pytest.mark.asyncio
async def test_notification_broadcast():
    """Test broadcast de notificaciones por WebSocket"""
    # Conectar cliente WebSocket
    async with websockets.connect("ws://localhost:8000/ws") as websocket:
        # Suscribirse al canal de notificaciones
        await websocket.send(json.dumps({
            "type": "subscribe",
            "channel": "notifications",
            "user_id": "user-001"
        }))
        
        # Recibir confirmación de suscripción
        response = await asyncio.wait_for(
            websocket.recv(),
            timeout=2.0  # Timeout obligatorio
        )
        data = json.loads(response)
        assert data["type"] == "subscription_success"
        
        # Enviar notificación a través del servicio
        notification_service = NotificationService()
        await notification_service.send_notification({
            "user_id": "user-001",
            "type": "course_update",
            "message": "Curso actualizado"
        })
        
        # Recibir notificación por WebSocket
        notification = await asyncio.wait_for(
            websocket.recv(),
            timeout=2.0  # Timeout obligatorio
        )
        notification_data = json.loads(notification)
        
        assert notification_data["type"] == "notification"
        assert notification_data["data"]["message"] == "Curso actualizado"
```

## Estructura de Tests Frontend

### Requisitos Técnicos Obligatorios

1. **Timeouts en Tests de Gráficos**
   ```typescript
   // AdvancedChart.test.tsx
   test('renders chart with data within timeout', async () => {
     render(<AdvancedChart data={mockChartData} />);
     
     // Esperar renderizado con timeout
     await waitFor(() => {
       // Verificar que el gráfico se ha renderizado
       expect(screen.getByTestId('advanced-chart')).toBeInTheDocument();
     }, { timeout: 3000 });
   });
   ```

2. **Tests de Componentes Interactivos**
   ```typescript
   // DrillDownChart.test.tsx
   test('handles drill down interaction', async () => {
     const handleDrillDown = vi.fn();
     const user = userEvent.setup();
     
     render(
       <DrillDownChart 
         data={mockChartData} 
         onDrillDown={handleDrillDown} 
       />
     );
     
     // Esperar renderizado
     await waitFor(() => {
       expect(screen.getByTestId('drill-down-chart')).toBeInTheDocument();
     }, { timeout: 2000 });
     
     // Simular interacción de drill down
     const dataPoint = screen.getByTestId('data-point-1');
     await user.click(dataPoint);
     
     // Verificar que se llamó al callback
     expect(handleDrillDown).toHaveBeenCalledWith({
       id: 'data-1',
       value: 42,
       category: 'Category A'
     });
   });
   ```

3. **Tests de WebSocket en Frontend**
   ```typescript
   // useWebSocket.test.ts
   test('connects to WebSocket and receives messages', async () => {
     // Mock de WebSocket
     const mockWebSocket = {
       addEventListener: vi.fn(),
       send: vi.fn(),
       close: vi.fn()
     };
     
     // Mock de la clase WebSocket
     global.WebSocket = vi.fn().mockImplementation(() => mockWebSocket);
     
     const { result } = renderHook(() => useWebSocket('ws://localhost:8000/ws'));
     
     // Simular mensaje recibido
     const messageHandler = mockWebSocket.addEventListener.mock.calls.find(
       call => call[0] === 'message'
     )[1];
     
     act(() => {
       messageHandler({ data: JSON.stringify({ type: 'test', data: 'message' }) });
     });
     
     // Verificar que se recibió el mensaje
     await waitFor(() => {
       expect(result.current.lastMessage).toEqual({ type: 'test', data: 'message' });
     }, { timeout: 2000 });
   });
   ```

### Estructura de Directorios de Tests

```
frontend/
└── src/
    ├── components/
    │   ├── search/
    │   │   ├── SearchBar.tsx
    │   │   ├── SearchBar.test.tsx
    │   │   ├── SearchResults.tsx
    │   │   └── SearchResults.test.tsx
    │   ├── notifications/
    │   │   ├── NotificationCenter.tsx
    │   │   └── NotificationCenter.test.tsx
    │   └── charts/
    │       ├── AdvancedChart.tsx
    │       ├── AdvancedChart.test.tsx
    │       ├── DrillDownChart.tsx
    │       └── DrillDownChart.test.tsx
    ├── hooks/
    │   ├── useSearch.ts
    │   ├── useSearch.test.ts
    │   ├── useNotifications.ts
    │   ├── useNotifications.test.ts
    │   ├── useWebSocket.ts
    │   └── useWebSocket.test.ts
    └── test/
        └── mocks/
            ├── websocket.ts
            └── chartData.ts
```

### Tests de Componentes Avanzados

```typescript
// NotificationCenter.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import userEvent from '@testing-library/user-event';
import NotificationCenter from './NotificationCenter';

// Mock de useNotifications
vi.mock('../../hooks/useNotifications', () => ({
  useNotifications: () => ({
    notifications: [
      { 
        id: 'notif-1', 
        title: 'New assignment', 
        message: 'You have a new assignment', 
        read: false,
        timestamp: new Date().toISOString()
      },
      { 
        id: 'notif-2', 
        title: 'Grade posted', 
        message: 'Your grade has been posted', 
        read: true,
        timestamp: new Date().toISOString()
      }
    ],
    markAsRead: vi.fn(),
    clearAll: vi.fn()
  })
}));

describe('NotificationCenter', () => {
  it('renders notifications correctly', async () => {
    render(<NotificationCenter />);
    
    // Verificar que se muestran las notificaciones
    expect(screen.getByText('New assignment')).toBeInTheDocument();
    expect(screen.getByText('Grade posted')).toBeInTheDocument();
    
    // Verificar indicador de no leído
    const unreadIndicator = screen.getByTestId('unread-indicator-notif-1');
    expect(unreadIndicator).toBeInTheDocument();
    
    // No debería haber indicador para notificación leída
    const readNotification = screen.queryByTestId('unread-indicator-notif-2');
    expect(readNotification).not.toBeInTheDocument();
  });
  
  it('marks notification as read on click', async () => {
    const user = userEvent.setup();
    const { markAsRead } = useNotifications();
    
    render(<NotificationCenter />);
    
    // Click en notificación
    const notification = screen.getByText('New assignment');
    await user.click(notification);
    
    // Verificar que se llamó a markAsRead
    expect(markAsRead).toHaveBeenCalledWith('notif-1');
  });
  
  it('clears all notifications', async () => {
    const user = userEvent.setup();
    const { clearAll } = useNotifications();
    
    render(<NotificationCenter />);
    
    // Click en botón clear all
    const clearButton = screen.getByRole('button', { name: /clear all/i });
    await user.click(clearButton);
    
    // Verificar que se llamó a clearAll
    expect(clearAll).toHaveBeenCalled();
  });
});
```

### Tests de Hooks Avanzados

```typescript
// useSearch.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useSearch } from './useSearch';

// Mock de fetch
global.fetch = vi.fn();

describe('useSearch', () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });
  
  it('performs search with query', async () => {
    // Mock de respuesta exitosa
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        data: {
          results: [
            { id: 'result-1', title: 'Result 1' },
            { id: 'result-2', title: 'Result 2' }
          ],
          total: 2,
          page: 1
        }
      })
    } as Response);
    
    const { result } = renderHook(() => useSearch());
    
    // Ejecutar búsqueda
    result.current.search('test query');
    
    // Verificar resultados con timeout
    await waitFor(() => {
      expect(result.current.results).toHaveLength(2);
      expect(result.current.isLoading).toBe(false);
      expect(result.current.error).toBeNull();
    }, { timeout: 3000 });
    
    // Verificar que se llamó a fetch correctamente
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining('/api/v1/search'),
      expect.objectContaining({
        method: 'POST',
        body: expect.stringContaining('test query')
      })
    );
  });
  
  it('handles search with filters', async () => {
    // Mock de respuesta exitosa
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        data: {
          results: [{ id: 'result-1', title: 'Result 1' }],
          total: 1,
          page: 1
        }
      })
    } as Response);
    
    const { result } = renderHook(() => useSearch());
    
    // Ejecutar búsqueda con filtros
    result.current.search('test query', {
      course_state: 'active',
      teacher_id: 'teacher-001'
    });
    
    // Verificar resultados
    await waitFor(() => {
      expect(result.current.results).toHaveLength(1);
    }, { timeout: 3000 });
    
    // Verificar que se incluyeron los filtros
    expect(fetch).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        body: expect.stringContaining('course_state')
      })
    );
  });
});
```

## Comandos de Testing

### Backend Tests

```bash
# Tests unitarios de servicios avanzados
pytest tests/unit/services/test_search_service.py tests/unit/services/test_notification_service.py --cov=src.app.services

# Tests de WebSocket
pytest tests/websocket/ --cov=src.app.websocket

# Tests completos con cobertura
pytest tests/ --cov=src --cov-report=term-missing
```

### Frontend Tests

```bash
# Tests de componentes de búsqueda
npm run test -- --testPathPattern=src/components/search

# Tests de componentes de notificaciones
npm run test -- --testPathPattern=src/components/notifications

# Tests de componentes de gráficos
npm run test -- --testPathPattern=src/components/charts

# Tests completos con cobertura
npm run test -- --coverage
```

## Criterios de Aceptación

### Backend Avanzado

- [ ] Sistema de búsqueda avanzada con filtros y paginación
- [ ] Servicio de notificaciones en tiempo real
- [ ] WebSockets para actualizaciones en tiempo real
- [ ] Métricas predictivas y alertas inteligentes
- [ ] Tests con cobertura ≥90% en módulos críticos

### Frontend Avanzado

- [ ] Componentes de búsqueda avanzada
- [ ] Centro de notificaciones en tiempo real
- [ ] Gráficos interactivos con drill-down
- [ ] Widgets personalizables
- [ ] Tests con cobertura ≥80%

### Visualización Completa

- [ ] Dashboards personalizables por rol
- [ ] Gráficos avanzados con D3.js y ApexCharts
- [ ] Exportación de datos y gráficos
- [ ] Optimización de rendimiento (<2s para cargar gráficos)
- [ ] Tests para todos los componentes visuales

### Integración Avanzada

- [ ] Tests E2E para flujos avanzados
- [ ] Optimización para dispositivos móviles
- [ ] Accesibilidad básica (navegación por teclado)
- [ ] WebSockets estables con reconexión automática

## Referencias

Para más detalles sobre la implementación TDD con visualización avanzada, consultar:
- [Estrategia de Testing Unificada](principal/09_ClassSphere_testing.md)
- [Plan de Implementación Unificado](principal/10_ClassSphere_plan_implementacion.md)
- [TDD Best Practices](extra/TDD_BEST_PRACTICES.md)

---

[← Fase 2: Integración Google](03_plan_fase2_google_integration.md) | [Índice](01_plam_index.md) | [Siguiente → Fase 4: Integración Completa](05_plan_fase4_integracion.md)
