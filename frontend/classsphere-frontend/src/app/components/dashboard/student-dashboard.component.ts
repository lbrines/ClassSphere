import { Component, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BaseDashboardComponent } from './base-dashboard.component';
import { AuthService } from '../../services/auth.service';
import { DashboardService } from '../../services/dashboard.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-student-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="px-4 py-6 sm:px-0">
      <!-- Student Welcome Message -->
      <div class="bg-white overflow-hidden shadow rounded-lg mb-6">
        <div class="px-4 py-5 sm:p-6">
          <h2 class="text-2xl font-bold text-gray-900 mb-2">
            Mi Panel de Estudiante
          </h2>
          <p class="text-gray-600">
            Hola {{ currentUser()?.name }} - Última actualización: {{ formatDate(dashboardData()?.timestamp) }}
          </p>
        </div>
      </div>

      <!-- Student Stats -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        @for (stat of getStudentStats(); track stat.key) {
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

      <!-- My Courses & Progress -->
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
                    <p class="text-sm text-gray-500">Profesor: {{ course.teacher }}</p>
                  </div>
                  <div class="flex-shrink-0">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                          [class]="getGradeClass(course.grade)">
                      {{ course.grade || 'Sin calificar' }}
                    </span>
                  </div>
                </div>
              }
            </div>
          </div>
        </div>

        <!-- My Progress -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
              Mi Progreso
            </h3>
            <div class="space-y-4">
              @for (progress of getMyProgress(); track progress.course) {
                <div>
                  <div class="flex justify-between items-center mb-1">
                    <span class="text-sm font-medium text-gray-700">{{ progress.course }}</span>
                    <span class="text-sm text-gray-500">{{ progress.percentage }}%</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-blue-600 h-2 rounded-full" 
                         [style.width.%]="progress.percentage"></div>
                  </div>
                </div>
              }
            </div>
          </div>
        </div>
      </div>

      <!-- Assignments & Grades -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- Upcoming Assignments -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-lg leading-6 font-medium text-gray-900">
                Próximas Tareas
              </h3>
              <button
                class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Ver Todas
              </button>
            </div>
            <div class="space-y-3">
              @for (assignment of getUpcomingAssignments(); track assignment.id) {
                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-gray-900">{{ assignment.title }}</p>
                    <p class="text-sm text-gray-500">{{ assignment.course }} - Vence: {{ assignment.due_date }}</p>
                  </div>
                  <div class="flex-shrink-0">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                          [class]="getAssignmentStatusClass(assignment.status)">
                      {{ assignment.status }}
                    </span>
                  </div>
                </div>
              }
            </div>
          </div>
        </div>

        <!-- Recent Grades -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-lg leading-6 font-medium text-gray-900">
                Calificaciones Recientes
              </h3>
              <button
                class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Ver Historial
              </button>
            </div>
            <div class="space-y-3">
              @for (grade of getRecentGrades(); track grade.id) {
                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-gray-900">{{ grade.assignment }}</p>
                    <p class="text-sm text-gray-500">{{ grade.course }} - {{ grade.date }}</p>
                  </div>
                  <div class="flex-shrink-0">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                          [class]="getGradeClass(grade.grade)">
                      {{ grade.grade }}
                    </span>
                  </div>
                </div>
              }
            </div>
          </div>
        </div>
      </div>

      <!-- Study Recommendations -->
      @if (getStudyRecommendations().length > 0) {
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
              Recomendaciones de Estudio
            </h3>
            <div class="space-y-3">
              @for (recommendation of getStudyRecommendations(); track recommendation.id) {
                <div class="flex items-center space-x-3 p-3 bg-blue-50 rounded-md">
                  <div class="flex-shrink-0">
                    <div class="w-2 h-2 rounded-full bg-blue-500"></div>
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-gray-900">{{ recommendation.title }}</p>
                    <p class="text-sm text-gray-500">{{ recommendation.description }}</p>
                  </div>
                  <div class="flex-shrink-0">
                    <span class="text-xs text-gray-500">{{ recommendation.priority }}</span>
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
export class StudentDashboardComponent extends BaseDashboardComponent implements OnInit {
  
  override ngOnInit(): void {
    super.ngOnInit();
  }

  getStudentStats() {
    const data = this.dashboardData();
    if (!data?.dashboard?.stats) return [];

    const stats = data.dashboard.stats;
    return [
      { key: 'my_courses', label: 'Mis Cursos', value: this.getMyCourses().length },
      { key: 'completed_assignments', label: 'Tareas Completadas', value: stats.completed_assignments || this.getCompletedAssignments() },
      { key: 'pending_assignments', label: 'Tareas Pendientes', value: stats.pending_assignments || this.getPendingAssignments() },
      { key: 'average_grade', label: 'Promedio General', value: stats.average_grade || this.getAverageGrade() }
    ];
  }

  getStatIconClass(statKey: string): string {
    switch (statKey) {
      case 'my_courses':
        return 'bg-blue-500';
      case 'completed_assignments':
        return 'bg-green-500';
      case 'pending_assignments':
        return 'bg-yellow-500';
      case 'average_grade':
        return 'bg-purple-500';
      default:
        return 'bg-gray-500';
    }
  }

  getMyCourses() {
    // Mock data - in real implementation, this would come from the API
    return [
      { id: 1, name: 'Matemáticas 101', teacher: 'Dr. García', grade: 'A' },
      { id: 2, name: 'Física 201', teacher: 'Prof. López', grade: 'B+' },
      { id: 3, name: 'Álgebra Lineal', teacher: 'Dra. Martínez', grade: 'A-' }
    ];
  }

  getMyProgress() {
    // Mock data - in real implementation, this would come from the API
    return [
      { course: 'Matemáticas 101', percentage: 85 },
      { course: 'Física 201', percentage: 72 },
      { course: 'Álgebra Lineal', percentage: 90 }
    ];
  }

  getUpcomingAssignments() {
    // Mock data - in real implementation, this would come from the API
    return [
      { id: 1, title: 'Examen Parcial 1', course: 'Matemáticas 101', due_date: '2025-10-10', status: 'Pendiente' },
      { id: 2, title: 'Proyecto de Laboratorio', course: 'Física 201', due_date: '2025-10-12', status: 'En Progreso' },
      { id: 3, title: 'Tarea de Vectores', course: 'Álgebra Lineal', due_date: '2025-10-08', status: 'Completada' }
    ];
  }

  getRecentGrades() {
    // Mock data - in real implementation, this would come from the API
    return [
      { id: 1, assignment: 'Tarea 3', course: 'Matemáticas 101', grade: 'A', date: '2025-10-05' },
      { id: 2, assignment: 'Quiz 2', course: 'Física 201', grade: 'B+', date: '2025-10-03' },
      { id: 3, assignment: 'Examen 1', course: 'Álgebra Lineal', grade: 'A-', date: '2025-10-01' }
    ];
  }

  getStudyRecommendations() {
    // Mock data - in real implementation, this would come from the API
    return [
      { id: 1, title: 'Revisar conceptos de derivadas', description: 'Tu rendimiento en cálculo puede mejorar', priority: 'Alta' },
      { id: 2, title: 'Practicar problemas de física', description: 'Más práctica en mecánica clásica', priority: 'Media' }
    ];
  }

  getCompletedAssignments(): number {
    return this.getUpcomingAssignments().filter(a => a.status === 'Completada').length;
  }

  getPendingAssignments(): number {
    return this.getUpcomingAssignments().filter(a => a.status === 'Pendiente').length;
  }

  getAverageGrade(): string {
    // Mock calculation - in real implementation, this would come from the API
    return 'B+';
  }

  getGradeClass(grade: string): string {
    if (!grade) return 'bg-gray-100 text-gray-800';
    
    const gradeValue = grade.charAt(0);
    switch (gradeValue) {
      case 'A':
        return 'bg-green-100 text-green-800';
      case 'B':
        return 'bg-blue-100 text-blue-800';
      case 'C':
        return 'bg-yellow-100 text-yellow-800';
      case 'D':
      case 'F':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  }

  getAssignmentStatusClass(status: string): string {
    switch (status) {
      case 'Completada':
        return 'bg-green-100 text-green-800';
      case 'En Progreso':
        return 'bg-yellow-100 text-yellow-800';
      case 'Pendiente':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  }
}
