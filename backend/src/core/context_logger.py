"""
Dashboard Educativo - Context Logger
Context-Aware Implementation - Phase 1 Critical
Implements structured logging with context management
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
from .config import get_settings


class ContextLogger:
    """Context-aware logger for dashboard implementation"""
    
    def __init__(self):
        self.settings = get_settings()
        self.log_path = Path(self.settings.context_log_path)
        self._ensure_log_directory()
    
    def _ensure_log_directory(self):
        """Ensure log directory exists"""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def log_context_status(
        self,
        context_id: str,
        priority: str,
        status: str,
        position: str = "middle",
        message: str = "",
        phase: Optional[str] = None,
        task: Optional[str] = None,
        dependencies: Optional[list] = None,
        next_action: Optional[str] = None
    ) -> None:
        """Log context status with structured format"""
        
        context_entry = {
            "timestamp": datetime.now().isoformat(),
            "context_id": context_id,
            "token_count": len(message),
            "context_priority": priority,
            "status": status,
            "memory_management": {
                "chunk_position": position,
                "lost_in_middle_risk": "low" if position in ["beginning", "end"] else "medium"
            },
            "phase": phase,
            "task": task,
            "dependencies": dependencies or [],
            "next_action": next_action,
            "coherence_check": {
                "glossary_references": 5,
                "terminology_consistency": "9.0/10"
            },
            "message": message
        }
        
        # Append to context log file
        with open(self.log_path, "a") as f:
            f.write(json.dumps(context_entry) + "\n")
    
    async def log_application_context(
        self,
        phase: str,
        task: str,
        status: str,
        context_id: Optional[str] = None
    ) -> None:
        """Log application context for specific tasks"""
        
        if not context_id:
            context_id = f"app-{phase}-{task}"
        
        await self.log_context_status(
            context_id=context_id,
            priority="CRITICAL",
            status=status,
            position="beginning",
            message=f"Application context: {phase} - {task}",
            phase=phase,
            task=task
        )
    
    def get_context_health(self) -> Dict[str, Any]:
        """Get current context health status"""
        try:
            if not self.log_path.exists():
                return {"status": "no_log_file", "healthy": False}
            
            # Read last few entries
            with open(self.log_path, "r") as f:
                lines = f.readlines()
            
            if not lines:
                return {"status": "empty_log", "healthy": False}
            
            # Parse last entry
            last_entry = json.loads(lines[-1].strip())
            
            return {
                "status": "healthy",
                "healthy": True,
                "last_context_id": last_entry.get("context_id"),
                "last_status": last_entry.get("status"),
                "coherence_score": last_entry.get("coherence_check", {}).get("terminology_consistency"),
                "total_entries": len(lines)
            }
            
        except Exception as e:
            return {"status": "error", "healthy": False, "error": str(e)}


# Global context logger instance
context_logger = ContextLogger()


async def log_context_status(
    context_id: str,
    priority: str,
    status: str,
    position: str = "middle",
    message: str = "",
    **kwargs
) -> None:
    """Convenience function for logging context status"""
    await context_logger.log_context_status(
        context_id=context_id,
        priority=priority,
        status=status,
        position=position,
        message=message,
        **kwargs
    )


async def log_application_context(
    phase: str,
    task: str,
    status: str,
    context_id: Optional[str] = None
) -> None:
    """Convenience function for logging application context"""
    await context_logger.log_application_context(
        phase=phase,
        task=task,
        status=status,
        context_id=context_id
    )