/**
 * Search Models for Phase 3 - Advanced Search Functionality
 * Supports multi-entity search (students, courses, assignments)
 */

export type SearchEntityType = 'student' | 'course' | 'assignment' | 'all';

export interface SearchFilters {
  entityType: SearchEntityType;
  course?: string;
  status?: 'active' | 'inactive' | 'archived';
  dateFrom?: string;
  dateTo?: string;
}

export interface SearchResult {
  id: string;
  type: SearchEntityType;
  name: string;
  description?: string;
  metadata: Record<string, any>;
  relevanceScore: number;
}

export interface SearchResponse {
  query: string;
  filters: SearchFilters;
  results: SearchResult[];
  total: number;
  page: number;
  pageSize: number;
  executionTime: number; // milliseconds
}

export interface SearchState {
  loading: boolean;
  query: string;
  filters: SearchFilters;
  results: SearchResult[];
  total: number;
  error: string | null;
}

