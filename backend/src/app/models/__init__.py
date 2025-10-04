"""
Model modules for the application.
"""
from .user import (
    UserRole,
    UserStatus,
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    UserProfile,
    UserStats,
    UserSearch
)

from .oauth import (
    TokenType,
    OAuthProvider,
    TokenStatus,
    OAuthTokenBase,
    OAuthTokenCreate,
    OAuthTokenUpdate,
    OAuthTokenResponse,
    OAuthTokenRefresh,
    OAuthAuthorization,
    OAuthTokenExchange,
    OAuthTokenValidation,
    OAuthTokenRevoke
)

from .course import (
    CourseStatus,
    CourseLevel,
    CourseBase,
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    CourseList,
    CourseSearch,
    CourseStats
)

from .assignment import (
    AssignmentType,
    AssignmentStatus,
    AssignmentBase,
    AssignmentCreate,
    AssignmentUpdate,
    AssignmentResponse,
    AssignmentList,
    AssignmentSearch,
    AssignmentStats
)

from .enrollment import (
    EnrollmentStatus,
    EnrollmentRole,
    EnrollmentBase,
    EnrollmentCreate,
    EnrollmentUpdate,
    EnrollmentResponse,
    EnrollmentList,
    EnrollmentSearch,
    EnrollmentStats,
    BulkEnrollment
)

from .submission import (
    SubmissionStatus,
    SubmissionType,
    SubmissionBase,
    SubmissionCreate,
    SubmissionUpdate,
    SubmissionResponse,
    SubmissionList,
    SubmissionSearch,
    SubmissionStats,
    BulkSubmission
)

__all__ = [
    # User models
    "UserRole",
    "UserStatus",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "UserProfile",
    "UserStats",
    "UserSearch",
    
    # OAuth models
    "TokenType",
    "OAuthProvider",
    "TokenStatus",
    "OAuthTokenBase",
    "OAuthTokenCreate",
    "OAuthTokenUpdate",
    "OAuthTokenResponse",
    "OAuthTokenRefresh",
    "OAuthAuthorization",
    "OAuthTokenExchange",
    "OAuthTokenValidation",
    "OAuthTokenRevoke",
    
    # Course models
    "CourseStatus",
    "CourseLevel",
    "CourseBase",
    "CourseCreate",
    "CourseUpdate",
    "CourseResponse",
    "CourseList",
    "CourseSearch",
    "CourseStats",
    
    # Assignment models
    "AssignmentType",
    "AssignmentStatus",
    "AssignmentBase",
    "AssignmentCreate",
    "AssignmentUpdate",
    "AssignmentResponse",
    "AssignmentList",
    "AssignmentSearch",
    "AssignmentStats",
    
    # Enrollment models
    "EnrollmentStatus",
    "EnrollmentRole",
    "EnrollmentBase",
    "EnrollmentCreate",
    "EnrollmentUpdate",
    "EnrollmentResponse",
    "EnrollmentList",
    "EnrollmentSearch",
    "EnrollmentStats",
    "BulkEnrollment",
    
    # Submission models
    "SubmissionStatus",
    "SubmissionType",
    "SubmissionBase",
    "SubmissionCreate",
    "SubmissionUpdate",
    "SubmissionResponse",
    "SubmissionList",
    "SubmissionSearch",
    "SubmissionStats",
    "BulkSubmission"
]