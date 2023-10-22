from datetime import datetime

from model import database_model
from database import dynamodb_table_base
from boto3.dynamodb.conditions import Key, Attr
from collections.abc import Sequence
from config import settings


class BusinessSurveyTable(dynamodb_table_base.DynamodbTableBase[database_model.BusinessSurvey]):
    def __init__(self):
        super().__init__(table_name=settings.BUSINESS_SURVEY_TABLE_NAME)

    def get_item(self, survey_id: str) -> database_model.BusinessSurvey | None:
        key = {
            'survey_id': survey_id
        }
        entry_dict = super().get_item(key)
        if entry_dict is None:
            return None
        return database_model.BusinessSurvey(**entry_dict)

    def delete_item(self, survey_id: str) -> None:
        key = {
            'survey_id': survey_id
        }
        super().delete_item(key)

    def update_survey(self, survey: database_model.BusinessSurvey):
        return self.update_item(
            key={"survey_id": survey.survey_id},
            update_expression=(
                "SET survey_description = :survey_description, "
                "survey_name = :survey_name, "
                "initial_message = :initial_message, "
                "updated_at = :updated_at"),
            expression_attribute_values={
                ":survey_name": survey.survey_name,
                ":survey_description": survey.survey_description,
                ":initial_message": survey.initial_message,
                ":updated_at": datetime.utcnow().isoformat(),
            }
        )

    def get_surveys_by_business_id(self, business_id: str) -> Sequence[database_model.BusinessSurvey]:
        response = self.table.query(
            IndexName='gsi1',
            KeyConditionExpression=Key('business_id').eq(business_id)
        )
        res_list = response.get('Items', [])
        return [database_model.BusinessSurvey(**bs_dict) for bs_dict in res_list]

    def update_survey_insight(
        self,
        survey_id: str,
        insight: str,
    ):
        return self.update_item(
            key={"survey_id": survey_id},
            update_expression="SET insight = :insight, updated_at = :updated_at",
            expression_attribute_values={
                ":insight": insight,
                ":updated_at": datetime.utcnow().isoformat(),
            }
        )

    def get_survey_from_guild_id(self, guild_id: str) -> list[database_model.BusinessSurvey]:
        response = self.table.scan(FilterExpression=Attr('guild_id').eq(guild_id))
        if not response:
            return []
        return response.get('Items', [])

    def get_prompt_from_survey_id(self, survey_id: str) -> tuple[str, str] | None:
        record = self.get_item(survey_id=survey_id)
        return record.system_prompt, record.initial_message
