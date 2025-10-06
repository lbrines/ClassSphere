import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';

export interface DashboardData {
  user: {
    id: number;
    name: string;
    email: string;
    role: string;
  };
  dashboard: {
    type: string;
    welcome_message: string;
    stats: {
      total_users?: number;
      total_courses?: number;
      total_students?: number;
      total_teachers?: number;
      total_assignments?: number;
      completed_assignments?: number;
      pending_assignments?: number;
      average_grade?: string;
      system_uptime?: string;
      active_sessions?: number;
      storage_used?: string;
      api_calls?: string;
    };
    recent_activities: any[];
    upcoming_deadlines?: any[];
    upcoming_tasks?: any[];
    system_alerts?: any[];
    courses?: any[];
    students_at_risk?: any[];
    teacher_performance?: any[];
    programs?: any[];
    grade_distribution?: any[];
    study_recommendations?: any[];
  };
  timestamp: string;
}

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  private readonly API_URL = 'http://localhost:8080';

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) {}

  getStudentDashboard(): Observable<DashboardData> {
    return this.http.get<DashboardData>(`${this.API_URL}/api/dashboard/student`, {
      headers: this.authService.getAuthHeaders()
    });
  }

  getTeacherDashboard(): Observable<DashboardData> {
    return this.http.get<DashboardData>(`${this.API_URL}/api/dashboard/teacher`, {
      headers: this.authService.getAuthHeaders()
    });
  }

  getCoordinatorDashboard(): Observable<DashboardData> {
    return this.http.get<DashboardData>(`${this.API_URL}/api/dashboard/coordinator`, {
      headers: this.authService.getAuthHeaders()
    });
  }

  getAdminDashboard(): Observable<DashboardData> {
    return this.http.get<DashboardData>(`${this.API_URL}/api/dashboard/admin`, {
      headers: this.authService.getAuthHeaders()
    });
  }

  getDashboardByRole(role: string): Observable<DashboardData> {
    switch (role.toLowerCase()) {
      case 'student':
        return this.getStudentDashboard();
      case 'teacher':
        return this.getTeacherDashboard();
      case 'coordinator':
        return this.getCoordinatorDashboard();
      case 'admin':
        return this.getAdminDashboard();
      default:
        return this.getStudentDashboard();
    }
  }

  getDashboardData(): Observable<DashboardData> {
    const currentUser = this.authService.currentUser();
    if (!currentUser) {
      throw new Error('No user logged in');
    }
    
    // Check if token is available
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('No authentication token available');
    }
    
    return this.getDashboardByRole(currentUser.role);
  }
}
