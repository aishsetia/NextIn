from pydantic import BaseModel
from typing import Optional
from fashion.models import ClothingItemStatus, LookType


class ClothingInfoMinimal(BaseModel):
    id: str
    image_path: str
    status: ClothingItemStatus


class ClothingInfo(ClothingInfoMinimal):
    color: Optional[str] = None
    garment_type: Optional[str] = None
    patterns: Optional[str] = None
    look_type: Optional[LookType] = None


class Clothes(BaseModel):
    clothes: list[ClothingInfo]


class ClothesInProgress(BaseModel):
    clothes: list[ClothingInfoMinimal]


class UploadClothResponse(BaseModel):
    id: str
