import asyncio
import os

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from sqlmodel import select

from core.config import CONFIG
from core.db import DBSession
import traceback

from .models import ClothingItem, ClothingItemStatus
from .schemas import (Clothes, ClothesInProgress, ClothingInfo,
                      ClothingInfoMinimal, UploadClothResponse, ClothImageRequest, UploadClothRequest)

router = APIRouter(
    prefix="/clothes",
    tags=["clothes"],
)

uploads_router = APIRouter(
    prefix="/uploads",
    tags=["uploads"],
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
    for c in clothes:
        c.image_path = c.image_path.replace("uploads/", "")
    return Clothes(
        clothes=[
            ClothingInfo(
                id=c.id,
                image=c.image_path,
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
    db_session: DBSession, request: UploadClothRequest
) -> UploadClothResponse:
    try:
        if not request.image_buffer:
            raise HTTPException(status_code=400, detail="No file uploaded")
        os.makedirs("uploads", exist_ok=True)
        image_path = f"uploads/{request.image_name}"
        with open(image_path, "wb") as buffer:
            buffer.write(request.image_buffer.encode('utf-8'))
        cloth = ClothingItem(image_path=image_path, status=ClothingItemStatus.PROCESSING)
        db_session.add(cloth)
        await db_session.commit()
        await db_session.refresh(cloth)
        print("triggering project processing")
        await trigger_project_processing()
        print("project processing triggered")
        return UploadClothResponse(id=cloth.id)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to upload clothes")


@uploads_router.get("/{filename}")
async def get_upload(filename: str) -> FileResponse:
    print(f"Getting upload for {filename}")
    return FileResponse(f"uploads/{filename}")
