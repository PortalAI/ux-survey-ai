from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime

class UserInfo(BaseModel):
    user_id: str
    username: str
    login_method: str
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class Business(BaseModel):
    business_id: str = Field(default_factory=lambda: uuid4().hex)
    user_id: list[str]
    business_name: str
    business_description: str
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class BusinessSurvey(BaseModel):
    survey_id: str = Field(default_factory=lambda: uuid4().hex)
    business_id: str = Field(..., description="Id of the business from which survey belongs to")
    user_id: list[str]
    survey_name: str
    survey_description: str
    system_prompt: str
    initial_message: str
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class SurveyRecord(BaseModel):
    record_id: str
    survey_id: str
    business_id: str
    auth_id: list[str] = Field(...,
                               description="The user id from business owner who's should be authorized to view this record")
    customer_id: str | None = Field(default=None)
    chat_history: str | None
    summary: str | None
    structured_summary: dict | None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
