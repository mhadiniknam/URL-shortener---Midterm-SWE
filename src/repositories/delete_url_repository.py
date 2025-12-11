from typing import Optional
from sqlalchemy.orm import Session

from src.models.url import URL
from src.repositories.base_repo import BaseRepo


class DeleteUrlRepository(BaseRepo[URL]):
    """Repository for User Story 4: Delete Shortened URL"""

    def __init__(self, db: Session):
        super().__init__(db, URL)

    def delete_by_short_code(self, short_code: str) -> bool:
        """
        Delete a URL by short code

        Args:
            short_code: The short code to delete

        Returns:
            bool: True if deleted, False if not found
        """
        raise NotImplementedError

    def delete_expired_urls(self) -> int:
        """
        Delete all expired URLs

        Returns:
            int: Number of deleted URLs
        """
        raise NotImplementedError