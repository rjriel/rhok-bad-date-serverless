from uuid import uuid4
import boto3
import json
import decimal
from pprint import pprint


def get_table(table_name):
    dynamodb = boto3.resource('dynamodb', region_name='ca-central-1') 
    
    table = dynamodb.Table(table_name)
    return table


def get_uuid():
    return str(uuid4().hex)
    

# ----- ^^^^^^^^^ common code to all lambdas ---------------

def lambda_handler(event, context):
  incident = event.get('body-json')
  username = event.get('params').get('querystring').get('username')
    
  user = get_table('user').get_item(Key={'user_name': username})
  role = user.get('Item').get('role')
  incident['incident_id'] = event.get('params').get('querystring').get('incident_id')
  incident_id = incident.get('incident_id')
  incident_table = get_table('incident_report')
  if role != 'moderator':
    item = incident_table.get_item(Key={'incident_id': incident_id}).get('Item')
    incident['public_incident_description'] = item['public_incident_description']

  incident_table.put_item(
     Item=incident
  )
        
  return incident_id




