import uuid
from typing import Optional

from beanie import Document
from pydantic import (
    BaseModel,
    Field,
)
from datetime import datetime


class Reply(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    from_user: int
    comment: str
    to_reply: Optional[str] = None
    replies: Optional[str] = None


class BaseProductReview(BaseModel):
    product_id: int
    user_id: int
    rating: int
    comment: str


class ProductReview(Document, BaseProductReview):
    replies: list[Reply] = []

    class Settings:
        name = 'productReviews'

class ProductAnalytics(Document, BaseModel):
    product_id: int
    timestamp: datetime

    class Settings:
        name = 'productAnalytics'