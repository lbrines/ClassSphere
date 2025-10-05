"""
Mock service for development and testing.
"""
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime


class MockService:
    """Mock service with degradation patterns."""

    def __init__(self):
        """Initialize mock service."""
        self.redis_available = True
        self.cache_data: Dict[str, Any] = {}

    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check with timeout protection.

        Returns:
            Health status dictionary
        """
        try:
            return await asyncio.wait_for(
                self._perform_health_check(),
                timeout=2.0
            )
        except asyncio.TimeoutError:
            return {
                "status": "timeout",
                "timestamp": datetime.utcnow().isoformat(),
                "checks": {
                    "database": "timeout",
                    "redis": "timeout",
                    "external_apis": "timeout"
                }
            }

    async def _perform_health_check(self) -> Dict[str, Any]:
        """Internal health check implementation."""
        # Simulate health checks
        await asyncio.sleep(0.1)  # Simulate processing time

        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "checks": {
                "database": "healthy",
                "redis": "healthy" if self.redis_available else "degraded",
                "external_apis": "healthy"
            }
        }

    async def get_from_cache(
        self,
        key: str,
        default: Optional[Any] = None
    ) -> Optional[Any]:
        """
        Get value from cache with degradation support.

        Args:
            key: Cache key
            default: Default value if key not found

        Returns:
            Cached value or default
        """
        try:
            if not self.redis_available:
                # Degraded mode: return default
                return default

            return await asyncio.wait_for(
                self._get_cache_internal(key, default),
                timeout=1.0
            )
        except asyncio.TimeoutError:
            # Graceful degradation
            return default

    async def _get_cache_internal(
        self,
        key: str,
        default: Optional[Any] = None
    ) -> Optional[Any]:
        """Internal cache get implementation."""
        await asyncio.sleep(0.05)  # Simulate cache access
        return self.cache_data.get(key, default)

    async def set_in_cache(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = None
    ) -> bool:
        """
        Set value in cache with degradation support.

        Args:
            key: Cache key
            value: Value to cache
            expire: Expiration time in seconds

        Returns:
            True if successful, False if degraded
        """
        try:
            if not self.redis_available:
                # Degraded mode: just store in memory
                self.cache_data[key] = value
                return False  # Indicate degraded mode

            return await asyncio.wait_for(
                self._set_cache_internal(key, value, expire),
                timeout=1.0
            )
        except asyncio.TimeoutError:
            # Graceful degradation
            self.cache_data[key] = value
            return False

    async def _set_cache_internal(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = None
    ) -> bool:
        """Internal cache set implementation."""
        await asyncio.sleep(0.05)  # Simulate cache write
        self.cache_data[key] = value
        return True

    async def get_mock_google_classroom_data(self) -> Dict[str, Any]:
        """
        Get mock Google Classroom data.

        Returns:
            Mock classroom data
        """
        try:
            return await asyncio.wait_for(
                self._generate_mock_classroom_data(),
                timeout=2.0
            )
        except asyncio.TimeoutError:
            return {"error": "Mock data generation timeout"}

    async def _generate_mock_classroom_data(self) -> Dict[str, Any]:
        """Generate mock Google Classroom data."""
        await asyncio.sleep(0.1)  # Simulate API call

        return {
            "courses": [
                {
                    "id": "course-001",
                    "name": "Introduction to Computer Science",
                    "section": "CS101-A",
                    "descriptionHeading": "Learn the fundamentals of programming",
                    "description": "This course covers basic programming concepts.",
                    "room": "Room 101",
                    "ownerId": "teacher-001",
                    "creationTime": "2024-01-15T09:00:00Z",
                    "updateTime": "2024-01-15T09:00:00Z",
                    "enrollmentCode": "abc123",
                    "courseState": "ACTIVE",
                    "alternateLink": "https://classroom.google.com/c/course-001",
                },
                {
                    "id": "course-002",
                    "name": "Advanced Mathematics",
                    "section": "MATH201-B",
                    "descriptionHeading": "Advanced mathematical concepts",
                    "description": "Covers calculus and linear algebra.",
                    "room": "Room 202",
                    "ownerId": "teacher-001",
                    "creationTime": "2024-01-15T10:00:00Z",
                    "updateTime": "2024-01-15T10:00:00Z",
                    "enrollmentCode": "def456",
                    "courseState": "ACTIVE",
                    "alternateLink": "https://classroom.google.com/c/course-002",
                }
            ],
            "students": [
                {
                    "courseId": "course-001",
                    "userId": "student-001",
                    "profile": {
                        "id": "student-001",
                        "name": {"fullName": "Jane Student"},
                        "emailAddress": "student@classsphere.edu",
                        "photoUrl": "https://example.com/photo.jpg"
                    }
                }
            ]
        }

    def simulate_redis_failure(self):
        """Simulate Redis failure for testing."""
        self.redis_available = False

    def restore_redis(self):
        """Restore Redis for testing."""
        self.redis_available = True