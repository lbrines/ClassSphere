import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { TeacherDashboardComponent } from './teacher-dashboard.component';
import { AuthService } from '../../services/auth.service';
import { DashboardService } from '../../services/dashboard.service';
import { MetricsService } from '../../services/metrics.service';
import { Router } from '@angular/router';
import { of } from 'rxjs';

describe('TeacherDashboardComponent', () => {
  let component: TeacherDashboardComponent;
  let fixture: ComponentFixture<TeacherDashboardComponent>;
  let mockAuthService: jasmine.SpyObj<AuthService>;
  let mockDashboardService: jasmine.SpyObj<DashboardService>;
  let mockMetricsService: jasmine.SpyObj<MetricsService>;
  let mockRouter: jasmine.SpyObj<Router>;

  const mockTeacherMetrics = {
    user: {
      id: 1,
      name: 'Teacher User',
      email: 'teacher@test.com',
      role: 'teacher'
    },
    timestamp: new Date().toISOString(),
    dashboard: {
      type: 'teacher',
      welcome_message: 'Welcome Teacher',
      stats: {
        total_courses: 5,
        total_students: 120,
        total_assignments: 50,
        completed_assignments: 45,
        pending_assignments: 5,
        average_grade: '87.2'
      },
      recent_activities: [],
      upcoming_deadlines: [],
      courses: []
    }
  };

  beforeEach(async () => {
    const authServiceSpy = jasmine.createSpyObj('AuthService', ['currentUser', 'isAuthenticated']);
    const dashboardServiceSpy = jasmine.createSpyObj('DashboardService', ['getDashboardData']);
    const metricsServiceSpy = jasmine.createSpyObj('MetricsService', ['getDashboardMetrics', 'getPerformanceMetrics', 'getRoleMetrics']);
    const routerSpy = jasmine.createSpyObj('Router', ['navigate']);

    await TestBed.configureTestingModule({
      imports: [
        TeacherDashboardComponent,
        HttpClientTestingModule,
        RouterTestingModule
      ],
      providers: [
        { provide: AuthService, useValue: authServiceSpy },
        { provide: DashboardService, useValue: dashboardServiceSpy },
        { provide: MetricsService, useValue: metricsServiceSpy },
        { provide: Router, useValue: routerSpy }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(TeacherDashboardComponent);
    component = fixture.componentInstance;
    mockAuthService = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
    mockDashboardService = TestBed.inject(DashboardService) as jasmine.SpyObj<DashboardService>;
    mockMetricsService = TestBed.inject(MetricsService) as jasmine.SpyObj<MetricsService>;
    mockRouter = TestBed.inject(Router) as jasmine.SpyObj<Router>;

    // Setup default mocks
    mockAuthService.currentUser.and.returnValue({ id: 1, role: 'teacher', name: 'Teacher User', email: 'teacher@test.com', is_active: true });
    mockAuthService.isAuthenticated.and.returnValue(true);
    mockDashboardService.getDashboardData.and.returnValue(of(mockTeacherMetrics));
    mockMetricsService.getDashboardMetrics.and.returnValue(of({
      course_metrics: {
        total_courses: 3,
        active_courses: 3,
        archived_courses: 0,
        total_students: 45,
        average_grade: 87.8,
        total_assignments: 20
      },
      student_metrics: {
        total_students: 45,
        active_students: 42
      },
      assignment_metrics: {
        total_assignments: 20,
        published_assignments: 18,
        draft_assignments: 2,
        total_points: 2000,
        average_points: 100
      },
      role_specific: mockTeacherMetrics.dashboard.stats
    }));
    mockMetricsService.getPerformanceMetrics.and.returnValue(of({
      completion_rate: 85.2,
      average_grade: 87.8,
      engagement_score: 89.5,
      productivity_index: 86.3,
      trends: {
        grade_trend: 'up',
        participation: 'stable',
        completion_rate: 'up'
      }
    }));
    mockMetricsService.getRoleMetrics.and.returnValue(of([
      { title: 'My Courses', value: 3, icon: 'book', color: 'bg-blue-500' },
      { title: 'Total Students', value: 45, icon: 'users', color: 'bg-green-500' }
    ]));
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should display teacher metrics', () => {
    component.ngOnInit();
    fixture.detectChanges();
    
    const compiled = fixture.nativeElement;
    expect(compiled.querySelector('.my-courses')).toBeTruthy();
    expect(compiled.querySelector('.total-students')).toBeTruthy();
    expect(compiled.querySelector('.total-assignments')).toBeTruthy();
  });

  it('should load data on init', () => {
    component.ngOnInit();
    expect(mockDashboardService.getDashboardData).toHaveBeenCalled();
  });

  it('should get teacher stats correctly', () => {
    component.ngOnInit();
    fixture.detectChanges();
    
    const stats = component.getTeacherStats();
    expect(stats).toBeDefined();
    expect(stats.length).toBeGreaterThan(0);
    expect(stats[0].value).toBe(5); // myCourses
  });

  it('should get stat icon class correctly', () => {
    const iconClass = component.getStatIconClass('my_courses');
    expect(iconClass).toContain('bg-blue-500');
  });

  it('should format date correctly', () => {
    const date = new Date('2025-10-06T19:25:00Z');
    const formatted = component.formatDate(date.toISOString());
    expect(formatted).toContain('2025');
  });
});
