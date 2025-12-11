from typing import Optional
from sqlalchemy.orm import Session

from src.repositories.delete_url_repository import DeleteUrlRepository
from src.models.url import URL
from src.services.base_service import BaseService


class DeleteUrlService(BaseService):
    """Service for User Story 4: Delete Shortened URL"""

    def __init__(self, db: Session):
        super().__init__(db)
        self.repository = DeleteUrlRepository(db)

    def delete_url(self, short_code: str) -> bool:
        """
        Delete a URL by its short code

        Args:
            short_code: The short code to delete

        Returns:
            bool: True if deleted, False otherwise
        """
        raise NotImplementedError