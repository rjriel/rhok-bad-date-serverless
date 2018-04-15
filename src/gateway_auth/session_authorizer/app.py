import boto3
import re
import time
import json
import calendar
import os
from boto3.dynamodb.conditions import Key

def lambda_handler(event, ctx):
  dynamodb = boto3.resource('dynamodb', region_name='ca-central-1')
  table = dynamodb.Table('token')
  username = event['queryStringParameters'].get('username')
  token = event['queryStringParameters'].get('authorization')
  debug = os.getenv('DEBUG') is '1'

  response = table.query(
    KeyConditionExpression=Key('user_name').eq(username)
  )
  if debug:
    print("[DEBUG] is user allowed?")
    print("    {}".format(is_user_allowed(dynamodb,event,username)))
    if 0 in response['Items']:
        print("[DEBUG] token from dynamo is")
        print('    {}'.format(response['Items'][0].get('token')))
    else:
      print('[DEBUG] dynamo db request gave no items')
    print("[DEBUG] token from query string is")
    print('    {}'.format(token))

  if response.get('Items'):
    # this is hard coded to the role used for the lambda execution
    # if deployed to a new account this should either be an env var or 
    # chagned in code
    #principal = 'arn:aws:iam::141147486306:role/bad-date'
    if response['Items'][0].get('token') == token and response['Items'][0].get('token') is not None:
      if is_user_allowed(dynamodb,event,username) and is_session_valid(response):
        if debug:
          print('authroization was successful')
        return generate_policy(username, 'Allow', 'arn:aws:execute-api:*:*:*')
   
  if debug:
    print('[DEBUG]authorization failed')
  raise Exception('Unauthorized')

def is_session_valid(dynamoResponse):
    return dynamoResponse['Items'][0].get('ttl') > calendar.timegm(time.gmtime())

def is_user_allowed(dynamo,event,username):
  if event.get('request') == '/login' or event.get('request') == '/register':
    # login and register are find
    return True
  if 'incident_id' not in event.get('queryStringParameters'):
    # if we're not dealing with a specific incident we're not concerned
    return True
  if event.get('request') == '/incident' and event.get('httpMethod') == 'POST':
    # anyone can create and incident
    return True
  if is_user_moderator(dynamo,username):
    # moderators can deal with any incident
    return True
  if is_user_owner(dynamo,username,event.get('queryStringParameters').get('incident_id')):
    # the owner can deal with the incident
    return True
    
  return False
  
def is_user_moderator(dynamo,username):
  userTable = dynamo.Table('user')
  userResponse = userTable.get_item(Key={'user_name': username})
  return userResponse.get('Item').get('role') == "moderator"
  
def is_user_owner(dynamo,username,incident):
  incidentTable = dynamo.Table('incident_report')
  incidentResponse = incidentTable.get_item(Key={'incident_id': incident})
  return incidentResponse.get('Item').get('user_name') == username

def generate_policy(principalId, effect, resource):
  authResponse = {
    'principalId': principalId,
    'policyDocument': {
      'Version': '2012-10-17',
      'Statement': [{
        'Action': 'execute-api:Invoke',
        'Effect': effect,
        'Resource': resource
      }]
    }
  }
  return authResponse


if __name__ == '__main__':
  os.environ['DEBUG'] = '1'
  lambda_handler({'queryStringParameters': {'username' : 'barkbark', 
                                            'password' : '1234567', 
                                            'authorization' : 'd5050cd0-8e89-4061-b815-1f972b7aa5a3'},
                  'username' : 'jacob-test', 
                  'password' : '1234567', 
                  'token' : 'd5050cd0-8e89-4061-b815-1f972b7aa5a3'}, {})
