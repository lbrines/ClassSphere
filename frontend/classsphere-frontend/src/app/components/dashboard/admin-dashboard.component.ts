import { Component, OnInit, signal, computed, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BaseDashboardComponent } from './base-dashboard.component';
import { AuthService } from '../../services/auth.service';
import { DashboardService } from '../../services/dashboard.service';
import { MetricsService, MetricCardData, ChartData } from '../../services/metrics.service';
import { MetricsCardComponent } from '../../shared/components/metrics-card/metrics-card.component';
import { MetricsChartComponent } from '../../shared/components/metrics-chart/metrics-chart.component';
import { Router } from '@angular/router';
import { ExportPanelComponent } from '../export/export-panel.component';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [CommonModule, MetricsCardComponent, MetricsChartComponent, ExportPanelComponent],
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

      <!-- System Overview Stats with Enhanced Metrics Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        @for (metric of getEnhancedMetrics(); track metric.title) {
          <app-metrics-card [data]="metric"></app-metrics-card>
        }
      </div>

      <!-- System Analytics Charts -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- System Usage Chart -->
        <app-metrics-chart
          [chartData]="getSystemUsageChart()"
          chartType="bar"
          title="Uso del Sistema"
          subtitle="Actividad por mes">
        </app-metrics-chart>

        <!-- User Distribution Chart -->
        <app-metrics-chart
          [chartData]="getUserDistributionChart()"
          chartType="doughnut"
          title="Distribución de Usuarios"
          subtitle="Por rol">
        </app-metrics-chart>
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

      <!-- Charts Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- Users Distribution Chart -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Distribución de Usuarios</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="w-4 h-4 bg-blue-500 rounded-full mr-3"></div>
                  <span class="text-sm text-gray-600">Estudiantes</span>
                </div>
                <div class="flex items-center">
                  <div class="w-32 bg-gray-200 rounded-full h-2 mr-3">
                    <div class="bg-blue-500 h-2 rounded-full" [style.width.%]="getUserPercentage('students')"></div>
                  </div>
                  <span class="text-sm font-medium text-gray-900">{{ getTotalStudents() }}</span>
                </div>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="w-4 h-4 bg-green-500 rounded-full mr-3"></div>
                  <span class="text-sm text-gray-600">Profesores</span>
                </div>
                <div class="flex items-center">
                  <div class="w-32 bg-gray-200 rounded-full h-2 mr-3">
                    <div class="bg-green-500 h-2 rounded-full" [style.width.%]="getUserPercentage('teachers')"></div>
                  </div>
                  <span class="text-sm font-medium text-gray-900">{{ getTotalTeachers() }}</span>
                </div>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="w-4 h-4 bg-yellow-500 rounded-full mr-3"></div>
                  <span class="text-sm text-gray-600">Coordinadores</span>
                </div>
                <div class="flex items-center">
                  <div class="w-32 bg-gray-200 rounded-full h-2 mr-3">
                    <div class="bg-yellow-500 h-2 rounded-full" [style.width.%]="getUserPercentage('coordinators')"></div>
                  </div>
                  <span class="text-sm font-medium text-gray-900">2</span>
                </div>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="w-4 h-4 bg-red-500 rounded-full mr-3"></div>
                  <span class="text-sm text-gray-600">Administradores</span>
                </div>
                <div class="flex items-center">
                  <div class="w-32 bg-gray-200 rounded-full h-2 mr-3">
                    <div class="bg-red-500 h-2 rounded-full" [style.width.%]="getUserPercentage('admins')"></div>
                  </div>
                  <span class="text-sm font-medium text-gray-900">1</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- System Performance Chart -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Rendimiento del Sistema</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">CPU Usage</span>
                <div class="flex items-center">
                  <div class="w-32 bg-gray-200 rounded-full h-2 mr-3">
                    <div class="bg-blue-500 h-2 rounded-full" style="width: 45%"></div>
                  </div>
                  <span class="text-sm font-medium text-gray-900">45%</span>
                </div>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Memory Usage</span>
                <div class="flex items-center">
                  <div class="w-32 bg-gray-200 rounded-full h-2 mr-3">
                    <div class="bg-green-500 h-2 rounded-full" style="width: 62%"></div>
                  </div>
                  <span class="text-sm font-medium text-gray-900">62%</span>
                </div>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Disk Usage</span>
                <div class="flex items-center">
                  <div class="w-32 bg-gray-200 rounded-full h-2 mr-3">
                    <div class="bg-yellow-500 h-2 rounded-full" style="width: 78%"></div>
                  </div>
                  <span class="text-sm font-medium text-gray-900">78%</span>
                </div>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Network I/O</span>
                <div class="flex items-center">
                  <div class="w-32 bg-gray-200 rounded-full h-2 mr-3">
                    <div class="bg-purple-500 h-2 rounded-full" style="width: 34%"></div>
                  </div>
                  <span class="text-sm font-medium text-gray-900">34%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Export Panel -->
      <div class="mt-6">
        <app-export-panel
          [dashboardElement]="dashboardElement?.nativeElement"
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

  constructor(
    authService: AuthService,
    dashboardService: DashboardService,
    router: Router,
    private metricsService: MetricsService
  ) {
    super(authService, dashboardService, router);
  }

  // Computed signals to avoid ExpressionChangedAfterItHasBeenCheckedError
  totalUsers = computed(() => {
    const data = this.dashboardData();
    return data?.dashboard?.stats?.total_users || 486;
  });

  totalCourses = computed(() => {
    const data = this.dashboardData();
    return data?.dashboard?.stats?.total_courses || 70;
  });

  activeUsers = computed(() => {
    return Math.floor(this.totalUsers() * 0.85); // 85% active
  });

  totalTeachers = computed(() => {
    const data = this.dashboardData();
    return data?.dashboard?.stats?.total_teachers || 0;
  });

  totalStudents = computed(() => {
    const data = this.dashboardData();
    return data?.dashboard?.stats?.total_students || 0;
  });

  override ngOnInit(): void {
    super.ngOnInit();
    this.loadMetrics();
  }

  private loadMetrics() {
    this.metricsService.getDashboardMetrics().subscribe();
    this.metricsService.getPerformanceMetrics().subscribe();
  }

  getEnhancedMetrics(): MetricCardData[] {
    const data = this.dashboardData();
    const stats = data?.dashboard?.stats;
    
    return [
      {
        title: 'Total Usuarios',
        value: stats?.total_users || this.getTotalUsers(),
        icon: 'fas fa-users',
        color: 'blue',
        trend: {
          value: 25,
          direction: 'up',
          label: 'nuevos usuarios'
        }
      },
      {
        title: 'Total Cursos',
        value: stats?.total_courses || this.getTotalCourses(),
        icon: 'fas fa-graduation-cap',
        color: 'green',
        trend: {
          value: 12,
          direction: 'up',
          label: 'nuevos cursos'
        }
      },
      {
        title: 'Total Profesores',
        value: stats?.total_teachers || this.getTotalTeachers(),
        icon: 'fas fa-chalkboard-teacher',
        color: 'purple',
        trend: {
          value: 3,
          direction: 'up',
          label: 'nuevos profesores'
        }
      },
      {
        title: 'Uptime del Sistema',
        value: '99.9%',
        icon: 'fas fa-server',
        color: 'indigo',
        format: 'text',
        trend: {
          value: 0.1,
          direction: 'up',
          label: 'mejora mensual'
        }
      }
    ];
  }

  getSystemUsageChart(): ChartData {
    const months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'];
    
    return {
      labels: months,
      datasets: [{
        label: 'Usuarios Activos',
        data: [1200, 1350, 1480, 1620, 1750, 1890],
        backgroundColor: ['#3B82F6'],
        borderColor: ['#1D4ED8'],
        borderWidth: 2
      }]
    };
  }

  getUserDistributionChart(): ChartData {
    return {
      labels: ['Estudiantes', 'Profesores', 'Coordinadores', 'Administradores'],
      datasets: [{
        label: 'Usuarios',
        data: [450, 25, 8, 3],
        backgroundColor: ['#10B981', '#3B82F6', '#F59E0B', '#EF4444'],
        borderWidth: 2
      }]
    };
  }

  onExportComplete(result: { success: boolean; filename?: string; error?: string }): void {
    console.log('Export completed:', result);
  }

  getTotalStudents(): number {
    return this.totalStudents();
  }

  getTotalTeachers(): number {
    return this.totalTeachers();
  }

  getUserPercentage(type: string): number {
    const total = this.getTotalStudents() + this.getTotalTeachers() + 2 + 1; // +2 coordinators +1 admin
    if (total === 0) return 0;
    
    switch (type) {
      case 'students':
        return Math.round((this.getTotalStudents() / total) * 100);
      case 'teachers':
        return Math.round((this.getTotalTeachers() / total) * 100);
      case 'coordinators':
        return Math.round((2 / total) * 100);
      case 'admins':
        return Math.round((1 / total) * 100);
      default:
        return 0;
    }
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
    return this.totalUsers();
  }

  getTotalCourses(): number {
    return this.totalCourses();
  }

  getActiveUsers(): number {
    return this.activeUsers();
  }

  getTeachers(): number {
    return this.totalTeachers();
  }

  getStudents(): number {
    return this.totalStudents();
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
