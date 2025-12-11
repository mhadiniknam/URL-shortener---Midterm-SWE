from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
from datetime import datetime

from src.models.url import URL


class URLRepository:
    """Repository layer for URL operations"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, original_url: str, short_code: str, expiration_time: Optional[datetime] = None) -> URL:
        """
        Create a new URL record in the database
        
        Args:
            original_url: The original URL to shorten
            short_code: The generated short code
            expiration_time: Optional expiration datetime
            
        Returns:
            URL: The created URL object
            
        Raises:
            IntegrityError: If short_code already exists
        """
        url = URL(
            original_url=original_url,
            short_code=short_code,
            expiration_time=expiration_time
        )
        self.db.add(url)
        self.db.commit()
        self.db.refresh(url)
        return url

    def get_by_short_code(self, short_code: str) -> Optional[URL]:
        """
        Retrieve a URL by its short code
        
        Args:
            short_code: The short code to look up
            
        Returns:
            Optional[URL]: The URL object if found, None otherwise
        """
        return self.db.query(URL).filter(URL.short_code == short_code).first()

    def get_by_short_code_and_check_expiry(self, short_code: str) -> Optional[URL]:
        """
        Retrieve a URL by short code and check if it's expired
        
        Args:
            short_code: The short code to look up
            
        Returns:
            Optional[URL]: The URL object if found and not expired, None otherwise
        """
        url = self.get_by_short_code(short_code)
        if url and url.expiration_time:
            if datetime.utcnow() > url.expiration_time:
                return None
        return url

    def exists_by_short_code(self, short_code: str) -> bool:
        """
        Check if a short code already exists
        
        Args:
            short_code: The short code to check
            
        Returns:
            bool: True if exists, False otherwise
        """
        return self.db.query(URL).filter(URL.short_code == short_code).first() is not None

    def delete(self, short_code: str) -> bool:
        """
        Delete a URL by short code
        
        Args:
            short_code: The short code to delete
            
        Returns:
            bool: True if deleted, False if not found
        """
        url = self.get_by_short_code(short_code)
        if url:
            self.db.delete(url)
            self.db.commit()
            return True
        return False

