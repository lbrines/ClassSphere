import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { Router } from '@angular/router';
import { of } from 'rxjs';

import { DashboardLayoutComponent } from './dashboard-layout.component';
import { AuthService } from '../../core/services/auth.service';
import { ClassroomService } from '../../core/services/classroom.service';
import { IntegrationMode } from '../../core/models/classroom.model';
import { User, UserRole } from '../../core/models/user.model';

class ClassroomServiceStub {
  readonly mode$ = of<IntegrationMode>('mock');
  readonly courseState$ = of({
    mode: 'mock' as IntegrationMode,
    generatedAt: '2025-10-07T10:00:00Z',
    availableModes: ['mock'] as IntegrationMode[],
    courses: [],
  });
  readonly availableModes$ = of(['mock'] as IntegrationMode[]);
  setMode = jasmine.createSpy('setMode');
  refresh = jasmine.createSpy('refresh');
}

describe('DashboardLayoutComponent', () => {
  let component: DashboardLayoutComponent;
  let fixture: ComponentFixture<DashboardLayoutComponent>;
  let authServiceSpy: jasmine.SpyObj<AuthService>;
  let router: Router;

  const mockUser: User = {
    id: 'user-1',
    email: 'test@example.com',
    displayName: 'Test User',
    role: 'admin' as UserRole,
  };

  beforeEach(async () => {
    const spy = jasmine.createSpyObj('AuthService', ['logout'], {
      currentUser$: of(mockUser),
    });

    await TestBed.configureTestingModule({
      imports: [DashboardLayoutComponent, RouterTestingModule],
      providers: [
        { provide: AuthService, useValue: spy },
        { provide: ClassroomService, useClass: ClassroomServiceStub },
      ],
    }).compileComponents();

    authServiceSpy = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
    router = TestBed.inject(Router);
    spyOn(router, 'navigate');
    
    fixture = TestBed.createComponent(DashboardLayoutComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render ClassSphere title', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('h1')?.textContent).toContain('ClassSphere');
  });

  it('should display user information', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.textContent).toContain('Test User');
    expect(compiled.textContent).toContain('Admin');
  });

  it('should have router outlet', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('router-outlet')).toBeTruthy();
  });

  describe('User Dropdown Menu', () => {
    it('should have dropdown closed by default', () => {
      expect(component.dropdownOpen()).toBe(false);
    });

    it('should not show dropdown menu when closed', () => {
      const compiled = fixture.nativeElement as HTMLElement;
      const dropdownMenu = compiled.querySelector('[role="menu"]');
      expect(dropdownMenu).toBeFalsy();
    });

    it('should toggle dropdown when user button is clicked', () => {
      const compiled = fixture.nativeElement as HTMLElement;
      const userButton = compiled.querySelector('button[aria-label="User menu"]') as HTMLButtonElement;
      
      expect(component.dropdownOpen()).toBe(false);
      
      userButton.click();
      fixture.detectChanges();
      
      expect(component.dropdownOpen()).toBe(true);
      
      userButton.click();
      fixture.detectChanges();
      
      expect(component.dropdownOpen()).toBe(false);
    });

    it('should show dropdown menu when open', () => {
      component.toggleDropdown();
      fixture.detectChanges();
      
      const compiled = fixture.nativeElement as HTMLElement;
      const dropdownMenu = compiled.querySelector('[role="menu"]');
      
      expect(dropdownMenu).toBeTruthy();
    });

    it('should display Profile option in dropdown (disabled)', () => {
      component.toggleDropdown();
      fixture.detectChanges();
      
      const compiled = fixture.nativeElement as HTMLElement;
      const profileButton = compiled.querySelector('[role="menuitem"]') as HTMLButtonElement;
      
      expect(profileButton?.textContent).toContain('Profile');
      expect(profileButton?.textContent).toContain('Coming soon');
      expect(profileButton?.disabled).toBe(true);
    });

    it('should display Settings option in dropdown (disabled)', () => {
      component.toggleDropdown();
      fixture.detectChanges();
      
      const compiled = fixture.nativeElement as HTMLElement;
      const menuItems = compiled.querySelectorAll('[role="menuitem"]');
      const settingsButton = menuItems[1] as HTMLButtonElement;
      
      expect(settingsButton?.textContent).toContain('Settings');
      expect(settingsButton?.textContent).toContain('Coming soon');
      expect(settingsButton?.disabled).toBe(true);
    });

    it('should display Logout option in dropdown', () => {
      component.toggleDropdown();
      fixture.detectChanges();
      
      const compiled = fixture.nativeElement as HTMLElement;
      const menuItems = compiled.querySelectorAll('[role="menuitem"]');
      const logoutButton = menuItems[2] as HTMLButtonElement;
      
      expect(logoutButton?.textContent).toContain('Logout');
      expect(logoutButton?.disabled).toBe(false);
    });

    it('should have correct aria-expanded attribute when closed', () => {
      const compiled = fixture.nativeElement as HTMLElement;
      const userButton = compiled.querySelector('button[aria-label="User menu"]') as HTMLButtonElement;
      
      expect(userButton.getAttribute('aria-expanded')).toBe('false');
    });

    it('should have correct aria-expanded attribute when open', () => {
      component.toggleDropdown();
      fixture.detectChanges();
      
      const compiled = fixture.nativeElement as HTMLElement;
      const userButton = compiled.querySelector('button[aria-label="User menu"]') as HTMLButtonElement;
      
      expect(userButton.getAttribute('aria-expanded')).toBe('true');
    });

    it('should call authService.logout when logout button is clicked', () => {
      component.toggleDropdown();
      fixture.detectChanges();
      
      const compiled = fixture.nativeElement as HTMLElement;
      const menuItems = compiled.querySelectorAll('[role="menuitem"]');
      const logoutButton = menuItems[2] as HTMLButtonElement;
      
      logoutButton.click();
      fixture.detectChanges();
      
      expect(authServiceSpy.logout).toHaveBeenCalled();
    });

    it('should navigate to login page when logout is clicked', () => {
      component.toggleDropdown();
      fixture.detectChanges();
      
      const compiled = fixture.nativeElement as HTMLElement;
      const menuItems = compiled.querySelectorAll('[role="menuitem"]');
      const logoutButton = menuItems[2] as HTMLButtonElement;
      
      logoutButton.click();
      fixture.detectChanges();
      
      expect(router.navigate).toHaveBeenCalledWith(['/auth/login']);
    });

    it('should close dropdown after logout', () => {
      component.toggleDropdown();
      fixture.detectChanges();
      
      expect(component.dropdownOpen()).toBe(true);
      
      component.handleLogout();
      fixture.detectChanges();
      
      expect(component.dropdownOpen()).toBe(false);
    });

    it('should rotate chevron icon when dropdown is open', () => {
      const compiled = fixture.nativeElement as HTMLElement;
      const chevronIcon = compiled.querySelector('button[aria-label="User menu"] svg') as SVGElement;
      
      expect(chevronIcon.classList.contains('rotate-180')).toBe(false);
      
      component.toggleDropdown();
      fixture.detectChanges();
      
      expect(chevronIcon.classList.contains('rotate-180')).toBe(true);
    });
  });
});
