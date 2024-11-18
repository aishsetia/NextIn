import traceback

from fastapi import APIRouter
from sqlmodel import select

from core.db import DBSession
from fashion.models import ClothingItem, ClothingItemStatus

from .extractor import extract_attributes
from .suggestions import process_prompt
from .schemas import SuggestionRequest, SuggestionResponse

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
    item_to_process = clothing_items.first()
    if not item_to_process:
        return {"message": "No items to process"}

    print(f"Processing item: {item_to_process.id}")

    await process_item(db_session, item_to_process)


async def process_item(db_session: DBSession, item: ClothingItem):
    try:
        attributes = extract_attributes(item.image_path)

        for attr, value in attributes.items():
            setattr(item, attr, value)

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
async def suggest(db_session: DBSession, request: SuggestionRequest) -> SuggestionResponse:
    available_items = await db_session.exec(
        select(ClothingItem).where(ClothingItem.status == ClothingItemStatus.FINISHED)
    )
    items = available_items.all()

    clothing_items = "\n".join(
        f"{i+1}: {item.look_type.value} - {item.color} colored {item.garment_type} with {item.patterns} pattern"
        for i, item in enumerate(items)
    )
    suggestion = process_prompt(request.prompt, clothing_items)

    return SuggestionResponse(suggestion=suggestion)
