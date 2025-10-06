import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { BaseDashboardComponent } from './base-dashboard.component';
import { AuthService } from '../../services/auth.service';
import { DashboardService } from '../../services/dashboard.service';
import { Router } from '@angular/router';
import { of, throwError } from 'rxjs';

describe('BaseDashboardComponent', () => {
  let component: BaseDashboardComponent;
  let fixture: ComponentFixture<BaseDashboardComponent>;
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
        BaseDashboardComponent,
        HttpClientTestingModule,
        RouterTestingModule
      ],
      providers: [
        { provide: AuthService, useValue: authServiceSpy },
        { provide: DashboardService, useValue: dashboardServiceSpy },
        { provide: Router, useValue: routerSpy }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(BaseDashboardComponent);
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

  it('should handle dashboard data loading error', () => {
    const error = new Error('Failed to load dashboard data');
    mockDashboardService.getDashboardData.and.returnValue(throwError(() => error));
    
    component.ngOnInit();
    
    expect(component.errorMessage()).toBe('Error al cargar los datos del dashboard');
    expect(component.isLoading()).toBeFalse();
  });

  it('should get role badge class correctly', () => {
    expect(component.getRoleBadgeClass('admin')).toBe('bg-red-100 text-red-800');
    expect(component.getRoleBadgeClass('coordinator')).toBe('bg-purple-100 text-purple-800');
    expect(component.getRoleBadgeClass('teacher')).toBe('bg-blue-100 text-blue-800');
    expect(component.getRoleBadgeClass('student')).toBe('bg-green-100 text-green-800');
    expect(component.getRoleBadgeClass('unknown')).toBe('bg-gray-100 text-gray-800');
  });

  it('should navigate to search page', () => {
    component.goToSearch();
    expect(mockRouter.navigate).toHaveBeenCalledWith(['/search']);
  });

  it('should navigate to charts page', () => {
    component.goToCharts();
    expect(mockRouter.navigate).toHaveBeenCalledWith(['/charts']);
  });

  it('should navigate to D3 visualizations page', () => {
    component.goToD3Visualizations();
    expect(mockRouter.navigate).toHaveBeenCalledWith(['/d3-visualizations']);
  });

  it('should logout and navigate to login', () => {
    component.logout();
    expect(mockAuthService.logout).toHaveBeenCalled();
    expect(mockRouter.navigate).toHaveBeenCalledWith(['/login']);
  });

  it('should format date correctly', () => {
    const timestamp = '2025-10-06T19:25:00Z';
    const formatted = component.formatDate(timestamp);
    expect(formatted).toContain('2025');
    expect(formatted).toContain('10');
  });

  it('should return empty string for invalid date', () => {
    const formatted = component.formatDate('');
    expect(formatted).toBe('');
  });

  it('should return empty string for undefined date', () => {
    const formatted = component.formatDate(undefined);
    expect(formatted).toBe('');
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

  it('should display dashboard content when data is loaded', () => {
    component.dashboardData.set(mockDashboardData);
    component.isLoading.set(false);
    component.errorMessage.set('');
    fixture.detectChanges();
    
    const contentElement = fixture.nativeElement.querySelector('ng-content');
    expect(contentElement).toBeTruthy();
  });
});
