import { inject, Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { BehaviorSubject, Observable, map, tap, catchError, of, finalize } from 'rxjs';

import { environment } from '../../../environments/environment';
import { SearchResponse, SearchFilters, SearchState, SearchResult } from '../models/search.model';

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
   * Perform multi-entity search with filters
   * 
   * @param query - Search query string
   * @param filters - Search filters (entityType, course, date range, etc.)
   * @returns Observable of SearchResponse
   */
  search(query: string, filters: SearchFilters): Observable<SearchResponse> {
    // Update loading state
    this.updateState({ loading: true, query, filters, error: null });

    // Build query parameters
    let params = new HttpParams()
      .set('q', query.trim())
      .set('type', filters.entityType);

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
      .get<SearchResponse>(`${environment.apiUrl}/search`, { params })
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

