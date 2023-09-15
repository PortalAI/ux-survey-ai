import boto3
from typing import Optional, TypeVar, Generic
from pydantic import BaseModel
from boto3.dynamodb.conditions import Key

Table = TypeVar('Table', bound=BaseModel)

class DynamoDBTable(Generic[Table]):

    def __init__(self, table_name: str, region_name: str = 'us-west-2'):
        # TODO: use generic instead of profile session when deploying
        session = boto3.Session(profile_name='portal-ai')
        self.dynamodb = session.resource('dynamodb', region_name=region_name)
        self.table = self.dynamodb.Table(table_name)

    def create_item(self, item: Table) -> Table:
        self.table.put_item(Item=item.model_dump())
        return item

    def get_item(self, key: dict) -> Optional[Table]:
        response = self.table.get_item(Key=key)
        return response.get('Item')

    def update_item(self, key: dict, update_expression: str, expression_attribute_values: dict) -> Optional[Table]:
        response = self.table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return response.get('Attributes')

    def delete_item(self, key: dict) -> dict:
        response = self.table.delete_item(Key=key)
        return response

    def query(self, key_condition_expression: Key, index_name: str | None = None) -> list[Table]:
        if index_name is not None:
            response = self.table.query(
                IndexName=index_name,
                KeyConditionExpression=key_condition_expression
            )
        else:
            response = self.table.query(
                KeyConditionExpression=key_condition_expression
            ) 
        return response.get('Items', [])


