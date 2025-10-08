import { Routes } from '@angular/router';

import { authGuard } from './core/guards/auth.guard';
import { roleGuard } from './core/guards/role.guard';
import { DashboardLayoutComponent } from './features/dashboard/dashboard-layout.component';
import { DashboardComponent } from './features/dashboard/dashboard.component';
import { AdminDashboardComponent } from './features/dashboard/pages/admin/admin-dashboard.component';
import { CoordinatorDashboardComponent } from './features/dashboard/pages/coordinator/coordinator-dashboard.component';
import { StudentDashboardComponent } from './features/dashboard/pages/student/student-dashboard.component';
import { TeacherDashboardComponent } from './features/dashboard/pages/teacher/teacher-dashboard.component';
import { LoginPageComponent } from './features/auth/pages/login/login.page';
import { NotFoundComponent } from './shared/components/not-found/not-found.component';

export const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    redirectTo: 'auth/login',
  },
  {
    path: 'auth',
    children: [
      {
        path: 'login',
        component: LoginPageComponent,
      },
      {
        path: '',
        pathMatch: 'full',
        redirectTo: 'login',
      },
    ],
  },
  {
    path: 'dashboard',
    component: DashboardLayoutComponent,
    canActivate: [authGuard],
    children: [
      {
        path: '',
        pathMatch: 'full',
        component: DashboardComponent,
      },
      {
        path: 'admin',
        component: AdminDashboardComponent,
        canActivate: [roleGuard],
        data: { roles: ['admin'] },
      },
      {
        path: 'coordinator',
        component: CoordinatorDashboardComponent,
        canActivate: [roleGuard],
        data: { roles: ['coordinator', 'admin'] },
      },
      {
        path: 'teacher',
        component: TeacherDashboardComponent,
        canActivate: [roleGuard],
        data: { roles: ['teacher', 'coordinator', 'admin'] },
      },
      {
        path: 'student',
        component: StudentDashboardComponent,
        canActivate: [roleGuard],
        data: { roles: ['student', 'teacher', 'coordinator', 'admin'] },
      },
    ],
  },
  {
    path: '**',
    component: NotFoundComponent,
  },
];
