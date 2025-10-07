import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of, throwError } from 'rxjs';

import { LoginPageComponent } from './login.page';
import { AuthService } from '../../../../core/services/auth.service';
import { NavigationService } from '../../../../core/services/navigation.service';
import { User, UserRole } from '../../../../core/models/user.model';

describe('LoginPageComponent', () => {
  let component: LoginPageComponent;
  let fixture: ComponentFixture<LoginPageComponent>;
  let authServiceSpy: jasmine.SpyObj<AuthService>;
  let navigationServiceSpy: jasmine.SpyObj<NavigationService>;

  const mockUser: User = {
    id: 'user-1',
    email: 'test@example.com',
    displayName: 'Test User',
    role: 'student' as UserRole,
  };

  beforeEach(async () => {
    const authSpy = jasmine.createSpyObj('AuthService', [
      'login',
      'startOAuth',
      'navigateToRoleDashboard',
    ]);
    const navSpy = jasmine.createSpyObj('NavigationService', ['redirectToExternal']);

    await TestBed.configureTestingModule({
      imports: [LoginPageComponent],
      providers: [
        { provide: AuthService, useValue: authSpy },
        { provide: NavigationService, useValue: navSpy },
      ],
    }).compileComponents();

    authServiceSpy = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
    navigationServiceSpy = TestBed.inject(NavigationService) as jasmine.SpyObj<NavigationService>;
    fixture = TestBed.createComponent(LoginPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call login on handleCredentials success', () => {
    authServiceSpy.login.and.returnValue(of(mockUser));
    authServiceSpy.navigateToRoleDashboard.and.stub();

    component.handleCredentials({ email: 'test@test.com', password: 'password' });

    expect(authServiceSpy.login).toHaveBeenCalledWith({
      email: 'test@test.com',
      password: 'password',
    });
  });

  it('should set error on login failure', (done) => {
    authServiceSpy.login.and.returnValue(throwError(() => new Error('Login failed')));

    component.handleCredentials({ email: 'test@test.com', password: 'wrong' });

    setTimeout(() => {
      expect(component.error()).toBe('Unable to sign in. Please check your credentials.');
      expect(component.pending()).toBe(false);
      done();
    }, 100);
  });

  it('should set error on OAuth failure', (done) => {
    authServiceSpy.startOAuth.and.returnValue(throwError(() => new Error('OAuth failed')));

    component.handleOAuthRedirect();

    setTimeout(() => {
      expect(component.error()).toBe('Unable to initiate Google sign-in.');
      expect(component.pending()).toBe(false);
      done();
    }, 100);
  });

  it('should redirect to Google OAuth URL on success', (done) => {
    authServiceSpy.startOAuth.and.returnValue(
      of({ state: 'state123', url: 'https://accounts.google.com/o/oauth2/v2/auth' })
    );

    component.handleOAuthRedirect();

    setTimeout(() => {
      expect(authServiceSpy.startOAuth).toHaveBeenCalled();
      expect(navigationServiceSpy.redirectToExternal).toHaveBeenCalledWith(
        'https://accounts.google.com/o/oauth2/v2/auth'
      );
      expect(component.pending()).toBe(false);
      done();
    }, 100);
  });
});

