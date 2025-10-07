import { AsyncPipe, NgIf, TitleCasePipe } from '@angular/common';
import { Component, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-dashboard-layout',
  standalone: true,
  imports: [RouterOutlet, NgIf, AsyncPipe, TitleCasePipe],
  template: `
    <div class="min-h-screen bg-slate-950 text-slate-100">
      <header class="border-b border-slate-800 bg-slate-900/80 px-6 py-4">
        <div class="mx-auto flex max-w-5xl items-center justify-between">
          <div>
            <h1 class="text-xl font-semibold">ClassSphere</h1>
            <p class="text-sm text-slate-400">Intelligent classroom orchestration</p>
          </div>
          <div *ngIf="authService.currentUser$ | async as user" class="text-right">
            <p class="font-medium">{{ user.displayName }}</p>
            <p class="text-sm text-slate-400">{{ user.role | titlecase }}</p>
          </div>
        </div>
      </header>

      <main class="mx-auto max-w-5xl px-6 py-8">
        <router-outlet></router-outlet>
      </main>
    </div>
  `,
})
export class DashboardLayoutComponent {
  readonly authService = inject(AuthService);
}
