from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4

if TYPE_CHECKING:
    from fashion.clothes import ClothingItem


class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: uuid4().hex, primary_key=True)

    name: str
    email: str = Field(unique=True)
    photo_url: str | None = None

    # Relationships
    clothing_items: List["ClothingItem"] = Relationship(back_populates="owner")
