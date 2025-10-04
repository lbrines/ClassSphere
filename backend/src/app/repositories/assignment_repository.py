"""
Assignment repository for MongoDB operations.
"""
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

from .base import BaseRepository
from src.app.models.assignment import AssignmentType, AssignmentStatus
from src.app.exceptions.base import NotFoundError, ConflictError


class AssignmentRepository(BaseRepository):
    """Assignment repository for MongoDB operations."""
    
    def __init__(self):
        super().__init__("assignments")
    
    async def create_assignment(self, assignment_data: Dict[str, Any]) -> str:
        """Create a new assignment."""
        return await self.create(assignment_data)
    
    async def get_assignments_by_course(self, course_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get assignments by course."""
        return await self.get_many(
            filter_dict={'course_id': course_id},
            skip=skip,
            limit=limit,
            sort=[('due_date', 1)]
        )
    
    async def get_assignments_by_instructor(self, instructor_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get assignments by instructor."""
        return await self.get_many(
            filter_dict={'instructor_id': instructor_id},
            skip=skip,
            limit=limit,
            sort=[('created_at', -1)]
        )
    
    async def get_assignments_by_type(self, assignment_type: AssignmentType, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get assignments by type."""
        return await self.get_many(
            filter_dict={'assignment_type': assignment_type.value},
            skip=skip,
            limit=limit,
            sort=[('due_date', 1)]
        )
    
    async def get_assignments_by_status(self, status: AssignmentStatus, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get assignments by status."""
        return await self.get_many(
            filter_dict={'status': status.value},
            skip=skip,
            limit=limit,
            sort=[('due_date', 1)]
        )
    
    async def get_upcoming_assignments(self, days_ahead: int = 7, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get assignments due within specified days."""
        future_date = datetime.utcnow() + timedelta(days=days_ahead)
        
        filter_dict = {
            'due_date': {'$lte': future_date},
            'status': {'$in': [AssignmentStatus.PUBLISHED.value, AssignmentStatus.DRAFT.value]}
        }
        
        return await self.get_many(
            filter_dict=filter_dict,
            skip=skip,
            limit=limit,
            sort=[('due_date', 1)]
        )
    
    async def get_overdue_assignments(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get overdue assignments."""
        filter_dict = {
            'due_date': {'$lt': datetime.utcnow()},
            'status': AssignmentStatus.PUBLISHED.value
        }
        
        return await self.get_many(
            filter_dict=filter_dict,
            skip=skip,
            limit=limit,
            sort=[('due_date', -1)]
        )
    
    async def search_assignments(self, query: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Search assignments by title or description."""
        filter_dict = {
            '$or': [
                {'title': {'$regex': query, '$options': 'i'}},
                {'description': {'$regex': query, '$options': 'i'}}
            ]
        }
        
        return await self.get_many(
            filter_dict=filter_dict,
            skip=skip,
            limit=limit,
            sort=[('due_date', 1)]
        )
    
    async def get_assignments_by_date_range(self, start_date: datetime, end_date: datetime, 
                                          skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get assignments within date range."""
        filter_dict = {
            'due_date': {'$gte': start_date, '$lte': end_date}
        }
        
        return await self.get_many(
            filter_dict=filter_dict,
            skip=skip,
            limit=limit,
            sort=[('due_date', 1)]
        )
    
    async def update_assignment_status(self, assignment_id: str, status: AssignmentStatus) -> bool:
        """Update assignment status."""
        return await self.update_by_id(assignment_id, {'status': status.value})
    
    async def update_assignment_due_date(self, assignment_id: str, due_date: datetime) -> bool:
        """Update assignment due date."""
        return await self.update_by_id(assignment_id, {'due_date': due_date})
    
    async def get_assignment_stats(self, assignment_id: str) -> Dict[str, Any]:
        """Get assignment statistics."""
        pipeline = [
            {'$match': {'_id': self._convert_to_object_id(assignment_id)}},
            {'$lookup': {
                'from': 'submissions',
                'localField': '_id',
                'foreignField': 'assignment_id',
                'as': 'submissions'
            }},
            {'$project': {
                'assignment_id': '$_id',
                'total_submissions': {'$size': '$submissions'},
                'on_time_submissions': {
                    '$size': {
                        '$filter': {
                            'input': '$submissions',
                            'cond': {'$eq': ['$$this.is_late', False]}
                        }
                    }
                },
                'late_submissions': {
                    '$size': {
                        '$filter': {
                            'input': '$submissions',
                            'cond': {'$eq': ['$$this.is_late', True]}
                        }
                    }
                },
                'graded_submissions': {
                    '$size': {
                        '$filter': {
                            'input': '$submissions',
                            'cond': {'$ne': ['$$this.grade', None]}
                        }
                    }
                },
                'average_grade': {
                    '$avg': '$submissions.grade'
                },
                'completion_rate': {
                    '$multiply': [
                        {'$divide': [
                            {'$size': {
                                '$filter': {
                                    'input': '$submissions',
                                    'cond': {'$ne': ['$$this.status', 'draft']}
                                }
                            }},
                            {'$size': '$submissions'}
                        ]},
                        100
                    ]
                }
            }}
        ]
        
        results = await self.aggregate(pipeline)
        return results[0] if results else {}
    
    async def get_assignments_with_stats(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get assignments with statistics."""
        pipeline = [
            {'$lookup': {
                'from': 'submissions',
                'localField': '_id',
                'foreignField': 'assignment_id',
                'as': 'submissions'
            }},
            {'$addFields': {
                'submission_count': {'$size': '$submissions'},
                'graded_count': {
                    '$size': {
                        '$filter': {
                            'input': '$submissions',
                            'cond': {'$ne': ['$$this.grade', None]}
                        }
                    }
                },
                'average_grade': {'$avg': '$submissions.grade'}
            }},
            {'$sort': {'created_at': -1}},
            {'$skip': skip},
            {'$limit': limit}
        ]
        
        return await self.aggregate(pipeline)
    
    async def get_assignments_by_points_range(self, min_points: float, max_points: float, 
                                            skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get assignments by points range."""
        filter_dict = {
            'max_points': {'$gte': min_points, '$lte': max_points}
        }
        
        return await self.get_many(
            filter_dict=filter_dict,
            skip=skip,
            limit=limit,
            sort=[('max_points', -1)]
        )
    
    async def get_late_assignments_by_course(self, course_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get late assignments for a specific course."""
        filter_dict = {
            'course_id': course_id,
            'due_date': {'$lt': datetime.utcnow()},
            'status': AssignmentStatus.PUBLISHED.value
        }
        
        return await self.get_many(
            filter_dict=filter_dict,
            skip=skip,
            limit=limit,
            sort=[('due_date', -1)]
        )
    
    async def bulk_update_status(self, assignment_ids: List[str], status: AssignmentStatus) -> int:
        """Bulk update assignment status."""
        return await self.bulk_update(
            {'_id': {'$in': [self._convert_to_object_id(aid) for aid in assignment_ids]}},
            {'status': status.value}
        )
    
    async def get_assignments_by_course_and_status(self, course_id: str, status: AssignmentStatus, 
                                                 skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get assignments by course and status."""
        filter_dict = {
            'course_id': course_id,
            'status': status.value
        }
        
        return await self.get_many(
            filter_dict=filter_dict,
            skip=skip,
            limit=limit,
            sort=[('due_date', 1)]
        )
    
    async def create_assignment_indexes(self) -> None:
        """Create assignment-specific indexes."""
        indexes = [
            [('course_id', 1)],  # Index for course
            [('instructor_id', 1)],  # Index for instructor
            [('assignment_type', 1)],  # Index for type
            [('status', 1)],  # Index for status
            [('due_date', 1)],  # Index for due date
            [('max_points', 1)],  # Index for points
            [('created_at', -1)],  # Index for creation date
            [('course_id', 1), ('status', 1)],  # Compound index
            [('course_id', 1), ('due_date', 1)],  # Compound index
            [('title', 'text'), ('description', 'text')]  # Text index for search
        ]
        
        await self.create_indexes(indexes)