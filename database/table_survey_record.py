from model import database_model
from database import dynamodb_table_base
from datetime import datetime
from config import settings



class SurveyRecordTable(dynamodb_table_base.DynamodbTableBase[database_model.SurveyRecord]):
    def __init__(self):
        super().__init__(table_name = settings.SURVEY_RECORD_TABLE_NAME)

    def initiate_survey_session(self, survey_id: str, session_id: str):
        survey_session_entry = database_model.SurveySession(
            survey_id=survey_id,
            session_id=session_id,
            chat_history=None,
            summary=None,
            structured_summary=None,
        )
        self.create_item(survey_session_entry)

    def get_item(self, record_id: str) -> dict | None:
        key = {
            'record_id': record_id
        }
        return super().get_item(key)

    def update_chat_history(
        self,
        record_id: str,
        chat_history: str,
    ):
        return self.update_item(
            key={"record_id": record_id},
            update_expression="SET chat_history = :chat_history, updated_at = :updated_at",
            expression_attribute_values={
                ":chat_history": chat_history,
                ":updated_at": datetime.utcnow().isoformat(),
            }
        )


    def update_survey_session(
        self,
        survey_id: str,
        session_id: str,
        summary: str | None = None,
        chat_history: str | None = None,
        structured_summary: dict = {}
    ):
        self.update_item(
            key={"survey_id": survey_id, "session_id": session_id},
            update_expression='SET summary = :summary, chat_history = :chat_history, structured_summary = :structured_summary,  updated_at = :updated_at',
            expression_attribute_values={
                ":summary": summary,
                ":chat_history": chat_history,
                ":structured_summary": structured_summary,
                ":updated_at": datetime.utcnow().isoformat(),
            }
        )


