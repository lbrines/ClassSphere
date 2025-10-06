import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { CoordinatorDashboardComponent } from './coordinator-dashboard.component';
import { AuthService } from '../../services/auth.service';
import { DashboardService } from '../../services/dashboard.service';
import { MetricsService } from '../../services/metrics.service';
import { Router } from '@angular/router';
import { of } from 'rxjs';

describe('CoordinatorDashboardComponent', () => {
  let component: CoordinatorDashboardComponent;
  let fixture: ComponentFixture<CoordinatorDashboardComponent>;
  let mockAuthService: jasmine.SpyObj<AuthService>;
  let mockDashboardService: jasmine.SpyObj<DashboardService>;
  let mockMetricsService: jasmine.SpyObj<MetricsService>;
  let mockRouter: jasmine.SpyObj<Router>;

  const mockCoordinatorMetrics = {
    user: {
      id: 1,
      name: 'Coordinator User',
      email: 'coordinator@test.com',
      role: 'coordinator'
    },
    timestamp: new Date().toISOString(),
    dashboard: {
      type: 'coordinator',
      welcome_message: 'Welcome Coordinator',
      stats: {
        total_courses: 10,
        total_teachers: 8,
        total_students: 200,
        total_assignments: 100,
        completed_assignments: 90,
        pending_assignments: 10,
        average_grade: '86.3'
      },
      recent_activities: [],
      upcoming_deadlines: [],
      programs: [],
      grade_distribution: []
    }
  };

  beforeEach(async () => {
    const authServiceSpy = jasmine.createSpyObj('AuthService', ['currentUser', 'isAuthenticated']);
    const dashboardServiceSpy = jasmine.createSpyObj('DashboardService', ['getDashboardData']);
    const metricsServiceSpy = jasmine.createSpyObj('MetricsService', ['getDashboardMetrics', 'getPerformanceMetrics', 'getRoleMetrics']);
    const routerSpy = jasmine.createSpyObj('Router', ['navigate']);

    await TestBed.configureTestingModule({
      imports: [
        CoordinatorDashboardComponent,
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

    fixture = TestBed.createComponent(CoordinatorDashboardComponent);
    component = fixture.componentInstance;
    mockAuthService = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
    mockDashboardService = TestBed.inject(DashboardService) as jasmine.SpyObj<DashboardService>;
    mockMetricsService = TestBed.inject(MetricsService) as jasmine.SpyObj<MetricsService>;
    mockRouter = TestBed.inject(Router) as jasmine.SpyObj<Router>;

    // Setup default mocks
    mockAuthService.currentUser.and.returnValue({ id: 1, role: 'coordinator', name: 'Coordinator User', email: 'coordinator@test.com', is_active: true });
    mockAuthService.isAuthenticated.and.returnValue(true);
    mockDashboardService.getDashboardData.and.returnValue(of(mockCoordinatorMetrics));
    mockMetricsService.getDashboardMetrics.and.returnValue(of({
      course_metrics: {
        total_courses: 12,
        active_courses: 10,
        archived_courses: 2,
        total_students: 200,
        average_grade: 86.9,
        total_assignments: 120
      },
      student_metrics: {
        total_students: 200,
        active_students: 185
      },
      assignment_metrics: {
        total_assignments: 120,
        published_assignments: 110,
        draft_assignments: 10,
        total_points: 12000,
        average_points: 100
      },
      role_specific: mockCoordinatorMetrics.dashboard.stats
    }));
    mockMetricsService.getPerformanceMetrics.and.returnValue(of({
      completion_rate: 87.3,
      average_grade: 86.9,
      engagement_score: 88.7,
      productivity_index: 87.1,
      trends: {
        grade_trend: 'up',
        participation: 'stable',
        completion_rate: 'up'
      }
    }));
    mockMetricsService.getRoleMetrics.and.returnValue(of([
      { title: 'Department Courses', value: 12, icon: 'book', color: 'bg-purple-500' },
      { title: 'Department Teachers', value: 8, icon: 'users', color: 'bg-blue-500' }
    ]));
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should display coordinator metrics', () => {
    component.ngOnInit();
    fixture.detectChanges();
    
    const compiled = fixture.nativeElement;
    expect(compiled.querySelector('.managed-courses')).toBeTruthy();
    expect(compiled.querySelector('.total-teachers')).toBeTruthy();
    expect(compiled.querySelector('.total-students')).toBeTruthy();
  });

  it('should load data on init', () => {
    component.ngOnInit();
    expect(mockDashboardService.getDashboardData).toHaveBeenCalled();
  });

  it('should get coordinator stats correctly', () => {
    component.ngOnInit();
    fixture.detectChanges();
    
    const stats = component.getCoordinatorStats();
    expect(stats).toBeDefined();
    expect(stats.length).toBeGreaterThan(0);
    expect(stats[0].value).toBe(10); // managedCourses
  });

  it('should get stat icon class correctly', () => {
    const iconClass = component.getStatIconClass('total_courses');
    expect(iconClass).toContain('bg-green-500');
  });

  it('should format date correctly', () => {
    const date = new Date('2025-10-06T19:25:00Z');
    const formatted = component.formatDate(date.toISOString());
    expect(formatted).toContain('2025');
  });
});
