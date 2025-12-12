import secrets
import string
import re
import os
import time
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session

from src.repositories.create_url_repository import CreateUrlRepository
from src.models.url import URL
from src.db.config import MINUTES_TTL_APP
from src.services.base_service import BaseService


def encode_base62(num: int) -> str:
    """
    Encode a positive integer into Base62 string

    Args:
        num: The positive integer to encode

    Returns:
        str: The Base62 encoded string
    """
    if num == 0:
        return "0"

    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""

    while num > 0:
        result = chars[num % 62] + result
        num //= 62

    return result


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

    def _generate_short_code_from_id(self, url_id: int) -> str:
        """
        Generate a short code using Base62 encoding of the URL ID

        Args:
            url_id: The database ID of the URL record

        Returns:
            str: The Base62 encoded short code
        """
        return encode_base62(url_id)

    def _generate_short_code(self) -> str:
        """
        Generate a unique short code (deprecated - kept for backward compatibility)

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
        Create a short URL from an original URL using Base62 encoding of the database ID

        Args:
            original_url: The original URL to shorten
            expiration_minutes: Optional expiration time in minutes

        Returns:
            URL: The created URL object

        Raises:
            ValueError: If URL is invalid
            Exception: If unable to create the URL
        """
        # Validate and sanitize URL
        validated_url = self._validate_and_sanitize_url(original_url)

        # Check if this URL was already shortened
        existing_url = self.repository.get_by_original_url(validated_url)
        if existing_url:
            return existing_url

        # Calculate expiration time if provided
        expiration_time = None
        if expiration_minutes:
            expiration_time = datetime.utcnow() + timedelta(minutes=expiration_minutes)
        elif MINUTES_TTL_APP:
            # Use default TTL from config
            expiration_time = datetime.utcnow() + timedelta(minutes=MINUTES_TTL_APP)

        # Create URL record with Base62-encoded ID as the short code
        url = self.repository.create_url_with_id_based_short_code(
            original_url=validated_url,
            expiration_time=expiration_time
        )

        if url is None:
            raise Exception("Failed to create URL")

        return url