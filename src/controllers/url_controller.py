from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.services.create_url_service import CreateUrlService
from src.services.redirect_to_url_service import RedirectToUrlService
from src.services.get_all_urls_service import GetAllUrlsService
from src.schemas.url import URLShortenRequest, URLShortenResponse, URLResponse, GetAllUrlsResponse, URLItem


class URLController:
    """Controller layer for URL operations"""

    def __init__(self, db: Session):
        self.service = CreateUrlService(db)
        self.get_all_service = GetAllUrlsService(db)

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
            URLShortenResponse: The response containing status and data or error message

        Raises:
            HTTPException: If URL creation fails
        """
        try:
            # Validate the URL format first
            original_url = str(request.original_url)

            # Check if this exact URL already exists
            # This is handled by the service, but we can still validate here
            url = self.service.create_short_url(
                original_url=original_url,
                expiration_minutes=request.expiration_minutes
            )

            short_url = f"{base_url}/{url.short_code}"

            # Return success response with data
            return URLShortenResponse(
                status="success",
                data={
                    "short_code": url.short_code,
                    "short_url": short_url,
                    "original_url": url.original_url,
                    "expires_at": url.expiration_time
                }
            )
        except ValueError as ve:
            # Handle validation errors (invalid URL format)
            return URLShortenResponse(
                status="failure",
                message=str(ve)
            )
        except Exception as e:
            # Handle other errors (database, etc.)
            return URLShortenResponse(
                status="failure",
                message=f"Failed to create short URL: {str(e)}"
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
        redirect_service = RedirectToUrlService(self.service.db)
        url = redirect_service.get_original_url(short_code)

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

    def get_all_urls(self, base_url: str) -> GetAllUrlsResponse:
        """
        Retrieve all URLs in the system

        Args:
            base_url: The base URL for constructing the short URLs

        Returns:
            GetAllUrlsResponse: The response containing status and data array
        """
        try:
            urls = self.get_all_service.get_all_urls()
            data = [
                URLItem(
                    short_code=url.short_code,
                    original_url=url.original_url,
                    short_url=f"{base_url}/{url.short_code}",
                    created_at=url.created_at,
                    expires_at=getattr(url, 'expiration_time', None)
                )
                for url in urls
            ]
            return GetAllUrlsResponse(
                status="success",
                data=data
            )
        except Exception as e:
            return GetAllUrlsResponse(
                status="failure",
                data=[],
                message=f"Failed to fetch URLs: {str(e)}"
            )

