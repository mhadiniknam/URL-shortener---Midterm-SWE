from abc import ABC
from sqlalchemy.orm import Session


class BaseService(ABC):
    """Base service class with common functionality"""
    
    def __init__(self, db: Session):
        self.db = db