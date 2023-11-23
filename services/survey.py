from fastapi_cognito import CognitoToken
from conversation.langchain.langchain_agent import LangChainAgent

from database import table_survey, table_survey_record
from model.service import GetSurveyResponse
from services.auth import Auth

survey_table = table_survey.BusinessSurveyTable()
survey_record_table = table_survey_record.SurveyRecordTable()


class SurveyService:
    @staticmethod
    def get_survey(survey_id: str, auth: CognitoToken) -> GetSurveyResponse:
        survey = survey_table.get_item(survey_id)
        Auth.validate_permission(survey, auth)
        records = survey_record_table.list_survey_records(survey_id=survey_id)
        return GetSurveyResponse(**survey.model_dump(), survey_records_count=len(records))

    @staticmethod
    def create_init_message(system_prompt: str) -> str:
        agent = LangChainAgent(system_message=system_prompt)
        return agent.reply(system_prompt)
