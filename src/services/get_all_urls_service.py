from typing import List
from sqlalchemy.orm import Session

from src.repositories.get_all_urls_repository import GetAllUrlsRepository
from src.models.url import URL
from src.services.base_service import BaseService


class GetAllUrlsService(BaseService):
    """Service for User Story 3: View All Shortened URLs"""

    def __init__(self, db: Session):
        super().__init__(db)
        self.repository = GetAllUrlsRepository(db)

    def get_all_urls(self) -> List[URL]:
        """
        Retrieve all URLs in the system

        Returns:
            List[URL]: List of all URL objects
        """
        return self.repository.get_all_urls()
