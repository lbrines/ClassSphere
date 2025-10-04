"""
Submission repository for MongoDB operations.
"""
from typing import Any, Dict, List, Optional
from datetime import datetime

from .base import BaseRepository
from src.app.models.submission import SubmissionStatus, SubmissionType
from src.app.exceptions.base import NotFoundError, ConflictError


class SubmissionRepository(BaseRepository):
    """Submission repository for MongoDB operations."""
    
    def __init__(self):
        super().__init__("submissions")
    
    async def create_submission(self, submission_data: Dict[str, Any]) -> str:
        """Create a new submission."""
        # Check if submission already exists for this assignment and student
        if await self.exists({
            'assignment_id': submission_data['assignment_id'],
            'student_id': submission_data['student_id']
        }):
            raise ConflictError(f"Student {submission_data['student_id']} already has a submission for assignment {submission_data['assignment_id']}")
        
        return await self.create(submission_data)
    
    async def get_submissions_by_assignment(self, assignment_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get submissions by assignment."""
        return await self.get_many(
            filter_dict={'assignment_id': assignment_id},
            skip=skip,
            limit=limit,
            sort=[('submitted_at', -1)]
        )
    
    async def get_submissions_by_student(self, student_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get submissions by student."""
        return await self.get_many(
            filter_dict={'student_id': student_id},
            skip=skip,
            limit=limit,
            sort=[('submitted_at', -1)]
        )
    
    async def get_submissions_by_status(self, status: SubmissionStatus, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get submissions by status."""
        return await self.get_many(
            filter_dict={'status': status.value},
            skip=skip,
            limit=limit,
            sort=[('submitted_at', -1)]
        )
    
    async def get_submissions_by_type(self, submission_type: SubmissionType, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get submissions by type."""
        return await self.get_many(
            filter_dict={'submission_type': submission_type.value},
            skip=skip,
            limit=limit,
            sort=[('submitted_at', -1)]
        )
    
    async def get_student_assignment_submission(self, student_id: str, assignment_id: str) -> Optional[Dict[str, Any]]:
        """Get specific student-assignment submission."""
        filter_dict = {
            'student_id': student_id,
            'assignment_id': assignment_id
        }
        
        return await self.get_by_field('student_id', student_id) and await self.get_by_field('assignment_id', assignment_id)
    
    async def get_late_submissions(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get late submissions."""
        filter_dict = {'is_late': True}
        
        return await self.get_many(
            filter_dict=filter_dict,
            skip=skip,
            limit=limit,
            sort=[('submitted_at', -1)]
        )
    
    async def get_graded_submissions(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get graded submissions."""
        filter_dict = {'grade': {'$ne': None}}
        
        return await self.get_many(
            filter_dict=filter_dict,
            skip=skip,
            limit=limit,
            sort=[('graded_at', -1)]
        )
    
    async def get_ungraded_submissions(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get ungraded submissions."""
        filter_dict = {'grade': None}
        
        return await self.get_many(
            filter_dict=filter_dict,
            skip=skip,
            limit=limit,
            sort=[('submitted_at', 1)]
        )
    
    async def update_submission_status(self, submission_id: str, status: SubmissionStatus) -> bool:
        """Update submission status."""
        update_data = {'status': status.value}
        
        if status == SubmissionStatus.SUBMITTED:
            update_data['submitted_at'] = datetime.utcnow()
        
        return await self.update_by_id(submission_id, update_data)
    
    async def grade_submission(self, submission_id: str, grade: float, feedback: str, graded_by: str) -> bool:
        """Grade a submission."""
        return await self.update_by_id(submission_id, {
            'grade': grade,
            'feedback': feedback,
            'graded_by': graded_by,
            'graded_at': datetime.utcnow(),
            'status': SubmissionStatus.GRADED.value
        })
    
    async def get_submission_stats(self, submission_id: str) -> Dict[str, Any]:
        """Get submission statistics."""
        pipeline = [
            {'$match': {'_id': self._convert_to_object_id(submission_id)}},
            {'$lookup': {
                'from': 'assignments',
                'localField': 'assignment_id',
                'foreignField': '_id',
                'as': 'assignment'
            }},
            {'$lookup': {
                'from': 'users',
                'localField': 'student_id',
                'foreignField': '_id',
                'as': 'student'
            }},
            {'$project': {
                'submission_id': '$_id',
                'assignment_title': {'$arrayElemAt': ['$assignment.title', 0]},
                'assignment_due_date': {'$arrayElemAt': ['$assignment.due_date', 0]},
                'student_name': {'$arrayElemAt': ['$student.name', 0]},
                'student_email': {'$arrayElemAt': ['$student.email', 0]},
                'percentage': {
                    '$multiply': [
                        {'$divide': ['$grade', {'$arrayElemAt': ['$assignment.max_points', 0]}]},
                        100
                    ]
                },
                'final_grade': {
                    '$cond': {
                        'if': {'$and': ['$is_late', {'$ne': ['$late_penalty', None]}]},
                        'then': {
                            '$multiply': [
                                '$grade',
                                {'$divide': [{'$subtract': [100, '$late_penalty']}, 100]}
                            ]
                        },
                        'else': '$grade'
                    }
                }
            }}
        ]
        
        results = await self.aggregate(pipeline)
        return results[0] if results else {}
    
    async def get_submissions_with_stats(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get submissions with statistics."""
        pipeline = [
            {'$lookup': {
                'from': 'assignments',
                'localField': 'assignment_id',
                'foreignField': '_id',
                'as': 'assignment'
            }},
            {'$lookup': {
                'from': 'users',
                'localField': 'student_id',
                'foreignField': '_id',
                'as': 'student'
            }},
            {'$addFields': {
                'assignment_title': {'$arrayElemAt': ['$assignment.title', 0]},
                'assignment_due_date': {'$arrayElemAt': ['$assignment.due_date', 0]},
                'student_name': {'$arrayElemAt': ['$student.name', 0]},
                'student_email': {'$arrayElemAt': ['$student.email', 0]},
                'percentage': {
                    '$multiply': [
                        {'$divide': ['$grade', {'$arrayElemAt': ['$assignment.max_points', 0]}]},
                        100
                    ]
                },
                'final_grade': {
                    '$cond': {
                        'if': {'$and': ['$is_late', {'$ne': ['$late_penalty', None]}]},
                        'then': {
                            '$multiply': [
                                '$grade',
                                {'$divide': [{'$subtract': [100, '$late_penalty']}, 100]}
                            ]
                        },
                        'else': '$grade'
                    }
                }
            }},
            {'$sort': {'submitted_at': -1}},
            {'$skip': skip},
            {'$limit': limit}
        ]
        
        return await self.aggregate(pipeline)
    
    async def get_assignment_submission_stats(self, assignment_id: str) -> Dict[str, Any]:
        """Get assignment submission statistics."""
        pipeline = [
            {'$match': {'assignment_id': self._convert_to_object_id(assignment_id)}},
            {'$group': {
                '_id': None,
                'total_submissions': {'$sum': 1},
                'submitted_submissions': {
                    '$sum': {
                        '$cond': [
                            {'$ne': ['$status', 'draft']},
                            1,
                            0
                        ]
                    }
                },
                'late_submissions': {
                    '$sum': {
                        '$cond': ['$is_late', 1, 0]
                    }
                },
                'graded_submissions': {
                    '$sum': {
                        '$cond': [
                            {'$ne': ['$grade', None]},
                            1,
                            0
                        ]
                    }
                },
                'average_grade': {'$avg': '$grade'}
            }},
            {'$project': {
                'assignment_id': assignment_id,
                'total_submissions': 1,
                'submitted_submissions': 1,
                'late_submissions': 1,
                'graded_submissions': 1,
                'average_grade': 1,
                'completion_rate': {
                    '$multiply': [
                        {'$divide': ['$submitted_submissions', '$total_submissions']},
                        100
                    ]
                }
            }}
        ]
        
        results = await self.aggregate(pipeline)
        return results[0] if results else {}
    
    async def get_student_submission_stats(self, student_id: str) -> Dict[str, Any]:
        """Get student submission statistics."""
        pipeline = [
            {'$match': {'student_id': self._convert_to_object_id(student_id)}},
            {'$group': {
                '_id': None,
                'total_submissions': {'$sum': 1},
                'submitted_submissions': {
                    '$sum': {
                        '$cond': [
                            {'$ne': ['$status', 'draft']},
                            1,
                            0
                        ]
                    }
                },
                'late_submissions': {
                    '$sum': {
                        '$cond': ['$is_late', 1, 0]
                    }
                },
                'graded_submissions': {
                    '$sum': {
                        '$cond': [
                            {'$ne': ['$grade', None]},
                            1,
                            0
                        ]
                    }
                },
                'average_grade': {'$avg': '$grade'}
            }},
            {'$project': {
                'student_id': student_id,
                'total_submissions': 1,
                'submitted_submissions': 1,
                'late_submissions': 1,
                'graded_submissions': 1,
                'average_grade': 1,
                'completion_rate': {
                    '$multiply': [
                        {'$divide': ['$submitted_submissions', '$total_submissions']},
                        100
                    ]
                }
            }}
        ]
        
        results = await self.aggregate(pipeline)
        return results[0] if results else {}
    
    async def get_submissions_by_date_range(self, start_date: datetime, end_date: datetime, 
                                          skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get submissions within date range."""
        filter_dict = {
            'submitted_at': {'$gte': start_date, '$lte': end_date}
        }
        
        return await self.get_many(
            filter_dict=filter_dict,
            skip=skip,
            limit=limit,
            sort=[('submitted_at', -1)]
        )
    
    async def bulk_grade_submissions(self, submission_ids: List[str], grade: float, feedback: str, graded_by: str) -> int:
        """Bulk grade submissions."""
        return await self.bulk_update(
            {'_id': {'$in': [self._convert_to_object_id(sid) for sid in submission_ids]}},
            {
                'grade': grade,
                'feedback': feedback,
                'graded_by': graded_by,
                'graded_at': datetime.utcnow(),
                'status': SubmissionStatus.GRADED.value
            }
        )
    
    async def bulk_create_submissions(self, submission_data_list: List[Dict[str, Any]]) -> List[str]:
        """Bulk create submissions."""
        # Check for existing submissions
        existing_submissions = []
        for data in submission_data_list:
            if await self.exists({
                'assignment_id': data['assignment_id'],
                'student_id': data['student_id']
            }):
                existing_submissions.append(f"Student {data['student_id']} in assignment {data['assignment_id']}")
        
        if existing_submissions:
            raise ConflictError(f"Some submissions already exist: {', '.join(existing_submissions)}")
        
        return await self.bulk_create(submission_data_list)
    
    async def create_submission_indexes(self) -> None:
        """Create submission-specific indexes."""
        indexes = [
            [('assignment_id', 1)],  # Index for assignment
            [('student_id', 1)],  # Index for student
            [('status', 1)],  # Index for status
            [('submission_type', 1)],  # Index for type
            [('submitted_at', -1)],  # Index for submission date
            [('graded_at', -1)],  # Index for grading date
            [('is_late', 1)],  # Index for late submissions
            [('grade', 1)],  # Index for grade
            [('assignment_id', 1), ('student_id', 1)],  # Unique compound index
            [('student_id', 1), ('status', 1)],  # Compound index
            [('assignment_id', 1), ('status', 1)]  # Compound index
        ]
        
        await self.create_indexes(indexes)