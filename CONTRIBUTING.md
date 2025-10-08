# Contributing to ClassSphere

Thank you for your interest in contributing to ClassSphere! This document provides guidelines and standards for contributing to the project.

---

## 📋 Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Testing Requirements](#testing-requirements)
6. [Pull Request Process](#pull-request-process)
7. [Commit Message Convention](#commit-message-convention)

---

## 🤝 Code of Conduct

### Our Pledge

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards others

---

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/ClassSphere.git
cd ClassSphere
```

### 2. Set Up Development Environment

**Option A: Dev Containers** (Recommended)
```bash
code .
# F1 → "Dev Containers: Reopen in Container"
# Wait ~3-5 minutes for setup
```

**Option B: Manual Setup**
```bash
# Backend
cd backend
go mod download
export JWT_SECRET="dev-secret-key"
# ... (see backend/README.md)

# Frontend
cd frontend
npm ci
npm start
```

### 3. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

---

## 🔄 Development Workflow

### 1. Development Process

```
1. Create branch from main
   ↓
2. Implement feature + tests
   ↓
3. Run tests locally (must pass)
   ↓
4. Commit with conventional commits
   ↓
5. Push to your fork
   ↓
6. Create Pull Request
   ↓
7. Address review feedback
   ↓
8. Merge when approved
```

### 2. Before Committing

**Checklist**:
- [ ] Tests pass: `go test ./...` (backend) and `npm test` (frontend)
- [ ] Coverage maintained: ≥80%
- [ ] Linter passes: `golangci-lint run` (backend)
- [ ] Code formatted: `go fmt` (backend), `npm run lint` (frontend)
- [ ] No console.log or debug statements
- [ ] Documentation updated if needed

---

## 📝 Coding Standards

### Backend (Go)

#### File Organization

```go
// 1. Package declaration
package mypackage

// 2. Imports (grouped)
import (
    // Standard library
    "context"
    "fmt"
    
    // External dependencies
    "github.com/labstack/echo/v4"
    
    // Internal packages
    "github.com/lbrines/classsphere/internal/domain"
)

// 3. Constants
const DefaultTimeout = 30 * time.Second

// 4. Types
type MyService struct { ... }

// 5. Functions
func New(...) *MyService { ... }
```

#### Naming Conventions

- **Packages**: lowercase, single word (`domain`, `app`, `http`)
- **Files**: snake_case (`auth_service.go`, `user_repo.go`)
- **Types**: PascalCase (`AuthService`, `UserRepository`)
- **Functions**: PascalCase for exported, camelCase for private
- **Constants**: PascalCase or UPPER_SNAKE_CASE for public

#### Error Handling

```go
// ✅ GOOD: Wrap errors with context
if err != nil {
    return fmt.Errorf("fetch user %s: %w", userID, err)
}

// ❌ BAD: Lose error context
if err != nil {
    return err
}
```

#### Testing

- Test files: `*_test.go` alongside source files
- Use testify for assertions: `assert.Equal(t, expected, actual)`
- Mock external dependencies (ports)
- Coverage target: ≥80%

---

### Frontend (Angular + TypeScript)

#### File Organization

```typescript
// 1. Imports (grouped)
import { Component, OnInit } from '@angular/core';  // Angular
import { Observable } from 'rxjs';  // RxJS
import { MyService } from '@core/services/my.service';  // Local

// 2. Decorator
@Component({...})

// 3. Class
export class MyComponent implements OnInit {
  // Properties
  // Constructor
  // Lifecycle hooks
  // Methods
}
```

#### Naming Conventions

- **Files**: kebab-case (`auth.service.ts`, `login-form.component.ts`)
- **Classes**: PascalCase (`AuthService`, `LoginFormComponent`)
- **Methods**: camelCase (`getUser()`, `handleSubmit()`)
- **Observables**: End with `$` (`user$`, `loading$`)

#### TypeScript Safety

```typescript
// ✅ GOOD: Optional chaining and nullish coalescing
const userName = user?.name ?? 'Unknown';

// ❌ BAD: Potential null/undefined errors
const userName = user.name;
```

#### Component Structure

- **Smart Components**: Pages, containers (inject services)
- **Dumb Components**: Presentational (inputs/outputs only)
- **Standalone**: All components standalone (no modules)

#### Testing

- Test files: `*.spec.ts` alongside source
- Use Jasmine for assertions: `expect(value).toBe(expected)`
- Coverage target: ≥80%

---

## 🧪 Testing Requirements

### Backend Tests

#### Minimum Requirements

- [ ] All public functions have tests
- [ ] Coverage ≥80% per package
- [ ] Integration tests for HTTP handlers
- [ ] Mock external dependencies (OAuth, Google API, Redis)

#### Running Tests

```bash
cd backend

# All tests
go test ./...

# With coverage
go test -coverprofile=coverage.out ./...

# View coverage
go tool cover -func=coverage.out | grep total
# Must show: total: (statements) ≥80.0%
```

---

### Frontend Tests

#### Minimum Requirements

- [ ] All components have spec files
- [ ] Services have comprehensive tests
- [ ] Guards and interceptors tested
- [ ] E2E tests for critical flows
- [ ] Coverage ≥80%

#### Running Tests

```bash
cd frontend

# Unit tests
npm test

# E2E tests
npx playwright test

# Coverage
npm test -- --code-coverage
```

---

## 🎯 Pull Request Process

### 1. Before Creating PR

- [ ] Code compiles without errors
- [ ] All tests pass
- [ ] Coverage maintained (≥80%)
- [ ] Linter passes
- [ ] Documentation updated
- [ ] Commit messages follow convention

### 2. PR Title Format

```
<type>(<scope>): <description>

Examples:
feat(backend): add email notification service
fix(frontend): resolve dashboard loading state
docs(api): update authentication endpoints
chore(deps): update Go dependencies
```

### 3. PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] E2E tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings introduced
```

### 4. Review Process

- **Required approvals**: 1
- **Checks must pass**: Tests, linting, security scan
- **Merge strategy**: Squash and merge

---

## 📜 Commit Message Convention

### Format

```
<type>(<scope>): <subject>

<body (optional)>

<footer (optional)>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Build, deps, configs

### Scopes

- `backend`: Go backend code
- `frontend`: Angular frontend code
- `api`: API endpoints
- `auth`: Authentication system
- `dashboard`: Dashboard features
- `devcontainer`: Dev containers
- `deps`: Dependencies
- `ci`: CI/CD pipelines

### Examples

```bash
feat(backend): add role-based dashboard endpoints

Implement 4 dashboard endpoints (admin, coordinator, teacher, student)
with role-specific data filtering and mock/google mode support.

Closes #123

---

fix(frontend): resolve dashboard loading state bug

Dashboard was showing stale data when switching modes.
Now properly resets loading state on mode change.

---

docs(api): add complete API documentation

Create API_DOCUMENTATION.md with all endpoints,
request/response examples, and error codes.

---

chore(deps): update Go to 1.24.7

Update go.mod to require Go 1.24.7 for latest features
and security patches.
```

---

## 🏗️ Architecture Guidelines

### Backend: Hexagonal Architecture

- **Domain layer**: Pure Go, no external dependencies
- **Application layer**: Use cases, orchestration
- **Adapters**: HTTP, database, OAuth, APIs
- **Ports**: Interfaces defining contracts

**Rule**: Dependencies point inward (domain is innermost)

### Frontend: Feature Folders

- **Features**: Business capabilities (auth, dashboard, search)
- **Core**: Services, guards, models
- **Shared**: Reusable UI components

**Rule**: Features don't depend on each other, only on core/shared

---

## 🔐 Security Guidelines

### Never Commit

- [ ] Secrets, API keys, passwords
- [ ] .env files (use .env.example instead)
- [ ] Google credentials JSON
- [ ] JWT secrets
- [ ] Any PII (Personally Identifiable Information)

### Code Security

- Always validate user input
- Use parameterized queries (prevent SQL injection)
- Sanitize HTML output (prevent XSS)
- Implement rate limiting
- Use HTTPS in production
- Validate JWT on backend (never trust frontend)

---

## 📚 Resources

### Documentation
- [README](README.md) - Project overview
- [Architecture](ARCHITECTURE.md) - System design
- [API Documentation](API_DOCUMENTATION.md) - API reference
- [Backend README](backend/README.md) - Backend guide

### Learning
- [Go by Example](https://gobyexample.com/)
- [Angular Documentation](https://angular.dev)
- [Echo Framework](https://echo.labstack.com/)
- [TailwindCSS](https://tailwindcss.com/)

---

## ❓ Questions?

- Open an issue for bugs or feature requests
- Discussion tab for questions
- Check existing issues before creating new ones

---

**Thank you for contributing to ClassSphere!** 🎉

**Version**: 1.0  
**Last Updated**: 2025-10-08

