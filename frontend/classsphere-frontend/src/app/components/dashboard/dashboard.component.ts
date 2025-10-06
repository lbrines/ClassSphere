import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService, User } from '../../services/auth.service';
import { DashboardService, DashboardData } from '../../services/dashboard.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="min-h-screen bg-gray-50">
      <!-- Header -->
      <header class="bg-white shadow">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between items-center py-6">
            <div class="flex items-center">
              <h1 class="text-3xl font-bold text-gray-900">ClassSphere</h1>
            </div>
            <div class="flex items-center space-x-4">
              <span class="text-sm text-gray-700">
                Bienvenido, {{ currentUser()?.name }}
              </span>
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                {{ currentUser()?.role | titlecase }}
              </span>
              <button
                (click)="logout()"
                class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Cerrar sesión
              </button>
            </div>
          </div>
        </div>
      </header>

      <!-- Main Content -->
      <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        @if (isLoading()) {
          <div class="flex justify-center items-center h-64">
            <div class="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600"></div>
          </div>
        } @else if (errorMessage()) {
          <div class="rounded-md bg-red-50 p-4">
            <div class="text-sm text-red-700">
              {{ errorMessage() }}
            </div>
          </div>
        } @else if (dashboardData()) {
          <div class="px-4 py-6 sm:px-0">
            <!-- Welcome Message -->
            <div class="bg-white overflow-hidden shadow rounded-lg mb-6">
              <div class="px-4 py-5 sm:p-6">
                <h2 class="text-2xl font-bold text-gray-900 mb-2">
                  {{ dashboardData()?.dashboard?.welcome_message }}
                </h2>
                <p class="text-gray-600">
                  Última actualización: {{ formatDate(dashboardData()?.timestamp) }}
                </p>
              </div>
            </div>

            <!-- Stats Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
              @for (stat of getStatsArray(); track stat.key) {
                <div class="bg-white overflow-hidden shadow rounded-lg">
                  <div class="p-5">
                    <div class="flex items-center">
                      <div class="flex-shrink-0">
                        <div class="w-8 h-8 bg-indigo-500 rounded-md flex items-center justify-center">
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

            <!-- Recent Activities -->
            <div class="bg-white shadow rounded-lg mb-6">
              <div class="px-4 py-5 sm:p-6">
                <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                  Actividades Recientes
                </h3>
                <div class="space-y-3">
                  @for (activity of dashboardData()?.dashboard?.recent_activities; track activity.title) {
                    <div class="flex items-center space-x-3 p-3 bg-gray-50 rounded-md">
                      <div class="flex-shrink-0">
                        <div class="w-2 h-2 bg-indigo-500 rounded-full"></div>
                      </div>
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-medium text-gray-900">{{ activity.title }}</p>
                        <p class="text-sm text-gray-500">{{ activity.date }}</p>
                      </div>
                      @if (activity.status) {
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          {{ activity.status }}
                        </span>
                      }
                    </div>
                  }
                </div>
              </div>
            </div>

            <!-- Upcoming Tasks/Deadlines -->
            @if (getUpcomingItems().length > 0) {
              <div class="bg-white shadow rounded-lg">
                <div class="px-4 py-5 sm:p-6">
                  <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                    {{ getUpcomingTitle() }}
                  </h3>
                  <div class="space-y-3">
                    @for (item of getUpcomingItems(); track item.title) {
                      <div class="flex items-center justify-between p-3 bg-yellow-50 rounded-md">
                        <div class="flex-1 min-w-0">
                          <p class="text-sm font-medium text-gray-900">{{ item.title }}</p>
                          <p class="text-sm text-gray-500">{{ item.due_date || item.date }}</p>
                        </div>
                        @if (item.priority) {
                          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                            {{ item.priority }}
                          </span>
                        }
                      </div>
                    }
                  </div>
                </div>
              </div>
            }

            <!-- System Alerts (Admin only) -->
            @if (dashboardData()?.dashboard?.system_alerts && (dashboardData()?.dashboard?.system_alerts?.length ?? 0) > 0) {
              <div class="bg-white shadow rounded-lg mt-6">
                <div class="px-4 py-5 sm:p-6">
                  <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                    Alertas del Sistema
                  </h3>
                  <div class="space-y-3">
                    @for (alert of dashboardData()?.dashboard?.system_alerts; track alert.title) {
                      <div class="flex items-center space-x-3 p-3 rounded-md" 
                           [class]="alert.type === 'warning' ? 'bg-red-50' : 'bg-blue-50'">
                        <div class="flex-shrink-0">
                          <div class="w-2 h-2 rounded-full" 
                               [class]="alert.type === 'warning' ? 'bg-red-500' : 'bg-blue-500'"></div>
                        </div>
                        <div class="flex-1 min-w-0">
                          <p class="text-sm font-medium text-gray-900">{{ alert.title }}</p>
                          <p class="text-sm text-gray-500">{{ alert.message }}</p>
                        </div>
                      </div>
                    }
                  </div>
                </div>
              </div>
            }
          </div>
        }
      </main>
    </div>
  `,
  styles: []
})
export class DashboardComponent implements OnInit {
  currentUser = signal<User | null>(null);
  dashboardData = signal<DashboardData | null>(null);
  isLoading = signal(false);
  errorMessage = signal('');

  constructor(
    private authService: AuthService,
    private dashboardService: DashboardService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.currentUser.set(this.authService.currentUser());
    
    if (!this.authService.isAuthenticated()) {
      this.router.navigate(['/login']);
      return;
    }

    this.loadDashboard();
  }

  loadDashboard(): void {
    this.isLoading.set(true);
    this.errorMessage.set('');

    const user = this.currentUser();
    if (!user) {
      this.errorMessage.set('Usuario no encontrado');
      this.isLoading.set(false);
      return;
    }

    this.dashboardService.getDashboardByRole(user.role).subscribe({
      next: (data) => {
        this.dashboardData.set(data);
        this.isLoading.set(false);
      },
      error: (error) => {
        this.errorMessage.set(error.error?.error || 'Error al cargar el dashboard');
        this.isLoading.set(false);
      }
    });
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  getStatsArray(): Array<{key: string, label: string, value: any}> {
    const stats = this.dashboardData()?.dashboard?.stats;
    if (!stats) return [];

    return Object.entries(stats).map(([key, value]) => ({
      key,
      label: this.getStatLabel(key),
      value
    }));
  }

  getStatLabel(key: string): string {
    const labels: {[key: string]: string} = {
      'total_courses': 'Cursos Totales',
      'total_students': 'Estudiantes',
      'total_teachers': 'Profesores',
      'assignments_pending': 'Tareas Pendientes',
      'assignments_completed': 'Tareas Completadas',
      'assignments_graded': 'Tareas Calificadas',
      'average_grade': 'Promedio',
      'active_programs': 'Programas Activos',
      'total_users': 'Usuarios Totales',
      'system_uptime': 'Tiempo Activo'
    };
    return labels[key] || key;
  }

  getUpcomingItems(): any[] {
    const data = this.dashboardData();
    if (!data) return [];

    return data.dashboard?.upcoming_deadlines || data.dashboard?.upcoming_tasks || [];
  }

  getUpcomingTitle(): string {
    const data = this.dashboardData();
    if (!data) return '';

    return data.dashboard?.upcoming_deadlines ? 'Próximas Fechas Límite' : 'Próximas Tareas';
  }

  formatDate(dateString: string | undefined): string {
    if (!dateString) return '';
    return new Date(dateString).toLocaleString('es-ES');
  }
}
