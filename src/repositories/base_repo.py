from typing import TypeVar, Generic, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import delete, select
from datetime import datetime

T = TypeVar('T')

class BaseRepo(Generic[T]):
    """Base repository with common CRUD operations"""
    
    def __init__(self, db: Session, model: T):
        self.db = db
        self.model = model

    def create(self, obj) -> T:
        """Create a new object in database"""
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get_by_id(self, id: int) -> Optional[T]:
        """Get object by ID"""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all objects with pagination"""
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def update(self, id: int, obj_data: dict) -> Optional[T]:
        """Update object by ID"""
        obj = self.get_by_id(id)
        if obj:
            for key, value in obj_data.items():
                setattr(obj, key, value)
            self.db.commit()
            self.db.refresh(obj)
            return obj
        return None

    def delete(self, id: int) -> bool:
        """Delete object by ID"""
        obj = self.get_by_id(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False