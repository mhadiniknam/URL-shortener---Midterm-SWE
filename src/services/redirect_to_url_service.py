from typing import Optional
from sqlalchemy.orm import Session

from src.repositories.redirect_to_url_repository import RedirectToUrlRepository
from src.models.url import URL
from src.services.base_service import BaseService


class RedirectToUrlService(BaseService):
    """Service for User Story 2: Redirect to Original URL"""

    def __init__(self, db: Session):
        super().__init__(db)
        self.repository = RedirectToUrlRepository(db)

    def get_original_url(self, short_code: str) -> Optional[URL]:
        """
        Retrieve the original URL by short code

        Args:
            short_code: The short code to look up

        Returns:
            Optional[URL]: The URL object if found and not expired, None otherwise
        """
        return self.repository.get_by_short_code_and_check_expiry(short_code)