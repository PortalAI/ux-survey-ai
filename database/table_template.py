from boto3.dynamodb.conditions import Key

from database.dynamodb_table_base import DynamodbTableBase
from model import database_model
from config import settings


# todo need an ability to get template by survey id
class TemplateTable(DynamodbTableBase[database_model.Template]):

    def __init__(self):
        super().__init__(table_name=settings.TEMPLATE_TABLE_NAME)
        self.hash_key = "template_id"

    def get_item(self, template_id) -> database_model.Template | None:
        key = {
            self.hash_key: template_id
        }
        entry_dict = super().get_item(key)
        if entry_dict is None:
            return None
        return database_model.Template(**entry_dict)

    def update_template(self, template: database_model.Template):
        return self.update_item(
            key={self.hash_key: template.template_id},
            update_expression=(
                "SET survey_id = :survey_id, "
                "system_message = :system_message, "
                "system_message_params = :system_message_params, "
                "agent_initial_message = :agent_initial_message, "
                "agent_initial_message_params = :agent_initial_message_params, "
                "summary_single_prompt = :summary_single_prompt, "
                "summary_single_prompt_params = :summary_single_prompt_params, "
                "get_insight_prompt = :get_insight_prompt, "
                "get_insight_prompt_params = :get_insight_prompt_params"
            ),
            expression_attribute_values={
                ":survey_id": template.survey_id,
                ":system_message": template.system_message,
                ":system_message_params": template.system_message_params,
                ":agent_initial_message": template.agent_initial_message,
                ":agent_initial_message_params": template.agent_initial_message_params,
                ":summary_single_prompt": template.summary_single_prompt,
                ":summary_single_prompt_params": template.summary_single_prompt_params,
                ":get_insight_prompt": template.get_insight_prompt,
                ":get_insight_prompt_params": template.get_insight_prompt_params,
            }
        )

    def get_by_survey_id(self, survey_id) -> database_model.Template | None:
        response = self.table.query(
            IndexName='survey_id_index',
            KeyConditionExpression=Key('survey_id').eq(survey_id)
        )
        return response.get('Items', [])
