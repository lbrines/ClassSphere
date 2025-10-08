---
id: "03"
title: "Phase 2: Google Classroom Integration"
version: "4.0"
priority: "HIGH"
tokens: "<1500"
duration: "10 days"
date: "2025-10-07"
status: "⏳ PENDING"
prerequisites: "Phase 1 completed (Backend + Frontend + Integration)"
---

# Phase 2: Google Classroom Integration

**Duration**: 10 days (Days 13-22)  
**Status**: ⏳ PENDING  
**Prerequisites**: Phase 1 ✅ Complete

---

## 🎯 INICIO: Phase 2 Objectives

### Mission
Integrate Google Classroom API with dual mode (Mock/Real), implement role-based dashboards, and establish data synchronization foundation.

### Critical Objectives

**Days 13-15: Google Classroom API**
- [ ] Google Classroom API client (oauth2, rate limiting)
- [ ] Dual mode service (Mock/Real switchable)
- [ ] Basic endpoints: courses, students, assignments
- [ ] Mock data generator for development
- [ ] Rate limiting: 100 req/100s per user

**Days 16-18: Dashboard Endpoints**
- [ ] Admin dashboard API (system metrics)
- [ ] Coordinator dashboard API (program metrics)
- [ ] Teacher dashboard API (course metrics)
- [ ] Student dashboard API (personal progress)
- [ ] Role-based data filtering

**Days 19-22: Dashboard UI + Integration**
- [ ] Dashboard components per role (4 components)
- [ ] ApexCharts integration (basic charts)
- [ ] Real-time data updates
- [ ] Mode switcher UI (Mock ↔ Real)
- [ ] E2E tests for all dashboards

### Success Criteria

**Backend**:
- AC-BE-201: Dual mode implementation ✅/❌
- AC-BE-202: Course synchronization ✅/❌
- AC-BE-203: Student management ✅/❌
- AC-BE-204: Assignment integration ✅/❌
- AC-BE-205-208: Dashboard APIs (4 roles) ✅/❌
- AC-BE-209: Coverage maintained ≥80% ✅/❌

**Frontend**:
- AC-FE-301-304: Dashboard UIs (4 roles) ✅/❌
- AC-FE-305: ApexCharts integration ✅/❌
- AC-FE-311: Component tests ✅/❌

**Integration**:
- AC-INT-201: Mock mode functional ✅/❌
- AC-INT-202: Real mode functional ✅/❌
- AC-INT-203: Mode switching seamless ✅/❌

---

## 📅 MEDIO: Implementation Plan

### Days 13-15: Google Classroom API (TDD)

#### Day 13: API Client + Mock Service

**Test First** (RED):
```go
// tests/unit/google_classroom_test.go
func TestListCourses_MockMode(t *testing.T) {
    client := NewClassroomService(ModeMock)
    courses, err := client.ListCourses(context.Background())
    
    assert.NoError(t, err)
    assert.Len(t, courses, 10) // Mock returns 10 courses
    assert.Equal(t, "eCommerce Specialist", courses[0].Name)
}

func TestListCourses_RealMode(t *testing.T) {
    client := NewClassroomService(ModeReal)
    // Skip if no credentials
    if os.Getenv("GOOGLE_CREDENTIALS") == "" {
        t.Skip("No Google credentials")
    }
    
    courses, err := client.ListCourses(context.Background())
    assert.NoError(t, err)
}
```

**Implementation** (GREEN):
```go
// internal/adapters/google/classroom.go
type ClassroomService struct {
    mode   Mode
    client *classroom.Service
    mock   *MockService
}

func (c *ClassroomService) ListCourses(ctx context.Context) ([]*Course, error) {
    if c.mode == ModeMock {
        return c.mock.ListCourses(), nil
    }
    
    resp, err := c.client.Courses.List().Do()
    if err != nil {
        return nil, err
    }
    
    return convertCourses(resp.Courses), nil
}
```

**Mock Data Generator**:
```go
// internal/adapters/google/mock.go
func (m *MockService) ListCourses() []*Course {
    return []*Course{
        {ID: "course-001", Name: "eCommerce Specialist", Students: 150},
        {ID: "course-002", Name: "Digital Marketing", Students: 120},
        // ... 8 more courses
    }
}
```

---

#### Day 14: Rate Limiting + Error Handling

**Rate Limiter**:
```go
// internal/adapters/google/rate_limiter.go
type RateLimiter struct {
    limiter *rate.Limiter
}

func NewRateLimiter() *RateLimiter {
    return &RateLimiter{
        limiter: rate.NewLimiter(rate.Every(time.Second), 100), // 100/sec
    }
}

func (r *RateLimiter) Wait(ctx context.Context) error {
    return r.limiter.Wait(ctx)
}
```

**Error Handling**:
```go
func (c *ClassroomService) ListCourses(ctx context.Context) ([]*Course, error) {
    if err := c.rateLimiter.Wait(ctx); err != nil {
        return nil, fmt.Errorf("rate limit: %w", err)
    }
    
    // ... implementation with exponential backoff
}
```

---

#### Day 15: Students + Assignments Endpoints

**Tests**:
```go
func TestListStudents(t *testing.T) {
    client := NewClassroomService(ModeMock)
    students, err := client.ListStudents(ctx, "course-001")
    
    assert.NoError(t, err)
    assert.NotEmpty(t, students)
}
```

**Acceptance Criteria**: AC-BE-201, AC-BE-202, AC-BE-203, AC-BE-204 ✅

---

### Days 16-18: Dashboard APIs

#### Day 16: Admin Dashboard Endpoint

**Test First**:
```go
func TestAdminDashboard(t *testing.T) {
    e := echo.New()
    req := httptest.NewRequest(http.MethodGet, "/api/v1/dashboard/admin", nil)
    req.Header.Set("Authorization", "Bearer "+adminToken)
    rec := httptest.NewRecorder()
    c := e.NewContext(req, rec)
    
    err := AdminDashboardHandler(c)
    
    assert.NoError(t, err)
    assert.Equal(t, 200, rec.Code)
    
    var resp AdminDashboardResponse
    json.Unmarshal(rec.Body.Bytes(), &resp)
    assert.NotZero(t, resp.Metrics.TotalUsers)
}
```

**Implementation**:
```go
// internal/adapters/http/dashboard_handler.go
func AdminDashboardHandler(c echo.Context) error {
    metrics := service.GetAdminMetrics(c.Request().Context())
    return c.JSON(200, metrics)
}
```

**Acceptance Criteria**: AC-BE-205 ✅

---

#### Day 17: Coordinator + Teacher Dashboards

**Implement**:
- Coordinator: Program-level metrics (filtered by assigned programs)
- Teacher: Course-level metrics (filtered by assigned courses)

**Acceptance Criteria**: AC-BE-206, AC-BE-207 ✅

---

#### Day 18: Student Dashboard + RBAC Validation

**Student Dashboard**:
```go
func StudentDashboardHandler(c echo.Context) error {
    userID := c.Get("user_id").(string)
    progress := service.GetStudentProgress(c.Request().Context(), userID)
    return c.JSON(200, progress)
}
```

**RBAC Tests**:
```go
func TestStudentCannotAccessAdminDashboard(t *testing.T) {
    // ... test that student token gets 403 on admin endpoint
}
```

**Acceptance Criteria**: AC-BE-208, AC-BE-209 ✅

---

### Days 19-22: Dashboard UI

#### Day 19: Dashboard Components Structure

**Create Components**:
```bash
cd frontend
npx ng generate component dashboard/admin --standalone
npx ng generate component dashboard/coordinator --standalone
npx ng generate component dashboard/teacher --standalone
npx ng generate component dashboard/student --standalone
```

**Test First**:
```typescript
// admin-dashboard.component.spec.ts
describe('AdminDashboardComponent', () => {
  it('should load admin metrics', () => {
    spyOn(dashboardService, 'getAdminMetrics').and.returnValue(of(mockMetrics));
    component.ngOnInit();
    expect(component.metrics).toBeDefined();
  });
});
```

---

#### Day 20: ApexCharts Integration

**Install**:
```bash
npm install apexcharts@5.3.5 ng-apexcharts
```

**Implementation**:
```typescript
// admin-dashboard.component.ts
export class AdminDashboardComponent {
  chartOptions: any;

  ngOnInit() {
    this.chartOptions = {
      series: [{name: "Users", data: [10, 41, 35, 51, 49, 62, 69]}],
      chart: {type: "line", height: 350},
      xaxis: {categories: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]}
    };
  }
}
```

**Acceptance Criteria**: AC-FE-305 ✅

---

#### Day 21: Mode Switcher + Real-time Updates

**Mode Switcher**:
```typescript
// mode-switcher.component.ts
export class ModeSwitcherComponent {
  currentMode$ = this.modeService.currentMode$;

  toggleMode() {
    this.modeService.toggleMode().subscribe();
  }
}
```

**Real-time Updates** (RxJS):
```typescript
ngOnInit() {
  this.dashboardService.getMetrics().pipe(
    switchMap(() => interval(30000)), // Refresh every 30s
    switchMap(() => this.dashboardService.getMetrics())
  ).subscribe(metrics => this.metrics = metrics);
}
```

---

#### Day 22: E2E Tests + Validation

**E2E Test**:
```typescript
// e2e/dashboards.spec.ts
test('admin dashboard loads correctly', async ({ page }) => {
  await page.goto('http://localhost:4200/login');
  await loginAsAdmin(page);
  
  await expect(page).toHaveURL('/dashboard/admin');
  await expect(page.locator('h1')).toContainText('Admin Dashboard');
  await expect(page.locator('.metrics-card')).toHaveCount(4);
});
```

**Acceptance Criteria**: AC-FE-301, AC-FE-302, AC-FE-303, AC-FE-304, AC-FE-311 ✅

---

## ✅ FINAL: Validation and Handoff

### Phase 2 Checklist

**Backend**:
- [ ] Google Classroom API client functional
- [ ] Dual mode (Mock/Real) working
- [ ] Rate limiting implemented (100 req/100s)
- [ ] 4 dashboard endpoints (admin, coordinator, teacher, student)
- [ ] RBAC enforced on all endpoints
- [ ] Coverage ≥80% maintained

**Frontend**:
- [ ] 4 dashboard components implemented
- [ ] ApexCharts displaying data
- [ ] Mode switcher functional
- [ ] Real-time updates working
- [ ] Component tests passing

**Integration**:
- [ ] Mock mode provides realistic data
- [ ] Real mode connects to Google API (when credentials available)
- [ ] Mode switching seamless
- [ ] E2E tests for all dashboards passing

### Verification Commands

```bash
# Backend
go test ./internal/adapters/google/... -v
curl -H "Authorization: Bearer $ADMIN_TOKEN" http://localhost:8080/api/v1/dashboard/admin

# Frontend
npx ng test --include='**/dashboard/**'
npx playwright test e2e/dashboards.spec.ts

# Integration
curl http://localhost:8080/api/v1/google/status
```

### Next Phase Prerequisites

**Before Starting Phase 3**:
- [ ] All Phase 2 acceptance criteria ✅
- [ ] Google API integration tested
- [ ] Dashboard APIs documented
- [ ] Mock data comprehensive
- [ ] Charts displaying correctly

### Handoff to Phase 3

**Status**: Phase 2 → Phase 3  
**Next**: Advanced Search + WebSocket Notifications  
**Read**: `04_plan_fase3_visualizacion.md`

---

**CRITICAL**: Verify all dashboard endpoints return appropriate data for each role before proceeding.

**Last Updated**: 2025-10-07 | **Version**: 4.0

