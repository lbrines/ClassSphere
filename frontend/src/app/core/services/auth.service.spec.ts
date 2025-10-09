import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { RouterTestingModule } from '@angular/router/testing';

import { AuthService } from './auth.service';
import { User } from '../models/user.model';
import { EnvironmentService } from './environment.service';

const loginPayload = {
  email: 'admin@classsphere.edu',
  password: 'secret',
};

const serverResponse = {
  accessToken: 'token-123',
  expiresAt: '2025-10-07T10:00:00Z',
  user: {
    id: 'user-1',
    email: 'admin@classsphere.edu',
    displayName: 'Administrator',
    role: 'admin' as const,
  },
};

describe('AuthService', () => {
  let service: AuthService;
  let http: HttpTestingController;
  const runtimeApiUrl = 'http://runtime-config.local/api/v1';

  beforeEach(() => {
    localStorage.clear();

    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule, RouterTestingModule],
      providers: [
        { provide: EnvironmentService, useValue: { apiUrl: runtimeApiUrl } },
      ],
    });

    service = TestBed.inject(AuthService);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    http.verify();
    localStorage.clear();
  });

  it('logs in and stores the session', () => {
    let receivedUser: User | null = null;

    service.login(loginPayload).subscribe((user) => (receivedUser = user));

    const req = http.expectOne(`${runtimeApiUrl}/auth/login`);
    expect(req.request.method).toBe('POST');
    req.flush(serverResponse);

    expect(receivedUser).not.toBeNull();
    if (receivedUser) {
      expect(receivedUser).toEqual(serverResponse.user);
    }
    expect(service.getAccessToken()).toBe(serverResponse.accessToken);
  });

  it('starts the OAuth flow and returns provider URL', () => {
    let startUrl: string | null = null;

    service.startOAuth().subscribe((response) => (startUrl = response.url));

    const req = http.expectOne(`${runtimeApiUrl}/auth/oauth/google`);
    req.flush({ state: 'state-123', url: 'https://accounts.google.com' });

    expect(startUrl).not.toBeNull();
    if (startUrl) {
      expect(startUrl).toBe('https://accounts.google.com');
    }
  });

  it('completes the OAuth flow and persists credentials', () => {
    service.completeOAuth('code-456', 'state-123').subscribe();

    const req = http.expectOne((request) => request.url === `${runtimeApiUrl}/auth/oauth/callback`);
    expect(req.request.params.get('code')).toBe('code-456');
    expect(req.request.params.get('state')).toBe('state-123');
    req.flush(serverResponse);

    expect(service.getAccessToken()).toBe(serverResponse.accessToken);
  });

  it('restores session data from localStorage', (done) => {
    localStorage.setItem('classsphere.token', serverResponse.accessToken);
    localStorage.setItem('classsphere.user', JSON.stringify(serverResponse.user));

    // force rehydration
    (service as unknown as { restoreSession: () => void }).restoreSession();

    service.currentUser$.subscribe((user) => {
      expect(user).toEqual(serverResponse.user);
      done();
    });
  });

  it('clears stored data on logout', () => {
    service.login(loginPayload).subscribe();
    http.expectOne(`${runtimeApiUrl}/auth/login`).flush(serverResponse);

    service.logout();

    expect(service.getAccessToken()).toBeNull();
  });

  it('maps roles to dashboard routes', () => {
    expect(service.routeForRole('admin')).toBe('/dashboard/admin');
    expect(service.routeForRole('coordinator')).toBe('/dashboard/coordinator');
    expect(service.routeForRole('teacher')).toBe('/dashboard/teacher');
    expect(service.routeForRole('student')).toBe('/dashboard/student');
  });

  it('navigates to the dashboard associated with the user role', () => {
    const router = TestBed.inject(Router);
    const navigateSpy = spyOn(router, 'navigateByUrl');

    service.navigateToRoleDashboard(serverResponse.user);

    expect(navigateSpy).toHaveBeenCalledWith('/dashboard/admin');
  });
});
