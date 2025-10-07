import { CommonModule, DatePipe, DecimalPipe, NgClass, NgFor, NgIf, TitleCasePipe } from '@angular/common';
import { Component, Input } from '@angular/core';

import { DashboardData, CourseOverview, IntegrationMode } from '../../../core/models/classroom.model';
import { ApexChartComponent } from '../../../shared/components/apex-chart/apex-chart.component';

@Component({
  selector: 'app-dashboard-view',
  standalone: true,
  imports: [CommonModule, NgIf, NgFor, TitleCasePipe, DatePipe, DecimalPipe, NgClass, ApexChartComponent],
  template: `
    <ng-container *ngIf="data; else loading">
      <header class="mb-6 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 class="text-2xl font-semibold text-slate-100">{{ title }}</h2>
          <p *ngIf="generatedAt" class="text-sm text-slate-400">Last updated {{ generatedAt | date: 'short' }}</p>
        </div>
        <div class="flex items-center gap-3">
          <span *ngIf="mode" class="rounded-full bg-slate-800 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-sky-300">{{ mode | titlecase }} Mode</span>
          <span class="text-xs text-slate-500">{{ data.generatedAt | date: 'short' }}</span>
        </div>
      </header>

      <section *ngIf="data.summary?.length" class="mb-8">
        <div class="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <article *ngFor="let metric of data.summary" class="rounded-xl border border-slate-800 bg-slate-900/60 p-4 shadow-sm shadow-slate-900/20">
            <p class="text-sm text-slate-400">{{ metric.label }}</p>
            <p class="mt-2 text-2xl font-semibold text-slate-100">{{ formatValue(metric.value, metric.format) }}</p>
            <p class="mt-3 flex items-center gap-2 text-xs" [ngClass]="trendClass(metric.trend)">
              <span>{{ trendIcon(metric.trend) }}</span>
              <span>{{ formatDelta(metric.delta, metric.format) }}</span>
            </p>
          </article>
        </div>
      </section>

      <section *ngIf="data.charts?.length" class="mb-8 grid gap-6 xl:grid-cols-2">
        <div *ngFor="let chart of data.charts" class="rounded-xl border border-slate-800 bg-slate-900/60 p-4">
          <header class="mb-4 flex items-center justify-between">
            <h3 class="text-lg font-semibold text-slate-100">{{ chart.title }}</h3>
            <span class="text-xs text-slate-500 uppercase tracking-wide">{{ chart.type }}</span>
          </header>
          <app-apex-chart [chart]="chart"></app-apex-chart>
        </div>
      </section>

      <section *ngIf="data.highlights?.length" class="mb-8">
        <h3 class="mb-4 text-lg font-semibold text-slate-100">Highlights</h3>
        <div class="grid gap-4 md:grid-cols-2">
          <article *ngFor="let highlight of data.highlights" class="rounded-xl border border-slate-800 bg-slate-900/60 p-4">
            <span class="mb-2 inline-flex items-center rounded-full px-2 py-1 text-xs font-semibold" [ngClass]="highlightClass(highlight.status)">
              {{ highlight.status | titlecase }}
            </span>
            <h4 class="text-base font-semibold text-slate-100">{{ highlight.title }}</h4>
            <p class="mt-2 text-sm text-slate-400">{{ highlight.details }}</p>
          </article>
        </div>
      </section>

      <section *ngIf="data.alerts?.length" class="mb-8">
        <h3 class="mb-4 text-lg font-semibold text-slate-100">Alerts</h3>
        <ul class="space-y-2">
          <li *ngFor="let alert of data.alerts" class="flex items-start gap-3 rounded-lg border border-amber-500/40 bg-amber-500/10 px-3 py-2 text-sm text-amber-200">
            <span class="mt-0.5 text-lg">⚠️</span>
            <span>{{ alert }}</span>
          </li>
        </ul>
      </section>

      <section *ngIf="courses?.length" class="mb-8">
        <h3 class="mb-4 text-lg font-semibold text-slate-100">Course Overview</h3>
        <div class="overflow-x-auto rounded-xl border border-slate-800">
          <table class="min-w-full divide-y divide-slate-800 text-sm">
            <thead class="bg-slate-900/70 text-left text-xs uppercase tracking-wide text-slate-400">
              <tr>
                <th class="px-4 py-3">Course</th>
                <th class="px-4 py-3">Program</th>
                <th class="px-4 py-3">Teacher</th>
                <th class="px-4 py-3 text-right">Enrollment</th>
                <th class="px-4 py-3 text-right">Completion</th>
                <th class="px-4 py-3 text-right">Upcoming</th>
                <th class="px-4 py-3">Last Activity</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-800/60 text-slate-200">
              <tr *ngFor="let course of courses">
                <td class="px-4 py-3">
                  <div class="font-medium text-slate-100">{{ course.name }}</div>
                  <div class="text-xs text-slate-500">{{ course.section }}</div>
                </td>
                <td class="px-4 py-3 text-slate-400">{{ course.program }}</td>
                <td class="px-4 py-3 text-slate-400">{{ course.primaryTeacher }}</td>
                <td class="px-4 py-3 text-right">{{ course.enrollment }}</td>
                <td class="px-4 py-3 text-right">{{ course.completionRate | number: '1.0-1' }}%</td>
                <td class="px-4 py-3 text-right">{{ course.upcomingAssignments }}</td>
                <td class="px-4 py-3 text-slate-400">{{ course.lastActivity | date: 'short' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section *ngIf="data.timeline?.length" class="mb-8">
        <h3 class="mb-4 text-lg font-semibold text-slate-100">Upcoming Milestones</h3>
        <ol class="space-y-3">
          <li *ngFor="let item of data.timeline" class="flex items-center justify-between gap-4 rounded-xl border border-slate-800 bg-slate-900/60 px-4 py-3">
            <div>
              <p class="font-medium text-slate-100">{{ item.title }}</p>
              <p class="text-xs text-slate-500">Course • {{ item.courseId }}</p>
            </div>
            <div class="flex flex-col items-end">
              <span class="text-sm font-semibold text-slate-100">{{ item.dueDate | date: 'mediumDate' }}</span>
              <span class="mt-1 text-xs" [ngClass]="timelineBadge(item.status)">{{ item.status | titlecase }}</span>
            </div>
          </li>
        </ol>
      </section>
    </ng-container>

    <ng-template #loading>
      <div class="rounded-xl border border-slate-800 bg-slate-900/60 p-6 text-sm text-slate-400">Loading dashboard data…</div>
    </ng-template>
  `,
})
export class DashboardViewComponent {
  @Input() data: DashboardData | null = null;
  @Input() courses: CourseOverview[] | null = null;
  @Input() title = '';
  @Input() generatedAt?: string;
  @Input() mode?: IntegrationMode;

  formatValue(value: number, format: SummaryMetric['format'] = 'number'): string {
    if (format === 'percent') {
      return `${value.toFixed(1)}%`;
    }
    return value.toLocaleString();
  }

  formatDelta(delta: number, format: SummaryMetric['format'] = 'number'): string {
    const sign = delta > 0 ? '+' : '';
    const suffix = format === 'percent' ? '%' : '';
    return `${sign}${delta.toFixed(1)}${suffix}`;
  }

  trendIcon(trend: SummaryMetric['trend']): string {
    if (trend === 'up') {
      return '▲';
    }
    if (trend === 'down') {
      return '▼';
    }
    return '•';
  }

  trendClass(trend: SummaryMetric['trend']): string {
    switch (trend) {
      case 'up':
        return 'text-emerald-400';
      case 'down':
        return 'text-rose-400';
      default:
        return 'text-slate-500';
    }
  }

  highlightClass(status: Highlight['status']): string {
    switch (status) {
      case 'success':
        return 'bg-emerald-500/10 text-emerald-300 border border-emerald-500/40';
      case 'warning':
        return 'bg-amber-500/10 text-amber-200 border border-amber-500/40';
      default:
        return 'bg-sky-500/10 text-sky-200 border border-sky-500/40';
    }
  }

  timelineBadge(status: TimelineItem['status']): string {
    switch (status) {
      case 'atRisk':
        return 'rounded-full bg-rose-500/20 px-2 py-1 text-rose-200';
      case 'pending':
        return 'rounded-full bg-amber-500/20 px-2 py-1 text-amber-200';
      default:
        return 'rounded-full bg-emerald-500/20 px-2 py-1 text-emerald-200';
    }
  }
}

type SummaryMetric = DashboardData['summary'][number];
type Highlight = DashboardData['highlights'][number];
type TimelineItem = NonNullable<DashboardData['timeline']>[number];
