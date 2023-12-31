from model import database_model
from database import dynamodb_table_base
from boto3.dynamodb.conditions import Key
from datetime import datetime
from config import settings


class SurveyRecordTable(dynamodb_table_base.DynamodbTableBase[database_model.SurveyRecord]):
    def __init__(self):
        super().__init__(table_name=settings.SURVEY_RECORD_TABLE_NAME)

    def get_item(self, record_id: str) -> database_model.SurveyRecord | None:
        key = {
            'record_id': record_id
        }
        entry_dict = super().get_item(key)
        if entry_dict is None:
            return None
        return database_model.SurveyRecord(**entry_dict)

    def delete_item(self, record_id: str) -> None:
        key = {
            'record_id': record_id
        }
        super().delete_item(key)

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

    def update_record_state(
        self,
        record_id: str,
        record_state: database_model.SurveyRecordState,
    ):
        return self.update_item(
            key={"record_id": record_id},
            update_expression="SET record_state = :record_state, updated_at = :updated_at",
            expression_attribute_values={
                ":record_state": record_state,
                ":updated_at": datetime.utcnow().isoformat(),
            }
        )

    def update_summary(
        self,
        record_id: str,
        summary: str,
    ):
        return self.update_item(
            key={"record_id": record_id},
            update_expression="SET summary = :summary, updated_at = :updated_at",
            expression_attribute_values={
                ":summary": summary,
                ":updated_at": datetime.utcnow().isoformat(),
            }
        )

    def list_survey_records(self, survey_id: str) -> list[database_model.SurveyRecord]:
        response = self.query(
            index_name="gsi1",
            key_condition_expression=Key("survey_id").eq(survey_id)
        )
        results = [database_model.SurveyRecord(**record) for record in response]
        return results

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
