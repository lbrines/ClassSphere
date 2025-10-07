import { Component, OnInit, inject } from '@angular/core';
import { AuthService } from '../../core/services/auth.service';
import { Router } from '@angular/router';
import { UserRole } from '../../core/models/user.model';
import { AdminDashboardComponent } from './pages/admin/admin-dashboard.component';
import { CoordinatorDashboardComponent } from './pages/coordinator/coordinator-dashboard.component';
import { TeacherDashboardComponent } from './pages/teacher/teacher-dashboard.component';
import { StudentDashboardComponent } from './pages/student/student-dashboard.component';
import { NgIf } from '@angular/common';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    NgIf,
    AdminDashboardComponent,
    CoordinatorDashboardComponent,
    TeacherDashboardComponent,
    StudentDashboardComponent
  ],
  template: `
    <div class="dashboard-container">
      <app-admin-dashboard *ngIf="role === 'admin'"></app-admin-dashboard>
      <app-coordinator-dashboard *ngIf="role === 'coordinator'"></app-coordinator-dashboard>
      <app-teacher-dashboard *ngIf="role === 'teacher'"></app-teacher-dashboard>
      <app-student-dashboard *ngIf="role === 'student'"></app-student-dashboard>
    </div>
  `,
  styles: [`
    .dashboard-container {
      width: 100%;
      min-height: 100vh;
    }
  `]
})
export class DashboardComponent implements OnInit {
  private readonly authService = inject(AuthService);
  private readonly router = inject(Router);
  
  role: UserRole = 'student';
  
  ngOnInit() {
    this.authService.currentUser$.subscribe(user => {
      if (user) {
        this.role = user.role;
      } else {
        // If no user, redirect to login
        this.router.navigate(['/auth/login']);
      }
    });
  }
}