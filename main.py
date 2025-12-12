from fastapi import FastAPI
from src.api import router
import uvicorn
import logging

app = FastAPI(title="URL Shortener API", version="0.1.0")

# Include API routes
app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting URL Shortener API server...")
    logger.info("API available at: http://0.0.0.0:8000")
    logger.info("Documentation available at: http://0.0.0.0:8000/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0", 
        port=8000,
        reload=True,
        log_level="info"
    )