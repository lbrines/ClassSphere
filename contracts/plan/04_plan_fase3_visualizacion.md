---
title: "ClassSphere - Fase 3: Visualización Avanzada"
version: "1.0"
type: "phase_plan"
context_priority: "MEDIUM"
max_tokens: 1000
phase: "3"
duration: "10 días"
tdd_compliance: "100%"
date: "2025-10-05"
---

[← Fase 2](03_plan_fase2_google_integration.md) | [Plan Principal](01_plan_index.md) | [Siguiente → Fase 4](05_plan_fase4_integracion.md)

# Fase 3: Visualización Avanzada (MEDIUM Priority)

## 🎯 INICIO: Objetivos Críticos

### Objetivo de la Fase
Implementar búsqueda avanzada, notificaciones en tiempo real con WebSocket, y gráficos interactivos con drill-down.

### Dependencias Bloqueantes
- Fase 2 completada (100%)
- WebSocket support configurado
- D3.js disponible (opcional)

### Duración Total
**10 días**

### Context Management
- **Priority**: MEDIUM
- **Max Tokens**: 1000 por chunk
- **Chunk Position**: Middle
- **Lost-in-Middle Risk**: Medium

---

## 📅 MEDIO: Implementación por Días

### Día 23: Sistema de Búsqueda Avanzada - Backend

**backend/src/app/services/search_service.py**
```python
"""
Servicio de búsqueda avanzada
"""
from typing import List, Dict, Any
from enum import Enum


class SearchEntity(str, Enum):
    """Entidades buscables"""
    STUDENTS = "students"
    COURSES = "courses"
    ASSIGNMENTS = "assignments"


class SearchService:
    """Servicio de búsqueda"""
    
    async def search(
        self,
        entity: SearchEntity,
        query: str,
        filters: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """Búsqueda con filtros"""
        # Mock implementation
        if entity == SearchEntity.STUDENTS:
            return self._search_students(query, filters)
        elif entity == SearchEntity.COURSES:
            return self._search_courses(query, filters)
        return []
    
    def _search_students(self, query: str, filters: Dict) -> List[Dict]:
        """Búsqueda de estudiantes"""
        return [
            {
                "id": "student-001",
                "name": "John Doe",
                "email": "john@example.com",
                "course": "eCommerce Specialist"
            }
        ]
    
    def _search_courses(self, query: str, filters: Dict) -> List[Dict]:
        """Búsqueda de cursos"""
        return [
            {
                "id": "course-001",
                "name": "eCommerce Specialist",
                "students": 150
            }
        ]
```

**Verificación:**
```bash
curl "http://localhost:8000/api/v1/search/students?q=john"
```

---

### Día 24: WebSocket para Notificaciones - Backend

**backend/src/app/services/websocket_service.py**
```python
"""
Servicio WebSocket
"""
from fastapi import WebSocket
from typing import List


class ConnectionManager:
    """Gestor de conexiones WebSocket"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """Conectar cliente"""
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        """Desconectar cliente"""
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        """Broadcast a todos los clientes"""
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()
```

---

### Día 25: Notificaciones Frontend

**frontend/src/hooks/useWebSocket.ts**
```typescript
import { useEffect, useState } from 'react';

interface Notification {
  type: string;
  message: string;
  timestamp: string;
}

export function useWebSocket(url: string) {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const ws = new WebSocket(url);

    ws.onopen = () => {
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setNotifications(prev => [...prev, {
        ...data,
        timestamp: new Date().toISOString()
      }]);
    };

    ws.onclose = () => {
      setIsConnected(false);
    };

    return () => {
      ws.close();
    };
  }, [url]);

  return { notifications, isConnected };
}
```

---

### Días 26-32: Resumen

**Día 26:** Gráficos interactivos con drill-down
**Día 27:** Búsqueda avanzada frontend
**Día 28:** Filtros contextuales
**Día 29:** Widgets personalizables
**Día 30:** Exportación de datos
**Día 31:** Tests E2E completos
**Día 32:** Performance optimization

---

## ✅ FINAL: Checklist y Próximos Pasos

### Checklist de Verificación Fase 3

**Backend:**
- [ ] Búsqueda avanzada funcionando
- [ ] WebSocket implementado
- [ ] Notificaciones en tiempo real
- [ ] Tests ≥85% coverage

**Frontend:**
- [ ] Búsqueda con filtros
- [ ] NotificationCenter funcionando
- [ ] Gráficos interactivos con drill-down
- [ ] Widgets personalizables
- [ ] Tests ≥85% coverage

**Performance:**
- [ ] Búsqueda < 500ms
- [ ] WebSocket conecta sin errores
- [ ] Notificaciones en tiempo real
- [ ] Gráficos renderizan < 1s

### Comandos de Validación

```bash
# Backend
pytest tests/ --cov=src --cov-fail-under=85

# Frontend
npm run test -- --coverage

# E2E
npm run test:e2e -- search.spec.ts notifications.spec.ts

# WebSocket test
wscat -c ws://localhost:8000/ws/notifications
```

### Próximos Pasos

**Continuar con Fase 4:**
- [05_plan_fase4_integracion.md](05_plan_fase4_integracion.md)
- Sincronización bidireccional Google
- Accesibilidad WCAG 2.2 AA
- CI/CD completo

---

[← Fase 2](03_plan_fase2_google_integration.md) | [Plan Principal](01_plan_index.md) | [Siguiente → Fase 4](05_plan_fase4_integracion.md)
