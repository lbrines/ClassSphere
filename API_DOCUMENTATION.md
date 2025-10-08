# ClassSphere API Documentation

**Version**: 1.0  
**Base URL**: `http://localhost:8080/api/v1`  
**Authentication**: JWT Bearer Token

---

## 📋 Table of Contents

1. [Authentication](#authentication)
2. [User Management](#user-management)
3. [Google Classroom](#google-classroom)
4. [Dashboards](#dashboards)
5. [Error Responses](#error-responses)
6. [Rate Limiting](#rate-limiting)

---

## 🔐 Authentication

### POST /auth/login

Email/password authentication returning JWT token.

**Request**:
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "admin@classsphere.edu",
  "password": "admin123"
}
```

**Response** (200 OK):
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expiresAt": "2025-10-08T11:00:00Z",
  "user": {
    "id": "1",
    "name": "Admin User",
    "email": "admin@classsphere.edu",
    "role": "admin"
  }
}
```

**Errors**:
- `400 Bad Request` - Invalid request body
- `401 Unauthorized` - Invalid credentials

---

### GET /auth/oauth/google

Initiate Google OAuth 2.0 flow with PKCE and State.

**Request**:
```http
GET /api/v1/auth/oauth/google
```

**Response** (302 Redirect):
```
Location: https://accounts.google.com/o/oauth2/v2/auth?
  client_id=...
  &redirect_uri=http://localhost:4200/auth/callback
  &response_type=code
  &scope=openid+email+profile
  &state=<csrf-token>
  &code_challenge=<pkce-challenge>
  &code_challenge_method=S256
```

**PKCE Implementation**: Uses SHA256 code challenge for enhanced security.

---

### GET /auth/oauth/callback

OAuth callback handler that exchanges code for JWT.

**Request**:
```http
GET /api/v1/auth/oauth/callback?code=<auth-code>&state=<state-token>
```

**Response** (200 OK):
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expiresAt": "2025-10-08T11:00:00Z",
  "user": {
    "id": "google-123456",
    "name": "John Doe",
    "email": "john.doe@gmail.com",
    "role": "student"
  }
}
```

**Errors**:
- `400 Bad Request` - Missing code or state
- `401 Unauthorized` - Invalid state (CSRF)
- `500 Internal Server Error` - OAuth exchange failed

---

## 👤 User Management

### GET /users/me

Get current authenticated user profile.

**Authentication**: Required (JWT Bearer Token)

**Request**:
```http
GET /api/v1/users/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response** (200 OK):
```json
{
  "id": "1",
  "name": "Admin User",
  "email": "admin@classsphere.edu",
  "role": "admin"
}
```

**Errors**:
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - User not found

---

### GET /admin/ping

Admin-only test endpoint for RBAC verification.

**Authentication**: Required (JWT Bearer Token)  
**Authorization**: Admin role only

**Request**:
```http
GET /api/v1/admin/ping
Authorization: Bearer <admin-jwt-token>
```

**Response** (200 OK):
```json
{
  "message": "pong (admin access granted)"
}
```

**Errors**:
- `401 Unauthorized` - Missing token
- `403 Forbidden` - Non-admin user

---

## 🎓 Google Classroom

### GET /google/courses

List Google Classroom courses with analytics.

**Authentication**: Required  
**Modes**: Mock or Google (configurable)

**Request**:
```http
GET /api/v1/google/courses?mode=mock
Authorization: Bearer <jwt-token>
```

**Query Parameters**:
- `mode` (optional) - Force mode: `mock` or `google` (default: config)

**Response** (200 OK):
```json
{
  "mode": "mock",
  "generatedAt": "2025-10-08T10:00:00Z",
  "courses": [
    {
      "id": "course-001",
      "name": "Introduction to Programming",
      "section": "CS-101-A",
      "program": "Computer Science",
      "primaryTeacher": "Dr. Smith",
      "enrollment": 30,
      "completionRate": 85.5,
      "upcomingAssignments": 3,
      "lastActivity": "2025-10-07T15:30:00Z"
    }
  ],
  "availableModes": ["mock", "google"]
}
```

**Errors**:
- `401 Unauthorized` - Missing token
- `503 Service Unavailable` - Classroom integration not configured

---

## 📊 Dashboards

### GET /dashboard/admin

Admin dashboard with system-wide metrics.

**Authentication**: Required  
**Authorization**: Admin role only

**Request**:
```http
GET /api/v1/dashboard/admin?mode=mock
Authorization: Bearer <admin-jwt-token>
```

**Query Parameters**:
- `mode` (optional) - Data source: `mock` or `google`

**Response** (200 OK):
```json
{
  "role": "admin",
  "generatedAt": "2025-10-08T10:00:00Z",
  "mode": "mock",
  "summary": [
    {
      "label": "Total Courses",
      "value": 45,
      "format": "number",
      "trend": "up",
      "delta": 5
    },
    {
      "label": "Total Students",
      "value": 1250,
      "format": "number",
      "trend": "up",
      "delta": 50
    },
    {
      "label": "Avg Completion Rate",
      "value": 78.5,
      "format": "percentage",
      "trend": "up",
      "delta": 3.2
    }
  ],
  "charts": [
    {
      "id": "enrollment-trend",
      "title": "Enrollment Trend",
      "type": "line",
      "series": [...],
      "categories": [...]
    }
  ],
  "highlights": [...],
  "alerts": [...],
  "courses": [...]
}
```

**Errors**:
- `401 Unauthorized` - Missing token
- `403 Forbidden` - Non-admin user
- `503 Service Unavailable` - Classroom service not available

---

### GET /dashboard/coordinator

Coordinator dashboard with program-level metrics.

**Authentication**: Required  
**Authorization**: Coordinator or Admin

**Request**:
```http
GET /api/v1/dashboard/coordinator?mode=mock
Authorization: Bearer <coordinator-jwt-token>
```

**Response**: Similar structure to admin dashboard, filtered by coordinator's programs.

---

### GET /dashboard/teacher

Teacher dashboard with course-specific metrics.

**Authentication**: Required  
**Authorization**: Teacher, Coordinator, or Admin

**Request**:
```http
GET /api/v1/dashboard/teacher?mode=mock
Authorization: Bearer <teacher-jwt-token>
```

**Response**: Courses and students for the specific teacher.

---

### GET /dashboard/student

Student dashboard with personal progress.

**Authentication**: Required  
**Authorization**: Any authenticated user

**Request**:
```http
GET /api/v1/dashboard/student?mode=mock
Authorization: Bearer <student-jwt-token>
```

**Response**:
```json
{
  "role": "student",
  "generatedAt": "2025-10-08T10:00:00Z",
  "mode": "mock",
  "summary": [
    {
      "label": "Enrolled Courses",
      "value": 5,
      "format": "number"
    },
    {
      "label": "Completion Rate",
      "value": 92.3,
      "format": "percentage",
      "trend": "up",
      "delta": 5.1
    },
    {
      "label": "Pending Assignments",
      "value": 3,
      "format": "number"
    }
  ],
  "timeline": [
    {
      "id": "assignment-001",
      "title": "Final Project",
      "courseId": "CS-101-A",
      "dueDate": "2025-10-15T23:59:59Z",
      "status": "upcoming"
    }
  ]
}
```

---

## ⚠️ Error Responses

### Standard Error Format

```json
{
  "message": "Error description",
  "code": "ERROR_CODE"
}
```

### HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| `200` | OK | Successful request |
| `400` | Bad Request | Invalid request body or parameters |
| `401` | Unauthorized | Missing or invalid JWT token |
| `403` | Forbidden | Valid token but insufficient permissions |
| `404` | Not Found | Resource not found |
| `500` | Internal Server Error | Server-side error |
| `503` | Service Unavailable | Service not configured or down |

---

## ⏱️ Rate Limiting

### Limits per User

- **Authenticated endpoints**: 100 requests / 100 seconds
- **Public endpoints**: 20 requests / 60 seconds

### Headers

**Response headers**:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1696770000
```

**Rate limit exceeded** (429):
```json
{
  "message": "Rate limit exceeded. Try again in 45 seconds."
}
```

---

## 🔑 Authentication Headers

### Required Format

```http
Authorization: Bearer <jwt-token>
```

### Example

```bash
curl http://localhost:8080/api/v1/users/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### JWT Token Structure

```json
{
  "sub": "user-id",
  "email": "user@example.com",
  "role": "admin",
  "iss": "classsphere",
  "exp": 1696770000,
  "iat": 1696766400
}
```

---

## 📝 Request Examples

### Complete Authentication Flow

```bash
# 1. Login
TOKEN=$(curl -s -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@classsphere.edu","password":"admin123"}' \
  | jq -r '.accessToken')

# 2. Get user profile
curl http://localhost:8080/api/v1/users/me \
  -H "Authorization: Bearer $TOKEN"

# 3. Get courses
curl "http://localhost:8080/api/v1/google/courses?mode=mock" \
  -H "Authorization: Bearer $TOKEN"

# 4. Get dashboard
curl "http://localhost:8080/api/v1/dashboard/admin?mode=mock" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🧪 Testing Endpoints

### Health Check (No Auth)

```bash
curl http://localhost:8080/health
# Response: {"status":"ok"}
```

### Login Test

```bash
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teacher@classsphere.edu",
    "password": "teach123"
  }' | jq
```

### Protected Endpoint Test

```bash
# Get token first
TOKEN=$(curl -s -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@classsphere.edu","password":"admin123"}' \
  | jq -r '.accessToken')

# Use token
curl http://localhost:8080/api/v1/admin/ping \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🎨 Mode Selection

### Available Modes

| Mode | Description | Requirements |
|------|-------------|--------------|
| `mock` | Mock data generator | None (always available) |
| `google` | Real Google Classroom API | `GOOGLE_CREDENTIALS_FILE` configured |

### Query Parameter

All Google Classroom and Dashboard endpoints accept `?mode=` parameter:

```bash
# Force mock mode
curl "http://localhost:8080/api/v1/google/courses?mode=mock" \
  -H "Authorization: Bearer $TOKEN"

# Force google mode (if available)
curl "http://localhost:8080/api/v1/google/courses?mode=google" \
  -H "Authorization: Bearer $TOKEN"

# Use default (from CLASSROOM_MODE env var)
curl http://localhost:8080/api/v1/google/courses \
  -H "Authorization: Bearer $TOKEN"
```

---

## 📦 Response Models

### User Model

```typescript
interface User {
  id: string;
  name: string;
  email: string;
  role: "admin" | "coordinator" | "teacher" | "student";
}
```

### Course Overview Model

```typescript
interface CourseOverview {
  id: string;
  name: string;
  section: string;
  program: string;
  primaryTeacher: string;
  enrollment: number;
  completionRate: number;
  upcomingAssignments: number;
  lastActivity: string; // ISO 8601 datetime
}
```

### Dashboard Data Model

```typescript
interface DashboardData {
  role: string;
  generatedAt: string; // ISO 8601
  mode: string;
  summary: MetricSummary[];
  charts?: ChartConfig[];
  highlights?: Highlight[];
  alerts?: string[];
  courses?: CourseOverview[];
  timeline?: TimelineItem[];
}

interface MetricSummary {
  label: string;
  value: number;
  format: "number" | "percentage" | "currency";
  trend?: "up" | "down" | "stable";
  delta?: number;
}
```

---

## 🔒 Security

### CORS Configuration

**Allowed Origins**:
- `http://localhost:4200` (development)
- Production origins (configured via env)

**Allowed Methods**: GET, POST, PUT, DELETE, OPTIONS  
**Allowed Headers**: Authorization, Content-Type  
**Credentials**: Supported

### JWT Configuration

- **Algorithm**: HS256
- **Expiry**: 60 minutes (configurable)
- **Issuer**: classsphere
- **Secret**: Environment variable `JWT_SECRET` (min 32 chars)

### OAuth 2.0 Security

- **PKCE**: SHA256 code challenge
- **State Parameter**: CSRF protection
- **Scopes**: openid, email, profile

---

## 📚 Additional Resources

- **[Backend README](backend/README.md)** - Backend setup and development
- **[Architecture](ARCHITECTURE.md)** - System design and patterns
- **[Security](SECURITY.md)** - Detailed security protocols
- **[Testing](backend/TESTING.md)** - Testing strategy and examples

---

**Last Updated**: 2025-10-08  
**API Version**: 1.0  
**OpenAPI Spec**: (TODO: Generate from code)

