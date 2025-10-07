---
id: "04"
title: "Phase 3: Advanced Visualization"
version: "4.0"
priority: "MEDIUM"
tokens: "<1000"
duration: "10 days"
date: "2025-10-07"
status: "⏳ PENDING"
prerequisites: "Phase 2 completed (Google Integration + Dashboards)"
---

# Phase 3: Advanced Visualization

**Duration**: 10 days (Days 23-32)  
**Prerequisites**: Phase 1 ✅ + Phase 2 ✅

---

## 🎯 INICIO: Objectives

### Mission
Implement advanced search, real-time WebSocket notifications, and interactive D3.js visualizations.

### Critical Objectives

**Days 23-25: Advanced Search**
- [ ] Multi-entity search backend (students, courses, assignments)
- [ ] Contextual filters (role-based, date range, status)
- [ ] Search UI with autocomplete
- [ ] Saved searches functionality

**Days 26-28: WebSocket Notifications**
- [ ] WebSocket server (Echo/ws)
- [ ] Notification service (create, send, mark read)
- [ ] Frontend WebSocket client (RxJS)
- [ ] Polling fallback (30s intervals)

**Days 29-32: Interactive Charts**
- [ ] D3.js custom visualizations
- [ ] Drill-down functionality
- [ ] Chart export (PDF, PNG, SVG)
- [ ] Mobile-responsive charts

---

## 📅 MEDIO: Implementation

### Days 23-25: Advanced Search (TDD)

**Backend Test**:
```go
func TestSearch_MultiEntity(t *testing.T) {
    service := NewSearchService()
    results, err := service.Search(ctx, "John", []string{"students", "teachers"})
    
    assert.NoError(t, err)
    assert.NotEmpty(t, results)
}
```

**Backend Implementation**:
```go
// internal/app/search_service.go
func (s *SearchService) Search(ctx context.Context, query string, entities []string) (*SearchResults, error) {
    var results SearchResults
    
    for _, entity := range entities {
        switch entity {
        case "students":
            students, _ := s.repo.SearchStudents(ctx, query)
            results.Students = students
        case "courses":
            courses, _ := s.repo.SearchCourses(ctx, query)
            results.Courses = courses
        }
    }
    
    return &results, nil
}
```

**Frontend Search Component**:
```typescript
// search.component.ts
export class SearchComponent {
  searchControl = new FormControl('');
  results$ = this.searchControl.valueChanges.pipe(
    debounceTime(300),
    distinctUntilChanged(),
    switchMap(query => this.searchService.search(query))
  );
}
```

**Acceptance Criteria**: AC-FE-308 ✅

---

### Days 26-28: WebSocket Notifications

**Backend WebSocket Server**:
```go
// internal/adapters/http/websocket_handler.go
func WebSocketHandler(c echo.Context) error {
    ws, err := upgrader.Upgrade(c.Response(), c.Request(), nil)
    if err != nil {
        return err
    }
    defer ws.Close()
    
    for {
        notification := <-notificationChan
        ws.WriteJSON(notification)
    }
}
```

**Frontend WebSocket Client**:
```typescript
// notification.service.ts
export class NotificationService {
  private ws$ = webSocket('ws://localhost:8080/api/v1/ws/notifications');
  
  notifications$ = this.ws$.pipe(
    retryWhen(errors => errors.pipe(delay(3000))),
    catchError(() => this.pollingFallback())
  );
  
  private pollingFallback() {
    return interval(30000).pipe(
      switchMap(() => this.http.get('/api/v1/notifications'))
    );
  }
}
```

**Acceptance Criteria**: AC-FE-309, AC-FE-310 ✅

---

### Days 29-32: Interactive Charts

**D3.js Custom Visualization**:
```typescript
// chart.component.ts
export class ChartComponent implements AfterViewInit {
  ngAfterViewInit() {
    const svg = d3.select('#chart')
      .append('svg')
      .attr('width', 800)
      .attr('height', 400);
    
    // Custom visualization with drill-down
    svg.selectAll('rect')
      .data(this.data)
      .enter()
      .append('rect')
      .on('click', (event, d) => this.drillDown(d));
  }
}
```

**Chart Export**:
```typescript
exportChart(format: 'pdf' | 'png' | 'svg') {
  const svg = document.querySelector('#chart svg');
  // Convert to selected format
}
```

**Acceptance Criteria**: AC-FE-306, AC-FE-307 ✅

---

## ✅ FINAL: Validation

### Phase 3 Checklist

**Backend**:
- [ ] Search API functional (multi-entity)
- [ ] WebSocket server running
- [ ] Notification service working
- [ ] Coverage ≥80%

**Frontend**:
- [ ] Search UI with autocomplete
- [ ] WebSocket notifications real-time
- [ ] D3.js charts interactive
- [ ] Charts exportable
- [ ] Polling fallback working

**E2E**:
- [ ] Search returns results <500ms
- [ ] Notifications deliver <1s
- [ ] Charts responsive on mobile

### Verification Commands

```bash
# WebSocket
wscat -c ws://localhost:8080/api/v1/ws/notifications

# Search
curl "http://localhost:8080/api/v1/search/students?q=John"

# Frontend
npx playwright test e2e/search.spec.ts
npx playwright test e2e/notifications.spec.ts
```

### Handoff to Phase 4

**Next**: Bidirectional Sync + WCAG 2.2 AA + CI/CD  
**Read**: `05_plan_fase4_integracion.md`

---

**Last Updated**: 2025-10-07

