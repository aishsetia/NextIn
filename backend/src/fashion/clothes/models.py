from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from enum import Enum
from uuid import uuid4
from fashion.user import User


class ClothingItemStatus(str, Enum):
    WAITING_FOR_FILE = "WAITING_FOR_FILE"
    PROCESSING = "PROCESSING"
    FINISHED = "FINISHED"
    FAILED = "FAILED"


class LookType(str, Enum):
    FORMAL = "FORMAL"
    CASUAL = "CASUAL"
    SPORTS = "SPORTS"
    NIGHT_OUT = "NIGHT_OUT"
    OTHER = "OTHER"

class ClothingItem(SQLModel, table=True):
    id: str = Field(default_factory=lambda: uuid4().hex, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    image_path: str
    color: Optional[str] = Field(default=None)
    garment_type: Optional[str] = Field(default=None)
    patterns: Optional[str] = Field(default=None)
    look_type: Optional[LookType] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(datetime.UTC))
    status: ClothingItemStatus = Field()

    # Relationships
    owner: User = Relationship(back_populates="clothing_items")
