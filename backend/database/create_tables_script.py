import boto3
import constant

session = boto3.Session(profile_name=constant.AWS_LOCAL_PROFILE)
dynamodb = session.resource('dynamodb', region_name=constant.AWS_REGION)
dynamodb_client = boto3.client('dynamodb', region_name=constant.AWS_REGION)

def get_existing_table():
    return dynamodb_client.list_tables()['TableNames']

def delete_table(name):
    dynamodb.Table(name).delete()
    

def create_business_table():
    table_name = 'Businesses'
    # if table_name in get_existing_table():
    #     print(f'{table_name} already exist, skip creation')
    #     return
    delete_table(table_name)
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'business_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'business_id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'business_name',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        },
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'business_name_index',
                'KeySchema': [
                    {
                        'AttributeName': 'business_name',
                        'KeyType': 'HASH'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            }
        ]
    )
    table.wait_until_exists()
    print(f"Table {table_name} created successfully!")


def create_business_surveys_table():
    table_name = 'BusinessSurveys'
    if table_name in get_existing_table():
        print(f'{table_name} already exist, skip creation')
        return
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'business_id',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'survey_id',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'business_id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'survey_id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'survey_name',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        },
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'survey_name_index',
                'KeySchema': [
                    {
                        'AttributeName': 'survey_name',
                        'KeyType': 'HASH'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            }
        ]
    )

    # Wait until the table exists, this will block and loop until table is created
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    print(f"Table {table_name} is created!")

def create_survey_sessions_table():
    table_name = 'SurveySessions'
    if table_name in get_existing_table():
        print(f'{table_name} already exist, skip creation')
        return

    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'survey_id',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'session_id',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'survey_id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'session_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    print(f"Table {table_name} is created!")

if __name__ == "__main__":
    create_business_table()
    create_business_surveys_table()
    create_survey_sessions_table()
