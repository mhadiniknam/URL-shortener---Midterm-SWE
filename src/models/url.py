from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import re

Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)  # Changed from url_original to original_url
    short_code = Column(String(10), unique=True, nullable=False, index=True)  # Changed from code_short to short_code
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expiration_time = Column(DateTime, nullable=True)  # For TTL feature
    
