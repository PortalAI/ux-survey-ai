from model import database_model
from database import dynamodb_table_base
from boto3.dynamodb.conditions import Key, Attr
from collections.abc import Sequence
from config import settings



class BusinessSurveyTable(dynamodb_table_base.DynamodbTableBase[database_model.BusinessSurvey]):
    def __init__(self):
        super().__init__(table_name = settings.BUSINESS_SURVEY_TABLE_NAME)

    def get_item(self, survey_id: str) -> dict | None:
        key = {
            'survey_id': survey_id
        }
        return super().get_item(key)

    def get_by_survey_name(self, survey_name: str) -> Sequence[database_model.BusinessSurvey]:
        response = self.table.query(
            IndexName='survey_name_index',
            KeyConditionExpression=Key('survey_name').eq(survey_name)
        )
        return response.get('Items', [])
    
    def get_survey_from_guild_id(self, guild_id: str) -> list[database_model.BusinessSurvey]:
        response = self.table.scan(FilterExpression=Attr('guild_id').eq(guild_id))
        if not response:
            return []
        return response.get('Items', [])

    def get_prompt_from_survey_id(self, survey_id: str) -> str | None:
        record = self.get_item(survey_id=survey_id)
        return record.get("system_prompt")
        