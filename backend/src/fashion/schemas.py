from typing import Optional

from core.schemas import APIModel

from fashion.models import ClothingItemStatus, LookType

from fastapi import UploadFile, File

class ClothingInfoMinimal(APIModel):
    id: str
    image: str
    status: ClothingItemStatus


class ClothingInfo(ClothingInfoMinimal):
    color: Optional[str] = None
    garment_type: Optional[str] = None
    patterns: Optional[str] = None
    look_type: Optional[LookType] = None


class Clothes(APIModel):
    clothes: list[ClothingInfo]


class ClothesInProgress(APIModel):
    clothes: list[ClothingInfoMinimal]


class UploadClothResponse(APIModel):
    id: str
    

class ClothImageRequest(APIModel):
    filename: str
    
    
class UploadClothRequest(APIModel):
    image_name: str
    image_buffer: str
