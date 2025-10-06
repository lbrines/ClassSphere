import { Component, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

interface SearchResult {
  type: string;
  id: string;
  title: string;
  description: string;
  score: number;
  metadata: any;
}

interface SearchFilters {
  course: string;
  grade: string;
  date_from: string;
  date_to: string;
  min_points: number;
  max_points: number;
  state: string;
}

interface SearchRequest {
  query: string;
  filters: SearchFilters;
  limit: number;
  offset: number;
}

interface SearchResponse {
  results: SearchResult[];
  total: number;
  query: string;
  filters: SearchFilters;
  search_time: string;
}

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="min-h-screen bg-gray-50">
      <!-- Header -->
      <header class="bg-white shadow">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between items-center py-6">
            <div class="flex items-center">
              <h1 class="text-3xl font-bold text-gray-900">ClassSphere Search</h1>
            </div>
            <div class="flex items-center space-x-4">
              <button
                (click)="goToDashboard()"
                class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Dashboard
              </button>
            </div>
          </div>
        </div>
      </header>

      <!-- Main Content -->
      <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div class="px-4 py-6 sm:px-0">
          <!-- Search Form -->
          <div class="bg-white shadow rounded-lg mb-6">
            <div class="px-4 py-5 sm:p-6">
              <h2 class="text-lg font-medium text-gray-900 mb-4">Advanced Search</h2>
              
              <!-- Search Input -->
              <div class="mb-4">
                <label for="search-query" class="block text-sm font-medium text-gray-700 mb-2">
                  Search Query
                </label>
                <div class="relative">
                  <input
                    id="search-query"
                    type="text"
                    [(ngModel)]="searchQuery"
                    (input)="onSearchInput()"
                    placeholder="Search students, courses, assignments..."
                    class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                  />
                  <div class="absolute inset-y-0 right-0 pr-3 flex items-center">
                    @if (isSearching()) {
                      <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-indigo-600"></div>
                    } @else {
                      <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                      </svg>
                    }
                  </div>
                </div>
              </div>

              <!-- Search Suggestions -->
              @if (suggestions().length > 0 && showSuggestions()) {
                <div class="mb-4">
                  <div class="bg-white border border-gray-300 rounded-md shadow-lg max-h-48 overflow-y-auto">
                    @for (suggestion of suggestions(); track suggestion) {
                      <button
                        (click)="selectSuggestion(suggestion)"
                        class="w-full px-4 py-2 text-left hover:bg-gray-50 border-b border-gray-100 last:border-b-0"
                      >
                        {{ suggestion }}
                      </button>
                    }
                  </div>
                </div>
              }

              <!-- Filters -->
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div>
                  <label for="course-filter" class="block text-sm font-medium text-gray-700 mb-1">
                    Course
                  </label>
                  <input
                    id="course-filter"
                    type="text"
                    [(ngModel)]="filters.course"
                    placeholder="Filter by course"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </div>
                
                <div>
                  <label for="state-filter" class="block text-sm font-medium text-gray-700 mb-1">
                    State
                  </label>
                  <select
                    id="state-filter"
                    [(ngModel)]="filters.state"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                  >
                    <option value="">All States</option>
                    <option value="ACTIVE">Active</option>
                    <option value="ARCHIVED">Archived</option>
                    <option value="PUBLISHED">Published</option>
                    <option value="DRAFT">Draft</option>
                  </select>
                </div>

                <div>
                  <label for="grade-filter" class="block text-sm font-medium text-gray-700 mb-1">
                    Grade
                  </label>
                  <input
                    id="grade-filter"
                    type="text"
                    [(ngModel)]="filters.grade"
                    placeholder="Filter by grade"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </div>
              </div>

              <!-- Points Range -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                  <label for="min-points" class="block text-sm font-medium text-gray-700 mb-1">
                    Min Points
                  </label>
                  <input
                    id="min-points"
                    type="number"
                    [(ngModel)]="filters.min_points"
                    placeholder="Minimum points"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </div>
                
                <div>
                  <label for="max-points" class="block text-sm font-medium text-gray-700 mb-1">
                    Max Points
                  </label>
                  <input
                    id="max-points"
                    type="number"
                    [(ngModel)]="filters.max_points"
                    placeholder="Maximum points"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </div>
              </div>

              <!-- Search Buttons -->
              <div class="flex space-x-4">
                <button
                  (click)="performSearch()"
                  [disabled]="isSearching()"
                  class="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2 rounded-md text-sm font-medium disabled:opacity-50"
                >
                  @if (isSearching()) {
                    Searching...
                  } @else {
                    Search
                  }
                </button>
                
                <button
                  (click)="clearFilters()"
                  class="bg-gray-300 hover:bg-gray-400 text-gray-700 px-6 py-2 rounded-md text-sm font-medium"
                >
                  Clear Filters
                </button>
              </div>
            </div>
          </div>

          <!-- Search Results -->
          @if (searchResults().length > 0) {
            <div class="bg-white shadow rounded-lg">
              <div class="px-4 py-5 sm:p-6">
                <div class="flex justify-between items-center mb-4">
                  <h3 class="text-lg font-medium text-gray-900">
                    Search Results ({{ totalResults() }})
                  </h3>
                  <span class="text-sm text-gray-500">
                    Search time: {{ searchTime() }}
                  </span>
                </div>

                <div class="space-y-4">
                  @for (result of searchResults(); track result.id) {
                    <div class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                      <div class="flex items-start justify-between">
                        <div class="flex-1">
                          <div class="flex items-center space-x-2 mb-2">
                            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                                  [class]="getTypeBadgeClass(result.type)">
                              {{ result.type | titlecase }}
                            </span>
                            <span class="text-sm text-gray-500">
                              Score: {{ (result.score * 100).toFixed(1) }}%
                            </span>
                          </div>
                          
                          <h4 class="text-lg font-medium text-gray-900 mb-1">
                            {{ result.title }}
                          </h4>
                          
                          <p class="text-gray-600 mb-2">
                            {{ result.description }}
                          </p>

                          <!-- Metadata -->
                          @if (result.metadata && Object.keys(result.metadata).length > 0) {
                            <div class="flex flex-wrap gap-2">
                              @for (item of getMetadataItems(result.metadata); track item.key) {
                                <span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-100 text-gray-800">
                                  {{ item.key }}: {{ item.value }}
                                </span>
                              }
                            </div>
                          }
                        </div>
                        
                        <div class="ml-4">
                          <button
                            (click)="viewDetails(result)"
                            class="text-indigo-600 hover:text-indigo-500 text-sm font-medium"
                          >
                            View Details
                          </button>
                        </div>
                      </div>
                    </div>
                  }
                </div>

                <!-- Pagination -->
                @if (totalResults() > currentLimit()) {
                  <div class="mt-6 flex justify-between items-center">
                    <div class="text-sm text-gray-700">
                      Showing {{ currentOffset() + 1 }} to {{ Math.min(currentOffset() + currentLimit(), totalResults()) }} of {{ totalResults() }} results
                    </div>
                    
                    <div class="flex space-x-2">
                      <button
                        (click)="previousPage()"
                        [disabled]="currentOffset() === 0"
                        class="px-3 py-1 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
                      >
                        Previous
                      </button>
                      
                      <button
                        (click)="nextPage()"
                        [disabled]="currentOffset() + currentLimit() >= totalResults()"
                        class="px-3 py-1 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
                      >
                        Next
                      </button>
                    </div>
                  </div>
                }
              </div>
            </div>
          } @else if (hasSearched() && !isSearching()) {
            <div class="bg-white shadow rounded-lg">
              <div class="px-4 py-5 sm:p-6 text-center">
                <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>
                <h3 class="mt-2 text-sm font-medium text-gray-900">No results found</h3>
                <p class="mt-1 text-sm text-gray-500">
                  Try adjusting your search criteria or filters.
                </p>
              </div>
            </div>
          }
        </div>
      </main>
    </div>
  `,
  styles: []
})
export class SearchComponent implements OnInit {
  searchQuery = signal('');
  searchResults = signal<SearchResult[]>([]);
  suggestions = signal<string[]>([]);
  showSuggestions = signal(false);
  isSearching = signal(false);
  hasSearched = signal(false);
  totalResults = signal(0);
  searchTime = signal('');
  
  filters: SearchFilters = {
    course: '',
    grade: '',
    date_from: '',
    date_to: '',
    min_points: 0,
    max_points: 0,
    state: ''
  };

  currentOffset = signal(0);
  currentLimit = signal(10);

  // Computed properties
  Math = Math;

  constructor(
    private http: HttpClient,
    private router: Router
  ) {}

  ngOnInit() {
    // Initialize component
  }

  onSearchInput() {
    const query = this.searchQuery();
    if (query.length >= 2) {
      this.getSuggestions(query);
      this.showSuggestions.set(true);
    } else {
      this.suggestions.set([]);
      this.showSuggestions.set(false);
    }
  }

  selectSuggestion(suggestion: string) {
    this.searchQuery.set(suggestion);
    this.showSuggestions.set(false);
    this.performSearch();
  }

  performSearch() {
    if (!this.searchQuery().trim()) {
      return;
    }

    this.isSearching.set(true);
    this.hasSearched.set(true);
    this.showSuggestions.set(false);

    const request: SearchRequest = {
      query: this.searchQuery(),
      filters: this.filters,
      limit: this.currentLimit(),
      offset: this.currentOffset()
    };

    this.http.post<SearchResponse>('/api/search', request).subscribe({
      next: (response) => {
        this.searchResults.set(response.results);
        this.totalResults.set(response.total);
        this.searchTime.set(response.search_time);
        this.isSearching.set(false);
      },
      error: (error) => {
        console.error('Search error:', error);
        this.isSearching.set(false);
        // Handle error appropriately
      }
    });
  }

  getSuggestions(query: string) {
    this.http.get<{suggestions: string[]}>(`/api/search/suggestions?q=${encodeURIComponent(query)}`).subscribe({
      next: (response) => {
        this.suggestions.set(response.suggestions);
      },
      error: (error) => {
        console.error('Suggestions error:', error);
      }
    });
  }

  clearFilters() {
    this.filters = {
      course: '',
      grade: '',
      date_from: '',
      date_to: '',
      min_points: 0,
      max_points: 0,
      state: ''
    };
    this.currentOffset.set(0);
    this.performSearch();
  }

  viewDetails(result: SearchResult) {
    // Navigate to details page based on result type
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

  previousPage() {
    const newOffset = Math.max(0, this.currentOffset() - this.currentLimit());
    this.currentOffset.set(newOffset);
    this.performSearch();
  }

  nextPage() {
    const newOffset = this.currentOffset() + this.currentLimit();
    this.currentOffset.set(newOffset);
    this.performSearch();
  }

  goToDashboard() {
    this.router.navigate(['/dashboard']);
  }

  getTypeBadgeClass(type: string): string {
    switch (type) {
      case 'student':
        return 'bg-blue-100 text-blue-800';
      case 'course':
        return 'bg-green-100 text-green-800';
      case 'assignment':
        return 'bg-purple-100 text-purple-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  }

  getMetadataItems(metadata: any): {key: string, value: string}[] {
    return Object.entries(metadata).map(([key, value]) => ({
      key: key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
      value: String(value)
    }));
  }
}
