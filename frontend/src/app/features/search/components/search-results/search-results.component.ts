import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SearchResult, SearchEntityType } from '../../../../core/models/search.model';

/**
 * SearchResultsComponent - Phase 3 Advanced Search Results Display
 * 
 * Features:
 * - Display multi-entity search results
 * - Entity-specific icons and metadata
 * - Pagination support
 * - Loading states
 * - Empty states
 * - Accessible keyboard navigation
 * - Click events for result selection
 */
@Component({
  selector: 'app-search-results',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="search-results-container">
      <!-- Loading State -->
      <div *ngIf="loading" class="loading-indicator flex items-center justify-center py-12" aria-live="polite" aria-busy="true">
        <svg
          class="animate-spin h-8 w-8 text-blue-600"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            class="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            stroke-width="4"
          ></circle>
          <path
            class="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          ></path>
        </svg>
        <span class="ml-3 text-gray-600">Loading results...</span>
      </div>

      <!-- Results Count -->
      <div *ngIf="!loading && results.length > 0" class="results-count mb-4 text-sm text-gray-600">
        Found <strong>{{ total }}</strong> {{ total === 1 ? 'result' : 'results' }}
      </div>

      <!-- Results List -->
      <div *ngIf="!loading && results.length > 0" role="list" class="results-list space-y-3">
        <div
          *ngFor="let result of results"
          role="listitem"
          tabindex="0"
          (click)="onResultClick(result)"
          (keydown.enter)="onResultClick(result)"
          (keydown.space)="onResultClick(result)"
          class="result-item p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <div class="flex items-start gap-3">
            <!-- Entity Icon -->
            <div class="result-icon flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center" 
                 [ngClass]="getIconClass(result.type)">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" [attr.aria-label]="result.type + ' icon'">
                <path *ngIf="result.type === 'student'" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" />
                <path *ngIf="result.type === 'course'" d="M10.394 2.08a1 1 0 00-.788 0l-7 3a1 1 0 000 1.84L5.25 8.051a.999.999 0 01.356-.257l4-1.714a1 1 0 11.788 1.838L7.667 9.088l1.94.831a1 1 0 00.787 0l7-3a1 1 0 000-1.838l-7-3zM3.31 9.397L5 10.12v4.102a8.969 8.969 0 00-1.05-.174 1 1 0 01-.89-.89 11.115 11.115 0 01.25-3.762zM9.3 16.573A9.026 9.026 0 007 14.935v-3.957l1.818.78a3 3 0 002.364 0l5.508-2.361a11.026 11.026 0 01.25 3.762 1 1 0 01-.89.89 8.968 8.968 0 00-5.35 2.524 1 1 0 01-1.4 0zM6 18a1 1 0 001-1v-2.065a8.935 8.935 0 00-2-.712V17a1 1 0 001 1z" />
                <path *ngIf="result.type === 'assignment'" d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" />
              </svg>
            </div>

            <!-- Result Content -->
            <div class="flex-1 min-w-0">
              <h3 class="result-name text-lg font-semibold text-gray-900 mb-1">
                {{ result.name }}
              </h3>
              <p *ngIf="result.description" class="result-description text-sm text-gray-600 mb-2">
                {{ result.description }}
              </p>
              
              <!-- Metadata -->
              <div class="result-metadata flex flex-wrap gap-3 text-xs text-gray-500">
                <span *ngFor="let item of getMetadataArray(result.metadata)" class="inline-flex items-center">
                  <span class="font-medium">{{ item.key }}:</span>
                  <span class="ml-1">{{ item.value }}</span>
                </span>
              </div>

              <!-- Relevance Score (for debugging, can be hidden in production) -->
              <div class="mt-2 text-xs text-gray-400">
                Relevance: {{ (result.relevanceScore * 100).toFixed(0) }}%
              </div>
            </div>

            <!-- Entity Type Badge -->
            <div class="flex-shrink-0">
              <span 
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                [ngClass]="getBadgeClass(result.type)"
              >
                {{ result.type }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div *ngIf="!loading && results.length === 0" class="empty-state text-center py-12">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <p class="empty-message mt-4 text-lg font-medium text-gray-900">
          {{ getEmptyMessage() }}
        </p>
        <p class="mt-2 text-sm text-gray-500">
          {{ query ? 'Try adjusting your search terms' : 'Enter a search query above to get started' }}
        </p>
      </div>

      <!-- Pagination -->
      <div *ngIf="!loading && results.length > 0 && total > pageSize" class="pagination mt-6 flex items-center justify-between">
        <div class="text-sm text-gray-700">
          Showing <strong>{{ (page - 1) * pageSize + 1 }}</strong> to <strong>{{ Math.min(page * pageSize, total) }}</strong> of <strong>{{ total }}</strong> results
        </div>
        <div class="flex gap-2">
          <button
            type="button"
            (click)="onPageChange(page - 1)"
            [disabled]="page === 1"
            class="pagination-prev px-3 py-1 border border-gray-300 rounded text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:bg-gray-100 disabled:text-gray-400 disabled:cursor-not-allowed"
            aria-label="Go to previous page"
          >
            Previous
          </button>
          <button
            type="button"
            (click)="onPageChange(page + 1)"
            [disabled]="page >= Math.ceil(total / pageSize)"
            class="pagination-next px-3 py-1 border border-gray-300 rounded text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:bg-gray-100 disabled:text-gray-400 disabled:cursor-not-allowed"
            aria-label="Go to next page"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  `,
  styles: [],
})
export class SearchResultsComponent {
  @Input() results: SearchResult[] = [];
  @Input() total = 0;
  @Input() page = 1;
  @Input() pageSize = 10;
  @Input() loading = false;
  @Input() query = '';

  @Output() resultClicked = new EventEmitter<SearchResult>();
  @Output() pageChanged = new EventEmitter<number>();

  readonly Math = Math;

  onResultClick(result: SearchResult): void {
    this.resultClicked.emit(result);
  }

  onPageChange(newPage: number): void {
    this.pageChanged.emit(newPage);
  }

  getIconClass(type: SearchEntityType): string {
    const classes = {
      student: 'bg-blue-100 text-blue-600',
      course: 'bg-green-100 text-green-600',
      assignment: 'bg-purple-100 text-purple-600',
      all: 'bg-gray-100 text-gray-600',
    };
    return classes[type] || classes.all;
  }

  getBadgeClass(type: SearchEntityType): string {
    const classes = {
      student: 'bg-blue-100 text-blue-800',
      course: 'bg-green-100 text-green-800',
      assignment: 'bg-purple-100 text-purple-800',
      all: 'bg-gray-100 text-gray-800',
    };
    return classes[type] || classes.all;
  }

  getMetadataArray(metadata: Record<string, any>): Array<{ key: string; value: string }> {
    if (!metadata) return [];
    return Object.entries(metadata).map(([key, value]) => ({
      key: this.formatKey(key),
      value: String(value),
    }));
  }

  getEmptyMessage(): string {
    if (!this.query) {
      return 'Start searching to see results';
    }
    return 'No results found';
  }

  private formatKey(key: string): string {
    return key.charAt(0).toUpperCase() + key.slice(1).replace(/([A-Z])/g, ' $1');
  }

  /**
   * Get result count text
   */
  getResultCountText(): string {
    if (this.total === 0) return 'No results';
    if (this.total === 1) return '1 result';
    return `${this.total} results`;
  }

  /**
   * Check if pagination is needed
   */
  shouldShowPagination(): boolean {
    return this.total > this.pageSize;
  }
}

