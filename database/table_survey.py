from datetime import datetime
from typing import Optional

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

    def survey_exist(self, survey_id: str) -> bool:
        return self.get_item(survey_id=survey_id) is not None

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
                "system_prompt = :system_prompt, "
                "updated_at = :updated_at"),
            expression_attribute_values={
                ":survey_name": survey.survey_name,
                ":survey_description": survey.survey_description,
                ":initial_message": survey.initial_message,
                ":system_prompt": survey.system_prompt,
                ":updated_at": datetime.utcnow().isoformat(),
            }
        )

    def get_surveys(self, user_id: str, business_id: Optional[str] = None) -> Sequence[database_model.BusinessSurvey]:
        if business_id is not None:
            # Using query when business_id is provided
            query_kwargs = {
                "IndexName": "gsi1",
                "KeyConditionExpression": Key("business_id").eq(business_id),
                "FilterExpression": Attr("user_id").contains(user_id),
            }
            response = self.table.query(**query_kwargs)
        else:
            # Using scan as a fallback when no business_id is provided
            query_kwargs = {
                "IndexName": "gsi1",
                "FilterExpression": Attr("user_id").contains(user_id),
            }
            response = self.table.scan(**query_kwargs)

        res_list = response.get("Items", [])
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
        survey = self.get_item(survey_id=survey_id)
        return survey.system_prompt, survey.initial_message

    def update_prompts(self, survey_id: str, system_message: str, summerization_prompt: str, insight_prompt: str) -> None:
        pass
