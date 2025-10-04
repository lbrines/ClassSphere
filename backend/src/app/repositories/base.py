"""
Base repository class for MongoDB operations.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar, Generic
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from bson import ObjectId
from pydantic import BaseModel
from loguru import logger

from src.app.core.database import get_database
from src.app.exceptions.base import DatabaseError, NotFoundError

T = TypeVar('T', bound=BaseModel)


class BaseRepository(ABC, Generic[T]):
    """Base repository class for MongoDB operations."""
    
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self._db: Optional[AsyncIOMotorDatabase] = None
        self._collection: Optional[AsyncIOMotorCollection] = None
    
    async def _get_collection(self) -> AsyncIOMotorCollection:
        """Get MongoDB collection."""
        if self._collection is None:
            self._db = await get_database()
            self._collection = self._db[self.collection_name]
        return self._collection
    
    def _convert_to_object_id(self, id_value: str) -> ObjectId:
        """Convert string ID to ObjectId."""
        try:
            return ObjectId(id_value)
        except Exception as e:
            logger.error(f"Invalid ObjectId format: {id_value}")
            raise ValueError(f"Invalid ID format: {id_value}")
    
    def _convert_from_object_id(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Convert ObjectId to string in document."""
        if doc and '_id' in doc:
            doc['id'] = str(doc['_id'])
            del doc['_id']
        return doc
    
    async def create(self, data: Dict[str, Any]) -> str:
        """Create a new document."""
        try:
            collection = await self._get_collection()
            
            # Add timestamps
            now = datetime.utcnow()
            data['created_at'] = now
            data['updated_at'] = now
            
            result = await collection.insert_one(data)
            logger.info(f"Created document in {self.collection_name} with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error creating document in {self.collection_name}: {e}")
            raise DatabaseError(f"Failed to create document: {str(e)}")
    
    async def get_by_id(self, id_value: str) -> Optional[Dict[str, Any]]:
        """Get document by ID."""
        try:
            collection = await self._get_collection()
            object_id = self._convert_to_object_id(id_value)
            
            doc = await collection.find_one({'_id': object_id})
            if doc:
                return self._convert_from_object_id(doc)
            return None
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error getting document by ID from {self.collection_name}: {e}")
            raise DatabaseError(f"Failed to get document: {str(e)}")
    
    async def get_by_field(self, field: str, value: Any) -> Optional[Dict[str, Any]]:
        """Get document by field value."""
        try:
            collection = await self._get_collection()
            
            doc = await collection.find_one({field: value})
            if doc:
                return self._convert_from_object_id(doc)
            return None
        except Exception as e:
            logger.error(f"Error getting document by field from {self.collection_name}: {e}")
            raise DatabaseError(f"Failed to get document: {str(e)}")
    
    async def get_many(self, filter_dict: Optional[Dict[str, Any]] = None, 
                      skip: int = 0, limit: int = 100, 
                      sort: Optional[List[tuple]] = None) -> List[Dict[str, Any]]:
        """Get multiple documents."""
        try:
            collection = await self._get_collection()
            
            # Build query
            query = filter_dict or {}
            
            # Build cursor
            cursor = collection.find(query)
            
            # Apply sorting
            if sort:
                cursor = cursor.sort(sort)
            
            # Apply pagination
            cursor = cursor.skip(skip).limit(limit)
            
            # Execute query
            docs = await cursor.to_list(length=limit)
            
            # Convert ObjectIds
            return [self._convert_from_object_id(doc) for doc in docs]
        except Exception as e:
            logger.error(f"Error getting documents from {self.collection_name}: {e}")
            raise DatabaseError(f"Failed to get documents: {str(e)}")
    
    async def update_by_id(self, id_value: str, update_data: Dict[str, Any]) -> bool:
        """Update document by ID."""
        try:
            collection = await self._get_collection()
            object_id = self._convert_to_object_id(id_value)
            
            # Add update timestamp
            update_data['updated_at'] = datetime.utcnow()
            
            result = await collection.update_one(
                {'_id': object_id},
                {'$set': update_data}
            )
            
            if result.matched_count == 0:
                return False
            
            logger.info(f"Updated document in {self.collection_name} with ID: {id_value}")
            return True
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error updating document in {self.collection_name}: {e}")
            raise DatabaseError(f"Failed to update document: {str(e)}")
    
    async def delete_by_id(self, id_value: str) -> bool:
        """Delete document by ID."""
        try:
            collection = await self._get_collection()
            object_id = self._convert_to_object_id(id_value)
            
            result = await collection.delete_one({'_id': object_id})
            
            if result.deleted_count == 0:
                return False
            
            logger.info(f"Deleted document from {self.collection_name} with ID: {id_value}")
            return True
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error deleting document from {self.collection_name}: {e}")
            raise DatabaseError(f"Failed to delete document: {str(e)}")
    
    async def count(self, filter_dict: Optional[Dict[str, Any]] = None) -> int:
        """Count documents matching filter."""
        try:
            collection = await self._get_collection()
            query = filter_dict or {}
            return await collection.count_documents(query)
        except Exception as e:
            logger.error(f"Error counting documents in {self.collection_name}: {e}")
            raise DatabaseError(f"Failed to count documents: {str(e)}")
    
    async def exists(self, filter_dict: Dict[str, Any]) -> bool:
        """Check if document exists."""
        try:
            collection = await self._get_collection()
            doc = await collection.find_one(filter_dict, {'_id': 1})
            return doc is not None
        except Exception as e:
            logger.error(f"Error checking document existence in {self.collection_name}: {e}")
            raise DatabaseError(f"Failed to check document existence: {str(e)}")
    
    async def bulk_create(self, data_list: List[Dict[str, Any]]) -> List[str]:
        """Create multiple documents."""
        try:
            collection = await self._get_collection()
            
            # Add timestamps
            now = datetime.utcnow()
            for data in data_list:
                data['created_at'] = now
                data['updated_at'] = now
            
            result = await collection.insert_many(data_list)
            logger.info(f"Created {len(result.inserted_ids)} documents in {self.collection_name}")
            return [str(id_val) for id_val in result.inserted_ids]
        except Exception as e:
            logger.error(f"Error bulk creating documents in {self.collection_name}: {e}")
            raise DatabaseError(f"Failed to bulk create documents: {str(e)}")
    
    async def bulk_update(self, filter_dict: Dict[str, Any], update_data: Dict[str, Any]) -> int:
        """Update multiple documents."""
        try:
            collection = await self._get_collection()
            
            # Add update timestamp
            update_data['updated_at'] = datetime.utcnow()
            
            result = await collection.update_many(
                filter_dict,
                {'$set': update_data}
            )
            
            logger.info(f"Updated {result.modified_count} documents in {self.collection_name}")
            return result.modified_count
        except Exception as e:
            logger.error(f"Error bulk updating documents in {self.collection_name}: {e}")
            raise DatabaseError(f"Failed to bulk update documents: {str(e)}")
    
    async def bulk_delete(self, filter_dict: Dict[str, Any]) -> int:
        """Delete multiple documents."""
        try:
            collection = await self._get_collection()
            
            result = await collection.delete_many(filter_dict)
            
            logger.info(f"Deleted {result.deleted_count} documents from {self.collection_name}")
            return result.deleted_count
        except Exception as e:
            logger.error(f"Error bulk deleting documents from {self.collection_name}: {e}")
            raise DatabaseError(f"Failed to bulk delete documents: {str(e)}")
    
    async def create_indexes(self, indexes: List[tuple]) -> None:
        """Create database indexes."""
        try:
            collection = await self._get_collection()
            
            for index_spec in indexes:
                await collection.create_index(index_spec)
            
            logger.info(f"Created {len(indexes)} indexes for {self.collection_name}")
        except Exception as e:
            logger.error(f"Error creating indexes for {self.collection_name}: {e}")
            raise DatabaseError(f"Failed to create indexes: {str(e)}")
    
    async def aggregate(self, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute aggregation pipeline."""
        try:
            collection = await self._get_collection()
            
            cursor = collection.aggregate(pipeline)
            results = await cursor.to_list(length=None)
            
            # Convert ObjectIds
            return [self._convert_from_object_id(doc) for doc in results]
        except Exception as e:
            logger.error(f"Error executing aggregation in {self.collection_name}: {e}")
            raise DatabaseError(f"Failed to execute aggregation: {str(e)}")