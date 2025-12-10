from fastapi import APIRouter
from src.api.urls import router as urls_router

router = APIRouter()

# Include the URL endpoints
router.include_router(urls_router)