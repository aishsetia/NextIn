from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pydantic.alias_generators import to_camel

from .exceptions import FastAPIException


class APIModel(BaseModel):
    class Config:
        populate_by_name = True
        alias_generator = to_camel


class Message(APIModel):
    message: str


class AccessFailure(Message):
    login_failed: bool = False
    should_logout: bool = False


class Response:
    @staticmethod
    def exc_unauthorized(content: Message):
        return FastAPIException(status_code=401, content=content)

    @staticmethod
    def exc_forbidden(content: AccessFailure):
        return FastAPIException(status_code=403, content=content)

    @staticmethod
    def exc_not_found(content: Message):
        return FastAPIException(status_code=404, content=content)

    @staticmethod
    def exc_runtime_error(content: Message):
        return FastAPIException(status_code=500, content=content)

    @staticmethod
    def runtime_error(content: Message):
        return JSONResponse(status_code=500, content=content.model_dump())
