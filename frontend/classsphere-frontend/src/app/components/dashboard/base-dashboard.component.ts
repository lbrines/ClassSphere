import { Component, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService, User } from '../../services/auth.service';
import { DashboardService, DashboardData } from '../../services/dashboard.service';
import { GoogleModeToggleComponent } from '../google-mode-toggle/google-mode-toggle.component';

@Component({
  selector: 'app-base-dashboard',
  standalone: true,
  imports: [CommonModule, GoogleModeToggleComponent],
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
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    [class]="getRoleBadgeClass(currentUser()?.role)">
                {{ currentUser()?.role | titlecase }}
              </span>
              <app-google-mode-toggle></app-google-mode-toggle>
              <button
                (click)="goToSearch()"
                class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Búsqueda Avanzada
              </button>
              <button
                (click)="goToCharts()"
                class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Gráficos
              </button>
              <button
                (click)="goToD3Visualizations()"
                class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                D3.js
              </button>
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
        } @else {
          <!-- Dashboard Content - To be overridden by child components -->
          <ng-content></ng-content>
        }
      </main>
    </div>
  `,
  styles: []
})
export class BaseDashboardComponent implements OnInit {
  currentUser = signal<User | null>(null);
  dashboardData = signal<DashboardData | null>(null);
  isLoading = signal(false);
  errorMessage = signal('');

  constructor(
    protected authService: AuthService,
    protected dashboardService: DashboardService,
    protected router: Router
  ) {}

  ngOnInit(): void {
    this.currentUser.set(this.authService.currentUser());
    this.loadDashboardData();
  }

  protected loadDashboardData(): void {
    this.isLoading.set(true);
    this.errorMessage.set('');

    this.dashboardService.getDashboardData().subscribe({
      next: (data) => {
        this.dashboardData.set(data);
        this.isLoading.set(false);
      },
      error: (error) => {
        console.error('Error loading dashboard data:', error);
        this.errorMessage.set('Error al cargar los datos del dashboard');
        this.isLoading.set(false);
      }
    });
  }

  getRoleBadgeClass(role?: string): string {
    switch (role) {
      case 'admin':
        return 'bg-red-100 text-red-800';
      case 'coordinator':
        return 'bg-purple-100 text-purple-800';
      case 'teacher':
        return 'bg-blue-100 text-blue-800';
      case 'student':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  }

  goToSearch(): void {
    this.router.navigate(['/search']);
  }

  goToCharts(): void {
    this.router.navigate(['/charts']);
  }

  goToD3Visualizations(): void {
    this.router.navigate(['/d3-visualizations']);
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  formatDate(timestamp?: string): string {
    if (!timestamp) return '';
    return new Date(timestamp).toLocaleString('es-ES');
  }
}
