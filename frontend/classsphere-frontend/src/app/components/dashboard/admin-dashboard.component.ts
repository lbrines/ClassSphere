import { Component, OnInit, signal, computed, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BaseDashboardComponent } from './base-dashboard.component';
import { AuthService } from '../../services/auth.service';
import { DashboardService } from '../../services/dashboard.service';
import { Router } from '@angular/router';
import { ExportPanelComponent } from '../export/export-panel.component';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [CommonModule, ExportPanelComponent],
  template: `
    <div #dashboardContainer class="px-4 py-6 sm:px-0">
      <!-- Admin Welcome Message -->
      <div class="bg-white overflow-hidden shadow rounded-lg mb-6">
        <div class="px-4 py-5 sm:p-6">
          <h2 class="text-2xl font-bold text-gray-900 mb-2">
            Panel de Administración del Sistema
          </h2>
          <p class="text-gray-600">
            Última actualización: {{ formatDate(dashboardData()?.timestamp) }}
          </p>
        </div>
      </div>

      <!-- System Overview Stats -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        @for (stat of getSystemStats(); track stat.key) {
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 rounded-md flex items-center justify-center"
                       [class]="getStatIconClass(stat.key)">
                    <span class="text-white text-sm font-medium">{{ stat.value }}</span>
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">
                      {{ stat.label }}
                    </dt>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        }
      </div>

      <!-- System Health & Performance -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- System Health -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
              Estado del Sistema
            </h3>
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Tiempo de Actividad</span>
                <span class="text-sm font-medium text-green-600">99.9%</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Conexiones Activas</span>
                <span class="text-sm font-medium text-blue-600">{{ getActiveConnections() }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Uso de Memoria</span>
                <span class="text-sm font-medium text-yellow-600">45%</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Espacio en Disco</span>
                <span class="text-sm font-medium text-green-600">78%</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Google Integration Status -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
              Integración Google Classroom
            </h3>
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Estado de Conexión</span>
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  Conectado
                </span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Última Sincronización</span>
                <span class="text-sm font-medium text-gray-900">Hace 5 min</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Cursos Sincronizados</span>
                <span class="text-sm font-medium text-blue-600">{{ getSyncedCourses() }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Estudiantes Sincronizados</span>
                <span class="text-sm font-medium text-blue-600">{{ getSyncedStudents() }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- User Management -->
      <div class="bg-white shadow rounded-lg mb-6">
        <div class="px-4 py-5 sm:p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg leading-6 font-medium text-gray-900">
              Gestión de Usuarios
            </h3>
            <button
              class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium"
            >
              Gestionar Usuarios
            </button>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div class="text-center">
              <div class="text-2xl font-bold text-gray-900">{{ getTotalUsers() }}</div>
              <div class="text-sm text-gray-500">Total Usuarios</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-blue-600">{{ getActiveUsers() }}</div>
              <div class="text-sm text-gray-500">Usuarios Activos</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-green-600">{{ getTeachers() }}</div>
              <div class="text-sm text-gray-500">Profesores</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-purple-600">{{ getStudents() }}</div>
              <div class="text-sm text-gray-500">Estudiantes</div>
            </div>
          </div>
        </div>
      </div>

      <!-- System Alerts -->
      @if (getSystemAlerts().length > 0) {
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
              Alertas del Sistema
            </h3>
            <div class="space-y-3">
              @for (alert of getSystemAlerts(); track alert.id) {
                <div class="flex items-center space-x-3 p-3 rounded-md" 
                     [class]="getAlertClass(alert.type)">
                  <div class="flex-shrink-0">
                    <div class="w-2 h-2 rounded-full" 
                         [class]="getAlertDotClass(alert.type)"></div>
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-gray-900">{{ alert.title }}</p>
                    <p class="text-sm text-gray-500">{{ alert.message }}</p>
                  </div>
                  <div class="flex-shrink-0">
                    <span class="text-xs text-gray-500">{{ alert.timestamp }}</span>
                  </div>
                </div>
              }
            </div>
          </div>
        </div>
      }

      <!-- Export Panel -->
      <div class="mt-6">
        <app-export-panel
          [dashboardElement]="dashboardElement"
          [dashboardData]="dashboardData()"
          (exportComplete)="onExportComplete($event)"
        ></app-export-panel>
      </div>
    </div>
  `,
  styles: []
})
export class AdminDashboardComponent extends BaseDashboardComponent implements OnInit {
  @ViewChild('dashboardContainer', { static: false }) dashboardElement?: ElementRef;

  ngOnInit(): void {
    super.ngOnInit();
  }

  onExportComplete(result: { success: boolean; filename?: string; error?: string }): void {
    console.log('Export completed:', result);
  }

  getSystemStats() {
    const data = this.dashboardData();
    if (!data?.dashboard?.stats) return [];

    const stats = data.dashboard.stats;
    return [
      { key: 'total_users', label: 'Usuarios Totales', value: stats.total_users || 0 },
      { key: 'total_courses', label: 'Cursos Totales', value: stats.total_courses || 0 },
      { key: 'total_students', label: 'Estudiantes', value: stats.total_students || 0 },
      { key: 'total_teachers', label: 'Profesores', value: stats.total_teachers || 0 },
      { key: 'system_uptime', label: 'Tiempo Activo', value: stats.system_uptime || '99.9%' },
      { key: 'active_sessions', label: 'Sesiones Activas', value: stats.active_sessions || this.getActiveConnections() },
      { key: 'storage_used', label: 'Almacenamiento', value: stats.storage_used || '78%' },
      { key: 'api_calls', label: 'Llamadas API', value: stats.api_calls || '1.2K' }
    ];
  }

  getStatIconClass(statKey: string): string {
    switch (statKey) {
      case 'total_users':
        return 'bg-indigo-500';
      case 'total_courses':
        return 'bg-blue-500';
      case 'total_students':
        return 'bg-green-500';
      case 'total_teachers':
        return 'bg-purple-500';
      case 'system_uptime':
        return 'bg-green-500';
      case 'active_sessions':
        return 'bg-yellow-500';
      case 'storage_used':
        return 'bg-orange-500';
      case 'api_calls':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  }

  getActiveConnections(): number {
    return Math.floor(Math.random() * 50) + 20; // Mock data
  }

  getSyncedCourses(): number {
    const data = this.dashboardData();
    return data?.dashboard?.stats?.total_courses || 0;
  }

  getSyncedStudents(): number {
    const data = this.dashboardData();
    return data?.dashboard?.stats?.total_students || 0;
  }

  getTotalUsers(): number {
    const data = this.dashboardData();
    return data?.dashboard?.stats?.total_users || 0;
  }

  getActiveUsers(): number {
    return Math.floor(this.getTotalUsers() * 0.85); // 85% active
  }

  getTeachers(): number {
    const data = this.dashboardData();
    return data?.dashboard?.stats?.total_teachers || 0;
  }

  getStudents(): number {
    const data = this.dashboardData();
    return data?.dashboard?.stats?.total_students || 0;
  }

  getSystemAlerts() {
    const data = this.dashboardData();
    return data?.dashboard?.system_alerts || [];
  }

  getAlertClass(alertType: string): string {
    switch (alertType) {
      case 'warning':
        return 'bg-red-50';
      case 'info':
        return 'bg-blue-50';
      case 'success':
        return 'bg-green-50';
      default:
        return 'bg-gray-50';
    }
  }

  getAlertDotClass(alertType: string): string {
    switch (alertType) {
      case 'warning':
        return 'bg-red-500';
      case 'info':
        return 'bg-blue-500';
      case 'success':
        return 'bg-green-500';
      default:
        return 'bg-gray-500';
    }
  }
}
