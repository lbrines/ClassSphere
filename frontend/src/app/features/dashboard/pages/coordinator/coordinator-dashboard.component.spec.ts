import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';

import { ClassroomService } from '../../../../core/services/classroom.service';
import { CourseOverview, DashboardData, IntegrationMode } from '../../../../core/models/classroom.model';
import { ApexChartComponent } from '../../../../shared/components/apex-chart/apex-chart.component';
import { CoordinatorDashboardComponent } from './coordinator-dashboard.component';

const sampleDashboard: DashboardData = {
  role: 'coordinator',
  mode: 'mock',
  generatedAt: '2025-10-07T10:00:00Z',
  summary: [],
  charts: [],
  highlights: [],
  courses: [],
  timeline: [],
  alerts: [],
};

const sampleCourseState: {
  mode: 'mock';
  generatedAt: string;
  availableModes: IntegrationMode[];
  courses: CourseOverview[];
} = {
  mode: 'mock',
  generatedAt: '2025-10-07T10:00:00Z',
  availableModes: ['mock'],
  courses: [],
};

class ClassroomServiceStub {
  dashboardResponse: DashboardData = sampleDashboard;
  courseStateResponse = sampleCourseState;

  dashboard() {
    return of(this.dashboardResponse);
  }

  get courseState$() {
    return of(this.courseStateResponse);
  }
}

describe('CoordinatorDashboardComponent', () => {
  let fixture: ComponentFixture<CoordinatorDashboardComponent>;
  let classroomService: ClassroomServiceStub;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CoordinatorDashboardComponent],
      providers: [{ provide: ClassroomService, useClass: ClassroomServiceStub }],
    }).compileComponents();

    spyOn(ApexChartComponent.prototype as any, 'createChart').and.returnValue({
      render: jasmine.createSpy('render').and.returnValue(Promise.resolve()),
      updateOptions: jasmine.createSpy('updateOptions').and.returnValue(Promise.resolve()),
      destroy: jasmine.createSpy('destroy'),
    } as never);

    classroomService = TestBed.inject(ClassroomService) as unknown as ClassroomServiceStub;
  });

  function createComponent(): ComponentFixture<CoordinatorDashboardComponent> {
    fixture = TestBed.createComponent(CoordinatorDashboardComponent);
    fixture.detectChanges();
    return fixture;
  }

  it('renders the coordinator dashboard view', () => {
    createComponent();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.textContent).toContain('Program Coordination');
  });

  it('prefers dashboard-specific courses when available', () => {
    classroomService.dashboardResponse = {
      ...sampleDashboard,
      courses: [
        {
          id: 'c-1',
          name: 'Advanced Integration Patterns',
          section: 'Section A',
          program: 'STEM',
          primaryTeacher: 'Morgan Day',
          enrollment: 32,
          completionRate: 0.89,
          upcomingAssignments: 4,
          lastActivity: '2025-02-01T00:00:00Z',
        },
      ],
    };

    const localFixture = createComponent();
    let latestVm: { displayCourses: DashboardData['courses'] } | undefined;
    const subscription = localFixture.componentInstance.vm$.subscribe((vm) => {
      latestVm = vm;
    });
    subscription.unsubscribe();

    expect(latestVm?.displayCourses?.length).toBe(1);
    expect(latestVm?.displayCourses?.[0].name).toBe('Advanced Integration Patterns');
  });
});
