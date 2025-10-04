"use client";

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { contextLogger } from '@/utils/context-logger';

interface AuthGuardProps {
  children: React.ReactNode;
  requireAuth?: boolean;
  redirectTo?: string;
}

export default function AuthGuard({ 
  children, 
  requireAuth = true,
  redirectTo = '/login'
}: AuthGuardProps) {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    const contextId = 'auth-guard-' + Date.now();
    
    contextLogger.logContextStatus(
      contextId,
      'HIGH',
      'started',
      'middle',
      'AuthGuard checking authentication',
      'frontend',
      'auth_check'
    );

    if (!isLoading) {
      if (requireAuth && !user) {
        contextLogger.logContextStatus(
          contextId,
          'HIGH',
          'redirecting',
          'middle',
          'User not authenticated, redirecting to login',
          'frontend',
          'auth_redirect'
        );
        router.push(redirectTo);
      } else if (!requireAuth && user) {
        contextLogger.logContextStatus(
          contextId,
          'HIGH',
          'redirecting',
          'middle',
          'User authenticated, redirecting to dashboard',
          'frontend',
          'auth_redirect'
        );
        router.push('/dashboard');
      }
    }
  }, [user, isLoading, requireAuth, redirectTo, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Cargando...</p>
        </div>
      </div>
    );
  }

  if (requireAuth && !user) {
    return null; // Will redirect
  }

  if (!requireAuth && user) {
    return null; // Will redirect
  }

  return <>{children}</>;
}