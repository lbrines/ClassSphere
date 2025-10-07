import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DashboardViewComponent } from './dashboard-view.component';
import { DashboardData } from '../../../core/models/classroom.model';

const sampleDashboard: DashboardData = {
  role: 'admin',
  mode: 'mock',
  generatedAt: '2025-10-07T10:00:00Z',
  summary: [
    { id: 'courses', label: 'Courses', value: 12, delta: 2.5, trend: 'up', format: 'number' },
    { id: 'completion', label: 'Completion', value: 88.2, delta: -3.4, trend: 'down', format: 'percent' },
  ],
  charts: [
    {
      id: 'progress',
      title: 'Progress',
      type: 'bar',
      series: [
        {
          name: 'Completed',
          data: [
            { x: 'Week 1', y: 10 },
            { x: 'Week 2', y: 15 },
          ],
        },
      ],
    },
  ],
  highlights: [
    { id: 'h1', title: 'Great engagement', details: 'Students are engaging more.', status: 'success' },
    { id: 'h2', title: 'Assignments due', details: 'Two assignments due this week.', status: 'warning' },
  ],
  timeline: [
    { id: 't1', title: 'Midterm review', courseId: 'course-1', dueDate: '2025-10-10T12:00:00Z', status: 'onTrack' },
  ],
  courses: [
    {
      id: 'course-1',
      name: 'Math 101',
      section: 'A',
      program: 'Mathematics',
      primaryTeacher: 'John Doe',
      enrollment: 30,
      completionRate: 86.4,
      upcomingAssignments: 2,
      lastActivity: '2025-10-06T08:30:00Z',
    },
  ],
  alerts: ['Performance drop detected'],
};

describe('DashboardViewComponent', () => {
  let fixture: ComponentFixture<DashboardViewComponent>;
  let component: DashboardViewComponent;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DashboardViewComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(DashboardViewComponent);
    component = fixture.componentInstance;
  });

  it('renders dashboard content when data is provided', () => {
    component.data = sampleDashboard;
    component.courses = sampleDashboard.courses ?? [];
    component.title = 'Administrator overview';
    component.mode = 'mock';
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;

    expect(compiled.querySelector('h2')?.textContent).toContain('Administrator overview');
    expect(compiled.querySelectorAll('article').length).toBeGreaterThan(0);
    expect(compiled.querySelector('table')).not.toBeNull();
  });

  it('shows loading placeholder when data is missing', () => {
    component.data = null;
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.textContent).toContain('Loading dashboard data');
  });

  it('formats metric values and deltas consistently', () => {
    expect(component.formatValue(1234.56)).toBe('1,234.56');
    expect(component.formatValue(88.2, 'percent')).toBe('88.2%');

    expect(component.formatDelta(3.25)).toBe('+3.3');
    expect(component.formatDelta(-1.5, 'percent')).toBe('-1.5%');
  });

  it('maps trends and highlight badges to styling helpers', () => {
    expect(component.trendIcon('up')).toBe('▲');
    expect(component.trendIcon('down')).toBe('▼');
    expect(component.trendClass('flat')).toBe('text-slate-500');

    expect(component.highlightClass('success')).toContain('emerald');
    expect(component.highlightClass('warning')).toContain('amber');
    expect(component.timelineBadge('atRisk')).toContain('rose');
  });
});
