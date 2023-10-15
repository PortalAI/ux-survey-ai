import boto3
from typing import Optional, TypeVar, Generic
from pydantic import BaseModel
from boto3.dynamodb.conditions import Key, Attr
from config import settings

Table = TypeVar('Table', bound=BaseModel)


dynamodb_resource = boto3.resource('dynamodb', region_name=settings.AWS_DEFAULT_REGION)

class DynamodbTableBase(Generic[Table]):

    def __init__(self, table_name: str):
        self.dynamodb = dynamodb_resource
        self.table = self.dynamodb.Table(table_name)

    def create_item(self, item: Table) -> None:
        self.table.put_item(Item=item.model_dump())


    def get_item(self, key: dict) -> Optional[dict]:
        response = self.table.get_item(Key=key)
        return response.get('Item')

    def update_item(self, key: dict, update_expression: str, expression_attribute_values: dict) -> Optional[Table]:
        response = self.table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW"
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

    def scan(self, filter_expression: Attr, index_name: str | None = None) -> list[dict]:
        if index_name is not None:
            response = self.table.scan(
                IndexName=index_name,
                FilterExpression=filter_expression
            )
        else:
            response = self.table.scan(
                FilterExpression=filter_expression
            )

        items = response.get('Items', [])

        while 'LastEvaluatedKey' in response:
            if index_name is not None:
                response = self.table.scan(
                    IndexName=index_name,
                    FilterExpression=filter_expression,
                    ExclusiveStartKey=response['LastEvaluatedKey']
                )
            else:
                response = self.table.scan(
                    FilterExpression=filter_expression,
                    ExclusiveStartKey=response['LastEvaluatedKey']
                )

            items.extend(response.get('Items', []))
        
        return items

