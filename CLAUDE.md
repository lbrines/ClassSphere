# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ClassSphere** is a comprehensive educational dashboard system integrating with Google Classroom. This is a full-stack project currently in **Phase 1 implementation** with TDD methodology, featuring a FastAPI backend and Next.js 15 frontend.

### Current Status
- **Phase 1 - Fundations**: 5/12 days completed (42% progress)
- **Backend**: FastAPI 0.104.1 running on port 8000 with JWT + OAuth 2.0
- **Frontend**: Next.js 15 + React 19 (updated from previous versions)
- **Testing**: 78 unit tests passing with 100% coverage

## Architecture Overview

### Technology Stack
**Backend:**
- Python 3.11.4 with FastAPI 0.104.1
- Pydantic v2 for validation
- JWT + OAuth 2.0 (Google) authentication
- Redis for caching (optional, degrades gracefully)
- pytest for testing

**Frontend:**
- Next.js 15 + React 19
- TypeScript 5.1.6
- Tailwind CSS 3.3.3
- **Testing Stack**: Vitest + React Testing Library + Playwright
- **Important**: Do NOT use Jest (incompatible with ESM and React 19)

### Key Architectural Principles
- **Port 8000 Standard**: All backend services run on port 8000
- **TDD Methodology**: Strict Test-Driven Development
- **Resilient Services**: Graceful degradation when external services fail
- **Google Classroom Integration**: Mock system for development, real API for production

## Development Commands

### Backend Commands
```bash
# Start backend server (always port 8000)
python -m uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --reload

# Or using the activated environment
PYTHONPATH=/path/to/backend/src python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/unit/test_auth_api.py::test_login_success
```

### Frontend Commands
```bash
# Install dependencies
pnpm install

# Start development server
pnpm dev

# Run tests (Vitest + React Testing Library)
pnpm test

# Run E2E tests (Playwright)
pnpm test:e2e

# Build for production
pnpm build

# Type checking
pnpm type-check

# Linting
pnpm lint
```

### Port Management
```bash
# Check port 8000 availability
netstat -tulpn | grep :8000

# Kill processes on port 8000 (if needed)
lsof -ti:8000 | xargs -r kill -9
```

## Project Structure

```
/
├── contracts/              # Project documentation and specifications
│   ├── principal/          # Main documentation files
│   └── extra/             # Best practices and guidelines
├── backend/               # Python FastAPI backend
│   ├── src/app/          # Source code
│   │   ├── api/endpoints/ # API route handlers
│   │   ├── services/      # Business logic services
│   │   ├── models/        # Data models
│   │   ├── core/          # Core configuration
│   │   └── middleware/    # Custom middleware
│   └── tests/            # Test files
└── frontend/             # Next.js 15 frontend
    ├── src/app/          # App router pages
    ├── src/components/   # Reusable components
    ├── src/hooks/        # Custom hooks
    ├── src/lib/          # Utility libraries
    └── tests/            # Test files
```

## Testing Strategy

### TDD Methodology
Follow strict Test-Driven Development:
1. **Red**: Write failing test
2. **Green**: Implement minimal code to pass
3. **Refactor**: Improve code while keeping tests green

### Coverage Requirements
- **Global**: ≥80% lines, ≥65% branches
- **Critical Modules**: ≥90% lines, ≥80% branches
- **Security Components**: ≥95% lines, ≥85% branches
- **API Endpoints**: 100% success and error cases

### Frontend Testing Rules
- **Use**: Vitest + React Testing Library + Playwright
- **DO NOT USE**: Jest (incompatible with Next.js 15 + React 19)
- **Migration**: Convert existing Jest tests to Vitest gradually

## API Endpoints

Current endpoints (Phase 1):
- `GET /` - Welcome endpoint
- `GET /health` - Health check
- `GET /info` - System information
- `POST /auth/login` - Traditional login
- `GET /auth/google` - Google OAuth initiation
- `GET /auth/google/callback` - Google OAuth callback
- `POST /auth/refresh` - Token refresh
- `GET /auth/me` - Current user info
- `POST /auth/logout` - Logout
- `GET /auth/verify` - Token verification

## Key Implementation Notes

### Error Prevention
- Services degrade gracefully when external dependencies fail
- Google Classroom API has mock fallback for development
- Redis is optional with in-memory fallback
- All critical paths have comprehensive error handling

### Context Management
- Services implement context-aware architecture for LLM development
- Chunking by priority (CRITICAL > HIGH > MEDIUM > LOW)
- Anti lost-in-the-middle patterns in service structure

### Security
- JWT tokens with configurable expiration
- OAuth 2.0 with Google (PKCE + State validation)
- Role-based access control (admin > coordinator > teacher > student)
- Rate limiting middleware

## Common Development Tasks

### Running the Full Stack
1. Start backend: `python -m uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --reload`
2. Start frontend: `pnpm dev` (usually runs on port 3000)
3. Access application at http://localhost:3000

### Adding New Features
1. Write tests first (TDD)
2. Implement backend endpoint if needed
3. Create frontend components
4. Add integration tests
5. Update documentation

### Debugging
- Backend logs are structured JSON
- Frontend uses console.log for development
- Check browser network tab for API issues
- Use React DevTools for component debugging

## Important Files
- `contracts/principal/00_ClassSphere_index.md` - Project overview and status
- `contracts/principal/05_ClassSphere_arquitectura.md` - Detailed architecture
- `contracts/principal/09_ClassSphere_testing.md` - Testing strategy
- `contracts/extra/TDD_BEST_PRACTICES.md` - TDD guidelines

## Phase Implementation Status

**Phase 1 (Current) - Fundations:**
- ✅ Backend authentication and core APIs
- ✅ Frontend base structure with Next.js 15
- ⏳ Role-based middleware (Day 6)
- ⏳ UI components and authentication forms (Day 7)
- ⏳ API services and error handling (Days 8-9)
- ⏳ Frontend-backend integration (Days 10-11)
- ⏳ CI/CD and documentation (Day 12)

Future phases will include Google Classroom integration, advanced visualizations, search functionality, and deployment automation.