# PROMPT: Análisis Unificado de Plan y Especificaciones ClassSphere

## OBJETIVO PRINCIPAL
Realizar análisis completo de trazabilidad, coherencia, dependencias, patrones, completitud, complejidad, riesgos y calidad para el plan de desarrollo (/contracts/plan/) o las especificaciones (/contracts/principal/).

## PREGUNTA INICIAL
¿Este análisis es para:
1. **Plan de desarrollo** (/contracts/plan/)
2. **Especificaciones** (/contracts/principal/)

Por favor, responde con "plan" o "especificaciones" para proceder.

---

## ANÁLISIS DEL PLAN (/contracts/plan/)

### 3. Análisis de Trazabilidad del Plan
Verificar que cada requisito de las especificaciones esté cubierto en el plan de desarrollo.

**Scope:** `/contracts/plan/` - Prioridad: ALTA - Criterio: ≥95% cobertura

**Pasos clave:**
1. Extraer requisitos de especificaciones
2. Buscar cobertura en plan
3. Identificar gaps

**Comandos de verificación:**
```bash
# Verificar requisitos clave
grep -r "FastAPI 0.104.1\|Next.js 15\|React 19" contracts/plan/
grep -r "JWT\|OAuth 2.0\|Google Classroom" contracts/plan/
grep -r "ApexCharts 5.3.5\|WebSocket\|WCAG 2.2 AA" contracts/plan/
```

### 4. Análisis de Coherencia del Plan
Validar consistencia de términos técnicos en todo el plan.

**Scope:** `/contracts/plan/` - Prioridad: ALTA - Criterio: ≥85% coherencia

**Términos a validar:**
- Versiones: FastAPI 0.104.1, Next.js 15, React 19, Pydantic v2, ApexCharts 5.3.5
- Configuraciones: Puerto 8000, Cobertura ≥80%, Testing Vitest + Playwright
- Metodología: TDD estricto, Cero confianza, WCAG 2.2 AA

### 5. Análisis de Dependencias del Plan
Verificar que dependencias críticas entre fases estén documentadas.

**Dependencias a validar:**
- Fase 2 requiere Fase 1 completada
- Fase 3 requiere Fase 2 completada
- Fase 4 requiere Fase 3 completada

### 6. Análisis de Patrones del Plan
Verificar consistencia de patrones arquitectónicos.

**Patrones a validar:**
1. TDD Estricto (Red-Green-Refactor)
2. Context-Aware Services (Chunking por prioridad)
3. Anti Lost-in-the-Middle (INICIO-MEDIO-FINAL)
4. Cero Confianza (Verificación obligatoria)
5. Logs Estructurados (JSON, /tmp/)

### 7. Análisis de Completitud del Plan
Validar cobertura de funcionalidades en especificaciones.

**Funcionalidades a verificar:**
1. Autenticación y Autorización
2. Google Classroom Integration
3. Dashboards por Rol
4. Visualizaciones Avanzadas
5. Sistema de Búsqueda
6. Notificaciones
7. Métricas y Analytics
8. Accesibilidad
9. Testing
10. CI/CD Pipeline

### 8. Análisis de Complejidad del Plan
Analizar complejidad de instrucciones para ejecutabilidad.

**Métricas:**
- Días totales, Pasos promedio/día, Comandos promedio/paso
- Condicionales por sección, Nivel de anidación
- Umbrales: ≤10 pasos/día, ≤5 comandos/paso, ≤3 condicionales

### 9. Análisis de Riesgos del Plan
Identificar y validar mitigación de riesgos técnicos.

**Riesgos a validar:**
1. Dependencias Externas (Google API)
2. Compatibilidad de Versiones
3. Timeouts de Testing
4. Performance
5. Security Vulnerabilities
6. Context Window Overflow
7. Testing Coverage
8. OAuth Failures

### 10. Análisis de Calidad del Plan
Evaluar calidad global usando métricas objetivas.

**Métricas:**
1. Precisión (≥95%)
2. Completitud (100%)
3. Coherencia (≥85%)
4. Seguridad (100%)
5. Calidad Global (≥90%)

---

## ANÁLISIS DE ESPECIFICACIONES (/contracts/principal/)

### 11. Análisis de Trazabilidad de Especificaciones
Verificar que requisitos estén claramente definidos y trazables.

**Scope:** `/contracts/principal/` - Prioridad: ALTA - Criterio: 100% identificables

### 12. Análisis de Coherencia de Especificaciones
Validar consistencia de términos técnicos.

### 13. Análisis de Dependencias de Especificaciones
Verificar que dependencias estén identificadas.

### 14. Análisis de Patrones de Especificaciones
Verificar definición clara de patrones arquitectónicos.

### 15. Análisis de Completitud de Especificaciones
Verificar cobertura de áreas del sistema.

### 16. Análisis de Complejidad de Especificaciones
Evaluar claridad y simplicidad.

### 17. Análisis de Riesgos de Especificaciones
Verificar identificación de riesgos técnicos.

### 18. Análisis de Calidad de Especificaciones
Evaluar calidad global de especificaciones.

---

## EJECUCIÓN DEL ANÁLISIS

**Basado en tu respuesta:**

**Si respondes "plan":**
- Ejecutar análisis completo del plan usando métricas 3-10
- Usar comandos específicos para `/contracts/plan/`
- Generar resumen ejecutivo con resultados del plan

**Si respondes "especificaciones":**
- Ejecutar análisis completo de especificaciones usando métricas 11-18
- Usar comandos específicos para `/contracts/principal/`
- Generar resumen ejecutivo con resultados de especificaciones

**Comandos generales de verificación (adaptar según respuesta):**
```bash
# Para plan
grep -r "término_buscado" contracts/plan/

# Para especificaciones
grep -r "término_buscado" contracts/principal/

# Contar menciones
echo "Término: $(grep -rc "término" contracts/plan/ | awk -F: '{sum+=$2} END {print sum}')"
```

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

# Resumen Ejecutivo: Análisis Unificado [Plan/Especificaciones]

## 🎯 Objetivo Cumplido
Análisis completo de [trazabilidad/coherencia/dependencias/etc.] para [plan/especificaciones].

## 📊 Resultados Principales

### Métricas de Análisis
- **Trazabilidad:** X% (objetivo: ≥95%)
- **Coherencia:** X% (objetivo: ≥85%)
- **Dependencias:** X% documentadas (objetivo: 100%)
- **Patrones:** X% consistentes (objetivo: ≥80%)
- **Completitud:** X% (objetivo: ≥95%)
- **Complejidad:** [LOW/MEDIUM] (objetivo: ≤MEDIUM)
- **Riesgos:** X/X mitigados (objetivo: 100%)
- **Calidad:** X% (objetivo: ≥90%)

## ⚠️ Hallazgos Críticos
[Detallar gaps o problemas encontrados]

## ✅ Recomendaciones
1. [Acción inmediata]
2. [Acción a corto plazo]
3. [Acción a largo plazo]

## 📈 Estado General
✅ [PASS/NEEDS_IMPROVEMENT] - [Porcentaje] cumplimiento promedio

**Próxima verificación:** Después de próxima actualización
**Frecuencia recomendada:** Después de cambios mayores
