#/usr/bin/python3

import boto3
import hashlib
from uuid import uuid4
import os

def hash_password(passwd):
  passwd_hash = hashlib.sha256()
  passwd_hash.update(passwd.encode('utf-8'))
  return passwd_hash.hexdigest()

def create_user(client, event):
  passwd = hash_password(event['password'])
  client.put_item(TableName='user', Item={'username' : {'S' : event['name']},
                      'password' : {'S' : passwd},
                      'role' : {'S' : 'submitter'}
  })
  

def user_exists(client, username):
    response = client.get_item(TableName='user',
        Key={'username' : {'S': username}})
    
    if not 'Item' in response:
      #the user does not exist
      return False
    else:
      #the User does exist
      return True

  
def lambda_handler(event, ctx):
  #gross, find a way to not hard code that 
  dynamo_client = boto3.client('dynamodb')
  if not  user_exists(dynamo_client, event['name']):
    create_user(dynamo_client, event)
    return { 'success': True }
  else:
    return { 'success': False, 'message': "Username already exists" }