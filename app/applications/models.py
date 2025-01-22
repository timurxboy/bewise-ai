from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text
from app.DB import Base


class Applications(Base):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True)
    user_name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

