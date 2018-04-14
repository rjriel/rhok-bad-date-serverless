import boto3
import os
import hashlib
import uuid
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
  hashed_passwd = hash_password(event['password'])
  dynamodb = boto3.resource('dynamodb', region_name='ca-central-1')
  table = dynamodb.Table('user')
  response = table.query(
    KeyConditionExpression=Key('username').eq(event['name'])
  )
  if len(response):
    if response['Items'][0]['password'] == hashed_passwd:
      token = str(uuid.uuid4())
      token_table = dynamodb.Table('token')
      token_table.put_item(Item={'username': event['name'], 'token': token, 'ttl': 3600 })
      return token
    else:
      return False
  else:
    return False

def hash_password(passwd):
  passwd_hash = hashlib.sha256()
  passwd_hash.update(passwd.encode('utf-8'))
  return passwd_hash.hexdigest()
