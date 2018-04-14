import boto3
import hashlib
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
      return True
    else:
      return False
  else:
    return False

def hash_password(passwd):
  passwd_hash = hashlib.sha256()
  passwd_hash.update(passwd.encode('utf-8'))
  return passwd_hash.hexdigest()
