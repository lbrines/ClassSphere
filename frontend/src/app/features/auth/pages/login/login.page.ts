import { CommonModule } from '@angular/common';
import { Component, DestroyRef, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { finalize } from 'rxjs/operators';

import { LoginFormComponent } from '../../../../shared/components/login-form/login-form.component';
import { OAuthButtonComponent } from '../../../../shared/components/oauth-button/oauth-button.component';
import { AuthService } from '../../../../core/services/auth.service';
import { Credentials } from '../../../../core/models/auth.model';

@Component({
  selector: 'app-login-page',
  standalone: true,
  imports: [CommonModule, LoginFormComponent, OAuthButtonComponent],
  template: `
    <section class="flex min-h-screen items-center justify-center bg-slate-950 px-4 py-12">
      <div class="w-full max-w-md space-y-6 rounded-xl border border-slate-800 bg-slate-900/80 p-8 shadow-xl">
        <header class="space-y-2 text-center">
          <h1 class="text-2xl font-semibold">Welcome to ClassSphere</h1>
          <p class="text-sm text-slate-400">Sign in to access your dashboard.</p>
        </header>

        <app-login-form [pending]="pending()" (submitted)="handleCredentials($event)"></app-login-form>

        <div class="relative py-4 text-center text-sm text-slate-400">
          <span class="bg-slate-900 px-2">or</span>
          <div class="absolute inset-x-0 top-1/2 -z-10 h-px bg-slate-700"></div>
        </div>

        <app-oauth-button [disabled]="pending()" (clicked)="handleOAuthRedirect()"></app-oauth-button>

        <p *ngIf="error()" class="rounded-md bg-red-500/10 p-3 text-sm text-red-300">{{ error() }}</p>
      </div>
    </section>
  `,
})
export class LoginPageComponent {
  private readonly authService = inject(AuthService);
  private readonly destroyRef = inject(DestroyRef);

  readonly pending = signal(false);
  readonly error = signal<string | null>(null);

  handleCredentials(credentials: Credentials): void {
    this.pending.set(true);
    this.error.set(null);

    this.authService
      .login(credentials)
      .pipe(
        takeUntilDestroyed(this.destroyRef),
        finalize(() => this.pending.set(false))
      )
      .subscribe({
        next: (user) => this.authService.navigateToRoleDashboard(user),
        error: () => this.error.set('Unable to sign in. Please check your credentials.'),
      });
  }

  handleOAuthRedirect(): void {
    this.pending.set(true);
    this.error.set(null);

    this.authService
      .startOAuth()
      .pipe(takeUntilDestroyed(this.destroyRef), finalize(() => this.pending.set(false)))
      .subscribe({
        next: (response) => {
          window.location.href = response.url;
        },
        error: () => this.error.set('Unable to initiate Google sign-in.'),
      });
  }
}
