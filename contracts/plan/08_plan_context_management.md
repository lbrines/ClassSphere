---
title: "ClassSphere - Gestión de Contexto LLM"
version: "3.0"
type: "development_plan"
related_files:
  - "contracts/principal/02_ClassSphere_glosario_tecnico.md"
  - "contracts/extra/SOFTWARE_PROJECT_BEST_PRACTICES.md"
---

# Gestión de Contexto LLM - Optimización para Ejecución

## Arquitectura Context-Aware

### Definición
Sistema de gestión de contexto optimizado para ejecución por LLM, implementando chunking por prioridad y estructura anti "lost-in-the-middle".

### Componentes Críticos
- **Chunking por Prioridad**: CRITICAL → HIGH → MEDIUM → LOW
- **Estructura Anti Lost-in-the-Middle**: INICIO-MEDIO-FINAL
- **Logs Estructurados**: JSON con context_id único
- **Context Recovery**: Recuperación automática de contexto perdido

## Chunking por Prioridad

### Reglas de Context Window Management
```yaml
Chunking por Prioridad:
  CRITICAL: máximo 2000 tokens
    - Autenticación, configuración, main.go
    - Dependencias bloqueantes
    - Objetivos críticos
  
  HIGH: máximo 1500 tokens
    - Servicios principales (google_service, classroom_service)
    - Handlers de API críticos
    - Componentes Angular principales
  
  MEDIUM: máximo 1000 tokens
    - Componentes de UI, gráficos
    - Servicios auxiliares
    - Utilidades y helpers
  
  LOW: máximo 800 tokens
    - Páginas de administración
    - Funcionalidades de accesibilidad
    - Documentación y comentarios
```

### Implementación de Chunking
```go
// internal/context/chunking.go
type ContextChunk struct {
    ID          string    `json:"id"`
    Priority    string    `json:"priority"`
    Content     string    `json:"content"`
    TokenCount  int       `json:"token_count"`
    CreatedAt   time.Time `json:"created_at"`
    Dependencies []string `json:"dependencies"`
}

type ContextManager struct {
    chunks map[string]*ContextChunk
    maxTokens map[string]int
}

func NewContextManager() *ContextManager {
    return &ContextManager{
        chunks: make(map[string]*ContextChunk),
        maxTokens: map[string]int{
            "CRITICAL": 2000,
            "HIGH":     1500,
            "MEDIUM":   1000,
            "LOW":      800,
        },
    }
}

func (cm *ContextManager) AddChunk(priority, content string) (*ContextChunk, error) {
    tokenCount := estimateTokens(content)
    maxTokens := cm.maxTokens[priority]
    
    if tokenCount > maxTokens {
        return nil, fmt.Errorf("chunk exceeds maximum tokens for priority %s: %d > %d", priority, tokenCount, maxTokens)
    }
    
    chunk := &ContextChunk{
        ID:         generateChunkID(),
        Priority:   priority,
        Content:    content,
        TokenCount: tokenCount,
        CreatedAt:  time.Now(),
    }
    
    cm.chunks[chunk.ID] = chunk
    return chunk, nil
}
```

## Estructura Anti Lost-in-the-Middle

### Patrón INICIO-MEDIO-FINAL
```markdown
## 🎯 INICIO: Objetivos Críticos y Dependencias Bloqueantes
- Objetivo principal
- Dependencias críticas
- Stack tecnológico
- Criterios de éxito

## 📅 MEDIO: Implementación Detallada
- Pasos específicos
- Comandos de implementación
- TDD examples
- Validaciones

## ✅ FINAL: Checklist y Próximos Pasos
- Criterios de aceptación
- Comandos de verificación
- Métricas de éxito
- Próximos pasos
```

### Implementación del Patrón
```go
// internal/context/structure.go
type DocumentStructure struct {
    Inicio struct {
        Objetivos    []string `json:"objetivos"`
        Dependencias []string `json:"dependencias"`
        Stack        []string `json:"stack"`
    } `json:"inicio"`
    
    Medio struct {
        Pasos        []string `json:"pasos"`
        Comandos     []string `json:"comandos"`
        Ejemplos     []string `json:"ejemplos"`
        Validaciones []string `json:"validaciones"`
    } `json:"medio"`
    
    Final struct {
        Criterios    []string `json:"criterios"`
        Verificacion []string `json:"verificacion"`
        Metricas     []string `json:"metricas"`
        Proximos     []string `json:"proximos"`
    } `json:"final"`
}

func (ds *DocumentStructure) ValidateStructure() error {
    if len(ds.Inicio.Objetivos) == 0 {
        return fmt.Errorf("INICIO section must contain objectives")
    }
    
    if len(ds.Medio.Pasos) == 0 {
        return fmt.Errorf("MEDIO section must contain implementation steps")
    }
    
    if len(ds.Final.Criterios) == 0 {
        return fmt.Errorf("FINAL section must contain acceptance criteria")
    }
    
    return nil
}
```

## Logs Estructurados

### Template Obligatorio
```json
{
  "timestamp": "2025-10-06T16:42:34-03:00",
  "context_id": "ctx_001_phase1_fundaciones",
  "token_count": 1847,
  "context_priority": "CRITICAL",
  "status": "in_progress",
  "memory_management": {
    "chunk_position": "beginning",
    "lost_in_middle_risk": "low",
    "context_window_usage": "67%"
  },
  "operation": {
    "phase": "fase1_fundaciones",
    "step": "backend_go_setup",
    "command": "go mod init github.com/classsphere/backend"
  },
  "performance": {
    "execution_time": "2.3s",
    "memory_usage": "45MB",
    "cpu_usage": "12%"
  }
}
```

### Implementación de Logging
```go
// internal/context/logger.go
type ContextLogger struct {
    contextID string
    priority  string
    startTime time.Time
}

func NewContextLogger(contextID, priority string) *ContextLogger {
    return &ContextLogger{
        contextID: contextID,
        priority:  priority,
        startTime: time.Now(),
    }
}

func (cl *ContextLogger) LogOperation(operation string, step string, command string) {
    logEntry := ContextLogEntry{
        Timestamp:       time.Now().Format(time.RFC3339),
        ContextID:       cl.contextID,
        TokenCount:      estimateCurrentTokens(),
        ContextPriority: cl.priority,
        Status:          "in_progress",
        MemoryManagement: MemoryManagement{
            ChunkPosition:      determineChunkPosition(),
            LostInMiddleRisk:   assessRisk(),
            ContextWindowUsage: calculateUsage(),
        },
        Operation: Operation{
            Phase:   operation,
            Step:    step,
            Command: command,
        },
        Performance: Performance{
            ExecutionTime: time.Since(cl.startTime).Seconds(),
            MemoryUsage:   getMemoryUsage(),
            CPUUsage:      getCPUUsage(),
        },
    }
    
    logJSON(logEntry)
}
```

## Context Recovery

### Estrategias de Recuperación
```go
// internal/context/recovery.go
type ContextRecovery struct {
    checkpoints map[string]*ContextCheckpoint
    lastValidState *ContextState
}

type ContextCheckpoint struct {
    ID        string                 `json:"id"`
    Timestamp time.Time             `json:"timestamp"`
    State     map[string]interface{} `json:"state"`
    Position  string                 `json:"position"`
}

func (cr *ContextRecovery) CreateCheckpoint(contextID string, state map[string]interface{}) {
    checkpoint := &ContextCheckpoint{
        ID:        generateCheckpointID(),
        Timestamp: time.Now(),
        State:     state,
        Position:  "middle",
    }
    
    cr.checkpoints[contextID] = checkpoint
}

func (cr *ContextRecovery) RecoverContext(contextID string) (*ContextState, error) {
    checkpoint, exists := cr.checkpoints[contextID]
    if !exists {
        return nil, fmt.Errorf("no checkpoint found for context %s", contextID)
    }
    
    // Rebuild context from checkpoint
    recoveredState := &ContextState{
        ID:      contextID,
        Chunks:  rebuildChunksFromCheckpoint(checkpoint),
        Position: checkpoint.Position,
    }
    
    return recoveredState, nil
}
```

## Optimización de Memoria

### Gestión Eficiente de Contexto
```go
// internal/context/memory.go
type MemoryManager struct {
    activeContexts map[string]*ContextState
    maxContexts    int
    maxMemory      int64
}

func (mm *MemoryManager) OptimizeMemory() {
    // Remove least recently used contexts
    if len(mm.activeContexts) > mm.maxContexts {
        lruContexts := mm.getLRUContexts()
        for _, contextID := range lruContexts {
            mm.evictContext(contextID)
        }
    }
    
    // Compress context data
    for contextID, context := range mm.activeContexts {
        if context.TokenCount > 1000 {
            compressed := mm.compressContext(context)
            mm.activeContexts[contextID] = compressed
        }
    }
}

func (mm *MemoryManager) CompressContext(context *ContextState) *ContextState {
    // Implement context compression
    compressed := &ContextState{
        ID:         context.ID,
        Priority:   context.Priority,
        Compressed: true,
        Data:       compressData(context.Data),
    }
    
    return compressed
}
```

## Contextual Retrieval Strategies

### RAG Integration
```go
// internal/context/rag.go
type RAGRetriever struct {
    vectorStore VectorStore
    embeddings  EmbeddingService
}

func (rr *RAGRetriever) RetrieveContext(query string, maxResults int) ([]*ContextChunk, error) {
    // Generate embedding for query
    queryEmbedding, err := rr.embeddings.Generate(query)
    if err != nil {
        return nil, err
    }
    
    // Search similar contexts
    similarChunks, err := rr.vectorStore.Search(queryEmbedding, maxResults)
    if err != nil {
        return nil, err
    }
    
    // Rank by relevance and priority
    rankedChunks := rr.rankByRelevanceAndPriority(similarChunks)
    
    return rankedChunks, nil
}

func (rr *RAGRetriever) rankByRelevanceAndPriority(chunks []*ContextChunk) []*ContextChunk {
    // Priority weights
    priorityWeights := map[string]float64{
        "CRITICAL": 1.0,
        "HIGH":     0.8,
        "MEDIUM":   0.6,
        "LOW":      0.4,
    }
    
    // Sort by weighted score
    sort.Slice(chunks, func(i, j int) bool {
        scoreI := chunks[i].RelevanceScore * priorityWeights[chunks[i].Priority]
        scoreJ := chunks[j].RelevanceScore * priorityWeights[chunks[j].Priority]
        return scoreI > scoreJ
    })
    
    return chunks
}
```

## Comandos de Verificación

### Verificación de Contexto
```bash
# Verificar chunking por prioridad
grep -r "CRITICAL\|HIGH\|MEDIUM\|LOW" contracts/plan/ | wc -l

# Verificar estructura anti lost-in-the-middle
for file in contracts/plan/0[2-5]*.md; do
  echo "=== $file ==="
  grep -c "## 🎯 INICIO:" "$file"
  grep -c "## 📅 MEDIO:" "$file"
  grep -c "## ✅ FINAL:" "$file"
done

# Verificar logs estructurados
grep -r "context_id\|token_count" contracts/plan/ | wc -l

# Verificar límites de tokens
for file in contracts/plan/*.md; do
  tokens=$(wc -w < "$file")
  echo "$file: $tokens tokens"
done
```

### Verificación de Performance
```bash
# Verificar uso de memoria
ps aux | grep classsphere-backend | awk '{print $6}'

# Verificar CPU usage
top -p $(pgrep classsphere-backend) -n 1 | tail -1

# Verificar contexto activo
curl -s http://localhost:8081/context/status | jq '.active_contexts'
```

## Métricas de Contexto

### KPIs de Gestión de Contexto
- **Context Window Usage**: ≤80% utilization
- **Lost-in-Middle Risk**: LOW para chunks CRITICAL
- **Context Recovery Time**: <2s
- **Memory Efficiency**: ≤100MB por contexto activo
- **Token Estimation Accuracy**: ±5% error

### Dashboard de Contexto
```typescript
// src/app/components/context/context-dashboard.component.ts
export class ContextDashboardComponent implements OnInit {
  contextMetrics = {
    activeContexts: 5,
    totalTokens: 12500,
    contextWindowUsage: 67,
    lostInMiddleRisk: 'LOW',
    memoryUsage: '85MB',
    avgRecoveryTime: '1.2s'
  };

  ngOnInit() {
    this.loadContextMetrics();
  }

  private loadContextMetrics() {
    this.contextService.getMetrics().subscribe(metrics => {
      this.contextMetrics = metrics;
    });
  }
}
```

## Comandos de Gestión

### Comandos de Contexto
```bash
# Crear nuevo contexto
curl -X POST http://localhost:8081/context/create \
  -H "Content-Type: application/json" \
  -d '{"priority":"CRITICAL","content":"..."}'

# Obtener contexto activo
curl -X GET http://localhost:8081/context/active

# Crear checkpoint
curl -X POST http://localhost:8081/context/checkpoint \
  -H "Content-Type: application/json" \
  -d '{"context_id":"ctx_001","state":{}}'

# Recuperar contexto
curl -X POST http://localhost:8081/context/recover \
  -H "Content-Type: application/json" \
  -d '{"context_id":"ctx_001"}'

# Optimizar memoria
curl -X POST http://localhost:8081/context/optimize
```

**Estado**: ✅ GESTIÓN DE CONTEXTO OPTIMIZADA  
**Arquitectura**: Context-Aware con chunking por prioridad  
**Estructura**: Anti Lost-in-the-Middle implementada  
**Logs**: Estructurados con context_id único  
**Recovery**: Automática con checkpoints  
**Performance**: ≤80% context window usage
