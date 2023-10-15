from pydantic import BaseModel, Field
from model import chat


################ Business ################
class CreateBusinessRequest(BaseModel):
    business_name: str
    business_description: str

class CreateBusinessResponse(BaseModel):
    business_id: str
    business_name: str
    business_description: str

class UpdateBusinessRequest(BaseModel):
    business_id: str
    business_name: str
    business_description: str

class UpdateBusinessResponse(BaseModel):
    business_id: str
    business_name: str
    business_description: str

class GetBusinessRequest(BaseModel):
    business_id: str

class GetBusinessResponse(BaseModel):
    business_id: str
    business_name: str
    business_description: str

class ListBusinessResponse(BaseModel):
    businesses: list[GetBusinessResponse]

################ Survey ################
class CreateSurveyRequest(BaseModel):
    business_id: str
    survey_name: str
    survey_description: str
    initial_message: str | None = Field(default=None)

class CreateSurveyResponse(BaseModel):
    business_id: str
    survey_id: str
    survey_name: str
    survey_description: str
    initial_message: str

class UpdateSurveyRequest(BaseModel):
    business_id: str
    survey_id: str
    survey_name: str
    survey_description: str
    initial_message: str | None = Field(default=None)

class UpdateSurveyResponse(BaseModel):
    business_id: str
    survey_id: str
    survey_name: str
    survey_description: str
    initial_message: str

class GetSurveyRequest(BaseModel):
    business_id: str
    survey_id: str

class GetSurveyResponse(BaseModel):
    business_id: str
    survey_id: str
    survey_name: str
    survey_description: str
    initial_message: str

class ListSurveyByBusinessRequest(BaseModel):
    business_id: str

class ListSurveyByBusinessResponse(BaseModel):
    surveys: list[GetSurveyResponse]

################ Record ################
class CreataSurveyRecordRequest(BaseModel):
    survey_id: str

class CreateSurveyRecordResponse(BaseModel):
    survey_id: str

class UpdateChatRequest(BaseModel):
    record_id: str
    user_messages: str

class UpdateSurveyRecordResponse(BaseModel):
    pass

class GetChatHistoryRequest(BaseModel):
    survey_id: str
    record_id: str

class GetChatHistoryResponse(BaseModel):
    chat_history: chat.ChatHistory
