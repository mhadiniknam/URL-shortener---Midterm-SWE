import secrets
import string
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session

from src.repositories.url_repository import URLRepository
from src.models.url import URL
from src.db.config import MINUTES_TTL_APP


class URLService:
    """Service layer for URL shortening business logic"""

    SHORT_CODE_LENGTH = 8
    SHORT_CODE_CHARS = string.ascii_letters + string.digits

    def __init__(self, db: Session):
        self.repository = URLRepository(db)

    def _generate_short_code(self) -> str:
        """
        Generate a unique short code
        
        Returns:
            str: A random short code
        """
        while True:
            short_code = ''.join(
                secrets.choice(self.SHORT_CODE_CHARS) 
                for _ in range(self.SHORT_CODE_LENGTH)
            )
            if not self.repository.exists_by_short_code(short_code):
                return short_code

    def create_short_url(
        self, 
        original_url: str, 
        expiration_minutes: Optional[int] = None
    ) -> URL:
        """
        Create a short URL from an original URL
        
        Args:
            original_url: The original URL to shorten
            expiration_minutes: Optional expiration time in minutes
            
        Returns:
            URL: The created URL object
            
        Raises:
            ValueError: If URL is invalid
            IntegrityError: If short code collision occurs (very rare)
        """
        # Generate unique short code
        short_code = self._generate_short_code()
        
        # Calculate expiration time if provided
        expiration_time = None
        if expiration_minutes:
            expiration_time = datetime.utcnow() + timedelta(minutes=expiration_minutes)
        elif MINUTES_TTL_APP:
            # Use default TTL from config
            expiration_time = datetime.utcnow() + timedelta(minutes=MINUTES_TTL_APP)
        
        # Create URL record
        try:
            url = self.repository.create(
                original_url=original_url,
                short_code=short_code,
                expiration_time=expiration_time
            )
            return url
        except Exception as e:
            # Retry once if collision occurs (very rare)
            if "unique" in str(e).lower() or "duplicate" in str(e).lower():
                short_code = self._generate_short_code()
                url = self.repository.create(
                    original_url=original_url,
                    short_code=short_code,
                    expiration_time=expiration_time
                )
                return url
            raise

    def get_original_url(self, short_code: str) -> Optional[URL]:
        """
        Retrieve the original URL by short code
        
        Args:
            short_code: The short code to look up
            
        Returns:
            Optional[URL]: The URL object if found and not expired, None otherwise
        """
        return self.repository.get_by_short_code_and_check_expiry(short_code)

