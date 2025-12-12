from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from starlette.requests import Request
from src.db.session import get_db
from src.controllers.url_controller import URLController
from src.schemas.url import URLShortenRequest, URLShortenResponse, URLResponse, GetAllUrlsResponse

router = APIRouter(tags=["URLs"])

@router.post("/", response_model=URLShortenResponse, status_code=201)
async def create_short_url(request: URLShortenRequest, http_request: Request, db: Session = Depends(get_db)):
    controller = URLController(db)
    base_url = f"{str(http_request.base_url).rstrip('/')}/api/v1"
    return controller.shorten_url(request, base_url)

@router.get("/urls")
async def get_all_urls(request: Request, db: Session = Depends(get_db)):
    controller = URLController(db)
    base_url = f"{str(request.base_url).rstrip('/')}/api/v1"
    result = controller.get_all_urls(base_url)
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR if result.status == "failure" else status.HTTP_200_OK
    return JSONResponse(content=result.model_dump(mode='json'), status_code=status_code)

import re
import logging

# Set up logger
logger = logging.getLogger(__name__)

def validate_and_fix_url(url: str) -> str:
    """
    Validate and fix URL to ensure it has proper protocol for redirect
    """
    if not url:
        return url

    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    # Basic URL validation
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

    if url_pattern.match(url):
        return url
    else:
        # If URL is still invalid after adding protocol, return None to indicate failure
        return None

from urllib.parse import urlparse

def is_valid_url(url: str) -> bool:
    """
    Check if the URL is valid by parsing it
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

@router.get("/{short_code}")
async def redirect_to_original_url(short_code: str, db: Session = Depends(get_db)):
    logger.debug(f"Redirect endpoint called with short_code: {short_code}")
    controller = URLController(db)
    try:
        url = controller.get_original_url_by_code(short_code)
        logger.debug(f"Found URL in database: {url}")
        if url and url.original_url:
            logger.debug(f"Original URL to redirect to: {url.original_url}")
            # Validate and sanitize the URL before redirecting
            fixed_url = validate_and_fix_url(url.original_url)
            logger.debug(f"Fixed URL: {fixed_url}")
            if fixed_url and is_valid_url(fixed_url):
                # Using 307 Temporary Redirect to preserve HTTP method
                logger.debug(f"Performing redirect to: {fixed_url}")
                return RedirectResponse(url=fixed_url, status_code=307)
            else:
                # If URL is invalid, treat as not found
                logger.debug(f"Invalid URL detected (fixed_url: {fixed_url}, is_valid: {fixed_url and is_valid_url(fixed_url)}), returning failure response")
                return JSONResponse(
                    content={"status": "failure", "message": f"URL not found or invalid: {url.original_url}"},
                    status_code=status.HTTP_404_NOT_FOUND
                )
        else:
            logger.debug(f"No URL found for short_code: {short_code}")
            return JSONResponse(
                content={"status": "failure", "message": "URL not found"},
                status_code=status.HTTP_404_NOT_FOUND
            )
    except HTTPException as e:
        logger.error(f"HTTPException in redirect endpoint: {str(e)}")
        return JSONResponse(
            content={"status": "failure", "message": "URL not found"},
            status_code=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Exception in redirect endpoint: {str(e)}")
        return JSONResponse(
            content={"status": "failure", "message": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.delete("/urls/{short_code}")
async def delete_url(short_code: str, db: Session = Depends(get_db)):
    controller = URLController(db)
    try:
        response, code = controller.delete_url(short_code)
        return JSONResponse(content=response, status_code=code)
    except HTTPException as e:
        return JSONResponse(content={"success": "failure", "message": e.detail}, status_code=e.status_code)
