import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { of, throwError } from 'rxjs';

import { SearchPageComponent } from './search-page.component';
import { SearchService } from '../../../../core/services/search.service';
import { SearchResult } from '../../../../core/models/search.model';

describe('SearchPageComponent', () => {
  let component: SearchPageComponent;
  let fixture: ComponentFixture<SearchPageComponent>;
  let searchService: jasmine.SpyObj<SearchService>;
  let router: jasmine.SpyObj<Router>;

  beforeEach(async () => {
    const searchServiceSpy = jasmine.createSpyObj('SearchService', ['search', 'clearSearch'], {
      searchState$: of({
        loading: false,
        query: '',
        filters: { entityType: 'all' },
        results: [],
        total: 0,
        error: null,
      }),
    });

    const routerSpy = jasmine.createSpyObj('Router', ['navigate']);

    await TestBed.configureTestingModule({
      imports: [SearchPageComponent],
      providers: [
        { provide: SearchService, useValue: searchServiceSpy },
        { provide: Router, useValue: routerSpy },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(SearchPageComponent);
    component = fixture.componentInstance;
    searchService = TestBed.inject(SearchService) as jasmine.SpyObj<SearchService>;
    router = TestBed.inject(Router) as jasmine.SpyObj<Router>;

    searchService.search.and.returnValue(
      of({
        query: 'test',
        filters: { entityType: 'all' },
        results: [],
        total: 0,
        page: 1,
        pageSize: 10,
        executionTime: 10,
      })
    );
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should display search bar and results components', () => {
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;

    const searchBar = compiled.querySelector('app-search-bar');
    const searchResults = compiled.querySelector('app-search-results');

    expect(searchBar).toBeTruthy();
    expect(searchResults).toBeTruthy();
  });

  it('should reset pagination when new search is triggered', () => {
    component.currentPage = 5;

    component.onSearchTriggered({
      query: 'test',
      filters: { entityType: 'all' },
    });

    expect(component.currentPage).toBe(1);
  });

  it('should navigate to student detail when student result is clicked', () => {
    const studentResult: SearchResult = {
      id: 'student-001',
      type: 'student',
      name: 'John Doe',
      description: 'Test student',
      metadata: {},
      relevanceScore: 0.9,
    };

    component.onResultClicked(studentResult);

    expect(router.navigate).toHaveBeenCalledWith(['/students', 'student-001']);
  });

  it('should navigate to course detail when course result is clicked', () => {
    const courseResult: SearchResult = {
      id: 'course-001',
      type: 'course',
      name: 'Math 101',
      description: 'Test course',
      metadata: {},
      relevanceScore: 0.9,
    };

    component.onResultClicked(courseResult);

    expect(router.navigate).toHaveBeenCalledWith(['/courses', 'course-001']);
  });

  it('should clear search state when search is cleared', () => {
    component.searchState.query = 'test';
    component.searchState.results = [
      {
        id: '1',
        type: 'student',
        name: 'Test',
        metadata: {},
        relevanceScore: 0.9,
      },
    ];

    component.onSearchCleared();

    expect(component.searchState.query).toBe('');
    expect(component.searchState.results).toEqual([]);
    expect(component.currentPage).toBe(1);
  });

  it('should update page and trigger new search when page is changed', () => {
    component.searchState.query = 'test';

    component.onPageChanged(2);

    expect(component.currentPage).toBe(2);
    expect(searchService.search).toHaveBeenCalled();
  });

  describe('additional coverage', () => {
    it('should handle assignment result click navigation', () => {
      const assignmentResult = {
        id: 'assignment-001',
        type: 'assignment' as const,
        name: 'Math Quiz',
        metadata: {},
        relevanceScore: 0.9,
      };

      component.onResultClicked(assignmentResult);

      expect(router.navigate).toHaveBeenCalledWith(['/assignments', 'assignment-001']);
    });

    it('should not search when page changed without query', () => {
      component.searchState.query = '';

      searchService.search.calls.reset();
      component.onPageChanged(2);

      expect(searchService.search).not.toHaveBeenCalled();
    });

    it('should subscribe to search state on init', () => {
      spyOn(searchService.searchState$, 'pipe').and.callThrough();

      component.ngOnInit();

      expect(searchService.searchState$.pipe).toHaveBeenCalled();
    });

    it('should unsubscribe on destroy', () => {
      fixture.detectChanges();
      spyOn(component['destroy$'], 'next');
      spyOn(component['destroy$'], 'complete');

      component.ngOnDestroy();

      expect(component['destroy$'].next).toHaveBeenCalled();
      expect(component['destroy$'].complete).toHaveBeenCalled();
    });

    it('should log search events to console', () => {
      spyOn(console, 'log');

      component.onSearchTriggered({ query: 'test', filters: { entityType: 'all' } });

      expect(console.log).toHaveBeenCalledWith('Search triggered:', jasmine.any(Object));
    });

    it('should log result clicks to console', () => {
      spyOn(console, 'log');

      const result = {
        id: '1',
        type: 'student' as const,
        name: 'Test',
        metadata: {},
        relevanceScore: 0.9,
      };

      component.onResultClicked(result);

      expect(console.log).toHaveBeenCalledWith('Result clicked:', result);
    });

    it('should not change page to invalid page number', () => {
      component.currentPage = 2;

      component.onPageChanged(0);

      expect(component.currentPage).toBe(2);
    });

    it('should handle page change search error', () => {
      component.searchState.query = 'test';
      searchService.search.and.returnValue(throwError(() => new Error('Page error')));
      spyOn(console, 'error');

      component.onPageChanged(2);

      expect(console.error).toHaveBeenCalled();
    });
  });
});

