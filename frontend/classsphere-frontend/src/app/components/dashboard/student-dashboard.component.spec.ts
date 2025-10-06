import { ComponentFixture, TestBed } from '@angular/core/testing';
import { StudentDashboardComponent } from './student-dashboard.component';
import { AuthService } from '../../services/auth.service';
import { DashboardService } from '../../services/dashboard.service';
import { Router } from '@angular/router';
import { of } from 'rxjs';

describe('StudentDashboardComponent', () => {
  let component: StudentDashboardComponent;
  let fixture: ComponentFixture<StudentDashboardComponent>;
  let mockAuthService: jasmine.SpyObj<AuthService>;
  let mockDashboardService: jasmine.SpyObj<DashboardService>;
  let mockRouter: jasmine.SpyObj<Router>;

  const mockStudentMetrics = {
    user: {
      id: 1,
      name: 'Student User',
      email: 'student@test.com',
      role: 'student'
    },
    timestamp: new Date().toISOString(),
    dashboard: {
      type: 'student',
      welcome_message: 'Welcome Student',
      stats: {
        total_courses: 4,
        total_assignments: 20,
        completed_assignments: 15,
        pending_assignments: 5,
        average_grade: '88.5'
      },
      recent_activities: [],
      upcoming_deadlines: [],
      study_recommendations: []
    }
  };

  beforeEach(async () => {
    const authServiceSpy = jasmine.createSpyObj('AuthService', ['currentUser', 'isAuthenticated']);
    const dashboardServiceSpy = jasmine.createSpyObj('DashboardService', ['getDashboardData']);
    const routerSpy = jasmine.createSpyObj('Router', ['navigate']);

    await TestBed.configureTestingModule({
      imports: [StudentDashboardComponent],
      providers: [
        { provide: AuthService, useValue: authServiceSpy },
        { provide: DashboardService, useValue: dashboardServiceSpy },
        { provide: Router, useValue: routerSpy }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(StudentDashboardComponent);
    component = fixture.componentInstance;
    mockAuthService = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
    mockDashboardService = TestBed.inject(DashboardService) as jasmine.SpyObj<DashboardService>;
    mockRouter = TestBed.inject(Router) as jasmine.SpyObj<Router>;

    // Setup default mocks
    mockAuthService.currentUser.and.returnValue({ id: 1, role: 'student', name: 'Student User', email: 'student@test.com', is_active: true });
    mockAuthService.isAuthenticated.and.returnValue(true);
    mockDashboardService.getDashboardData.and.returnValue(of(mockStudentMetrics));
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should display student metrics', () => {
    component.ngOnInit();
    fixture.detectChanges();
    
    const compiled = fixture.nativeElement;
    expect(compiled.querySelector('.enrolled-courses')).toBeTruthy();
    expect(compiled.querySelector('.total-assignments')).toBeTruthy();
    expect(compiled.querySelector('.completed-assignments')).toBeTruthy();
  });

  it('should load data on init', () => {
    component.ngOnInit();
    expect(mockDashboardService.getDashboardData).toHaveBeenCalled();
  });

  it('should get student stats correctly', () => {
    component.ngOnInit();
    fixture.detectChanges();
    
    const stats = component.getStudentStats();
    expect(stats).toBeDefined();
    expect(stats.length).toBeGreaterThan(0);
    expect(stats[0].value).toBe(4); // enrolledCourses
  });

  it('should get stat icon class correctly', () => {
    const iconClass = component.getStatIconClass('average_grade');
    expect(iconClass).toContain('bg-purple-500');
  });

  it('should format date correctly', () => {
    const date = new Date('2025-10-06T19:25:00Z');
    const formatted = component.formatDate(date.toISOString());
    expect(formatted).toContain('2025');
  });
});
