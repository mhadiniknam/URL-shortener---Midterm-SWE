from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from src.models.url import URL
from src.repositories.base_repo import BaseRepo


class CreateUrlRepository(BaseRepo[URL]):
    """Repository for User Story 1: Create Short URL"""

    def __init__(self, db: Session):
        super().__init__(db, URL)

    def create_url(self, original_url: str, short_code: str, expiration_time: Optional[datetime] = None) -> Optional[URL]:
        """
        Create a new URL record in the database with error handling

        Args:
            original_url: The original URL to shorten
            short_code: The generated short code
            expiration_time: Optional expiration datetime

        Returns:
            Optional[URL]: The created URL object, or None if creation failed
        """
        url = URL(
            original_url=original_url,
            short_code=short_code,
            expiration_time=expiration_time
        )
        self.db.add(url)
        try:
            self.db.commit()
            self.db.refresh(url)
            return url
        except IntegrityError:
            self.db.rollback()
            return None

    def exists_by_short_code(self, short_code: str) -> bool:
        """
        Check if a short code already exists

        Args:
            short_code: The short code to check

        Returns:
            bool: True if exists, False otherwise
        """
        return self.db.query(URL).filter(URL.short_code == short_code).first() is not None

    def get_by_original_url(self, original_url: str) -> Optional[URL]:
        """
        Retrieve a URL by its original URL

        Args:
            original_url: The original URL to look up

        Returns:
            Optional[URL]: The URL object if found, None otherwise
        """
        return self.db.query(URL).filter(URL.original_url == original_url).first()