from pydantic import BaseModel, Field
from datetime import datetime


class SApplication(BaseModel):
    id: int
    user_name: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True


class SApplicationCreate(BaseModel):
    user_name: str
    description: str = Field(..., description="Описание заявки")

    class Config:
        from_attributes = True


