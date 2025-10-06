import { Component, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BaseDashboardComponent } from './base-dashboard.component';
import { AuthService } from '../../services/auth.service';
import { DashboardService } from '../../services/dashboard.service';
import { MetricsService, MetricCardData, ChartData } from '../../services/metrics.service';
import { MetricsCardComponent } from '../../shared/components/metrics-card/metrics-card.component';
import { MetricsChartComponent } from '../../shared/components/metrics-chart/metrics-chart.component';
import { Router } from '@angular/router';

@Component({
  selector: 'app-coordinator-dashboard',
  standalone: true,
  imports: [CommonModule, MetricsCardComponent, MetricsChartComponent],
  template: `
    <div class="px-4 py-6 sm:px-0">
      <!-- Coordinator Welcome Message -->
      <div class="bg-white overflow-hidden shadow rounded-lg mb-6">
        <div class="px-4 py-5 sm:p-6">
          <h2 class="text-2xl font-bold text-gray-900 mb-2">
            Panel de Coordinación
          </h2>
          <p class="text-gray-600">
            Bienvenido, {{ currentUser()?.name }} - Última actualización: {{ formatDate(dashboardData()?.timestamp) }}
          </p>
        </div>
      </div>

      <!-- Coordinator Stats with Enhanced Metrics Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        @for (metric of getEnhancedMetrics(); track metric.title) {
          <app-metrics-card [data]="metric"></app-metrics-card>
        }
      </div>

      <!-- Coordinator Analytics Charts -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- Program Performance Chart -->
        <app-metrics-chart
          [chartData]="getProgramPerformanceChart()"
          chartType="bar"
          title="Rendimiento por Programa"
          subtitle="Promedio de calificaciones">
        </app-metrics-chart>

        <!-- Faculty Distribution Chart -->
        <app-metrics-chart
          [chartData]="getFacultyDistributionChart()"
          chartType="doughnut"
          title="Distribución de Profesores"
          subtitle="Por departamento">
        </app-metrics-chart>
      </div>

      <!-- Program Overview & Teacher Performance -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- Program Overview -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-lg leading-6 font-medium text-gray-900">
                Resumen de Programas
              </h3>
              <button
                class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Gestionar Programas
              </button>
            </div>
            <div class="space-y-3">
              @for (program of getPrograms(); track program.id) {
                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-gray-900">{{ program.name }}</p>
                    <p class="text-sm text-gray-500">{{ program.courses }} cursos, {{ program.students }} estudiantes</p>
                  </div>
                  <div class="flex-shrink-0">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                          [class]="getProgramStatusClass(program.status)">
                      {{ program.status }}
                    </span>
                  </div>
                </div>
              }
            </div>
          </div>
        </div>

        <!-- Teacher Performance -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-lg leading-6 font-medium text-gray-900">
                Rendimiento de Profesores
              </h3>
              <button
                class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Ver Detalles
              </button>
            </div>
            <div class="space-y-3">
              @for (teacher of getTeacherPerformance(); track teacher.id) {
                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-gray-900">{{ teacher.name }}</p>
                    <p class="text-sm text-gray-500">{{ teacher.courses }} cursos, Promedio: {{ teacher.average }}</p>
                  </div>
                  <div class="flex-shrink-0">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                          [class]="getPerformanceClass(teacher.performance)">
                      {{ teacher.performance }}
                    </span>
                  </div>
                </div>
              }
            </div>
          </div>
        </div>
      </div>

      <!-- Course Analytics & Student Success -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- Course Analytics -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
              Análisis de Cursos
            </h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Tasa de Completación</span>
                <div class="flex items-center space-x-2">
                  <div class="w-24 bg-gray-200 rounded-full h-2">
                    <div class="bg-green-600 h-2 rounded-full" style="width: 78%"></div>
                  </div>
                  <span class="text-sm font-medium text-gray-900">78%</span>
                </div>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Satisfacción Estudiantil</span>
                <div class="flex items-center space-x-2">
                  <div class="w-24 bg-gray-200 rounded-full h-2">
                    <div class="bg-blue-600 h-2 rounded-full" style="width: 85%"></div>
                  </div>
                  <span class="text-sm font-medium text-gray-900">85%</span>
                </div>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Tasa de Retención</span>
                <div class="flex items-center space-x-2">
                  <div class="w-24 bg-gray-200 rounded-full h-2">
                    <div class="bg-purple-600 h-2 rounded-full" style="width: 92%"></div>
                  </div>
                  <span class="text-sm font-medium text-gray-900">92%</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Student Success Metrics -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
              Métricas de Éxito Estudiantil
            </h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Estudiantes en Riesgo</span>
                <span class="text-sm font-medium text-red-600">{{ getStudentsAtRisk() }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Intervenciones Exitosas</span>
                <span class="text-sm font-medium text-green-600">{{ getSuccessfulInterventions() }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Tasa de Graduación</span>
                <span class="text-sm font-medium text-blue-600">{{ getGraduationRate() }}%</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Promedio General</span>
                <span class="text-sm font-medium text-purple-600">{{ getOverallAverage() }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activities & Alerts -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- Recent Activities -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
              Actividades Recientes
            </h3>
            <div class="space-y-3">
              @for (activity of getRecentActivities(); track activity.id) {
                <div class="flex items-center space-x-3 p-3 bg-gray-50 rounded-md">
                  <div class="flex-shrink-0">
                    <div class="w-2 h-2 rounded-full" 
                         [class]="getActivityDotClass(activity.type)"></div>
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-gray-900">{{ activity.title }}</p>
                    <p class="text-sm text-gray-500">{{ activity.description }}</p>
                  </div>
                  <div class="flex-shrink-0">
                    <span class="text-xs text-gray-500">{{ activity.timestamp }}</span>
                  </div>
                </div>
              }
            </div>
          </div>
        </div>

        <!-- System Alerts -->
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
      </div>
    </div>
  `,
  styles: []
})
export class CoordinatorDashboardComponent extends BaseDashboardComponent implements OnInit {
  
  constructor(
    authService: AuthService,
    dashboardService: DashboardService,
    router: Router,
    private metricsService: MetricsService
  ) {
    super(authService, dashboardService, router);
  }
  
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
        title: 'Total Cursos',
        value: stats?.total_courses || this.getTotalCourses(),
        icon: 'fas fa-graduation-cap',
        color: 'blue',
        trend: {
          value: 18,
          direction: 'up',
          label: 'vs semestre anterior'
        }
      },
      {
        title: 'Total Profesores',
        value: stats?.total_teachers || this.getTotalTeachers(),
        icon: 'fas fa-chalkboard-teacher',
        color: 'green',
        trend: {
          value: 5,
          direction: 'up',
          label: 'nuevos profesores'
        }
      },
      {
        title: 'Total Estudiantes',
        value: stats?.total_students || this.getTotalStudents(),
        icon: 'fas fa-users',
        color: 'purple',
        trend: {
          value: 45,
          direction: 'up',
          label: 'nuevos estudiantes'
        }
      },
      {
        title: 'Programas Activos',
        value: this.getActivePrograms(),
        icon: 'fas fa-project-diagram',
        color: 'indigo',
        trend: {
          value: 1,
          direction: 'up',
          label: 'nuevo programa'
        }
      }
    ];
  }

  getProgramPerformanceChart(): ChartData {
    const programs = this.getPrograms();
    
    return {
      labels: programs.map(p => p.name),
      datasets: [{
        label: 'Promedio (%)',
        data: programs.map(p => 85), // Mock average grade
        backgroundColor: ['#10B981', '#3B82F6', '#F59E0B', '#EF4444', '#8B5CF6'],
        borderWidth: 2
      }]
    };
  }

  getFacultyDistributionChart(): ChartData {
    const departments = this.getFacultyByDepartment();
    
    return {
      labels: departments.map(d => d.name),
      datasets: [{
        label: 'Profesores',
        data: departments.map(d => d.count),
        backgroundColor: ['#10B981', '#3B82F6', '#F59E0B', '#EF4444'],
        borderWidth: 2
      }]
    };
  }

  getCoordinatorStats() {
    const data = this.dashboardData();
    if (!data?.dashboard?.stats) return [];

    const stats = data.dashboard.stats;
    return [
      { key: 'total_programs', label: 'Programas Activos', value: this.getPrograms().length },
      { key: 'total_teachers', label: 'Profesores', value: stats.total_teachers || this.getTeacherPerformance().length },
      { key: 'total_courses', label: 'Cursos', value: stats.total_courses || this.getTotalCourses() },
      { key: 'students_at_risk', label: 'Estudiantes en Riesgo', value: this.getStudentsAtRisk() }
    ];
  }

  getStatIconClass(statKey: string): string {
    switch (statKey) {
      case 'total_programs':
        return 'bg-purple-500';
      case 'total_teachers':
        return 'bg-blue-500';
      case 'total_courses':
        return 'bg-green-500';
      case 'students_at_risk':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  }

  getPrograms() {
    // Mock data - in real implementation, this would come from the API
    return [
      { id: 1, name: 'Ingeniería de Sistemas', courses: 15, students: 120, status: 'Activo' },
      { id: 2, name: 'Matemáticas', courses: 8, students: 80, status: 'Activo' },
      { id: 3, name: 'Física', courses: 6, students: 60, status: 'Activo' }
    ];
  }

  getTeacherPerformance() {
    // Mock data - in real implementation, this would come from the API
    return [
      { id: 1, name: 'Dr. García', courses: 3, average: 'A-', performance: 'Excelente' },
      { id: 2, name: 'Prof. López', courses: 2, average: 'B+', performance: 'Bueno' },
      { id: 3, name: 'Dra. Martínez', courses: 4, average: 'A', performance: 'Excelente' }
    ];
  }

  getTotalCourses(): number {
    return this.getPrograms().reduce((total, program) => total + program.courses, 0);
  }

  getTotalTeachers(): number {
    return this.getFacultyByDepartment().reduce((total, dept) => total + dept.count, 0);
  }

  getTotalStudents(): number {
    return 450; // Mock data
  }

  getActivePrograms(): number {
    return this.getPrograms().length;
  }


  getFacultyByDepartment() {
    return [
      { name: 'Matemáticas', count: 8 },
      { name: 'Física', count: 6 },
      { name: 'Química', count: 5 },
      { name: 'Ingeniería', count: 12 }
    ];
  }

  getStudentsAtRisk(): number {
    // Mock data - in real implementation, this would come from the API
    return 12;
  }

  getSuccessfulInterventions(): number {
    // Mock data - in real implementation, this would come from the API
    return 8;
  }

  getGraduationRate(): number {
    // Mock data - in real implementation, this would come from the API
    return 85;
  }

  getOverallAverage(): string {
    // Mock data - in real implementation, this would come from the API
    return 'B+';
  }

  getRecentActivities() {
    // Mock data - in real implementation, this would come from the API
    return [
      { id: 1, type: 'course', title: 'Nuevo curso creado', description: 'Matemáticas Avanzadas por Dr. García', timestamp: 'Hace 2 horas' },
      { id: 2, type: 'student', title: 'Estudiante en riesgo identificado', description: 'Juan Pérez en Física 201', timestamp: 'Hace 4 horas' },
      { id: 3, type: 'teacher', title: 'Evaluación completada', description: 'Evaluación de Prof. López', timestamp: 'Hace 6 horas' }
    ];
  }

  getSystemAlerts() {
    // Mock data - in real implementation, this would come from the API
    return [
      { id: 1, type: 'warning', title: 'Baja participación', message: 'Física 201 tiene baja participación estudiantil', timestamp: 'Hace 1 hora' },
      { id: 2, type: 'info', title: 'Nueva actualización', message: 'Sistema actualizado a la versión 2.1', timestamp: 'Hace 3 horas' }
    ];
  }

  getProgramStatusClass(status: string): string {
    switch (status) {
      case 'Activo':
        return 'bg-green-100 text-green-800';
      case 'Inactivo':
        return 'bg-gray-100 text-gray-800';
      case 'Archivado':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  }

  getPerformanceClass(performance: string): string {
    switch (performance) {
      case 'Excelente':
        return 'bg-green-100 text-green-800';
      case 'Bueno':
        return 'bg-blue-100 text-blue-800';
      case 'Regular':
        return 'bg-yellow-100 text-yellow-800';
      case 'Necesita Mejora':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  }

  getActivityDotClass(activityType: string): string {
    switch (activityType) {
      case 'course':
        return 'bg-blue-500';
      case 'student':
        return 'bg-green-500';
      case 'teacher':
        return 'bg-purple-500';
      default:
        return 'bg-gray-500';
    }
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
