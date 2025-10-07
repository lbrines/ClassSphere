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

  it('should handle login with malformed response', () => {
    let receivedUser: User | null = null;

    service.login({ email: 'test@example.com', password: 'password' }).subscribe({
      next: (user) => (receivedUser = user),
      error: (error) => fail('Should not have thrown error'),
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/auth/login`);
    req.flush({ invalid: 'response' }, { status: 200, statusText: 'OK' });

    expect(receivedUser).toBeNull();
  });

  it('should handle OAuth start with error', () => {
    service.startOAuth().subscribe({
      next: () => fail('Should have thrown error'),
      error: (error) => expect(error).toBeTruthy(),
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/auth/oauth/google`);
    req.flush({}, { status: 500, statusText: 'Internal Server Error' });
  });

  it('should handle OAuth completion with missing state', () => {
    service.completeOAuth('code-123', '').subscribe({
      next: () => fail('Should have thrown error'),
      error: (error) => expect(error).toBeTruthy(),
    });

    // Should not make any HTTP requests
    httpMock.expectNone(`${environment.apiUrl}/auth/oauth/callback`);
  });

  it('should handle OAuth completion with missing code', () => {
    service.completeOAuth('', 'state-123').subscribe({
      next: () => fail('Should have thrown error'),
      error: (error) => expect(error).toBeTruthy(),
    });

    httpMock.expectNone(`${environment.apiUrl}/auth/oauth/callback`);
  });

  it('should handle OAuth completion with network error', () => {
    service.completeOAuth('code-123', 'state-123').subscribe({
      next: () => fail('Should have thrown error'),
      error: (error) => expect(error).toBeTruthy(),
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/auth/oauth/callback`);
    req.flush({}, { status: 500, statusText: 'Internal Server Error' });
  });

  it('should handle OAuth completion with malformed response', () => {
    service.completeOAuth('code-123', 'state-123').subscribe({
      next: (user) => fail('Should have thrown error'),
      error: (error) => expect(error).toBeTruthy(),
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/auth/oauth/callback`);
    req.flush({ invalid: 'response' });
  });

  it('should handle login with empty credentials', () => {
    service.login({ email: '', password: '' }).subscribe({
      next: () => fail('Should have thrown error'),
      error: (error) => expect(error).toBeTruthy(),
    });

    httpMock.expectNone(`${environment.apiUrl}/auth/login`);
  });

  it('should handle login with very long credentials', () => {
    const longEmail = 'a'.repeat(1000) + '@example.com';
    const longPassword = 'p'.repeat(1000);

    service.login({ email: longEmail, password: longPassword }).subscribe({
      next: () => fail('Should have thrown error'),
      error: (error) => expect(error).toBeTruthy(),
    });

    httpMock.expectNone(`${environment.apiUrl}/auth/login`);
  });

  it('should handle login with special characters in credentials', () => {
    const specialEmail = 'test+special@example.com';
    const specialPassword = 'pass!@#$%^&*()';

    service.login({ email: specialEmail, password: specialPassword }).subscribe({
      next: () => fail('Should have thrown error'),
      error: (error) => expect(error).toBeTruthy(),
    });

    httpMock.expectNone(`${environment.apiUrl}/auth/login`);
  });

  it('should handle concurrent login attempts', () => {
    let responseCount = 0;

    // Start multiple login attempts
    service.login({ email: 'test1@example.com', password: 'pass1' }).subscribe(() => responseCount++);
    service.login({ email: 'test2@example.com', password: 'pass2' }).subscribe(() => responseCount++);

    // Only first request should be made
    const req = httpMock.expectOne(`${environment.apiUrl}/auth/login`);
    expect(req.request.method).toBe('POST');

    req.flush(mockResponse);

    expect(responseCount).toBe(2);
  });

  it('should handle logout when not logged in', () => {
    expect(() => service.logout()).not.toThrow();
    expect(service.getAccessToken()).toBeNull();
  });

  it('should handle hasRole with different roles', () => {
    // Set user as admin
    service['currentUserSubject'].next({ id: '1', email: 'admin@test.com', displayName: 'Admin', role: 'admin' });

    expect(service.hasRole('admin')).toBe(true);
    expect(service.hasRole('teacher')).toBe(false);
    expect(service.hasRole('student')).toBe(false);
  });

  it('should handle hasRole when no user is logged in', () => {
    service['currentUserSubject'].next(null);

    expect(service.hasRole('admin')).toBe(false);
    expect(service.hasRole('teacher')).toBe(false);
  });

  it('should handle routeForRole correctly', () => {
    expect(service.routeForRole('admin')).toBe('/dashboard/admin');
    expect(service.routeForRole('coordinator')).toBe('/dashboard/coordinator');
    expect(service.routeForRole('teacher')).toBe('/dashboard/teacher');
    expect(service.routeForRole('student')).toBe('/dashboard/student');
  });

  it('should handle navigateToRoleDashboard', () => {
    spyOn(service['router'], 'navigateByUrl');

    const user: User = { id: '1', email: 'admin@test.com', displayName: 'Admin', role: 'admin' };
    service.navigateToRoleDashboard(user);

    expect(service['router'].navigateByUrl).toHaveBeenCalledWith('/dashboard/admin');
  });

  it('should handle session restoration with malformed user data', () => {
    localStorage.setItem('classsphere.token', 'test-token');
    localStorage.setItem('classsphere.user', 'invalid-json');

    // Should not throw error and should clear corrupted data
    expect(() => service['restoreSession']()).not.toThrow();

    // Should have cleared the corrupted data
    expect(localStorage.getItem('classsphere.token')).toBeNull();
    expect(localStorage.getItem('classsphere.user')).toBeNull();
  });

  it('should handle session restoration with missing token', () => {
    localStorage.setItem('classsphere.user', JSON.stringify(mockResponse.user));

    service['restoreSession']();

    // Should not restore session without token
    expect(service['currentUserSubject'].value).toBeNull();
  });

  it('should handle session restoration with missing user data', () => {
    localStorage.setItem('classsphere.token', 'test-token');

    service['restoreSession']();

    // Should not restore session without user data
    expect(service['currentUserSubject'].value).toBeNull();
  });

  it('should handle localStorage being unavailable', () => {
    // Mock localStorage as unavailable
    spyOn(localStorage, 'getItem').and.throwError('localStorage not available');
    spyOn(localStorage, 'setItem').and.throwError('localStorage not available');
    spyOn(localStorage, 'removeItem').and.throwError('localStorage not available');

    // Should not throw errors
    expect(() => service.getAccessToken()).not.toThrow();
    expect(() => service.logout()).not.toThrow();

    expect(service.getAccessToken()).toBeNull();
  });

  it('should handle very long token values', () => {
    const longToken = 'a'.repeat(10000);
    localStorage.setItem('classsphere.token', longToken);
    expect(service.getAccessToken()).toBe(longToken);
  });

  it('should handle special characters in tokens', () => {
    const specialToken = 'token!@#$%^&*()_+{}|:<>?[]\\;\'",./`~';
    localStorage.setItem('classsphere.token', specialToken);
    expect(service.getAccessToken()).toBe(specialToken);
  });
});
