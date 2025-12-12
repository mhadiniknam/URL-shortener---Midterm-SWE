from fastapi import APIRouter, Depends, HTTPException, status
from starlette.requests import Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Union

from src.db.session import get_db
from src.controllers.url_controller import URLController
from src.schemas.url import URLShortenRequest, URLShortenResponse, URLResponse, GetAllUrlsResponse

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
    controller = URLController(db)
    base_url = f"{str(http_request.base_url).rstrip('/')}/api/v1"
    return controller.shorten_url(request, base_url)


@router.get(
    "/urls",
    summary="View all shortened URLs",
    description="Retrieve a list of all shortened URLs in the system.",
    response_description="Returns a response with status and data array containing all URLs with metadata"
)
async def get_all_urls(
    request: Request,
    db: Session = Depends(get_db)
):
    controller = URLController(db)
    try:
        base_url = f"{str(request.base_url).rstrip('/')}/api/v1"
        result = controller.get_all_urls(base_url)
        # Set HTTP status code based on response status
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR if result.status == "failure" else status.HTTP_200_OK
        return JSONResponse(
            content=result.model_dump(mode='json'),
            status_code=status_code
        )
    except Exception as e:
        # Handle unexpected errors
        error_response = GetAllUrlsResponse(
            status="failure",
            data=[],
            message=f"Failed to fetch URLs: {str(e)}"
        )
        return JSONResponse(
            content=error_response.model_dump(mode='json'),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


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
    controller = URLController(db)
    return controller.get_original_url(short_code)
