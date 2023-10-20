from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime
from agent import prompt_templates


class UserInfo(BaseModel):
    user_id: str
    username: str
    login_method: str
    created_at: str
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class Business(BaseModel):
    business_id: str = Field(default_factory=lambda: uuid4().hex)
    user_id: list[str] = Field(default=[])
    business_name: str
    business_description: str
    created_at: str
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class BusinessSurvey(BaseModel):
    survey_id: str = Field(default_factory=lambda: uuid4().hex)
    business_id: str = Field(..., description="Id of the business from which survey belongs to.")
    user_id: list[str]
    target_audience_description: str | None = Field(default=None)
    survey_name: str
    survey_description: str
    system_prompt: str
    initial_message: str
    assistant_name: str = Field(default="Assistant", description="The name BO want to show on top of the chat.")
    quota: int
    created_at: str
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class SurveyRecord(BaseModel):
    record_id: str = Field(default_factory=lambda: uuid4().hex)
    survey_id: str
    business_id: str
    auth_id: list[str] = Field(
        default=[],
        description="The user id from business owner who's should be authorized to view this record")
    customer_id: str | None = Field(default=None)
    chat_history: str | None = Field(default=None)
    summary: str | None = Field(default=None)
    structured_summary: dict | None = Field(default=None)
    created_at: str
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    survey_ended: bool = Field(default=False)


class Template(BaseModel):
    template_id: str = Field(default_factory=lambda: uuid4().hex)
    survey_id: str

    system_message: str | None = Field(default=prompt_templates.SYSTEM_MESSAGE)
    system_message_params: list[str] | None = Field(default=prompt_templates.SYSTEM_MESSAGE_PARAMS)

    agent_initial_message: str | None = Field(default=prompt_templates.AGENT_INITIAL_MESSAGE)
    agent_initial_message_params: list[str] | None = Field(default=prompt_templates.AGENT_INITIAL_MESSAGE_PARAMS)

    summary_single_prompt: str | None = Field(default=prompt_templates.SUMMARY_SINGLE_PROMPT)
    summary_single_prompt_params: list[str] | None = Field(default=prompt_templates.SUMMARY_SINGLE_PROMPT_PARAMS)

    get_insight_prompt: str | None = Field(default=prompt_templates.GET_INSIGHT_PROMPT)
    get_insight_prompt_params: list[str] | None = Field(default=prompt_templates.GET_INSIGHT_PROMPT_PARAMS)
