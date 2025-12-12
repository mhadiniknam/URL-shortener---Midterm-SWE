from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.services.create_url_service import CreateUrlService
from src.services.redirect_to_url_service import RedirectToUrlService
from src.services.get_all_urls_service import GetAllUrlsService
from src.services.delete_url_service import DeleteUrlService
from src.schemas.url import URLShortenRequest, URLShortenResponse, URLResponse, GetAllUrlsResponse, URLItem

class URLController:
    def __init__(self, db: Session):
        self.service = CreateUrlService(db)
        self.get_all_service = GetAllUrlsService(db)

    def shorten_url(self, request: URLShortenRequest, base_url: str) -> URLShortenResponse:
        try:
            original_url = str(request.original_url)
            url = self.service.create_short_url(
                original_url=original_url,
                expiration_minutes=request.expiration_minutes
            )
            short_url = f"{base_url}/{url.short_code}"
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
            return URLShortenResponse(status="failure", message=str(ve))
        except Exception as e:
            return URLShortenResponse(status="failure", message=f"Failed to create short URL: {str(e)}")

    def get_original_url(self, short_code: str) -> URLResponse:
        redirect_service = RedirectToUrlService(self.service.db)
        url = redirect_service.get_original_url(short_code)
        if not url:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found or expired")
        return URLResponse(original_url=url.original_url, short_code=url.short_code, created_at=url.created_at)

    def get_original_url_by_code(self, short_code: str):
        try:
            redirect_service = RedirectToUrlService(self.service.db)
            return redirect_service.get_original_url(short_code)
        except Exception:
            return None

    def get_all_urls(self, base_url: str) -> GetAllUrlsResponse:
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
            return GetAllUrlsResponse(status="success", data=data)
        except Exception as e:
            return GetAllUrlsResponse(status="failure", data=[], message=f"Failed to fetch URLs: {str(e)}")

    def delete_url(self, short_code: str):
        delete_service = DeleteUrlService(self.service.db)
        deleted = delete_service.delete_url(short_code)
        if deleted:
            return {"success": "status", "message": "deleted URL successfully"}, status.HTTP_200_OK
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")
