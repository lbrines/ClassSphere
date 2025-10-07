import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { firstValueFrom } from 'rxjs';
import { skip, take } from 'rxjs/operators';

import { environment } from '../../../environments/environment';
import { IntegrationMode } from '../models/classroom.model';
import { ClassroomService } from './classroom.service';

describe('ClassroomService', () => {
  let service: ClassroomService;
  let http: HttpTestingController;

  const courseUrl = `${environment.apiUrl}/google/courses?mode=mock`;
  const defaultCourseResponse = {
    mode: 'mock' as const,
    generatedAt: '2025-10-07T10:00:00Z',
    availableModes: ['mock', 'google'] as IntegrationMode[],
    courses: [],
  };

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
    });

    service = TestBed.inject(ClassroomService);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    http.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('loads courses for the default mode', async () => {
    const statePromise = firstValueFrom(service.courseState$);
    mockCourses();
    const state = await statePromise;

    expect(state.mode).toBe('mock');
    expect(state.availableModes).toContain('google');
    expect(state.courses).toEqual([]);
  });

  it('refresh triggers course reload', async () => {
    const states: string[] = [];
    const subscription = service.courseState$.subscribe((state) => states.push(state.generatedAt));

    mockCourses();
    service.refresh();
    mockCourses({ ...defaultCourseResponse, generatedAt: '2025-10-07T10:01:00Z' });

    expect(states.length).toBeGreaterThanOrEqual(2);
    expect(states[0]).toBe('2025-10-07T10:00:00Z');
    expect(states[1]).toBe('2025-10-07T10:01:00Z');
    subscription.unsubscribe();
  });

  it('setMode changes the current mode', async () => {
    // Load initial state
    mockCourses();
    await firstValueFrom(service.courseState$);

    // Change mode
    service.setMode('google');

    // Should trigger new request with google mode
    const req = http.expectOne(`${environment.apiUrl}/google/courses?mode=google`);
    req.flush({
      mode: 'google' as const,
      generatedAt: '2025-10-07T10:02:00Z',
      availableModes: ['mock', 'google'] as IntegrationMode[],
      courses: [],
    });

    const state = await firstValueFrom(service.courseState$);
    expect(state.mode).toBe('google');
  });

  it('availableModes$ provides available modes', async () => {
    mockCourses();
    await firstValueFrom(service.courseState$);

    const modes = await firstValueFrom(service.availableModes$);
    expect(modes).toEqual(['google', 'mock']);
  });

  it('mode$ provides current mode', async () => {
    mockCourses();
    await firstValueFrom(service.courseState$);

    const mode = await firstValueFrom(service.mode$);
    expect(mode).toBe('mock');

    service.setMode('google');
    const googleMode = await firstValueFrom(service.mode$);
    expect(googleMode).toBe('google');
  });

  it('falls back to empty courses when request fails', async () => {
    const statePromise = firstValueFrom(service.courseState$);

    const req = http.expectOne(courseUrl);
    req.flush({}, { status: 500, statusText: 'server error' });

    const state = await statePromise;
    expect(state.courses).toEqual([]);
    expect(state.mode).toBe('mock');
    expect(state.availableModes).toEqual([]);
  });

  it('handles network errors gracefully', async () => {
    const statePromise = firstValueFrom(service.courseState$);

    const req = http.expectOne(courseUrl);
    req.error(new ErrorEvent('network error'));

    const state = await statePromise;
    expect(state.courses).toEqual([]);
  });

  it('handles malformed responses', async () => {
    const statePromise = firstValueFrom(service.courseState$);

    const req = http.expectOne(courseUrl);
    req.flush({ invalid: 'response' });

    const state = await statePromise;
    expect(state.courses).toEqual([]);
  });

  it('loads dashboard data for specific role', async () => {
    mockDashboard('mock');

    const dashboard = await firstValueFrom(service.dashboard('admin'));
    expect(dashboard.role).toBe('admin');
    expect(dashboard.mode).toBe('mock');
  });

  it('handles dashboard request failures', async () => {
    const req = http.expectOne(`${environment.apiUrl}/dashboard/admin?mode=mock`);
    req.flush({}, { status: 500, statusText: 'server error' });

    await expectAsync(firstValueFrom(service.dashboard('admin'))).toBeRejected();
  });

  it('handles invalid mode gracefully', async () => {
    // @ts-ignore - testing invalid mode
    service.setMode('invalid');

    // Should fall back to default mode
    const state = await firstValueFrom(service.courseState$);
    expect(state.mode).toBe('mock');
  });

  it('handles empty available modes', async () => {
    mockCourses({ ...defaultCourseResponse, availableModes: [] });
    const state = await firstValueFrom(service.courseState$);

    expect(state.availableModes).toEqual([]);
  });

  it('handles courses with data', async () => {
    const coursesWithData = {
      ...defaultCourseResponse,
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
          lastActivity: '2025-10-07T10:00:00Z'
        }
      ] as any
    };

    mockCourses(coursesWithData);
    const state = await firstValueFrom(service.courseState$);

    expect(state.courses).toHaveSize(1);
    expect(state.courses[0].name).toBe('Math 101');
  });

  function mockCourses(response: typeof defaultCourseResponse = defaultCourseResponse): void {
    const req = http.expectOne(courseUrl);
    req.flush(response);
  }

  function mockDashboard(mode: IntegrationMode): void {
    const req = http.expectOne(`${environment.apiUrl}/dashboard/admin?mode=${mode}`);
    req.flush({
      role: 'admin',
      mode,
      generatedAt: '2025-10-07T10:00:00Z',
      summary: [],
      charts: [],
      highlights: [],
    });
  }
});
