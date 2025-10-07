---
id: "08"
title: "Context Management for LLMs"
priority: "HIGH"
version: "1.0"
date: "2025-10-07"
---

# Context Management for LLMs

## Overview

Context management is critical for LLM-driven development. This document defines strategies to optimize context usage and prevent information loss.

## Chunking by Priority

### Token Limits per Priority Level
```yaml
CRITICAL: max 2000 tokens
  - Authentication services
  - Configuration files
  - Main entry points (main.go, main.ts)
  - Security-critical components

HIGH: max 1500 tokens
  - Core business services
  - API integrations
  - Database repositories
  - Middleware components

MEDIUM: max 1000 tokens
  - UI components
  - Visualization services
  - Search functionality
  - Notification services

LOW: max 800 tokens
  - Admin utilities
  - Accessibility components
  - Documentation
  - Helper utilities
```

### Priority Assignment Rules
1. **Security components** → CRITICAL
2. **Core business logic** → HIGH
3. **User-facing features** → MEDIUM
4. **Administrative tools** → LOW

## Anti Lost-in-the-Middle Structure

### Document Structure Template
```markdown
## 🎯 INICIO: CRITICAL INFORMATION
- Objectives
- Blocking dependencies
- Success criteria

## 📅 MEDIO: DETAILED IMPLEMENTATION
- Step-by-step instructions
- Code examples
- Configuration details

## ✅ FINAL: VERIFICATION AND NEXT STEPS
- Acceptance criteria
- Validation commands
- Next steps
```

### Why This Structure Works
- **Beginning (INICIO)**: LLMs have strong attention at start
- **Middle (MEDIO)**: Detailed content in middle, less critical
- **End (FINAL)**: LLMs have strong attention at end
- Prevents "lost-in-the-middle" phenomenon where middle content gets ignored

## Context-Aware Logging

### Log Structure
```json
{
  "timestamp": "2025-10-07T10:30:00Z",
  "context_id": "phase1-day3-auth",
  "token_count": 1847,
  "context_priority": "CRITICAL",
  "chunk_position": "middle",
  "lost_in_middle_risk": "low",
  "phase": "Phase 1: Fundaciones",
  "day": "Day 3",
  "component": "OAuth 2.0 Google",
  "status": "in_progress",
  "tests_passed": 45,
  "coverage": 82.3,
  "next_tasks": [
    "Complete OAuth callback handler",
    "Add state validation",
    "Test OAuth flow end-to-end"
  ]
}
```

### Log Locations
```bash
# Development logs
/tmp/classsphere_status.json

# Context tracking
/tmp/classsphere_context_status.json

# tmux session logs
/tmp/classsphere_tmux_status.log

# Frontend context
/tmp/classsphere_frontend_context.json
```

## Context Recovery

### Point-in-Time Recovery
```bash
# Save context checkpoint
cat > /tmp/classsphere_checkpoint_day3.json << EOF
{
  "phase": "Phase 1",
  "day": "Day 3",
  "completed": [
    "Backend Go setup",
    "JWT authentication",
    "User repository"
  ],
  "in_progress": "OAuth 2.0 Google integration",
  "next": "OAuth callback handler"
}
EOF

# Restore from checkpoint
cat /tmp/classsphere_checkpoint_day3.json
```

### Context Refresh Protocol
When context window fills:
1. **Summarize** completed work
2. **Save** current state to checkpoint
3. **List** pending tasks
4. **Continue** with fresh context

## Token Management

### Token Counting
```go
// internal/shared/context_manager.go
package shared

import "strings"

func CountTokens(text string) int {
    // Rough estimation: 1 token ≈ 4 characters
    return len(text) / 4
}

func ValidateChunkSize(content string, priority string) error {
    tokens := CountTokens(content)
    limits := map[string]int{
        "CRITICAL": 2000,
        "HIGH":     1500,
        "MEDIUM":   1000,
        "LOW":      800,
    }
    
    if tokens > limits[priority] {
        return fmt.Errorf("chunk exceeds %d tokens for priority %s", limits[priority], priority)
    }
    
    return nil
}
```

### Monitoring Token Usage
```typescript
// src/app/core/services/context-monitor.service.ts
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class ContextMonitorService {
  private readonly TOKEN_LIMIT = 100000;
  private currentTokens = 0;
  
  trackTokenUsage(content: string): void {
    // Rough estimation: 1 token ≈ 4 characters
    const tokens = Math.ceil(content.length / 4);
    this.currentTokens += tokens;
    
    if (this.currentTokens > this.TOKEN_LIMIT * 0.8) {
      console.warn('Context window 80% full. Consider summarizing.');
    }
  }
  
  reset(): void {
    this.currentTokens = 0;
  }
}
```

## Tmux Integration

### Tmux Session Management
```bash
#!/bin/bash
# scripts/tmux-setup.sh

SESSION_NAME="classsphere-dev"

# Create tmux session with context logging
tmux new-session -d -s $SESSION_NAME

# Window 1: Backend
tmux rename-window -t $SESSION_NAME:1 'backend'
tmux send-keys -t $SESSION_NAME:1 'cd /backend' C-m
tmux send-keys -t $SESSION_NAME:1 'echo "Backend context initialized" | tee -a /tmp/classsphere_tmux_status.log' C-m

# Window 2: Frontend
tmux new-window -t $SESSION_NAME:2 -n 'frontend'
tmux send-keys -t $SESSION_NAME:2 'cd /frontend' C-m
tmux send-keys -t $SESSION_NAME:2 'echo "Frontend context initialized" | tee -a /tmp/classsphere_tmux_status.log' C-m

# Window 3: Tests
tmux new-window -t $SESSION_NAME:3 -n 'tests'
tmux send-keys -t $SESSION_NAME:3 'echo "Test runner ready" | tee -a /tmp/classsphere_tmux_status.log' C-m

# Attach to session
tmux attach-session -t $SESSION_NAME
```

### Context Logging in Tmux
```bash
# Add to ~/.tmux.conf
set-option -g history-limit 50000
set-option -g status-right "#(cat /tmp/classsphere_status.json | jq -r .status)"

# Log all output
tmux pipe-pane -o 'cat >> /tmp/classsphere_tmux_status.log'
```

## Context Best Practices

### 1. Prioritize Critical Information
- Always start with critical objectives
- End with verification steps
- Place detailed implementation in middle

### 2. Use Structured Formats
- JSON for logs (machine-readable)
- Markdown for documentation (human-readable)
- YAML for configuration (both readable)

### 3. Regular Checkpoints
- Save context every major milestone
- Document completed tasks
- List pending tasks clearly

### 4. Avoid Context Pollution
- Remove unnecessary details
- Summarize verbose output
- Focus on actionable information

### 5. Monitor Context Usage
- Track token counts
- Watch for 80% threshold
- Prepare summaries proactively

## Context Recovery Scripts

### Save Current Context
```bash
#!/bin/bash
# scripts/save-context.sh

CONTEXT_FILE="/tmp/classsphere_checkpoint_$(date +%Y%m%d_%H%M%S).json"

cat > $CONTEXT_FILE << EOF
{
  "timestamp": "$(date -Iseconds)",
  "phase": "$(grep -oP 'phase":\s*"\K[^"]+' /tmp/classsphere_status.json)",
  "day": "$(grep -oP 'day":\s*"\K[^"]+' /tmp/classsphere_status.json)",
  "git_commit": "$(git rev-parse HEAD)",
  "tests_status": "$(go test ./... 2>&1 | tail -n 1)",
  "coverage": "$(go test ./... -cover 2>&1 | grep -oP 'coverage: \K[0-9.]+' | head -n 1)"
}
EOF

echo "Context saved to $CONTEXT_FILE"
```

### Restore Context
```bash
#!/bin/bash
# scripts/restore-context.sh

if [ -z "$1" ]; then
  echo "Usage: ./restore-context.sh <checkpoint_file>"
  exit 1
fi

CHECKPOINT_FILE="$1"

if [ ! -f "$CHECKPOINT_FILE" ]; then
  echo "Checkpoint file not found: $CHECKPOINT_FILE"
  exit 1
fi

echo "Restoring context from $CHECKPOINT_FILE"
cat $CHECKPOINT_FILE | jq .

# Restore git commit
GIT_COMMIT=$(jq -r .git_commit $CHECKPOINT_FILE)
echo "Git commit: $GIT_COMMIT"

# Show phase and day
PHASE=$(jq -r .phase $CHECKPOINT_FILE)
DAY=$(jq -r .day $CHECKPOINT_FILE)
echo "Phase: $PHASE, Day: $DAY"

# Show test status
TEST_STATUS=$(jq -r .tests_status $CHECKPOINT_FILE)
echo "Tests: $TEST_STATUS"
```

## Validation

### Context Structure Validation
```bash
# Check if all phase files follow structure
for file in workspace/plan/*.md; do
  echo "Checking $file"
  grep -q "🎯 INICIO" "$file" && echo "✅ Has INICIO" || echo "❌ Missing INICIO"
  grep -q "📅 MEDIO" "$file" && echo "✅ Has MEDIO" || echo "❌ Missing MEDIO"
  grep -q "✅ FINAL" "$file" && echo "✅ Has FINAL" || echo "❌ Missing FINAL"
done
```

### Token Count Validation
```bash
# Verify token limits per priority
for file in workspace/plan/*.md; do
  PRIORITY=$(grep -oP 'priority:\s*"\K[^"]+' "$file")
  TOKEN_COUNT=$(($(wc -c < "$file") / 4))
  
  case $PRIORITY in
    CRITICAL) LIMIT=2000 ;;
    HIGH) LIMIT=1500 ;;
    MEDIUM) LIMIT=1000 ;;
    LOW) LIMIT=800 ;;
    *) LIMIT=2000 ;;
  esac
  
  if [ $TOKEN_COUNT -le $LIMIT ]; then
    echo "✅ $file: $TOKEN_COUNT tokens (limit $LIMIT)"
  else
    echo "❌ $file: $TOKEN_COUNT tokens exceeds limit $LIMIT"
  fi
done
```

---

**Last updated**: 2025-10-07  
**Context management enables efficient LLM-driven development.**

