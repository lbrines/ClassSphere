/**
 * Dashboard Educativo - Providers
 * Context-Aware Implementation - Day 5-7 High Priority
 */

'use client';

import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { contextLogger } from '@/utils/context-logger';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 3,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

export const Providers: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  React.useEffect(() => {
    contextLogger.logContextStatus('providers-init-001', 'CRITICAL', 'started', 'middle', 'Providers initialized', 'frontend', 'providers_init');
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};