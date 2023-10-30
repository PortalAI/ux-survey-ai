from database.dynamodb_table_base import DynamodbTableBase
from model import database_model
from boto3.dynamodb.conditions import Key
from collections.abc import Sequence
from config import settings
import logging

logger = logging.getLogger(__name__)

class BusinessTable(DynamodbTableBase[database_model.Business]):
    def __init__(self):
        super().__init__(table_name=settings.BUSINESS_TABLE_NAME)
        self.hash_key = "business_id"

    def get_item(self, business_id: str) -> database_model.Business | None:
        key = {
            self.hash_key: business_id
        }
        entry_dict = super().get_item(key)
        if entry_dict is None:
            return None
        return database_model.Business(**entry_dict)

    def get_by_business_name(self, business_name: str) -> Sequence[database_model.Business]:
        response = self.table.query(
            IndexName='business_name_index',
            KeyConditionExpression=Key('business_name').eq(business_name)
        )
        return response.get('Items', [])

    def update_business(self, business: database_model.Business):
        return self.update_item(
            key={self.hash_key: business.business_id},
            update_expression=(
                "SET business_name = :business_name, "
                "business_description = :business_description, "
                "updated_at = :updated_at"),
            expression_attribute_values={
                ":business_name": business.business_name,
                ":business_description": business.business_description,
                ":updated_at": business.updated_at,
            }
        )

    def delete_item(self, business_id: str):
        key = {
            self.hash_key: business_id
        }
        super().delete_item(key)

    def get_businesses(self, user_id: str) -> list[database_model.Business]:
        response = self.query_all(user_id)
        businesses = []
        for record in response:
            businesses.append(database_model.Business(**record))
        return businesses
