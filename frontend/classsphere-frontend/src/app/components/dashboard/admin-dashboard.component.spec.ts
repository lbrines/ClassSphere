import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AdminDashboardComponent } from './admin-dashboard.component';
import { AuthService } from '../../services/auth.service';
import { DashboardService } from '../../services/dashboard.service';
import { Router } from '@angular/router';
import { of } from 'rxjs';

describe('AdminDashboardComponent', () => {
  let component: AdminDashboardComponent;
  let fixture: ComponentFixture<AdminDashboardComponent>;
  let mockAuthService: jasmine.SpyObj<AuthService>;
  let mockDashboardService: jasmine.SpyObj<DashboardService>;
  let mockRouter: jasmine.SpyObj<Router>;

  const mockAdminMetrics = {
    user: {
      id: 1,
      name: 'Admin User',
      email: 'admin@test.com',
      role: 'admin'
    },
    timestamp: new Date().toISOString(),
    dashboard: {
      type: 'admin',
      welcome_message: 'Welcome Admin',
      stats: {
        total_users: 150,
        total_courses: 25,
        total_students: 1200,
        total_teachers: 50,
        total_assignments: 500,
        average_grade: '85.5',
        system_uptime: '99.9%',
        active_sessions: 45,
        storage_used: '2.5GB',
        api_calls: '1.2M'
      },
      recent_activities: [],
      upcoming_deadlines: [],
      system_alerts: []
    }
  };

  beforeEach(async () => {
    const authServiceSpy = jasmine.createSpyObj('AuthService', ['currentUser', 'isAuthenticated']);
    const dashboardServiceSpy = jasmine.createSpyObj('DashboardService', ['getDashboardData']);
    const routerSpy = jasmine.createSpyObj('Router', ['navigate']);

    await TestBed.configureTestingModule({
      imports: [AdminDashboardComponent],
      providers: [
        { provide: AuthService, useValue: authServiceSpy },
        { provide: DashboardService, useValue: dashboardServiceSpy },
        { provide: Router, useValue: routerSpy }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(AdminDashboardComponent);
    component = fixture.componentInstance;
    mockAuthService = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
    mockDashboardService = TestBed.inject(DashboardService) as jasmine.SpyObj<DashboardService>;
    mockRouter = TestBed.inject(Router) as jasmine.SpyObj<Router>;

    // Setup default mocks
    mockAuthService.currentUser.and.returnValue({ id: 1, role: 'admin', name: 'Admin User', email: 'admin@test.com', is_active: true });
    mockAuthService.isAuthenticated.and.returnValue(true);
    mockDashboardService.getDashboardData.and.returnValue(of(mockAdminMetrics));
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should display all admin metrics', () => {
    component.ngOnInit();
    fixture.detectChanges();
    
    const compiled = fixture.nativeElement;
    expect(compiled.querySelector('.total-users')).toBeTruthy();
    expect(compiled.querySelector('.total-courses')).toBeTruthy();
    expect(compiled.querySelector('.total-students')).toBeTruthy();
    expect(compiled.querySelector('.total-teachers')).toBeTruthy();
  });

  it('should load data on init', () => {
    component.ngOnInit();
    expect(mockDashboardService.getDashboardData).toHaveBeenCalled();
  });

  it('should get system stats correctly', () => {
    component.ngOnInit();
    fixture.detectChanges();
    
    const stats = component.getSystemStats();
    expect(stats).toBeDefined();
    expect(stats.length).toBeGreaterThan(0);
    expect(stats[0].value).toBe(150); // totalUsers
  });

  it('should get stat icon class correctly', () => {
    const iconClass = component.getStatIconClass('total_users');
    expect(iconClass).toContain('bg-indigo-500');
  });

  it('should format date correctly', () => {
    const date = new Date('2025-10-06T19:25:00Z');
    const formatted = component.formatDate(date.toISOString());
    expect(formatted).toContain('2025');
  });

  it('should handle export complete', () => {
    const result = { success: true, filename: 'test.pdf' };
    expect(() => component.onExportComplete(result)).not.toThrow();
  });

  it('should handle export error', () => {
    const result = { success: false, error: 'Export failed' };
    expect(() => component.onExportComplete(result)).not.toThrow();
  });
});
