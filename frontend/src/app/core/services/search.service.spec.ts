import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { firstValueFrom } from 'rxjs';

import { SearchService } from './search.service';
import { SearchResponse, SearchFilters } from '../models/search.model';
import { EnvironmentService } from './environment.service';

describe('SearchService', () => {
  let service: SearchService;
  let httpMock: HttpTestingController;

  const mockSearchResponse: SearchResponse = {
    query: 'math',
    filters: { entityType: 'all' },
    results: [
      {
        id: 'student-001',
        type: 'student',
        name: 'John Doe',
        description: 'Math student',
        metadata: { email: 'john@example.com', grade: 'A' },
        relevanceScore: 0.95,
      },
      {
        id: 'course-001',
        type: 'course',
        name: 'Mathematics 101',
        description: 'Introduction to Mathematics',
        metadata: { enrolled: 25 },
        relevanceScore: 0.87,
      },
    ],
    total: 2,
    page: 1,
    pageSize: 10,
    executionTime: 45,
  };

  const runtimeApiUrl = 'http://runtime-config.local/api/v1';

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        SearchService,
        {
          provide: EnvironmentService,
          useValue: {
            apiUrl: runtimeApiUrl,
          },
        },
      ],
    });

    service = TestBed.inject(SearchService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  describe('search()', () => {
    it('should be created', () => {
      expect(service).toBeTruthy();
    });

    it('should perform multi-entity search with query', async () => {
      const query = 'math';
      const filters: SearchFilters = { entityType: 'all' };

      const searchPromise = firstValueFrom(service.search(query, filters));

      const req = httpMock.expectOne((request) => {
        return (
          request.url === `${runtimeApiUrl}/search` &&
          request.params.get('q') === query &&
          request.params.get('entities') === 'students,teachers,courses,assignments,announcements'
        );
      });

      expect(req.request.method).toBe('GET');
      req.flush(mockSearchResponse);

      const response = await searchPromise;
      expect(response.results.length).toBe(2);
      expect(response.total).toBe(2);
      expect(response.query).toBe('math');
    });

    it('should search students only when entityType is student', async () => {
      const query = 'john';
      const filters: SearchFilters = { entityType: 'student' };

      const searchPromise = firstValueFrom(service.search(query, filters));

      const req = httpMock.expectOne((request) => {
        return (
          request.url === `${runtimeApiUrl}/search` &&
          request.params.get('entities') === 'students' &&
          request.params.get('q') === 'john'
        );
      });

      req.flush({
        ...mockSearchResponse,
        results: [mockSearchResponse.results[0]],
        total: 1,
      });

      const response = await searchPromise;
      expect(response.results.length).toBe(1);
      expect(response.results[0].type).toBe('student');
    });

    it('should apply course filter when provided', async () => {
      const query = 'assignment';
      const filters: SearchFilters = {
        entityType: 'assignment',
        course: 'course-123',
      };

      const searchPromise = firstValueFrom(service.search(query, filters));

      const req = httpMock.expectOne((request) => {
        return (
          request.url === `${runtimeApiUrl}/search` &&
          request.params.get('q') === query &&
          request.params.get('entities') === 'assignments' &&
          request.params.get('course') === 'course-123'
        );
      });

      req.flush(mockSearchResponse);
      await searchPromise;

      expect(req.request.params.get('course')).toBe('course-123');
    });

    it('should apply date range filters when provided', async () => {
      const query = 'test';
      const filters: SearchFilters = {
        entityType: 'assignment',
        dateFrom: '2025-01-01',
        dateTo: '2025-12-31',
      };

      const searchPromise = firstValueFrom(service.search(query, filters));

      const req = httpMock.expectOne((request) => {
        return (
          request.url === `${runtimeApiUrl}/search` &&
          request.params.get('dateFrom') === '2025-01-01' &&
          request.params.get('dateTo') === '2025-12-31'
        );
      });

      req.flush(mockSearchResponse);
      await searchPromise;

      expect(req.request.params.get('dateFrom')).toBe('2025-01-01');
    });

    it('should handle empty search results', async () => {
      const query = 'nonexistent';
      const filters: SearchFilters = { entityType: 'all' };

      const searchPromise = firstValueFrom(service.search(query, filters));

      const req = httpMock.expectOne(
        (request) => request.url === `${runtimeApiUrl}/search` && request.params.get('q') === query
      );

      req.flush({
        ...mockSearchResponse,
        results: [],
        total: 0,
      });

      const response = await searchPromise;
      expect(response.results.length).toBe(0);
      expect(response.total).toBe(0);
    });

    it('should handle HTTP errors gracefully', async () => {
      const query = 'error';
      const filters: SearchFilters = { entityType: 'all' };

      const searchPromise = firstValueFrom(service.search(query, filters));

      const req = httpMock.expectOne(
        (request) => request.url === `${runtimeApiUrl}/search` && request.params.get('q') === query
      );

      req.flush('Server error', { status: 500, statusText: 'Internal Server Error' });

      try {
        await searchPromise;
        fail('Should have thrown an error');
      } catch (error) {
        expect(error).toBeTruthy();
      }
    });
  });

  describe('searchState$', () => {
    it('should expose search state observable', (done) => {
      service.searchState$.subscribe((state) => {
        expect(state).toBeDefined();
        expect(state.loading).toBe(false);
        expect(state.results).toEqual([]);
        done();
      });
    });

    it('should update loading state during search', (done) => {
      const states: boolean[] = [];

      service.searchState$.subscribe((state) => {
        states.push(state.loading);

        if (states.length === 2) {
          expect(states[0]).toBe(false); // Initial state
          expect(states[1]).toBe(true); // Loading state
          done();
        }
      });

      service.search('test', { entityType: 'all' }).subscribe();

      const req = httpMock.expectOne((request) => request.url === `${runtimeApiUrl}/search`);
      req.flush(mockSearchResponse);
    });
  });

  describe('clearSearch()', () => {
    it('should clear search results and query', async () => {
      // First perform a search
      const searchPromise = firstValueFrom(service.search('math', { entityType: 'all' }));
      const req = httpMock.expectOne((request) => request.url === `${runtimeApiUrl}/search`);
      req.flush(mockSearchResponse);
      await searchPromise;

      // Then clear
      service.clearSearch();

      const state = await firstValueFrom(service.searchState$);
      expect(state.query).toBe('');
      expect(state.results).toEqual([]);
      expect(state.total).toBe(0);
    });
  });

  describe('getCurrentState()', () => {
    it('should return current state synchronously', () => {
      const state = service.getCurrentState();
      
      expect(state).toBeDefined();
      expect(state.query).toBe('');
      expect(state.results).toEqual([]);
    });
  });

  describe('error scenarios', () => {
    it('should handle network timeout errors', async () => {
      const searchPromise = firstValueFrom(service.search('test', { entityType: 'all' }));
      
      const req = httpMock.expectOne((request) => request.url === `${runtimeApiUrl}/search`);
      req.error(new ProgressEvent('timeout'));

      try {
        await searchPromise;
        fail('Should have thrown error');
      } catch (error) {
        expect(error).toBeTruthy();
      }
    });

    it('should set loading to false after error', async () => {
      const searchPromise = firstValueFrom(service.search('error', { entityType: 'all' }));
      
      const req = httpMock.expectOne((request) => request.url === `${runtimeApiUrl}/search`);
      req.flush('Error', { status: 500, statusText: 'Server Error' });

      try {
        await searchPromise;
      } catch (error) {
        // Expected
      }

      const state = service.getCurrentState();
      expect(state.loading).toBe(false);
    });

    it('should set error message on search failure', async () => {
      const searchPromise = firstValueFrom(service.search('fail', { entityType: 'all' }));
      
      const req = httpMock.expectOne((request) => request.url === `${runtimeApiUrl}/search`);
      req.flush('Error', { status: 500, statusText: 'Server Error' });

      try {
        await searchPromise;
      } catch (error) {
        // Expected
      }

      const state = service.getCurrentState();
      expect(state.error).toBeTruthy();
    });
  });

  describe('search history', () => {
    it('should return empty search history initially', () => {
      const history = service.getSearchHistory();

      expect(history).toEqual([]);
    });
  });

  describe('comprehensive branch coverage', () => {
    it('should handle all filter combinations', async () => {
      const filters = {
        entityType: 'assignment' as const,
        course: 'course-123',
        status: 'active' as const,
        dateFrom: '2025-01-01',
        dateTo: '2025-12-31',
      };

      const searchPromise = firstValueFrom(service.search('test', filters));

      const req = httpMock.expectOne((request) => {
        return (
          request.params.get('q') === 'test' &&
          request.params.get('entities') === 'assignments' &&
          request.params.get('course') === 'course-123' &&
          request.params.get('status') === 'active' &&
          request.params.get('dateFrom') === '2025-01-01' &&
          request.params.get('dateTo') === '2025-12-31'
        );
      });

      req.flush(mockSearchResponse);
      await searchPromise;

      expect(req.request.params.keys().length).toBeGreaterThan(2);
    });

    it('should handle search with only required filters', async () => {
      const filters = { entityType: 'all' as const };

      const searchPromise = firstValueFrom(service.search('minimal', filters));

      const req = httpMock.expectOne((request) => {
        return (
          request.params.get('q') === 'minimal' &&
          request.params.get('entities') === 'students,teachers,courses,assignments,announcements' &&
          !request.params.has('course') &&
          !request.params.has('status')
        );
      });

      req.flush(mockSearchResponse);
      await searchPromise;

      expect(req.request.params.keys().length).toBe(4);
    });

    it('should trim query whitespace before sending', async () => {
      const searchPromise = firstValueFrom(service.search('  spaced  ', { entityType: 'all' }));

      const req = httpMock.expectOne((request) => request.params.get('q') === 'spaced');

      req.flush(mockSearchResponse);
      await searchPromise;

      expect(req.request.params.get('q')).toBe('spaced');
    });

    it('should ensure loading is false in finalize block on success', async () => {
      const searchPromise = firstValueFrom(service.search('test', { entityType: 'all' }));

      const req = httpMock.expectOne((request) => request.url === `${runtimeApiUrl}/search`);
      req.flush(mockSearchResponse);
      
      await searchPromise;

      const state = service.getCurrentState();
      expect(state.loading).toBe(false);
    });

    it('should ensure loading is false in finalize block on error', async () => {
      const searchPromise = firstValueFrom(service.search('test', { entityType: 'all' }));

      const req = httpMock.expectOne((request) => request.url === `${runtimeApiUrl}/search`);
      req.flush('Error', { status: 500, statusText: 'Error' });

      try {
        await searchPromise;
      } catch (error) {
        // Expected
      }

      const state = service.getCurrentState();
      expect(state.loading).toBe(false);
    });

    it('should update state with results on successful search', async () => {
      const searchPromise = firstValueFrom(service.search('test', { entityType: 'all' }));

      const req = httpMock.expectOne((request) => request.url === `${runtimeApiUrl}/search`);
      req.flush(mockSearchResponse);
      
      await searchPromise;

      const state = service.getCurrentState();
      expect(state.results).toEqual(mockSearchResponse.results);
      expect(state.total).toBe(mockSearchResponse.total);
    });

    it('should clear results on error', async () => {
      const searchPromise = firstValueFrom(service.search('test', { entityType: 'all' }));

      const req = httpMock.expectOne((request) => request.url === `${runtimeApiUrl}/search`);
      req.flush('Error', { status: 500, statusText: 'Error' });

      try {
        await searchPromise;
      } catch (error) {
        // Expected
      }

      const state = service.getCurrentState();
      expect(state.results).toEqual([]);
      expect(state.total).toBe(0);
    });
  });
});
