from pydantic import BaseModel, Field
from model import chat, database_model


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


class GetBusinessListResponse(BaseModel):
    businesses: list[GetBusinessResponse]


class ListBusinessResponse(BaseModel):
    businesses: list[GetBusinessResponse]


################ Survey ################
class CreateSurveyRequest(BaseModel):
    business_id: str
    survey_name: str
    survey_description: str
    quota: int = Field(default=1000)
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
    initial_message: str


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


class GetSurveyInsightResponse(BaseModel):
    survey_insight: str


class ListSurveyByBusinessRequest(BaseModel):
    business_id: str


class ListSurveysByBusinessResponse(BaseModel):
    surveys: list[GetSurveyResponse]


################ Record ################
class GetOrCreateSurveyRecordRequest(BaseModel):
    survey_id: str
    record_id: str | None = Field(default=None)


class GetSurveyRecordResponse(BaseModel):
    survey_id: str
    record_id: str
    chat_history: chat.ChatHistory
    record_state: database_model.SurveyRecordState


class GetOrCreateSurveyRecordResponse(BaseModel):
    survey_id: str
    record_id: str
    chat_history: chat.ChatHistory
    record_state: database_model.SurveyRecordState
    description: str


class UpdateChatHistoryRequest(BaseModel):
    record_id: str
    chat_history: chat.ChatHistory


class UpdateChatRequest(BaseModel):
    record_id: str
    user_messages: str


class UpdateSurveyRecordResponse(BaseModel):
    pass


class ListSurveyRecordsResponse(BaseModel):
    records: list[database_model.SurveyRecord]


class GetChatHistoryRequest(BaseModel):
    survey_id: str
    record_id: str


class GetChatHistoryResponse(BaseModel):
    chat_history: chat.ChatHistory


class SendNewMessageRequest(BaseModel):
    record_id: str
    survey_id: str
    message: chat.Message


class SendNewMessageResponse(BaseModel):
    messages: chat.ChatHistory
    record_state: database_model.SurveyRecordState


class GetSurveyRecordSummaryResponse(BaseModel):
    record_id: str
    chat_summary: str


################ Template ################
class CreateTemplateRequest(BaseModel):
    survey_id: str
    system_message: str | None = Field(default=None)
    system_message_params: list[str] | None = Field(default=None)
    agent_initial_message: str | None = Field(default=None)
    agent_initial_message_params: list[str] = Field(default=None)
    summary_single_prompt: str | None = Field(default=None)
    summary_single_prompt_params: list[str] | None = Field(default=None)
    get_insight_prompt: str | None = Field(default=None)
    get_insight_prompt_params: list[str] | None = Field(default=None)


class CreateTemplateResponse(BaseModel):
    template_id: str
    survey_id: str
    system_message: str
    system_message_params: list[str]
    agent_initial_message: str
    agent_initial_message_params: list[str]
    summary_single_prompt: str
    summary_single_prompt_params: list[str]
    get_insight_prompt: str
    get_insight_prompt_params: list[str]


class UpdateTemplateRequest(BaseModel):
    template_id: str
    survey_id: str
    system_message: str
    system_message_params: list[str]
    agent_initial_message: str
    agent_initial_message_params: list[str]
    summary_single_prompt: str
    summary_single_prompt_params: list[str]
    get_insight_prompt: str
    get_insight_prompt_params: list[str]


class UpdateTemplateResponse(BaseModel):
    template_id: str
    survey_id: str
    system_message: str
    system_message_params: list[str]
    agent_initial_message: str
    agent_initial_message_params: list[str]
    summary_single_prompt: str
    summary_single_prompt_params: list[str]
    get_insight_prompt: str
    get_insight_prompt_params: list[str]


class GetTemplateRequest(BaseModel):
    template_id: str


class GetTemplateResponse(BaseModel):
    template_id: str
    template_id: str
    survey_id: str
    system_message: str
    system_message_params: list[str]
    agent_initial_message: str
    agent_initial_message_params: list[str]
    summary_single_prompt: str
    summary_single_prompt_params: list[str]
    get_insight_prompt: str
    get_insight_prompt_params: list[str]
