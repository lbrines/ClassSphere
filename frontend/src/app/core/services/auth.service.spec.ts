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
});
