from fastapi import APIRouter
from sqlmodel import select

from core.db import DBSession
from .models import ClothingItem, ClothingItemStatus
from .schemas import (
    Clothes,
    ClothesInProgress,
    ClothingInfo,
    ClothingInfoMinimal,
    UploadClothResponse,
)
from fastapi import UploadFile, File, HTTPException
import shutil
import os
import httpx
import asyncio
from core.config import CONFIG

router = APIRouter(
    prefix="/clothes",
    tags=["clothes"],
)


async def _trigger_project_processing():
    client = httpx.AsyncClient()
    print("Triggering project processing")
    resp = await client.post(f"{CONFIG.FASHIONGPT.API_URL}/execute")
    print(f"Project processing triggered")


async def trigger_project_processing():
    asyncio.ensure_future(_trigger_project_processing())


@router.get("/")
async def get_clothes(db_session: DBSession) -> Clothes:
    clothes_query = await db_session.exec(
        select(ClothingItem).where(ClothingItem.status == ClothingItemStatus.FINISHED)
    )
    clothes = clothes_query.all()
    return Clothes(
        clothes=[
            ClothingInfo(
                id=c.id,
                image_path=c.image_path,
                status=c.status,
                color=c.color,
                garment_type=c.garment_type,
                patterns=c.patterns,
                look_type=c.look_type,
            )
            for c in clothes
        ]
    )


@router.get("/in-progress")
async def get_in_progress_clothes(db_session: DBSession) -> ClothesInProgress:
    clothes_query = await db_session.exec(
        select(ClothingItem).where(ClothingItem.status == ClothingItemStatus.PROCESSING)
    )
    clothes = clothes_query.all()
    return ClothesInProgress(
        clothes=[
            ClothingInfoMinimal(
                id=c.id,
                image_path=c.image_path,
                status=c.status,
            )
            for c in clothes
        ]
    )


@router.post("/")
async def upload_clothes(
    db_session: DBSession, image: UploadFile = File(...)
) -> UploadClothResponse:
    if not image.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    os.makedirs("uploads", exist_ok=True)
    image_path = f"uploads/{image.filename}"
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    cloth = ClothingItem(image_path=image_path, status=ClothingItemStatus.PROCESSING)
    db_session.add(cloth)
    await db_session.commit()
    await db_session.refresh(cloth)
    print("triggering project processing")
    await trigger_project_processing()
    print("project processing triggered")
    return UploadClothResponse(id=cloth.id)
