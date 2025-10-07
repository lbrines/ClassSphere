import { CommonModule, NgIf, TitleCasePipe } from '@angular/common';
import { Component, inject } from '@angular/core';
import { AsyncPipe } from '@angular/common';
import { finalize } from 'rxjs/operators';

import { ClassroomService } from '../../../core/services/classroom.service';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-google-connect',
  standalone: true,
  imports: [CommonModule, NgIf, AsyncPipe, TitleCasePipe],
  template: `
    <section class="mb-8 rounded-2xl border border-slate-800 bg-slate-900/50 p-5">
      <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <p class="text-sm uppercase tracking-wide text-slate-400">Google Classroom</p>
          <ng-container *ngIf="mode$ | async as mode">
            <h3 class="text-xl font-semibold text-slate-100">{{ mode === 'google' ? 'Connected' : 'Mock data active' }}</h3>
            <p class="text-sm text-slate-400">
              <ng-container *ngIf="mode === 'google'; else mockMessage">
                Live Google Classroom data is streaming into the dashboards.
              </ng-container>
              <ng-template #mockMessage>Working with curated mock dataset. Connect Google to sync real classrooms.</ng-template>
            </p>
          </ng-container>
        </div>

        <div class="flex flex-col items-start gap-3 md:flex-row md:items-center">
          <button type="button" (click)="connect()" [disabled]="connecting" class="rounded-full bg-sky-500 px-5 py-2 text-sm font-semibold text-slate-950 transition hover:bg-sky-400 disabled:cursor-not-allowed disabled:bg-slate-600">
            {{ connecting ? 'Redirecting…' : 'Connect Google Classroom' }}
          </button>
          <span *ngIf="message" class="text-sm" [ngClass]="{ 'text-emerald-300': success, 'text-rose-300': !success }">{{ message }}</span>
        </div>
      </div>
    </section>
  `,
})
export class GoogleConnectComponent {
  private readonly classroomService = inject(ClassroomService);
  private readonly authService = inject(AuthService);

  readonly mode$ = this.classroomService.mode$;

  connecting = false;
  message: string | null = null;
  success = false;

  connect(): void {
    if (this.connecting) {
      return;
    }
    this.connecting = true;
    this.success = false;
    this.message = null;

    this.authService
      .startOAuth()
      .pipe(finalize(() => (this.connecting = false)))
      .subscribe({
        next: (response) => {
          sessionStorage.setItem('classsphere.oauth.state', response.state);
          this.success = true;
          this.message = 'Redirecting to Google…';
          window.open(response.url, '_self');
        },
        error: () => {
          this.message = 'Failed to start Google authentication. Try again later.';
        },
      });
  }
}
