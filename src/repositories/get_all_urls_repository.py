from typing import List
from sqlalchemy.orm import Session

from src.models.url import URL
from src.repositories.base_repo import BaseRepo


class GetAllUrlsRepository(BaseRepo[URL]):
    """Repository for User Story 3: View All Shortened URLs"""

    def __init__(self, db: Session):
        super().__init__(db, URL)

    def get_all_urls(self) -> List[URL]:
        """
        Retrieve all URLs in the database

        Returns:
            List[URL]: List of all URL objects
        """
        return self.db.query(self.model).all()
