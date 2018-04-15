from uuid import uuid4
import boto3
import json
import decimal
from pprint import pprint

# ATTENTION: Execution role must be "bad-date"


def get_table():
    dynamodb = boto3.resource('dynamodb', region_name='ca-central-1') 
        # aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    
    table = dynamodb.Table('incident_report')
    return table


def get_uuid():
    return str(uuid4().hex)
    

# ----- ^^^^^^^^^ common code to all lambdas ---------------

def lambda_handler(event, context):
    table = get_table()
    
    pprint(event)
    
    print("Adding incident for user", event['user_name'])

    uuid = get_uuid()
    event['incident_id'] = uuid
    table.put_item(
       Item=event
    )
        
    return uuid

