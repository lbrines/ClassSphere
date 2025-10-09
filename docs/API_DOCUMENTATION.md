# ClassSphere API Documentation

## Base URL

```
http://localhost:8080/api/v1
```

## Authentication

Most endpoints require JWT authentication via Bearer token in the Authorization header:

```
Authorization: Bearer <jwt-token>
```

## Endpoints

### Health Check

**GET** `/health`

Returns server health status.

**Response:**
```json
{
  "status": "ok"
}
```

---

### Authentication

#### Login

**POST** `/auth/login`

Authenticate with email and password.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIs...",
  "expiresAt": "2025-10-09T12:00:00Z",
  "user": {
    "id": "user-123",
    "email": "user@example.com",
    "displayName": "John Doe",
    "role": "student"
  }
}
```

#### OAuth Start

**GET** `/auth/oauth/google`

Initiates Google OAuth flow.

**Response:**
```json
{
  "state": "random-state-token",
  "url": "https://accounts.google.com/o/oauth2/v2/auth?..."
}
```

#### OAuth Callback

**GET** `/auth/oauth/callback?code=...&state=...`

Completes OAuth flow.

**Response:** Same as login.

---

### User Management

#### Get Current User

**GET** `/users/me`

**Auth:** Required

Returns the authenticated user's profile.

**Response:**
```json
{
  "id": "user-123",
  "email": "user@example.com",
  "displayName": "John Doe",
  "role": "student",
  "createdAt": "2025-01-01T00:00:00Z",
  "updatedAt": "2025-10-08T12:00:00Z"
}
```

---

### Dashboards

#### Admin Dashboard

**GET** `/dashboard/admin`

**Auth:** Required (Admin only)

**Response:**
```json
{
  "role": "admin",
  "stats": {},
  "message": "Admin dashboard data"
}
```

#### Coordinator Dashboard

**GET** `/dashboard/coordinator`

**Auth:** Required (Coordinator only)

#### Teacher Dashboard

**GET** `/dashboard/teacher`

**Auth:** Required (Teacher only)

#### Student Dashboard

**GET** `/dashboard/student`

**Auth:** Required (Student only)

---

### Google Classroom Integration

#### List Courses

**GET** `/google/courses`

**Auth:** Required

Returns list of Google Classroom courses.

**Response:**
```json
{
  "courses": [
    {
      "id": "course-123",
      "name": "Mathematics 101",
      "section": "A",
      "enrollmentCode": "abc123"
    }
  ]
}
```

**GET** `/classroom/courses` (alias)

---

### Search (Phase 3)

#### Multi-Entity Search with Pagination

**GET** `/search?q={query}&entities={entities}&page={page}&limit={limit}`

**Auth:** Required

**Query Parameters:**
- `q` (string, required): Search query
- `entities` (string, required): Comma-separated entity types
  - Valid: `students`, `teachers`, `courses`, `assignments`, `announcements`
- `page` (int, optional, default=1): Page number (1-indexed)
- `limit` (int, optional, default=10): Results per page

**Example:**
```
GET /search?q=mathematics&entities=courses,assignments&page=1&limit=10
```

**Response:**
```json
{
  "query": "mathematics",
  "total": 25,
  "totalPages": 3,
  "page": 1,
  "pageSize": 10,
  "results": {
    "courses": [
      {
        "type": "courses",
        "id": "course-1",
        "title": "Mathematics 101",
        "description": "Introduction to Algebra",
        "relevance": 0.95
      }
    ],
    "assignments": [
      {
        "type": "assignments",
        "id": "assign-1",
        "title": "Math Homework 1",
        "description": "Solve problems 1-10",
        "relevance": 0.87,
        "meta": {
          "courseId": "course-1"
        }
      }
    ]
  }
}
```

**Role-Based Access Control:**
- Students: Can search courses, assignments, announcements (NOT students or teachers)
- Teachers: Can search all except announcements
- Coordinators: Can search teachers, courses, assignments, announcements (NOT students)
- Admins: Can search everything

---

### Real-time Notifications (Phase 3) - SSE

#### Notification Stream

**GET** `/notifications/stream`

**Auth:** Required (JWT via Authorization header)

**Protocol:** Server-Sent Events (SSE)

**Headers:**
```
Authorization: Bearer <jwt-token>
Accept: text/event-stream
```

**Response Stream:**
```
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive

event: connected
data: {"clientId":"abc-123","userId":"user-1"}

event: notification
data: {"id":"notif-1","title":"New Message","message":"You have a new message","type":"info","priority":"medium","timestamp":"2025-10-08T12:00:00Z"}

: keep-alive 2025-10-08T12:00:05Z
```

**Event Types:**
- `connected`: Initial connection confirmation
- `notification`: New notification for the user
- `: keep-alive`: Comment line to keep connection alive (every 15 seconds)

**Client Example (JavaScript):**
```javascript
const token = 'your-jwt-token';
const eventSource = new EventSource(`/api/v1/notifications/stream`, {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

// Note: Native EventSource doesn't support custom headers
// Use fetch + ReadableStream polyfill (see frontend implementation)

eventSource.addEventListener('connected', (event) => {
  const data = JSON.parse(event.data);
  console.log('Connected:', data);
});

eventSource.addEventListener('notification', (event) => {
  const notification = JSON.parse(event.data);
  console.log('New notification:', notification);
});

eventSource.onerror = (error) => {
  console.error('SSE error:', error);
  // Browser will automatically attempt reconnection
};
```

**Client Example (Fetch + ReadableStream):**
```javascript
const response = await fetch('/api/v1/notifications/stream', {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Accept': 'text/event-stream'
  }
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  
  const text = decoder.decode(value);
  // Parse SSE format: event: type\ndata: json\n\n
  console.log('Received:', text);
}
```

**Features:**
- Automatic reconnection (handled by browser)
- Keep-alive messages every 15 seconds
- JWT authentication via Authorization header
- Connection status monitoring
- Multiple simultaneous clients per user

**Advantages over WebSocket:**
- Simpler unidirectional server→client communication
- Better proxy/firewall compatibility (standard HTTP)
- Automatic reconnection (no manual implementation needed)
- Easier debugging (visible in browser Network tab)
- No ping/pong mechanism required

---

## Error Responses

All errors follow a standardized format:

```json
{
  "error": "Human readable error message",
  "code": "ERROR_CODE",
  "details": "Optional additional context",
  "requestId": "trace-id-123"
}
```

**Common Error Codes:**
- `BAD_REQUEST` (400): Invalid request parameters
- `UNAUTHORIZED` (401): Missing or invalid authentication
- `FORBIDDEN` (403): Insufficient permissions
- `NOT_FOUND` (404): Resource not found
- `INTERNAL_ERROR` (500): Server error

**Examples:**
```json
{
  "error": "entities parameter is required",
  "code": "BAD_REQUEST",
  "requestId": "req-456"
}
```

```json
{
  "error": "authentication required",
  "code": "UNAUTHORIZED",
  "requestId": "req-789"
}
```

---

## Rate Limiting

Currently not implemented. Future versions may include rate limiting per user/IP.

---

## Pagination

Endpoints that support pagination use the following pattern:

**Parameters:**
- `page` (int, optional, default=1): Page number (1-indexed)
- `limit` (int, optional, default=10): Results per page

**Response includes:**
- `page`: Current page number
- `pageSize`: Results per page
- `totalPages`: Total number of pages
- `total`: Total number of results

---

## Versioning

Current API version: `v1`

All endpoints are prefixed with `/api/v1/`

---

## Changelog

### Version 1.0 (Current)

**Phase 3 Updates:**
- ✅ Added: Multi-entity search with pagination (`/search`)
- ✅ Added: SSE for real-time notifications (`/notifications/stream`)
- ✅ Added: Centralized error handling with standardized responses
- ✅ Added: Request ID tracing in error responses
- ⚠️ Deprecated: WebSocket endpoint (`/ws/notifications`) - Removed
- ✅ Improved: RBAC for search (role-based filtering)

**Security Improvements:**
- Environment-based user seeding (production-safe)
- JWT authentication for SSE
- Centralized error handler with audit logging
- Request ID for error tracing

**Technical Improvements:**
- Error handler middleware with structured logging
- Pagination support in search
- SSE for simpler real-time communication
- Better proxy/firewall compatibility

---

## Support

For issues or questions, please refer to the project documentation or create an issue in the repository.
