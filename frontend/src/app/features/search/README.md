# 🔍 Search Module - ClassSphere Frontend

**Phase 3 Advanced Search Implementation**

---

## 📁 Module Structure

```
search/
├── components/
│   ├── search-bar/
│   │   ├── search-bar.component.ts         # Search input + filters
│   │   └── search-bar.component.spec.ts    # 19 tests
│   └── search-results/
│       ├── search-results.component.ts     # Results display
│       └── search-results.component.spec.ts # 18 tests
├── pages/
│   └── search-page/
│       ├── search-page.component.ts        # Page container
│       └── search-page.component.spec.ts   # 6 tests
└── README.md
```

---

## 🚀 Quick Start

### 1. Import Components

```typescript
import { SearchPageComponent } from './features/search/pages/search-page/search-page.component';

// Add to routes
{
  path: 'search',
  component: SearchPageComponent,
  canActivate: [AuthGuard]
}
```

### 2. Use Components Individually

```typescript
// In your component
import { SearchBarComponent } from '@features/search/components/search-bar/search-bar.component';
import { SearchResultsComponent } from '@features/search/components/search-results/search-results.component';

@Component({
  template: `
    <app-search-bar
      [enableAutoSearch]="true"
      [debounceTime]="500"
      (searchTriggered)="onSearch($event)"
      (searchCleared)="onClear()"
    ></app-search-bar>

    <app-search-results
      [results]="results"
      [total]="total"
      [loading]="loading"
      (resultClicked)="onResultClick($event)"
      (pageChanged)="onPageChange($event)"
    ></app-search-results>
  `
})
```

---

## 🎯 Features

### SearchService
- Multi-entity search (students, courses, assignments)
- Advanced filtering (date range, status, course)
- Real-time state management with RxJS
- Error handling
- Loading states

### SearchBarComponent
- **Inputs**:
  - `enableAutoSearch: boolean` - Enable debounced auto-search (default: false)
  - `debounceTime: number` - Debounce time in ms (default: 500)
- **Outputs**:
  - `searchTriggered: EventEmitter<{query, filters}>` - Fired on search
  - `searchCleared: EventEmitter<void>` - Fired on clear
- **Features**:
  - Reactive forms validation
  - Entity type filter dropdown
  - Manual search trigger
  - Clear functionality
  - Loading indicator
  - Accessibility (WCAG 2.2 AA)

### SearchResultsComponent
- **Inputs**:
  - `results: SearchResult[]` - Search results to display
  - `total: number` - Total number of results
  - `page: number` - Current page (default: 1)
  - `pageSize: number` - Results per page (default: 10)
  - `loading: boolean` - Loading state
  - `query: string` - Current search query
- **Outputs**:
  - `resultClicked: EventEmitter<SearchResult>` - Fired on result click
  - `pageChanged: EventEmitter<number>` - Fired on page change
- **Features**:
  - Entity-specific icons and colors
  - Metadata display
  - Relevance score visualization
  - Pagination
  - Empty states
  - Keyboard navigation

---

## 📊 Test Coverage

| Component | Tests | Coverage |
|-----------|-------|----------|
| SearchService | 13 | 100% |
| SearchBarComponent | 19 | 100% |
| SearchResultsComponent | 18 | 100% |
| SearchPageComponent | 6 | 100% |
| **Total** | **56** | **96.34%** |

### Run Tests

```bash
# Run all search tests
npm test -- --include='**/search*.spec.ts' --watch=false

# Run with coverage
npm test -- --no-watch --code-coverage --include='**/search*.spec.ts'
```

---

## 🔧 API Integration

### Backend Endpoint Expected

```typescript
GET /api/search

Query Parameters:
- q: string (required) - Search query
- type: 'student' | 'course' | 'assignment' | 'all' (required)
- course?: string - Filter by course ID
- status?: 'active' | 'inactive' | 'archived'
- dateFrom?: string (ISO 8601)
- dateTo?: string (ISO 8601)
- page?: number (default: 1)
- pageSize?: number (default: 10)

Response:
{
  query: string;
  filters: SearchFilters;
  results: SearchResult[];
  total: number;
  page: number;
  pageSize: number;
  executionTime: number; // milliseconds
}
```

### SearchResult Model

```typescript
interface SearchResult {
  id: string;
  type: 'student' | 'course' | 'assignment';
  name: string;
  description?: string;
  metadata: Record<string, any>;
  relevanceScore: number; // 0-1
}
```

---

## 🎨 Styling

All components use **TailwindCSS** utility classes. No custom CSS required.

### Customization

Override Tailwind classes in your component:

```typescript
@Component({
  template: `
    <app-search-bar class="custom-search-bar"></app-search-bar>
  `,
  styles: [`
    .custom-search-bar {
      /* Your custom styles */
    }
  `]
})
```

---

## ♿ Accessibility

All components follow **WCAG 2.2 AA** standards:
- ✅ Semantic HTML
- ✅ ARIA labels and roles
- ✅ Keyboard navigation (Tab, Enter, Space)
- ✅ Focus management
- ✅ Screen reader compatible
- ✅ Color contrast ≥4.5:1

---

## 📱 Responsive Design

Components are fully responsive:
- Mobile: Stacked layout
- Tablet: Partial grid
- Desktop: Full grid layout

---

## 🐛 Troubleshooting

### Search not triggering
- Check `enableAutoSearch` is set correctly
- Verify debounce time is appropriate
- Ensure query is not empty or whitespace

### Results not displaying
- Verify backend endpoint is accessible
- Check browser console for errors
- Ensure SearchService is provided

### Styling issues
- Verify Tailwind CSS is configured
- Check for CSS conflicts
- Review browser DevTools

---

## 📚 Related Documentation

- [Phase 3 Plan](../../../../workspace/plan/04_plan_fase3_visualizacion.md)
- [Testing Strategy](../../../../workspace/contracts/09_ClassSphere_testing.md)
- [Implementation Report](../../../../workspace/fase1/FASE3_SEARCH_IMPLEMENTATION.md)

---

## 🤝 Contributing

1. Write tests first (TDD)
2. Follow Angular style guide
3. Maintain test coverage ≥85%
4. Update documentation
5. Run linter before commit

---

**Last Updated**: 2025-10-07  
**Status**: ✅ Production Ready  
**Maintainer**: ClassSphere Team

