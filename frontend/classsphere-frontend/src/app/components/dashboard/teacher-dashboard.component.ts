import { Component, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BaseDashboardComponent } from './base-dashboard.component';
import { AuthService } from '../../services/auth.service';
import { DashboardService } from '../../services/dashboard.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-teacher-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="px-4 py-6 sm:px-0">
      <!-- Teacher Welcome Message -->
      <div class="bg-white overflow-hidden shadow rounded-lg mb-6">
        <div class="px-4 py-5 sm:p-6">
          <h2 class="text-2xl font-bold text-gray-900 mb-2">
            Panel del Profesor
          </h2>
          <p class="text-gray-600">
            Bienvenido, {{ currentUser()?.name }} - Última actualización: {{ formatDate(dashboardData()?.timestamp) }}
          </p>
        </div>
      </div>

      <!-- Teacher Stats -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        @for (stat of getTeacherStats(); track stat.key) {
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

      <!-- My Courses & Students at Risk -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- My Courses -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-lg leading-6 font-medium text-gray-900">
                Mis Cursos
              </h3>
              <button
                class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Ver Todos
              </button>
            </div>
            <div class="space-y-3">
              @for (course of getMyCourses(); track course.id) {
                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-gray-900">{{ course.name }}</p>
                    <p class="text-sm text-gray-500">{{ course.students }} estudiantes</p>
                  </div>
                  <div class="flex-shrink-0">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                          [class]="getCourseStatusClass(course.status)">
                      {{ course.status }}
                    </span>
                  </div>
                </div>
              }
            </div>
          </div>
        </div>

        <!-- Students at Risk -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-lg leading-6 font-medium text-gray-900">
                Estudiantes en Riesgo
              </h3>
              <button
                class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Intervenir
              </button>
            </div>
            <div class="space-y-3">
              @for (student of getStudentsAtRisk(); track student.id) {
                <div class="flex items-center justify-between p-3 bg-red-50 rounded-md">
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-gray-900">{{ student.name }}</p>
                    <p class="text-sm text-gray-500">{{ student.course }} - Promedio: {{ student.average }}</p>
                  </div>
                  <div class="flex-shrink-0">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                      {{ student.risk_level }}
                    </span>
                  </div>
                </div>
              }
            </div>
          </div>
        </div>
      </div>

      <!-- Assignments & Grades -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- Recent Assignments -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-lg leading-6 font-medium text-gray-900">
                Tareas Recientes
              </h3>
              <button
                class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Crear Tarea
              </button>
            </div>
            <div class="space-y-3">
              @for (assignment of getRecentAssignments(); track assignment.id) {
                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-gray-900">{{ assignment.title }}</p>
                    <p class="text-sm text-gray-500">{{ assignment.course }} - Vence: {{ assignment.due_date }}</p>
                  </div>
                  <div class="flex-shrink-0">
                    <span class="text-sm text-gray-500">{{ assignment.submissions }}/{{ assignment.total_students }}</span>
                  </div>
                </div>
              }
            </div>
          </div>
        </div>

        <!-- Grade Distribution -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
              Distribución de Calificaciones
            </h3>
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">A (90-100)</span>
                <div class="flex items-center space-x-2">
                  <div class="w-24 bg-gray-200 rounded-full h-2">
                    <div class="bg-green-600 h-2 rounded-full" style="width: 25%"></div>
                  </div>
                  <span class="text-sm font-medium text-gray-900">25%</span>
                </div>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">B (80-89)</span>
                <div class="flex items-center space-x-2">
                  <div class="w-24 bg-gray-200 rounded-full h-2">
                    <div class="bg-blue-600 h-2 rounded-full" style="width: 35%"></div>
                  </div>
                  <span class="text-sm font-medium text-gray-900">35%</span>
                </div>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">C (70-79)</span>
                <div class="flex items-center space-x-2">
                  <div class="w-24 bg-gray-200 rounded-full h-2">
                    <div class="bg-yellow-600 h-2 rounded-full" style="width: 25%"></div>
                  </div>
                  <span class="text-sm font-medium text-gray-900">25%</span>
                </div>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">D/F (<70)</span>
                <div class="flex items-center space-x-2">
                  <div class="w-24 bg-gray-200 rounded-full h-2">
                    <div class="bg-red-600 h-2 rounded-full" style="width: 15%"></div>
                  </div>
                  <span class="text-sm font-medium text-gray-900">15%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Upcoming Deadlines -->
      @if (getUpcomingDeadlines().length > 0) {
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
              Próximas Fechas Límite
            </h3>
            <div class="space-y-3">
              @for (deadline of getUpcomingDeadlines(); track deadline.id) {
                <div class="flex items-center justify-between p-3 bg-yellow-50 rounded-md">
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-gray-900">{{ deadline.title }}</p>
                    <p class="text-sm text-gray-500">{{ deadline.course }} - {{ deadline.description }}</p>
                  </div>
                  <div class="flex-shrink-0">
                    <span class="text-sm text-gray-500">{{ deadline.due_date }}</span>
                  </div>
                </div>
              }
            </div>
          </div>
        </div>
      }
    </div>
  `,
  styles: []
})
export class TeacherDashboardComponent extends BaseDashboardComponent implements OnInit {
  
  override ngOnInit(): void {
    super.ngOnInit();
  }

  getTeacherStats() {
    const data = this.dashboardData();
    if (!data?.dashboard?.stats) return [];

    const stats = data.dashboard.stats;
    return [
      { key: 'my_courses', label: 'Mis Cursos', value: this.getMyCourses().length },
      { key: 'total_students', label: 'Mis Estudiantes', value: this.getTotalMyStudents() },
      { key: 'pending_grades', label: 'Calificaciones Pendientes', value: stats.pending_assignments || this.getPendingGrades() },
      { key: 'upcoming_deadlines', label: 'Fechas Límite', value: this.getUpcomingDeadlines().length }
    ];
  }

  getStatIconClass(statKey: string): string {
    switch (statKey) {
      case 'my_courses':
        return 'bg-blue-500';
      case 'total_students':
        return 'bg-green-500';
      case 'pending_grades':
        return 'bg-yellow-500';
      case 'upcoming_deadlines':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  }

  getMyCourses() {
    // Mock data - in real implementation, this would come from the API
    return [
      { id: 1, name: 'Matemáticas 101', students: 25, status: 'Activo' },
      { id: 2, name: 'Física 201', students: 18, status: 'Activo' },
      { id: 3, name: 'Álgebra Lineal', students: 22, status: 'Activo' }
    ];
  }

  getTotalMyStudents(): number {
    return this.getMyCourses().reduce((total, course) => total + course.students, 0);
  }

  getStudentsAtRisk() {
    // Mock data - in real implementation, this would come from the API
    return [
      { id: 1, name: 'Juan Pérez', course: 'Matemáticas 101', average: 65, risk_level: 'Alto' },
      { id: 2, name: 'María García', course: 'Física 201', average: 68, risk_level: 'Medio' },
      { id: 3, name: 'Carlos López', course: 'Álgebra Lineal', average: 62, risk_level: 'Alto' }
    ];
  }

  getRecentAssignments() {
    // Mock data - in real implementation, this would come from the API
    return [
      { id: 1, title: 'Examen Parcial 1', course: 'Matemáticas 101', due_date: '2025-10-10', submissions: 20, total_students: 25 },
      { id: 2, title: 'Proyecto de Laboratorio', course: 'Física 201', due_date: '2025-10-12', submissions: 15, total_students: 18 },
      { id: 3, title: 'Tarea de Vectores', course: 'Álgebra Lineal', due_date: '2025-10-08', submissions: 22, total_students: 22 }
    ];
  }

  getPendingGrades(): number {
    return this.getRecentAssignments().reduce((total, assignment) => 
      total + (assignment.total_students - assignment.submissions), 0);
  }

  getUpcomingDeadlines() {
    // Mock data - in real implementation, this would come from the API
    return [
      { id: 1, title: 'Examen Final', course: 'Matemáticas 101', description: 'Examen final del semestre', due_date: '2025-10-15' },
      { id: 2, title: 'Proyecto Final', course: 'Física 201', description: 'Proyecto de investigación', due_date: '2025-10-18' }
    ];
  }

  getCourseStatusClass(status: string): string {
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
}
