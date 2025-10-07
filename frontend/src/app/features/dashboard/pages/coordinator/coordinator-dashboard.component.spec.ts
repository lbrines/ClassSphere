import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';

import { ClassroomService } from '../../../../core/services/classroom.service';
import { DashboardData } from '../../../../core/models/classroom.model';
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

class ClassroomServiceStub {
  dashboard() {
    return of(sampleDashboard);
  }

  get courseState$() {
    return of({
      mode: 'mock',
      generatedAt: '2025-10-07T10:00:00Z',
      availableModes: ['mock'],
      courses: [],
    });
  }
}

describe('CoordinatorDashboardComponent', () => {
  let fixture: ComponentFixture<CoordinatorDashboardComponent>;

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

    fixture = TestBed.createComponent(CoordinatorDashboardComponent);
    fixture.detectChanges();
  });

  it('renders the coordinator dashboard view', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.textContent).toContain('Program Coordination');
  });
});
