from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    url_original = Column(String, index=True)
    code_short = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)