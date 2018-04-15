from uuid import uuid4
import boto3
import json
import decimal
from pprint import pprint

# ATTENTION: Execution role must be "bad-date"


def get_table(table_name):
    dynamodb = boto3.resource('dynamodb', region_name='ca-central-1') 
        # aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    
    table = dynamodb.Table(table_name)
    return table


def get_uuid():
    return str(uuid4().hex)
    

# ----- ^^^^^^^^^ common code to all lambdas ---------------

def lambda_handler(event, context):
    pprint(event)
    
    print("Updating incident for user", event['user_name'])
    user = get_table('user').get_item(Key=dict(user_name=event['user_name']))
    pprint(user)
    role = user['Item']['role']
    incident_id = event['incident_id']
    incident_table = get_table('incident_report')
    if role != 'moderator':
        item = incident_table.get_item(Key=dict(incident_id=incident_id))['Item']
        current_public = item['public_incident_description']
        event['public_incident_description'] = current_public

    print("Key info: ", incident_id, dict(incident_id=incident_id))
    incident_table.put_item(
       Item=event
    )
        
    return incident_id




