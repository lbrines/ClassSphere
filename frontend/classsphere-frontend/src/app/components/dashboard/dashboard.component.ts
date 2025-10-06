import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService, User } from '../../services/auth.service';
import { DashboardService, DashboardData } from '../../services/dashboard.service';
import { AdminDashboardComponent } from './admin-dashboard.component';
import { TeacherDashboardComponent } from './teacher-dashboard.component';
import { StudentDashboardComponent } from './student-dashboard.component';
import { CoordinatorDashboardComponent } from './coordinator-dashboard.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, AdminDashboardComponent, TeacherDashboardComponent, StudentDashboardComponent, CoordinatorDashboardComponent],
  template: `
    <!-- Role-based Dashboard -->
    @switch (currentUser()?.role) {
      @case ('admin') {
        <app-admin-dashboard></app-admin-dashboard>
      }
      @case ('coordinator') {
        <app-coordinator-dashboard></app-coordinator-dashboard>
      }
      @case ('teacher') {
        <app-teacher-dashboard></app-teacher-dashboard>
      }
      @case ('student') {
        <app-student-dashboard></app-student-dashboard>
      }
      @default {
        <!-- Fallback for unknown roles -->
        <div class="min-h-screen bg-gray-50 flex items-center justify-center">
          <div class="text-center">
            <h1 class="text-2xl font-bold text-gray-900 mb-4">Rol no reconocido</h1>
            <p class="text-gray-600 mb-4">Tu rol actual no tiene un dashboard específico.</p>
            <button
              (click)="logout()"
              class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium"
            >
              Cerrar sesión
            </button>
          </div>
        </div>
      }
    }
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
    // Subscribe to user changes
    this.authService.currentUser$.subscribe(user => {
      if (user) {
        this.currentUser.set(user);
        this.loadDashboardData();
      } else {
        // User not logged in, redirect to login
        this.router.navigate(['/auth/login']);
      }
    });
  }

  private loadDashboardData(): void {
    this.isLoading.set(true);
    this.errorMessage.set('');

    this.dashboardService.getDashboardData().subscribe({
      next: (data) => {
        this.dashboardData.set(data);
        this.isLoading.set(false);
      },
      error: (error) => {
        console.error('Error loading dashboard data:', error);
        
        // If it's an authentication error, redirect to login
        if (error.status === 401) {
          console.log('Authentication error, redirecting to login');
          this.authService.logout();
          this.router.navigate(['/auth/login']);
          return;
        }
        
        this.errorMessage.set('Error al cargar los datos del dashboard');
        this.isLoading.set(false);
      }
    });
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}