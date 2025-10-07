import { HttpHandlerFn, HttpRequest, HttpResponse } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';

import { authInterceptor } from './auth.interceptor';
import { AuthService } from '../services/auth.service';

describe('authInterceptor', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: AuthService,
          useValue: {
            getAccessToken: () => 'token-abc',
          },
        },
      ],
    });
  });

  it('should add authorization header when token available', (done) => {
    const request = new HttpRequest('GET', '/api');
    let interceptedRequest: HttpRequest<unknown> | null = null;
    const handler: HttpHandlerFn = (req) => {
      interceptedRequest = req;
      return of(new HttpResponse({ status: 200 }));
    };

    TestBed.runInInjectionContext(() => {
      authInterceptor(request, handler).subscribe(() => {
        expect(interceptedRequest?.headers.get('Authorization')).toBe('Bearer token-abc');
        done();
      });
    });
  });

  it('should pass through when no token', (done) => {
    const request = new HttpRequest('GET', '/api');
    let interceptedRequest: HttpRequest<unknown> | null = null;
    const handler: HttpHandlerFn = (req) => {
      interceptedRequest = req;
      return of(new HttpResponse({ status: 200 }));
    };

    TestBed.overrideProvider(AuthService, { useValue: { getAccessToken: () => null } });

    TestBed.runInInjectionContext(() => {
      authInterceptor(request, handler).subscribe(() => {
        expect(interceptedRequest?.headers.has('Authorization')).toBeFalse();
        done();
      });
    });
  });
});
