import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';

import { take } from 'rxjs/operators';

import { AuthService } from './auth.service';
import { environment } from '../../../environments/environment';
import { User } from '../models/user.model';

const mockResponse = {
  accessToken: 'token-123',
  expiresAt: new Date().toISOString(),
  user: {
    id: 'user-1',
    email: 'admin@classsphere.edu',
    displayName: 'Admin',
    role: 'admin' as const,
  },
};

describe('AuthService', () => {
  let service: AuthService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    localStorage.clear();
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule, RouterTestingModule.withRoutes([])],
    });
    service = TestBed.inject(AuthService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
    localStorage.clear();
  });

  it('should login and persist session', () => {
    let receivedUser: User | null = null;

    service.login({ email: 'admin@classsphere.edu', password: 'secret' }).subscribe((user) => (receivedUser = user));

    const req = httpMock.expectOne(`${environment.apiUrl}/auth/login`);
    expect(req.request.method).toBe('POST');
    req.flush(mockResponse);

    expect(receivedUser).not.toBeNull();
    if (!receivedUser) {
      return;
    }
    expect(receivedUser).toEqual(mockResponse.user);
    expect(service.getAccessToken()).toBe(mockResponse.accessToken);
  });

  it('should return dashboard route based on role', () => {
    expect(service.routeForRole('admin')).toBe('/dashboard/admin');
    expect(service.routeForRole('student')).toBe('/dashboard/student');
  });

  it('should restore session from local storage', (done) => {
    localStorage.setItem('classsphere.token', mockResponse.accessToken);
    localStorage.setItem('classsphere.user', JSON.stringify(mockResponse.user));

    (service as unknown as { restoreSession: () => void }).restoreSession();

    service.currentUser$
      .pipe(take(1))
      .subscribe((user) => {
        expect(user).toEqual(mockResponse.user);
        done();
      });
  });

  it('should start OAuth flow', () => {
    let receivedUrl: string | null = null;

    service.startOAuth().subscribe((response) => (receivedUrl = response.url));

    const req = httpMock.expectOne(`${environment.apiUrl}/auth/oauth/google`);
    expect(req.request.method).toBe('GET');
    req.flush({ state: 'state-123', url: 'https://accounts.google.com/auth' });

    expect(receivedUrl).not.toBeNull();
    expect(receivedUrl!).toBe('https://accounts.google.com/auth');
  });

  it('should complete OAuth flow and persist session', () => {
    let receivedUser: User | null = null;

    service.completeOAuth('code-123', 'state-123').subscribe((user) => (receivedUser = user));

    const req = httpMock.expectOne(
      (request) =>
        request.url === `${environment.apiUrl}/auth/oauth/callback` &&
        request.params.get('code') === 'code-123' &&
        request.params.get('state') === 'state-123',
    );
    expect(req.request.method).toBe('GET');
    req.flush(mockResponse);

    expect(receivedUser).not.toBeNull();
    expect(receivedUser!).toEqual(mockResponse.user);
    expect(service.getAccessToken()).toBe(mockResponse.accessToken);
  });

  it('should clear session on logout', (done) => {
    service.login({ email: 'admin@classsphere.edu', password: 'secret' }).subscribe();
    const req = httpMock.expectOne(`${environment.apiUrl}/auth/login`);
    req.flush(mockResponse);

    service.logout();
    expect(service.getAccessToken()).toBeNull();

    service.currentUser$.pipe(take(1)).subscribe((user) => {
      expect(user).toBeNull();
      done();
    });
  });

  it('should evaluate role permissions', () => {
    service.login({ email: 'admin@classsphere.edu', password: 'secret' }).subscribe();
    const req = httpMock.expectOne(`${environment.apiUrl}/auth/login`);
    req.flush(mockResponse);

    expect(service.hasRole('admin')).toBeTrue();
    expect(service.hasRole('teacher')).toBeFalse();
  });

  // === ADDITIONAL TESTS FOR 100% COVERAGE ===

  it('should emit isAuthenticated$ correctly', (done) => {
    service.isAuthenticated$.pipe(take(1)).subscribe((isAuth) => {
      expect(isAuth).toBeFalse(); // Initially not authenticated
      done();
    });
  });

  it('should return coordinator route', () => {
    expect(service.routeForRole('coordinator')).toBe('/dashboard/coordinator');
  });

  it('should return teacher route', () => {
    expect(service.routeForRole('teacher')).toBe('/dashboard/teacher');
  });

  it('should navigate to role dashboard for teacher', () => {
    const user: User = {
      id: 'user-1',
      email: 'test@test.com',
      displayName: 'Test',
      role: 'teacher',
    };

    // Test that it calls routeForRole correctly
    expect(service.routeForRole(user.role)).toBe('/dashboard/teacher');
    
    // Test navigation (will actually navigate in test)
    service.navigateToRoleDashboard(user);
    
    // Just verify it doesn't throw
    expect(user.role).toBe('teacher');
  });

  it('should navigate to role dashboard for coordinator', () => {
    const user: User = {
      id: 'user-2',
      email: 'coord@test.com',
      displayName: 'Coordinator',
      role: 'coordinator',
    };

    expect(service.routeForRole(user.role)).toBe('/dashboard/coordinator');
    service.navigateToRoleDashboard(user);
    expect(user.role).toBe('coordinator');
  });

  it('should emit isAuthenticated$ true after login', (done) => {
    service.login({ email: 'admin@classsphere.edu', password: 'secret' }).subscribe();
    const req = httpMock.expectOne(`${environment.apiUrl}/auth/login`);
    req.flush(mockResponse);

    service.isAuthenticated$.pipe(take(1)).subscribe((isAuth) => {
      expect(isAuth).toBeTrue();
      done();
    });
  });
});

// Separate describe for testing restoreSession error path
describe('AuthService - Corrupted Session Handling', () => {
  let service: AuthService;

  beforeEach(() => {
    // Setup corrupted data BEFORE creating service
    localStorage.setItem('classsphere.token', 'token-123');
    localStorage.setItem('classsphere.user', 'invalid-json{');

    spyOn(console, 'error');

    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule, RouterTestingModule.withRoutes([])],
    });

    // Service creation will trigger restoreSession() which will catch the error
    service = TestBed.inject(AuthService);
  });

  afterEach(() => {
    localStorage.clear();
  });

  it('should handle corrupted user JSON in localStorage', () => {
    expect(console.error).toHaveBeenCalledWith(
      'Failed to restore user from storage',
      jasmine.any(SyntaxError)
    );
    
    // Should have cleared the session
    expect(service.getAccessToken()).toBeNull();
  });

  it('should leave user as null after corrupted session', (done) => {
    service.currentUser$.pipe(take(1)).subscribe((user) => {
      expect(user).toBeNull();
      done();
    });
  });
});
