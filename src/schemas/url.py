from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from typing import Optional


class URLShortenRequest(BaseModel):
    """Request schema for creating a short URL"""
    original_url: HttpUrl = Field(..., description="The original URL to shorten")
    expiration_minutes: Optional[int] = Field(
        None, 
        ge=1, 
        description="Optional expiration time in minutes (TTL feature)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "original_url": "https://www.example.com/very/long/url/path",
                "expiration_minutes": 1440
            }
        }


class URLShortenResponse(BaseModel):
    """Response schema for creating a short URL"""
    status: str = Field(..., description="Status of the operation: success or failure")
    data: Optional[dict] = Field(None, description="Data returned on success")
    message: Optional[str] = Field(None, description="Message returned on failure")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "data": {
                    "short_code": "abc123xyz",
                    "short_url": "http://localhost:8000/api/v1/abc123xyz",
                    "original_url": "https://www.example.com/very/long/url/path",
                    "expires_at": "2025-12-12T20:05:18"
                }
            }
        }


class URLShortenSuccessData(BaseModel):
    """Success data for URL shortening"""
    short_code: str = Field(..., description="The generated short code")
    short_url: str = Field(..., description="The complete short URL")
    original_url: str = Field(..., description="The original URL")
    expires_at: Optional[datetime] = Field(None, description="Expiration datetime if set")


class URLResponse(BaseModel):
    """Response schema for retrieving original URL"""
    original_url: str = Field(..., description="The original URL")
    short_code: str = Field(..., description="The short code")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "original_url": "https://www.example.com/very/long/url/path",
                "short_code": "abc123xyz",
                "created_at": "2025-12-11T20:05:18"
            }
        }


class URLErrorResponse(BaseModel):
    """Error response schema"""
    detail: str = Field(..., description="Error message")

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "URL not found or expired"
            }
        }

