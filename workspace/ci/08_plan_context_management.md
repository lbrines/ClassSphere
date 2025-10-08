---
id: "08"
title: "Context Management for LLMs"
version: "4.0"
type: "support"
date: "2025-10-07"
---

# Context Management - LLM Optimization

## Chunking by Priority

### Token Budgets
- **CRITICAL**: 2000 tokens max (Phase 1, security, blocking dependencies)
- **HIGH**: 1500 tokens max (Phase 2, Google API integration)
- **MEDIUM**: 1000 tokens max (Phase 3, visualization)
- **LOW**: 800 tokens max (Phase 4, final integration)

### Priority Assignment Rules
1. **CRITICAL**: Foundation, authentication, security, error prevention
2. **HIGH**: Core business logic, external integrations
3. **MEDIUM**: Advanced features, UI/UX enhancements
4. **LOW**: Nice-to-have features, final polish

## Anti Lost-in-the-Middle Structure

### Document Template
```
## 🎯 INICIO (Beginning)
- Critical objectives
- Blocking dependencies
- Success criteria

## 📅 MEDIO (Middle)
- Detailed implementation steps
- Code examples
- Day-by-day plan

## ✅ FINAL (End)
- Verification checklist
- Acceptance criteria validation
- Next steps
```

### Why This Works
- **Beginning**: LLMs have strong recall for document start
- **Middle**: Detailed content with context anchors
- **End**: LLMs have strong recall for document end

## Context Tracking

### Log Structure
```json
{
  "timestamp": "2025-10-07T10:30:00Z",
  "context_id": "ctx-20251007-001",
  "token_count": 1500,
  "priority": "CRITICAL",
  "chunk_position": "middle",
  "lost_in_middle_risk": "low",
  "phase": "phase_1",
  "day": "day_3"
}
```

### Tmux Session Management
```bash
# Create persistent session
tmux new-session -s classsphere-dev

# Attach to existing
tmux attach-session -t classsphere-dev

# Context logging in session
echo "$(date -Iseconds) | Phase 1 | Day 3 | Backend JWT" >> /tmp/classsphere_context.log
```

## Context Recovery

### Point-in-Time Recovery
```bash
# View context history
tail -100 /tmp/classsphere_context.log

# Find specific phase
grep "Phase 2" /tmp/classsphere_context.log

# Resume from checkpoint
cat /tmp/classsphere_status.json
```

### Status File Format
```json
{
  "project": "ClassSphere",
  "version": "4.0",
  "phase": "phase_2",
  "day": "day_15",
  "status": "in_progress",
  "last_updated": "2025-10-07 15:30:00",
  "tests_passed": 145,
  "coverage_percentage": 87.3,
  "next_tasks": [
    "Implement dashboard endpoint",
    "Add role-based filtering"
  ],
  "context_management": {
    "current_context_id": "ctx-20251007-015",
    "token_count": 1200,
    "chunk_position": "middle"
  }
}
```

## Best Practices

### 1. Frequent Context Checkpoints
- Save context every 30 minutes
- Update status file after each task
- Log phase/day transitions

### 2. Clear Task Boundaries
- One task per context chunk
- Explicit start/end markers
- Acceptance criteria per task

### 3. Minimize Context Switching
- Complete phase before moving to next
- Batch related tasks
- Avoid jumping between unrelated features

### 4. Context Prioritization
- Critical information first and last
- Supporting details in middle
- Repetition of key concepts

## Verification

### Context Quality Metrics
- **Coherence**: Terms consistent across documents (target: ≥85%)
- **Completeness**: All required info present (target: 100%)
- **Precision**: No hallucinated or incorrect info (target: ≥95%)

### Validation Commands
```bash
# Check document structure
for file in workspace/ci/0[2-5]*.md; do
  grep -c "## 🎯 INICIO:" "$file"
  grep -c "## 📅 MEDIO:" "$file"
  grep -c "## ✅ FINAL:" "$file"
done

# Verify token budgets (approximate)
wc -w workspace/ci/02*.md  # Should be ~1500 words (~2000 tokens)
```

---

**Reference**: Based on LLM context management best practices (2024-2025 papers).

