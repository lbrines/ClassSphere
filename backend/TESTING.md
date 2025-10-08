# ClassSphere Backend Testing Guide

**Framework**: testify + httptest  
**Coverage**: 94.4% (target ≥80%)  
**Tests**: 150+

---

## 🎯 Testing Philosophy

### TDD-RunFix+ Methodology

```
1. RED    → Write failing test
2. RUN    → Verify test fails
3. FIX    → Implement minimal code
4. RUN    → Verify test passes
5. REFACTOR → Improve code
6. VALIDATE → Check coverage
7. DOCUMENT → Add comments/docs
```

---

## 🧪 Test Types

### Unit Tests (60% of tests)

**Location**: Alongside source files (`*_test.go`)  
**Focus**: Individual functions, business logic  
**Dependencies**: Mocked

**Example**:
```go
// internal/domain/role_test.go
package domain

import (
    "testing"
    "github.com/stretchr/testify/assert"
)

func TestRole_IsValid(t *testing.T) {
    tests := []struct{
        name     string
        role     Role
        expected bool
    }{
        {"admin is valid", RoleAdmin, true},
        {"empty is invalid", Role(""), false},
        {"unknown is invalid", Role("unknown"), false},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            assert.Equal(t, tt.expected, tt.role.IsValid())
        })
    }
}
```

---

### Integration Tests (30% of tests)

**Location**: `tests/integration/` or alongside adapters  
**Focus**: Component interaction, HTTP handlers  
**Dependencies**: Real or in-memory (miniredis)

**Example**:
```go
// internal/adapters/http/handler_test.go
func TestHandler_Login(t *testing.T) {
    // Setup
    repo := setupTestRepo()
    cache := setupTestCache()
    service := app.NewAuthService(repo, cache, ...)
    handler := New(service, ...)
    
    // Request
    body := `{"email":"admin@test.com","password":"admin123"}`
    req := httptest.NewRequest(POST, "/api/v1/auth/login", strings.NewReader(body))
    req.Header.Set("Content-Type", "application/json")
    rec := httptest.NewRecorder()
    
    // Execute
    handler.ServeHTTP(rec, req)
    
    // Assert
    assert.Equal(t, 200, rec.Code)
    var response authResponse
    json.Unmarshal(rec.Body.Bytes(), &response)
    assert.NotEmpty(t, response.AccessToken)
}
```

---

### E2E Tests (10% of tests)

**Location**: `cmd/api/main_test.go`  
**Focus**: Complete flows, real server  
**Dependencies**: Test server, mock external APIs

**Example**:
```go
// cmd/api/main_test.go
func TestOAuthFlow(t *testing.T) {
    // Start test server
    server := startTestServer(t)
    defer server.Close()
    
    // 1. Initiate OAuth
    resp := httpGet(t, server.URL+"/api/v1/auth/oauth/google")
    assert.Equal(t, 302, resp.StatusCode)
    location := resp.Header.Get("Location")
    assert.Contains(t, location, "accounts.google.com")
    
    // 2. Mock Google callback
    state := extractState(location)
    code := "mock-auth-code"
    resp = httpGet(t, server.URL+"/api/v1/auth/oauth/callback?code="+code+"&state="+state)
    
    // 3. Verify JWT returned
    var authResp authResponse
    json.Unmarshal(readBody(resp), &authResp)
    assert.NotEmpty(t, authResp.AccessToken)
}
```

---

## 🛠️ Running Tests

### Basic Commands

```bash
# Run all tests
go test ./...

# Run with coverage
go test -coverprofile=coverage.out ./...

# View coverage report (HTML)
go tool cover -html=coverage.out

# View coverage summary
go tool cover -func=coverage.out | grep total
```

### Specific Package

```bash
# Domain tests only
go test ./internal/domain/...

# Application tests only
go test ./internal/app/...

# Adapters tests only
go test ./internal/adapters/...
```

### Specific Test

```bash
# Run single test
go test ./internal/app -run TestAuthService_Login

# Run tests matching pattern
go test ./... -run TestAuth
```

### Verbose Output

```bash
# See test names and output
go test ./... -v

# See coverage per function
go test -coverprofile=coverage.out ./...
go tool cover -func=coverage.out
```

---

## 📊 Coverage Analysis

### View Coverage by Package

```bash
go test -coverprofile=coverage.out ./...
go tool cover -func=coverage.out

# Output example:
# github.com/lbrines/classsphere/internal/domain/role.go:15: IsValid 100.0%
# github.com/lbrines/classsphere/internal/app/auth_service.go:45: Login 95.2%
# total: (statements) 94.4%
```

### Find Untested Code

```bash
# Show lines with 0% coverage
go tool cover -func=coverage.out | grep "0.0%"

# Or use HTML view (uncovered lines highlighted in red)
go tool cover -html=coverage.out
```

---

## 🎭 Mocking

### Using testify/mock

```go
// Define mock
type MockUserRepository struct {
    mock.Mock
}

func (m *MockUserRepository) FindByEmail(ctx context.Context, email string) (*domain.User, error) {
    args := m.Called(ctx, email)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*domain.User), args.Error(1)
}

// Use in test
func TestAuthService_Login(t *testing.T) {
    mockRepo := new(MockUserRepository)
    
    // Setup expectations
    mockRepo.On("FindByEmail", mock.Anything, "admin@test.com").
        Return(&domain.User{ID: "1", Email: "admin@test.com"}, nil)
    
    // Test
    service := app.NewAuthService(mockRepo, ...)
    result, err := service.Login(ctx, "admin@test.com", "password")
    
    // Assert
    assert.NoError(t, err)
    mockRepo.AssertExpectations(t)  // Verify mock was called
}
```

---

## 🚦 Test Fixtures

### Test Data Setup

```go
// tests/fixtures/users.go
package fixtures

func AdminUser() *domain.User {
    return &domain.User{
        ID:    "admin-1",
        Name:  "Admin Test User",
        Email: "admin@test.com",
        Role:  domain.RoleAdmin,
    }
}

func TeacherUser() *domain.User {
    return &domain.User{
        ID:    "teacher-1",
        Name:  "Teacher Test User",
        Email: "teacher@test.com",
        Role:  domain.RoleTeacher,
    }
}

// Use in tests
func TestSomething(t *testing.T) {
    user := fixtures.AdminUser()
    // ...
}
```

---

## ⚡ Performance Testing

### Benchmarks

```go
// internal/app/auth_service_benchmark_test.go
func BenchmarkAuthService_Login(b *testing.B) {
    service := setupAuthService()
    
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        _, _ = service.Login(ctx, "admin@test.com", "password")
    }
}
```

**Run benchmarks**:
```bash
go test -bench=. -benchmem ./...
```

---

## 🐛 Debugging Tests

### Failed Tests

```bash
# Run with verbose
go test ./... -v

# Run specific test
go test ./internal/app -run TestAuthService_Login -v

# See panic stack traces
go test ./... -v 2>&1 | grep -A 20 "panic:"
```

### Test Timeouts

```bash
# Default timeout: 10 minutes
# Increase if needed
go test ./... -timeout 30s

# For OAuth tests (network calls)
go test ./internal/adapters/oauth -timeout 20s
```

---

## ✅ Coverage Targets

### By Package

| Package | Target | Actual | Status |
|---------|--------|--------|--------|
| **domain** | ≥90% | 97%+ | ✅ Exceeded |
| **app** | ≥90% | 96%+ | ✅ Exceeded |
| **adapters/http** | ≥85% | 92%+ | ✅ Exceeded |
| **adapters/oauth** | ≥85% | 90%+ | ✅ Exceeded |
| **adapters/repo** | ≥80% | 88%+ | ✅ Exceeded |
| **adapters/cache** | ≥80% | 100% | ✅ Exceeded |
| **adapters/google** | ≥80% | 94%+ | ✅ Exceeded |
| **shared** | ≥80% | 95%+ | ✅ Exceeded |
| **TOTAL** | ≥80% | **94.4%** | ✅ Exceeded |

---

## 📋 Testing Checklist

### Before Pull Request

- [ ] All tests pass: `go test ./...`
- [ ] Coverage maintained: `≥80%`
- [ ] No race conditions: `go test -race ./...`
- [ ] Linter passes: `golangci-lint run`
- [ ] Benchmarks don't regress (if applicable)

### Writing New Tests

- [ ] Test file named `*_test.go`
- [ ] Test function named `Test<FunctionName>`
- [ ] Use table-driven tests for multiple cases
- [ ] Mock external dependencies
- [ ] Test happy path + error cases
- [ ] Add comments explaining complex test logic

---

## 🎓 Best Practices

### 1. Table-Driven Tests

```go
func TestRole_String(t *testing.T) {
    tests := []struct{
        name     string
        role     Role
        expected string
    }{
        {"admin", RoleAdmin, "admin"},
        {"coordinator", RoleCoordinator, "coordinator"},
        {"teacher", RoleTeacher, "teacher"},
        {"student", RoleStudent, "student"},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            assert.Equal(t, tt.expected, tt.role.String())
        })
    }
}
```

### 2. Use Subtests

```go
func TestAuthService(t *testing.T) {
    t.Run("Login", func(t *testing.T) {
        t.Run("with valid credentials", func(t *testing.T) { ... })
        t.Run("with invalid credentials", func(t *testing.T) { ... })
        t.Run("with missing user", func(t *testing.T) { ... })
    })
    
    t.Run("ValidateToken", func(t *testing.T) { ... })
}
```

### 3. Test Cleanup

```go
func TestSomething(t *testing.T) {
    // Setup
    tempFile := createTempFile()
    defer os.Remove(tempFile)  // ✅ Cleanup
    
    // Test
    result := doSomething(tempFile)
    assert.NoError(t, result)
}
```

---

## 📚 Additional Resources

- [testify documentation](https://github.com/stretchr/testify)
- [Testing in Go](https://go.dev/doc/tutorial/add-a-test)
- [Table-driven tests](https://dave.cheney.net/2019/05/07/prefer-table-driven-tests)
- [Project Testing Strategy](../workspace/ci/06_plan_testing_strategy.md)

---

**Version**: 1.0  
**Coverage**: 94.4%  
**Last Updated**: 2025-10-08

