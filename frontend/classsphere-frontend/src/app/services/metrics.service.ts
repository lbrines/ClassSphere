import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject, combineLatest } from 'rxjs';
import { map, tap, catchError, shareReplay } from 'rxjs/operators';
import { of } from 'rxjs';
import { MetricsCacheService } from '../shared/services/metrics-cache.service';

export interface DashboardMetrics {
  course_metrics: CourseMetrics;
  student_metrics: StudentMetrics;
  assignment_metrics: AssignmentMetrics;
  role_specific: any;
}

export interface CourseMetrics {
  total_courses: number;
  active_courses: number;
  archived_courses: number;
  total_students: number;
  average_grade: number;
  total_assignments: number;
}

export interface StudentMetrics {
  total_students: number;
  active_students: number;
}

export interface AssignmentMetrics {
  total_assignments: number;
  published_assignments: number;
  draft_assignments: number;
  total_points: number;
  average_points: number;
}

export interface PerformanceMetrics {
  completion_rate: number;
  average_grade: number;
  engagement_score: number;
  productivity_index: number;
  trends: {
    grade_trend: string;
    participation: string;
    completion_rate: string;
  };
}

export interface ChartDataPoint {
  label: string;
  value: number;
  color?: string;
}

export interface MetricCardData {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: string;
  trend?: {
    value: number;
    direction: 'up' | 'down' | 'neutral';
    label?: string;
  };
  color?: 'blue' | 'green' | 'red' | 'yellow' | 'purple' | 'indigo';
  format?: 'number' | 'percentage' | 'currency' | 'text';
}

export interface ChartData {
  labels: string[];
  datasets: {
    label: string;
    data: number[];
    backgroundColor?: string | string[];
    borderColor?: string | string[];
    borderWidth?: number;
  }[];
}

@Injectable({
  providedIn: 'root'
})
export class MetricsService {
  private baseUrl = 'http://localhost:8080/api';
  
  // BehaviorSubjects for reactive data
  private dashboardMetrics$ = new BehaviorSubject<DashboardMetrics | null>(null);
  private performanceMetrics$ = new BehaviorSubject<PerformanceMetrics | null>(null);
  private loading$ = new BehaviorSubject<boolean>(false);

  constructor(
    private http: HttpClient,
    private cacheService: MetricsCacheService
  ) {}

  // Getters for reactive data
  get dashboardMetrics() { return this.dashboardMetrics$.asObservable(); }
  get performanceMetrics() { return this.performanceMetrics$.asObservable(); }
  get loading() { return this.loading$.asObservable(); }

  /**
   * Get dashboard metrics for the current user with caching
   */
  getDashboardMetrics(): Observable<DashboardMetrics> {
    return this.cacheService.get(
      'dashboard_metrics',
      () => {
        this.loading$.next(true);
        return this.http.get<DashboardMetrics>(`${this.baseUrl}/google/dashboard/metrics`)
          .pipe(
            tap(metrics => {
              this.dashboardMetrics$.next(metrics);
              this.loading$.next(false);
            }),
            catchError(error => {
              console.error('Error fetching dashboard metrics:', error);
              this.loading$.next(false);
              // Return mock data on error
              return of(this.getMockDashboardMetrics());
            })
          );
      },
      3 * 60 * 1000 // 3 minutes cache
    );
  }

  /**
   * Get performance metrics with caching
   */
  getPerformanceMetrics(): Observable<PerformanceMetrics> {
    return this.cacheService.get(
      'performance_metrics',
      () => {
        this.loading$.next(true);
        return this.http.get<PerformanceMetrics>(`${this.baseUrl}/google/performance/metrics`)
          .pipe(
            tap(metrics => {
              this.performanceMetrics$.next(metrics);
              this.loading$.next(false);
            }),
            catchError(error => {
              console.error('Error fetching performance metrics:', error);
              this.loading$.next(false);
              // Return mock data on error
              return of(this.getMockPerformanceMetrics());
            })
          );
      },
      5 * 60 * 1000 // 5 minutes cache
    );
  }

  /**
   * Get metrics for a specific role
   */
  getRoleMetrics(role: string): Observable<any> {
    return this.dashboardMetrics.pipe(
      map(metrics => {
        if (!metrics) return null;
        return metrics.role_specific;
      })
    );
  }

  /**
   * Convert course metrics to chart data
   */
  getCourseMetricsChartData(metrics: CourseMetrics): ChartDataPoint[] {
    return [
      { label: 'Active Courses', value: metrics.active_courses, color: '#10B981' },
      { label: 'Archived Courses', value: metrics.archived_courses, color: '#6B7280' }
    ];
  }

  /**
   * Convert student metrics to chart data
   */
  getStudentMetricsChartData(metrics: StudentMetrics): ChartDataPoint[] {
    return [
      { label: 'Active Students', value: metrics.active_students, color: '#3B82F6' },
      { label: 'Inactive Students', value: metrics.total_students - metrics.active_students, color: '#EF4444' }
    ];
  }

  /**
   * Convert assignment metrics to chart data
   */
  getAssignmentMetricsChartData(metrics: AssignmentMetrics): ChartDataPoint[] {
    return [
      { label: 'Published', value: metrics.published_assignments, color: '#10B981' },
      { label: 'Draft', value: metrics.draft_assignments, color: '#F59E0B' }
    ];
  }

  /**
   * Get performance trends chart data
   */
  getPerformanceTrendsChartData(metrics: PerformanceMetrics): ChartDataPoint[] {
    return [
      { label: 'Completion Rate', value: metrics.completion_rate, color: '#10B981' },
      { label: 'Average Grade', value: metrics.average_grade, color: '#3B82F6' },
      { label: 'Engagement', value: metrics.engagement_score, color: '#8B5CF6' },
      { label: 'Productivity', value: metrics.productivity_index, color: '#F59E0B' }
    ];
  }

  /**
   * Get grade distribution data (mock)
   */
  getGradeDistributionData(): ChartDataPoint[] {
    return [
      { label: 'A (90-100)', value: 25, color: '#10B981' },
      { label: 'B (80-89)', value: 35, color: '#3B82F6' },
      { label: 'C (70-79)', value: 25, color: '#F59E0B' },
      { label: 'D (60-69)', value: 10, color: '#EF4444' },
      { label: 'F (<60)', value: 5, color: '#DC2626' }
    ];
  }

  /**
   * Get monthly activity data (mock)
   */
  getMonthlyActivityData(): { labels: string[], datasets: any[] } {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
    
    return {
      labels: months,
      datasets: [
        {
          label: 'Assignments Submitted',
          data: [120, 135, 148, 142, 156, 163],
          backgroundColor: '#3B82F6',
          borderColor: '#1D4ED8'
        },
        {
          label: 'Grades Given',
          data: [98, 112, 125, 118, 134, 141],
          backgroundColor: '#10B981',
          borderColor: '#047857'
        }
      ]
    };
  }

  /**
   * Refresh all metrics
   */
  refreshMetrics(): Observable<any> {
    return combineLatest([
      this.getDashboardMetrics(),
      this.getPerformanceMetrics()
    ]);
  }

  /**
   * Mock data for development/fallback
   */
  private getMockDashboardMetrics(): DashboardMetrics {
    return {
      course_metrics: {
        total_courses: 15,
        active_courses: 12,
        archived_courses: 3,
        total_students: 240,
        average_grade: 85.5,
        total_assignments: 72
      },
      student_metrics: {
        total_students: 240,
        active_students: 228
      },
      assignment_metrics: {
        total_assignments: 72,
        published_assignments: 65,
        draft_assignments: 7,
        total_points: 7200,
        average_points: 100
      },
      role_specific: {
        role: 'student',
        base: {},
        specific: {
          my_courses: 3,
          pending_assignments: 5,
          completed_assignments: 12,
          average_grade: 85.5
        }
      }
    };
  }

  private getMockPerformanceMetrics(): PerformanceMetrics {
    return {
      completion_rate: 85.0,
      average_grade: 85.5,
      engagement_score: 78.2,
      productivity_index: 82.1,
      trends: {
        grade_trend: 'increasing',
        participation: 'stable',
        completion_rate: 'improving'
      }
    };
  }
}
