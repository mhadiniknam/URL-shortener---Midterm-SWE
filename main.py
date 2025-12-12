from fastapi import FastAPI
from src.api import router
import uvicorn
import logging
from fastapi.middleware.cors import CORSMiddleware

# Enable more detailed logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed from INFO to DEBUG for more details
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(title="URL Shortener API", version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    logger.info("Starting URL Shortener API server...")
    logger.info("API available at: http://0.0.0.0:8000")
    logger.info("Documentation available at: http://0.0.0.0:8000/docs")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug"  # Changed from "info" to "debug"
    )