import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { DashboardComponent } from './dashboard.component';
import { AuthService } from '../../services/auth.service';
import { DashboardService } from '../../services/dashboard.service';
import { Router } from '@angular/router';
import { of, throwError } from 'rxjs';

describe('DashboardComponent', () => {
  let component: DashboardComponent;
  let fixture: ComponentFixture<DashboardComponent>;
  let mockAuthService: jasmine.SpyObj<AuthService>;
  let mockDashboardService: jasmine.SpyObj<DashboardService>;
  let mockRouter: jasmine.SpyObj<Router>;

  const mockDashboardData = {
    user: {
      id: 1,
      name: 'Test User',
      email: 'test@test.com',
      role: 'admin'
    },
    timestamp: new Date().toISOString(),
    dashboard: {
      type: 'admin',
      welcome_message: 'Welcome Test User',
      stats: {
        total_users: 100,
        total_courses: 20
      },
      recent_activities: [],
      upcoming_deadlines: []
    }
  };

  beforeEach(async () => {
    const authServiceSpy = jasmine.createSpyObj('AuthService', ['currentUser', 'isAuthenticated', 'logout']);
    const dashboardServiceSpy = jasmine.createSpyObj('DashboardService', ['getDashboardData']);
    const routerSpy = jasmine.createSpyObj('Router', ['navigate']);

    await TestBed.configureTestingModule({
      imports: [
        DashboardComponent,
        HttpClientTestingModule,
        RouterTestingModule
      ],
      providers: [
        { provide: AuthService, useValue: authServiceSpy },
        { provide: DashboardService, useValue: dashboardServiceSpy },
        { provide: Router, useValue: routerSpy }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(DashboardComponent);
    component = fixture.componentInstance;
    mockAuthService = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
    mockDashboardService = TestBed.inject(DashboardService) as jasmine.SpyObj<DashboardService>;
    mockRouter = TestBed.inject(Router) as jasmine.SpyObj<Router>;

    // Setup default mocks
    mockAuthService.currentUser.and.returnValue({ id: 1, role: 'admin', name: 'Test User', email: 'test@test.com', is_active: true });
    mockAuthService.isAuthenticated.and.returnValue(true);
    mockDashboardService.getDashboardData.and.returnValue(of(mockDashboardData));
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize with current user', () => {
    component.ngOnInit();
    expect(mockAuthService.currentUser).toHaveBeenCalled();
    expect(component.currentUser()).toEqual({ id: 1, role: 'admin', name: 'Test User', email: 'test@test.com', is_active: true });
  });

  it('should load dashboard data on init', () => {
    component.ngOnInit();
    expect(mockDashboardService.getDashboardData).toHaveBeenCalled();
    expect(component.dashboardData()).toEqual(mockDashboardData);
    expect(component.isLoading()).toBeFalse();
  });

  it('should display admin dashboard for admin role', () => {
    mockAuthService.currentUser.and.returnValue({ id: 1, role: 'admin', name: 'Admin User', email: 'admin@test.com', is_active: true });
    component.ngOnInit();
    fixture.detectChanges();
    
    const adminDashboard = fixture.nativeElement.querySelector('app-admin-dashboard');
    expect(adminDashboard).toBeTruthy();
  });

  it('should display coordinator dashboard for coordinator role', () => {
    mockAuthService.currentUser.and.returnValue({ id: 1, role: 'coordinator', name: 'Coordinator User', email: 'coordinator@test.com', is_active: true });
    component.ngOnInit();
    fixture.detectChanges();
    
    const coordinatorDashboard = fixture.nativeElement.querySelector('app-coordinator-dashboard');
    expect(coordinatorDashboard).toBeTruthy();
  });

  it('should display teacher dashboard for teacher role', () => {
    mockAuthService.currentUser.and.returnValue({ id: 1, role: 'teacher', name: 'Teacher User', email: 'teacher@test.com', is_active: true });
    component.ngOnInit();
    fixture.detectChanges();
    
    const teacherDashboard = fixture.nativeElement.querySelector('app-teacher-dashboard');
    expect(teacherDashboard).toBeTruthy();
  });

  it('should display student dashboard for student role', () => {
    mockAuthService.currentUser.and.returnValue({ id: 1, role: 'student', name: 'Student User', email: 'student@test.com', is_active: true });
    component.ngOnInit();
    fixture.detectChanges();
    
    const studentDashboard = fixture.nativeElement.querySelector('app-student-dashboard');
    expect(studentDashboard).toBeTruthy();
  });

  it('should display fallback message for unknown role', () => {
    mockAuthService.currentUser.and.returnValue({ id: 1, role: 'unknown', name: 'Unknown User', email: 'unknown@test.com', is_active: true });
    component.ngOnInit();
    fixture.detectChanges();
    
    const fallbackMessage = fixture.nativeElement.querySelector('h1');
    expect(fallbackMessage).toBeTruthy();
    expect(fallbackMessage.textContent).toContain('Rol no reconocido');
  });

  it('should display fallback message for null user', () => {
    mockAuthService.currentUser.and.returnValue(null);
    component.ngOnInit();
    fixture.detectChanges();
    
    const fallbackMessage = fixture.nativeElement.querySelector('h1');
    expect(fallbackMessage).toBeTruthy();
    expect(fallbackMessage.textContent).toContain('Rol no reconocido');
  });

  it('should logout and navigate to login', () => {
    component.logout();
    expect(mockAuthService.logout).toHaveBeenCalled();
    expect(mockRouter.navigate).toHaveBeenCalledWith(['/login']);
  });

  it('should handle dashboard data loading error', () => {
    const error = new Error('Failed to load dashboard data');
    mockDashboardService.getDashboardData.and.returnValue(throwError(() => error));
    
    component.ngOnInit();
    
    expect(component.errorMessage()).toBe('Error al cargar los datos del dashboard');
    expect(component.isLoading()).toBeFalse();
  });

  it('should set loading state correctly during data load', () => {
    let loadingStates: boolean[] = [];
    
    // Mock the service to track loading states
    mockDashboardService.getDashboardData.and.callFake(() => {
      loadingStates.push(component.isLoading());
      return of(mockDashboardData);
    });
    
    component.ngOnInit();
    
    // Should start with loading true, then false after data loads
    expect(loadingStates).toContain(true);
    expect(component.isLoading()).toBeFalse();
  });

  it('should clear error message when loading new data', () => {
    // First set an error
    component.errorMessage.set('Previous error');
    
    // Then load new data
    component.ngOnInit();
    
    expect(component.errorMessage()).toBe('');
  });

  it('should display loading spinner when loading', () => {
    component.isLoading.set(true);
    fixture.detectChanges();
    
    const loadingSpinner = fixture.nativeElement.querySelector('.animate-spin');
    expect(loadingSpinner).toBeTruthy();
  });

  it('should display error message when error occurs', () => {
    component.errorMessage.set('Test error message');
    fixture.detectChanges();
    
    const errorElement = fixture.nativeElement.querySelector('.text-red-700');
    expect(errorElement).toBeTruthy();
    expect(errorElement.textContent).toContain('Test error message');
  });

  it('should display appropriate dashboard based on role switch', () => {
    // Start with admin role
    mockAuthService.currentUser.and.returnValue({ id: 1, role: 'admin', name: 'Admin User', email: 'admin@test.com', is_active: true });
    component.ngOnInit();
    fixture.detectChanges();
    
    let adminDashboard = fixture.nativeElement.querySelector('app-admin-dashboard');
    expect(adminDashboard).toBeTruthy();
    
    // Switch to student role
    mockAuthService.currentUser.and.returnValue({ id: 1, role: 'student', name: 'Student User', email: 'student@test.com', is_active: true });
    component.ngOnInit();
    fixture.detectChanges();
    
    const studentDashboard = fixture.nativeElement.querySelector('app-student-dashboard');
    expect(studentDashboard).toBeTruthy();
    
    // Admin dashboard should no longer be present
    adminDashboard = fixture.nativeElement.querySelector('app-admin-dashboard');
    expect(adminDashboard).toBeFalsy();
  });

  it('should handle empty dashboard data gracefully', () => {
    const emptyData = {
      user: { id: 1, name: 'Test User', email: 'test@test.com', role: 'admin' },
      timestamp: new Date().toISOString(),
      dashboard: {
        type: 'admin',
        welcome_message: 'Welcome Test User',
        stats: {
          total_users: 0,
          total_courses: 0
        },
        recent_activities: [],
        upcoming_deadlines: []
      }
    };
    
    mockDashboardService.getDashboardData.and.returnValue(of(emptyData));
    component.ngOnInit();
    
    expect(component.dashboardData()).toEqual(emptyData);
    expect(component.isLoading()).toBeFalse();
  });

  it('should handle undefined user gracefully', () => {
    mockAuthService.currentUser.and.returnValue(null);
    component.ngOnInit();
    fixture.detectChanges();
    
    const fallbackMessage = fixture.nativeElement.querySelector('h1');
    expect(fallbackMessage).toBeTruthy();
    expect(fallbackMessage.textContent).toContain('Rol no reconocido');
  });
});
