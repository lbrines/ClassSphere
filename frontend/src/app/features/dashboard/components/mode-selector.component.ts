import { CommonModule, NgFor, NgIf, TitleCasePipe } from '@angular/common';
import { Component, inject } from '@angular/core';
import { AsyncPipe } from '@angular/common';
import { map } from 'rxjs/operators';

import { ClassroomService } from '../../../core/services/classroom.service';
import { IntegrationMode } from '../../../core/models/classroom.model';

@Component({
  selector: 'app-mode-selector',
  standalone: true,
  imports: [CommonModule, NgIf, NgFor, AsyncPipe, TitleCasePipe],
  template: `
    <section class="mb-6 rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
      <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <p class="text-sm uppercase tracking-wide text-slate-400">Data Mode</p>
          <h3 class="text-xl font-semibold text-slate-100">{{ mode$ | async | titlecase }} dataset</h3>
          <p class="text-xs text-slate-500" *ngIf="state$ | async as state">Last sync {{ state.generatedAt | date: 'short' }}</p>
        </div>

        <div class="flex flex-wrap items-center gap-3">
          <button
            *ngFor="let mode of modes$ | async; trackBy: trackMode"
            type="button"
            (click)="selectMode(mode)"
            class="rounded-full border px-4 py-2 text-sm font-medium transition"
            [ngClass]="{
              'border-sky-500 bg-sky-500/10 text-sky-200 shadow shadow-sky-500/20': (mode$ | async) === mode,
              'border-slate-700 bg-slate-800 text-slate-300 hover:border-slate-600 hover:bg-slate-800/80': (mode$ | async) !== mode
            }"
          >
            {{ mode | titlecase }}
          </button>

          <button type="button" (click)="refresh()" class="rounded-full border border-slate-700 px-4 py-2 text-sm text-slate-300 transition hover:border-slate-500 hover:bg-slate-800/60">
            Refresh
          </button>
        </div>
      </div>
    </section>
  `,
})
export class ModeSelectorComponent {
  private readonly classroomService = inject(ClassroomService);

  readonly mode$ = this.classroomService.mode$;
  readonly state$ = this.classroomService.courseState$;
  readonly modes$ = this.classroomService.availableModes$.pipe(map((modes) => [...modes].sort()));

  selectMode(mode: IntegrationMode): void {
    this.classroomService.setMode(mode);
  }

  refresh(): void {
    this.classroomService.refresh();
  }

  trackMode(_: number, mode: IntegrationMode): IntegrationMode {
    return mode;
  }
}
