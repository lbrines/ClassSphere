/**
 * Dashboard Educativo - Context Logger Utility
 * Context-Aware Implementation - Day 5-7 High Priority
 */

import { ContextLog } from '@/types';

export class ContextLogger {
  private static instance: ContextLogger;
  private logs: ContextLog[] = [];

  private constructor() {}

  public static getInstance(): ContextLogger {
    if (!ContextLogger.instance) {
      ContextLogger.instance = new ContextLogger();
    }
    return ContextLogger.instance;
  }

  public logContext(
    contextId: string,
    priority: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW',
    status: 'started' | 'in_progress' | 'completed' | 'failed' | 'blocked',
    message: string = '',
    phase?: string,
    task?: string
  ): void {
    const log: ContextLog = {
      timestamp: new Date().toISOString(),
      context_id: contextId,
      token_count: message.length,
      context_priority: priority,
      status,
      memory_management: {
        chunk_position: this.getChunkPosition(priority),
        lost_in_middle_risk: this.getLostInMiddleRisk(priority)
      },
      phase,
      task,
      message
    };

    this.logs.push(log);
    
    // Log to console in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`[CONTEXT-${priority}] ${contextId}: ${message}`, log);
    }
  }

  private getChunkPosition(priority: string): string {
    switch (priority) {
      case 'CRITICAL':
        return 'beginning';
      case 'HIGH':
        return 'beginning-middle';
      case 'MEDIUM':
        return 'middle';
      case 'LOW':
        return 'end';
      default:
        return 'middle';
    }
  }

  private getLostInMiddleRisk(priority: string): string {
    switch (priority) {
      case 'CRITICAL':
      case 'LOW':
        return 'low';
      case 'HIGH':
      case 'MEDIUM':
        return 'medium';
      default:
        return 'medium';
    }
  }

  public getLogs(): ContextLog[] {
    return [...this.logs];
  }

  public getLogsByContextId(contextId: string): ContextLog[] {
    return this.logs.filter(log => log.context_id === contextId);
  }

  public getLogsByPriority(priority: string): ContextLog[] {
    return this.logs.filter(log => log.context_priority === priority);
  }

  public clearLogs(): void {
    this.logs = [];
  }
}

export const contextLogger = ContextLogger.getInstance();

// Convenience functions
export const logComponentContext = (
  contextId: string,
  priority: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW',
  status: 'started' | 'in_progress' | 'completed' | 'failed' | 'blocked',
  message: string = '',
  phase?: string,
  task?: string
) => {
  contextLogger.logContext(contextId, priority, status, message, phase, task);
};