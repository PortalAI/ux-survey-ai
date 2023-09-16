from .dynamodb_table import DynamoDBTable
from .models import Business, BusinessSurvey, SurveySession
from constant import BUSINESS_TABLE_NAME, BUSINESS_SURVEY_TABLE_NAME, SURVEY_SESSION_TABLE_NAME
from boto3.dynamodb.conditions import Key, Attr
from collections.abc import Sequence
from datetime import datetime


class BusinessTable(DynamoDBTable[Business]):
    def __init__(self):
        super().__init__(table_name = BUSINESS_TABLE_NAME)

    def get_by_business_name(self, business_name: str) -> Sequence[Business]:
        response = self.table.query(
            IndexName='business_name_index',
            KeyConditionExpression=Key('business_name').eq(business_name)
        )
        return response.get('Items', [])

class BusinessSurveyTable(DynamoDBTable[BusinessSurvey]):
    def __init__(self):
        super().__init__(table_name = BUSINESS_SURVEY_TABLE_NAME)

    def get_by_survey_name(self, survey_name: str) -> Sequence[BusinessSurvey]:
        response = self.table.query(
            IndexName='survey_name_index',
            KeyConditionExpression=Key('survey_name').eq(survey_name)
        )
        return response.get('Items', [])
    
    def get_prompt_from_survey_id(self, survey_id: str) -> str | None:
        surveys = self.table.scan(FilterExpression=Attr('survey_id').eq(survey_id)).get("Items", [])
        if surveys and 'prompt' in surveys[0]:
            return surveys[0].get('prompt')
        return None
        

class SurveySessionTable(DynamoDBTable[SurveySession]):
    def __init__(self):
        super().__init__(table_name = SURVEY_SESSION_TABLE_NAME)

    def initiate_survey_session(self, survey_id: str, session_id: str):

        survey_session_entry = SurveySession(
            survey_id=survey_id,
            session_id=session_id,
            chat_history=None,
            summary=None,
            structured_summary=None,
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat(),
        )
        self.create_item(survey_session_entry)

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


