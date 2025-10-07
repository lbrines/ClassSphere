import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SimpleChange, SimpleChanges } from '@angular/core';

import { DashboardViewComponent } from './dashboard-view.component';
import { DashboardData, CourseOverview, IntegrationMode } from '../../../core/models/classroom.model';

describe('DashboardViewComponent', () => {
  let component: DashboardViewComponent;
  let fixture: ComponentFixture<DashboardViewComponent>;

  const mockDashboardData: DashboardData = {
    role: 'admin',
    mode: 'mock',
    generatedAt: new Date().toISOString(),
    summary: [
      {
        id: 'totalCourses',
        label: 'Total Courses',
        value: 10,
        delta: 2,
        trend: 'up',
        format: 'number'
      },
      {
        id: 'completionRate',
        label: 'Completion Rate',
        value: 85.5,
        delta: -5.2,
        trend: 'down',
        format: 'percent'
      }
    ],
    charts: [
      {
        id: 'chart1',
        title: 'Test Chart',
        type: 'bar',
        series: [
          {
            name: 'Series 1',
            data: [{ x: 'Jan', y: 10 }, { x: 'Feb', y: 20 }]
          }
        ]
      }
    ],
    highlights: [
      {
        id: 'highlight1',
        title: 'Excellent Performance',
        details: 'Great job this month',
        status: 'success'
      }
    ],
    timeline: [
      {
        id: 'timeline1',
        title: 'Assignment Due',
        courseId: 'course1',
        dueDate: new Date().toISOString(),
        status: 'pending'
      }
    ],
    courses: [
      {
        id: 'course1',
        name: 'Math 101',
        section: 'A',
        program: 'Mathematics',
        primaryTeacher: 'John Doe',
        enrollment: 25,
        completionRate: 85.5,
        upcomingAssignments: 2,
        lastActivity: new Date().toISOString()
      }
    ]
  };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DashboardViewComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(DashboardViewComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('formatValue', () => {
    it('should format number values correctly', () => {
      expect(component.formatValue(1234.56)).toBe('1,234.56');
      expect(component.formatValue(0)).toBe('0');
      expect(component.formatValue(-123)).toBe('-123');
    });

    it('should format percentage values correctly', () => {
      expect(component.formatValue(85.5, 'percent')).toBe('85.5%');
      expect(component.formatValue(100, 'percent')).toBe('100.0%');
      expect(component.formatValue(0, 'percent')).toBe('0.0%');
    });

    it('should handle decimal precision', () => {
      expect(component.formatValue(123.456, 'percent')).toBe('123.5%');
    });
  });

  describe('formatDelta', () => {
    it('should format positive delta correctly', () => {
      expect(component.formatDelta(5.2)).toBe('+5.2');
      expect(component.formatDelta(5.2, 'percent')).toBe('+5.2%');
    });

    it('should format negative delta correctly', () => {
      expect(component.formatDelta(-3.1)).toBe('-3.1');
      expect(component.formatDelta(-3.1, 'percent')).toBe('-3.1%');
    });

    it('should format zero delta correctly', () => {
      expect(component.formatDelta(0)).toBe('0.0');
      expect(component.formatDelta(0, 'percent')).toBe('0.0%');
    });

    it('should handle decimal precision', () => {
      expect(component.formatDelta(5.123)).toBe('+5.1');
    });
  });

  describe('trendIcon', () => {
    it('should return correct icon for up trend', () => {
      expect(component.trendIcon('up')).toBe('▲');
    });

    it('should return correct icon for down trend', () => {
      expect(component.trendIcon('down')).toBe('▼');
    });

    it('should return default icon for flat trend', () => {
      expect(component.trendIcon('flat')).toBe('•');
    });

    it('should handle undefined trend', () => {
      // @ts-ignore - testing runtime behavior
      expect(component.trendIcon(undefined)).toBe('•');
    });
  });

  describe('trendClass', () => {
    it('should return correct CSS class for up trend', () => {
      expect(component.trendClass('up')).toBe('text-emerald-400');
    });

    it('should return correct CSS class for down trend', () => {
      expect(component.trendClass('down')).toBe('text-rose-400');
    });

    it('should return default CSS class for flat trend', () => {
      expect(component.trendClass('flat')).toBe('text-slate-500');
    });
  });

  describe('highlightClass', () => {
    it('should return correct CSS class for success status', () => {
      expect(component.highlightClass('success')).toBe('bg-emerald-500/10 text-emerald-300 border border-emerald-500/40');
    });

    it('should return correct CSS class for warning status', () => {
      expect(component.highlightClass('warning')).toBe('bg-amber-500/10 text-amber-200 border border-amber-500/40');
    });

    it('should return default CSS class for info status', () => {
      expect(component.highlightClass('info')).toBe('bg-sky-500/10 text-sky-200 border border-sky-500/40');
    });
  });

  describe('timelineBadge', () => {
    it('should return correct CSS class for atRisk status', () => {
      expect(component.timelineBadge('atRisk')).toBe('rounded-full bg-rose-500/20 px-2 py-1 text-rose-200');
    });

    it('should return correct CSS class for pending status', () => {
      expect(component.timelineBadge('pending')).toBe('rounded-full bg-amber-500/20 px-2 py-1 text-amber-200');
    });

    it('should return default CSS class for other statuses', () => {
      expect(component.timelineBadge('onTrack')).toBe('rounded-full bg-emerald-500/20 px-2 py-1 text-emerald-200');
    });
  });

  describe('component integration', () => {
    beforeEach(() => {
      component.data = mockDashboardData;
      component.courses = mockDashboardData.courses || [];
      component.title = 'Test Dashboard';
      component.generatedAt = mockDashboardData.generatedAt;
      component.mode = 'mock';
      fixture.detectChanges();
    });

    it('should render dashboard data correctly', () => {
      const compiled = fixture.nativeElement as HTMLElement;

      // Check if summary metrics are rendered
      const summaryElements = compiled.querySelectorAll('.grid > article');
      expect(summaryElements.length).toBeGreaterThan(0);

      // Check if charts are rendered
      const chartElements = compiled.querySelectorAll('.grid > div');
      expect(chartElements.length).toBeGreaterThan(0);

      // Check if highlights are rendered
      const highlightElements = compiled.querySelectorAll('[class*="bg-emerald-500/10"]');
      expect(highlightElements.length).toBeGreaterThan(0);

      // Check if courses table is rendered
      const courseTable = compiled.querySelector('table');
      expect(courseTable).toBeTruthy();
    });

    it('should handle null data gracefully', () => {
      component.data = null;
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const loadingTemplate = compiled.querySelector('ng-template');
      expect(loadingTemplate).toBeTruthy();
    });

    it('should handle empty arrays gracefully', () => {
      component.data = {
        ...mockDashboardData,
        summary: [],
        charts: [],
        highlights: [],
        timeline: [],
        courses: []
      };
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;

      // Should not crash and should show basic structure
      const header = compiled.querySelector('header');
      expect(header).toBeTruthy();
    });

    it('should respond to input changes', () => {
      const newData: DashboardData = {
        ...mockDashboardData,
        summary: [
          {
            id: 'newMetric',
            label: 'New Metric',
            value: 42,
            delta: 1,
            trend: 'up',
            format: 'number'
          }
        ]
      };

      component.data = newData;
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const summaryElements = compiled.querySelectorAll('.grid > article');
      // Should have at least 1 element
      expect(summaryElements.length).toBeGreaterThanOrEqual(1);
    });
  });

  describe('edge cases and error handling', () => {
    it('should handle very large numbers', () => {
      expect(component.formatValue(999999999)).toBe('999,999,999');
    });

    it('should handle very small numbers', () => {
      expect(component.formatValue(0.001)).toBe('0.001');
      expect(component.formatValue(0.001, 'percent')).toBe('0.0%');
    });

    it('should handle negative percentages', () => {
      expect(component.formatValue(-15.5, 'percent')).toBe('-15.5%');
      expect(component.formatDelta(-5.2, 'percent')).toBe('-5.2%');
    });

    it('should handle zero values', () => {
      expect(component.formatValue(0)).toBe('0');
      expect(component.formatValue(0, 'percent')).toBe('0.0%');
      expect(component.formatDelta(0)).toBe('0.0');
    });

    it('should handle NaN values gracefully', () => {
      expect(component.formatValue(NaN)).toBe('NaN');
      expect(component.formatDelta(NaN)).toBe('NaN');
    });

    it('should handle Infinity values', () => {
      expect(component.formatValue(Infinity)).toBe('Infinity');
      expect(component.formatDelta(Infinity)).toBe('+Infinity');
    });
  });
});
