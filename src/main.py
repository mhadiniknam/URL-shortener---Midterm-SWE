from fastapi import FastAPI
from src.api import router

app = FastAPI(title="URL Shortener API", version="0.1.0")

# Include API routes
app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)