#!/bin/bash
# Context-Aware Tmux Session Management
# Implementa Work Plan Development Rules (LLM 2024-2025)
set -e

# Context Management Functions
init_context_logging() {
    mkdir -p /tmp/dashboard_context
    touch /tmp/dashboard_context_status.json
    touch /tmp/dashboard_tmux_context.log

    # Initial context log (CRITICAL priority)
    cat > /tmp/dashboard_context_status.json << EOF
{
  "timestamp": "$(date -Iseconds)",
  "context_id": "tmux-init-$(date +%s)",
  "token_count": 0,
  "context_priority": "CRITICAL",
  "status": "started",
  "memory_management": {
    "chunk_position": "beginning",
    "lost_in_middle_risk": "low"
  },
  "tmux_phase": "initialization"
}
EOF
}

# Context-Aware Session Creation
create_context_aware_sessions() {
    local PHASE=$1
    local CONTEXT_PRIORITY=$2

    echo "🚀 [CONTEXT-INIT] Creando sesiones tmux para Fase $PHASE (Prioridad: $CONTEXT_PRIORITY)"

    # Backend Session (CRITICAL priority)
    tmux new-session -d -s "edu-dashboard-backend-p$PHASE"
    tmux send-keys -t "edu-dashboard-backend-p$PHASE" "cd backend" Enter
    tmux send-keys -t "edu-dashboard-backend-p$PHASE" "echo '🔧 [BACKEND-$CONTEXT_PRIORITY] Fase $PHASE iniciada'" Enter

    # Frontend Session (HIGH/MEDIUM priority based on phase)
    tmux new-session -d -s "edu-dashboard-frontend-p$PHASE"
    tmux send-keys -t "edu-dashboard-frontend-p$PHASE" "cd frontend" Enter
    tmux send-keys -t "edu-dashboard-frontend-p$PHASE" "echo '⚡ [FRONTEND-$CONTEXT_PRIORITY] Fase $PHASE iniciada'" Enter

    # Context Monitoring Session (LOW priority)
    tmux new-session -d -s "edu-dashboard-context-p$PHASE"
    tmux send-keys -t "edu-dashboard-context-p$PHASE" "echo '📊 [CONTEXT-MONITOR] Fase $PHASE - Monitoring activo'" Enter
    tmux send-keys -t "edu-dashboard-context-p$PHASE" "tail -f /tmp/dashboard_context_status.json" Enter

    # Log context creation
    log_context_status "tmux-sessions-p$PHASE" "$CONTEXT_PRIORITY" "completed" "beginning" "Tmux sessions created for phase $PHASE"
}

# Context Status Logging Function
log_context_status() {
    local context_id=$1
    local priority=$2
    local status=$3
    local position=$4
    local message=$5

    cat >> /tmp/dashboard_context_status.json << EOF
{
  "timestamp": "$(date -Iseconds)",
  "context_id": "$context_id",
  "token_count": ${#message},
  "context_priority": "$priority",
  "status": "$status",
  "memory_management": {
    "chunk_position": "$position",
    "lost_in_middle_risk": "low"
  },
  "component": "tmux_management",
  "message": "$message"
}
EOF
}

# Context-Aware Health Check
verify_context_health() {
    local phase=$1
    local expected_priority=$2

    echo "🔍 [CONTEXT-HEALTH] Verificando salud contextual Fase $phase"

    # Verify tmux sessions exist
    if tmux has-session -t "edu-dashboard-backend-p$phase" 2>/dev/null; then
        echo "✅ [CONTEXT-OK] Backend session Fase $phase activa"
    else
        echo "❌ [CONTEXT-FAIL] Backend session Fase $phase no encontrada"
        log_context_status "health-check-p$phase" "CRITICAL" "failed" "middle" "Backend session missing for phase $phase"
        return 1
    fi

    # Verify context log integrity
    if jq empty /tmp/dashboard_context_status.json 2>/dev/null; then
        echo "✅ [CONTEXT-OK] Context log válido"
    else
        echo "❌ [CONTEXT-FAIL] Context log corrupto"
        log_context_status "health-check-p$phase" "CRITICAL" "failed" "middle" "Context log corrupted"
        return 1
    fi

    # Verify server health for backend phases
    if [ "$phase" -ge 1 ]; then
        if curl -f http://127.0.0.1:8003/health &>/dev/null; then
            echo "✅ [CONTEXT-OK] Backend health check exitoso"
            log_context_status "health-check-p$phase" "$expected_priority" "completed" "middle" "Health check successful for phase $phase"
        else
            echo "❌ [CONTEXT-FAIL] Backend health check falló"
            log_context_status "health-check-p$phase" "CRITICAL" "failed" "middle" "Backend health check failed"
            return 1
        fi
    fi

    return 0
}

# Initialize context logging
init_context_logging

# Create sessions for Phase 1 (CRITICAL Context - Fundaciones)
create_context_aware_sessions "1" "CRITICAL"

# Backend Session Commands (CRITICAL priority)
tmux send-keys -t "edu-dashboard-backend-p1" "python3 -m uvicorn src.app.main:app --host 127.0.0.1 --port 8000 --reload" Enter

# Context Monitoring (chunk position: beginning)
tmux send-keys -t "edu-dashboard-context-p1" "echo 'Context Phase 1: Fundaciones - Token limit 2000'" Enter

# Wait and verify
sleep 5
verify_context_health "1" "CRITICAL"

echo "🎉 [CONTEXT-SUCCESS] Fase 1 Context-Aware setup completado"
echo "📊 [CONTEXT-INFO] Sesiones tmux activas:"
tmux list-sessions | grep "edu-dashboard"