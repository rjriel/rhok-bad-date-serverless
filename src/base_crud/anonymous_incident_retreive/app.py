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

# ----- ^^^^^^^^^ common code to all lambdas ---------------

def lambda_handler(event, context):
    table = get_table()
    
    pprint(event)
    
    print("Retrieving list of public incidents")

    # Get all instances of public expression from the database
    # FIXME: This will be slow and expensive because this will get the data for ALL the reports,
    # and only after having read the whole data and then filter for public comments
    # FIXME: This will not work if the data returned is larger than 1 MB
    response = table.scan(
        # Condition to look for is any non-null public_incident_description
        FilterExpression=("attribute_exists(public_incident_description)"),
        # And only get the public_incident_description
        ProjectionExpression=("public_incident_description")
    )
    return response["Items"]
