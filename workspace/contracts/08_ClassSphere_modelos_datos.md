---
title: "ClassSphere - Consolidated Data Models"
version: "4.0"
type: "documentation"
language: "English (Mandatory)"
date: "2025-10-07"
related_files:
  - "00_ClassSphere_index.md"
  - "07_ClassSphere_api_endpoints.md"
  - "09_ClassSphere_testing.md"
---

[← API Endpoints](07_ClassSphere_api_endpoints.md) | [Índice](00_ClassSphere_index.md) | [Siguiente → Estrategia de Testing](09_ClassSphere_testing.md)

# Modelos de Datos Consolidados

## Usuario (Stage 1)
```json
{
  "id": "user-001",
  "email": "user@classsphere.edu",
  "role": "Admin|Coordinator|Teacher|Student",
  "name": "Full Name",
  "active": true,
  "lastLogin": "2025-10-03T10:00:00Z",
  "authStatus": "AUTH_SUCCESS",
  "preferences": {
    "language": "en",
    "timezone": "UTC",
    "notifications": {
      "email": true,
      "push": true,
      "digest": "daily"
    },
    "accessibility": {
      "highContrast": false,
      "fontSize": "medium",
      "screenReader": false
    }
  },
  "oauth": {
    "google": {
      "connected": true,
      "scopes": ["classroom.courses", "classroom.rosters"],
      "lastSync": "2025-10-03T09:00:00Z",
      "status": "AUTH_SUCCESS"
    }
  }
}
```

## Curso Completo (Stage 2 + 4)
```json
{
  "id": "course-001",
  "googleId": "123456789",
  "name": "eCommerce Specialist",
  "section": "Section A",
  "description": "Complete eCommerce course",
  "ownerId": "teacher-001",
  "status": "COURSE_ACTIVE|COURSE_INACTIVE|COURSE_ARCHIVED",
  "enrollmentCode": "abc123",
  "students": ["student-001", "student-002"],
  "metrics": {
    "totalStudents": 150,
    "activeStudents": 142,
    "completionRate": 78.5,
    "averageGrade": 8.2,
    "engagementScore": 85.3
  },
  "syncStatus": {
    "lastSync": "2025-10-03T09:00:00Z",
    "status": "SYNC_COMPLETE|SYNC_PENDING|SYNC_ERROR",
    "conflicts": []
  },
  "createdAt": "2025-08-15T10:00:00Z",
  "updatedAt": "2025-10-03T09:00:00Z"
}
```

## Métrica Avanzada (Stage 3)
```json
{
  "id": "metric-001",
  "type": "engagement|risk|performance",
  "entityType": "student|course|program",
  "entityId": "student-001",
  "value": 85.3,
  "formula": {
    "type": "weighted_average",
    "components": [
      {"name": "participation", "weight": 0.4, "value": 90},
      {"name": "submission", "weight": 0.3, "value": 85},
      {"name": "resource_access", "weight": 0.3, "value": 80}
    ]
  },
  "thresholds": {
    "excellent": 90,
    "good": 70,
    "warning": 50,
    "critical": 30
  },
  "trends": {
    "direction": "improving|declining|stable",
    "change": 5.2,
    "period": "weekly"
  },
  "calculatedAt": "2025-10-03T10:00:00Z",
  "validUntil": "2025-10-03T16:00:00Z"
}
```

## Notificación (Stage 3)
```json
{
  "id": "notif-001",
  "userId": "teacher-001",
  "type": "alert|info|warning|success",
  "priority": "high|medium|low",
  "channel": "websocket|email|push",
  "title": "Student at Risk",
  "message": "John Smith needs attention",
  "data": {
    "studentId": "student-001",
    "courseId": "course-001",
    "riskScore": 0.75,
    "recommendation": "Contact student within 24 hours"
  },
  "actions": [
    {
      "label": "View Student",
      "type": "navigate",
      "url": "/students/student-001"
    },
    {
      "label": "Send Message",
      "type": "action",
      "action": "sendMessage"
    }
  ],
  "status": "NOTIF_READ|NOTIF_UNREAD",
  "deliveryStatus": "NOTIF_DELIVERED|NOTIF_FAILED",
  "createdAt": "2025-10-03T10:00:00Z",
  "expiresAt": "2025-10-10T10:00:00Z"
}
```

## Estado de Sincronización (Stage 4)
```json
{
  "id": "sync-001",
  "status": "SYNC_IDLE|SYNC_RUNNING|SYNC_COMPLETE|SYNC_ERROR",
  "type": "manual|scheduled|webhook",
  "startedAt": "2025-10-03T09:00:00Z",
  "completedAt": "2025-10-03T09:15:00Z",
  "progress": {
    "total": 150,
    "processed": 150,
    "succeeded": 145,
    "failed": 5,
    "percentComplete": 100
  },
  "entities": {
    "courses": {"total": 10, "synced": 10, "failed": 0},
    "students": {"total": 120, "synced": 118, "failed": 2},
    "assignments": {"total": 20, "synced": 17, "failed": 3}
  },
  "conflicts": [
    {
      "entityType": "assignment",
      "entityId": "assignment-123",
      "field": "dueDate",
      "sourceValue": "2025-10-15T23:59:59Z",
      "targetValue": "2025-10-20T23:59:59Z",
      "status": "CONFLICT_PENDING|CONFLICT_RESOLVED"
    }
  ],
  "errors": [
    {
      "entity": "student",
      "id": "student-045",
      "error": "API_RATE_LIMIT_EXCEEDED",
      "message": "Rate limit exceeded, retrying in 60 seconds",
      "timestamp": "2025-10-03T09:10:00Z"
    }
  ]
}
```

## Implementación en Backend

### Usuario (Pydantic v2)
```python
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

class UserRole(str, Enum):
    ADMIN = "Admin"
    COORDINATOR = "Coordinator"
    TEACHER = "Teacher"
    STUDENT = "Student"

class AuthStatus(str, Enum):
    SUCCESS = "AUTH_SUCCESS"
    PENDING = "AUTH_PENDING"
    FAILED = "AUTH_FAILED"

class NotificationPreferences(BaseModel):
    email: bool = True
    push: bool = True
    digest: str = "daily"  # daily, weekly, none
    
    model_config = ConfigDict(extra="ignore")

class AccessibilityPreferences(BaseModel):
    highContrast: bool = False
    fontSize: str = "medium"  # small, medium, large
    screenReader: bool = False
    
    model_config = ConfigDict(extra="ignore")

class UserPreferences(BaseModel):
    language: str = "en"
    timezone: str = "UTC"
    notifications: NotificationPreferences = NotificationPreferences()
    accessibility: AccessibilityPreferences = AccessibilityPreferences()
    
    model_config = ConfigDict(extra="ignore")

class OAuthGoogle(BaseModel):
    connected: bool = False
    scopes: List[str] = []
    lastSync: Optional[datetime] = None
    status: AuthStatus = AuthStatus.PENDING
    
    model_config = ConfigDict(extra="ignore")

class OAuth(BaseModel):
    google: OAuthGoogle = OAuthGoogle()
    
    model_config = ConfigDict(extra="ignore")

class User(BaseModel):
    id: str
    email: EmailStr
    role: UserRole
    name: str
    active: bool = True
    lastLogin: Optional[datetime] = None
    authStatus: AuthStatus = AuthStatus.PENDING
    preferences: UserPreferences = UserPreferences()
    oauth: OAuth = OAuth()
    
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "id": "user-001",
                "email": "user@classsphere.edu",
                "role": "Teacher",
                "name": "John Smith",
                "active": True
            }
        }
    )
```

### Curso (Pydantic v2)
```python
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

class CourseStatus(str, Enum):
    ACTIVE = "COURSE_ACTIVE"
    INACTIVE = "COURSE_INACTIVE"
    ARCHIVED = "COURSE_ARCHIVED"

class SyncStatus(str, Enum):
    COMPLETE = "SYNC_COMPLETE"
    PENDING = "SYNC_PENDING"
    ERROR = "SYNC_ERROR"

class CourseMetrics(BaseModel):
    totalStudents: int = 0
    activeStudents: int = 0
    completionRate: float = 0.0
    averageGrade: float = 0.0
    engagementScore: float = 0.0
    
    model_config = ConfigDict(extra="ignore")

class CourseSyncStatus(BaseModel):
    lastSync: Optional[datetime] = None
    status: SyncStatus = SyncStatus.PENDING
    conflicts: List[Dict[str, Any]] = []
    
    model_config = ConfigDict(extra="ignore")

class Course(BaseModel):
    id: str
    googleId: str
    name: str
    section: str
    description: Optional[str] = None
    ownerId: str
    status: CourseStatus = CourseStatus.ACTIVE
    enrollmentCode: Optional[str] = None
    students: List[str] = []
    metrics: CourseMetrics = CourseMetrics()
    syncStatus: CourseSyncStatus = CourseSyncStatus()
    createdAt: datetime
    updatedAt: datetime
    
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "id": "course-001",
                "googleId": "123456789",
                "name": "eCommerce Specialist",
                "section": "Section A",
                "ownerId": "teacher-001",
                "status": "COURSE_ACTIVE"
            }
        }
    )
```

## Implementación en Frontend

### Usuario (TypeScript)
```typescript
// types/user.types.ts
export enum UserRole {
  ADMIN = "Admin",
  COORDINATOR = "Coordinator",
  TEACHER = "Teacher",
  STUDENT = "Student"
}

export enum AuthStatus {
  SUCCESS = "AUTH_SUCCESS",
  PENDING = "AUTH_PENDING",
  FAILED = "AUTH_FAILED"
}

export interface NotificationPreferences {
  email: boolean;
  push: boolean;
  digest: "daily" | "weekly" | "none";
}

export interface AccessibilityPreferences {
  highContrast: boolean;
  fontSize: "small" | "medium" | "large";
  screenReader: boolean;
}

export interface UserPreferences {
  language: string;
  timezone: string;
  notifications: NotificationPreferences;
  accessibility: AccessibilityPreferences;
}

export interface OAuthGoogle {
  connected: boolean;
  scopes: string[];
  lastSync: string | null;
  status: AuthStatus;
}

export interface OAuth {
  google: OAuthGoogle;
}

export interface User {
  id: string;
  email: string;
  role: UserRole;
  name: string;
  active: boolean;
  lastLogin: string | null;
  authStatus: AuthStatus;
  preferences: UserPreferences;
  oauth: OAuth;
}
```

### Curso (TypeScript)
```typescript
// types/course.types.ts
export enum CourseStatus {
  ACTIVE = "COURSE_ACTIVE",
  INACTIVE = "COURSE_INACTIVE",
  ARCHIVED = "COURSE_ARCHIVED"
}

export enum SyncStatus {
  COMPLETE = "SYNC_COMPLETE",
  PENDING = "SYNC_PENDING",
  ERROR = "SYNC_ERROR"
}

export interface CourseMetrics {
  totalStudents: number;
  activeStudents: number;
  completionRate: number;
  averageGrade: number;
  engagementScore: number;
}

export interface CourseSyncStatus {
  lastSync: string | null;
  status: SyncStatus;
  conflicts: any[];
}

export interface Course {
  id: string;
  googleId: string;
  name: string;
  section: string;
  description?: string;
  ownerId: string;
  status: CourseStatus;
  enrollmentCode?: string;
  students: string[];
  metrics: CourseMetrics;
  syncStatus: CourseSyncStatus;
  createdAt: string;
  updatedAt: string;
}
```

## Referencias a Otros Documentos

- Para detalles sobre los endpoints API, consulte [API Endpoints](07_ClassSphere_api_endpoints.md).
- Para detalles sobre la estrategia de testing, consulte [Estrategia de Testing](09_ClassSphere_testing.md).
- Para detalles sobre el plan de implementación, consulte [Plan de Implementación](10_ClassSphere_plan_implementacion.md).

---

[← API Endpoints](07_ClassSphere_api_endpoints.md) | [Índice](00_ClassSphere_index.md) | [Siguiente → Estrategia de Testing](09_ClassSphere_testing.md)
