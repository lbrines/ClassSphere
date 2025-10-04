/**
 * Dashboard Educativo - Dashboard Page
 * Context-Aware Implementation - Day 5-7 High Priority
 */

'use client';

import React from 'react';
import { ContextAwareComponent } from '@/components/ContextAwareComponent';
import { AuthGuard } from '@/components/AuthGuard';
import { useAuth } from '@/hooks/useAuth';
import { logComponentContext } from '@/utils/context-logger';

export default function DashboardPage() {
  const { user } = useAuth();

  React.useEffect(() => {
    logComponentContext('dashboard-page-001', 'HIGH', 'started', 'Dashboard page loaded', 'frontend', 'dashboard_page_load');
  }, []);

  return (
    <AuthGuard requireAuth={true}>
      <ContextAwareComponent contextId="dashboard-page-001" priority="HIGH">
        <div className="min-h-screen bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="py-6">
              <div className="mb-8">
                <h1 className="text-3xl font-bold text-gray-900">
                  Dashboard Educativo
                </h1>
                <p className="mt-2 text-gray-600">
                  Bienvenido, {user?.name || user?.username}
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div className="card">
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    Cursos
                  </h3>
                  <p className="text-gray-600">
                    Gestiona tus cursos de Google Classroom
                  </p>
                </div>

                <div className="card">
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    Estudiantes
                  </h3>
                  <p className="text-gray-600">
                    Visualiza información de tus estudiantes
                  </p>
                </div>

                <div className="card">
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    Métricas
                  </h3>
                  <p className="text-gray-600">
                    Analiza el rendimiento educativo
                  </p>
                </div>
              </div>

              <div className="mt-8">
                <div className="card">
                  <h3 className="text-lg font-medium text-gray-900 mb-4">
                    Estado del Sistema
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="flex items-center">
                      <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
                      <span className="text-gray-700">Backend conectado</span>
                    </div>
                    <div className="flex items-center">
                      <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
                      <span className="text-gray-700">Google Classroom integrado</span>
                    </div>
                    <div className="flex items-center">
                      <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
                      <span className="text-gray-700">Context logging activo</span>
                    </div>
                    <div className="flex items-center">
                      <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
                      <span className="text-gray-700">Autenticación dual funcionando</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </ContextAwareComponent>
    </AuthGuard>
  );
}