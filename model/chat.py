from pydantic import BaseModel
from enum import auto

from fastapi_restful.enums import StrEnum


class RoleEnum(StrEnum):
    human = auto()
    system = auto()
    ai = auto()
    

class Message(BaseModel):
    role: RoleEnum
    content: str


class ChatHistory(BaseModel):
    messages: list[Message]
