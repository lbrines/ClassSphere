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

  it('loads courses for the default mode', async () => {
    const statePromise = firstValueFrom(service.courseState$);
    mockCourses();
    const state = await statePromise;

    expect(state.mode).toBe('mock');
    expect(state.availableModes).toContain('google');
  });

  it('refresh triggers course reload', async () => {
    const states: string[] = [];
    const subscription = service.courseState$.subscribe((state) => states.push(state.mode));

    mockCourses();
    service.refresh();
    mockCourses({ ...defaultCourseResponse, generatedAt: '2025-10-07T10:01:00Z' });

    expect(states.length).toBeGreaterThanOrEqual(2);
    subscription.unsubscribe();
  });

  it('falls back to empty courses when request fails', async () => {
    const statePromise = firstValueFrom(service.courseState$);

    const req = http.expectOne(courseUrl);
    req.flush({}, { status: 500, statusText: 'server error' });

    const state = await statePromise;
    expect(state.courses).toEqual([]);
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
