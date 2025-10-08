---
id: "06"
title: "Testing Strategy"
version: "4.0"
type: "support"
date: "2025-10-07"
---

# Testing Strategy - ClassSphere

## Stack de Testing

### Backend (Go)
- **testify/assert**: Assertions
- **testify/mock**: Mocking
- **httptest**: HTTP testing
- **go test -cover**: Coverage analysis

### Frontend (Angular)
- **Jasmine**: Test framework (Angular standard)
- **Karma**: Test runner
- **Playwright**: E2E testing
- **karma-coverage**: Coverage reporting

## TDD-RunFix+ Methodology

```
1. RED    → Write failing test
2. GREEN  → Minimum code to pass
3. REFACTOR → Improve while green
4. VALIDATE → Apply error prevention patterns
5. DOCUMENT → Record decisions
6. INTEGRATE → Merge with system
7. VERIFY  → Check acceptance criteria
```

## Coverage Requirements

- **Global**: ≥80% lines, ≥65% branches
- **Critical Modules**: ≥90% lines, ≥80% branches
- **Security Components**: ≥95% lines, ≥85% branches
- **API Endpoints**: 100% success + error cases

## Test Templates

### Backend Unit Test
```go
func TestServiceMethod(t *testing.T) {
    // Arrange
    service := NewService()
    input := "test-input"
    
    // Act
    result, err := service.Method(context.Background(), input)
    
    // Assert
    assert.NoError(t, err)
    assert.NotEmpty(t, result)
}
```

### Frontend Component Test
```typescript
describe('Component', () => {
  it('should do something', () => {
    // Arrange
    component.input = 'test';
    
    // Act
    component.method();
    
    // Assert
    expect(component.output).toBe('expected');
  });
});
```

### E2E Test
```typescript
test('user flow', async ({ page }) => {
  await page.goto('http://localhost:4200');
  await page.click('button');
  await expect(page).toHaveURL('/success');
});
```

## Verification Commands

### Backend
```bash
go test ./... -coverprofile=coverage.out
go tool cover -func=coverage.out | grep total
go tool cover -html=coverage.out -o coverage.html
```

### Frontend
```bash
ng test --code-coverage
npx playwright test
open coverage/index.html
```

---

**Reference**: See `../contracts/09_ClassSphere_testing.md` for detailed testing strategy.

