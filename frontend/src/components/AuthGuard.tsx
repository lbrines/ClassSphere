/**
 * Dashboard Educativo - Auth Guard Component
 * Context-Aware Implementation - Day 5-7 High Priority
 */

import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { ContextAwareComponent } from './ContextAwareComponent';
import { useAuth } from '@/hooks/useAuth';
import { logComponentContext } from '@/utils/context-logger';

interface AuthGuardProps {
  children: React.ReactNode;
  requireAuth?: boolean;
  redirectTo?: string;
}

export const AuthGuard: React.FC<AuthGuardProps> = ({
  children,
  requireAuth = true,
  redirectTo = '/login'
}) => {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    logComponentContext('auth-guard-001', 'HIGH', 'started', 'Auth guard checking authentication', 'frontend', 'auth_guard_check');

    if (!isLoading) {
      if (requireAuth && !isAuthenticated) {
        logComponentContext('auth-guard-001', 'HIGH', 'failed', 'User not authenticated, redirecting to login', 'frontend', 'auth_guard_redirect');
        router.push(redirectTo);
      } else if (!requireAuth && isAuthenticated) {
        logComponentContext('auth-guard-001', 'HIGH', 'completed', 'User authenticated, redirecting to dashboard', 'frontend', 'auth_guard_redirect');
        router.push('/dashboard');
      } else {
        logComponentContext('auth-guard-001', 'HIGH', 'completed', 'Auth guard check completed successfully', 'frontend', 'auth_guard_check');
      }
    }
  }, [isAuthenticated, isLoading, requireAuth, redirectTo, router]);

  // Show loading state while checking authentication
  if (isLoading) {
    return (
      <ContextAwareComponent contextId="auth-guard-loading-002" priority="HIGH">
        <div className="min-h-screen flex items-center justify-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
        </div>
      </ContextAwareComponent>
    );
  }

  // Don't render children if auth requirements aren't met
  if (requireAuth && !isAuthenticated) {
    return null;
  }

  if (!requireAuth && isAuthenticated) {
    return null;
  }

  return (
    <ContextAwareComponent contextId="auth-guard-001" priority="HIGH">
      {children}
    </ContextAwareComponent>
  );
};