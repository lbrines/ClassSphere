"""
Enrollment repository for MongoDB operations.
"""
from typing import Any, Dict, List, Optional
from datetime import datetime

from .base import BaseRepository
from src.app.models.enrollment import EnrollmentStatus, EnrollmentRole
from src.app.exceptions.base import NotFoundError, ConflictError


class EnrollmentRepository(BaseRepository):
    """Enrollment repository for MongoDB operations."""
    
    def __init__(self):
        super().__init__("enrollments")
    
    async def create_enrollment(self, enrollment_data: Dict[str, Any]) -> str:
        """Create a new enrollment."""
        # Check if enrollment already exists
        if await self.exists({
            'user_id': enrollment_data['user_id'],
            'course_id': enrollment_data['course_id']
        }):
            raise ConflictError(f"User {enrollment_data['user_id']} is already enrolled in course {enrollment_data['course_id']}")
        
        return await self.create(enrollment_data)
    
    async def get_enrollments_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get enrollments by user."""
        return await self.get_many(
            filter_dict={'user_id': user_id},
            skip=skip,
            limit=limit,
            sort=[('enrollment_date', -1)]
        )
    
    async def get_enrollments_by_course(self, course_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get enrollments by course."""
        return await self.get_many(
            filter_dict={'course_id': course_id},
            skip=skip,
            limit=limit,
            sort=[('enrollment_date', -1)]
        )
    
    async def get_enrollments_by_status(self, status: EnrollmentStatus, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get enrollments by status."""
        return await self.get_many(
            filter_dict={'status': status.value},
            skip=skip,
            limit=limit,
            sort=[('enrollment_date', -1)]
        )
    
    async def get_enrollments_by_role(self, role: EnrollmentRole, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get enrollments by role."""
        return await self.get_many(
            filter_dict={'role': role.value},
            skip=skip,
            limit=limit,
            sort=[('enrollment_date', -1)]
        )
    
    async def get_user_course_enrollment(self, user_id: str, course_id: str) -> Optional[Dict[str, Any]]:
        """Get specific user-course enrollment."""
        return await self.get_by_field('user_id', user_id) and await self.get_by_field('course_id', course_id)
    
    async def get_active_enrollments_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get active enrollments by user."""
        filter_dict = {
            'user_id': user_id,
            'status': EnrollmentStatus.ACTIVE.value
        }
        
        return await self.get_many(
            filter_dict=filter_dict,
            skip=skip,
            limit=limit,
            sort=[('enrollment_date', -1)]
        )
    
    async def get_active_enrollments_by_course(self, course_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get active enrollments by course."""
        filter_dict = {
            'course_id': course_id,
            'status': EnrollmentStatus.ACTIVE.value
        }
        
        return await self.get_many(
            filter_dict=filter_dict,
            skip=skip,
            limit=limit,
            sort=[('enrollment_date', -1)]
        )
    
    async def update_enrollment_status(self, enrollment_id: str, status: EnrollmentStatus) -> bool:
        """Update enrollment status."""
        update_data = {'status': status.value}
        
        if status == EnrollmentStatus.COMPLETED:
            update_data['completion_date'] = datetime.utcnow()
        
        return await self.update_by_id(enrollment_id, update_data)
    
    async def update_enrollment_role(self, enrollment_id: str, role: EnrollmentRole) -> bool:
        """Update enrollment role."""
        return await self.update_by_id(enrollment_id, {'role': role.value})
    
    async def update_enrollment_grade(self, enrollment_id: str, final_grade: float, credits_earned: int) -> bool:
        """Update enrollment final grade and credits."""
        return await self.update_by_id(enrollment_id, {
            'final_grade': final_grade,
            'credits_earned': credits_earned
        })
    
    async def get_enrollment_stats(self, enrollment_id: str) -> Dict[str, Any]:
        """Get enrollment statistics."""
        pipeline = [
            {'$match': {'_id': self._convert_to_object_id(enrollment_id)}},
            {'$lookup': {
                'from': 'assignments',
                'localField': 'course_id',
                'foreignField': 'course_id',
                'as': 'assignments'
            }},
            {'$lookup': {
                'from': 'submissions',
                'let': {'user_id': '$user_id', 'assignment_ids': '$assignments._id'},
                'pipeline': [
                    {'$match': {
                        '$expr': {
                            '$and': [
                                {'$eq': ['$student_id', '$$user_id']},
                                {'$in': ['$assignment_id', '$$assignment_ids']}
                            ]
                        }
                    }}
                ],
                'as': 'submissions'
            }},
            {'$project': {
                'enrollment_id': '$_id',
                'assignments_completed': {
                    '$size': {
                        '$filter': {
                            'input': '$submissions',
                            'cond': {'$ne': ['$$this.status', 'draft']}
                        }
                    }
                },
                'assignments_total': {'$size': '$assignments'},
                'average_grade': {'$avg': '$submissions.grade'}
            }}
        ]
        
        results = await self.aggregate(pipeline)
        return results[0] if results else {}
    
    async def get_enrollments_with_stats(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get enrollments with statistics."""
        pipeline = [
            {'$lookup': {
                'from': 'users',
                'localField': 'user_id',
                'foreignField': '_id',
                'as': 'user'
            }},
            {'$lookup': {
                'from': 'courses',
                'localField': 'course_id',
                'foreignField': '_id',
                'as': 'course'
            }},
            {'$lookup': {
                'from': 'assignments',
                'localField': 'course_id',
                'foreignField': 'course_id',
                'as': 'assignments'
            }},
            {'$lookup': {
                'from': 'submissions',
                'let': {'user_id': '$user_id', 'assignment_ids': '$assignments._id'},
                'pipeline': [
                    {'$match': {
                        '$expr': {
                            '$and': [
                                {'$eq': ['$student_id', '$$user_id']},
                                {'$in': ['$assignment_id', '$$assignment_ids']}
                            ]
                        }
                    }}
                ],
                'as': 'submissions'
            }},
            {'$addFields': {
                'user_name': {'$arrayElemAt': ['$user.name', 0]},
                'user_email': {'$arrayElemAt': ['$user.email', 0]},
                'course_title': {'$arrayElemAt': ['$course.title', 0]},
                'course_code': {'$arrayElemAt': ['$course.code', 0]},
                'assignments_completed': {
                    '$size': {
                        '$filter': {
                            'input': '$submissions',
                            'cond': {'$ne': ['$$this.status', 'draft']}
                        }
                    }
                },
                'assignments_total': {'$size': '$assignments'},
                'average_grade': {'$avg': '$submissions.grade'}
            }},
            {'$sort': {'enrollment_date': -1}},
            {'$skip': skip},
            {'$limit': limit}
        ]
        
        return await self.aggregate(pipeline)
    
    async def get_course_enrollment_stats(self, course_id: str) -> Dict[str, Any]:
        """Get course enrollment statistics."""
        pipeline = [
            {'$match': {'course_id': self._convert_to_object_id(course_id)}},
            {'$group': {
                '_id': '$status',
                'count': {'$sum': 1}
            }},
            {'$group': {
                '_id': None,
                'total_enrollments': {'$sum': '$count'},
                'status_counts': {
                    '$push': {
                        'status': '$_id',
                        'count': '$count'
                    }
                }
            }},
            {'$project': {
                'course_id': course_id,
                'total_enrollments': 1,
                'active_enrollments': {
                    '$let': {
                        'vars': {
                            'active': {
                                '$filter': {
                                    'input': '$status_counts',
                                    'cond': {'$eq': ['$$this.status', 'active']}
                                }
                            }
                        },
                        'in': {'$arrayElemAt': ['$$active.count', 0]}
                    }
                },
                'completed_enrollments': {
                    '$let': {
                        'vars': {
                            'completed': {
                                '$filter': {
                                    'input': '$status_counts',
                                    'cond': {'$eq': ['$$this.status', 'completed']}
                                }
                            }
                        },
                        'in': {'$arrayElemAt': ['$$completed.count', 0]}
                    }
                },
                'dropped_enrollments': {
                    '$let': {
                        'vars': {
                            'dropped': {
                                '$filter': {
                                    'input': '$status_counts',
                                    'cond': {'$eq': ['$$this.status', 'dropped']}
                                }
                            }
                        },
                        'in': {'$arrayElemAt': ['$$dropped.count', 0]}
                    }
                }
            }}
        ]
        
        results = await self.aggregate(pipeline)
        return results[0] if results else {}
    
    async def bulk_create_enrollments(self, enrollment_data_list: List[Dict[str, Any]]) -> List[str]:
        """Bulk create enrollments."""
        # Check for existing enrollments
        existing_enrollments = []
        for data in enrollment_data_list:
            if await self.exists({
                'user_id': data['user_id'],
                'course_id': data['course_id']
            }):
                existing_enrollments.append(f"User {data['user_id']} in course {data['course_id']}")
        
        if existing_enrollments:
            raise ConflictError(f"Some enrollments already exist: {', '.join(existing_enrollments)}")
        
        return await self.bulk_create(enrollment_data_list)
    
    async def bulk_update_status(self, enrollment_ids: List[str], status: EnrollmentStatus) -> int:
        """Bulk update enrollment status."""
        update_data = {'status': status.value}
        
        if status == EnrollmentStatus.COMPLETED:
            update_data['completion_date'] = datetime.utcnow()
        
        return await self.bulk_update(
            {'_id': {'$in': [self._convert_to_object_id(eid) for eid in enrollment_ids]}},
            update_data
        )
    
    async def create_enrollment_indexes(self) -> None:
        """Create enrollment-specific indexes."""
        indexes = [
            [('user_id', 1)],  # Index for user
            [('course_id', 1)],  # Index for course
            [('status', 1)],  # Index for status
            [('role', 1)],  # Index for role
            [('enrollment_date', -1)],  # Index for enrollment date
            [('completion_date', -1)],  # Index for completion date
            [('user_id', 1), ('course_id', 1)],  # Unique compound index
            [('course_id', 1), ('status', 1)],  # Compound index
            [('user_id', 1), ('status', 1)]  # Compound index
        ]
        
        await self.create_indexes(indexes)