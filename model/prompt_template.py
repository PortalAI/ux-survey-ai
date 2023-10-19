from enum import auto
from fastapi_restful.enums import StrEnum
from pydantic import BaseModel


class TemplateEnum(StrEnum):
    system_message = auto()
    agent_initial_message = auto()
    single_chat_summary = auto()
    multi_chat_summary = auto()


class Template(BaseModel):
    template_type: TemplateEnum
    template: str
    params: list[str]

# todo might be able to create a class for each
