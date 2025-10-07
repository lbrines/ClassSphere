import { TestBed } from '@angular/core/testing';
import { ActivatedRouteSnapshot, UrlTree } from '@angular/router';
import { RouterTestingModule } from '@angular/router/testing';
import { BehaviorSubject, firstValueFrom, isObservable, Observable } from 'rxjs';

import { roleGuard } from './role.guard';
import { AuthService } from '../services/auth.service';
import { User } from '../models/user.model';

class AuthRoleStub {
  private readonly userSubject = new BehaviorSubject<User | null>(null);
  readonly currentUser$ = this.userSubject.asObservable();

  setUser(user: User | null) {
    this.userSubject.next(user);
  }
}

describe('roleGuard', () => {
  let authService: AuthRoleStub;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [RouterTestingModule.withRoutes([])],
      providers: [{ provide: AuthService, useClass: AuthRoleStub }],
    });
    authService = TestBed.inject(AuthService) as unknown as AuthRoleStub;
  });

  it('should allow users with required role', async () => {
    authService.setUser({
      id: '1',
      email: 'teacher@classsphere.edu',
      displayName: 'Teacher',
      role: 'teacher',
    });

    const route = new ActivatedRouteSnapshot();
    route.data = { roles: ['teacher'] };
    const result = TestBed.runInInjectionContext(() => roleGuard(route, {} as any));
    const outcome = await resolveGuardResult(result);
    expect(outcome).toBeTrue();
  });

  it('should redirect when role missing', async () => {
    authService.setUser({
      id: '1',
      email: 'student@classsphere.edu',
      displayName: 'Student',
      role: 'student',
    });

    const route = new ActivatedRouteSnapshot();
    route.data = { roles: ['admin'] };
    const result = TestBed.runInInjectionContext(() => roleGuard(route, {} as any));
    const outcome = await resolveGuardResult(result);
    expect(outcome instanceof UrlTree).toBeTrue();
  });
});

async function resolveGuardResult(
  result: ReturnType<typeof roleGuard>,
): Promise<boolean | UrlTree> {
  if (isObservable(result)) {
    return (await firstValueFrom(result)) as boolean | UrlTree;
  }
  if (result instanceof Promise) {
    return (await result) as boolean | UrlTree;
  }
  return result as boolean | UrlTree;
}
