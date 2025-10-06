import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { AuthService } from './auth.service';

export interface GoogleModeResponse {
  mock_mode: boolean;
  message: string;
}

@Injectable({
  providedIn: 'root'
})
export class GoogleService {
  private readonly API_URL = 'http://localhost:8080';
  private mockModeSubject = new BehaviorSubject<boolean>(false);

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) {
    // Initialize with default mode (real Google API)
    this.mockModeSubject.next(false);
  }

  /**
   * Toggle between Google API mode and Mock mode
   */
  toggleMockMode(enabled: boolean): Observable<GoogleModeResponse> {
    return this.http.post<GoogleModeResponse>(
      `${this.API_URL}/api/google/toggle-mock-mode`,
      { enabled },
      { headers: this.authService.getAuthHeaders() }
    );
  }

  /**
   * Get current mock mode status
   */
  isMockMode(): boolean {
    return this.mockModeSubject.value;
  }

  /**
   * Get mock mode as observable
   */
  getMockMode(): Observable<boolean> {
    return this.mockModeSubject.asObservable();
  }

  /**
   * Set mock mode status
   */
  setMockMode(enabled: boolean): void {
    this.mockModeSubject.next(enabled);
  }

  /**
   * Get system status including Google integration status
   */
  getSystemStatus(): Observable<any> {
    return this.http.get(`${this.API_URL}/api/google/system-status`, {
      headers: this.authService.getAuthHeaders()
    });
  }

  /**
   * Get performance metrics
   */
  getPerformanceMetrics(): Observable<any> {
    return this.http.get(`${this.API_URL}/api/google/performance-metrics`, {
      headers: this.authService.getAuthHeaders()
    });
  }

  /**
   * Get dashboard metrics
   */
  getDashboardMetrics(): Observable<any> {
    return this.http.get(`${this.API_URL}/api/google/dashboard-metrics`, {
      headers: this.authService.getAuthHeaders()
    });
  }
}
