import { inject, Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { BehaviorSubject, Observable, map, tap, catchError, of, finalize } from 'rxjs';

import { SearchResponse, SearchFilters, SearchState, SearchResult } from '../models/search.model';
import { EnvironmentService } from './environment.service';

/**
 * SearchService - Phase 3 Advanced Search
 * 
 * Provides multi-entity search functionality across:
 * - Students
 * - Courses
 * - Assignments
 * 
 * Features:
 * - Real-time search with debounce
 * - Advanced filtering (date range, status, course)
 * - Pagination support
 * - Search state management with RxJS
 */
@Injectable({ providedIn: 'root' })
export class SearchService {
  private readonly http = inject(HttpClient);
  private readonly environmentService = inject(EnvironmentService);

  private readonly searchStateSubject = new BehaviorSubject<SearchState>({
    loading: false,
    query: '',
    filters: { entityType: 'all' },
    results: [],
    total: 0,
    error: null,
  });

  readonly searchState$ = this.searchStateSubject.asObservable();

  /**
   * Perform multi-entity search with filters and pagination
   * 
   * @param query - Search query string
   * @param filters - Search filters (entityType, course, date range, etc.)
   * @param page - Page number (1-indexed, default: 1)
   * @param pageSize - Results per page (default: 10)
   * @returns Observable of SearchResponse
   */
  search(query: string, filters: SearchFilters, page: number = 1, pageSize: number = 10): Observable<SearchResponse> {
    // Update loading state
    this.updateState({ loading: true, query, filters, error: null });

    // Build query parameters for backend API
    let params = new HttpParams()
      .set('q', query.trim())
      .set('entities', this.mapEntityTypeToEntities(filters.entityType))
      .set('limit', pageSize.toString())
      .set('page', page.toString());

    // Add optional filters
    if (filters.course) {
      params = params.set('course', filters.course);
    }
    if (filters.status) {
      params = params.set('status', filters.status);
    }
    if (filters.dateFrom) {
      params = params.set('dateFrom', filters.dateFrom);
    }
    if (filters.dateTo) {
      params = params.set('dateTo', filters.dateTo);
    }

    return this.http
      .get<SearchResponse>(`${this.environmentService.apiUrl}/search`, { params })
      .pipe(
        tap((response) => {
          this.updateState({
            loading: false,
            results: response.results || [],
            total: response.total || 0,
            error: null,
          });
        }),
        catchError((error) => {
          this.updateState({
            loading: false,
            error: error.message || 'Search failed',
            results: [],
            total: 0,
          });
          throw error;
        }),
        finalize(() => {
          // Ensure loading is always set to false
          const currentState = this.searchStateSubject.value;
          if (currentState.loading) {
            this.updateState({ loading: false });
          }
        })
      );
  }

  /**
   * Map frontend entity type to backend entities parameter
   * Backend expects comma-separated entity types (e.g., "courses", "students,teachers")
   */
  private mapEntityTypeToEntities(entityType: string): string {
    switch (entityType) {
      case 'student':
        return 'students';
      case 'course':
        return 'courses';
      case 'assignment':
        return 'assignments';
      case 'all':
        return 'students,teachers,courses,assignments,announcements';
      default:
        return 'courses'; // Safe default
    }
  }

  /**
   * Clear search results and reset state
   */
  clearSearch(): void {
    this.searchStateSubject.next({
      loading: false,
      query: '',
      filters: { entityType: 'all' },
      results: [],
      total: 0,
      error: null,
    });
  }

  /**
   * Get current search state (synchronous)
   */
  getCurrentState(): SearchState {
    return this.searchStateSubject.value;
  }

  /**
   * Update search state partially
   */
  private updateState(partial: Partial<SearchState>): void {
    this.searchStateSubject.next({
      ...this.searchStateSubject.value,
      ...partial,
    });
  }

  /**
   * Get search history (for future implementation)
   */
  getSearchHistory(): string[] {
    return []; // Placeholder for future feature
  }
}
