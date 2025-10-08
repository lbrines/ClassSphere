import { Component, OnInit, OnDestroy, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { Subject, takeUntil } from 'rxjs';

import { SearchBarComponent } from '../../components/search-bar/search-bar.component';
import { SearchResultsComponent } from '../../components/search-results/search-results.component';
import { SearchService } from '../../../../core/services/search.service';
import { SearchResult, SearchFilters } from '../../../../core/models/search.model';

/**
 * SearchPageComponent - Phase 3 Search Page Container
 * 
 * Integrates SearchBar and SearchResults components
 * Manages search state and navigation
 */
@Component({
  selector: 'app-search-page',
  standalone: true,
  imports: [CommonModule, SearchBarComponent, SearchResultsComponent],
  template: `
    <div class="search-page-container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Page Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Search</h1>
        <p class="text-gray-600">
          Search for students, courses, and assignments across all your classes
        </p>
      </div>

      <!-- Search Bar -->
      <div class="mb-8">
        <app-search-bar
          [enableAutoSearch]="false"
          (searchTriggered)="onSearchTriggered($event)"
          (searchCleared)="onSearchCleared()"
        ></app-search-bar>
      </div>

      <!-- Search Results -->
      <app-search-results
        [results]="searchState.results"
        [total]="searchState.total"
        [page]="currentPage"
        [pageSize]="pageSize"
        [loading]="searchState.loading"
        [query]="searchState.query"
        (resultClicked)="onResultClicked($event)"
        (pageChanged)="onPageChanged($event)"
      ></app-search-results>

      <!-- Error Message -->
      <div
        *ngIf="searchState.error"
        class="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg"
        role="alert"
      >
        <p class="text-red-800">
          <strong>Error:</strong> {{ searchState.error }}
        </p>
      </div>
    </div>
  `,
  styles: [],
})
export class SearchPageComponent implements OnInit, OnDestroy {
  private readonly searchService = inject(SearchService);
  private readonly router = inject(Router);
  private readonly destroy$ = new Subject<void>();

  searchState: {
    loading: boolean;
    query: string;
    filters: SearchFilters;
    results: SearchResult[];
    total: number;
    error: string | null;
  } = {
    loading: false,
    query: '',
    filters: { entityType: 'all' },
    results: [],
    total: 0,
    error: null,
  };

  currentPage = 1;
  pageSize = 10;

  ngOnInit(): void {
    this.searchService.searchState$
      .pipe(takeUntil(this.destroy$))
      .subscribe((state) => {
        this.searchState = state;
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  onSearchTriggered(event: { query: string; filters: SearchFilters }): void {
    this.currentPage = 1; // Reset pagination on new search
    console.log('Search triggered:', event);
    
    // Execute search with pagination
    this.searchService
      .search(event.query, event.filters, this.currentPage, this.pageSize)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        error: (error) => {
          console.error('Search failed:', error);
        },
      });
  }

  onSearchCleared(): void {
    this.currentPage = 1;
    this.searchState = {
      loading: false,
      query: '',
      filters: { entityType: 'all' },
      results: [],
      total: 0,
      error: null,
    };
  }

  onResultClicked(result: SearchResult): void {
    console.log('Result clicked:', result);

    // Navigate to detail page based on entity type
    switch (result.type) {
      case 'student':
        this.router.navigate(['/students', result.id]);
        break;
      case 'course':
        this.router.navigate(['/courses', result.id]);
        break;
      case 'assignment':
        this.router.navigate(['/assignments', result.id]);
        break;
    }
  }

  onPageChanged(page: number): void {
    if (page < 1) {
      return;
    }
    
    this.currentPage = page;

    // Re-execute search with new page and pagination params
    if (this.searchState.query) {
      this.searchService
        .search(this.searchState.query, this.searchState.filters, this.currentPage, this.pageSize)
        .pipe(takeUntil(this.destroy$))
        .subscribe({
          error: (error) => {
            console.error('Page search failed:', error);
          },
        });
    }
  }
}

