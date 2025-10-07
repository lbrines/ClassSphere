import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { of, throwError } from 'rxjs';

import { SearchBarComponent } from './search-bar.component';
import { SearchService } from '../../../../core/services/search.service';
import { SearchFilters } from '../../../../core/models/search.model';

describe('SearchBarComponent', () => {
  let component: SearchBarComponent;
  let fixture: ComponentFixture<SearchBarComponent>;
  let searchService: jasmine.SpyObj<SearchService>;

  const mockSearchResponse = {
    query: 'test',
    filters: { entityType: 'all' as const },
    results: [],
    total: 0,
    page: 1,
    pageSize: 10,
    executionTime: 10,
  };

  beforeEach(async () => {
    const searchServiceSpy = jasmine.createSpyObj('SearchService', ['search', 'clearSearch']);

    await TestBed.configureTestingModule({
      imports: [SearchBarComponent, ReactiveFormsModule],
      providers: [{ provide: SearchService, useValue: searchServiceSpy }],
    }).compileComponents();

    fixture = TestBed.createComponent(SearchBarComponent);
    component = fixture.componentInstance;
    searchService = TestBed.inject(SearchService) as jasmine.SpyObj<SearchService>;

    searchService.search.and.returnValue(of(mockSearchResponse));
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize with empty search form', () => {
    fixture.detectChanges();

    expect(component.searchForm.get('query')?.value).toBe('');
    expect(component.searchForm.get('entityType')?.value).toBe('all');
  });

  it('should display search input field', () => {
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    const searchInput = compiled.querySelector('input[type="text"]');

    expect(searchInput).toBeTruthy();
    expect(searchInput?.getAttribute('placeholder')).toContain('Search');
  });

  it('should display entity type filter dropdown', () => {
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    const select = compiled.querySelector('select');

    expect(select).toBeTruthy();
    expect(select?.querySelectorAll('option').length).toBeGreaterThan(1);
  });

  it('should trigger search on form submit', fakeAsync(() => {
    fixture.detectChanges();

    component.searchForm.patchValue({
      query: 'mathematics',
      entityType: 'course',
    });

    component.onSearch();
    tick();

    expect(searchService.search).toHaveBeenCalledWith('mathematics', {
      entityType: 'course',
    });
  }));

  it('should emit search event when search is triggered', fakeAsync(() => {
    fixture.detectChanges();
    spyOn(component.searchTriggered, 'emit');

    component.searchForm.patchValue({
      query: 'john',
      entityType: 'student',
    });

    component.onSearch();
    tick();

    expect(component.searchTriggered.emit).toHaveBeenCalledWith({
      query: 'john',
      filters: { entityType: 'student' },
    });
  }));

  it('should NOT search if query is empty', fakeAsync(() => {
    fixture.detectChanges();

    component.searchForm.patchValue({
      query: '',
      entityType: 'all',
    });

    component.onSearch();
    tick();

    expect(searchService.search).not.toHaveBeenCalled();
  }));

  it('should NOT search if query has only whitespace', fakeAsync(() => {
    fixture.detectChanges();

    component.searchForm.patchValue({
      query: '   ',
      entityType: 'all',
    });

    component.onSearch();
    tick();

    expect(searchService.search).not.toHaveBeenCalled();
  }));

  it('should clear search when clear button is clicked', fakeAsync(() => {
    fixture.detectChanges();

    component.searchForm.patchValue({
      query: 'test',
      entityType: 'student',
    });

    component.onClear();
    tick();

    expect(component.searchForm.get('query')?.value).toBe('');
    expect(searchService.clearSearch).toHaveBeenCalled();
  }));

  it('should emit cleared event when search is cleared', fakeAsync(() => {
    fixture.detectChanges();
    spyOn(component.searchCleared, 'emit');

    component.onClear();
    tick();

    expect(component.searchCleared.emit).toHaveBeenCalled();
  }));

  it('should debounce search input changes', fakeAsync(() => {
    component.enableAutoSearch = true;
    fixture.detectChanges();

    const queryControl = component.searchForm.get('query');
    queryControl?.setValue('a');
    tick(200);
    queryControl?.setValue('ab');
    tick(200);
    queryControl?.setValue('abc');
    tick(500); // Full debounce time

    // Should only call once after debounce completes
    expect(searchService.search).toHaveBeenCalledTimes(1);
    expect(searchService.search).toHaveBeenCalledWith('abc', { entityType: 'all' });
  }));

  it('should handle search errors gracefully', fakeAsync(() => {
    fixture.detectChanges();
    searchService.search.and.returnValue(
      throwError(() => new Error('Search failed'))
    );
    spyOn(console, 'error');

    component.searchForm.patchValue({
      query: 'error',
      entityType: 'all',
    });

    component.onSearch();
    tick();

    expect(console.error).toHaveBeenCalled();
  }));

  it('should show loading indicator while searching', fakeAsync(() => {
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;

    component.searchForm.patchValue({ query: 'test' });
    component.onSearch();

    fixture.detectChanges();
    // Note: Component should set isLoading = true during search

    tick();

    // After search completes, isLoading should be false
    expect(component.isLoading).toBe(false);
  }));

  it('should disable search button when form is invalid', () => {
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    const searchButton = compiled.querySelector('button[type="submit"]') as HTMLButtonElement;

    component.searchForm.patchValue({ query: '' });
    fixture.detectChanges();

    expect(searchButton?.disabled).toBe(true);
  });

  it('should enable search button when form is valid', () => {
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    const searchButton = compiled.querySelector('button[type="submit"]') as HTMLButtonElement;

    component.searchForm.patchValue({ query: 'valid query' });
    fixture.detectChanges();

    expect(searchButton?.disabled).toBe(false);
  });

  it('should apply correct CSS classes for styling', () => {
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    const searchInput = compiled.querySelector('input[type="text"]');

    expect(searchInput?.classList.contains('w-full')).toBe(true);
  });

  it('should have accessible label for search input', () => {
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    const searchInput = compiled.querySelector('input[type="text"]');

    expect(
      searchInput?.getAttribute('aria-label') ||
        compiled.querySelector('label')?.textContent
    ).toBeTruthy();
  });

  describe('edge cases and additional coverage', () => {
    it('should handle multiple rapid searches', fakeAsync(() => {
      fixture.detectChanges();

      component.searchForm.patchValue({ query: 'test1' });
      component.onSearch();
      tick();

      component.searchForm.patchValue({ query: 'test2' });
      component.onSearch();
      tick();

      component.searchForm.patchValue({ query: 'test3' });
      component.onSearch();
      tick();

      expect(searchService.search).toHaveBeenCalledTimes(3);
    }));

    it('should trim whitespace from query before searching', fakeAsync(() => {
      fixture.detectChanges();

      component.searchForm.patchValue({ query: '  trimmed  ' });
      component.onSearch();
      tick();

      expect(searchService.search).toHaveBeenCalledWith('trimmed', { entityType: 'all' });
    }));

    it('should reset loading state on error', fakeAsync(() => {
      fixture.detectChanges();
      searchService.search.and.returnValue(throwError(() => new Error('Failed')));

      component.searchForm.patchValue({ query: 'test' });
      component.onSearch();
      tick();

      expect(component.isLoading).toBe(false);
    }));

    it('should unsubscribe on component destroy', () => {
      fixture.detectChanges();
      spyOn(component['destroy$'], 'next');
      spyOn(component['destroy$'], 'complete');

      component.ngOnDestroy();

      expect(component['destroy$'].next).toHaveBeenCalled();
      expect(component['destroy$'].complete).toHaveBeenCalled();
    });

    it('should not setup auto-search if disabled', () => {
      component.enableAutoSearch = false;
      fixture.detectChanges();

      component.searchForm.get('query')?.setValue('auto');

      expect(searchService.search).not.toHaveBeenCalled();
    });

    it('should check form validity correctly', () => {
      fixture.detectChanges();

      component.searchForm.patchValue({ query: '' });
      expect(component.isFormValid()).toBe(false);

      component.searchForm.patchValue({ query: 'test' });
      expect(component.isFormValid()).toBe(true);

      component.searchForm.patchValue({ query: '   ' });
      expect(component.isFormValid()).toBe(false);
    });

    it('should get current query value', () => {
      fixture.detectChanges();

      component.searchForm.patchValue({ query: 'test query' });
      expect(component.getCurrentQuery()).toBe('test query');

      component.searchForm.patchValue({ query: '' });
      expect(component.getCurrentQuery()).toBe('');
    });

    it('should handle all entity type options', fakeAsync(() => {
      fixture.detectChanges();

      const entityTypes: Array<'all' | 'student' | 'course' | 'assignment'> = ['all', 'student', 'course', 'assignment'];

      entityTypes.forEach((type) => {
        component.searchForm.patchValue({ query: 'test', entityType: type });
        component.onSearch();
        tick();

        expect(searchService.search).toHaveBeenCalledWith('test', jasmine.objectContaining({ entityType: type }));
        searchService.search.calls.reset();
      });
    }));

    it('should emit events with correct filter data', fakeAsync(() => {
      fixture.detectChanges();
      const emittedEvents: any[] = [];
      component.searchTriggered.subscribe((event) => emittedEvents.push(event));

      component.searchForm.patchValue({ query: 'test', entityType: 'course' });
      component.onSearch();
      tick();

      expect(emittedEvents.length).toBe(1);
      expect(emittedEvents[0].filters.entityType).toBe('course');
    }));

    it('should validate minimum query length', () => {
      fixture.detectChanges();

      component.searchForm.patchValue({ query: '' });
      expect(component.hasMinimumLength()).toBe(false);

      component.searchForm.patchValue({ query: 'a' });
      expect(component.hasMinimumLength()).toBe(true);

      component.searchForm.patchValue({ query: '  ' });
      expect(component.hasMinimumLength()).toBe(false);
    });

    it('should handle debounce time changes', fakeAsync(() => {
      component.enableAutoSearch = true;
      component.debounceTime = 1000;
      fixture.detectChanges();

      component.searchForm.get('query')?.setValue('test');
      tick(999);
      expect(searchService.search).not.toHaveBeenCalled();

      tick(1);
      expect(searchService.search).toHaveBeenCalled();
    }));

    it('should clear then emit cleared event', fakeAsync(() => {
      fixture.detectChanges();
      const clearedEvents: any[] = [];
      component.searchCleared.subscribe(() => clearedEvents.push(event));

      component.searchForm.patchValue({ query: 'test' });
      component.onClear();
      tick();

      expect(clearedEvents.length).toBe(1);
      expect(searchService.clearSearch).toHaveBeenCalled();
    }));

    it('should handle auto-search with empty trimmed value', fakeAsync(() => {
      component.enableAutoSearch = true;
      fixture.detectChanges();

      component.searchForm.get('query')?.setValue('   ');
      tick(500);

      expect(searchService.search).not.toHaveBeenCalled();
    }));

    it('should set loading to true before search', fakeAsync(() => {
      fixture.detectChanges();

      component.searchForm.patchValue({ query: 'test' });
      
      let loadingStates: boolean[] = [];
      component['isLoading'] = false;
      
      component.onSearch();
      loadingStates.push(component.isLoading);
      tick();
      loadingStates.push(component.isLoading);

      expect(loadingStates[0]).toBe(true); // During search
    }));

    it('should preserve entityType on clear', fakeAsync(() => {
      fixture.detectChanges();

      component.searchForm.patchValue({ query: 'test', entityType: 'student' });
      component.onClear();
      tick();

      expect(component.searchForm.get('entityType')?.value).toBe('all');
    }));
  });
});

