import secrets
import string
import re
import os
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session

from src.repositories.create_url_repository import CreateUrlRepository
from src.models.url import URL
from src.db.config import MINUTES_TTL_APP
from src.services.base_service import BaseService


class CreateUrlService(BaseService):
    """Service for User Story 1: Create Short URL"""

    def __init__(self, db: Session):
        super().__init__(db)
        self.repository = CreateUrlRepository(db)
        # Read short code length from environment, default to 6
        self.SHORT_CODE_LENGTH = int(os.getenv('SHORT_CODE_LENGTH', 6))
        self.SHORT_CODE_CHARS = string.ascii_letters + string.digits

    def validate_url(self, url: str) -> bool:
        """
        Validate URL format

        Args:
            url: The URL to validate

        Returns:
            bool: True if URL is valid, False otherwise
        """
        if not url:
            return False
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        # URL validation regex
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:'
            r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'  # ...or ip
            r')'
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )
        return url_pattern.match(url) is not None

    def _validate_and_sanitize_url(self, url: str) -> str:
        """
        Validate and sanitize URL

        Args:
            url: The URL to validate and sanitize

        Returns:
            str: The sanitized URL

        Raises:
            ValueError: If URL is invalid
        """
        if not url:
            raise ValueError("URL cannot be empty")
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        if not self.validate_url(url):
            raise ValueError(f"Invalid URL format: {url}")
        
        return url

    def _generate_short_code(self) -> str:
        """
        Generate a unique short code

        Returns:
            str: A random short code
        """
        for _ in range(100):  # Try up to 100 times to generate a unique code
            short_code = ''.join(
                secrets.choice(self.SHORT_CODE_CHARS)
                for _ in range(self.SHORT_CODE_LENGTH)
            )
            if not self.repository.exists_by_short_code(short_code):
                return short_code
        
        # If we can't generate a unique code after 100 attempts, raise an error
        raise Exception("Could not generate unique short code after 100 attempts")

    def create_short_url(self, original_url: str, expiration_minutes: Optional[int] = None) -> URL:
        """
        Create a short URL from an original URL

        Args:
            original_url: The original URL to shorten
            expiration_minutes: Optional expiration time in minutes

        Returns:
            URL: The created URL object

        Raises:
            ValueError: If URL is invalid
            Exception: If unable to generate unique short code
        """
        # Validate and sanitize URL
        validated_url = self._validate_and_sanitize_url(original_url)

        # Check if this URL was already shortened
        existing_url = self.repository.get_by_original_url(validated_url)
        if existing_url:
            return existing_url

        # Generate unique short code
        short_code = self._generate_short_code()

        # Calculate expiration time if provided
        expiration_time = None
        if expiration_minutes:
            expiration_time = datetime.utcnow() + timedelta(minutes=expiration_minutes)
        elif MINUTES_TTL_APP:
            # Use default TTL from config
            expiration_time = datetime.utcnow() + timedelta(minutes=MINUTES_TTL_APP)

        # Create URL record with error handling
        url = self.repository.create_url(
            original_url=validated_url,
            short_code=short_code,
            expiration_time=expiration_time
        )

        if url is None:
            # If creation failed due to collision, try once more
            short_code = self._generate_short_code()
            url = self.repository.create(
                original_url=validated_url,
                short_code=short_code,
                expiration_time=expiration_time
            )

        return url