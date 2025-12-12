from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from typing import Optional

class URLShortenRequest(BaseModel):
    original_url: HttpUrl = Field(...)
    expiration_minutes: Optional[int] = Field(None, ge=1)

class URLShortenResponse(BaseModel):
    status: str
    data: Optional[dict] = None
    message: Optional[str] = None

class URLResponse(BaseModel):
    original_url: str
    short_code: str
    created_at: datetime

class URLItem(BaseModel):
    short_code: str
    original_url: str
    short_url: str
    created_at: datetime
    expires_at: Optional[datetime] = None

class GetAllUrlsResponse(BaseModel):
    status: str
    data: list[URLItem] = []
    message: Optional[str] = None

class URLDeleteResponse(BaseModel):
    success: str
    message: str
