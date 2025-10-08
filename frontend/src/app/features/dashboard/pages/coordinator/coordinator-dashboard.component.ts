import { AsyncPipe, NgIf } from '@angular/common';
import { Component, inject } from '@angular/core';
import { combineLatest, map } from 'rxjs';

import { ClassroomService } from '../../../../core/services/classroom.service';
import { DashboardViewComponent } from '../../components/dashboard-view.component';

@Component({
  selector: 'app-coordinator-dashboard',
  standalone: true,
  imports: [DashboardViewComponent, AsyncPipe, NgIf],
  template: `
    <ng-container *ngIf="vm$ | async as vm; else loading">
      <app-dashboard-view
        [title]="'Program Coordination'"
        [data]="vm.dashboard"
        [courses]="vm.displayCourses"
        [generatedAt]="vm.courses.generatedAt"
        [mode]="vm.courses.mode"
      ></app-dashboard-view>
    </ng-container>

    <ng-template #loading>
      <div class="rounded-xl border border-slate-800 bg-slate-900/60 p-6 text-sm text-slate-400">Loading coordinator insights…</div>
    </ng-template>
  `,
})
export class CoordinatorDashboardComponent {
  private readonly classroomService = inject(ClassroomService);

  readonly vm$ = combineLatest([
    this.classroomService.dashboard('coordinator'),
    this.classroomService.courseState$,
  ]).pipe(
    map(([dashboard, courses]) => ({
      dashboard,
      courses,
      displayCourses: dashboard.courses?.length ? dashboard.courses : courses.courses,
    })),
  );
}
