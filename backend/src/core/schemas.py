from enum import EnumMeta as _EnumMeta

from fastapi_utils.enums import StrEnum as _StrEnum
from pydantic import BaseModel
from pydantic.alias_generators import to_camel

class __EnumMeta(_EnumMeta):
    def __contains__(self, __o: str) -> bool:
        return __o in list(map(lambda m: m.value, self))


class StrEnum(_StrEnum, metaclass=__EnumMeta):
    pass


class APIModel(BaseModel):
    class Config:
        populate_by_name = True
        alias_generator = to_camel


class Message(APIModel):
    message: str