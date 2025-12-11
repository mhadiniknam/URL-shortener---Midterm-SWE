from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from src.models.url import URL
from src.repositories.base_repo import BaseRepo


class RedirectToUrlRepository(BaseRepo[URL]):
    """Repository for User Story 2: Redirect to Original URL"""

    def __init__(self, db: Session):
        super().__init__(db, URL)

    def get_by_short_code(self, short_code: str) -> Optional[URL]:
        """
        Retrieve a URL by its short code

        Args:
            short_code: The short code to look up

        Returns:
            Optional[URL]: The URL object if found, None otherwise
        """
        raise NotImplementedError

    def get_by_short_code_and_check_expiry(self, short_code: str) -> Optional[URL]:
        """
        Retrieve a URL by short code and check if it's expired

        Args:
            short_code: The short code to look up

        Returns:
            Optional[URL]: The URL object if found and not expired, None otherwise
        """
        raise NotImplementedError

    def is_expired(self, url: URL) -> bool:
        """
        Check if a URL is expired

        Args:
            url: The URL object to check

        Returns:
            bool: True if expired, False otherwise
        """
        raise NotImplementedError