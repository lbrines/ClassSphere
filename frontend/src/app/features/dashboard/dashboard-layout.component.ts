import { AsyncPipe, NgIf, TitleCasePipe } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';

import { AuthService } from '../../core/services/auth.service';
import { ModeSelectorComponent } from './components/mode-selector.component';
import { GoogleConnectComponent } from './components/google-connect.component';

@Component({
  selector: 'app-dashboard-layout',
  standalone: true,
  imports: [RouterOutlet, NgIf, AsyncPipe, TitleCasePipe, ModeSelectorComponent, GoogleConnectComponent],
  template: `
    <div class="min-h-screen bg-slate-950 text-slate-100">
      <header class="border-b border-slate-800 bg-slate-900/80 px-6 py-4">
        <div class="mx-auto flex max-w-5xl items-center justify-between">
          <div>
            <h1 class="text-xl font-semibold">ClassSphere</h1>
            <p class="text-sm text-slate-400">Intelligent classroom orchestration</p>
          </div>
          <div *ngIf="authService.currentUser$ | async as user" class="relative">
            <button
              (click)="toggleDropdown()"
              class="flex items-center gap-3 rounded-md px-3 py-2 text-right transition-colors hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-600"
              aria-label="User menu"
              [attr.aria-expanded]="dropdownOpen()"
            >
              <div>
                <p class="font-medium">{{ user.displayName }}</p>
                <p class="text-sm text-slate-400">{{ user.role | titlecase }}</p>
              </div>
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke-width="1.5" 
                stroke="currentColor" 
                class="h-4 w-4 text-slate-400 transition-transform"
                [class.rotate-180]="dropdownOpen()"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
              </svg>
            </button>

            <!-- Dropdown Menu -->
            <div 
              *ngIf="dropdownOpen()"
              class="absolute right-0 mt-2 w-56 rounded-md border border-slate-700 bg-slate-800 py-1 shadow-lg"
              role="menu"
            >
              <button
                class="flex w-full items-center gap-3 px-4 py-2 text-left text-sm text-slate-300 transition-colors hover:bg-slate-700"
                role="menuitem"
                disabled
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-4 w-4">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                </svg>
                <span class="opacity-50">Profile (Coming soon)</span>
              </button>
              
              <button
                class="flex w-full items-center gap-3 px-4 py-2 text-left text-sm text-slate-300 transition-colors hover:bg-slate-700"
                role="menuitem"
                disabled
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-4 w-4">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span class="opacity-50">Settings (Coming soon)</span>
              </button>

              <div class="my-1 h-px bg-slate-700"></div>

              <button
                (click)="handleLogout()"
                class="flex w-full items-center gap-3 px-4 py-2 text-left text-sm text-red-400 transition-colors hover:bg-slate-700"
                role="menuitem"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-4 w-4">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
                </svg>
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      <main class="mx-auto max-w-5xl px-6 py-8">
        <app-mode-selector></app-mode-selector>
        <app-google-connect></app-google-connect>
        <router-outlet></router-outlet>
      </main>
    </div>
  `,
})
export class DashboardLayoutComponent {
  readonly authService = inject(AuthService);
  private readonly router = inject(Router);
  readonly dropdownOpen = signal(false);

  toggleDropdown(): void {
    this.dropdownOpen.update(open => !open);
  }

  handleLogout(): void {
    this.dropdownOpen.set(false);
    this.authService.logout();
    this.router.navigate(['/auth/login']);
  }
}
