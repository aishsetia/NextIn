import traceback

from fastapi import APIRouter
from sqlmodel import select

from core.db import DBSession
from fashion.models import ClothingItem, ClothingItemStatus

from .extractor import extract_attributes
from .suggestions import process_prompt

router = APIRouter(
    prefix="/fashiongpt",
    tags=["fashiongpt"],
)


@router.post("/execute")
async def execute(db_session: DBSession):
    clothing_items = await db_session.exec(
        select(ClothingItem)
        .where(ClothingItem.status == ClothingItemStatus.PROCESSING)
        .order_by(ClothingItem.created_at.desc())
    )
    to_be_processed = clothing_items.first()
    if not to_be_processed:
        return {"No items to process"}

    print(f"Processing item: {to_be_processed.id}")

    await process_item(db_session, to_be_processed)


async def process_item(db_session: DBSession, item: ClothingItem):
    try:
        attributes = extract_attributes(item.image_path)

        for attribute, value in attributes.items():
            setattr(item, attribute, value)

        item.status = ClothingItemStatus.FINISHED
        db_session.add(item)
        await db_session.commit()
        await db_session.refresh(item)

    except Exception as e:
        print(f"Error processing item: {e}")
        print(traceback.format_exc())
        item.status = ClothingItemStatus.FAILED
        db_session.add(item)
        await db_session.commit()
        await db_session.refresh(item)


@router.post("/suggest")
async def suggest(db_session: DBSession, prompt: str):
    available_items = await db_session.exec(
        select(ClothingItem).where(ClothingItem.status == ClothingItemStatus.FINISHED)
    )
    available_items = available_items.all()

    clothing_items = ""
    for item in available_items:
        clothing_items += f"{item.id}: {item.look_type.value} - {item.color} colored {item.garment_type} with {item.patterns} pattern\n"

    suggestions = process_prompt(prompt, clothing_items)

    return suggestions
