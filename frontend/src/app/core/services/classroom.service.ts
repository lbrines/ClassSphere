import { inject, Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { BehaviorSubject, Observable, Subject, combineLatest, map, of, shareReplay, startWith, switchMap, catchError, distinctUntilChanged } from 'rxjs';

import { IntegrationMode, CourseListResponse, DashboardData } from '../models/classroom.model';
import { UserRole } from '../models/user.model';
import { EnvironmentService } from './environment.service';

export interface CourseListState {
  mode: IntegrationMode;
  generatedAt: string;
  availableModes: IntegrationMode[];
  courses: CourseListResponse['courses'];
}

@Injectable({ providedIn: 'root' })
export class ClassroomService {
  private readonly http = inject(HttpClient);
  private readonly environmentService = inject(EnvironmentService);

  private readonly modeSubject = new BehaviorSubject<IntegrationMode>('mock');
  private readonly refreshSubject = new Subject<void>();
  private readonly dashboardCache = new Map<UserRole, Observable<DashboardData>>();

  readonly mode$ = this.modeSubject.asObservable().pipe(distinctUntilChanged());

  private readonly coursesStateInternal$ = combineLatest([
    this.mode$,
    this.refreshSubject.pipe(startWith<void>(undefined)),
  ]).pipe(
    switchMap(([mode]) => {
      let params = new HttpParams();
      if (mode) {
        params = params.set('mode', mode);
      }
      return this.http
        .get<CourseListResponse>(`${this.environmentService.apiUrl}/google/courses`, { params })
        .pipe(
          map((response) => this.normalizeCourseState(response, mode)),
          catchError((error) => {
            console.error('Failed to load courses', error);
            const fallback: CourseListState = {
              mode,
              generatedAt: new Date().toISOString(),
              availableModes: [mode],
              courses: [],
            };
            return of(fallback);
          }),
        );
    }),
    shareReplay({ bufferSize: 1, refCount: true }),
  );

  readonly courseState$ = this.coursesStateInternal$;
  readonly availableModes$ = this.coursesStateInternal$.pipe(map((state) => state.availableModes));

  setMode(mode: IntegrationMode): void {
    if (mode === this.modeSubject.value) {
      this.refreshSubject.next();
      return;
    }
    this.modeSubject.next(mode);
  }

  refresh(): void {
    this.refreshSubject.next();
  }

  courses(): Observable<CourseListState['courses']> {
    return this.coursesStateInternal$.pipe(map((state) => state.courses));
  }

  dashboard(role: UserRole): Observable<DashboardData> {
    if (!this.dashboardCache.has(role)) {
      const stream = combineLatest([
        this.mode$,
        this.refreshSubject.pipe(startWith<void>(undefined)),
      ]).pipe(
        switchMap(([mode]) => {
          let params = new HttpParams();
          if (mode) {
            params = params.set('mode', mode);
          }
          return this.http.get<DashboardData>(`${this.environmentService.apiUrl}/dashboard/${role}`, { params });
        }),
        shareReplay({ bufferSize: 1, refCount: true }),
      );
      this.dashboardCache.set(role, stream);
    }
    return this.dashboardCache.get(role)!;
  }

  private normalizeCourseState(response: CourseListResponse, requestedMode: IntegrationMode): CourseListState {
    const normalizedModes = Array.from(
      new Set<IntegrationMode>([requestedMode, ...(response.availableModes ?? [])])
    ) as IntegrationMode[];

    return {
      mode: response.mode ?? requestedMode,
      generatedAt: response.generatedAt,
      availableModes: normalizedModes,
      courses: response.courses ?? [],
    };
  }
}
