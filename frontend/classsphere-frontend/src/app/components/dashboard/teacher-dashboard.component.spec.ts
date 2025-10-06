import { ComponentFixture, TestBed } from '@angular/core/testing';
import { TeacherDashboardComponent } from './teacher-dashboard.component';
import { AuthService } from '../../services/auth.service';
import { DashboardService } from '../../services/dashboard.service';
import { Router } from '@angular/router';
import { of } from 'rxjs';

describe('TeacherDashboardComponent', () => {
  let component: TeacherDashboardComponent;
  let fixture: ComponentFixture<TeacherDashboardComponent>;
  let mockAuthService: jasmine.SpyObj<AuthService>;
  let mockDashboardService: jasmine.SpyObj<DashboardService>;
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
    const routerSpy = jasmine.createSpyObj('Router', ['navigate']);

    await TestBed.configureTestingModule({
      imports: [TeacherDashboardComponent],
      providers: [
        { provide: AuthService, useValue: authServiceSpy },
        { provide: DashboardService, useValue: dashboardServiceSpy },
        { provide: Router, useValue: routerSpy }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(TeacherDashboardComponent);
    component = fixture.componentInstance;
    mockAuthService = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
    mockDashboardService = TestBed.inject(DashboardService) as jasmine.SpyObj<DashboardService>;
    mockRouter = TestBed.inject(Router) as jasmine.SpyObj<Router>;

    // Setup default mocks
    mockAuthService.currentUser.and.returnValue({ id: 1, role: 'teacher', name: 'Teacher User', email: 'teacher@test.com', is_active: true });
    mockAuthService.isAuthenticated.and.returnValue(true);
    mockDashboardService.getDashboardData.and.returnValue(of(mockTeacherMetrics));
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
