"""
Course repository for MongoDB operations.
"""
from typing import Any, Dict, List, Optional
from datetime import datetime

from .base import BaseRepository
from src.app.models.course import CourseStatus, CourseLevel
from src.app.exceptions.base import NotFoundError, ConflictError


class CourseRepository(BaseRepository):
    """Course repository for MongoDB operations."""
    
    def __init__(self):
        super().__init__("courses")
    
    async def create_course(self, course_data: Dict[str, Any]) -> str:
        """Create a new course."""
        # Check if course code already exists
        if await self.exists({'code': course_data['code']}):
            raise ConflictError(f"Course with code {course_data['code']} already exists")
        
        return await self.create(course_data)
    
    async def get_course_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        """Get course by code."""
        return await self.get_by_field('code', code.upper())
    
    async def get_courses_by_instructor(self, instructor_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get courses by instructor."""
        return await self.get_many(
            filter_dict={'instructor_id': instructor_id},
            skip=skip,
            limit=limit,
            sort=[('created_at', -1)]
        )
    
    async def get_courses_by_status(self, status: CourseStatus, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get courses by status."""
        return await self.get_many(
            filter_dict={'status': status.value},
            skip=skip,
            limit=limit,
            sort=[('created_at', -1)]
        )
    
    async def get_courses_by_level(self, level: CourseLevel, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get courses by level."""
        return await self.get_many(
            filter_dict={'level': level.value},
            skip=skip,
            limit=limit,
            sort=[('title', 1)]
        )
    
    async def get_courses_by_department(self, department: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get courses by department."""
        return await self.get_many(
            filter_dict={'department': department},
            skip=skip,
            limit=limit,
            sort=[('title', 1)]
        )
    
    async def search_courses(self, query: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Search courses by title or description."""
        filter_dict = {
            '$or': [
                {'title': {'$regex': query, '$options': 'i'}},
                {'description': {'$regex': query, '$options': 'i'}},
                {'code': {'$regex': query, '$options': 'i'}}
            ]
        }
        
        return await self.get_many(
            filter_dict=filter_dict,
            skip=skip,
            limit=limit,
            sort=[('title', 1)]
        )
    
    async def get_active_courses(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get active courses."""
        return await self.get_courses_by_status(CourseStatus.ACTIVE, skip, limit)
    
    async def get_courses_by_date_range(self, start_date: datetime, end_date: datetime, 
                                      skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get courses within date range."""
        filter_dict = {
            'start_date': {'$gte': start_date},
            'end_date': {'$lte': end_date}
        }
        
        return await self.get_many(
            filter_dict=filter_dict,
            skip=skip,
            limit=limit,
            sort=[('start_date', 1)]
        )
    
    async def update_course_status(self, course_id: str, status: CourseStatus) -> bool:
        """Update course status."""
        return await self.update_by_id(course_id, {'status': status.value})
    
    async def update_course_instructor(self, course_id: str, instructor_id: str) -> bool:
        """Update course instructor."""
        return await self.update_by_id(course_id, {'instructor_id': instructor_id})
    
    async def get_course_stats(self, course_id: str) -> Dict[str, Any]:
        """Get course statistics."""
        pipeline = [
            {'$match': {'_id': self._convert_to_object_id(course_id)}},
            {'$lookup': {
                'from': 'enrollments',
                'localField': '_id',
                'foreignField': 'course_id',
                'as': 'enrollments'
            }},
            {'$lookup': {
                'from': 'assignments',
                'localField': '_id',
                'foreignField': 'course_id',
                'as': 'assignments'
            }},
            {'$project': {
                'course_id': '$_id',
                'total_students': {'$size': '$enrollments'},
                'active_students': {
                    '$size': {
                        '$filter': {
                            'input': '$enrollments',
                            'cond': {'$eq': ['$$this.status', 'active']}
                        }
                    }
                },
                'completed_assignments': {'$size': '$assignments'},
                'average_grade': {
                    '$avg': '$assignments.average_grade'
                },
                'completion_rate': {
                    '$multiply': [
                        {'$divide': [
                            {'$size': {
                                '$filter': {
                                    'input': '$enrollments',
                                    'cond': {'$eq': ['$$this.status', 'completed']}
                                }
                            }},
                            {'$size': '$enrollments'}
                        ]},
                        100
                    ]
                }
            }}
        ]
        
        results = await self.aggregate(pipeline)
        return results[0] if results else {}
    
    async def get_courses_with_stats(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get courses with statistics."""
        pipeline = [
            {'$lookup': {
                'from': 'enrollments',
                'localField': '_id',
                'foreignField': 'course_id',
                'as': 'enrollments'
            }},
            {'$lookup': {
                'from': 'assignments',
                'localField': '_id',
                'foreignField': 'course_id',
                'as': 'assignments'
            }},
            {'$addFields': {
                'student_count': {'$size': '$enrollments'},
                'assignment_count': {'$size': '$assignments'}
            }},
            {'$sort': {'created_at': -1}},
            {'$skip': skip},
            {'$limit': limit}
        ]
        
        return await self.aggregate(pipeline)
    
    async def get_popular_courses(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most popular courses by enrollment count."""
        pipeline = [
            {'$lookup': {
                'from': 'enrollments',
                'localField': '_id',
                'foreignField': 'course_id',
                'as': 'enrollments'
            }},
            {'$addFields': {
                'enrollment_count': {'$size': '$enrollments'}
            }},
            {'$sort': {'enrollment_count': -1}},
            {'$limit': limit}
        ]
        
        return await self.aggregate(pipeline)
    
    async def get_courses_by_credits(self, credits: int, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get courses by credits."""
        return await self.get_many(
            filter_dict={'credits': credits},
            skip=skip,
            limit=limit,
            sort=[('title', 1)]
        )
    
    async def bulk_update_status(self, course_ids: List[str], status: CourseStatus) -> int:
        """Bulk update course status."""
        return await self.bulk_update(
            {'_id': {'$in': [self._convert_to_object_id(cid) for cid in course_ids]}},
            {'status': status.value}
        )
    
    async def create_course_indexes(self) -> None:
        """Create course-specific indexes."""
        indexes = [
            [('code', 1)],  # Unique index for course code
            [('instructor_id', 1)],  # Index for instructor
            [('status', 1)],  # Index for status
            [('level', 1)],  # Index for level
            [('department', 1)],  # Index for department
            [('credits', 1)],  # Index for credits
            [('start_date', 1)],  # Index for start date
            [('end_date', 1)],  # Index for end date
            [('created_at', -1)],  # Index for creation date
            [('title', 'text'), ('description', 'text'), ('code', 'text')]  # Text index for search
        ]
        
        await self.create_indexes(indexes)