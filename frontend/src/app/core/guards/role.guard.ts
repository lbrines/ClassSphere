import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { map, take } from 'rxjs/operators';

import { AuthService } from '../services/auth.service';
import { UserRole } from '../models/user.model';

export const roleGuard: CanActivateFn = (route) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  const allowedRoles = (route.data?.['roles'] ?? []) as UserRole[];

  return authService.currentUser$.pipe(
    take(1),
    map((user) => {
      if (user && (allowedRoles.length === 0 || allowedRoles.includes(user.role))) {
        return true;
      }
      return router.createUrlTree(['/auth/login']);
    })
  );
};
