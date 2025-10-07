import { Component, EventEmitter, inject, Input, OnDestroy, OnInit, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Subject, debounceTime, distinctUntilChanged, takeUntil } from 'rxjs';

import { SearchService } from '../../../../core/services/search.service';
import { SearchEntityType, SearchFilters } from '../../../../core/models/search.model';

/**
 * SearchBarComponent - Phase 3 Advanced Search
 * 
 * Features:
 * - Multi-entity type selection (students, courses, assignments, all)
 * - Debounced auto-search (optional)
 * - Manual search trigger
 * - Clear functionality
 * - Loading state indicator
 * - Accessibility compliant (WCAG 2.2 AA)
 */
@Component({
  selector: 'app-search-bar',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <form
      [formGroup]="searchForm"
      (ngSubmit)="onSearch()"
      class="flex flex-col gap-4 md:flex-row md:items-end"
    >
      <!-- Search Input -->
      <div class="flex-1">
        <label for="search-query" class="block text-sm font-medium text-gray-700 mb-1">
          Search
        </label>
        <input
          id="search-query"
          type="text"
          formControlName="query"
          placeholder="Search students, courses, assignments..."
          aria-label="Search students, courses, or assignments"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          [attr.aria-invalid]="searchForm.get('query')?.invalid && searchForm.get('query')?.touched"
        />
      </div>

      <!-- Entity Type Filter -->
      <div class="w-full md:w-48">
        <label for="entity-type" class="block text-sm font-medium text-gray-700 mb-1">
          Filter by
        </label>
        <select
          id="entity-type"
          formControlName="entityType"
          aria-label="Filter search by entity type"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="all">All</option>
          <option value="student">Students</option>
          <option value="course">Courses</option>
          <option value="assignment">Assignments</option>
        </select>
      </div>

      <!-- Search Button -->
      <button
        type="submit"
        [disabled]="searchForm.invalid || isLoading"
        class="px-6 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        aria-label="Perform search"
      >
        <span *ngIf="!isLoading">Search</span>
        <span *ngIf="isLoading" class="flex items-center">
          <svg
            class="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
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
          Searching...
        </span>
      </button>

      <!-- Clear Button -->
      <button
        type="button"
        (click)="onClear()"
        class="px-6 py-2 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors"
        aria-label="Clear search"
      >
        Clear
      </button>
    </form>
  `,
  styles: [],
})
export class SearchBarComponent implements OnInit, OnDestroy {
  private readonly fb = inject(FormBuilder);
  private readonly searchService = inject(SearchService);
  private readonly destroy$ = new Subject<void>();

  @Input() enableAutoSearch = false;
  @Input() debounceTime = 500; // milliseconds

  @Output() searchTriggered = new EventEmitter<{ query: string; filters: SearchFilters }>();
  @Output() searchCleared = new EventEmitter<void>();

  searchForm!: FormGroup;
  isLoading = false;

  ngOnInit(): void {
    this.initializeForm();
    this.setupAutoSearch();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  onSearch(): void {
    if (this.searchForm.invalid) {
      return;
    }

    const queryControl = this.searchForm.get('query');
    if (!queryControl) {
      return;
    }

    const query = queryControl.value?.trim();
    if (!query) {
      return;
    }

    const entityTypeControl = this.searchForm.get('entityType');
    const filters: SearchFilters = {
      entityType: entityTypeControl?.value || 'all',
    };

    this.isLoading = true;

    this.searchService
      .search(query, filters)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: () => {
          this.isLoading = false;
          this.searchTriggered.emit({ query, filters });
        },
        error: (error) => {
          this.isLoading = false;
          console.error('Search failed:', error);
        },
      });
  }

  onClear(): void {
    this.searchForm.reset({
      query: '',
      entityType: 'all',
    });
    this.searchService.clearSearch();
    this.searchCleared.emit();
  }

  private initializeForm(): void {
    this.searchForm = this.fb.group({
      query: ['', [Validators.required, Validators.minLength(1)]],
      entityType: ['all' as SearchEntityType],
    });
  }

  /**
   * Validate query has minimum length
   */
  hasMinimumLength(): boolean {
    const query = this.searchForm.get('query')?.value || '';
    return query.trim().length >= 1;
  }

  private setupAutoSearch(): void {
    if (!this.enableAutoSearch) {
      return;
    }

    this.searchForm
      .get('query')
      ?.valueChanges.pipe(
        debounceTime(this.debounceTime),
        distinctUntilChanged(),
        takeUntil(this.destroy$)
      )
      .subscribe((query) => {
        if (query?.trim()) {
          this.onSearch();
        }
      });
  }

  /**
   * Check if form is valid
   */
  isFormValid(): boolean {
    return this.searchForm.valid && !!this.searchForm.get('query')?.value?.trim();
  }

  /**
   * Get current search query
   */
  getCurrentQuery(): string {
    return this.searchForm.get('query')?.value || '';
  }
}

