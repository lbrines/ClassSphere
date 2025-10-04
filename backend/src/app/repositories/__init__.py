"""
Repository modules for the application.
"""
from .base import BaseRepository
from .user_repository import UserRepository
from .course_repository import CourseRepository
from .assignment_repository import AssignmentRepository
from .enrollment_repository import EnrollmentRepository
from .submission_repository import SubmissionRepository

__all__ = [
    "BaseRepository",
    "UserRepository", 
    "CourseRepository",
    "AssignmentRepository",
    "EnrollmentRepository",
    "SubmissionRepository"
]