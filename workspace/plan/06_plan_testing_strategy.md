---
id: "06"
title: "Testing Strategy"
priority: "CRITICAL"
version: "1.0"
date: "2025-10-07"
max_tokens: 1500
---

# Testing Strategy - ClassSphere

## Overview

ClassSphere follows strict Test-Driven Development (TDD) with comprehensive testing at all levels.

## Testing Stack

### Backend (Go)
```yaml
Unit Testing: testify/assert + testify/mock
HTTP Testing: httptest (Go standard library)
Mocking: testify/mock + mockery
Coverage: go test -cover
```

### Frontend (Angular 19)
```yaml
Unit Testing: Jasmine + Karma (Angular standard)
Component Testing: Angular Testing Library
E2E Testing: Playwright
Coverage: karma-coverage
```

## Coverage Requirements

| Type | Global | Critical | Security |
|------|--------|----------|----------|
| Lines | ≥80% | ≥90% | ≥95% |
| Branches | ≥65% | ≥80% | ≥85% |
| Functions | ≥80% | ≥90% | ≥95% |

## TDD Methodology

### Red-Green-Refactor Cycle
1. **Red**: Write failing test
2. **Green**: Implement minimum code to pass
3. **Refactor**: Improve code keeping tests green
4. **Repeat**: For every feature

### Test Structure (AAA Pattern)
```go
func TestAuthService_Login_Success(t *testing.T) {
    // ARRANGE: Setup test data and mocks
    mockRepo := new(MockUserRepo)
    authService := NewAuthService("secret", mockRepo)
    
    // ACT: Execute the function under test
    token, err := authService.Login("test@example.com", "password")
    
    // ASSERT: Verify results
    assert.NoError(t, err)
    assert.NotEmpty(t, token)
}
```

## Backend Testing

### Unit Tests
```go
// tests/unit/auth_service_test.go
package unit

import (
    "testing"
    "github.com/stretchr/testify/assert"
)

func TestGenerateToken_ValidUser(t *testing.T) {
    // Test implementation
}

func TestVerifyToken_ExpiredToken(t *testing.T) {
    // Test implementation
}
```

### Integration Tests
```go
// tests/integration/auth_endpoints_test.go
package integration

import (
    "net/http/httptest"
    "testing"
)

func TestLoginEndpoint_ValidCredentials(t *testing.T) {
    // Test implementation
}
```

## Frontend Testing

### Component Tests (Jasmine)
```typescript
// src/app/features/auth/login/login.component.spec.ts
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { LoginComponent } from './login.component';

describe('LoginComponent', () => {
  let component: LoginComponent;
  let fixture: ComponentFixture<LoginComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LoginComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(LoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should display login form', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('form')).toBeTruthy();
  });

  it('should call login service on submit', () => {
    spyOn(component.authService, 'login');
    component.onSubmit({ email: 'test@example.com', password: 'pass' });
    expect(component.authService.login).toHaveBeenCalled();
  });
});
```

### Service Tests
```typescript
// src/app/core/services/auth.service.spec.ts
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { AuthService } from './auth.service';

describe('AuthService', () => {
  let service: AuthService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [AuthService]
    });
    service = TestBed.inject(AuthService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should login successfully', () => {
    const mockResponse = { token: 'abc123', user: { email: 'test@example.com' } };

    service.login('test@example.com', 'password').subscribe(response => {
      expect(response.token).toBe('abc123');
    });

    const req = httpMock.expectOne('http://localhost:8080/auth/login');
    expect(req.request.method).toBe('POST');
    req.flush(mockResponse);
  });
});
```

### E2E Tests (Playwright)
```typescript
// tests/e2e/auth/login.spec.ts
import { test, expect } from '@playwright/test';

test('user can login with valid credentials', async ({ page }) => {
  await page.goto('http://localhost:4200/login');
  
  await page.fill('input[name="email"]', 'admin@classsphere.edu');
  await page.fill('input[name="password"]', 'admin123');
  await page.click('button[type="submit"]');
  
  await expect(page).toHaveURL('http://localhost:4200/dashboard');
  await expect(page.locator('text=Welcome')).toBeVisible();
});

test('user sees error with invalid credentials', async ({ page }) => {
  await page.goto('http://localhost:4200/login');
  
  await page.fill('input[name="email"]', 'invalid@example.com');
  await page.fill('input[name="password"]', 'wrong');
  await page.click('button[type="submit"]');
  
  await expect(page.locator('text=Invalid credentials')).toBeVisible();
});
```

## Validation Commands

### Backend
```bash
# Run all tests
go test ./... -v

# Run with coverage
go test ./... -cover

# Generate coverage report
go test ./... -coverprofile=coverage.out
go tool cover -html=coverage.out

# Run specific tests
go test ./tests/unit/... -v
go test ./tests/integration/... -v

# Fail if coverage below threshold
go test ./... -coverprofile=coverage.out -covermode=count
go tool cover -func=coverage.out | grep total | awk '{if ($3+0 < 80.0) exit 1}'
```

### Frontend
```bash
# Run unit tests
ng test

# Run with coverage
ng test --code-coverage

# Run in headless mode
ng test --browsers=ChromeHeadless --watch=false

# Run E2E tests
npx playwright test

# Run specific E2E test
npx playwright test tests/e2e/auth/login.spec.ts
```

## Test Organization

```
tests/
├── unit/                      # Unit tests (isolated)
│   ├── services/
│   ├── domain/
│   └── utils/
├── integration/               # Integration tests
│   ├── api/
│   ├── database/
│   └── external/
└── e2e/                       # End-to-end tests
    ├── auth/
    ├── dashboard/
    └── admin/
```

## Mocking Strategy

### Backend Mocks
```go
// tests/mocks/user_repository.go
package mocks

import (
    "github.com/stretchr/testify/mock"
)

type MockUserRepository struct {
    mock.Mock
}

func (m *MockUserRepository) FindByEmail(email string) (*User, error) {
    args := m.Called(email)
    return args.Get(0).(*User), args.Error(1)
}

func (m *MockUserRepository) Create(user *User) error {
    args := m.Called(user)
    return args.Error(0)
}
```

### Frontend Mocks
```typescript
// src/app/core/services/auth.service.mock.ts
export class MockAuthService {
  login = jasmine.createSpy('login').and.returnValue(
    of({ token: 'mock-token', user: { email: 'test@example.com' } })
  );
  
  logout = jasmine.createSpy('logout').and.returnValue(of(true));
  
  getCurrentUser = jasmine.createSpy('getCurrentUser').and.returnValue(
    of({ id: '1', email: 'test@example.com', role: 'student' })
  );
}
```

## CI/CD Integration

### GitHub Actions
```yaml
# .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-go@v4
        with:
          go-version: '1.21'
      - name: Run tests
        run: go test ./... -cover
      - name: Check coverage
        run: |
          go test ./... -coverprofile=coverage.out
          coverage=$(go tool cover -func=coverage.out | grep total | awk '{print $3}' | sed 's/%//')
          if (( $(echo "$coverage < 80.0" | bc -l) )); then
            echo "Coverage $coverage% is below 80%"
            exit 1
          fi

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: npm install
      - name: Run unit tests
        run: ng test --code-coverage --watch=false --browsers=ChromeHeadless
      - name: Check coverage
        run: |
          # Karma generates coverage report
          # Fail if below threshold (configured in karma.conf.js)

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - name: Install Playwright
        run: npx playwright install --with-deps
      - name: Start services
        run: docker-compose up -d
      - name: Run E2E tests
        run: npx playwright test
      - name: Upload test results
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-results
          path: test-results/
```

## Best Practices

1. **Write tests first** (TDD strict)
2. **One assertion per test** (when possible)
3. **Independent tests** (no shared state)
4. **Fast tests** (unit <50ms, integration <500ms)
5. **Clear test names** (describe what is being tested)
6. **Mock external dependencies**
7. **Test edge cases and errors**
8. **Maintain coverage thresholds**

---

**Last updated**: 2025-10-07  
**Testing is not optional. It's the foundation of quality.**

