# Plan de Ejecución TDD: Fase 3 - Visualización Avanzada

---
**Autor**: Sistema de Planes de Ejecución TDD
**Fecha**: 2025-10-04
**Versión**: 1.0
**Fase**: Visualización Avanzada TDD (Días 24-34)
---

## Objetivo de la Fase

Implementar funcionalidades avanzadas de visualización, búsqueda, notificaciones y WebSockets siguiendo metodología TDD estricta, garantizando la cobertura 100% en todos los componentes de visualización y comunicación en tiempo real.

## Principios TDD de la Fase 3

### Ciclo TDD Estricto para Visualización

1. **Red**: Escribir test que falle para cada componente de visualización
2. **Green**: Implementar código mínimo para visualización funcional
3. **Refactor**: Optimizar visualización manteniendo tests verdes

### Timeouts para Tests de Visualización y WebSockets

Todos los tests de la Fase 3 tendrán timeouts específicos:

```python
# Tests unitarios de componentes: 2 segundos máximo
@pytest.mark.asyncio(timeout=2.0)
async def test_chart_component_unit():
    # Test code here
    pass

# Tests de WebSockets: 5 segundos máximo
@pytest.mark.asyncio(timeout=5.0)
async def test_websocket_connection():
    # Test code here
    pass

# Tests de renderizado de gráficos: 3 segundos máximo
@pytest.mark.asyncio(timeout=3.0)
async def test_chart_rendering():
    # Test code here
    pass
```

### Puerto 3000 para Frontend

El frontend siempre se ejecutará en el puerto 3000:

```javascript
// next.config.js
module.exports = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ];
  },
  server: {
    port: 3000, // Puerto fijo para frontend
  },
};
```

## Plan de Implementación TDD

### Día 24-26: Servicios Avanzados TDD

#### Día 24: Sistema de Búsqueda TDD

1. **Sistema de búsqueda avanzada (multi-entity)**
   - Test: Verificar funcionalidad de búsqueda
   - Implementación: Implementar servicio de búsqueda
   - Refactor: Optimizar algoritmos

2. **API de búsqueda**
   - Test: Verificar endpoints de búsqueda
   - Implementación: Implementar endpoints
   - Refactor: Optimizar respuestas

#### Día 25: Servicios de Notificaciones TDD

1. **Servicios de notificaciones (WebSocket + Email + Telegram mock)**
   - Test: Verificar envío de notificaciones
   - Implementación: Implementar servicios
   - Refactor: Optimizar entrega

2. **WebSockets en tiempo real con connection recovery**
   - Test: Verificar conexión WebSocket
   - Implementación: Implementar servicio WebSocket
   - Refactor: Implementar recovery

#### Día 26: Alertas y Métricas TDD

1. **Sistema de alertas inteligentes**
   - Test: Verificar generación de alertas
   - Implementación: Implementar sistema de alertas
   - Refactor: Optimizar reglas

2. **Métricas predictivas e insights**
   - Test: Verificar cálculo de métricas
   - Implementación: Implementar algoritmos
   - Refactor: Optimizar precisión

### Día 27-29: Visualización Backend TDD

#### Día 27: APIs para Gráficos TDD

1. **APIs para gráficos avanzados**
   - Test: Verificar generación de datos para gráficos
   - Implementación: Implementar endpoints
   - Refactor: Optimizar formato de datos

2. **Exportación de datos (PDF, PNG, SVG)**
   - Test: Verificar generación de archivos
   - Implementación: Implementar exportación
   - Refactor: Optimizar calidad

#### Día 28: Sistema de Widgets TDD

1. **Sistema de widgets personalizables**
   - Test: Verificar configuración de widgets
   - Implementación: Implementar sistema de widgets
   - Refactor: Optimizar personalización

2. **API de configuración de widgets**
   - Test: Verificar guardado/carga de configuración
   - Implementación: Implementar endpoints
   - Refactor: Optimizar persistencia

#### Día 29: Optimización de Visualización TDD

1. **Cache avanzado para visualizaciones**
   - Test: Verificar mejora de rendimiento
   - Implementación: Implementar estrategias de cache
   - Refactor: Optimizar invalidación

2. **Optimización de queries complejas**
   - Test: Verificar rendimiento de queries
   - Implementación: Implementar optimizaciones
   - Refactor: Ajustar índices y estructura

### Día 30-32: Frontend Avanzado TDD

#### Día 30: Componentes de Búsqueda TDD

1. **Componentes de búsqueda avanzada (SearchBar, SearchResults)**
   - Test: Verificar renderizado y funcionalidad
   - Implementación: Implementar componentes
   - Refactor: Optimizar UX

2. **Integración de búsqueda con API**
   - Test: Verificar comunicación con backend
   - Implementación: Implementar integración
   - Refactor: Optimizar manejo de errores

#### Día 31: Sistema de Notificaciones Frontend TDD

1. **Sistema de notificaciones (NotificationCenter, NotificationBadge)**
   - Test: Verificar renderizado y funcionalidad
   - Implementación: Implementar componentes
   - Refactor: Optimizar UX

2. **WebSocket hooks y real-time updates**
   - Test: Verificar actualización en tiempo real
   - Implementación: Implementar hooks
   - Refactor: Optimizar reconexión

#### Día 32: Gráficos Avanzados TDD

1. **Gráficos interactivos con D3.js + ApexCharts avanzado**
   - Test: Verificar renderizado e interactividad
   - Implementación: Implementar gráficos
   - Refactor: Optimizar rendimiento

2. **Widgets personalizables con drag & drop**
   - Test: Verificar funcionalidad drag & drop
   - Implementación: Implementar sistema de widgets
   - Refactor: Optimizar persistencia

### Día 33-34: Integración Avanzada TDD

#### Día 33: Testing E2E TDD

1. **Tests E2E para flujos avanzados**
   - Test: Verificar flujos completos
   - Implementación: Implementar tests E2E
   - Refactor: Optimizar cobertura

2. **WebSocket testing y performance**
   - Test: Verificar rendimiento de WebSockets
   - Implementación: Implementar tests específicos
   - Refactor: Optimizar configuración

#### Día 34: Optimización y Accesibilidad TDD

1. **Mobile optimization y responsive design**
   - Test: Verificar visualización en dispositivos móviles
   - Implementación: Implementar diseño responsive
   - Refactor: Optimizar UX móvil

2. **Accessibility básica (keyboard navigation)**
   - Test: Verificar navegación por teclado
   - Implementación: Implementar soporte
   - Refactor: Optimizar accesibilidad

3. **Visual regression testing**
   - Test: Verificar consistencia visual
   - Implementación: Implementar tests de regresión
   - Refactor: Optimizar detección

## Criterios de Aceptación TDD Fase 3

- [ ] Búsqueda avanzada funciona correctamente
- [ ] Notificaciones se envían en tiempo real
- [ ] WebSockets funcionan con connection recovery
- [ ] Gráficos interactivos renderizan correctamente
- [ ] Tests de performance pasan
- [ ] Mobile optimization funciona
- [ ] Accessibility básica implementada

## Templates TDD Estándar

### Template para Tests de Búsqueda

```python
"""
Test file for search_service.py

CRITICAL OBJECTIVES:
- Verify multi-entity search functionality
- Test search performance

DEPENDENCIES:
- AsyncMock for database
- Mock data for search results
"""

import pytest
from unittest.mock import AsyncMock, patch
import time

from src.app.services.search_service import SearchService
from src.app.core.config import settings

# BEGINNING: Critical tests for core functionality
@pytest.fixture
def mock_search_results():
    """Mock search results for testing"""
    return {
        "courses": [
            {"id": "course1", "name": "Matemáticas Avanzadas", "score": 0.95},
            {"id": "course2", "name": "Introducción a Matemáticas", "score": 0.85}
        ],
        "students": [
            {"id": "student1", "name": "María Matemática", "score": 0.90},
            {"id": "student2", "name": "Juan Matemático", "score": 0.80}
        ],
        "assignments": [
            {"id": "assignment1", "title": "Ejercicios de Matemáticas", "score": 0.92},
            {"id": "assignment2", "title": "Examen de Matemáticas", "score": 0.88}
        ]
    }

@pytest.mark.asyncio(timeout=2.0)
async def test_multi_entity_search(mock_search_results):
    # Arrange
    search_service = SearchService()
    query = "matemáticas"
    
    with patch('src.app.services.search_service.SearchService._search_courses') as mock_search_courses, \
         patch('src.app.services.search_service.SearchService._search_students') as mock_search_students, \
         patch('src.app.services.search_service.SearchService._search_assignments') as mock_search_assignments:
        
        mock_search_courses.return_value = mock_search_results["courses"]
        mock_search_students.return_value = mock_search_results["students"]
        mock_search_assignments.return_value = mock_search_results["assignments"]
        
        # Act
        results = await search_service.search(query)
        
        # Assert
        assert "courses" in results
        assert "students" in results
        assert "assignments" in results
        assert len(results["courses"]) == 2
        assert len(results["students"]) == 2
        assert len(results["assignments"]) == 2
        assert results["courses"][0]["score"] > results["courses"][1]["score"]  # Verify sorting

# MIDDLE: Detailed implementation tests
@pytest.mark.asyncio(timeout=2.0)
async def test_search_with_filters():
    # Arrange
    search_service = SearchService()
    query = "matemáticas"
    filters = {"entity_types": ["courses"], "min_score": 0.9}
    
    with patch('src.app.services.search_service.SearchService._search_courses') as mock_search_courses:
        mock_search_courses.return_value = [
            {"id": "course1", "name": "Matemáticas Avanzadas", "score": 0.95}
        ]
        
        # Act
        results = await search_service.search(query, filters=filters)
        
        # Assert
        assert "courses" in results
        assert "students" not in results
        assert "assignments" not in results
        assert len(results["courses"]) == 1
        assert results["courses"][0]["score"] >= 0.9

@pytest.mark.asyncio(timeout=2.0)
async def test_search_performance():
    # Arrange
    search_service = SearchService()
    query = "matemáticas"
    
    with patch('src.app.services.search_service.SearchService._search_courses') as mock_search_courses, \
         patch('src.app.services.search_service.SearchService._search_students') as mock_search_students, \
         patch('src.app.services.search_service.SearchService._search_assignments') as mock_search_assignments:
        
        mock_search_courses.return_value = []
        mock_search_students.return_value = []
        mock_search_assignments.return_value = []
        
        # Act
        start_time = time.time()
        await search_service.search(query)
        end_time = time.time()
        
        # Assert
        duration = end_time - start_time
        assert duration < 0.5  # Search should be fast

# END: Verification and next steps
@pytest.mark.asyncio(timeout=2.0)
async def test_empty_search_results():
    # Arrange
    search_service = SearchService()
    query = "nonexistentterm"
    
    with patch('src.app.services.search_service.SearchService._search_courses') as mock_search_courses, \
         patch('src.app.services.search_service.SearchService._search_students') as mock_search_students, \
         patch('src.app.services.search_service.SearchService._search_assignments') as mock_search_assignments:
        
        mock_search_courses.return_value = []
        mock_search_students.return_value = []
        mock_search_assignments.return_value = []
        
        # Act
        results = await search_service.search(query)
        
        # Assert
        assert "courses" in results
        assert "students" in results
        assert "assignments" in results
        assert len(results["courses"]) == 0
        assert len(results["students"]) == 0
        assert len(results["assignments"]) == 0
```

### Template para Tests de WebSockets

```python
"""
Test file for websocket_service.py

CRITICAL OBJECTIVES:
- Verify WebSocket connection and messaging
- Test connection recovery

DEPENDENCIES:
- AsyncMock for WebSocket
- Mock data for notifications
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import asyncio

from src.app.services.websocket_service import WebSocketService
from src.app.core.config import settings

# BEGINNING: Critical tests for core functionality
@pytest.fixture
def mock_websocket():
    """Mock WebSocket for testing"""
    mock_ws = AsyncMock()
    mock_ws.send_json = AsyncMock()
    mock_ws.receive_json = AsyncMock(return_value={"type": "ping"})
    mock_ws.close = AsyncMock()
    return mock_ws

@pytest.mark.asyncio(timeout=5.0)
async def test_websocket_connection(mock_websocket):
    # Arrange
    websocket_service = WebSocketService()
    
    # Act
    await websocket_service.connect(mock_websocket)
    
    # Assert
    assert mock_websocket in websocket_service.active_connections

@pytest.mark.asyncio(timeout=5.0)
async def test_websocket_broadcast():
    # Arrange
    websocket_service = WebSocketService()
    mock_ws1 = AsyncMock()
    mock_ws2 = AsyncMock()
    
    await websocket_service.connect(mock_ws1)
    await websocket_service.connect(mock_ws2)
    
    message = {"type": "notification", "content": "Test message"}
    
    # Act
    await websocket_service.broadcast(message)
    
    # Assert
    mock_ws1.send_json.assert_called_once_with(message)
    mock_ws2.send_json.assert_called_once_with(message)

# MIDDLE: Detailed implementation tests
@pytest.mark.asyncio(timeout=5.0)
async def test_websocket_disconnect():
    # Arrange
    websocket_service = WebSocketService()
    mock_ws = AsyncMock()
    
    await websocket_service.connect(mock_ws)
    assert mock_ws in websocket_service.active_connections
    
    # Act
    await websocket_service.disconnect(mock_ws)
    
    # Assert
    assert mock_ws not in websocket_service.active_connections

@pytest.mark.asyncio(timeout=5.0)
async def test_websocket_connection_recovery():
    # Arrange
    websocket_service = WebSocketService()
    mock_ws = AsyncMock()
    mock_ws.receive_json = AsyncMock(side_effect=[ConnectionError, {"type": "ping"}])
    
    # Act & Assert
    with patch('src.app.services.websocket_service.asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
        # Simulate connection error and recovery
        await websocket_service.connect(mock_ws)
        
        # First call raises ConnectionError, then recovers
        await websocket_service.listen(mock_ws)
        
        # Assert recovery attempt was made
        mock_sleep.assert_called_once()
        assert mock_ws in websocket_service.active_connections

# END: Verification and next steps
@pytest.mark.asyncio(timeout=5.0)
async def test_websocket_targeted_message():
    # Arrange
    websocket_service = WebSocketService()
    mock_ws1 = AsyncMock()
    mock_ws2 = AsyncMock()
    
    # Associate WebSockets with user IDs
    user_id1 = "user1"
    user_id2 = "user2"
    
    await websocket_service.connect(mock_ws1, user_id=user_id1)
    await websocket_service.connect(mock_ws2, user_id=user_id2)
    
    message = {"type": "notification", "content": "Test message for user1"}
    
    # Act
    await websocket_service.send_to_user(user_id1, message)
    
    # Assert
    mock_ws1.send_json.assert_called_once_with(message)
    mock_ws2.send_json.assert_not_called()
```

### Template para Tests de Componentes React

```javascript
// SearchBar.test.tsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { SearchBar } from '../components/search/SearchBar';
import { useSearch } from '../hooks/useSearch';

// Mock the custom hook
jest.mock('../hooks/useSearch', () => ({
  useSearch: jest.fn(),
}));

describe('SearchBar Component', () => {
  // BEGINNING: Critical tests for core functionality
  test('renders search input correctly', () => {
    // Arrange
    const mockSearch = jest.fn();
    (useSearch as jest.Mock).mockReturnValue({
      search: mockSearch,
      results: null,
      loading: false,
      error: null,
    });
    
    // Act
    render(<SearchBar placeholder="Buscar..." />);
    
    // Assert
    expect(screen.getByPlaceholderText('Buscar...')).toBeInTheDocument();
  });
  
  test('calls search function on submit', async () => {
    // Arrange
    const mockSearch = jest.fn();
    (useSearch as jest.Mock).mockReturnValue({
      search: mockSearch,
      results: null,
      loading: false,
      error: null,
    });
    
    // Act
    render(<SearchBar placeholder="Buscar..." />);
    const input = screen.getByPlaceholderText('Buscar...');
    fireEvent.change(input, { target: { value: 'matemáticas' } });
    fireEvent.submit(input.closest('form')!);
    
    // Assert
    await waitFor(() => {
      expect(mockSearch).toHaveBeenCalledWith('matemáticas');
    });
  });
  
  // MIDDLE: Detailed implementation tests
  test('displays loading state', () => {
    // Arrange
    const mockSearch = jest.fn();
    (useSearch as jest.Mock).mockReturnValue({
      search: mockSearch,
      results: null,
      loading: true,
      error: null,
    });
    
    // Act
    render(<SearchBar placeholder="Buscar..." />);
    
    // Assert
    expect(screen.getByTestId('search-loading')).toBeInTheDocument();
  });
  
  test('displays error message', () => {
    // Arrange
    const mockSearch = jest.fn();
    (useSearch as jest.Mock).mockReturnValue({
      search: mockSearch,
      results: null,
      loading: false,
      error: 'Error en la búsqueda',
    });
    
    // Act
    render(<SearchBar placeholder="Buscar..." />);
    
    // Assert
    expect(screen.getByText('Error en la búsqueda')).toBeInTheDocument();
  });
  
  // END: Verification and next steps
  test('clears input after submission', async () => {
    // Arrange
    const mockSearch = jest.fn();
    (useSearch as jest.Mock).mockReturnValue({
      search: mockSearch,
      results: null,
      loading: false,
      error: null,
    });
    
    // Act
    render(<SearchBar placeholder="Buscar..." clearOnSubmit />);
    const input = screen.getByPlaceholderText('Buscar...');
    fireEvent.change(input, { target: { value: 'matemáticas' } });
    fireEvent.submit(input.closest('form')!);
    
    // Assert
    await waitFor(() => {
      expect(input).toHaveValue('');
    });
  });
});
```

## Entregables TDD Fase 3

1. **Código Backend**
   - Sistema de búsqueda avanzada
   - Servicios de notificaciones
   - WebSockets en tiempo real
   - APIs para gráficos avanzados
   - Sistema de widgets personalizables

2. **Código Frontend**
   - Componentes de búsqueda avanzada
   - Sistema de notificaciones
   - WebSocket hooks
   - Gráficos interactivos
   - Widgets personalizables

3. **Tests**
   - Tests unitarios para servicios avanzados
   - Tests de WebSockets
   - Tests de componentes React
   - Tests de rendimiento
   - Tests de accesibilidad básica

4. **Documentación**
   - Documentación de API de búsqueda
   - Documentación de WebSockets
   - Documentación de componentes
   - Documentación de gráficos

## Próximos Pasos

1. Validar cumplimiento de criterios de aceptación
2. Preparar transición a Fase 4: Integración Completa TDD
3. Revisar y actualizar documentación
4. Optimizar pipeline CI/CD para Fase 4
