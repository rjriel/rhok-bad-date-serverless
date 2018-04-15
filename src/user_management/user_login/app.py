import boto3
import os
import hashlib
import uuid
import calendar
import time
from decimal import Decimal
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
  debug = os.getenv('DEBUG') is '1'
  hashed_passwd = hash_password(event['password'])
  dynamodb = boto3.resource('dynamodb', region_name='ca-central-1')
  table = dynamodb.Table(os.getenv('USER_TABLE', 'user'))
  username =  event['name']
  response = table.query(
    KeyConditionExpression=Key('user_name').eq(username)
  )
  
  if response.get('Items'):
    if response['Items'][0].get('password') == hashed_passwd:
      ttl = calendar.timegm(time.gmtime()) + (60 * Decimal(os.getenv('MINUTES_TO_LIVE', '60')))
      token = str(uuid.uuid4())
      token_table = dynamodb.Table('token')
      token_table.put_item(Item={'username': username,
                                'token': token,
                                'ttl': ttl})
      if debug:
        print(token)
      return token

    else:
      if debug:
        print(False)
      return False
  
  if debug:
    print(False)
  return False

def hash_password(passwd):
  passwd_hash = hashlib.sha256()
  passwd_hash.update(passwd.encode('utf-8'))
  return passwd_hash.hexdigest()

# testing hook
if __name__ == '__main__':
  os.environ['MINUTES_TO_LIVE'] = '0.5'
  os.environ['DEBUG'] = '1'
  lambda_handler({'name' : 'jacob-test', 'password' : '1234567'}, {})

