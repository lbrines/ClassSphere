"use client";

import { useEffect } from 'react';
import { contextLogger } from '@/utils/context-logger';

interface ContextAwareComponentProps {
  children: React.ReactNode;
  contextId?: string;
  componentName?: string;
}

export default function ContextAwareComponent({ 
  children, 
  contextId = 'default-context',
  componentName = 'ContextAwareComponent'
}: ContextAwareComponentProps) {
  
  useEffect(() => {
    // Log component mount
    contextLogger.logContextStatus(
      contextId,
      'MEDIUM',
      'started',
      'middle',
      `${componentName} mounted`,
      'frontend',
      'component_mount'
    );

    // Log component unmount
    return () => {
      contextLogger.logContextStatus(
        contextId,
        'MEDIUM',
        'completed',
        'middle',
        `${componentName} unmounted`,
        'frontend',
        'component_unmount'
      );
    };
  }, [contextId, componentName]);

  return <>{children}</>;
}