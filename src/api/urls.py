from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.controllers.url_controller import URLController
from src.schemas.url import URLShortenRequest, URLShortenResponse, URLResponse

router = APIRouter(tags=["URLs"])


@router.post(
    "/",
    response_model=URLShortenResponse,
    status_code=201,
    summary="Create a short URL",
    description="Create a shortened URL from an original URL. Optionally set expiration time in minutes.",
    response_description="Returns success status with short URL data or failure status with error message"
)
async def create_short_url(
    request: URLShortenRequest,
    http_request: Request,
    db: Session = Depends(get_db)
) -> URLShortenResponse:
    """
    Create a short URL

    - **original_url**: The original URL to shorten (required)
    - **expiration_minutes**: Optional expiration time in minutes (TTL feature)

    Returns a success response with short code and URL or a failure response with error message.
    """
    controller = URLController(db)
    base_url = f"{str(http_request.base_url).rstrip('/')}/api/v1"
    return controller.shorten_url(request, base_url)


@router.get(
    "/{short_code}",
    response_model=URLResponse,
    summary="Get original URL",
    description="Retrieve the original URL by its short code. Returns 404 if not found or expired.",
    response_description="Returns the original URL and metadata"
)
async def get_original_url(
    short_code: str,
    db: Session = Depends(get_db)
) -> URLResponse:
    """
    Get original URL by short code
    
    - **short_code**: The short code to look up
    
    Returns the original URL and creation timestamp.
    """
    controller = URLController(db)
    return controller.get_original_url(short_code)

