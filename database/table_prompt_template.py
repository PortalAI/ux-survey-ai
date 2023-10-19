from database.dynamodb_table_base import DynamodbTableBase
from model import database_model
from config import settings


class PromptTemplateTable(DynamodbTableBase[database_model.PromptTemplate]):

    def __init__(self):
        super().__init__(table_name=settings.PROMPT_TABLE_NAME)

