---
title: "ClassSphere - Gestión de Contexto para LLMs"
version: "1.0"
type: "strategy_document"
context_priority: "HIGH"
date: "2025-10-05"
---

[← Plan Principal](01_plan_index.md)

# Gestión de Contexto para LLMs

## Arquitectura Context-Aware

### Chunking por Prioridad

**Límites de tokens por prioridad:**
```yaml
CRITICAL: 2000 tokens máximo
  - Autenticación (JWT, OAuth)
  - Configuración base (config.py, main.py)
  - Health checks y endpoints críticos

HIGH: 1500 tokens máximo
  - Servicios Google Classroom
  - Integraciones principales
  - Middleware de seguridad

MEDIUM: 1000 tokens máximo
  - Componentes UI
  - Visualizaciones con ApexCharts
  - Dashboards por rol

LOW: 800 tokens máximo
  - Panel de administración
  - Accesibilidad WCAG 2.2 AA
  - Documentación complementaria
```

### Implementación en Servicios

**backend/src/app/core/context_aware.py**
```python
"""
Servicios con gestión de contexto
"""
from uuid import uuid4
from datetime import datetime
import json
from typing import Literal


ContextPriority = Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"]


class ContextAwareService:
    """Servicio con gestión de contexto según prioridad"""
    
    def __init__(self, priority: ContextPriority = "MEDIUM"):
        self.priority = priority
        self.max_tokens = self._get_max_tokens(priority)
        self.context_id = f"{priority.lower()}-{uuid4().hex[:8]}"
    
    def _get_max_tokens(self, priority: ContextPriority) -> int:
        """Límites de tokens según prioridad"""
        limits = {
            "CRITICAL": 2000,
            "HIGH": 1500,
            "MEDIUM": 1000,
            "LOW": 800
        }
        return limits.get(priority, 1000)
    
    async def log_context_status(
        self,
        status: str,
        token_count: int = 0,
        chunk_position: str = "middle",
        risk: str = "low"
    ):
        """Log estructurado según template obligatorio"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "context_id": self.context_id,
            "token_count": token_count,
            "context_priority": self.priority,
            "status": status,
            "memory_management": {
                "chunk_position": chunk_position,
                "lost_in_middle_risk": risk
            }
        }
        
        # Log a archivo temporal para tracking LLM
        with open("/tmp/classsphere_context_status.json", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
```

## Estructura Anti Lost-in-the-Middle

### Patrón Obligatorio para Documentos

**Estructura de 3 secciones:**
```markdown
## 🎯 INICIO: Objetivos Críticos (Primacy Bias)
- Objetivos principales
- Dependencias bloqueantes
- Comandos de verificación inmediata
- Context management info

## 📅 MEDIO: Implementación Detallada
- Paso a paso específico
- Código de ejemplo
- Casos de uso
- Comandos de ejecución

## ✅ FINAL: Checklist y Próximos Pasos (Recency Bias)
- Checklist de verificación
- Comandos de validación
- Próximos pasos
- Referencias a otros documentos
```

### Implementación en Código

**backend/src/app/services/anti_lost_middle.py**
```python
"""
Servicio estructurado para prevenir pérdida de contexto
"""
from typing import Dict, List, Any


class AntiLostInMiddleService:
    """Servicio con estructura anti lost-in-the-middle"""
    
    async def execute_with_context_priority(
        self,
        task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Estructura Anti Lost-in-the-Middle:
        - inicio: objetivos críticos + dependencias bloqueantes
        - medio: implementación detallada + casos de uso
        - final: checklist verificación + próximos pasos
        """
        
        # INICIO (primacy bias): información crítica
        critical_objectives = task_data.get("critical_objectives", [])
        blocking_dependencies = task_data.get("blocking_dependencies", [])
        
        await self._log_context_status(
            "started",
            chunk_position="beginning",
            risk="low",
            token_count=len(str(critical_objectives))
        )
        
        # MEDIO: implementación detallada (riesgo de pérdida)
        detailed_implementation = task_data.get("implementation", {})
        use_cases = task_data.get("use_cases", [])
        
        await self._log_context_status(
            "in_progress",
            chunk_position="middle",
            risk="medium",
            token_count=len(str(detailed_implementation))
        )
        
        # FINAL (recency bias): próximos pasos críticos
        verification_checklist = task_data.get("verification", [])
        next_steps = task_data.get("next_steps", [])
        
        await self._log_context_status(
            "completed",
            chunk_position="end",
            risk="low",
            token_count=len(str(verification_checklist))
        )
        
        return {
            "critical_processed": critical_objectives,
            "next_actions": next_steps,
            "verification_required": verification_checklist
        }
```

## Logs Estructurados Obligatorios

### Template de Log JSON

```json
{
  "timestamp": "2025-10-05T07:03:25-03:00",
  "context_id": "critical-a1b2c3d4",
  "token_count": 1850,
  "context_priority": "CRITICAL",
  "status": "in_progress",
  "memory_management": {
    "chunk_position": "beginning",
    "lost_in_middle_risk": "low"
  }
}
```

### Ubicación de Logs

```bash
# Estado general del proyecto
/tmp/classsphere_status.json

# Gestión de contexto
/tmp/classsphere_context_status.json

# Logs de sesiones tmux
/tmp/classsphere_tmux_status.log

# Context específico de frontend
/tmp/classsphere_frontend_context.json
```

### Script de Actualización de Logs

**scripts/update_context_status.sh**
```bash
#!/bin/bash
# Script para actualizar logs de contexto

TIMESTAMP=$(date -Iseconds)
CONTEXT_ID="${1:-unknown}"
TOKEN_COUNT="${2:-0}"
PRIORITY="${3:-MEDIUM}"
STATUS="${4:-in_progress}"

cat >> /tmp/classsphere_context_status.json << EOF
{
  "timestamp": "$TIMESTAMP",
  "context_id": "$CONTEXT_ID",
  "token_count": $TOKEN_COUNT,
  "context_priority": "$PRIORITY",
  "status": "$STATUS",
  "memory_management": {
    "chunk_position": "middle",
    "lost_in_middle_risk": "low"
  }
}
EOF

echo "✅ Context status updated: $CONTEXT_ID"
```

## Sistema de Logging de Control de Status

### Archivo Principal de Status

**Actualización automática en cada fase:**
```json
{
  "project": "ClassSphere",
  "version": "2.6",
  "phase": "fase_1",
  "day": "dia_3",
  "status": "in_progress",
  "last_updated": "2025-10-05T07:03:25-03:00",
  "tests_passed": 78,
  "coverage_percentage": 100,
  "health_endpoint": "http://localhost:8000/health",
  "server_running": true,
  "quality_gates": {
    "day_1": "completed",
    "day_2": "completed",
    "day_3": "in_progress"
  },
  "next_tasks": [
    "Implementar OAuth 2.0",
    "Crear sistema de roles"
  ],
  "errors": [],
  "warnings": [],
  "context_management": {
    "current_context_id": "critical-a1b2c3d4",
    "token_count": 1850,
    "context_priority": "CRITICAL",
    "chunk_position": "beginning",
    "lost_in_middle_risk": "low",
    "chunking_strategy": "priority_based",
    "anti_lost_middle_structure": "applied"
  },
  "tmux_sessions": {
    "active_sessions": ["tdd-dev", "classsphere-frontend"],
    "context_monitoring": true,
    "health_checks": ["backend:8000", "frontend:3000"]
  }
}
```

### Script de Actualización

**scripts/update_status.py**
```python
#!/usr/bin/env python3
"""
Script para actualizar status del proyecto
"""
import json
from datetime import datetime
from pathlib import Path


def update_status(
    phase: str,
    day: str,
    status: str,
    tests_passed: int = 0,
    coverage: int = 0
):
    """Actualizar archivo de status"""
    status_file = Path("/tmp/classsphere_status.json")
    
    status_data = {
        "project": "ClassSphere",
        "version": "2.6",
        "phase": phase,
        "day": day,
        "status": status,
        "last_updated": datetime.now().isoformat(),
        "tests_passed": tests_passed,
        "coverage_percentage": coverage,
        "health_endpoint": "http://localhost:8000/health",
        "server_running": True,
        "context_management": {
            "current_context_id": f"{phase}-{day}",
            "token_count": 0,
            "context_priority": "HIGH",
            "chunk_position": "middle",
            "lost_in_middle_risk": "low"
        }
    }
    
    with open(status_file, "w") as f:
        json.dump(status_data, f, indent=2)
    
    print(f"✅ Status updated: {phase} - {day} - {status}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 4:
        update_status(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage: update_status.py <phase> <day> <status>")
```

## Integración con Tmux

### Script de Monitoreo Tmux

**scripts/tmux_context_monitor.sh**
```bash
#!/bin/bash
# Monitoreo de contexto en sesiones tmux

SESSION_NAME="${1:-classsphere-dev}"
LOG_FILE="/tmp/classsphere_tmux_status.log"

# Función de logging
log_tmux_status() {
    local timestamp=$(date -Iseconds)
    local session_status=$(tmux has-session -t "$SESSION_NAME" 2>/dev/null && echo "active" || echo "inactive")
    
    echo "$timestamp | SESSION: $SESSION_NAME | STATUS: $session_status" >> "$LOG_FILE"
}

# Monitoreo continuo
while true; do
    log_tmux_status
    sleep 60  # Log cada minuto
done
```

### Configuración Tmux

**~/.tmux.conf (agregar)**
```bash
# Status bar con context info
set -g status-right '#[fg=green]#(cat /tmp/classsphere_status.json | jq -r .phase) #[fg=yellow]#(cat /tmp/classsphere_status.json | jq -r .day)'

# Auto-logging
set-hook -g session-created 'run-shell "echo Session created >> /tmp/classsphere_tmux_status.log"'
set-hook -g session-closed 'run-shell "echo Session closed >> /tmp/classsphere_tmux_status.log"'
```

## Context Recovery

### Script de Recuperación de Contexto

**scripts/recover_context.py**
```python
#!/usr/bin/env python3
"""
Recuperar contexto desde point-in-time específico
"""
import json
from datetime import datetime
from pathlib import Path


def recover_context(timestamp: str = None):
    """Recuperar contexto desde timestamp"""
    context_file = Path("/tmp/classsphere_context_status.json")
    
    if not context_file.exists():
        print("❌ No context file found")
        return None
    
    contexts = []
    with open(context_file, "r") as f:
        for line in f:
            try:
                contexts.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    
    if timestamp:
        # Buscar contexto más cercano al timestamp
        target = datetime.fromisoformat(timestamp)
        closest = min(
            contexts,
            key=lambda x: abs(
                datetime.fromisoformat(x["timestamp"]) - target
            )
        )
        return closest
    else:
        # Retornar último contexto
        return contexts[-1] if contexts else None


if __name__ == "__main__":
    import sys
    timestamp = sys.argv[1] if len(sys.argv) > 1 else None
    context = recover_context(timestamp)
    
    if context:
        print("✅ Context recovered:")
        print(json.dumps(context, indent=2))
    else:
        print("❌ No context found")
```

## Validación de Context Management

### Checklist de Validación

```bash
# 1. Verificar archivos de log existen
ls -la /tmp/classsphere_*.json

# 2. Verificar estructura de logs
cat /tmp/classsphere_context_status.json | jq '.'

# 3. Verificar chunking por prioridad
grep -c "CRITICAL" /tmp/classsphere_context_status.json
grep -c "HIGH" /tmp/classsphere_context_status.json

# 4. Verificar anti lost-in-middle
grep -c "beginning" /tmp/classsphere_context_status.json
grep -c "end" /tmp/classsphere_context_status.json

# 5. Verificar token counts
cat /tmp/classsphere_context_status.json | jq '.token_count'
```

### Comandos de Monitoreo

```bash
# Watch status en tiempo real
watch -n 5 'cat /tmp/classsphere_status.json | jq .'

# Tail de context logs
tail -f /tmp/classsphere_context_status.json | jq '.'

# Análisis de token usage
cat /tmp/classsphere_context_status.json | \
  jq -r '.token_count' | \
  awk '{sum+=$1; count++} END {print "Avg tokens:", sum/count}'
```

---

[← Plan Principal](01_plan_index.md)
