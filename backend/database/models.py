from pydantic import BaseModel

class Business(BaseModel):
    business_id: str
    business_name: str
    business_description: str

class BusinessSurvey(BaseModel):
    business_id: str
    survey_id: str
    survey_name: str
    survey_description: str
    chat_prompts: str | None
    survey_link: str
    presentation_link: str
    presentation_password: str
    created_at: str
    prompt: str | None

class SurveySession(BaseModel):
    survey_id: str
    session_id: str
    chat_history: str | None
    summary: str | None
    structured_summary: dict | None
    created_at: str
    updated_at: str

class CreateBusinessSurveyRequest(BaseModel):
    business_name: str
    business_description: str
    survey_name: str
    survey_description: str
    
class CreateBusinessSurveyResponse(BaseModel):
    business_id: str
    business_name: str
    business_description: str
    survey_link: str
    presentation_link: str
    presentation_password: str

class UpdateSurveySessionRequest(BaseModel):
    survey_id: str
    summary: str | None
    chat_history: str | None
    structured_summary: dict | None

class SaveDiscordChatResultRequest(BaseModel):
    guild_id: str
    user_id: str
    summary: str | None
    chat_history: str
    