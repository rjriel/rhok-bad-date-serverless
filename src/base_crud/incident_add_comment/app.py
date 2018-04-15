from uuid import uuid4
import boto3
import json
import decimal
from pprint import pprint

# ATTENTION: Execution role must be "bad-date"


def get_table(table_name):
    dynamodb = boto3.resource('dynamodb', region_name='ca-central-1') 

    table = dynamodb.Table(table_name)
    return table


def get_key_json(key):
    return dict(incident_id=key)
    

def lambda_handler(event, context):
    table = get_table('incident_report')
    response = table.update_item(
        Key=get_key_json(event['incident_id']),
        UpdateExpression="SET #comments = list_append(#comments, :vals)",
        ExpressionAttributeValues={
            ':vals': [event['comment']]
        },
        ExpressionAttributeNames={"#comments": "comments"},
        ReturnValues="UPDATED_NEW"
    )
    
    print("UpdateItem succeeded:")
    return json.dumps(response, indent=4)
