import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { firstValueFrom } from 'rxjs';

import { ClassroomService, CourseListState } from './classroom.service';
import { IntegrationMode } from '../models/classroom.model';
import { EnvironmentService } from './environment.service';

describe('ClassroomService', () => {
  let service: ClassroomService;
  let http: HttpTestingController;
  const runtimeApiUrl = 'http://runtime-config.local/api/v1';

  const baseCourses = {
    mode: 'mock' as IntegrationMode,
    generatedAt: '2025-10-07T10:00:00Z',
    availableModes: ['mock', 'google'] as IntegrationMode[],
    courses: [],
  };

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        { provide: EnvironmentService, useValue: { apiUrl: runtimeApiUrl } },
      ],
    });

    service = TestBed.inject(ClassroomService);
    http = TestBed.inject(HttpTestingController);
    spyOn(console, 'error').and.stub();
  });

  afterEach(() => {
    http.verify();
  });

  it('loads course state when subscribed', () => {
    let lastState: CourseListState | null = null;
    const sub = service.courseState$.subscribe((state) => (lastState = state));

    expectCoursesRequest().flush(baseCourses);

    expect(lastState).not.toBeNull();
    if (!lastState) {
      fail('Course state did not emit');
      return;
    }
    const state = lastState as CourseListState;
    expect(state.mode).toBe('mock');
    expect(state.availableModes).toEqual(['mock', 'google']);

    sub.unsubscribe();
  });

  it('refresh triggers a second fetch', () => {
    let emissions = 0;
    const sub = service.courseState$.subscribe(() => emissions++);
    expectCoursesRequest().flush(baseCourses);

    service.refresh();
    expectCoursesRequest().flush({ ...baseCourses, generatedAt: '2025-10-07T10:05:00Z' });

    sub.unsubscribe();
    expect(emissions).toBeGreaterThanOrEqual(2);
  });

  it('setMode switches mode and requests matching data', () => {
    const sub = service.courseState$.subscribe();
    expectCoursesRequest().flush(baseCourses);

    service.setMode('google');
    const modeRequest = http.expectOne(`${runtimeApiUrl}/google/courses?mode=google`);
    modeRequest.flush({ ...baseCourses, mode: 'google', generatedAt: '2025-10-07T10:10:00Z' });

    let latestMode: IntegrationMode | undefined;
    const modeSub = service.mode$.subscribe((mode) => (latestMode = mode));

    expect(latestMode).toBe('google');

    modeSub.unsubscribe();
    sub.unsubscribe();
  });

  it('setMode with same value triggers a refresh without changing mode', () => {
    let latestMode: IntegrationMode | undefined;
    const modeSub = service.mode$.subscribe((mode) => (latestMode = mode));
    const stateSub = service.courseState$.subscribe();

    expectCoursesRequest().flush(baseCourses);

    service.setMode('mock');
    expectCoursesRequest().flush({ ...baseCourses, generatedAt: '2025-10-07T10:06:00Z' });

    expect(latestMode).toBe('mock');

    stateSub.unsubscribe();
    modeSub.unsubscribe();
  });

  it('fetches dashboard data for a role', async () => {
    const dashboardPromise = firstValueFrom(service.dashboard('teacher'));

    const dashboardRequest = http.expectOne(`${runtimeApiUrl}/dashboard/teacher?mode=mock`);
    dashboardRequest.flush({
      role: 'teacher',
      mode: 'mock',
      generatedAt: '2025-10-07T10:00:00Z',
      summary: [],
      charts: [],
      highlights: [],
    });

    const dashboard = await dashboardPromise;
    expect(dashboard.role).toBe('teacher');
  });

  it('returns cached dashboard observable for repeated calls', async () => {
    const dashboard$ = service.dashboard('admin');
    const cached$ = service.dashboard('admin');
    expect(cached$).toBe(dashboard$);

    const valuePromise = firstValueFrom(dashboard$);

    const adminRequest = http.expectOne(`${runtimeApiUrl}/dashboard/admin?mode=mock`);
    adminRequest.flush({
      role: 'admin',
      mode: 'mock' as IntegrationMode,
      generatedAt: '2025-10-07T10:00:00Z',
      summary: [],
      charts: [],
      highlights: [],
    });

    const value = await valuePromise;
    expect(value.role).toBe('admin');
  });

  it('normalizes course responses when API omits optional fields', async () => {
    const statePromise = firstValueFrom(service.courseState$);

    expectCoursesRequest().flush({
      generatedAt: '2025-10-08T08:00:00Z',
      courses: [],
      // availableModes y mode ausentes a propósito
    } as unknown as typeof baseCourses);

    const state = await statePromise;
    expect(state.mode).toBe('mock');
    expect(state.availableModes).toEqual(['mock']);
    expect(state.courses).toEqual([]);
  });

  it('gracefully handles failing course request', (done) => {
    const sub = service.courseState$.subscribe((state) => {
      expect(state.courses).toEqual([]);
      sub.unsubscribe();
      done();
    });

    expectCoursesRequest().error(new ErrorEvent('network'));
  });

  function expectCoursesRequest() {
    return http.expectOne(`${runtimeApiUrl}/google/courses?mode=mock`);
  }
});
