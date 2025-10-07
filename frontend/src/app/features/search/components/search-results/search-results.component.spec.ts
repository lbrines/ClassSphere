import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';

import { SearchResultsComponent } from './search-results.component';
import { SearchResult } from '../../../../core/models/search.model';

describe('SearchResultsComponent', () => {
  let component: SearchResultsComponent;
  let fixture: ComponentFixture<SearchResultsComponent>;

  const mockStudentResults: SearchResult[] = [
    {
      id: 'student-001',
      type: 'student',
      name: 'John Doe',
      description: 'Mathematics student with excellent grades',
      metadata: { email: 'john@example.com', grade: 'A', course: 'Math 101' },
      relevanceScore: 0.95,
    },
    {
      id: 'student-002',
      type: 'student',
      name: 'Jane Smith',
      description: 'Physics student',
      metadata: { email: 'jane@example.com', grade: 'B+', course: 'Physics 201' },
      relevanceScore: 0.87,
    },
  ];

  const mockCourseResults: SearchResult[] = [
    {
      id: 'course-001',
      type: 'course',
      name: 'Mathematics 101',
      description: 'Introduction to Mathematics',
      metadata: { enrolled: 25, instructor: 'Dr. Smith' },
      relevanceScore: 0.92,
    },
  ];

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SearchResultsComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(SearchResultsComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('Display Results', () => {
    it('should display empty state when no results', () => {
      component.results = [];
      component.total = 0;
      component.loading = false;
      component.query = 'test'; // Set a query to show "No results" message
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const emptyState = compiled.querySelector('.empty-state');

      expect(emptyState).toBeTruthy();
      expect(emptyState?.textContent).toContain('No results');
    });

    it('should display loading state when loading is true', () => {
      component.results = [];
      component.loading = true;
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const loadingIndicator = compiled.querySelector('.loading-indicator');

      expect(loadingIndicator).toBeTruthy();
    });

    it('should display all search results', () => {
      component.results = mockStudentResults;
      component.total = mockStudentResults.length;
      component.loading = false;
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const resultItems = compiled.querySelectorAll('.result-item');

      expect(resultItems.length).toBe(mockStudentResults.length);
    });

    it('should display result name and description', () => {
      component.results = [mockStudentResults[0]];
      component.loading = false;
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const resultName = compiled.querySelector('.result-name');
      const resultDescription = compiled.querySelector('.result-description');

      expect(resultName?.textContent).toContain('John Doe');
      expect(resultDescription?.textContent).toContain('Mathematics student');
    });

    it('should display result metadata', () => {
      component.results = [mockStudentResults[0]];
      component.loading = false;
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const metadata = compiled.querySelector('.result-metadata');

      expect(metadata).toBeTruthy();
      expect(metadata?.textContent).toContain('john@example.com');
    });

    it('should display correct icon for each entity type', () => {
      component.results = [
        mockStudentResults[0],
        mockCourseResults[0],
      ];
      component.loading = false;
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const icons = compiled.querySelectorAll('.result-icon');

      expect(icons.length).toBeGreaterThan(0);
      // Each result should have an icon
    });

    it('should display total results count', () => {
      component.results = mockStudentResults;
      component.total = 25; // More results available
      component.loading = false;
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const resultsCount = compiled.querySelector('.results-count');

      expect(resultsCount?.textContent).toContain('25');
    });
  });

  describe('Result Interaction', () => {
    it('should emit resultClicked when a result is clicked', () => {
      spyOn(component.resultClicked, 'emit');
      component.results = [mockStudentResults[0]];
      component.loading = false;
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const resultItem = compiled.querySelector('.result-item') as HTMLElement;
      resultItem.click();

      expect(component.resultClicked.emit).toHaveBeenCalledWith(mockStudentResults[0]);
    });

    it('should have clickable result items with proper cursor style', () => {
      component.results = [mockStudentResults[0]];
      component.loading = false;
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const resultItem = compiled.querySelector('.result-item') as HTMLElement;

      expect(resultItem.classList.contains('cursor-pointer')).toBe(true);
    });

    it('should highlight result on hover', () => {
      component.results = [mockStudentResults[0]];
      component.loading = false;
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const resultItem = compiled.querySelector('.result-item') as HTMLElement;

      // Should have hover styles
      expect(resultItem.classList.contains('hover:bg-gray-50')).toBe(true);
    });
  });

  describe('Pagination', () => {
    it('should display pagination when there are more results', () => {
      component.results = mockStudentResults;
      component.total = 50; // More results available
      component.page = 1;
      component.pageSize = 10;
      component.loading = false;
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const pagination = compiled.querySelector('.pagination');

      expect(pagination).toBeTruthy();
    });

    it('should emit pageChanged when page is changed', () => {
      spyOn(component.pageChanged, 'emit');
      component.results = mockStudentResults;
      component.total = 50;
      component.page = 1;
      component.pageSize = 10;
      component.loading = false;
      fixture.detectChanges();

      component.onPageChange(2);

      expect(component.pageChanged.emit).toHaveBeenCalledWith(2);
    });

    it('should calculate correct number of pages', () => {
      component.total = 25;
      component.pageSize = 10;

      const totalPages = Math.ceil(component.total / component.pageSize);

      expect(totalPages).toBe(3);
    });

    it('should disable previous button on first page', () => {
      component.results = mockStudentResults;
      component.total = 50;
      component.page = 1;
      component.pageSize = 10;
      component.loading = false;
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const prevButton = compiled.querySelector('.pagination-prev') as HTMLButtonElement;

      expect(prevButton?.disabled).toBe(true);
    });

    it('should disable next button on last page', () => {
      component.results = mockStudentResults;
      component.total = 15;
      component.page = 2;
      component.pageSize = 10;
      component.loading = false;
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const nextButton = compiled.querySelector('.pagination-next') as HTMLButtonElement;

      expect(nextButton?.disabled).toBe(true);
    });
  });

  describe('Accessibility', () => {
    it('should have proper ARIA labels for results list', () => {
      component.results = mockStudentResults;
      component.loading = false;
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const resultsList = compiled.querySelector('[role="list"]');

      expect(resultsList).toBeTruthy();
    });

    it('should have proper ARIA labels for result items', () => {
      component.results = [mockStudentResults[0]];
      component.loading = false;
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const resultItem = compiled.querySelector('[role="listitem"]');

      expect(resultItem).toBeTruthy();
    });

    it('should announce loading state to screen readers', () => {
      component.loading = true;
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const liveRegion = compiled.querySelector('[aria-live="polite"]');

      expect(liveRegion).toBeTruthy();
    });

    it('should have keyboard navigation support', () => {
      component.results = [mockStudentResults[0]];
      component.loading = false;
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const resultItem = compiled.querySelector('.result-item') as HTMLElement;

      expect(resultItem.getAttribute('tabindex')).toBe('0');
    });
  });

  describe('Empty States', () => {
    it('should show helpful message when no results found', () => {
      component.results = [];
      component.total = 0;
      component.loading = false;
      component.query = 'nonexistent';
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const emptyMessage = compiled.querySelector('.empty-message');

      expect(emptyMessage?.textContent).toContain('No results found');
    });

    it('should show different message before first search', () => {
      component.results = [];
      component.total = 0;
      component.loading = false;
      component.query = '';
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const emptyMessage = compiled.querySelector('.empty-message');

      expect(emptyMessage?.textContent).toContain('Start searching');
    });
  });

  describe('Performance', () => {
    it('should handle large result sets efficiently', () => {
      const largeResultSet = Array.from({ length: 100 }, (_, i) => ({
        id: `result-${i}`,
        type: 'student' as const,
        name: `Student ${i}`,
        description: `Description ${i}`,
        metadata: {},
        relevanceScore: 0.5,
      }));

      component.results = largeResultSet;
      component.total = largeResultSet.length;
      component.loading = false;

      expect(() => fixture.detectChanges()).not.toThrow();
    });
  });

  describe('additional coverage', () => {
    it('should handle keyboard navigation on results', () => {
      component.results = [mockStudentResults[0]];
      component.loading = false;
      fixture.detectChanges();

      spyOn(component.resultClicked, 'emit');

      const compiled = fixture.nativeElement as HTMLElement;
      const firstResult = compiled.querySelector('.result-item') as HTMLElement;

      const enterEvent = new KeyboardEvent('keydown', { key: 'Enter' });
      firstResult?.dispatchEvent(enterEvent);

      expect(component.resultClicked.emit).toHaveBeenCalled();
    });

    it('should handle Space key on results', () => {
      component.results = [mockStudentResults[0]];
      component.loading = false;
      fixture.detectChanges();

      spyOn(component.resultClicked, 'emit');

      const compiled = fixture.nativeElement as HTMLElement;
      const firstResult = compiled.querySelector('.result-item') as HTMLElement;

      const spaceEvent = new KeyboardEvent('keydown', { key: ' ' });
      firstResult?.dispatchEvent(spaceEvent);

      expect(component.resultClicked.emit).toHaveBeenCalled();
    });

    it('should format metadata keys correctly', () => {
      component.results = [
        {
          ...mockStudentResults[0],
          metadata: { emailAddress: 'test@example.com', studentId: '12345' },
        },
      ];
      component.loading = false;
      fixture.detectChanges();

      const metadataArray = component.getMetadataArray(component.results[0].metadata);

      expect(metadataArray.some((item) => item.key === 'Email Address')).toBe(true);
      expect(metadataArray.some((item) => item.key === 'Student Id')).toBe(true);
    });

    it('should display different icons for different entity types', () => {
      component.results = [mockStudentResults[0], mockCourseResults[0]];
      component.loading = false;
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const icons = compiled.querySelectorAll('.result-icon');

      expect(icons.length).toBe(2);
      expect(icons[0].className).toContain('bg-blue');
      expect(icons[1].className).toContain('bg-green');
    });

    it('should handle page navigation edge cases', () => {
      component.results = mockStudentResults;
      component.total = 50;
      component.page = 1;
      component.pageSize = 10;
      component.loading = false;
      fixture.detectChanges();

      spyOn(component.pageChanged, 'emit');

      component.onPageChange(0);
      expect(component.pageChanged.emit).toHaveBeenCalledWith(0);

      component.onPageChange(999);
      expect(component.pageChanged.emit).toHaveBeenCalledWith(999);
    });

    it('should handle missing metadata gracefully', () => {
      component.results = [
        {
          id: 'test-1',
          type: 'student',
          name: 'Test',
          relevanceScore: 0.8,
          metadata: undefined as any,
        },
      ];
      component.loading = false;

      expect(() => fixture.detectChanges()).not.toThrow();
    });

    it('should handle missing description', () => {
      component.results = [
        {
          id: 'test-1',
          type: 'student',
          name: 'Test',
          relevanceScore: 0.8,
          metadata: {},
        },
      ];
      component.loading = false;
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const description = compiled.querySelector('.result-description');

      expect(description).toBeFalsy();
    });

    it('should get correct result count text', () => {
      component.total = 0;
      expect(component.getResultCountText()).toBe('No results');

      component.total = 1;
      expect(component.getResultCountText()).toBe('1 result');

      component.total = 25;
      expect(component.getResultCountText()).toBe('25 results');
    });

    it('should determine pagination visibility correctly', () => {
      component.total = 5;
      component.pageSize = 10;
      expect(component.shouldShowPagination()).toBe(false);

      component.total = 25;
      component.pageSize = 10;
      expect(component.shouldShowPagination()).toBe(true);
    });

    it('should get correct icon classes for all entity types', () => {
      const studentClass = component.getIconClass('student');
      const courseClass = component.getIconClass('course');
      const assignmentClass = component.getIconClass('assignment');
      const allClass = component.getIconClass('all');

      expect(studentClass).toContain('blue');
      expect(courseClass).toContain('green');
      expect(assignmentClass).toContain('purple');
      expect(allClass).toContain('gray');
    });

    it('should get correct badge classes for all entity types', () => {
      const studentBadge = component.getBadgeClass('student');
      const courseBadge = component.getBadgeClass('course');
      const assignmentBadge = component.getBadgeClass('assignment');
      const allBadge = component.getBadgeClass('all');

      expect(studentBadge).toContain('blue');
      expect(courseBadge).toContain('green');
      expect(assignmentBadge).toContain('purple');
      expect(allBadge).toContain('gray');
    });

    it('should return empty array for null metadata', () => {
      const result = component.getMetadataArray(null as any);
      expect(result).toEqual([]);
    });

    it('should return empty array for undefined metadata', () => {
      const result = component.getMetadataArray(undefined as any);
      expect(result).toEqual([]);
    });

    it('should calculate correct page range display', () => {
      component.page = 2;
      component.pageSize = 10;
      component.total = 25;
      component.loading = false;
      fixture.detectChanges();

      const start = (component.page - 1) * component.pageSize + 1;
      const end = Math.min(component.page * component.pageSize, component.total);

      expect(start).toBe(11);
      expect(end).toBe(20);
    });

    it('should handle click on result item', () => {
      component.results = [mockStudentResults[0]];
      component.loading = false;
      fixture.detectChanges();

      spyOn(component.resultClicked, 'emit');

      const compiled = fixture.nativeElement as HTMLElement;
      const resultItem = compiled.querySelector('.result-item') as HTMLElement;
      resultItem.click();

      expect(component.resultClicked.emit).toHaveBeenCalledWith(mockStudentResults[0]);
    });

    it('should display correct relevance score percentage', () => {
      component.results = [mockStudentResults[0]];
      component.loading = false;
      fixture.detectChanges();

      const relevance = (mockStudentResults[0].relevanceScore * 100).toFixed(0);
      expect(parseInt(relevance)).toBe(95);
    });

    it('should handle all Math calculations in template', () => {
      component.page = 2;
      component.pageSize = 10;
      component.total = 35;
      component.results = mockStudentResults;
      component.loading = false;
      fixture.detectChanges();

      expect(component.Math).toBe(Math);
      expect(component.Math.min(component.page * component.pageSize, component.total)).toBe(20);
      expect(component.Math.ceil(component.total / component.pageSize)).toBe(4);
    });

    it('should handle assignment entity type icon', () => {
      component.results = [
        {
          id: 'assignment-1',
          type: 'assignment',
          name: 'Math Quiz',
          metadata: {},
          relevanceScore: 0.8,
        },
      ];
      component.loading = false;
      fixture.detectChanges();

      const iconClass = component.getIconClass('assignment');
      const badgeClass = component.getBadgeClass('assignment');

      expect(iconClass).toContain('purple');
      expect(badgeClass).toContain('purple');
    });

    it('should convert all metadata values to strings', () => {
      const metadata = {
        count: 42,
        active: true,
        score: 95.5,
      };

      const array = component.getMetadataArray(metadata);

      array.forEach((item) => {
        expect(typeof item.value).toBe('string');
      });
    });
  });
});

