from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel


@dataclass
class FastAPIException(Exception):
    status_code: int
    content: dict[str, Any] | BaseModel
