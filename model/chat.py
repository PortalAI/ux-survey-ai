from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str
    content: str


class ChatHistory(BaseModel):
    messages: list[Message]
