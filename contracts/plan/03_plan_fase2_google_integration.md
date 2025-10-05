---
title: "ClassSphere - Fase 2: Integración Google Classroom"
version: "1.0"
type: "phase_plan"
context_priority: "HIGH"
max_tokens: 1500
phase: "2"
duration: "10 días"
tdd_compliance: "100%"
date: "2025-10-05"
---

[← Fase 1](02_plan_fase1_fundaciones.md) | [Plan Principal](01_plan_index.md) | [Siguiente → Fase 3](04_plan_fase3_visualizacion.md)

# Fase 2: Integración Google Classroom (HIGH Priority)

## 🎯 INICIO: Objetivos Críticos

### Objetivo de la Fase
Integrar Google Classroom API con sistema de mocks completos, modo dual (Google/Mock), y dashboards por rol con visualizaciones ApexCharts.

### Dependencias Bloqueantes
- Fase 1 completada (100%)
- Google Cloud Project creado
- OAuth 2.0 credentials configuradas
- ApexCharts 5.3.5 disponible

### Duración Total
**10 días**

### Context Management
- **Priority**: HIGH
- **Max Tokens**: 1500 por chunk
- **Chunk Position**: Middle (detalle de implementación)
- **Lost-in-Middle Risk**: Medium

---

## 📅 MEDIO: Implementación por Días

### Día 13: Google Classroom API Service

**Objetivo:** Crear servicio base para Google Classroom API con mocks.

**Archivos a crear:**

**backend/src/app/services/google_service.py**
```python
"""
Servicio Google Classroom API
"""
from typing import List, Optional
from pydantic import BaseModel


class Course(BaseModel):
    """Modelo de curso"""
    id: str
    google_id: str
    name: str
    section: str
    status: str
    student_count: int


class GoogleClassroomService:
    """Servicio para Google Classroom API"""
    
    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock
    
    async def get_courses(self) -> List[Course]:
        """Obtener cursos"""
        if self.use_mock:
            return self._get_mock_courses()
        return await self._get_real_courses()
    
    def _get_mock_courses(self) -> List[Course]:
        """Cursos mock para desarrollo"""
        return [
            Course(
                id="course-001",
                google_id="123456789",
                name="eCommerce Specialist",
                section="Section A",
                status="ACTIVE",
                student_count=150
            ),
            Course(
                id="course-002",
                google_id="987654321",
                name="Digital Marketing",
                section="Section B",
                status="ACTIVE",
                student_count=120
            )
        ]
    
    async def _get_real_courses(self) -> List[Course]:
        """Cursos reales de Google Classroom API"""
        # TODO: Implementar integración real
        raise NotImplementedError("Real Google API not implemented yet")
```

**backend/src/app/api/endpoints/google.py**
```python
"""
Endpoints Google Classroom
"""
from fastapi import APIRouter, Depends
from typing import List
from app.services.google_service import GoogleClassroomService, Course

router = APIRouter(prefix="/api/v1/google", tags=["google"])


@router.get("/courses", response_model=List[Course])
async def get_courses(
    service: GoogleClassroomService = Depends()
):
    """Obtener cursos de Google Classroom"""
    return await service.get_courses()


@router.get("/mode")
async def get_mode():
    """Obtener modo actual (Google/Mock)"""
    return {"mode": "mock", "description": "Using mock data"}
```

**Tests:**

**backend/tests/unit/services/test_google_service.py**
```python
"""
Tests para Google Classroom Service
"""
import pytest
from app.services.google_service import GoogleClassroomService


@pytest.mark.asyncio
async def test_get_mock_courses():
    """Test obtener cursos mock"""
    service = GoogleClassroomService(use_mock=True)
    courses = await service.get_courses()
    
    assert len(courses) == 2
    assert courses[0].name == "eCommerce Specialist"
    assert courses[0].student_count == 150


@pytest.mark.asyncio
async def test_real_courses_not_implemented():
    """Test cursos reales no implementados aún"""
    service = GoogleClassroomService(use_mock=False)
    
    with pytest.raises(NotImplementedError):
        await service._get_real_courses()
```

**Verificación Día 13:**
```bash
# Tests
pytest tests/unit/services/test_google_service.py -v

# Test endpoint
curl http://localhost:8000/api/v1/google/courses
curl http://localhost:8000/api/v1/google/mode
```

**Criterios de Aceptación:**
- [ ] GoogleClassroomService implementado
- [ ] Mocks funcionando correctamente
- [ ] Endpoints respondiendo
- [ ] Tests pasando
- [ ] Cobertura ≥85%

---

### Día 14: Dashboards por Rol - Backend

**Objetivo:** Implementar endpoints de dashboard específicos por rol.

**backend/src/app/services/dashboard_service.py**
```python
"""
Servicio de dashboards
"""
from typing import Dict, Any
from app.models.user import UserRole


class DashboardService:
    """Servicio para dashboards por rol"""
    
    async def get_admin_dashboard(self) -> Dict[str, Any]:
        """Dashboard para administradores"""
        return {
            "total_users": 500,
            "total_courses": 25,
            "total_students": 450,
            "system_health": "healthy",
            "recent_activity": []
        }
    
    async def get_coordinator_dashboard(self, user_id: str) -> Dict[str, Any]:
        """Dashboard para coordinadores"""
        return {
            "assigned_programs": 5,
            "total_teachers": 15,
            "total_students": 200,
            "program_metrics": []
        }
    
    async def get_teacher_dashboard(self, user_id: str) -> Dict[str, Any]:
        """Dashboard para profesores"""
        return {
            "my_courses": 3,
            "total_students": 90,
            "pending_assignments": 5,
            "at_risk_students": 2
        }
    
    async def get_student_dashboard(self, user_id: str) -> Dict[str, Any]:
        """Dashboard para estudiantes"""
        return {
            "enrolled_courses": 4,
            "completed_assignments": 15,
            "pending_assignments": 3,
            "overall_grade": 85.5
        }
```

**backend/src/app/api/endpoints/dashboard.py**
```python
"""
Endpoints de dashboards
"""
from fastapi import APIRouter, Depends, HTTPException
from app.services.dashboard_service import DashboardService
from app.models.user import User, UserRole
from app.api.endpoints.auth import get_current_user

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])


@router.get("/admin")
async def get_admin_dashboard(
    current_user: User = Depends(get_current_user),
    service: DashboardService = Depends()
):
    """Dashboard de administrador"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return await service.get_admin_dashboard()


@router.get("/coordinator")
async def get_coordinator_dashboard(
    current_user: User = Depends(get_current_user),
    service: DashboardService = Depends()
):
    """Dashboard de coordinador"""
    if current_user.role != UserRole.COORDINATOR:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return await service.get_coordinator_dashboard(current_user.id)


@router.get("/teacher")
async def get_teacher_dashboard(
    current_user: User = Depends(get_current_user),
    service: DashboardService = Depends()
):
    """Dashboard de profesor"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return await service.get_teacher_dashboard(current_user.id)


@router.get("/student")
async def get_student_dashboard(
    current_user: User = Depends(get_current_user),
    service: DashboardService = Depends()
):
    """Dashboard de estudiante"""
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return await service.get_student_dashboard(current_user.id)
```

**Verificación Día 14:**
```bash
# Login y obtener token
TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -d "username=admin@classsphere.edu&password=secret" | jq -r '.access_token')

# Test dashboards
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/dashboard/admin
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/dashboard/teacher
```

---

### Día 15: ApexCharts Integration - Frontend

**Objetivo:** Integrar ApexCharts 5.3.5 en frontend.

**frontend/package.json (agregar):**
```json
{
  "dependencies": {
    "apexcharts": "^5.3.5",
    "react-apexcharts": "^1.4.1"
  }
}
```

**frontend/src/components/charts/BarChart.tsx**
```typescript
'use client';

import dynamic from 'next/dynamic';
import { ApexOptions } from 'apexcharts';

const Chart = dynamic(() => import('react-apexcharts'), { ssr: false });

interface BarChartProps {
  data: number[];
  categories: string[];
  title: string;
}

export default function BarChart({ data, categories, title }: BarChartProps) {
  const options: ApexOptions = {
    chart: {
      type: 'bar',
      height: 350,
    },
    title: {
      text: title,
      align: 'left',
    },
    xaxis: {
      categories: categories,
    },
  };

  const series = [{
    name: 'Value',
    data: data,
  }];

  return (
    <div className="w-full">
      <Chart options={options} series={series} type="bar" height={350} />
    </div>
  );
}
```

**frontend/src/hooks/useDashboardData.ts**
```typescript
'use client';

import { useQuery } from '@tanstack/react-query';
import { useAuth } from './useAuth';

interface DashboardData {
  [key: string]: any;
}

export function useDashboardData(role: string) {
  const { token } = useAuth();

  return useQuery<DashboardData>({
    queryKey: ['dashboard', role],
    queryFn: async () => {
      const response = await fetch(
        `http://localhost:8000/api/v1/dashboard/${role}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error('Failed to fetch dashboard data');
      }

      return response.json();
    },
    enabled: !!token,
  });
}
```

**frontend/src/components/dashboard/AdminDashboard.tsx**
```typescript
'use client';

import { useDashboardData } from '@/hooks/useDashboardData';
import BarChart from '@/components/charts/BarChart';

export default function AdminDashboard() {
  const { data, isLoading, error } = useDashboardData('admin');

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading dashboard</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Admin Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold">Total Users</h3>
          <p className="text-3xl font-bold">{data?.total_users}</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold">Total Courses</h3>
          <p className="text-3xl font-bold">{data?.total_courses}</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold">Total Students</h3>
          <p className="text-3xl font-bold">{data?.total_students}</p>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <BarChart
          data={[500, 25, 450]}
          categories={['Users', 'Courses', 'Students']}
          title="System Overview"
        />
      </div>
    </div>
  );
}
```

**Verificación Día 15:**
```bash
# Instalar dependencias
cd frontend
npm install

# Tests
npm run test -- AdminDashboard.test.tsx

# Verificar visualmente
npm run dev
# Navegar a http://localhost:3000/dashboard
```

---

### Días 16-22: Resumen de Tareas

**Día 16:** Dashboards TeacherDashboard y StudentDashboard
**Día 17:** Métricas avanzadas backend
**Día 18:** Visualizaciones interactivas frontend
**Día 19:** Modo dual switching (Google/Mock)
**Día 20:** Tests de integración Google API
**Día 21:** Performance optimization y caching
**Día 22:** Documentación y validación completa

---

## ✅ FINAL: Checklist y Próximos Pasos

### Checklist de Verificación Fase 2

**Backend:**
- [ ] Google Classroom Service con mocks
- [ ] Endpoints de dashboard por rol
- [ ] Modo dual funcionando
- [ ] Métricas avanzadas
- [ ] Tests ≥85% coverage

**Frontend:**
- [ ] ApexCharts 5.3.5 integrado
- [ ] Dashboards por rol implementados
- [ ] Visualizaciones interactivas
- [ ] React Query funcionando
- [ ] Tests ≥85% coverage

**Integración:**
- [ ] Dashboards cargan en < 2 segundos
- [ ] Gráficos renderizan correctamente
- [ ] Modo dual switching sin errores
- [ ] Tests E2E pasando

### Comandos de Validación Final

```bash
# Backend
pytest tests/ --cov=src --cov-fail-under=85

# Frontend
npm run test -- --coverage

# E2E dashboards
npm run test:e2e -- dashboard.spec.ts

# Performance
lighthouse http://localhost:3000/dashboard --output=html
```

### Próximos Pasos

**Continuar con Fase 3:**
- [04_plan_fase3_visualizacion.md](04_plan_fase3_visualizacion.md)
- Sistema de búsqueda avanzada
- Notificaciones en tiempo real
- Gráficos interactivos con drill-down

---

[← Fase 1](02_plan_fase1_fundaciones.md) | [Plan Principal](01_plan_index.md) | [Siguiente → Fase 3](04_plan_fase3_visualizacion.md)
