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
        url = self.db.query(self.model).filter(self.model.short_code == short_code).first()
        if url:
            self.db.delete(url)
            self.db.commit()
            return True
        return False

    def delete_expired_urls(self) -> int:
        """
        Delete all expired URLs

        Returns:
            int: Number of deleted URLs
        """
        from datetime import datetime
        expired_urls = self.db.query(self.model).filter(
            self.model.expiration_time != None,
            self.model.expiration_time < datetime.utcnow()
        ).all()

        count = len(expired_urls)
        for url in expired_urls:
            self.db.delete(url)

        self.db.commit()
        return count