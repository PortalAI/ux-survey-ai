from fastapi_cognito import CognitoToken

from database import table_survey, table_survey_record
from model.service import GetSurveyResponse, GetSurveyInfoResponse, SurveyRecordsInfo
from services.auth import Auth

from model.chat import ChatHistory, Message

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
    def get_info(survey_id: str, auth: CognitoToken) -> GetSurveyInfoResponse:
        survey = survey_table.get_item(survey_id)
        Auth.validate_permission(survey, auth)
        records = survey_record_table.list_survey_records(survey_id=survey_id)

        survey_records = []
        for record in records:

            n_human_messages = 0
            chat_history: ChatHistory = ChatHistory.from_str(record.chat_history)
            for message in chat_history.messages:
                if message.role == 'human':
                    n_human_messages += 1

            survey_records.append(
                SurveyRecordsInfo(
                    **record.model_dump(),
                    n_human_messages=n_human_messages,
                )
            )

        response = GetSurveyInfoResponse(
            **survey.model_dump(),
            survey_records_count=len(records),
            survey_records=survey_records
        )

        return response
