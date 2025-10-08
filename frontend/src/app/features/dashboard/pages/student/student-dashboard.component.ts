import { AsyncPipe, NgIf } from '@angular/common';
import { Component, inject } from '@angular/core';
import { combineLatest, map } from 'rxjs';

import { ClassroomService } from '../../../../core/services/classroom.service';
import { DashboardViewComponent } from '../../components/dashboard-view.component';

@Component({
  selector: 'app-student-dashboard',
  standalone: true,
  imports: [DashboardViewComponent, AsyncPipe, NgIf],
  template: `
    <ng-container *ngIf="vm$ | async as vm; else loading">
      <app-dashboard-view
        [title]="'Learning Progress'"
        [data]="vm.dashboard"
        [courses]="vm.dashboard.courses ?? []"
        [generatedAt]="vm.courses.generatedAt"
        [mode]="vm.courses.mode"
      ></app-dashboard-view>
    </ng-container>

    <ng-template #loading>
      <div class="rounded-xl border border-slate-800 bg-slate-900/60 p-6 text-sm text-slate-400">Loading student progress…</div>
    </ng-template>
  `,
})
export class StudentDashboardComponent {
  private readonly classroomService = inject(ClassroomService);

  readonly vm$ = combineLatest([
    this.classroomService.dashboard('student'),
    this.classroomService.courseState$,
  ]).pipe(map(([dashboard, courses]) => ({ dashboard, courses })));
}
