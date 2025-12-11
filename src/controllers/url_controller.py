from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from src.services.url_service import URLService
from src.schemas.url import URLShortenRequest, URLShortenResponse, URLResponse


class URLController:
    """Controller layer for URL operations"""

    def __init__(self, db: Session):
        self.service = URLService(db)

    def shorten_url(
        self, 
        request: URLShortenRequest, 
        base_url: str
    ) -> URLShortenResponse:
        """
        Create a short URL from an original URL
        
        Args:
            request: The shorten request containing original_url and optional expiration
            base_url: The base URL for constructing the short URL
            
        Returns:
            URLShortenResponse: The response containing short code and URL
            
        Raises:
            HTTPException: If URL creation fails
        """
        try:
            url = self.service.create_short_url(
                original_url=str(request.original_url),
                expiration_minutes=request.expiration_minutes
            )
            
            short_url = f"{base_url}/{url.short_code}"
            
            return URLShortenResponse(
                short_code=url.short_code,
                short_url=short_url,
                original_url=url.original_url,
                expires_at=url.expiration_time
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create short URL: {str(e)}"
            )

    def get_original_url(self, short_code: str) -> URLResponse:
        """
        Retrieve the original URL by short code
        
        Args:
            short_code: The short code to look up
            
        Returns:
            URLResponse: The response containing original URL and metadata
            
        Raises:
            HTTPException: If URL not found or expired
        """
        url = self.service.get_original_url(short_code)
        
        if not url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="URL not found or expired"
            )
        
        return URLResponse(
            original_url=url.original_url,
            short_code=url.short_code,
            created_at=url.created_at
        )

