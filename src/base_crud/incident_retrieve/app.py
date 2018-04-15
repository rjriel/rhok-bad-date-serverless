import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
  dynamodb = boto3.resource('dynamodb', region_name='ca-central-1')
  table = dynamodb.Table('incident_report')
  admin = is_admin(dynamodb, event)
  if 'id' in event:
    return get_single(table, event, admin)
  else:
    return get_all(table, event, admin)
  
  
def get_single(table, event, admin):
  if admin:
    response = table.scan(
      FilterExpression='incident_id = :incident_id',
      ExpressionAttributeValues={
          ':incident_id': event.get('id')
      })
  else:
    response = table.scan(
      FilterExpression='incident_id = :incident_id and user_name = :username',
      ExpressionAttributeValues={
          ':incident_id': event.get('id'),
          ':username': event.get('username')
      }
    )
  return response.get('Items')

def get_all(table, event, admin):
  if admin:
    response = table.scan()
  else:
    response = table.scan(
      FilterExpression='user_name = :username',
      ExpressionAttributeValues={
          ':username': event.get('username')
      }
    )
  return response.get('Items')
  
def is_admin(dynamo, event):
  table = dynamo.Table('user')
  response = table.query(
      KeyConditionExpression=Key('username').eq(event['username']))
  if len(response.get('Items')):
    return response.get('Items')[0].get('role') == 'admin'
  else:
    return False