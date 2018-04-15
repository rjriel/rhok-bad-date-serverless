from uuid import uuid4
import boto3
import json
import decimal
from copy import deepcopy
from pprint import pprint

# ATTENTION: Execution role must be "bad-date"


def get_table():
    dynamodb = boto3.resource('dynamodb', region_name='ca-central-1') 
        # aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    
    table = dynamodb.Table('incident_report')
    return table


def get_uuid():
    return str(uuid4().hex)
    

def remove_empty_string_attributes(input: dict):
    """DynamoDB does not yet support attribute that have an emptry string as value !!!!
    This is discussed in many places on the web, including bug submissions in AWS. 
    As of June 2017, the comment was "this will be fixed at some unknown time in 2018
    """
    new_struct = deepcopy(input)
    for item, value in input.items():
        if value == '':
            print("Warning: removing empty attribute", item)
            del new_struct[item]
        elif type(value) == dict:
            new_struct[item] = remove_empty_string_attributes(value)
            
    return new_struct


            
# ----- ^^^^^^^^^ common code to all lambdas ---------------

def lambda_handler(event, context):
    table = get_table()
    
    # pprint(event)
    usernameFromQuery = event["params"]["querystring"]["username"]
    
    print("Adding incident for user", usernameFromQuery)
    
    uuid = get_uuid()
    
    incidentFromPost = event["body-json"]
    incidentFromPost["incident_id"] = uuid
    incidentFromPost["user_name"] = usernameFromQuery
    
    event['incident_id'] = uuid
    # pprint(incidentFromPost)
    incidentFromPost = remove_empty_string_attributes(incidentFromPost)
    
    table.put_item(
        TableName="incident_report",
        Item=incidentFromPost
    )
        
    return uuid
