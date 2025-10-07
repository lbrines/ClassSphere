import { TestBed } from '@angular/core/testing';
import { Router, UrlTree } from '@angular/router';
import { RouterTestingModule } from '@angular/router/testing';
import { BehaviorSubject, firstValueFrom, isObservable, Observable } from 'rxjs';

import { authGuard } from './auth.guard';
import { AuthService } from '../services/auth.service';

class AuthServiceStub {
  private readonly user$ = new BehaviorSubject<boolean>(false);
  readonly isAuthenticated$ = this.user$.asObservable();

  setAuthenticated(value: boolean) {
    this.user$.next(value);
  }
}

describe('authGuard', () => {
  let authService: AuthServiceStub;
  let router: Router;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [RouterTestingModule.withRoutes([])],
      providers: [{ provide: AuthService, useClass: AuthServiceStub }],
    });
    authService = TestBed.inject(AuthService) as unknown as AuthServiceStub;
    router = TestBed.inject(Router);
  });

  it('should allow navigation when authenticated', async () => {
    authService.setAuthenticated(true);
    const result = TestBed.runInInjectionContext(() => authGuard({} as any, {} as any));
    const outcome = await resolveGuardResult(result);
    expect(outcome).toBeTrue();
  });

  it('should redirect to login when not authenticated', async () => {
    authService.setAuthenticated(false);
    const result = TestBed.runInInjectionContext(() => authGuard({} as any, {} as any));
    const outcome = await resolveGuardResult(result);
    expect(outcome instanceof UrlTree).toBeTrue();
    expect((outcome as UrlTree).toString()).toContain('/auth/login');
  });
});

async function resolveGuardResult(result: ReturnType<typeof authGuard>): Promise<boolean | UrlTree> {
  if (isObservable(result)) {
    return (await firstValueFrom(result)) as boolean | UrlTree;
  }
  if (result instanceof Promise) {
    return (await result) as boolean | UrlTree;
  }
  return result as boolean | UrlTree;
}
