---
id: "03"
title: "Phase 2: Google Classroom Integration"
priority: "HIGH"
version: "1.0"
date: "2025-10-07"
duration: "10 days"
max_tokens: 1500
---

# Phase 2: Google Integration (Days 13-22)

## 🎯 INICIO: PHASE OBJECTIVES

### Phase Overview
Integrate Google Classroom API with dual mode (Google/Mock), implement role-specific dashboards, and add interactive visualizations with ApexCharts.

### Critical Dependencies (From Phase 1)
- ✅ Backend running on port 8080
- ✅ Frontend running on port 4200
- ✅ JWT + OAuth 2.0 working
- ✅ Role system implemented
- ✅ Test coverage ≥80%

### Success Criteria
- [ ] Google Classroom API integrated
- [ ] Dual mode (Google/Mock) functional
- [ ] 4 role-based dashboards complete
- [ ] ApexCharts interactive visualizations
- [ ] Tests coverage maintained at ≥80%

### Technology Stack
```yaml
Backend:
  - Google Classroom API SDK
  - Mock data service
  - Metrics calculation service
  - Dashboard aggregation service

Frontend:
  - ApexCharts v5.3.5
  - Angular reactive forms
  - RxJS for state management
  - Role-based components
```

## 📅 MEDIO: IMPLEMENTATION DETAILS

### Days 13-17: Backend Google Integration

#### Day 13: Google Classroom API Service
```go
// internal/adapters/google/classroom_service.go
package google

import (
    "context"
    
    "google.golang.org/api/classroom/v1"
    "google.golang.org/api/option"
)

type ClassroomService struct {
    service *classroom.Service
    mode    string // "google" or "mock"
}

func NewClassroomService(credentials, mode string) (*ClassroomService, error) {
    ctx := context.Background()
    srv, err := classroom.NewService(ctx, option.WithCredentialsFile(credentials))
    if err != nil {
        return nil, err
    }
    
    return &ClassroomService{
        service: srv,
        mode:    mode,
    }, nil
}

func (s *ClassroomService) ListCourses(userID string) ([]*Course, error) {
    if s.mode == "mock" {
        return s.getMockCourses(), nil
    }
    
    courses, err := s.service.Courses.List().Do()
    if err != nil {
        return nil, err
    }
    
    return convertCourses(courses.Courses), nil
}
```

#### Days 14-15: Dashboard Services
**Admin Dashboard**: System-wide metrics  
**Coordinator Dashboard**: Program-level metrics  
**Teacher Dashboard**: Course-level metrics  
**Student Dashboard**: Personal progress

#### Days 16-17: Dual Mode Implementation
Mock service with realistic data, toggle between Google and Mock modes, comprehensive testing for both modes.

### Days 18-22: Frontend Dashboards

#### Day 18: Dashboard Base Component
```typescript
// src/app/features/dashboard/dashboard.component.ts
import { Component, OnInit } from '@angular/core';
import { AuthService } from '@core/services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  template: `
    <div class="dashboard-container">
      <app-admin-dashboard *ngIf="role === 'admin'"></app-admin-dashboard>
      <app-coordinator-dashboard *ngIf="role === 'coordinator'"></app-coordinator-dashboard>
      <app-teacher-dashboard *ngIf="role === 'teacher'"></app-teacher-dashboard>
      <app-student-dashboard *ngIf="role === 'student'"></app-student-dashboard>
    </div>
  `
})
export class DashboardComponent implements OnInit {
  role: string = '';
  
  constructor(private authService: AuthService) {}
  
  ngOnInit() {
    this.role = this.authService.getCurrentUserRole();
  }
}
```

#### Days 19-20: Role-Specific Dashboards
Each dashboard with ApexCharts, metrics cards, real-time updates with RxJS.

#### Days 21-22: Google Connect Component
Mode selector, course list, connection status, error handling.

## ✅ FINAL: VERIFICATION CHECKLIST

### Backend Verification
- [ ] Google Classroom API connected
- [ ] Mock mode working
- [ ] Dashboard endpoints returning correct data
- [ ] Tests passing with ≥80% coverage

### Frontend Verification
- [ ] All 4 dashboards rendering
- [ ] ApexCharts displaying correctly
- [ ] Mode switching working
- [ ] Tests passing with ≥80% coverage

### Integration Verification
- [ ] Frontend fetches data from backend
- [ ] Role-based dashboards show correct data
- [ ] Mode switching reflects in UI
- [ ] Error handling working

### Validation Commands
```bash
# Backend
go test ./... -v -cover

# Frontend
ng test --code-coverage

# Integration
curl http://localhost:8080/api/dashboard/admin
curl http://localhost:8080/api/google/courses
```

---

**Last updated**: 2025-10-07  
**Duration**: 10 days  
**Status**: Ready for execution

