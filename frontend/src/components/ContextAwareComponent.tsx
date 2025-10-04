/**
 * Dashboard Educativo - Context Aware Component
 * Context-Aware Implementation - Day 5-7 High Priority
 */

import React, { useEffect } from 'react';
import { ContextAwareComponentProps } from '@/types';
import { logComponentContext } from '@/utils/context-logger';

export const ContextAwareComponent: React.FC<ContextAwareComponentProps> = ({
  contextId,
  priority,
  children
}) => {
  useEffect(() => {
    // Log component context when mounted
    logComponentContext(contextId, priority, 'started', 'Component mounted', 'frontend', 'component_mount');
    
    return () => {
      // Log component context when unmounted
      logComponentContext(contextId, priority, 'completed', 'Component unmounted', 'frontend', 'component_unmount');
    };
  }, [contextId, priority]);

  return (
    <div 
      data-context-id={contextId}
      data-context-priority={priority}
      className="context-aware-component"
    >
      {children}
    </div>
  );
};