from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum
from uuid import uuid4


class ClothingItemStatus(str, Enum):
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
    image_path: str
    color: Optional[str] = Field(default=None)
    garment_type: Optional[str] = Field(default=None)
    patterns: Optional[str] = Field(default=None)
    look_type: Optional[LookType] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    status: ClothingItemStatus = Field()
