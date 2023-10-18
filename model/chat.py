from pydantic import BaseModel
from enum import auto
import json
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
    
    @classmethod
    def from_str(cls, chat_history_str: str) -> "ChatHistory":
        chat_messages: list[dict] = json.loads(chat_history_str)
        messages: list[Message] = []
        for chat_message in chat_messages:
            messages.append(Message(
                role=chat_message["type"],
                content=chat_message["data"]["content"],
            ))
        return ChatHistory(messages=messages)
