import { inject, Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, map, tap } from 'rxjs';

import { AuthResponse, Credentials, OAuthInitResponse } from '../models/auth.model';
import { User, UserRole } from '../models/user.model';
import { EnvironmentService } from './environment.service';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly router = inject(Router);
  private readonly envService = inject(EnvironmentService);

  private readonly tokenStorageKey = 'classsphere.token';
  private readonly userStorageKey = 'classsphere.user';

  private readonly currentUserSubject = new BehaviorSubject<User | null>(null);

  readonly currentUser$ = this.currentUserSubject.asObservable();
  readonly isAuthenticated$ = this.currentUser$.pipe(map((user) => !!user));

  constructor() {
    this.restoreSession();
  }

  login(credentials: Credentials): Observable<User> {
    return this.http
      .post<AuthResponse>(`${this.envService.apiUrl}/auth/login`, credentials)
      .pipe(tap((response) => this.persistSession(response)), map((response) => response.user));
  }

  startOAuth(): Observable<OAuthInitResponse> {
    return this.http.get<OAuthInitResponse>(`${this.envService.apiUrl}/auth/oauth/google`);
  }

  completeOAuth(code: string, state: string): Observable<User> {
    const params = new HttpParams().set('code', code).set('state', state);
    return this.http
      .get<AuthResponse>(`${this.envService.apiUrl}/auth/oauth/callback`, { params })
      .pipe(tap((response) => this.persistSession(response)), map((response) => response.user));
  }

  logout(): void {
    localStorage.removeItem(this.tokenStorageKey);
    localStorage.removeItem(this.userStorageKey);
    this.currentUserSubject.next(null);
  }

  getAccessToken(): string | null {
    return localStorage.getItem(this.tokenStorageKey);
  }

  hasRole(role: UserRole): boolean {
    const user = this.currentUserSubject.value;
    return user?.role === role;
  }

  routeForRole(role: UserRole): string {
    switch (role) {
      case 'admin':
        return '/dashboard/admin';
      case 'coordinator':
        return '/dashboard/coordinator';
      case 'teacher':
        return '/dashboard/teacher';
      default:
        return '/dashboard/student';
    }
  }

  navigateToRoleDashboard(user: User): void {
    this.router.navigateByUrl(this.routeForRole(user.role));
  }

  private persistSession(response: AuthResponse): void {
    localStorage.setItem(this.tokenStorageKey, response.accessToken);
    localStorage.setItem(this.userStorageKey, JSON.stringify(response.user));
    this.currentUserSubject.next(response.user);
  }

  private restoreSession(): void {
    const rawToken = localStorage.getItem(this.tokenStorageKey);
    const rawUser = localStorage.getItem(this.userStorageKey);
    if (!rawToken || !rawUser) {
      return;
    }
    try {
      const user: User = JSON.parse(rawUser);
      this.currentUserSubject.next(user);
    } catch (error) {
      console.error('Failed to restore user from storage', error);
      this.logout();
    }
  }
}
