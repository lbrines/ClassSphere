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
    stats: any;
    recent_activities: any[];
    upcoming_deadlines?: any[];
    upcoming_tasks?: any[];
    system_alerts?: any[];
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
}
