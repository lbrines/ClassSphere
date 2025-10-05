---
title: "ClassSphere - Gestión de Contexto"
version: "1.0"
type: "context_management"
date: "2025-10-05"
---

# Gestión de Contexto para LLMs

## Chunking por Prioridad

### Límites de Tokens
```yaml
CRITICAL: 2000 tokens  # auth, config, main
HIGH: 1500 tokens      # servicios principales
MEDIUM: 1000 tokens    # componentes, charts
LOW: 800 tokens        # admin, a11y
```

## Estructura Anti Lost-in-the-Middle

### Patrón INICIO-MEDIO-FINAL
```
🎯 INICIO:
- Objetivos críticos
- Dependencias bloqueantes
- Criterios de aceptación

📅 MEDIO:
- Implementación detallada
- Casos de uso
- Ejemplos de código

✅ FINAL:
- Checklist de verificación
- Comandos de validación
- Próximos pasos
```

## Logs Estructurados

### Formato JSON
```json
{
  "timestamp": "2025-10-05T18:00:00Z",
  "context_id": "critical-auth-a1b2c3d4",
  "token_count": 1850,
  "context_priority": "CRITICAL",
  "status": "completed",
  "memory_management": {
    "chunk_position": "beginning",
    "lost_in_middle_risk": "low"
  }
}
```

## Context Recovery

### Recuperación Automática
```bash
# Save context
./scripts/save-context.sh

# Restore context
./scripts/restore-context.sh

# Verify context
./scripts/verify-context.sh
```

## Implementación Context-Aware

### Service Template
```go
type ContextAwareService struct {
    priority   string
    maxTokens  int
    contextID  string
}

func NewContextAwareService(priority string) *ContextAwareService {
    limits := map[string]int{
        "CRITICAL": 2000,
        "HIGH": 1500,
        "MEDIUM": 1000,
        "LOW": 800,
    }
    
    return &ContextAwareService{
        priority:  priority,
        maxTokens: limits[priority],
        contextID: generateContextID(priority),
    }
}
```

## Métricas de Contexto

- **Token usage**: Monitorear uso de tokens
- **Chunk position**: Tracking de posición
- **Lost-in-middle risk**: Evaluación de riesgo
- **Context recovery**: Tasa de recuperación exitosa

---

**Objetivo**: Optimizar uso de contexto para LLMs
