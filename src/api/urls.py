from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
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

@router.get("/{short_code}", response_model=URLResponse)
async def get_original_url(short_code: str, db: Session = Depends(get_db)):
    controller = URLController(db)
    return controller.get_original_url(short_code)

@router.delete("/urls/{short_code}")
async def delete_url(short_code: str, db: Session = Depends(get_db)):
    controller = URLController(db)
    try:
        response, code = controller.delete_url(short_code)
        return JSONResponse(content=response, status_code=code)
    except HTTPException as e:
        return JSONResponse(content={"success": "failure", "message": e.detail}, status_code=e.status_code)
